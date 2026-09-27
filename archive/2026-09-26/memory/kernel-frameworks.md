# Kernel / Frameworks / Core Platform Durable Knowledge

## Bionic boot failure lesson

A severe Android + recovery boot failure was traced to a Bionic loader change that introduced `thread_local` storage in code loaded too early.

The loader rejected the resulting TLS layout (`PT_TLS` issue) before normal userspace/recovery startup.

The fix moved buffers/state back to caller/local ownership rather than using new TLS in that loader path.

Durable lesson:

> Avoid introducing TLS/thread_local into early dynamic-loader code unless the loader environment explicitly supports that allocation model.

When both Android and recovery fail before userspace, inspect Bionic/loader and common early-init changes before assuming kernel or recovery-specific failure.

## Frameworks/av Xiaomi compatibility

A durable camera/audio compatibility change supports legacy Xiaomi single-role tag lookup in `frameworks/av`.

Keep vendor-compat behavior narrowly scoped.

## SurfaceFlinger / display

Historical only: Android 17 work included an opt-in legacy virtual-display refresh-pacing patch. Its organization fork is no longer tracked; do not assume that patch is present after resync. Check the actual source before using its property.

Kernel display work has also included fixes for exposure-dimming gain and brightness transitions.

## Kernel maintenance

The Alioth kernel has been maintained with Linux 4.19/CIP backports and device-specific display/input/power fixes.

Upstream/backport commits and device behavior changes should remain logically separated where possible.

## Bluetooth/input

Project history includes recovery work for DS4/composite Bluetooth controller behavior.

Treat controller fixes as input/Bluetooth compatibility work, not generic HID hacks.

## Android 17 overlay cleanup

Remove obsolete Android 17 resource overrides when the corresponding framework resource/flag no longer exists.

Examples of retired areas have included old haptic/IMS/signal/DC-dimming/camera-HFR/SystemUI-local overrides.

Prefer deletion of dead overlays over carrying no-op compatibility baggage.

## Verified kernel boot checkpoint

On 2026-09-23, running kernel `10f8a106de65` eliminated the previously observed WiGig probe, invalid ASoC route and white LHBM read errors. Earlier reports from kernel `78d5b0cd5d26` did not test those later fixes. Cirrus PDN and ultrasound failures remain unresolved. Missing DMA-BUF backends still produce warnings during memory queries. See [current boot evidence](../today/2026-09-23-latest-kernel-boot-verification.md). Always verify the running kernel revision before declaring a source fix ineffective.
