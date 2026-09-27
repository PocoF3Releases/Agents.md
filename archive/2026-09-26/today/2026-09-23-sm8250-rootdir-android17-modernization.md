# 2026-09-23 — SM8250 Common Rootdir Android 17 Modernization

## Scope

Active incremental review of:

```text
device/xiaomi/sm8250-common/rootdir
```

Target remains POCO F3 / `alioth`, SM8250/Kona, Android 17.

Review rule:

- inspect file-by-file and line-by-line;
- use AOSP `platform/system/core/rootdir` master as the Android 17-era baseline for generic init/cgroup/rootdir behavior;
- do not delete Qualcomm/vendor behavior merely because AOSP no longer carries it;
- verify vendor-specific behavior against the actual Alioth 4.19 kernel, current proprietary file lists, current vendor init files, and current device-tree ownership;
- make one small verified change at a time;
- commit and push each safe change before continuing.

## Baseline

Starting remote head:

```text
PocoF3Releases/device_xiaomi_sm8250-common:aosp-17
6e964d1447daa2e90007d36115ba4975f1309360
```

Current pushed remote head after the second cleanup batch:

```text
82b276fbd649f3e4b1eb399ed00cf0607b59ce4b
```

## Pushed cleanup sequence

### 1. Non-Kona init dispatch

```text
f69505728ab86a27feda340a68a5e6620a4329b8
sm8250-common: rootdir: Drop obsolete non-Kona init paths
```

`BoardConfigCommon.mk` hardcodes:

```make
TARGET_BOARD_PLATFORM := kona
```

`rootdir/bin/init.qcom.sh` still carried runtime branches and helpers for unrelated Qualcomm platforms. The file was reduced to the behavior that could actually execute on this tree while preserving the existing Kona irqbalance path, baseband handling, modem-config copy, and printk setup.

### 2. Legacy early-boot targets

```text
44d81821f144d3f18309397c412db3b8748ae1de
sm8250-common: rootdir: Trim legacy early-boot targets
```

`rootdir/bin/init.qcom.early_boot.sh` contained hundreds of lines for non-Kona platforms and unrelated reference/automotive products.

Removed unreachable platform/product branches while preserving:

- Kona `vendor.media.target_variant="_kona"`;
- existing Kona density setup;
- ATFWD property handling;
- common DRM/display permission handling;
- alarm-boot property handling;
- GPU frequency export.

### 3. Duplicate camera schedtune writes

```text
43e0b46cb82a58c3e9072f16f765f6f17fe6a807
sm8250-common: rootdir: Remove duplicate camera stune writes
```

In `rootdir/etc/init.qcom.power.rc`, the camera schedtune values were written twice consecutively after group creation. The second identical pair was removed.

Important conclusion: **do not remove schedtune wholesale just because modern AOSP does not use it generically.** The Alioth 4.19 kernel still enables `CONFIG_SCHED_TUNE=y`, so stune remains a real device capability until a separate migration is proven safe.

### 4. Obsolete irqbalance variants

```text
f784ef4af5a9b53f41acccadb706cd2c680736b9
sm8250-common: rootdir: Drop unused irqbalance services
```

Removed `vendor.msm_irqbal_lb` and `vendor.msm_irqbl_sdm630` service definitions.

Evidence:

- the Kona-only init path only starts `vendor.msm_irqbalance`;
- no remaining source references start the two legacy variants;
- only `vendor/etc/msm_irqbalance.conf` is packaged, not the little-big or SDM630 config files.

### 5. qlogd

```text
281091b662ca6fc15144b062cef1826803f85901
sm8250-common: rootdir: Remove obsolete qlogd service
```

Removed the `/system/xbin/qlogd` service and property triggers.

Evidence:

- binary absent from current Xiaomi common/alioth vendor trees;
- no other device-tree references;
- no Evolution X source match;
- no AOSP master rootdir service.

### 6. VM BMS

```text
9adaeafa7810a34667cc404a5f5f9450d5cdba6e
sm8250-common: rootdir: Remove unused VM BMS support
```

Removed:

- `service vm_bms /vendor/bin/vm_bms`;
- stale `/dev/vm_bms` uevent permission.

Evidence:

- no `vm_bms` userspace binary is packaged;
- Alioth kernel config uses `CONFIG_QPNP_SMB5=y`;
- Alioth does **not** enable `CONFIG_QPNP_VM_BMS`;
- after the Kona-only script cleanup, nothing starts `vm_bms`.

### 7. LKCore

```text
7988e9043042aa08b645477ebe091bed3800371b
sm8250-common: rootdir: Remove dead LKCore services
```

Removed the USER/USERDEBUG `LKCore` service stanzas.

Evidence:

- no `LKCore` binary in current Xiaomi common/alioth vendor trees;
- no Evolution X source match;
- both services were disabled;
- no start trigger remained.

### 8. Legacy QSEE proxy

```text
def448c318aee3def0ea34e5a5bc132030c69a75
sm8250-common: rootdir: Drop legacy QSEE proxy service
```

Removed `qseeproxydaemon`.

Current vendor image already supplies:

```text
/vendor/bin/qseecomd
/vendor/bin/hw/vendor.qti.hardware.qseecom@1.0-service
```

with their own current vendor init files. The legacy proxy binary is not packaged.

## AOSP master comparison notes

Current AOSP rootdir still creates and configures cpuctl/cpuset/blkio groups and uses libprocessgroup task profiles/cgroup descriptors. Therefore old-looking cgroup code in this device tree must not be removed solely because it dates from Android 11-era Qualcomm sources.

For Alioth specifically:

