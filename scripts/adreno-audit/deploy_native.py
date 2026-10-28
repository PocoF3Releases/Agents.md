from pathlib import Path
import os,subprocess
P=Path(__file__).parent;A=os.environ.get('ADB','/mnt/d/platform-tools/adb.exe')
serial_args=['-s',os.environ['ANDROID_SERIAL']] if os.environ.get('ANDROID_SERIAL') else []
for bits in (64,32):
 f=P/f'gpu-probe{bits}';assert f.is_file(),'Build native probes first'
 w=subprocess.check_output(['wslpath','-w',str(f)],text=True).strip()
 subprocess.run([A,*serial_args,'push',w,f'/data/local/tmp/codex-gpu-probe{bits}'],check=True)
 subprocess.run([A,*serial_args,'shell',f'chmod 755 /data/local/tmp/codex-gpu-probe{bits}'],check=True)
