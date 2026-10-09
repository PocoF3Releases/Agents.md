# Platform: device trees, kernel, NFC and build

## Ownership and source

Target: POCO F3 / alioth, SM8250/Kona / Snapdragon 870-class hardware; Android 17 focus with separately checked Android 16 backports. [The source map](../state/repositories.yaml) owns observed branches/heads; old uploaded-archive heads are not current checkout instructions.

`device/xiaomi/alioth/BoardConfig.mk` includes common BoardConfigCommon.mk. Its device.mk inherits common kona.mk, includes camera/miuicamera.mk and inherits vendor/xiaomi/alioth. Common kona.mk packages XiaomiParts and inherits vendor/xiaomi/sm8250-common. Camera integration inherits vendor/xiaomi/camera. Both camera delivery trees remain mandatory. Alioth-specific configuration belongs in alioth; shared init/audio/media/SELinux and Parts belong in sm8250-common. Standalone hardware/xiaomi owns reusable Xiaomi/Dolby integration.

An uploaded full-Git ZIP is usable only when supplied in the current environment. Inspect status and remote divergence; restore ZIP-lost executable bits and symlinks without discarding edits. The known common `.clang-format` target is `../../../build/soong/scripts/system-clang-format`. Do not commit extraction damage or reset to an old snapshot automatically. [Original workspace evidence](kernel-frameworks.md).

## Rootdir and compatibility lessons

Compare generic init behavior with the applicable AOSP source, but check vendor-specific writes against Alioth's actual kernel, packaged binaries and init ownership. `CONFIG_SCHED_TUNE=y` made schedtune a real capability: remove duplicate writes, not the entire mechanism merely because it is old. Likewise preserve valid cpuctl/cpuset/blkio/task-profile behavior.

Recorded cleanup removed unreachable non-Kona branches, duplicate camera stune writes and unshipped irqbalance variants, qlogd, VM BMS, LKCore, qseeproxydaemon, poweroffhandler, HBTP, QVOP, battery_monitor, profiler_daemon and hostapd FST services. Kona irqbalance, density/GPU/ATFWD/DRM handling and real power_off_alarm/ATFWD/dumpstate paths were retained. qcrild replaced the nonexistent rild fallback. Logical AVB first-stage mounting replaced obsolete charger physical-system mounting; charger mode no longer forces ADB. These are source-inspected historical changes, not permission to resume the old continuation list. [Exact 17-change evidence](kernel-frameworks.md).

Other retained platform lessons: remove dead Android resource overlays, not supported vendor functionality; avoid obsolete memory-cgroup writes on cgroup v2; set ZRAM page-cluster through init; preserve RAM-tier ART defaults and haptic-resonance labeling; keep camera/DisplayConfig/gralloc/C2D compatibility narrowly scoped. Historical SurfaceFlinger legacy VDS pacing is not guaranteed present after source resync. Verify actual source before using its property.

Early Bionic loader `thread_local`/PT_TLS changes caused Android and recovery failure. Keep state caller/local-owned unless that loader environment supports TLS. Failure before both systems reach userspace is not automatically a kernel problem. Kernel 4.19/CIP, dimming interpolation and DS4/composite Bluetooth work remain separate from generic framework changes.

## NFC

