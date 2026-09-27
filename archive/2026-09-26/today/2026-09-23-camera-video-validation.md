# Camera video fixes and rooted-device validation — 2026-09-23

## Scope and final state

The user explicitly resumed camera work. This checkpoint supersedes the older
paused Stage-1 rollback instructions. Work is limited to `device/xiaomi/camera`
and `vendor/xiaomi/camera`; no ROM was rebuilt or flashed for these tests.

- GitHub `PocoF3Releases/device_xiaomi_camera:aosp-17`: `6c25fe9babca33dfc37813be7a92f5bbbe4d6319`.
- GitLab `johnmart19/vendor_xiaomi_camera:aosp-17`: `f13797ef3d93508756e06a4a185c9208dbc3ee88`.
- Both remote heads were verified against local HEADs when offloading.
- Main-camera 4K30/60 records successfully. Ultrawide 1080p records successfully.
- Ultrawide 4K is **not implemented**: the app now prevents the failing lens switch.
- Ultrawide with the UI set to 1080p60 measured about 30 fps in this scene;
  do not advertise verified ultrawide 60fps support.

## Implemented corrections

1. `patches/alioth-videosat60-session-mode.patch` preserves non-EIS session mode
   `0xf010` for alioth/aliothin logical camera 4. Previously, the 60fps branch
   overwrote it with `0x803c`, producing corrupted main-camera 4K60 output,
   stabilization result ON despite request OFF, and CHIEISV3/EIS-margin errors.
2. `patches/alioth-ultrawide-video-limits.patch` filters zoom stops below 1x and
   constrains the shared normal-Video zoom range when 4K is selected. The
   toolbar index also clamps a stale 0.6x selection before rebuilding controls.
   Photo and lower-resolution choices remain unchanged.
3. The aligned companion APK contains the same correction. Only `classes2.dex`
   differs from the preceding APK for the latest ultrawide guard.

Both patches are maintained in the device tree's existing apktool patch flow.
The working decoded source is `~/evo17/out/camera-capabilities-cache/decoded`;
its Git branch is not the delivery authority. Do not push unrelated decoded
history or reconstruct the production APK from old stock-reference archives.

## Verified failure and limitation

Switching 4K30 to 0.6x reproduced `DSX_ProcessNcLib` error 67108866,
`DSX10CalculateSetting` failure, and `Invalid Full path MNDS ouput for DS16 path`,
followed by pipeline recovery. The installed ultrawide IMX355 advertises a
3280x2464 pixel array and no standard 3840x2160 stream. This establishes the
current pipeline failure; it does not prove that all possible software-upscale
implementations are impossible.

Logical camera 4 remains the VideoSAT camera. Vendor-internal ArcSoft master ID
3 must not be confused with Android physical camera ID 3.

## Runtime validation

| Test clip | Configuration | Measured output | Result |
|---|---|---|---|
| VID_20260923_172458.mp4 | Main 4K30 | 3840x2160, ~30.03 fps | H.264/AAC decode passed |
| VID_20260923_172540.mp4 | Main 4K60 | 3840x2160, ~60.04 fps | H.264/AAC decode passed |
| VID_20260923_172705.mp4 | Ultrawide 1080p30 | 1920x1080, ~30.05 fps | H.264/AAC decode passed |
| VID_20260923_173205.mp4 | Final APK, after ultrawide to 4K30 | 3840x2160, ~30.03 fps | Decode passed |
| VID_20260923_173302.mp4 | Ultrawide UI 1080p60 | 1920x1080, ~30.05 fps | Decode passed; not 60fps proof |
| VID_20260923_173400.mp4 | Final APK 4K60 | 3840x2160, ~60.04 fps | Decode passed |

Both final 1080p-ultrawide to 4K30/60 transitions restored 1x without Java/native
crashes or DSX10/MNDS errors in the transition logs. Extracted main-4K60 and
ultrawide frames were visually checked and did not show the earlier striped
corruption. Short clips do not establish long-duration thermal stability or
complete validation of every camera feature. Some CHIEISV3 messages were seen
on the preceding 1080p session; do not claim all camera logging is clean.

An intermediate guard crashed with `Illegal zoom ratio: 0.6, zoomRatios =
[1.0, 2.0]` during resolution changes. The final toolbar-index clamp fixes this;
both transitions were rerun successfully before committing.

## Artifact identity and installation

- Canonical file: `vendor/xiaomi/camera/proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk`.
- SHA-256: `29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`.
- Size: 223517496 bytes.
- Apktool 3.0.3 assembly and `zipalign -c -P 16 4` passed.
- The APK is a prebuilt for ROM platform signing, not a newly signed user-install APK.
- During testing it was mounted from `/data/local/tmp/MiuiCamera-uw2.apk` over
  `/system/priv-app/MiuiCamera/MiuiCamera.apk` using Magisk `su -mm`.
- Installed-path SHA-256 matched the canonical artifact at test completion.
- The mount is temporary and disappears after reboot. Recheck rather than
  assuming this APK is persistently installed after a later restart.
- Original local camera preferences were restored after testing.
- The installed CHI library already had SHA-256
  `8927747617c3729e2590ee06e3c9c1416182dab909647a7af044764459c76224`;
  it was not replaced in this APK test.

Rollback of the temporary APK mount (only if needed):

```sh
adb shell am force-stop com.android.camera
adb shell su -mm -c 'umount /system/priv-app/MiuiCamera/MiuiCamera.apk'
```

Local evidence is under `~/evo17/out/ultrawide-fix/` and
`~/evo17/out/camera-4k60-root-test/`. Do not upload private recordings or raw logs.

## History and continuation rules

Camera histories were rebuilt into final component commits at the user's
request; old camera heads in historical records are not active build targets.
Current histories contain 11 device commits and
6 vendor commits, including these latest fixes.
Only actual agent-authored modifications receive agent attribution; imports and
unchanged upstream work must not receive it. Server-side LFS storage reclamation
was not verified and must not be inferred from rewritten Git history.

Do not silently re-enable 0.6x in 4K. Further work requires a demonstrated valid
ultrawide pipeline, not another feature flag. The remaining 1080p60 frame-rate
question needs controlled bright-scene/sensor-mode evidence. No full ROM builds
unless requested; use the `user` variant exclusively.
