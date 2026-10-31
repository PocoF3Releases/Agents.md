# Alioth cross-component integration audit — 2026-10-30

Read-only source/device review, not a full functional certification or new ROM build.

## Checked

- Device runs kernel `4.19.325-Redline-f503c8d-cip136`, SELinux Enforcing; mi_thermald is running and map_ready is 1.
- Alioth, common device tree, hardware/xiaomi and both vendor repositories were clean. No production source changes were made in this audit.
- Installed powerhint.json, selected A/B fstab, init.target.rc and init.qcom.rc match checkout SHA-256 exactly.
- Power action references and literal values resolve to declared nodes. All file-backed power paths exist. The live power HAL runs as root in hal_power_default, reports HintManager Running and readable current node values. Root path inspection alone is not a complete SELinux permission proof.
- Every literal service executable declared in common rootdir RC files exists on this phone. This does not prove every optional service should run.
- Parts display, backlight, thermal profile and touch-sampling paths exist; AW8697 waveform/gain/calibration paths exist. Missing generic Xiaomi UDFPS paths are inactive implementations on this side-fingerprint device, not missing Alioth hardware support.
- Userdata is mounted F2FS through a mapped block device with inlinecrypt; metadata is ext4 and SPU storage is vfat. No destructive encryption test was performed.
- Wi-Fi control sockets have wpa_data_file labels. Audio HAL, audioserver and Dolby DMS run; AudioService reports MODE_NORMAL. This is registration/state evidence, not new playback/recording coverage.
- USB ADB is available. No USB mode changes or flash were performed.

## Confirmed gap requiring separate integration validation

Android thermalservice reports HAL Ready false and no connected HIDL Thermal HAL. This repeats the earlier Adreno audit finding; it is not evidence that Xiaomi/kernel thermal protection is disabled.
Resolved October 31 as intentionally absent: [decision and stock RE](thermal-hal-decision-20261031.md).

The stock dump actually contains android.hardware.thermal@2.0-service.qti, its RC and VINTF fragment; the common proprietary list omits them. The stock thermal-engine service is commented out while mi_thermald is separate. The Thermal HAL depends on thermal 1.0/2.0 HIDL libraries and reads thermal-zone/threshold/cooling sysfs paths. Strings alone do not establish read-only behavior, correct sensor mapping, or safe coexistence. Before importing it, inspect the implementation/configuration and policy, verify dependency resolution and sensor units/threshold semantics, then test with mi_thermald continuously active and SELinux enforcing. Do not invent severity/headroom values or enable competing thermal-engine control.

## Limits and next checks

No new fixes, rebuild or device installation were justified by the checks above. Display color differences during manual 60/120 Hz changes remain unresolved; existing low-brightness RRO is not a proven correction for that optical mismatch. Broader recording, external audio routes, USB OTG/MTP, encryption credentials and stress/thermal behavior need targeted functional checks, not extrapolation from service presence.

Private raw evidence: ~/evo/.repo/research/alioth-integration-20261030/. No device identifiers or complete raw logs are published.

## Installed parity recheck — 2026-10-31

All 311 hashed `/vendor` init, VINTF, audio, config, fstab, HAL binary, overlay
and ODM files match the October 28 build output. XiaomiParts, XiaomiDolby and
MiuiCamera run from their ROM paths; every `/data/app` update of a system
package is a Google/Play package. Device-tree commits newer than that build: only the
alioth anti-flicker RRO. Recovery overlay patches: 0 pending, and both local
re-applied public commits are patch-identical to their public originals.
Packaged thermal-engine has a fully commented init RC and does not run.

## Runtime log audit — 2026-10-31

Read-only, kernel 7d559e9 boot, Enforcing. No ANR, no fatal signal or
system-service death; the only tombstone is the intentional KGSL
cross-mapping test fault. Non-running init services are oneshots. Kernel log
errors are known boot noise: absent pm8009 camera PMIC GPIO probe, an
early `gpuss-max-step` virtual-zone read before tsens, debugfs/clock probes.
All declared HALs register; lshal's `N` column marks unfrozen vendor
interfaces, not missing services.

Denials triaged as non-defects: `/dev/diag` opens by vendor daemons (user-build
diag disabled), unlabeled unset `persist.sensor.sardisable` read by sensors,
dex2oat probing `/data/user/0` while background compilation succeeds, app
property probes, and an upstream Evolution X `init.rc` `rm` under `/data/adb`
that SELinux blocks.

Upstream gap, not changed: Pixel Private Compute Services
(`com.google.android.as.oss`, `pccId=-1`) becomes association-restricted after
a `BIND_RESTRICT_ASSOCIATIONS` bind; its live allowlist then admits only
`nowplaying`, so System Intelligence and `odad` binds fail ("association not
allowed"), including Live Caption model download. Owner: Evolution X
`vendor/gms` sysconfig and A17 PCC integration. Do not widen privacy
allowlists in maintained device trees.