- legacy schedtune remains kernel-supported;
- AOSP master is a reference for generic modern Android behavior, not a replacement for Qualcomm kernel requirements;
- each vendor-specific sysfs/cgroup write must be checked against the actual kernel before removal.

## Local workspace note

The extracted archive contains complete Git repositories, but the execution container could not resolve `github.com` for native `git push`. Local commits were still made for clean incremental diffs; canonical remote commits were pushed through the connected GitHub API.

When continuing in a fresh environment, use the **remote SHAs above** as source of truth rather than the local-only commit IDs from this container.

## Next continuation point

Continue `rootdir/etc/init.qcom.rc` linearly from the service block following the removed QSEE proxy, validating each legacy service against current packaged binaries and current Android/vendor architecture.

Do not batch-delete services merely because their names are old.


## Second pushed cleanup batch

### 9. Dead poweroffhandler

```text
8437c97fc2e47700536a4fb429fe50a6fd735691
sm8250-common: rootdir: Remove dead poweroffhandler service
```

The legacy `/system/vendor/bin/poweroffhandler` binary is not packaged by the current Alioth/common vendor trees and the service had no start trigger or other project reference.

### 10. Dead HBTP daemon

```text
6b005a5d5c0d55cdfd0158838cbfe19020d9b365
sm8250-common: rootdir: Remove unused HBTP daemon service
```

`hbtp_daemon` is not shipped and the disabled service had no start trigger or other project reference.

### 11. Obsolete QVOP daemon

```text
72f17bdd883d433c3df34c08541dce5d9f83baac
sm8250-common: rootdir: Remove obsolete QVOP daemon
```

`qvop-daemon` is not shipped. Unlike several other stale services it was a normal `late_start` service, so retaining it could make init attempt to launch a missing executable.

### 12. Obsolete battery_monitor executable service

```text
daea0845bb8aea9f96be756ff559a5ff49b091de
sm8250-common: rootdir: Remove obsolete battery_monitor service
```

The current platform health implementation contains a `BatteryMonitor` implementation class but does not build the historical `/system/bin/battery_monitor` executable. The old disabled service had no remaining trigger.

### 13. Obsolete profiler_daemon

```text
267fe9dabc14fcc825dcf3db39c12f5ef020386e
sm8250-common: rootdir: Remove obsolete profiler daemon
```

No current platform module builds `/system/bin/profiler_daemon`, and the disabled service had no start trigger.

### 14. Remove impossible rild fallback

```text
2a74ce2ae1b8a528f32b6bc8f7dea432362516b3
sm8250-common: rootdir: Drop obsolete rild fallback
```

Updated `rootdir/bin/init.class_main.sh` and `rootdir/etc/init.qcom.rc`.

Verified current radio stack:

```text
vendor/bin/hw/qcrild
vendor/etc/init/qcrild.rc
```

The vendor package contains no `rild` executable and current Evolution X has no `vendor.ril-daemon` service. The historical modem-version parser could select a nonexistent rild fallback.

The script now starts qcrild directly on supported radio basebands and uses `vendor.qcrild2` / `vendor.qcrild3` for multisim. The obsolete `vendor.ril-daemon2/3` definitions were removed.

### 15. Orphan hostapd FST service

```text
712c74555d526b4afe5eeb9bc0d6638ce3c6b7fb
sm8250-common: rootdir: Remove unused hostapd FST service
```

The disabled `hostapd_fst` service had no start/ctl caller in PocoF3Releases or current Evolution X sources. Normal hostapd integration was not changed.

### 16. Charger-mode physical system mount

```text
e248f2ba7f5b9bf9a068e20e761610291d72741b
sm8250-common: rootdir: Drop legacy charger system mount
```

Removed:

```text
wait /dev/block/bootdevice/by-name/system
mount ext4 /dev/block/bootdevice/by-name/system / ro barrier=1
```

Current `fstab.qcom` declares `system` as a logical, AVB-protected, `first_stage_mount` partition. Android 17/AOSP charger handling assumes partitions were handled by first-stage mount rather than manually mounting a physical `by-name/system` node.

### 17. Charger-mode forced ADB

```text
82b276fbd649f3e4b1eb399ed00cf0607b59ce4b
sm8250-common: rootdir: Stop forcing ADB in charger mode
```

Removed the unconditional:

```text
setprop sys.usb.config adb
```

from the charger action.

Modern Android derives persistent USB ADB policy from `ro.debuggable` and `persist.sys.usb.config`; configfs then starts/stops adbd based on that policy. Charger mode should not override the platform policy.

## Explicit keep decisions from this pass

### power_off_alarm — keep

`vendor/bin/power_off_alarm` is explicitly extracted in `proprietary-files.txt`, packaged by `vendor_xiaomi_sm8250-common`, and started by `init.target.rc` during charger mode.

### ATFWD — keep

`vendor/bin/ATFWD-daemon` is explicitly part of the current proprietary package. Do not delete it as a generic legacy Qualcomm service without new runtime/source evidence.

### device bugreport keycode service — keep for now

The service executes the current `/system/bin/dumpstate` binary and provides a device keycode trigger. Current platform dumpstate ownership is different from old monolithic rootdir services, but this particular entry is not a missing-binary stub and therefore was not removed during dead-service cleanup.

## Next continuation point

Continue `rootdir/etc/init.qcom.rc` immediately after the bugreport/property forwarding block, starting with the device `vendor.audio-hal` override and checking whether it duplicates or intentionally overrides the current Audio HAL service definition.

Continue using the same rule: inspect one ownership/runtime unit, verify against current platform/vendor/kernel, then commit and push only that unit.
