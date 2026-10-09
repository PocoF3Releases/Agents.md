# Graphics, games and parked experiments

**No general game-performance fix or frame-generation port is accepted.** The
maintainer parked donor-driver, Turnip and game-setting experiments. This record
preserves results and avoids repeating unsupported approaches; it is not an
instruction to restart testing. Thermal protection stays enabled.

## Alioth versus OnePlus 9R

Local comparison: shipped SM8250 vendor libraries versus `~/oneplus9r/out/vendor`.
Alioth GLES identifies V@0502.0 (2021-10-04), donor V@0502.46 (2025-06-17).
Compiler versions EV031.32.02.16 / .17. Vulkan/GLES2/GSL/compiler executable
sections differ; EGL/GLES1/helper sections mostly match. Direct dependencies and
export-name sets match; extension-name strings match but are not runtime queries.
A650 GMU/SQE firmware matches; some ZAP artifacts differ.

This is a V502 maintenance donor, not proof of newer Vulkan support or a fixed
GPU fault. Matching ELF dependencies does not verify KGSL ioctls, linker
namespaces, rendering, thermals or FPS. Prior subjective improvement in a game
was not a controlled benchmark. No donor module is a required production fix.

Adreno 650 mainline support uses its own kernel/userspace stack; it does not make
an unrelated newer Adreno proprietary driver interchangeable with Alioth KGSL.
Keep actual loaded driver, firmware, rendering settings, cache state and scene
identical when comparing a newly authorized experiment. Shader compilation or a
loading screen alone cannot prove a recovery-policy success/failure.

## Myron Smart Frame Rate

Recorded myron EEA build OS3.0.302.0.WPMEUXM selects the Novatek dual-DPU backend:
`product/etc/device_features/myron.xml` has `support_dual_dpu=NT`.
Security Center `GameBoxVisionEnhanceUtils` → Joyose
`IGPUTunerInterface.setFrameInsertingOrSuperResolution` → `NovaTekEnhanceContext`
→ FrameMaster/Novatek display services. Native paths include
`setDualDPUMemcState`, `DualDpuHandler::handleGameMemc`, `/dev/vis_display_spidev`
and `odm/etc/dqe` MEMC/game configuration.

The character device and services were observed on Myron; matching integration
was absent from the inspected Alioth dump. This is not a device-tree-only port.
A separate software interpolator would require its own implementation and
performance/latency evaluation. A 120 FPS dashboard does not prove 120 game
simulation frames or independently measured interpolated output. The audit made
no ROM/driver/settings changes and did not measure on/off frame output.

## Turnip and other gaps

Endfield previously loaded stock `vulkan.adreno.so` despite package opt-in.
A shell-domain test succeeding did not prove app-domain selection. If explicitly
reopened, inspect GraphicsEnvironment and package lookup/visibility before
repeating force-queryable patches. No universal Unity/Unreal rootdir flag,
unlocked 120fps/native-resolution solution or game-specific crash cure was
established. Wi-Fi download observations also lacked a controlled LAN throughput
comparison; do not infer a radio-driver fix from WAN download speed alone.

Provenance: local `out/gpu-driver-comparison/REPORT.md` and
`out/myron-frame-audit/REPORT.md`, imported 2026-09-30. This import adds no fresh
device measurement. Source ownership is in the [map](../state/repositories.yaml).
