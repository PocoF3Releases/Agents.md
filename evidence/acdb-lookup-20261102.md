# ACDB gain-table lookup — 2026-11-02

**Source/binary/device checked; no production change.** Follow-up to the
[audio format check](audio-formats-20261102.md), which captured -19 for a
speaker gain-dependent volume-table lookup. Do not confuse that result with
failure to load the complete speaker calibration bank.

## Read-only core comparison

The shipped 32-bit `libacdbloader.so` imports `acdb_ioctl` from `libaudcal.so`.
The core library's installed/source SHA-256 is
`6cc3ab2bd048867870330f9dbfbad2f11c6e913394fdabd1767af8fd5bf67056`.
Reference contracts are in `references_code`'s SM8250 `mm-audio-cal` ACDB header,
command implementation and loader. The inspected init path loads file data and
metadata into its process; the query did not call the loader/RTAC upload path.

A separate native 32-bit process initialized all seven installed Forte banks
plus `adsp_avs_config.acdb` successfully, then made 40 documented GET queries.
Wire layouts were checked against the header and compile-time size assertions.
Only stock files, configured device/app IDs, two ordinary rates and the observed
volume indices were used. No malformed-file or kernel-boundary test occurred.

| Query | Results |
| --- | --- |
| Common topology | 8/8 succeed for devices 10011/15 and app types 69936/69937/69940/69946 |
| Instance common-table size | 16/16 succeed at 48/96 kHz; nonempty tables 924–4632 bytes |
| Instance gain-step table size | All 16 selected tuples return ACDB_INPUT_PARAMS_NOT_FOUND (-19), for volume indices 0/5 |

Both normal common calibration and its topology can therefore be retrieved
with the current core, files and ABI. The selected gain-step records themselves
are absent. This resolves the observed -19 lookup, not every calibration/error
message or every unqueried volume index.

## Why changing the speaker ID is not a correction

Device 10011 is the stock speaker mapping. Device 15 is also configured for a
different speaker route; it was queried as a counterexample, never enabled.
Its selected gain-step records are absent too. Its topology differs from 10011
for some app types: for example, 69936/69937 select 0x1000a100 on 10011 but
0x10010314 on 15. Common-table sizes differ as well. No provenance identified
those different tunings as interchangeable. Replacing the device ID would
change factory processing without fixing the demonstrated missing lookup.

The generic loader path queries these volume tables separately from common
calibration. A -19 result does not authorize fabricating gains, changing ACDB
IDs, disabling DSP checks or suppressing the log. There is still no demonstrated
perceptible defect or verified replacement calibration to implement. The prior
PCM matrix establishes transport, not audible calibration equivalence. Keep
Dolby/MiSound and all factory tuning unchanged.

## Verification and limits

The private probe builds for the stock ARM32 ABI with Wall/Wextra/Werror using
the checkout toolchain. It loaded the actual installed core and made only
initialization/topology/size calls in its own address space; no calibration
payload was sent to the DSP and no mixer route was changed. Alarm/timeout bound
execution. Audioserver, the audio HAL and mi_thermald kept their PIDs, SELinux
remained Enforcing and kernel taint stayed 0. Kernel:
`4.19.325-Redline-1846f92-cip136`. Task staging was removed.

No production source, preferences, flags, waveform, security policy or thermal
limit changed. No new production build is claimed or required for this lookup.
This does not establish all table contents, acoustic output, all routes, cellular
sidetone or headset behavior. The blocked touch task remains skipped.
Private receipts: `~/evo/.repo/acdb-lookup-20261102`.
