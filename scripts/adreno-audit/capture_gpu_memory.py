import os
import re
import os
from pathlib import Path
import subprocess,time,sys
P=Path(__file__).parent;A=os.environ.get('ADB','/mnt/d/platform-tools/adb.exe');name=sys.argv[1]
serial_args=['-s',os.environ['ANDROID_SERIAL']] if os.environ.get('ANDROID_SERIAL') else []
assert re.fullmatch(r'[A-Za-z0-9_-]{1,40}',name),'Use a simple trace label'
def adb(*args,**kwargs):
 r=subprocess.run([A,*serial_args,*args],capture_output=True,**kwargs);r.check_returncode();return r.stdout
remote='/data/misc/perfetto-traces/codex-gpu-memory-'+name+'.pftrace'
p=subprocess.Popen([A,*serial_args,'shell','perfetto --txt -c - -o '+remote],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdin.write((P/'gpu-memory-trace.cfg').read_bytes());p.stdin.close();p.stdin=None
time.sleep(1)
adb('shell','am force-stop org.pocof3.gpuaudit',timeout=10);adb('shell','am start -W -n org.pocof3.gpuaudit/.MainActivity',timeout=15)
for i in range(3):adb('shell','/data/local/tmp/codex-gpu-probe64',timeout=15)
o,e=p.communicate(timeout=15);(P/(name+'-perfetto.log')).write_bytes(o+e)
if p.returncode:raise SystemExit('Perfetto capture failed '+(o+e).decode(errors='replace'))
trace=P/(name+'.pftrace');trace.write_bytes(adb('exec-out','su','-c','cat '+remote,timeout=15))
query="SELECT t.id,t.name,t.type,count(c.id) AS samples,min(c.value) AS minimum,max(c.value) AS maximum FROM counter_track t LEFT JOIN counter c ON c.track_id=t.id GROUP BY t.id,t.name,t.type;"
r=subprocess.run([str(P/'tools/trace_processor_shell'),str(trace),'-Q',query],capture_output=True,text=True,timeout=30);(P/(name+'-gpu-counters.csv')).write_text(r.stdout);(P/(name+'-trace-processor.log')).write_text(r.stderr);r.check_returncode();print(name,r.stdout[-2500:])
