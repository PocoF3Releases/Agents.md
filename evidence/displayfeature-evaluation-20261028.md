# Alioth DisplayFeature evaluation — October 28, 2026

Status: flat-mode candidate rejected; Alioth anti-flicker policy published. Manual 60/120 Hz luminance mismatch remains unresolved.

## Observed problem and measurements

The maintainer reports a persistent luminance/color difference between 60 and 120 Hz,
especially at low/medium brightness. It is not merely a brief transition flash.
Installed kernel before the experiment: `4.19.325-Redline-1e45b8c-cip136`.
The initial device snapshot had adaptive brightness enabled; controlled tests explicitly
used manual brightness and retained all original settings for restoration.

Five controlled 120/60 transitions at Android brightness 50 retained backlight 402 and
manual policy value 0.19291338. The later static-gray matrix confirmed physical 60/120
mode selection at Android brightness 20/50/100, backlight 161/402/803 respectively,
with flat mode both off and on. HBM stayed off; SELinux enforcing and thermal control
were retained. These readings do **not** measure panel luminance or color equality.
Screenshots capture digital output, not the panel's optical transfer function.

## Exact stock inputs and framework trace

The local `~/miui/out` is the Alioth Android-13-based stock/HyperOS dump, not another
Xiaomi device. Private input hashes and extracted methods are retained under
`~/evo/.repo/brightness-20261028`; proprietary decompilation is not copied here.
`vendor/lib64/hw/displayfeature.default.so` SHA-256:
`cfe69c918cbb83a826a5073967d14dca9cdd6dd4cdab375ad687771a817bd466`;
ELF build ID `bc60dc74c3793fb03634f9f11e77acce`.

JADX: `miui.hardware.display.DisplayFeatureManager` in `miui-framework.jar`;
existing `ScreenEffectService` and `DisplayContentStubImpl` extraction from
`miui-services.jar`. Manager routes setScreenEffect through Xiaomi HIDL. Refresh case
24 is distinct from color presets and callbacks 10035/10037. ScreenEffectService
uses custom SurfaceFlinger transactions 31035/31037; a direct service import cannot
assume the AOSP framework implements them. PCC callbacks also require integration.

Native disassembly plus targeted Ghidra decompilation:

- `HandleStandard` at ELF VA 0x44564 requests Qualcomm mode 4.
- `setDisplayEffect` at 0x3b0e8 couples Qualcomm mode 4 to panel flat-on parameter
  0x05000000, and other Qualcomm modes to flat-off 0x06000000. This is a color-preset
  companion, not demonstrated per-refresh gamma compensation.
- `HandleFpsSwitch` at 0x49260 calls SurfaceFlinger switching and kernel notification;
  the inspected function does not itself upload separate 60/120 gamma tables.
- `notifyKernelFpsSwitch` at 0x496a4 encodes old stock DFPS notifications
  0x40000000/0x60000000. Current kernel does not handle those notifications; regular
  DRM DMS already selects the panel rate. Do not confuse notifications with a missing
  panel gamma-correction command.
- `threadFuncBacklight` at 0x4188c gates Smart FPS at virtual brightness 0x36c (876).
  Constructor reference at 0x3e7f4 selects `brightness_clone`. AOSP lacks that virtual
  node and its stock transfer path, so 876 must not be copied into Android's legacy
  0–255 brightness overlay or treated as native 0–2047 brightness.
- Public `HandleDCBacklight` at 0x45758 is a logging/no-op entry in this exact blob;
  the separate `processDCBacklight` path exists. Alioth features declare normal DC
  support false and secret DC support true. Do not promise generic stock hardware DC.

The pinned references contain Xiaomi's newer v4 DisplayEffectBase/FlatMode/
MiBrightness stack, including `mi_disp.h`. It is useful contract evidence but not the
same ABI/version as this Alioth blob. No /dev/mi_disp or newer mi_display driver was
blindly imported. Alioth stock uses connector `disp_param`, `mipi_reg`, `panel_info`,
`doze_brightness`, plus backlight `brightness_clone` and stock Qualcomm color APIs.
Current common init/sepolicy still mention some connector paths that are absent at
runtime; adding those names alone would not restore the whole service contract.

## Panel and current AOSP coverage

