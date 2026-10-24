import os
from pathlib import Path
import os,subprocess,zipfile,tempfile
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent
J=R/'prebuilts/jdk/jdk21/linux-x86';T=R/'prebuilts/sdk/tools/linux';jar=R/'prebuilts/sdk/current/public/android.jar'
env=os.environ.copy();env['JAVA_HOME']=str(J);env['PATH']=str(J/'bin')+':'+env['PATH']
def run(args):subprocess.run([str(x) for x in args],env=env,check=True)
with tempfile.TemporaryDirectory(prefix='gpu-apk-',dir=P) as tmp:
 B=Path(tmp);classes=B/'classes';classes.mkdir();dex=B/'dex';dex.mkdir()
 run([J/'bin/javac','--release','11','-classpath',jar,'-d',classes,P/'src/MainActivity.java'])
 run([J/'bin/java','-cp',R/'prebuilts/r8/r8.jar','com.android.tools.r8.D8','--lib',jar,'--min-api','31','--output',dex,*classes.glob('org/pocof3/gpuaudit/*.class')])
 for bits,abi,library,apk in [(64,'arm64-v8a','libgpu_audit.so','gpu-audit.apk'),(32,'armeabi-v7a','libgpu_audit32.so','gpu-audit32.apk')]:
  unsigned=B/('unsigned'+str(bits)+'.apk')
  run([T/'bin/aapt2','link','--manifest',P/'src/AndroidManifest.xml','-I',jar,'-o',unsigned])
  with zipfile.ZipFile(unsigned,'a',compression=zipfile.ZIP_DEFLATED) as z:
   z.write(dex/'classes.dex','classes.dex');z.write(P/library,'lib/'+abi+'/libgpu_audit.so')
  run([J/'bin/java','-jar',T/'lib/apksigner.jar','sign','--key',R/'build/make/target/product/security/testkey.pk8','--cert',R/'build/make/target/product/security/testkey.x509.pem','--out',P/apk,unsigned])
  run([J/'bin/java','-jar',T/'lib/apksigner.jar','verify',P/apk])
