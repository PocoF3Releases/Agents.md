# Android tools and reverse-engineering recovery

Inventory checked 2026-09-30. Use [workstation recovery](workstation-recovery.md) for backups and source setup. Commands below are templates: set paths explicitly and inspect existing destinations before replacing anything.

## Build environment

```bash
export ANDROID_ROOT="$HOME/evo17"
cd "$ANDROID_ROOT"
source build/envsetup.sh
lunch
```

Choose the product/release/**user** combination offered by that checkout. Do not start a build merely to restore tools.

The working tree supplies build JDK/toolchains. Do not change global Java or compiler symlinks to make an analysis tool start. For haptics-only builds, after an appropriate user lunch, the production target is `android.hardware.vibrator-service.xiaomi_aw8697`. The old device-test target was removed; do not request it from the current tree. A target build still needs source/build prerequisites and authorization; it does not validate a complete image.

## Android Clang and LLVM

The inspected tree contains r547379, r563880c, r584948, r584948b and r596125. Latest haptics work used r596125 for the HAL and r563880c for kernel objects. Determine the compiler from the current build configuration or recorded compiler command; directory ordering is not evidence of the selected compiler.

```bash
export ANDROID_ROOT="$HOME/evo17"
export CLANG_REV=clang-r596125
export LLVM_BIN="$ANDROID_ROOT/prebuilts/clang/host/linux-x86/$CLANG_REV/bin"
test -x "$LLVM_BIN/llvm-readelf" || exit 1
"$LLVM_BIN/clang" --version
"$LLVM_BIN/llvm-readelf" -h -d -n path/to/library.so
"$LLVM_BIN/llvm-nm" -D --defined-only path/to/library.so
"$LLVM_BIN/llvm-objdump" -d --demangle path/to/library.so
sha256sum path/to/library.so
```

For convenient relinking, keep these exports in a private, reviewable environment file and source it only in analysis shells. Change ANDROID_ROOT/CLANG_REV after reinstall. Prefer explicit tool paths; if creating aliases or symlinks, use a dedicated user-owned bin directory and replace only links you own. Never overwrite `/usr/bin/clang`, Android prebuilt contents or an existing real directory. Ghidra does not require replacing its bundled decompiler with Android LLVM.

## Ghidra

Observed installation: `~/tools/ghidra_12.1.3_PUBLIC`, with `~/tools/ghidra` pointing to it. Its `Ghidra/application.properties` requires JDK 21 minimum; OpenJDK 21 was available. Future releases may require a different JDK: read the chosen release's Getting Started/application properties rather than applying the current development branch's requirement blindly.

Download the compiled distribution ZIP from [official Ghidra releases](https://github.com/NationalSecurityAgency/ghidra/releases), verify the publisher's digest when available, and extract into a new versioned directory under `~/tools`. Do not download the source archive expecting a ready binary. Restore custom scripts/projects separately from private backup. Keep the old project backup before accepting an upgrade conversion. [Official setup guide](https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md).

```bash
export GHIDRA_HOME="$HOME/tools/ghidra_12.1.3_PUBLIC"
export GHIDRA_JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
# Confirm both paths exist before using them.
JAVA_HOME="$GHIDRA_JAVA_HOME" "$GHIDRA_HOME/ghidraRun"
# Headless example; a new project avoids altering the original analysis:
mkdir -p "$HOME/analysis/ghidra"
JAVA_HOME="$GHIDRA_JAVA_HOME" "$GHIDRA_HOME/support/analyzeHeadless"   "$HOME/analysis/ghidra" StockAudit -import /absolute/path/library.so
```

WSLg normally supplies Linux GUI integration; headless analysis needs no display. Recreate the optional `~/tools/ghidra` link only after confirming that its destination is absent or an owned symlink. Use `-scriptPath` / `-postScript` only for scripts actually restored and reviewed. A decompiled C listing is a hypothesis: check AArch64 disassembly, relocations, callers and exact ELF identity before changing ABI or patch bytes.

## JADX, Apktool and ELF tools

Observed JADX: `~/tools/jadx/bin/jadx`, version 1.5.6, not on PATH. Observed Apktool: `/usr/local/bin/apktool`, 3.0.3. Restore from [JADX releases](https://github.com/skylot/jadx/releases) and [Apktool installation](https://apktool.org/docs/install); use versioned folders and their Java requirements. Install the Apktool wrapper and matching JAR together. Verify `--version` / `--help` before reusing old arguments.

```bash
"$HOME/tools/jadx/bin/jadx" --version
"$HOME/tools/jadx/bin/jadx" -d "$HOME/analysis/app-jadx" /absolute/path/app.apk
apktool --version
apktool d /absolute/path/app.apk -o "$HOME/analysis/app-smali"
```

Use a fresh output directory to preserve previous edits. JADX is for reading; patch actual smali/resources and rebuild with Apktool when authorized. Retrieve `aapt2`, `zipalign`, `apksigner` from Android SDK Build Tools or the checked-out build's declared host tools, not random binaries. Camera packaging previously used `zipalign -c -P 16 4`; follow its canonical delivery procedure and signature requirements. Camera remains finalized, so tool restoration is not permission to modify the APK.

Host utilities commonly needed: `git`, `git-lfs`, `python3`, `python3-venv`, `python3-yaml`, `ripgrep`, `unzip`, `zip`, `file`, `binutils`, `patchelf`, `ffmpeg`, `jq`, plus the build's declared dependencies. Record package versions for reproducibility. GitHub CLI was not on WSL PATH at this inspection; install via [official CLI instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) if needed, then authenticate interactively. Never put credentials in scripts or docs.

## ADB, fastboot and root boundary

Linux `/usr/bin/adb` and `/usr/bin/fastboot` exist in the inspected distro; the successful latest haptics session invoked `~/bin/adb`. Inspect `command -v adb` and any wrapper before choosing a server. Windows Platform Tools can instead own the USB device. Choose one owner; competing servers or USB passthrough often explain an empty device list. Set an explicit private path to Windows `adb.exe` when calling it from WSL. After reinstall, accept the on-phone debugging authorization; do not publish its serial.

The temporary haptics test also showed that a bind from a nosuid data mount can prevent a vendor HAL from starting. Its [tested deployment record](../evidence/haptics/2026-09-30.md#temporary-deployment-and-recovery) used an isolated executable tmpfs; do not weaken SELinux or global mount flags to work around it.

For native Linux USB access, follow [Microsoft usbipd guidance](https://learn.microsoft.com/en-us/windows/wsl/connect-usb): identify the bus with `usbipd list`, bind as administrator, then `usbipd attach --wsl --busid <bus-id>`. This removes the device from ordinary Windows ownership until detached. Recheck `adb devices -l`; fastboot is a separate USB mode and may need reattachment. Avoid exposing the ADB server on the network merely to bridge WSL.

Use `adb shell getprop ro.build.fingerprint`, `uname`, hashes and service state to identify the installed build before interpreting logs. Root permits research and temporary deployment; production changes belong in source, DAC/SELinux, init and build integration. Magisk bind mounts are temporary and can mask packaged files. Do not flash a stale `out/` image; verify hash, target device, partition/slot and authorization first.

## Reference data

For source indexing, use the dedicated [repoindex guide](repoindex.md). repoindex is unrelated to Android Repo or Gerrit repopick.

Common reference locations: `~/miui/out` (Alioth stock), `~/miui/decompiled/jadx-frameworks`, `~/references_code/miui_proprietary_cpp`, `~/munch/out`, `~/myron/out`, `~/oneplus9r/out`, `~/alioth-r-oss`, `~/kernel_devicetree_alioth-r-oss`. These are optional local conventions, not files hosted by this knowledge repo. Preserve firmware version/hashes with private dump backups. Public reference code is indexed in the source map. Reacquire only a needed artifact from its verified source if a backup is missing; do not silently substitute a newer OEM dump.
