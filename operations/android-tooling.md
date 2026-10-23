# Android tools and reverse-engineering recovery

Host additions verified 2026-10-23; see the current inventory below. Older examples remain historical unless explicitly rechecked. Use [workstation recovery](workstation-recovery.md) for backups and source setup. Commands below are templates: set paths explicitly and inspect existing destinations before replacing anything.

[Source/tool verification record](../evidence/source-tools-20261023.json).

## Current verified analysis tools

| Tool | Installed version / location | Check |
| --- | --- | --- |
| JADX | 1.5.6, `~/tools/jadx-1.5.6` | `jadx --version` |
| Ghidra | 12.2, `~/tools/ghidra_12.2_PUBLIC` | Headless usage starts |
| Apktool | Ubuntu package 2.7.0 | Version command passes |
| APK signer | Ubuntu package 35.0.2-1 | `apksigner version` passes |
| aapt | Ubuntu package 14 beta | Version command passes |
| TShark | 4.6.4 | Version command passes; no capture started |
| Binwalk | 2.4.3 | Help command passes; no extraction started |
| LLVM tools | Checkout `llvm-binutils-stable` | `llvm-objdump --version` passes |

Official JADX/Ghidra release ZIP SHA-256 values matched the GitHub release asset digests. User links live in `~/.local/bin`; open a fresh shell if PATH needs refreshing. Ghidra 12.2 requires JDK 25; its own `support/launch.properties` selects `~/evo/prebuilts/jdk/jdk25/linux-x86`. Revisit that path if the checkout moves. No global Java/compiler replacement was made. Ubuntu-packaged Apktool may lag modern resource formats; use the checkout's aapt2/build tools for ROM resources, not the distro aapt as a replacement. A version/usage check is not a decompilation or device test.

The [Leanrea skill](../.agents/skills/leanrea/SKILL.md) is available in Codex user skills and this workhub; [license/provenance](../.agents/skills/leanrea/PROVENANCE.md). Use the installed Android QA/performance skills for emulator/device evidence, the kernel skill only for kernel/driver work, and Review for requested reviews. These existing plugins need no duplicate install.

## Context7 and tool selection

Context7 is an on-demand documentation service, not a repository or skill catalogue. Native tools are `mcp__context7__resolve_library_id` and `mcp__context7__query_docs`; connector equivalents may also be present. Resolve once per library, then reuse the ID and a supported major-version scope. This check resolved JADX to `/skylot/jadx`; one query covered the 1.5 runtime/version command. The unversioned result is not a pinned 1.5 documentation snapshot; release metadata and local binary checks establish the installed version. Send no private code, credentials or device logs to documentation services.

Select skills by task and explicitly reread their bodies after compaction. [Resume entrypoint](../.agents/skills/alioth-resume/SKILL.md) restores only the required topic. Tool availability does not establish installation or successful runtime acceptance.

## Build environment

```bash
export ANDROID_ROOT="$HOME/evo"
cd "$ANDROID_ROOT"
source build/envsetup.sh
lunch
```

