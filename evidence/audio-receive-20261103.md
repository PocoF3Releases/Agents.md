# Audio response validation — 2026-11-03

Three independent kernel changes retain the production audio ABI and tuning:

- [APR transport bound](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f643345d193b1b473f1e92fb61dad003f769424c)
  rejects a packet whose advertised length exceeds its RPMSG buffer.
- [AFE fixed replies](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/00e702683eed5cbe6155cd7243aace870a58ced8)
  requires the four MIUS notification words and complete LPASS vote handle.
- [Memory-service replies](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d5936f1e0ba3a1fbb2cc22ab3540cfb56788d38c)
  requires complete ASM command/status and AFE/ASM mapping handles before reads
  or completion-state changes. Previously a missing ASM status could count as
  successful unmapping. These are source-demonstrated error paths; spontaneous
  malformed DSP traffic has not been observed on the phone.

**Host-tested:** extracted old callbacks reproduce sanitizer failures. The fixed
transport/MIUS/LPASS matrices pass 110,308 / 260 / 231 cases. The memory-service
matrix passes 600 cases; all 472 valid-response variants also pass the original
code, preserving successful/error replies, waiters, route direction and padding.
No malformed DSP messages were injected into the phone.

**Build-tested:** affected audio W=1/Werror and unlimited Sparse checks pass.
Full Image/modules/DTBs W=1/Werror passes with unchanged production configuration.
Twelve pre-existing trace kernel-doc warnings remain; this is not a whole-tree
Sparse-clean claim. Strict checkpatch reports no findings on the final patch.

**Device-tested:** the final kernel reports
`4.19.325-Redline-d5936f1-cip136`, SELinux Enforcing and taint 0. The ordinary-app
PCM matrix passes 48 cases; six built-in speaker/earpiece duplex switches pass
and restore normal mode. Dolby/Parts saved preference hashes are unchanged.
Audio/HAL/thermal service PIDs remain stable during testing, with no new critical
kernel messages or response-size rejections. Samples are discarded; the test APK
is removed. A diagnostic `run-as` denial required root collection of the completed
app result; the app itself ran normally and no policy was changed.

The same image is persistently installed and boot-complete. Its boot-image
SHA-256 is `0fd2ee5276a56bfd5d65ef47c10b74a35a373732ea196ec1024f791ccee39903`;
the existing Magisk ramdisk is preserved. Temporary device staging is removed.

The earlier `00e7026` image separately passed 48 app PCM cases and 12 route
switches. Its sensor matrix retains the known delayed MIUS flush completions.
The vendor poll/flush wakeup issue, unavailable external audio endpoints and
acoustic calibration remain unverified limitations. See the
[route findings](audio-route-compatibility-20261102.md) and
[proximity record](proximity-contract-20261102.md). The paused touch task stays
skipped; configuration, thermal protection and security policy are unchanged.
