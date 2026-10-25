# Turnip evaluation and restoration — October 25, 2026

**Build/device tested within the scope below; cancelled by the maintainer.**
No Mesa driver, property-policy change or performance tuning was committed to
ROM sources or pushed. Stock Qualcomm Vulkan is restored on both ABIs.

## Candidate and actual selection

The user's Mesa clone remained unchanged. A separate archive of
[Mesa 26.2.5](https://gitlab.freedesktop.org/mesa/mesa/-/tree/mesa-26.2.5) built
32/64-bit Vulkan-only Turnip with the KGSL backend, Android API 37/NDK r30,
static C++ runtime and no Gallium/EGL/GLES replacement. Runtime identified
Turnip Adreno 650, Vulkan **1.3.354**. Stock GL/EGL/HWC and firmware were retained.

Temporary root bind mounts replaced only the two Vulkan HAL paths; game process
maps and its initialization log confirmed it actually loaded Turnip. This
corrects the earlier historical package-opt-in experiment that still loaded stock.
It does not establish production APK selection or packaged SELinux compatibility.

## Bounded results

- Both ABIs passed 62 native checks. Each ABI also passed three app-domain runs
  of 62 native plus six window checks. These are targeted tests, not conformance.
- Seven depth/LRZ cases passed on Turnip and on the stock control, including
  direction switches and depth layer/mip preservation with GPU pixel readback.
- Endfield entered a playable scene. One completed stock scene-loading trace
  recorded **163 KGSL page faults**; the game continued. Prior fault work recorded
  similar low-address reads. This establishes a reproducible observation, not
  whether the game, compiler or proprietary driver caused it.
- A 29.91-second Turnip steady capture had 765 frame-arrival events, mean interval
  39.15 ms, max 43.65 ms and zero intervals over 50 ms. A repeat in the default
  view averaged 36.37 ms. Stock's separate capture averaged 17.40 ms. These
  observations flagged a substantial slowdown, not a controlled universal FPS
  benchmark or proof of thermal/performance equivalence.
- The completed Turnip steady trace had no recorded GPU faults or trace errors.
  The earlier startup trace also had none, but complete scene-load coverage was
  not established for every Turnip run. Do not claim the loading fault is fixed.
- Shader compilation produced repeated denied-read warnings for unlabelled
  `vendor.mesa.*` properties. No broad vendor-property grant or production policy
  workaround was added.

A temporary `debug.mesa.tu.autotune.algo=profiled` diagnostic was started, but the
maintainer cancelled before its result was accepted. Do not record it as a fix.

## Fault interpretation

Earlier snapshot analysis observed low read addresses `0x140`, `0x240` and `0x80`
attributed to UCHE/HLSQ, without a matching freed-allocation diagnostic. The
captured command buffers used ordinary high GPU virtual addresses; bindless
indices must not be interpreted as raw pointers. Originating game API arguments
and full descriptor contents were not captured, so game versus driver ownership
remains unresolved. No speculative kernel null mapping or log suppression was added.

The one-shot diagnostic changed page-fault policy from `0x0` to `0x2`, captured
one snapshot and restored `0x0`. Its halt/replay is diagnostic behavior, not proof
that normal policy was resetting the game. `reset_count` also increments on
ordinary GPU starts and is not a crash counter. Count explicit fault events and
inspect snapshot/dispatcher context. Printk time and `/proc/uptime` diverge across
suspend on this build; use log deltas or Perfetto correlation. Ratelimited dmesg
message counts do not replace ftrace event counts.

## Restoration and limits

The game/test app was stopped before removing the exact Vulkan bind mounts.
The reserved GPU audit APK was uninstalled. The autotune property was cleared
back to its original empty value; no persistent driver module was created.
Final stock SHA-256 readback:

| ABI | Stock `vulkan.adreno.so` SHA-256 |
| --- | --- |
| 64-bit | `e3eeb9d88850d4ee70eb723162301f0f020ddba89069ea9f927d3d1572870f06` |
| 32-bit | `928063d44d3f0b428462e222f7d9cd396db7de2bea9b15485076f4010abb6525` |

Final SELinux state was enforcing. No thermal/governor/clock override was made;
thermal protection was retained. Temporary trace/staging artifacts remain private
under `~/evo/.repo/mesa-turnip-20261025/`; they are not production inputs.

The user explicitly said **forget Turnip**. Do not restart this experiment without
a new request, replace stock drivers, or promote the preliminary no-fault result
into a production-fix claim. OnePlus donor retesting was also declined.

## Reusable source findings

Adreno 650 belongs to Mesa's **A650/gen3** group, with hardware LRZ direction/depth
view tracking; pre-A650 CPU-only behavior does not apply. Preserve A650 quirks and
cache handling. [Mesa LRZ documentation](https://docs.mesa3d.org/drivers/freedreno/hw/lrz.html).

`GraphicsEnvironment.chooseDriver` requires a system graphics-driver package
(`MATCH_SYSTEM_ONLY`), valid ABI/metadata and namespace dependencies. Installing a
user APK and setting an opt-in is not proof of driver selection; inspect process
maps/logs. Mesa's documented no-unused-arguments guards around static-libstdc++
are necessary for correct cross-compiler feature probes. Isolate pkg-config from
host libraries. No Context7 re-resolution is needed for this known Mesa library:
`/git_gitlab_freedesktop_org/mesa_mesa`; use only a specific new documentation gap.
