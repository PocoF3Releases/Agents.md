import os
from pathlib import Path
import subprocess,time,json,hashlib
P=Path(__file__).parent;A=os.environ.get('ADB','/mnt/d/platform-tools/adb.exe')
serial_args=['-s',os.environ['ANDROID_SERIAL']] if os.environ.get('ANDROID_SERIAL') else []
import os
label=os.environ.get('GPU_AUDIT_RUN_LABEL','')
def adb(*args,timeout=60):
 r=subprocess.run([A,*serial_args,*args],capture_output=True,text=True,timeout=timeout);r.check_returncode();return r.stdout.replace('\r','')
for bits,apk in [(64,'gpu-audit.apk'),(32,'gpu-audit32.apk')]:
 expected=hashlib.sha256((P/apk).read_bytes()).hexdigest()
 def installed_matches():
  r=subprocess.run([A,*serial_args,'shell','pm path org.pocof3.gpuaudit'],capture_output=True,text=True,timeout=15)
  if r.returncode==1 and not r.stdout.strip() and not r.stderr.strip():return False
  r.check_returncode();path=r.stdout.strip().removeprefix('package:')
  assert path.startswith('/data/app/') and '\n' not in path,'Unexpected installed APK path'
  return adb('shell','sha256sum '+path).split()[0]==expected
 if not installed_matches():
  w=subprocess.check_output(['wslpath','-w',str(P/apk)],text=True).strip()
  try:print(adb('install','-r','--no-streaming',w,timeout=30),flush=True)
  except subprocess.TimeoutExpired:print('Install client timed out; verifying committed APK hash before any test',flush=True)
  for retry in range(15):
   if installed_matches():break
   time.sleep(1)
  assert installed_matches(),'Expected APK was not installed; no test result accepted'
 print('Installed APK SHA256 matches expected ABI '+str(bits),flush=True)
 adb('shell','input keyevent KEYCODE_WAKEUP');adb('shell','wm dismiss-keyguard')
 assert 'mWakefulness=Awake' in adb('shell','dumpsys power'),'Screen must be awake for window presentation tests'
 for i in range(1,4):
  adb('shell','am force-stop org.pocof3.gpuaudit')
  adb('shell','su -c "rm -f /data/user/0/org.pocof3.gpuaudit/files/result.txt"')
  adb('shell','am start -W -n org.pocof3.gpuaudit/.MainActivity')
  text=''
  for j in range(20):
   text=adb('shell','su -c "cat /data/user/0/org.pocof3.gpuaudit/files/result.txt"')
   if 'SUMMARY_WINDOW' in text:break
   time.sleep(1)
  (P/f'{label}app{bits}-run{i}.txt').write_text(text)
  assert 'SUMMARY\tpass=62 fail=0' in text and 'SUMMARY_WINDOW\tpass=6 fail=0' in text,text[-1500:]
  exe=adb('shell','su -c "readlink /proc/$(pidof org.pocof3.gpuaudit)/exe"').strip()
  assert exe.endswith('app_process'+str(bits)),exe
  print(f'app ABI {bits}, run {i}: 62 native + 6 window checks PASS, {exe}',flush=True)
 (P/f'{label}app{bits}-final-maps.txt').write_text(adb('shell','su -c "cat /proc/$(pidof org.pocof3.gpuaudit)/maps"'))
 domain=adb('shell','ps -AZ | grep org.pocof3.gpuaudit')
 assert 'u:r:untrusted_app' in domain,'Unexpected SELinux domain; do not claim ordinary app coverage'
 (P/f'{label}app{bits}-final-domain.txt').write_text(domain)
