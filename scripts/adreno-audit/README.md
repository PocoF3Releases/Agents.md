# Adreno 650 audit tools

Targeted functional tests for the Alioth Android 17 checkout. These are development
tools in the workhub, not ROM packages or a full CTS/Vulkan conformance certificate.
They do not reboot, flash partitions, change GPU clocks, disable thermal protection,
or replace graphics drivers.

## Build and run

Use Ubuntu/WSL and an already built `lineage_alioth-cp2a-user` tree. The helpers use
its Android 37 NDK sysroot/CRT, JDK, compiler, dexer and APK signer. Native probes use
Clang r584948b; kernel validation used the device's pinned r563880c. Generated UAPI
headers, APKs and binaries are ignored by Git.

```bash
export ANDROID_BUILD_TOP="$HOME/evo"
# Optional; default follows this workstation's Windows platform-tools installation.
export ADB=/mnt/d/platform-tools/adb.exe
python3 build_native.py
python3 build_apk.py
python3 run_app_tests.py
```

Connect exactly one authorized Alioth or set `ANDROID_SERIAL`. The helper installs
only the reserved diagnostic package `org.pocof3.gpuaudit`, verifies its installed
APK hash, and runs three cold-process tests for each ABI. It wakes the screen and
dismisses a non-secure keyguard for the six window tests; it cannot unlock a secure
screen lock. Do not interact with the test activity during presentation tests.

All graphics/KGSL calls execute as `untrusted_app`, not root. Current report/map
collection uses the already authorized `su` because `run-as` context lookup failed
on the tested rooted installation. Root availability is not proof of production
SELinux access; app-domain execution was checked separately.

Each ABI has 62 native checks plus six window checks: KGSL device/context/memory
lifecycles, cached GPU objects, timeline/sync-file fences, GLES shader/pixel and
compute-buffer readback, AHardwareBuffer/EGL import, Vulkan submissions and coherent
readback, and 60 actual window swaps. The wall-clock swap duration is not measured
display FPS. Sparse mapping is disabled by this kernel; its optional regression is
hard-gated to the previously verified kernel and reports unsupported, not success.
Never enable it on an unverified kernel.

## Host regressions and memory tracing

```bash
python3 host-regressions/run.py
python3 deploy_native.py
python3 tools/get_trace_processor.py
python3 capture_gpu_memory.py before
# After independently building and temporarily booting a verified kernel:
python3 capture_gpu_memory.py after
```

Host fixtures regenerate the changed mapping/DMA-BUF functions from the current
checkout and mock external operations. They reproduce the pinned baseline's
2/4-GiB accounting failures without allocating those buffers; current functions run
under ASan/UBSan. They do not prove live OOM handling or concurrent kernel behavior.
Kernel-derived fixtures retain their source notices and [GPL terms](COPYING.kernel).

Perfetto uses Android's ordinary tracing service, a six-second capture, and an
offline trace processor. Its official binary is downloaded only on request and
checked against the SHA-256 pinned in the checkout's v54.0 manifest. Raw traces,
process maps and app reports stay private. No trace is uploaded by these tools.

`kgsl_coverage.py` reads private `strace -f -yy -e trace=ioctl` files, compares
observed request numbers with both the generic and Adreno dispatch tables, and
lists unobserved entries. It does not invoke or fuzz them. Its request-size list is
not proof of complete structure/argument decoding, especially for 32-bit traces.

```bash
python3 kgsl_coverage.py /private/path/kgsl64.trace /private/path/kgsl32.trace
```

`src/property_trace.c` is an optional ioctl-property logger for these native probes
only. Do not inject it globally or preload it into arbitrary applications. It
identified the driver's optional `KGSL_PROP_GAMING_BIN` probe as unsupported on both
ABIs; no fabricated capability response was added.

## Selected Khronos coverage

`deqp-selected-cases.txt` contains 633 deterministic samples from the checkout's
2020 Android must-pass lists: 163 GLES2, 214 GLES3, 187 GLES3.1 and 69 Vulkan cases.
This is a bounded sample, not all cases in those lists. Newer APIs, unsupported
formats, extensions and sample counts can report `NotSupported`; inspect reasons.
The surfaceless runner does not certify window/EGL conformance or protected/DRM use.

Build only the required runner through the normal production lunch:

```bash
source build/envsetup.sh
lunch lineage_alioth-cp2a-user
m -j4 out/target/product/alioth/testcases/deqp-binary/arm64/deqp-binary64
```

Deploy that executable as `/data/local/tmp/codex-deqp64`, its selected case list as
`/data/local/tmp/codex-deqp-cases.txt`, and the **contents** of `external/deqp/data`
and `external/deqp/external/vulkancts/data` under
`/data/local/tmp/codex-deqp-data`. Then run `python3 run_deqp.py before` or `after`.
Explicit 256×256 pbuffer dimensions are required: unspecified dimensions caused an
incomplete default framebuffer in the first harness attempt. The runner retains
failures/warnings/skips instead of converting them into passes.

## Cleanup and boundaries

Uninstall only `org.pocof3.gpuaudit` when finished. Remove only files/directories
created for this audit under its `codex-gpu-*` / `codex-deqp-*` namespace and its own
Perfetto output files; preserve unrelated device data. Generated raw boot images,
proprietary binaries, firmware, credentials, device identifiers and logs are not
part of this directory.

The October 24 [evidence record](../../evidence/adreno-audit-20261024.md) distinguishes
source, temporary-kernel testing and the restored installed build. The toolkit is
not permission to install APKs, boot a kernel, or change another device without the
current user's authorization.
