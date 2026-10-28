"""Summarize observed KGSL request numbers; never execute an ioctl."""
from pathlib import Path
import argparse,os,re,json,collections
p=argparse.ArgumentParser();p.add_argument('traces',nargs='+',type=Path);p.add_argument('--tree',type=Path,default=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo'))));a=p.parse_args()
k=a.tree/'kernel/xiaomi/sm8250';header=(k/'include/uapi/linux/msm_kgsl.h').read_text().replace('\\\n','')
nums={name:int(nr,16) for name,nr in re.findall(r'#define\s+(IOCTL_KGSL_\w+)\s+_IO\w*\(KGSL_IOC_TYPE,\s*(0x[0-9a-fA-F]+)',header)}
dispatch={}
for file in ('kgsl_ioctl.c','adreno_ioctl.c'):
 source=(k/'drivers/gpu/msm'/file).read_text()
 entries=re.findall(r'KGSL_IOCTL_FUNC\((IOCTL_KGSL_\w+),\s*(\w+)\)',source)+re.findall(r'\{\s*(IOCTL_KGSL_\w+),\s*(\w+)\s*\}',source)
 for name,handler in entries:
  if name in nums:dispatch[nums[name]]={'name':name,'handler':handler,'table':file}
reports=[]
for trace in a.traces:
 calls=collections.Counter();errors=collections.Counter();sizes=collections.defaultdict(set)
 for line in trace.read_text().splitlines():
  if '/dev/kgsl-3d0' not in line:continue
  match=re.search(r'_IOC\(.*?, 0x9, (0x[0-9a-f]+), (0x[0-9a-f]+)\)',line)
  if not match:continue
  nr=int(match[1],16);calls[nr]+=1;sizes[nr].add(int(match[2],16))
  err=re.search(r'= -1 (\w+)',line)
  if err:errors[(nr,err[1])]+=1
 reports.append({'trace':trace.name,'observed_requests':sum(calls.values()),'distinct_numbers':len(calls),'calls':[{'nr':hex(n),'name':dispatch.get(n,{}).get('name','unclassified'),'count':count,'request_sizes':sorted(sizes[n])} for n,count in sorted(calls.items())],'errors':[{'nr':hex(n),'errno':err,'count':count} for (n,err),count in sorted(errors.items())],'unobserved_dispatch_entries':[dict(nr=hex(n),**entry) for n,entry in sorted(dispatch.items()) if n not in calls]})
print(json.dumps({'scope':'ioctl-number coverage from strace -f -yy -e trace=ioctl; not argument/branch coverage or proof every table entry is supported','dispatch_entries':len(dispatch),'reports':reports},indent=2))
