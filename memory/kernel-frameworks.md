# Platform: device trees, kernel, NFC and build

## Ownership and source

Target: POCO F3 / alioth, SM8250/Kona / Snapdragon 870-class hardware; Android 17 focus with separately checked Android 16 backports. [The source map](repositories/TRACKED_HEADS.yaml) owns observed branches/heads; old uploaded-archive heads are not current checkout instructions.

`device/xiaomi/alioth/BoardConfig.mk` includes common BoardConfigCommon.mk. Its device.mk inherits common kona.mk, includes camera/miuicamera.mk and inherits vendor/xiaomi/alioth. Common kona.mk packages XiaomiParts and inherits vendor/xiaomi/sm8250-common. Camera integration inherits vendor/xiaomi/camera. Both camera delivery trees remain mandatory. Alioth-specific configuration belongs in alioth; shared init/audio/media/SELinux and Parts belong in sm8250-common. Standalone hardware/xiaomi owns reusable Xiaomi/Dolby integration.

An uploaded full-Git ZIP is usable only when supplied in the current environment. Inspect status and remote divergence; restore ZIP-lost executable bits and symlinks without discarding edits. The known common `.clang-format` target is `../../../build/soong/scripts/system-clang-format`. Do not commit extraction damage or reset to an old snapshot automatically. [Original workspace evidence](../archive/2026-09-26/memory/device-tree-workspace.md).

## Rootdir and compatibility lessons

Compare generic init behavior with the applicable AOSP source, but check vendor-specific writes against Alioth's actual kernel, packaged binaries and init ownership. `CONFIG_SCHED_TUNE=y` made schedtune a real capability: remove duplicate writes, not the entire mechanism merely because it is old. Likewise preserve valid cpuctl/cpuset/blkio/task-profile behavior.

Recorded cleanup removed unreachable non-Kona branches, duplicate camera stune writes and unshipped irqbalance variants, qlogd, VM BMS, LKCore, qseeproxydaemon, poweroffhandler, HBTP, QVOP, battery_monitor, profiler_daemon and hostapd FST services. Kona irqbalance, density/GPU/ATFWD/DRM handling and real power_off_alarm/ATFWD/dumpstate paths were retained. qcrild replaced the nonexistent rild fallback. Logical AVB first-stage mounting replaced obsolete charger physical-system mounting; charger mode no longer forces ADB. These are source-inspected historical changes, not permission to resume the old continuation list. [Exact 17-change evidence](../archive/2026-09-26/today/2026-09-23-sm8250-rootdir-android17-modernization.md).

Other retained platform lessons: remove dead Android resource overlays, not supported vendor functionality; avoid obsolete memory-cgroup writes on cgroup v2; set ZRAM page-cluster through init; preserve RAM-tier ART defaults and haptic-resonance labeling; keep camera/DisplayConfig/gralloc/C2D compatibility narrowly scoped. Historical SurfaceFlinger legacy VDS pacing is not guaranteed present after source resync. Verify actual source before using its property.

Early Bionic loader `thread_local`/PT_TLS changes caused Android and recovery failure. Keep state caller/local-owned unless that loader environment supports TLS. Failure before both systems reach userspace is not automatically a kernel problem. Kernel 4.19/CIP, dimming interpolation and DS4/composite Bluetooth work remain separate from generic framework changes.

## NFC

The SNxxx client in `snxxx/halimpl/hal/phNxpNciHal.cc` must snapshot its queue handle before the receive loop. Fix `8be75516d6d3cfff3a95ca2f249f0b36ceededb9` preserves upstream UAF mitigation `ad16c5c95a8613cc7ef8890c243068633e8d2f83`: global ID is cleared before timer cleanup while the running thread uses its saved handle through close completion and join. Do not revert the security fix or widen to PN8x/SNxxx v2 without evidence. Validation: [V-NFC](validation.md#v-nfc).

## Build policy

Recorded Android 17 choice: `PRODUCT_DEX_PREOPT_DEFAULT_COMPILER_FILTER := speed` for unprofiled preinstalled code, preserving profile-guided behavior where available. Do not globally force `everything` or restore obsolete `DEX_PREOPT_DEFAULT := generate-vdex-and-image` without current justification. Separate 6/8 GB device RAM tiers from host build resources. An unrestricted build previously coincided with a host crash; `-j4` was the conservative isolated-check starting point, not a measured universal optimum. Builds still require explicit authorization. [Original build record](../archive/2026-09-26/memory/android-build-optimization.md).

## Historical work, not an active backlog

Turnip: Endfield loaded stock `vulkan.adreno.so` despite package opt-in. Shell-domain R8 success did not prove app-domain selection; investigate GraphicsEnvironment / `getPackageInfo(MATCH_SYSTEM_ONLY|GET_META_DATA)` identity/filtering before repeating force-queryable workarounds. DeviceAsWebcam product gating was recorded uncommitted/unvalidated; kernel/HAL presence was not host UVC proof. DS4 composite-input repair required re-enabling an initially suppressed touchpad when gamepad/joystick interfaces joined. Current inclusion of these historical items is unestablished. [Removed raw-import boundary](../archive/PRIVACY.md).

Latest recorded boot outcomes, unresolved Cirrus/ultrasound behavior and the later libmeminfo correction are owned by [V-BOOT](validation.md#v-boot) and [V-MEMINFO](validation.md#v-meminfo), not duplicated as current failures here.

## September 30 source reconciliation

The public libmeminfo fork remains available, but the inspected local checkout uses `Evolution-X/system_memory_libmeminfo`, detached at the source-map head. Its optional BPF iterator log-spam correction is present upstream. Do not restore a fork override just because it appears in an older ledger. Android 17 frameworks/base has independent high-FPS screen recording and blur suppression commits; inspect current upstream integration before replaying either.

Optional font work belongs to vendor/extras branch `aosp-17-oh-my-font`, with actual font assets rather than a build-time downloader. The local head differs from its published branch; reconcile before build, preserving local changes. It is not a default requirement for every build.

GPU donor-driver, Turnip and game-setting experiments were parked by the maintainer. No broadly validated Unity/Unreal optimization, F8 GPU-driver compatibility, frame-generation port or unlocked 120fps is established. Keep thermal protection intact. Experimental root modules are not production fixes or required recovery dependencies.

Standalone hardware/xiaomi fixes: cbb57f1 rejects invalid legacy sensor-list/poll results and propagates direct-channel errors; 30c28d4 initializes fingerprint pointers and cleans failed opens; a2cf3b4 replaces unsafe delayed-session references with weak references and idempotent close; 5e49959 initializes lockout state and stops authentication during lockout. Recorded validation is target syntax compilation (sensor arm/arm64) and diff checks, not device replacement or biometric certification.
