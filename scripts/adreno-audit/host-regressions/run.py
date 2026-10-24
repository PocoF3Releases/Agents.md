from pathlib import Path
import os,subprocess,tempfile,ctypes,re
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent;K=R/'kernel/xiaomi/sm8250/drivers/gpu/msm'
assert ctypes.sizeof(ctypes.c_long)==8 and ctypes.sizeof(ctypes.c_int)==4,'Fixtures model an ARM64 kernel, including 32-bit callers'
with tempfile.TemporaryDirectory(prefix='gpu-host-regressions-') as tmp:
 for name in ('baseline','actual-map-accounting','actual-dmabuf-accounting'):
  s=(P/(name+'.c')).read_text()
  if name=='actual-map-accounting':
   src=(K/'kgsl_mmu.c').read_text();a=src.index('int\nkgsl_mmu_map(');b=src.index('EXPORT_SYMBOL(kgsl_mmu_map);',a)
   start=re.search(r'\bint\s+kgsl_mmu_map\s*\(',s).start();end=start+re.search(r'\bint\s+main\s*\(',s[start:]).start();s=s[:start]+src[a:b]+s[end:]
  elif name=='actual-dmabuf-accounting':
   src=(K/'kgsl.c').read_text();a=src.index('static void add_dmabuf_list(');b=src.index('#ifdef CONFIG_DMA_SHARED_BUFFER',a)
   start=re.search(r'static\s+void\s+add_dmabuf_list\s*\(',s).start();end=start+re.search(r'\bint\s+main\s*\(',s[start:]).start();s=s[:start]+src[a:b]+s[end:]
  f=Path(tmp)/(name+'.c');f.write_text(s);exe=Path(tmp)/name
  subprocess.run(['cc','-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',str(exe)],check=True)
  r=subprocess.run([str(exe)],capture_output=True,text=True);print(name+'\n'+r.stdout)
  assert r.returncode==(1 if name=='baseline' else 0),r.stderr
print('Pinned baseline reproduced; current driver functions pass host regression fixtures')
