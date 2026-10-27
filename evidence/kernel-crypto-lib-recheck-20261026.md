# Crypto/library recheck and RNG request completion — October 26, 2026

> Kernel links were updated to the [finalized history](kernel-history-map-20261027.json). Recorded test identities and measurements remain historical; corresponding rewritten commits are not claims of testing those hashes.

**Source/build/host/device checked.** Reviewed all 27 commits ending at
[the previous audit head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8f8e268ff28d5ab26108a19d0615c4ab5c1a2244), including their cumulative diff and
callers. They remain unchanged ancestors with original authorship intact.
One additional, separate fix is pushed on `aosp-17`:
[Fill crypto RNG requests across partial hardware reads](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/25ddc9a7d3619f9ab76b962b009679eaea3851a0).
No system-side source, defconfig, warning policy or thermal protection change.

## Real issue found during repeat phone testing

The first phone crypto repeat returned `-EFAULT` at the hardware QRNG stage.
`msm_rng_direct_read()` legitimately returns word-sized, possibly partial hwrng
reads. `qrng_get_random()` incorrectly assumed one such read filled an arbitrary
crypto API request. Small/odd lengths necessarily failed; larger requests could
fail after partial progress. This defect predates the 27 reviewed commits.

A before-fix probe made 104 requests at 13 lengths: **88 failures**, no boundary
corruption. Requests of 1/2/3/5/7/31/32/33/64/65/128 bytes failed in that run;
4- and 16-byte requests succeeded. This is API failure evidence, not an entropy
quality measurement or a diagnosis of any specific app failure.

The new callback reads through an aligned 64-byte scratch buffer, copies only
actual returned bytes, and continues until the requested output is complete.
It rounds the final hardware read to a word and discards unrequested tail bytes.
It checks pending signals, bounds consecutive empty reads to five, and clears
scratch data. Persistent starvation still returns an error, not fabricated data.
The hwrng reader, its poll/retry limits, clock/bus handling, quality setting and
lifetime lock remain unchanged. The crypto adapter can make several such reads.