Choose the product/release/**user** combination offered by that checkout. Do not start a build merely to restore tools.

For this checkout preserve `lineage_alioth-cp2a-user`. Full ROM builds require
current authorization. The maintainer's release workflow is `. build/envsetup.sh
&& lunch lineage_alioth-cp2a-user && m installclean && m evolution`; development
and fix rebuilds omit `m installclean`. Do not clean output on every iteration.
Use `repo sync --force-sync -j50` only for authorized sync. Keep build parallelism
separate: the verified full build used `NINJA_ARGS="--local_jobs 8 -k 0"` and
`NINJA_HIGHMEM_NUM_JOBS=2`. Inspect actual graph/resources; module requests can
expand into core dependencies. Pause unauthorized expansion rather than assuming
a dry-run count bounds the real work.

The working tree supplies build JDK/toolchains. Do not change global Java or compiler symlinks to make an analysis tool start. For haptics-only builds, after an appropriate user lunch, the production target is `android.hardware.vibrator-service.xiaomi_aw8697`. The old device-test target was removed; do not request it from the current tree. A target build still needs source/build prerequisites and authorization; it does not validate a complete image.

## Android Clang and LLVM

Recorded October 4 haptics work used r596125 for the HAL and r563880c for kernel objects. Determine the compiler from the current build configuration or recorded compiler command; directory ordering is not evidence of the selected compiler.

```bash
export ANDROID_ROOT="$HOME/evo"
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

## Ghidra and APK analysis

Use the current installed versions listed above. Historical Ghidra 12.1.3/JADX examples are superseded. Official distributions and setup references: [Ghidra releases](https://github.com/NationalSecurityAgency/ghidra/releases), [JADX releases](https://github.com/skylot/jadx/releases), [Ghidra setup](https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md).

```bash
jadx --version
apktool --version
apksigner version
ghidra-headless
```

Analyze only copies in a new private directory. Do not publish proprietary APKs, ELF files, credentials or extracted personal data. Copy SQLite WAL companions before opening a database read-only. Decompiler output is a hypothesis: verify ABI, relocations, callers and instruction bytes against the exact binary. Headless startup is not a completed decompilation test. Keep saved projects before version upgrades.

## ADB, fastboot and root boundary

October 14 native-recovery work used Windows `D:/platform-tools/adb.exe` and
`fastboot.exe`; WSL invokes the same Windows owner. A large transfer failure was
recovered with a hash-verified local Windows image and `fastboot -S 32M`.
Preserve the full image/AVB footer; do not truncate padded images. Verify the actual
bootloader, product and slot first. This is not a universal USB-driver/kernel fix.
If Windows sees an ADB interface but no transport, restarting the same Windows
ADB server recovered it. Secure shell authorization is separate.


October 9: Linux `/usr/bin/adb` and `/usr/bin/fastboot` exist; `~/bin/adb` is absent. A historical haptics session used that wrapper, so do not infer current server ownership from it. Inspect `command -v adb` and any wrapper before choosing a server. Windows Platform Tools can instead own the USB device. Choose one owner; competing servers or USB passthrough often explain an empty device list. Set an explicit private path to Windows `adb.exe` when calling it from WSL. After reinstall, accept the on-phone debugging authorization; do not publish its serial.

The temporary haptics test also showed that a bind from a nosuid data mount can prevent a vendor HAL from starting. Its [tested deployment record](../evidence/haptics/2026-09-30.md#temporary-deployment-and-recovery) used an isolated executable tmpfs; do not weaken SELinux or global mount flags to work around it.

For native Linux USB access, follow [Microsoft usbipd guidance](https://learn.microsoft.com/en-us/windows/wsl/connect-usb): identify the bus with `usbipd list`, bind as administrator, then `usbipd attach --wsl --busid <bus-id>`. This removes the device from ordinary Windows ownership until detached. Recheck `adb devices -l`; fastboot is a separate USB mode and may need reattachment. Avoid exposing the ADB server on the network merely to bridge WSL.

Use `adb shell getprop ro.build.fingerprint`, `uname`, hashes and service state to identify the installed build before interpreting logs. Root permits research and temporary deployment; production changes belong in source, DAC/SELinux, init and build integration. Magisk bind mounts are temporary and can mask packaged files. Do not flash a stale `out/` image; verify hash, target device, partition/slot and authorization first.

## Reference data

For source indexing, use the dedicated [repoindex guide](repoindex.md). repoindex is unrelated to Android Repo or Gerrit repopick.

Reference locations: `~/miui/out` (Alioth stock), `~/miui/decompiled/jadx-frameworks`, `~/references_code/miui_proprietary_cpp`, `~/munch/out`, `~/myron/out`, `~/oneplus9r/out`, `~/alioth-r-oss`, `~/kernel_devicetree_alioth-r-oss`. These are optional local conventions, not files hosted by this knowledge repo. Preserve firmware version/hashes with private dump backups. Public reference code is indexed in the source map. Reacquire only a needed artifact from its verified source if a backup is missing; do not silently substitute a newer OEM dump.

## Host utility setup

For missing search, JSON, Python and shell-check tools on Windows/Ubuntu, use
[Host tooling](host-tooling.md). Inventory first and keep Python tools isolated.

## Recorded haptics tools

October 4: `~/tools/android-ndk-r30` compiled the renderer. HAL checks used
exact vendor flags/r596125 and isolated `out/haptics-validation/` outputs;
normal ROM configuration was preserved. [Scope](../evidence/haptics/2026-10-04.md).
