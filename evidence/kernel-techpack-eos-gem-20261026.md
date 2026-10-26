# DSP status, GEM attachment and video EOS follow-up

Observation: 2026-10-26. **source-checked, host-tested, build-tested, device-tested**
within the scope below. Prior [techpack lifetime/DMA acceptance](kernel-techpack-followup-20261026.md)
remains separate evidence; previous tests are not silently counted as reruns.

## Source and behavior

Repository: [kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250),
branch `aosp-17`. Three feature commits retain all preceding history:

- [DSP status bounds](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ed20fff193f8b036ccbf8b036e02fcd0566bd66f):
  get-parameter and path-delay responses require a complete status word before
  reading it; optional no-wait debug logging also avoids a partial-word read.
  Valid four-byte status responses and zero-payload events retain their behavior.
  Rejection releases the session lock. No dormant in-band API redesign.
- [GEM attachment transaction](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bf99671f63481343370bc7a48d30c52d478251f9):
  obtain a replacement attachment before releasing the old one. Allocation failure
  returns its error and preserves recoverable old ownership instead of leaving
  an ERR_PTR while reporting success. Successful replacement clears the unmapped
  scatterlist; later mapping failures can retry or destroy safely. The selected
  ION exporter permits independent concurrent attachments.
- [Video EOS ownership](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ba20abb9cf2d7ef4cf60fa4f25bfb925298dae80):
  mark queued only after HFI accepts; stop on the first failed submission. Hold
  the EOS mutex across STOP insertion and unwind, and release mapped memory
  before deleting a failed STOP node. Earlier accepted nodes remain owned by
  the completion/close paths.

No exact compatible human upstream replacement was established for these fixes;
this is not a claim that none exists. The related
[official Qualcomm video snapshot](https://android.googlesource.com/kernel/msm-extra/video-driver/+/refs/heads/android-msm-redfin-4.19-android11-d1/msm/vidc/msm_vidc_common.c)
contains the same EOS submission/unwind pattern. Human-authored earlier commits
are preserved. No system-source, warning-policy, ABI, defconfig, thermal-policy
or MIUI optimization changes; fixtures remain outside the source repository.

## Host/build verification

- 36 extracted DSP guard cases cover lengths zero through eight and success/error
  status, verifying short replies unlock once and valid four-byte status remains.
- 24 actual GEM attachment/map transitions cover device changes and dirty same-
  device imports, mapped/unmapped old state, failure, immediate destruction and
  retry. Original code fails the expected-error assertion. Replacement leaves
  no live mocked attachments; the tested source matches the committed file.
- Eight actual EOS-function cases cover queue failure/success, retry, STOP unwind
  and completion, with DMA/node counts and mutex ownership asserted.
- These host cases pass strict compiler warnings plus ASan/UBSan. Mocked APIs do
  not establish physical fault injection or concurrent stress coverage.
- Complete configured `techpack/` W=1/C=2 passes with zero diagnostics and 446
  distinct C-source sparse checks. Normal Image passes with zero compiler
  warnings/errors. Cumulative strict checkpatch and diff checks are clean.

Final Image SHA-256:
`53f2daf2adbbfdc0886e5020c7e64f8b821d420adf6188edb9ddfbf517371c60`.

## Device checks and restoration

Temporarily booted the exact final Image/source with the installed ramdisk
preserved. SELinux enforcing, thermal protection and audio services active.

- Six Qualcomm hardware video cycles: AVC/HEVC decode and AVC encode twice each,
  generated 640x360 inputs, 300 frames total.
- 19 PCM capture/playback cases; no microphone content saved.
- 272 ordinary app-domain GPU/native/window checks, native32/64 at 60/120 Hz.
- Fresh marked kernel logs contain no critical warning/fault/stall matches.

Original installed kernel restored; boot partition hash unchanged. Refresh
preferences restored, probe package uninstalled and exact staging removed.
No partition flashed. Raw logs, identifiers and network information remain private.

## Remaining limits

The above normal hardware checks do not induce DSP malformed firmware replies,
ION attachment allocation failure or a full HFI command queue. Those error paths
are host-tested. Secure playback/domain-transition certification and physical
sound quality are not established by these tests.

The broader atomic runtime-PM failure remains open: a void prepare callback
cannot abort already-progressing plane updates after a failed resume. The later
commit guard alone does not protect earlier register programming. A safe fix
needs whole-commit acquisition/error/cleanup ownership, not a local return-type
change; no speculative redesign was included. The earlier apparent framebuffer
IOVA ref leak was retracted because this tree's put_iova is empty and the early
return predates the failed-get balance fix. Optional hardware and late LSM reply
generation limits remain in prior evidence. No universal bug-free claim.