The exact-fill rule follows [Brian Masney's upstream correction](https://github.com/torvalds/linux/commit/a680b1832ced3b5fa7c93484248fd221ea0d614b)
and the odd-tail rule follows [Ondrej Mosnacek's follow-up](https://github.com/torvalds/linux/commit/16287397ec5c08aa58db6acf7dbc55470d78087d).
Those patches change a different Qcom driver; this is a downstream adapter,
**not a claimed cherry-pick or a new human-authored upstream patch**. Existing
human authorship and the prior jitterentropy backport are preserved.

## Investigation of all nine sparse reports

The warning-owner implementations are unchanged by the 27-commit series.
Review traced success, failure, last-reference, racing-reference and IRQ states
through the actual headers and selected callers, including block keyslots,
UID/backing-device refcounts, dcache, fscrypt and TCP port randomization.

| Reported function | Actual contract and result |
| --- | --- |
| `_atomic_dec_and_lock` | Nonfinal decrement returns 0 unlocked; final decrement returns 1 locked. If a reference appears before the slow decrement, it unlocks and returns 0. Source and phone cases agree. |
| `_atomic_dec_and_lock_irqsave` | Same contract, with saved IRQ state owned only on successful acquisition. Phone cases preserve both initially enabled and disabled IRQ states. |
| `refcount_dec_and_lock` | Success returns true locked; nonfinal/saturated paths return false unlocked. Phone checks include sticky `UINT_MAX` saturation. |
| `refcount_dec_and_lock_irqsave` | Same refcount contract with IRQ save/restore. Selected callers restore only success-owned flags; phone cases agree. |
| `lockref_get_or_lock` | Returns 1 unlocked after increment, or 0 locked for zero/dead counts. Phone checks cover negative, zero and positive counts. |
| `lockref_put_or_lock` | Returns 1 unlocked after decrement, or 0 locked when count is at most one. Dcache callers follow this inverse-success convention; phone cases agree. |
| `__do_once_slow_start` | True keeps the mutex; false releases it. The old mutex declarations lack sparse context annotations, while this helper has an acquire declaration and existing false-path bookkeeping. Phone raw-helper and concurrent macro checks pass. |
| `__do_once_slow_done` | Sets done and releases the mutex, then schedules jump-label cleanup. Phone checks drain deferred module references and confirm once-only execution. |
| `fscrypt_put_direct_key` | Only the final reference unlinks under the shared table lock, unlocks, then frees. Lookup increments under the same lock. Source review and an exact-function host fixture confirm ordering; this private helper was not directly invoked on the phone. |

**No runtime locking defect was found in these nine reports.** Six library
helpers intentionally have conditional return lock states; the fscrypt caller
inherits the refcount analysis gap. The two slow-once reports also expose old
mutex annotation debt. [Current upstream mutex declarations](https://github.com/torvalds/linux/blob/master/include/linux/mutex.h)
have richer analysis support, but a broader annotation backport is not a runtime
repair. No false unconditional acquire contracts, new dummy annotations or
warning suppressions were added. All nine reports remain visible.

## Fresh build and host evidence

- Combined configured `W=1 C=2 CHECK='sparse --arch=arm64'` crypto/library and
  adjacent-encryption targets pass: **301 source checks**, exactly those nine
  sparse diagnostics, no compiler errors/new reports.
- Normal ARM64 `Image` and matching private test modules build successfully
  with checkout Clang `clang-r563880c`; production configuration hash unchanged.
- Image SHA-256: `1e2bd26ebca9c92d7e94076354831a616a33e54d4a84665c73022962c7daf564`.
- ASan/UBSan exact-callback fixture reproduces baseline odd/partial-read failures
  and passes fixed unaligned sizes, partial progress, transient empties,
  exhausted/reset empty budget, signals, removal/lock interruption, null/zero
  cases, output guards and scratch clearing. Its baseline is pinned to the
  pre-fix commit, not a moving HEAD. Mock hardware is not physical RNG testing.
- The existing RNG lifecycle fixture still passes. An exact
  `fscrypt_put_direct_key()` host fixture checks two nonfinal puts and final
  unlink-while-locked, unlock, then free, with controlled lock/refcount mocks.
- Separate source reviews found no introduced regression in the other 27
  changes. No test source/module/fixture was committed to the kernel.

## Final phone checks

The new kernel was temporarily booted with the installed ramdisk preserved.
SELinux stayed **Enforcing**, audio services and `mi_thermald` remained active.

- **256/256 QRNG requests** pass, with zero buffer-guard errors: 16 attempts each
  at 1/2/3/4/5/7/16/31/32/33/64/65/67/128/1024/4096 bytes, all using an unaligned
  destination. Generated bytes were never logged or published.
- **33/33 actual lock-contract cases** pass: atomic/refcount, IRQ restore,
  saturation, lockref and raw slow-once paths. Four workers make **512 once-only
  attempts** at one callsite, with exactly one callback/winner. Workers join and
  deferred once-work module references drain before unloading.
- **21/21 crypto/library checks** pass: hash/HMAC, AES modes, accelerated and
  generic GCM plus bad-tag rejection, LZ4/Zstd, jitterentropy/hardware RNG API
  reads, and radix-tree operations. This repeats the previously failed stage.
- Generated **4 MiB storage** round-trip, **6 video** and **19 PCM** cases pass.
- Fresh marked kernel logs show no matching critical BUG/WARNING/panic/stall/CFI
  or GPU/SMMU fault signatures. The expected private-module taint notice is
  separate; all private modules were unloaded.
- Original installed kernel restored, original slot and boot-partition hash
  verified unchanged, Enforcing retained, exact test staging removed. No boot
  partition flash, data wipe or user key operation was performed.

The test operation counts are bounded; completion/deferred-work waits do not
have a kernel-side timeout if a helper malfunctions. These results are not
statistical RNG/FIPS certification, exhaustive races or hardware fault injection.
The fscrypt host model does not certify every real FBE policy or credential mode.

[Prior audit, commit list and existing live-unbind/hardware limits](kernel-crypto-lib-audit-20261026.md)
remain applicable. Prior GPU/display/shutdown limits are not closed by this work.
