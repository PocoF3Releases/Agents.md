from pathlib import Path
import os,subprocess,tempfile,zipfile
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent
J=R/'prebuilts/jdk/jdk21/linux-x86';jar=R/'prebuilts/sdk/current/public/android.jar';env=os.environ.copy();env['JAVA_HOME']=str(J);env['PATH']=str(J/'bin')+':'+env['PATH']
with tempfile.TemporaryDirectory(prefix='clipcheck-build-') as tmp:
 B=Path(tmp);(B/'classes').mkdir();(B/'dex').mkdir()
 subprocess.run([str(J/'bin/javac'),'--release','11','-cp',str(jar),'-d',str(B/'classes'),str(P/'src/ClipCheck.java')],env=env,check=True)
 subprocess.run([str(J/'bin/java'),'-cp',str(R/'prebuilts/r8/r8.jar'),'com.android.tools.r8.D8','--lib',str(jar),'--min-api','31','--output',str(B/'dex'),*map(str,(B/'classes').rglob('*.class'))],env=env,check=True)
 with zipfile.ZipFile(P/'clipcheck.jar','w') as z:z.write(B/'dex/classes.dex','classes.dex')
