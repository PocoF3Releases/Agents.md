from pathlib import Path
import os,subprocess,tempfile
R=Path(os.environ.get('ANDROID_BUILD_TOP',str(Path.home()/'evo')));P=Path(__file__).parent
C=R/'prebuilts/clang/host/linux-x86/clang-r584948b/bin';S=R/'out/soong/ndk/sysroot';CRT=R/'out/soong/.intermediates/bionic/libc';V='android_arm64_armv8-2a-dotprod_cortex-a76';T='aarch64-linux-android'
subprocess.run([str(C/'clang'),str(CRT/'crtbegin_dynamic'/V/'crtbegin_dynamic.o'),'--target=aarch64-linux-android37','--sysroot='+str(S),'-isystem',str(S/'usr/include'/T),'-O2','-Wall','-Wextra','-Werror','-fPIE','-nostdlib',str(P/'src/storage-canary.c'),'-L'+str(S/'usr/lib'/T/'37'),'-lc',str(CRT/'crtend_android'/V/'crtend_android.o'),'-pie','-o',str(P/'storage-canary')],check=True)
# Read the extractor as Python source without leaving bytecode in the device tree.
ns={};f=R/'device/xiaomi/alioth/camera_session_fixup.py';exec(compile(f.read_text(),str(f),'exec'),ns)
with tempfile.TemporaryDirectory(prefix='camera-guard-build-') as tmp:
 B=Path(tmp);(B/'session-create-guard.bin').write_bytes(ns['PAYLOAD'])
 subprocess.run([str(C/'clang'),'--target=aarch64-linux-gnu','-c',str(P/'src/guard-regression.S'),'-o',str(B/'guard.o')],cwd=B,check=True)
 subprocess.run([str(C/'ld.lld'),'-T',str(P/'src/guard-regression.ld'),str(B/'guard.o'),'-o',str(P/'guard-regression')],check=True)