Current SNxxx `05b56f4` snapshots the queue ID before its receive loop so teardown does not replace the handle used by that thread. Upstream `66ef2f3` reverted the earlier timer-teardown mitigation across HAL variants after reported hangs/logging/battery drain. The old instruction to preserve that mitigation is superseded; do not replay it blindly. September 22 device acceptance in [V-NFC](../state/validation.md#v-nfc) is historical, not a new test of this current combined tree.

## Build policy

Recorded Android 17 choice: `PRODUCT_DEX_PREOPT_DEFAULT_COMPILER_FILTER := speed` for unprofiled preinstalled code, preserving profile-guided behavior where available. Do not globally force `everything` or restore obsolete `DEX_PREOPT_DEFAULT := generate-vdex-and-image` without current justification. Separate 6/8 GB device RAM tiers from host build resources. An unrestricted build previously coincided with a host crash; `-j4` was the conservative isolated-check starting point, not a measured universal optimum. Builds still require explicit authorization. [Original build record](kernel-frameworks.md).

## Historical work, not an active backlog

Turnip: Endfield loaded stock `vulkan.adreno.so` despite package opt-in. Shell-domain R8 success did not prove app-domain selection; investigate GraphicsEnvironment / `getPackageInfo(MATCH_SYSTEM_ONLY|GET_META_DATA)` identity/filtering before repeating force-queryable workarounds. DeviceAsWebcam product gating was recorded uncommitted/unvalidated; kernel/HAL presence was not host UVC proof. DS4 composite-input repair required re-enabling an initially suppressed touchpad when gamepad/joystick interfaces joined. Current inclusion of these historical items is unestablished. [Removed raw-import boundary](../archive/PRIVACY.md).

Historical boot outcomes and then-unresolved Cirrus/ultrasound behavior and the later libmeminfo correction are owned by [V-BOOT](../state/validation.md#v-boot) and [V-MEMINFO](../state/validation.md#v-meminfo), not duplicated as current failures here.

## Current source ownership

Upstream dependencies already provide the absent-kernel-attribute ENOENT handling and optional BPF iterator log-spam correction. Preserve these integration facts without tracking upstream heads or restoring retired fork overrides. Our Android 17 frameworks/base contains independent high-FPS screen recording and blur suppression; compare current behavior before replaying old patches.

The retired font override is not a build requirement. Verify packaged assets when font work is requested.

GPU donor-driver, Turnip and game-setting experiments were parked by the maintainer. No broadly validated Unity/Unreal optimization, F8 GPU-driver compatibility, frame-generation port or unlocked 120fps is established. Keep thermal protection intact. Experimental root modules are not production fixes or required recovery dependencies.

Standalone hardware/xiaomi fixes: cbb57f1 rejects invalid legacy sensor-list/poll results and propagates direct-channel errors; 30c28d4 initializes fingerprint pointers and cleans failed opens; a2cf3b4 replaces unsafe delayed-session references with weak references and idempotent close; 5e49959 initializes lockout state and stops authentication during lockout. Recorded validation is target syntax compilation (sensor arm/arm64) and diff checks, not device replacement or biometric certification.

## Android 16 and connectivity boundaries

Port against the actual A16 API/resources and kernel, not by copying all A17
flags. A16 HBM must not call the absent `hbmControllerEnabled()` helper. High-FPS
screen recording and recording-blur suppression are independent features/commits;
neither should require the other. Recheck WFD/ELF dependency rewrites and selected
Clang against that branch instead of undoing or restoring them by age alone.

Common `3621ad4` removed obsolete Bluetooth build configuration. Source policy
and library presence were reviewed, but no Bluetooth audio headset or WFD sink
was available. Xbox controller input does not establish headset audio through its
3.5 mm jack over Bluetooth. No complete Bluetooth-audio/WFD certification or
new workaround is claimed; use an actual endpoint for a future requested test.

The SQLite MEMORY/OFF overlay overrides were removed to inherit framework
durability defaults. Overlay table shape/monotonicity checks do not calibrate
brightness, and enabled temperature-warning resources do not replace HAL events.

## October 9 source checkpoint

Common `c75e23f` fingerprints actual modem MCFG files and optional metadata,
copying only after valid input; `6574ae0` keeps radio-owned cache markers 0640,
restores directory write permission for replacement and rejects marker symlinks.
No regional carrier selection or radio policy change. Kernel `65b3e61797f0`
guards invalid fuel-gauge reads and empty SOC recovery; `21360d5ab98a` validates
touch control parsing/registration; `779d3d6ac01f` fixes fast-charge cleanup.
Device-selected defconfig fragments/DTBO packaging and compiler probes were
modernized; these are build maintenance, not user-visible performance claims.
[Validation limits](../state/validation.md#v-source-20261009).
