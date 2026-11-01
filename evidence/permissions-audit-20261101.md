# Android permission audit — 2026-11-01

## Method

Rules are taken from the A17 checkout: `SystemConfig` reads privapp allowlists
per partition (system, system_ext, product, vendor/odm, apex), and
`AppIdPermissionPolicy` checks only the packages in a UID that request the
permission. System-UID apps therefore still need their own entries unless the
framework package requests the same permission. Production is `log` mode
(`ro.control_privapp_permissions=log` from vendor/lineage), so a gap warns at
boot instead of blocking it.

Permission definitions and protection levels come from the running Nov 1 ROM
(`dumpsys package permissions`, 1843 entries). Requested permissions come from
all 469 built APK manifests (aapt2), and allowlists, default grants and
sysconfig from the installed partition XMLs in out/. Live grant state was read
for the 18 apps shipped from device/xiaomi, hardware/xiaomi and vendor/xiaomi.
Boot-time violation logs had rotated, so the check was static plus grant state.

## Results

- Every privileged permission requested by our apps is allowlisted in the
  correct partition: Parts and Dolby (MODIFY_AUDIO_ROUTING, REAL_GET_TASKS),
  MiuiCamera, ExtraPhoto, the Hotword apps and the QTI ims, WFD and
  qcrilmsgtunnel apps. MANAGE_ACTIVITY_TASKS is signature|recents and is
  granted by signature.
- All install-time permissions are granted on the phone. The only ungranted
  permissions are runtime ones awaiting user choice after the wipe: camera
  Bluetooth, ExtraPhoto media and WFD local network.
- Default grants for MiuiCamera and CNE name defined runtime permissions that
  the apps request.
- Undefined requests are confined to prebuilt stock APKs (MIUI, Mediatek and
  Qualcomm extras) and are inert.

## Corrections (no grant changes)

- [DSPVolumeSynchronizer](https://github.com/PocoF3Releases/hardware_xiaomi/commit/7fbfe54cf0262481f9a2aa6520f0d4530796b6a7):
  removed the allowlist. It listed two normal permissions, one that was never
  requested, and INTERACT_ACROSS_USERS_FULL, which is not privileged and is
  already held by the system UID.
- [Camera](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/5bf7082784a3ff4793618fb68a956f7f0ca94901):
  removed the unrequested WRITE_MEDIA_STORAGE entry, the undefined Mediatek
  APU permission, and blocks for the unshipped Mimoji and Scanner apps.
- QTI `system/etc/permissions/privapp-permissions-qti.xml` is no longer
  extracted or shipped
  ([vendor](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/16c1af95bb3e23bc0e82e884fd67fa8a14a39c52),
  [common](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/83b33a6bc456f95508ae6039436520d7bea65ed2)).
  Its packages are either not shipped or installed on system_ext, which has
  its own allowlists.

## Retained

- The stock QTI system_ext allowlists and `qti_whitelist.xml` keep entries for
  unshipped packages and a few non-privileged permissions. They are pinned
  stock blobs and harmless.
- The IFAA service is exported without a permission as upstream designed it,
  so payment apps can bind to it.
- GMS DeskClock and Odad lack SCHEDULE_EXACT_ALARM allowlist entries; that
  belongs to the GApps vendor tree, not ours.

## Verification and limits

`m DSPVolumeSynchronizer` passed, including Soong/Kati analysis of the changed
copy lists. No ROM build or flash was done. The out/ tree still holds the old
installed XMLs until `m installclean`. Boot-time `log` warnings will be checked
on the next ROM build.
