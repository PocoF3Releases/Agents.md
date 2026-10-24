from pathlib import Path
import subprocess,re,sys
import os,tempfile
P=Path(__file__).parent; K=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')))/'kernel/xiaomi/sm8250'
T=tempfile.TemporaryDirectory(prefix='kgsl-global-lifetime-');O=Path(T.name)
def fn(src,name):
 a=re.search(r'^(?:static )?(?:int|void)\s+'+name+r'\(',src,re.M).start()
 start=src.index('{',a);depth=1;i=start+1
 while depth:
  depth+=(src[i]=='{')-(src[i]=='}');i+=1
 return src[a:i]
mmu=(K/'drivers/gpu/msm/kgsl_mmu.c').read_text();iommu=(K/'drivers/gpu/msm/kgsl_iommu.c').read_text()
if len(sys.argv)>1:iommu=subprocess.check_output(['git','show',sys.argv[1]+':drivers/gpu/msm/kgsl_iommu.c'],cwd=K,text=True)
s=(P/'global-lifetime-template.c').read_text().replace('/* DRIVER_FUNCTIONS */','\n'.join([fn(mmu,'kgsl_mmu_map'),fn(mmu,'kgsl_mmu_unmap'),fn(iommu,'kgsl_iommu_remove_global')]))
(O/'global-lifetime.c').write_text(s)
subprocess.run(['cc','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(O/'global-lifetime.c'),'-o',str(O/'global-lifetime')],check=True)
r=subprocess.run([str(O/'global-lifetime')],capture_output=True,text=True);print(r.stdout);raise SystemExit(r.returncode)
