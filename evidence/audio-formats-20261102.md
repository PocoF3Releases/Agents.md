# Audio format boundary checks — 2026-11-02

Follow-up to the [mixer/route audit](audio-route-compatibility-20261102.md).
**Source/device checked; no production source change.** The kernel, primary HAL,
policy, device-tree routes and approved Dolby/MiSound tuning remain unchanged.

## Actual device and scope

Running kernel `4.19.325-Redline-1846f92-cip136`, SELinux Enforcing, taint 0.
Installed primary HAL SHA-256:
`e4bf45f971ce8296785462bc576d61af21c2f294bd9f4b9adc7e2f93daf11123`.
Installed primary policy SHA-256:
`47e3a6c5fbb95c72cfa0eda1be62152c0749d73f049a50c039181a27039beba4`.
Current source identities remain in the [source map](../state/repositories.yaml).

Two matching 48-case matrices passed, **96 cases total**:

| Path per matrix | Cases | Coverage |
| --- | ---: | --- |
| Capture | 28 | PCM16, packed PCM24, PCM32 and float clients; MIC mono/stereo and UNPROCESSED mono at 48/96 kHz, plus MIC mono at 192 kHz |
| Mixed playback | 20 | Four client formats, stereo at 44.1/48/96/192 kHz and mono at 48 kHz; complete writes and advancing playback head |

The first matrix ran through a privileged `app_process` client. The second ran
as an ordinary application UID in `untrusted_app`, with only RECORD_AUDIO
requested/granted for the test. It used the normal framework AudioRecord and
AudioTrack APIs, without root, shell identity adoption or direct device access.
Root was used only to retrieve its own test report afterward. The temporary
APK was uninstalled and its data removed; the pre-test sleeping display state
was restored. Samples were discarded in memory; playback used zero-valued PCM.
No raw recording, global volume/profile change or audio preference reset.

The root batch retained the same audioserver/audio-HAL/mi_thermald PIDs. The
phone had a separate reboot before the app batch; the same kernel, HAL and
policy identities were rechecked. Boot reason was `reboot,`; the inspected
retained tail showed normal init shutdown activity, not a demonstrated panic.
A cross-reboot PID comparison is not claimed as service-stability evidence.

## What the formats prove

Common policy advertises packed 24-bit primary/deep-buffer output and a
`record_24` input. Live recording configuration and ALSA frontend metadata show
packed clients reaching S24_3LE, including the 192-kHz frontend case. PCM32 and
float recording clients are converted through the advertised packed 24-bit
HAL input. This is expected negotiation, not proof of a native 32-bit ADC.

Mixed output remained 48-kHz stereo S24_3LE at the ALSA frontend. Higher client
rates were accepted/resampled; `isDirectPlaybackSupported` alone does not prove
that these tracks used a direct output. The tests do not certify bit-perfect
high-resolution output, native ADC clock rate, microphone frequency response,
DAC acoustics, offload, external headsets or all concurrent clients. The earlier
speaker/earpiece mixer snapshots own the S24_LE backend observation; packed
frontend and 24-in-32 backend formats must not be conflated.

Private probes compiled with the checkout JDK/D8 and APK tools. An initial Java11
no-desugar probe failed before audio because StringConcatFactory was unavailable;
Java8 bytecode corrected that test setup. No product code was changed for it.
The app did not read privileged ALSA metadata. No SELinux or Play Protect policy
was relaxed to run either matrix. No changed production C/C++ object requires a
new kernel build; the installed kernel's strict build remains attached to its
[original verification](charging-controls-20261102.md).

## Calibration observation and later lookup

The root batch captured a gain-dependent volume-table lookup failure (-19) for
device 10011. The same speaker ACDB mapping exists in the HyperOS platform XML;
all seven Forte ACDB banks match source, stock dump and installed files exactly,
with no extra/missing installed Forte bank. Thus a missing or changed bank was
not demonstrated. These observations do not prove that every ACDB lookup or
DSP parameter is valid, nor that the logged error is harmless in every mode.

The [later core lookup](acdb-lookup-20261102.md) confirms successful common-table
retrieval but absent selected gain-step records, including the device-15
counterexample. Do not replace 10011 or invent calibration data to remove the
message. Audible calibration and the active DSP path retain their limits. Existing sidetone/external-route and acoustic limits remain in the
route audit. The blocked touch task remains skipped.

Private receipts: `~/evo/.repo/audio-formats-20261102`; the separate `app/` reports
record the ordinary-UID matrix and exact test APK identity. No tests or tools were
added to production source repositories.
