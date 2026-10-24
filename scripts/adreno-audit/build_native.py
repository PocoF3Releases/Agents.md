import os
from pathlib import Path
import subprocess,shutil
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent;S=R/'out/soong/ndk/sysroot';C=R/'prebuilts/clang/host/linux-x86/clang-r584948b/bin/clang';crt=R/'out/soong/.intermediates/bionic/libc'
shutil.copy2(R/'kernel/xiaomi/sm8250/include/uapi/linux/msm_kgsl.h',P/'src/msm_kgsl.h')
for bits,target,triple,variant in [(64,'aarch64-linux-android37','aarch64-linux-android','android_arm64_armv8-2a-dotprod_cortex-a76'),(32,'armv7a-linux-androideabi37','arm-linux-androideabi','android_arm_armv8-2a_cortex-a76')]:
 base=[str(C),'--target='+target,'--sysroot='+str(S),'-isystem',str(S/'usr/include'/triple),'-I'+str(R/'libnativehelper/include_jni'),'-O2','-g','-Wall','-Wextra','-Werror','-fPIE','-fno-addrsig','-nostdlib',str(P/'src/probe.c'),'-L'+str(S/'usr/lib'/triple/'37'),'-lEGL','-lGLESv3','-lvulkan','-landroid','-lc','-lm','-ldl','-Wl,--no-undefined']
 begin=crt/'crtbegin_dynamic'/variant/'crtbegin_dynamic.o';end=crt/'crtend_android'/variant/'crtend_android.o'
 for name,args in [(f'gpu-probe{bits}',base[:1]+[str(begin)]+base[1:]+[str(end),'-pie']),(('libgpu_audit.so' if bits==64 else 'libgpu_audit32.so'),base+['-DAPP_PROBE','-fPIC','-shared'])]:
  r=subprocess.run(args+['-o',str(P/name)],capture_output=True,text=True);(P/(name+'.build.log')).write_text(r.stdout+r.stderr);print(name,r.returncode,r.stderr[:3500]);r.check_returncode()
