import os
import re
import os
from pathlib import Path
import subprocess,time,re,json,sys
from collections import Counter
P=Path(__file__).parent;A=os.environ.get('ADB','/mnt/d/platform-tools/adb.exe');label=sys.argv[1]
serial_args=['-s',os.environ['ANDROID_SERIAL']] if os.environ.get('ANDROID_SERIAL') else []
assert re.fullmatch(r'[A-Za-z0-9_-]{1,40}',label),'Use a simple trace label'
remote='/data/local/tmp/codex-deqp-'+label+'.qpa'
cmd='/data/local/tmp/codex-deqp64 --deqp-caselist-file=/data/local/tmp/codex-deqp-cases.txt --deqp-surface-type=pbuffer --deqp-surface-width=256 --deqp-surface-height=256 --deqp-gl-config-name=rgba8888d24s8ms0 --deqp-watchdog=enable --deqp-log-images=disable --deqp-log-shader-sources=disable --deqp-archive-dir=/data/local/tmp/codex-deqp-data --deqp-log-filename='+remote
start=time.monotonic();r=subprocess.run([A,*serial_args,'shell',cmd],capture_output=True,text=True,timeout=600);(P/(label+'-deqp-console.txt')).write_text(r.stdout+r.stderr)
q=subprocess.run([A,*serial_args,'exec-out','cat',remote],capture_output=True,timeout=30);q.check_returncode();(P/(label+'-deqp.qpa')).write_bytes(q.stdout)
text=q.stdout.decode(errors='replace');results=re.findall(r'<TestCaseResult CasePath="([^"]+)".*?<Result StatusCode="([^"]+)"[^>]*>(.*?)</Result>',text,re.S)
expected=len((P/'deqp-selected-cases.txt').read_text().splitlines());summary={'exit':r.returncode,'seconds':round(time.monotonic()-start,1),'executed':len(results),'expected':expected,'statuses':dict(Counter(status for _,status,_ in results)),'failures':[{'case':case,'status':status,'detail':re.sub('<.*?>','',msg)} for case,status,msg in results if status not in ['Pass','NotSupported','QualityWarning','CompatibilityWarning']]}
(P/(label+'-deqp-results.json')).write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2)[:4000]);assert len(results)==expected and not summary['failures'] and r.returncode==0
