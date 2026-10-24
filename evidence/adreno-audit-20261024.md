# Adreno 650 validation — 24 October 2026

**source-checked · build-tested · host-tested · device-tested**. This is scoped
validation, not certification that every GPU API, game or driver path is bug-free.
[Reusable source-only tools](../scripts/adreno-audit/README.md) are kept outside ROM
packages. Raw traces, disassemblies, maps, APKs and boot backups remain private.

## Published changes

Repository: [kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250),
branch `aosp-17`. Baseline:
[b8fc2fc50a5c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b8fc2fc50a5cca0e3fa9bfb9381c2f2efd2bf2da).

- [7aeac751973b](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7aeac751973bebfd9fa1e546fc5b58c4a4751fdd):
  preserve mapped footprints in 64 bits. A signed `int` made a 2-GiB footprint
  negative and a 4-GiB footprint zero before pagetable accounting. Mapping addresses
  and allocation limits are unchanged.
- [12d26a785cf3](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/12d26a785cf386e875c1fb049614f9089436070b):
  emit per-process/global `gpu_mem_total` events. The tracepoint existed and was
  enabled, but KGSL did not emit it. Backported from Google's production 4.19
  [implementation](https://github.com/LineageOS/android_kernel_google_redbull/commit/43aff12c50062ec0e50a47859b2bc688e9686f61),
  retaining Sharat Masetty's authorship. Adaptation retains current descriptor-free
  callbacks and import failure unwind; the deduplicated DMA-BUF entry retains its
  accounting owner/original size until the final import is released.

The remote head was checked after a normal fast-forward push. No force push,
proprietary blob replacement, GPU overclock, thermal bypass, new advertised Vulkan
capability or system-side source change was made.

## Stack and reverse-engineering evidence

Physical Alioth, Android 17 / SDK 37, `user`, SELinux enforcing, Adreno 650 v3.
Runtime GLES: 3.2, Qualcomm V502.0, compiler EV031.32.02.16. Vulkan: 1.1.128;
the device's advertised Vulkan 1.1 feature agrees with runtime. Both ABIs advertise
99 GLES and 71 Vulkan extensions with identical name sets.

Device SHA-256 matches the checkout for six 32/64-bit GLES2/Vulkan/GSL libraries
and six A650 GMU/SQE/ZAP firmware files. Kernel logs show firmware load success.
App process maps confirm stock Adreno, GSL, compiler and mapper libraries; matching
ELF imports alone was not treated as runtime acceptance.

Copied ELF inventories and an AArch64 GSL disassembly identify the ioctl/mmap
boundary and context/property wrappers. **Seen:** 64-bit `libgsl.so` SHA-256
`894faf907f5719a9609295bce21ee0a89ca5f9a71bfa1db242ef0284b17d8b7e`
imports `ioctl`/`mmap`; `ioctl_kgsl_context_create` at file virtual address
`0x1ee118` constructs request `0xc0080913`. `ioctl_kgsl_device_getproperty` is
exported at `0x1ec4d8`. These are ELF-relative addresses, not process addresses. A bounded preload logger for the native
probe identified property `0x26` (`KGSL_PROP_GAMING_BIN`) as the only rejected
queried property on both ABIs. It is optional and unimplemented here; no synthetic
response was added. Exact function-label matching avoids confusing call sites with
disassembly function definitions.

## Targeted runtime tests

Both real `untrusted_app` ABIs passed three repeated runs of **62 native checks plus
six window checks** on the temporary patched kernel:

- KGSL info, context create/destroy, 100 allocate/query/mmap/free iterations,
  GPU-object cache synchronization and object cleanup.
- KGSL timeline create/query/signal/wait/destroy, exported fence polling,
  sync-file merging, unsignaled polling and merged completion.
- GLES shader compilation/linking, draw/clear pixel verification, compute SSBO
  dispatch/barrier/map readback, GL sync and Android native fence fd polling.
- AHardwareBuffer allocation, EGL image import, framebuffer completeness and
  GPU-write/CPU-read visibility through the real mapper/gralloc stack.
- Vulkan instance/device/queue/buffer/memory/command/fence lifecycle, submit,
  bounded fence wait and exact coherent-buffer readback.
- Real SurfaceView/EGL presentation: valid dimensions/context, swap interval and
  60 successful swaps. Swap wall time is not a display-FPS measurement.

Twenty earlier native repeat runs passed. Traced native runs exercised 24 distinct
KGSL ioctl numbers per ABI (710/703 total calls in the recorded trace); this is
observed coverage, not a claim that all 44 generic dispatch entries executed.
Sparse allocation is disabled by this kernel and returned its documented internal
unsupported error 524. That path was marked **unsupported**, not passed or enabled.
Protected/DRM paths and adversarial ioctl fuzzing were not exercised.

Initial harness mistakes were corrected without changing the driver: legacy
`gpu_id` is zero here, contexts require preamble/no-GMEM flags, and window tests
require an awake/visible surface. An early window attempt while the phone was
dozing was invalid; the rerun enforced the screen precondition and passed.

## Khronos sample

Built the checkout's ARM64 `deqp-binary` and selected 633 deterministic samples
from the 2020 Android must-pass lists: 163 GLES2, 214 GLES3, 187 GLES3.1, 69 Vulkan.
Explicit 256×256 pbuffers and the checkout's resource data were used. Initial
unspecified dimensions created an invalid default framebuffer; the harness was
corrected before recording the selected suite.

| Result | Installed kernel | Patched temporary kernel |
| --- | ---: | ---: |
| Pass | 556 | 556 |
| NotSupported | 76 | 76 |
| QualityWarning | 1 | 1 |
| Fail | 0 | 0 |

Every case's status/result matched before and after, not just the totals. Skips
include unavailable Vulkan 1.2/extensions/timeline semaphores, unsupported formats,
resource limits and non-MSAA default-framebuffer conditions. They are not passes.
The quality warning is GLES2 basic-line interpolation using projected coordinates;
it remains a closed-driver limitation. No driver binary patch or broad rendering
workaround was justified. This sample is not full CTS, EGL-window, protected/DRM,
all-game, sustained-load or Vulkan conformance certification.

## Accounting, build and host checks

Ordinary Android Perfetto tracing with the same workload produced **no GPU-memory
tracks before**, then seven tracks after the backport: 1,774 global samples and
2,241 process samples. Global readings stayed within approximately 159–174 MiB.
The diagnostic app and three native probe processes ended at zero; no negative or
implausibly large GPU-memory samples were captured. No permissive policy was used.

Host regression fixtures compile the actual changed functions with external
operations mocked. The pinned baseline reproduces three large-footprint failures;
the corrected current function passes 2/4-GiB boundaries and failed-map preservation
without allocating those buffers. ASan/UBSan checks pass duplicate DMA-BUF imports,
both release orders, original-size pairing and accounting-node allocation failure.
These fixtures do not prove live kernel OOM or concurrent fault injection.

Full test kernel Image linked with the device-pinned Clang r563880c. All twelve
configs regenerated in check mode with no difference. Both commits pass strict
checkpatch. KGSL W=1/sparse builds pass; an isolated baseline comparison found the
same **165 existing KGSL diagnostics**, with none added or removed. Existing
warnings were not suppressed or relabeled as a clean warning-free build.

## Deployment and remaining limits

Test image SHA-256:
`983d33bad73623382b38bfbe746ae56833118868dedef22d1e3df738c9400397`.
Only the kernel payload was replaced in a temporary boot image; the installed
ramdisk was preserved byte-for-byte. Its diagnostic build identity was
`adreno-audit`, build 3. A test-only release override retained the installed
`4.19.325-cip136-st20-perf-gb8fc2fc50a5c` string; that string alone does not identify
the patched source. The image hash, diagnostic build identity and trace behavior
establish which temporary artifact was tested.

After testing, the phone rebooted normally to its original installed kernel. The
boot partition's SHA-256 still matches the pre-test backup. The diagnostic package
and only the audit's own device files were removed. No new production ROM/OTA was
built or flashed; the published source requires the normal production rebuild.

Android thermal service reports `HAL Ready: false`. `mi_thermald` runs, GPU
temperature is readable and `msm-adreno-tz` is active with normal limits. This is
a standard Android thermal/ADPF telemetry gap, not proof that Xiaomi/kernel thermal
protection is absent. No thresholds or headroom values were invented. No sustained
thermal/performance or battery-calibration claim is made.

`run-as` context lookup failed on the rooted installation; reports were retrieved
with existing authorized root while all tested app calls stayed in `untrusted_app`.
No general SELinux allow rule was added. At the user's request only
`verifier_verify_adb_installs` was set to 0; normal Play Protect settings remained
unchanged, and subsequent diagnostic APK updates did not show the scan prompt.
