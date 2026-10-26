# Techpack lifetime and DMA follow-up

Observation: 2026-10-26. **source-checked, host-tested, build-tested, device-tested**
within the limits below. This follows the [configured techpack acceptance](kernel-techpack-completion-20261026.md);
its earlier broad coverage is historical evidence, not a claim that every test was repeated.

## Published source

Repository: [kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250),
branch `aosp-17`. Four separate fixes are published by fast-forward; prior history
and approved implementations remain ancestors:

- [LSM short mapping replies](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ac47ab8823797c34157d7ad4069344bb2c5581f3):
  preserve LuK1337's authorship, date and original message from the
  [human upstream fix](https://github.com/LineageOS/android_kernel_qcom_sm8350/commit/2ade12f6b103f186b167d6f327d24afc7419ae4c).
  Four-byte replies no longer read a nonexistent second word. Only the source path
  was adapted; no AI attribution was added to the unchanged human implementation.
- [SHS VMA lifetime](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2e4c2646b05eb275543bd52af320d796e12234b2):
  retain object references and module pins for mapped/forked VMAs. Procfs can force
  file release during removal while mappings survive. Releases now use their own
  private object; faults reject retired generations; old closes cannot clear a new
  shared alias. Existing ABI and fault signal are retained.
- [Video DMA ownership](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7c91a3ca81ef064f93512016bdb8299b5a203cfb):
  balance imported references, device maps and CPU access on failures; reject
  truncated IOVAs with an actual error; free valid zero-address mappings by
  attachment ownership rather than treating the address as an ownership flag.
- [CVP spans and firmware addresses](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c356b4b212bc9f5cddb9432a8364d22c7c4fbefc):
  reject u32 address addition wrap and CVP payloads outside imported buffers.
  VIDC total-plane length semantics remain distinct from CVP payload spans.

No warning suppressions, ABI changes, defconfig changes, tuning, thermal-policy
changes, MIUI policies or system-side source edits. Host fixtures and generated
media remain private build evidence, outside the kernel repository.

## Host and build evidence

- The old actual LSM callback reproduces ASan heap-buffer-overflow on a valid
  four-byte reply. The upstream replacement passes 104 bounded reply/status/owner,
  unmap and reset cases with ASan/UBSan.
- The old SHS handlers reproduce ASan use-after-free following forced procfs
  release, endpoint reopen and an old VMA fault. Actual-function fixtures pass all
  four channels' close/fork/rundown/reopen, allocation failure, module-going and
  retained page-reference cases. These are ordered lifetime tests, not concurrency
  stress or a substitute for kernel sanitizers.
- Extracted video functions pass 35 ASan/UBSan cases: 18 acquisition/reference
  paths, six u32 address boundaries, two mapped-zero frees and nine CVP ranges.
  Fixtures model this tree's actual `void *` DMA-buffer member.
- Final configured `techpack/` W=1/C=2 succeeds with zero diagnostics; this run
  contains 446 distinct C-source sparse checks and rebuilds affected objects.
  Earlier fresh compilation coverage is owned by the linked acceptance record.
- Normal kernel Image succeeds with unchanged compiler warning policy, including
  CONFIG_CC_WERROR. Final cumulative strict checkpatch: zero errors, warnings or
  CHECKs; Git diff checks pass and kernel worktree is clean.

Final Image SHA-256:
`4bb0e4b4e0ae594b9e56dc7ef9e2ddb55f85c6a83b409704b306d684db22d58d`.

## Phone evidence and restoration

Temporarily booted the exact final source/Image; packaged ramdisk preserved.
SELinux enforcing, mi_thermald and audio services running, battery health Good.

- 64 read-only SHS mmap/file-close/fork/fault/unmap cycles across four channels.
  No radio endpoint teardown, outgoing calls or modem policy changes.
- Six Qualcomm hardware video cycles: AVC/HEVC decode and AVC encode twice each,
  generated 640x360 content, 300 frames total.
- 19 PCM cases: repeated microphone/camcorder/recognition/communication capture
  at 16/48 kHz plus playback. No microphone content saved.
- Fresh marked kernel logs: zero critical warning/fault/stall matches.

Original installed kernel restored; boot partition hash unchanged. Exact task
staging removed. No partition flashed and no ROM/recovery release declared.
Raw logs, identifiers and network information remain private.

## Limits

Ordinary PCM capture does not prove sound-model registration or the actual LSM
firmware reply path. Same-client late LSM reply generations remain ambiguous;
this short-reply fix does not change that wire protocol. CVP invalid firmware
requests and valid-zero IOVA allocation are host-tested; their physical occurrence
on Alioth is unproved. Procfs forced-rundown regression is host-tested; phone
checks intentionally avoid deleting live modem interfaces. Optional hardware
variants and the prior PM-enabled failed-resume propagation limitation remain.
This is bounded acceptance, not a universal bug-free claim.
