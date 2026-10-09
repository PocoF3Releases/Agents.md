# Final investigations and retained conclusions

Consolidated October 9 from dated project records. Findings below are recorded
source/runtime evidence, not tests rerun by this summary. Current behavior lives
in the linked subsystem topics; current heads/artifacts live in state records.

## Camera integration and rejected approaches

[Camera](miuicamera.md) is finalized. The mod's 5.x ABI/features are authoritative;
Alioth stock 4.x is a compatibility reference, not a replacement release APK.
Native 48MP QCFA is distinct from 12MP upscaling. Macro/front video and metadata/
permissions/native integration were included in the cumulative implementation.
CameraX extensions and unused MiSys delivery were removed.

Photo SAT used exact isSupportOpticalZoom, not the similarly named
isSupportedOpticalZoom. Universal cached false feature/deviceCodename values
could mask correct source. Recorded logical Photo operation used role 60,
camera ID 4 with physical [0,2], retaining its session for zoom handoff. Earlier
physical reopen/timing observations preceded this activation and are not proof
all current paths reopen. Aliothin inherits Alioth. VideoSAT also uses proven role
60; strings mentioning role 62 never established a provider-exposed camera.
Stock-app substitution cannot manufacture missing provider roles or persist
calibration. Do not edit Persist to conceal a missing calibration warning.

Main 4K60 preserves non-EIS session 0xf010. Invalid ultrawide 4K caused DSX/MNDS
pipeline failures; the final app blocks it and restores 1x. Ultrawide UI 60fps
measured around 30fps. RefBase warnings alone established no measured memory
leak. Camera completion does not reopen those investigations automatically.

## Audio and control transport

[Audio](dolby-audio.md): accepted AC-4 is the opt-in 32-bit legacy OMX path with
21-entry B/C tables, private request layout/index and corrected helper lookup.
Wrong index and helper resolution were separate failures. Marble Codec2 is a
different ABI; no donor decoder or complete 64-bit migration was delivered.
Current OMX foundation must not be redirected to v33. Existing xlog/foundation
packaging did not justify a blanket VNDK symlink set.

VoIP bypass must preserve enabled preference and restore media routing. Vendor
property ownership/SELinux errors can explain missing native DSP capture; ACKs
and mapped effect libraries do not prove audible DSP/VQE/game behavior.
MiSound headphone profiles do not establish a supported Alioth speaker mode.

## Device, kernel and research boundaries

[Device UX](xiaomiparts-device-ux.md): dialog clipping uses actual panel overlap,
not fixed global insets. Per-app touch profiles retain original fields; expert
presets apply last. Ultrasound retry changes only the exact idle timeout branch
and uses hash-guarded extraction. Latest refresh/modem/thermal fixes have scoped
acceptance; a matching rebuilt image remains distinct from temporary tests.

[Platform](kernel-frameworks.md): keep supported schedtune/cgroup/vendor controls;
remove only obsolete ownership or unshipped services. Bionic loader TLS failure
could break Android and recovery before userspace, so it is not automatically a
kernel defect. Use checkout compiler/JDK and user builds. Kernel target checks
are not full ROM acceptance or proof that replacement-battery boot is fixed.

[Graphics](gaming-graphics.md): donor V502 dependency/extension-string similarity
is not runtime compatibility. Turnip shell success is not app selection. Myron
frame insertion uses Novatek hardware/services absent from the inspected Alioth
dump; it is not a device-tree toggle. No accepted generic FPS/unlocked-120fps,
Unity/Unreal, frame-generation or WAN-speed fix exists. Experiments remain parked.

## Evidence and future records

[Haptics](haptics.md), [PBRP](pbrp-recovery.md), [validation](../state/validation.md)
and [project history](project-history.md) retain final results and limits.
Raw clips/dumps/private logs are not supplied. Old head inventories, duplicate
release drafts, session instructions and superseded next steps were removed.
New investigations update their owning topic; create dated evidence only when it
adds decisive diagnostics. The archive skeleton is for future records, not startup.

## Final everyday UI and speaker-tuning pass

October 9 source check: frameworks/base makes tap-to-wake and ambient pulse
independent, avoids clamping automatic-mode AOD to momentary screen brightness,
and moves QS usage polling off the main thread. Companion Settings contains
matching gesture controls and clipboard auto-clear/timeout controllers. These
are final local implementations, not freshly measured responsiveness or UI tests.
Alioth vendor.prop enables stock speaker tuning despite common's default-off
gate. Android spatializer remains disabled. Profile/endpoint acoustic acceptance
is still scoped. Exact source coverage belongs to the
[initial-build audit](../state/changelog-audit.md).
