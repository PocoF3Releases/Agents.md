import os
from pathlib import Path
import os,subprocess,zipfile,tempfile,sys
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent
J=R/'prebuilts/jdk/jdk21/linux-x86';T=R/'prebuilts/sdk/tools/linux';jar=R/'prebuilts/sdk/current/public/android.jar'
package='org.lineageos.aperture.dev' if '--aux' in sys.argv else 'org.pocof3.hardwareaudit'
env=os.environ.copy();env['JAVA_HOME']=str(J);env['PATH']=str(J/'bin')+':'+env['PATH']
def run(args):subprocess.run([str(x) for x in args],env=env,check=True)
with tempfile.TemporaryDirectory(prefix='gpu-apk-',dir=P) as tmp:
 B=Path(tmp);classes=B/'classes';classes.mkdir();dex=B/'dex';dex.mkdir()
 source=B/'MainActivity.java';source.write_text((P/'src/MainActivity.java').read_text().replace('org.pocof3.hardwareaudit',package))
 manifest=B/'AndroidManifest.xml';manifest.write_text((P/'src/AndroidManifest.xml').read_text().replace('org.pocof3.hardwareaudit',package))
 run([J/'bin/javac','--release','11','-classpath',jar,'-d',classes,source])
 run([J/'bin/java','-cp',R/'prebuilts/r8/r8.jar','com.android.tools.r8.D8','--lib',jar,'--min-api','31','--output',dex,*classes.glob(package.replace('.','/')+'/*.class')])
 unsigned=B/'unsigned.apk'
 run([T/'bin/aapt2','link','--manifest',manifest,'-I',jar,'-o',unsigned])
 with zipfile.ZipFile(unsigned,'a',compression=zipfile.ZIP_DEFLATED) as z:z.write(dex/'classes.dex','classes.dex')
 run([J/'bin/java','-jar',T/'lib/apksigner.jar','sign','--key',R/'build/make/target/product/security/testkey.pk8','--cert',R/'build/make/target/product/security/testkey.x509.pem','--out',P/('hardware-aux.apk' if '--aux' in sys.argv else 'hardware-audit.apk'),unsigned])
 run([J/'bin/java','-jar',T/'lib/apksigner.jar','verify',P/('hardware-aux.apk' if '--aux' in sys.argv else 'hardware-audit.apk')])