[Official Xiaomi Alioth DTS](https://github.com/MiCode/kernel_devicetree/blob/e9e9c91d27f4e0a4a32e30c43d7a04f13aafb7f8/qcom/dsi-panel-k11a-38-08-0a-dsc-cmd.dtsi)
provides both flat command sets: C2 2D 27 / C2 2D 07, followed by F7 03. The current
panel retains them and native 60/120 support. Existing timing-switch changes also
restore D1 2E and adjust the settle delay; this evaluation did not revert them or
change clocks, voltages, thermal policy, porches or calibration values.

AOSP Qualcomm composer already applies calibrated color modes/render intents and
color transforms. It does not contain the stock DisplayFeature mode-4/flat coupling.
Current baseline selected DISPLAY_P3 with ENHANCE. Corrected physical comparisons
rejected flat mode as a solution to the refresh-dependent luminance mismatch.
The stock panel XML also contains CCBB/GABB, white-point, software-backlight and
expert-color tuning. Presence of tuning is not proof every feature is enabled or
needed to solve refresh-related color differences. Factory-white-point calibration
is disabled by the inspected stock property.

## Rejected flat-mode experiment

A private kernel experiment exposed only declared flat commands, checking panel
state and bracketing commands with display clocks. Targeted display compilation,
strict checkpatch and full release-config Image passed W=1/KCFLAGS=-Werror;
existing kernel-doc diagnostics were not suppressed. The image retained the exact
installed ramdisk and was temporarily booted; no boot partition was written.

An early app label/preferred-mode test did not reliably select the physical rate.
Its apparent positive result is withdrawn. The corrected buttons used a bounded
root helper and source-checked SurfaceFlinger diagnostic commands, acknowledging
selection only after actual physical mode verification. Actual button taps and the
system refresh overlay were checked. Screenshots cannot measure optical luminance.

With those corrected controls, the maintainer confirmed a visible difference for
all tested combinations: managed sRGB/flat off, enhanced P3/flat on, natural P3/flat
on, and the final natural sRGB/flat-on recheck. No flat-mode interface, forced color
profile, DisplayFeature HAL, guessed gamma table or voltage change was shipped.
Kernel sources were restored cleanly and the clean-source Image rebuilt successfully.

## Published anti-flicker policy

[alioth: Avoid low-brightness adaptive refresh flicker](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/041a887023405ae7aa805fd323f1eb8fb1b692d3)
adds only Alioth FrameworkResOverlayDevice resources: brightness threshold 55,
ambient threshold -1 and blocking-zone rate 120. It uses Android's existing
DisplayModeDirector brightness-zone policy; it is not per-mode gamma calibration.
See the [AOSP resource contract](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/res/res/values/config.xml)
and [multiple-refresh-rate documentation](https://source.android.com/docs/core/graphics/multiple-refresh-rate).

Threshold derivation: the stock cutoff 876 uses virtual 0–4095 brightness. Native
getRealBrightness at ELF VA 0x41f30 maps it to approximately 437–442/2047 depending
on the stock conversion branch. Android setting 55 measured native 442. Copying
876 directly into an Android 0–255 threshold would be wrong.

Resource compilation and linking against the existing framework-res APK passed;
compiled resources contain the intended paired arrays and integer. Runtime tests
used equivalent temporary DeviceConfig values on the normal installed kernel,
original enhanced P3 profile and enforcing SELinux, without a debug mode override:

- Guard off: idle physical 60 Hz; guard on at setting 50: physical 120 Hz.
- Settings 54/55 (native 434/442): guard active; setting 56 (450): guard inactive.
- Setting 100: blocking-zone votes absent.
- Explicit 60 Hz cap: physical 60 Hz, guard votes revoked.
- Battery Saver, with real unplug simulation confirmed: physical 60 Hz and guard
  votes absent. Battery reporting and power mode were restored afterward.
- Six input/idle cycles: all twelve observations remained at physical 120 Hz.

Existing power/thermal policy priorities are retained and thermal protection stayed
enabled. No thermal stress override was tested. Holding 120 Hz at low brightness
can consume more power than idling at 60 Hz. Manual rate changes still exhibit the
panel difference; legitimate calibration data and optical measurements would be
needed before claiming a calibration fix. No all-games, HDR or color-accuracy claim.

The public ROM branch contains only this feature; the local checkout also retains
its existing recovery overlay. No full ROM build or installation of the production
RRO was performed: the source change takes effect in the next ROM build.

## Final restoration and evidence

The phone returned to the unchanged installed production kernel
[1e45b8c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1e45b8cc1cbb9229a464395b5a8e12d8b4bc349c).
Boot-partition hash matched the original; SELinux was Enforcing. Original brightness,
refresh preferences, timeout and enhanced P3 profile were restored. All three test
DeviceConfig keys were removed; real battery reporting restored. The private APK
and task-created device helper/image directory were removed. No production kernel,
composer or DisplayFeature source changes remain from the experiment.

Raw measurements, input hashes, build logs and proprietary reverse-engineering
artifacts remain private under `~/evo/.repo/brightness-20261028`. Public evidence
contains findings and source links only, not proprietary decompilation or identifiers.
