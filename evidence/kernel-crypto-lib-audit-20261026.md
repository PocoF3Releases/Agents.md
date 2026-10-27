# Kernel crypto and library audit — October 26, 2026

> Kernel links were updated to the [finalized history](kernel-history-map-20261027.json). Recorded test identities and measurements remain historical; corresponding rewritten commits are not claims of testing those hashes.

**Follow-up:** [The 27-commit recheck](kernel-crypto-lib-recheck-20261026.md)
reproduced incomplete QRNG requests and records a subsequent separate fix. The
single successful QRNG request below did not establish arbitrary-length support.

**Source/build/host/device checked.** Kernel-only series on `aosp-17`, from
[the preceding GPU audit head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7b0c889d08add642d9022ac87288356030e65d29) to
[the verified final head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8f8e268ff28d5ab26108a19d0615c4ab5c1a2244). All 27 feature commits were pushed;
no Android system/device/vendor source, defconfig, warning policy or thermal
protection change. The installed ROM was not replaced.

## Final implementation

- Qualcomm QCE probe errors now retain allocation failures, balance owned
  resources, keep successful additional engines alive and avoid invalid list
  sentinel lookups. Engine shutdown gates timer/work scheduling before drain.
- QCE device removal no longer invokes a clock helper on an already freed QCE
  handle. A proposed broader mapping/client cleanup was **retracted** after
  independent review found an existing-FD race; it is absent from final history.
- ICE registration propagates ERR_PTR failures, balances character-device and
  bus resources, and gives retained file references a separately allocated cdev.
  Managed owner/name allocations keep devres IRQ cleanup ahead of owner free.
- QSEE application load/start/query overflow failures release their spinlocks;
  a startup allocation failure avoids unlocking a mutex never acquired.
  Native/compat user pointer types retain the existing UAPI layouts.
- Wrapped-key derivation frees only successfully allocated shared buffers on
  second-allocation and secure-call failures. Error values and successful output
  remain unchanged; no keys or secrets are logged.
- MSM RNG registration failures unwind acquired resources. Cached crypto reads
  and old ioctl descriptors synchronize with removal; failed crypto registration
  rolls back the platform driver. FIFO/read retry/entropy policies are unchanged.
- GCM encoded lengths use big-endian types, SHA assembly offsets share matching
  declarations, and radix parent links use appropriate RCU accessors. The GFP
  mask conversion follows integer arithmetic without changing mask bits.
  Library declarations, pointer constants and kernel-doc are corrected.
- The jitterentropy shared-header backport preserves **Ben Dooks**' authorship
  and existing human trailers, with the legacy rotation prototype retained.
  [Original upstream commit](https://github.com/torvalds/linux/commit/965d7286d871b622dcaaafd2e2346b11631584ff).
  Only unused startup bookkeeping is removed from entropy logic; health tests,
  rejection thresholds and timing loops remain intact.

## Build and static evidence

Clang `clang-r563880c`, ARM64, unchanged production configuration. Normal
`Image` build passes without compiler diagnostics. Selected checks use `W=1 C=2`
with `CHECK='sparse --arch=arm64'`; the explicit target architecture prevents the
host sparse default from supplying x86 assumptions. No diagnostic flags removed.

- `crypto/`, `lib/`, `drivers/crypto/`, `arch/arm64/crypto/`,
  `arch/arm64/lib/`: successful configured target pass; **277 C source checks**.
- Filesystem crypto, block inline crypto/keyslots, UFS crypto, Qualcomm crypto/TZ,
  QSEE/SCM and configured hardware RNG: successful target pass;
  **26 C source checks**. Unsupported platforms are not claimed hardware-tested.
- Configured kernel-doc warnings corrected rather than disabled.
- `CONFIG_CRYPTO_MANAGER_DISABLE_TESTS=y` remains unchanged. Runtime checks use
  an external, private module; no test module or fixture is committed to kernel.
- Final Image SHA-256: `dc5d33f039d8e284ec28f9dcfc6047a22c14a42c7b6bdc143f6f60eda6080b34`.

**Nine sparse reports remain visible**, with reviewed conditional lock contracts:
`_atomic_dec_and_lock`, `_atomic_dec_and_lock_irqsave`, `lockref_get_or_lock`,
`lockref_put_or_lock`, `__do_once_slow_start`, `__do_once_slow_done`,
`refcount_dec_and_lock`, `refcount_dec_and_lock_irqsave`, and the consuming
`fscrypt_put_direct_key`. The refcount/atomic/lockref helpers return with different
lock states; unconditional acquire annotations would be false. Once-slow pairing
also crosses the old mutex API's incomplete sparse annotations. No fake lock
annotations or suppressions were added. The three QSEE spinlock reports were
actual bugs and were fixed, not classified as these limitations.

Per-commit checkpatch was reviewed, not certified clean: the imported human
message has an existing malformed review-email delimiter, the old checker does
not recognize the required co-author trailer, assistant commits deliberately do
not invent DCO sign-offs, and formatting checks/vendor-header style notes remain. These are
separate from compiler/sparse findings; Git whitespace checks pass.

## Targeted host tests

Private ASan/UBSan fixtures exercise extracted implementation functions or
explicitly identified error branches with mocked hardware APIs:

- QCE allocation/probe, empty/unmatched engine lookup and timer/work stop gates;
  the narrow remove fixture reproduces the original post-close heap use-after-free
  and passes with the correction.
- ICE: nine registration failures, success/removal, retained-cdev lifetime and
  modeled devres IRQ-before-free ordering.
- QSEE: three overflow branches and startup allocation/error cleanup reproduce
  the original lock defects and preserve errors with balanced final state.
- QTI: first/second allocation failure, secure-call failure and success retain
  output semantics and leave no owned shared allocation outstanding.
- RNG: thirteen probe failures, optional clock/bus variants, held-descriptor
  ioctl and cached-pointer teardown recheck; three module-init outcomes.

These fixtures validate mocked failure paths, not real concurrent hardware
fault injection or secure-world certification. Raw logs and fixtures stay private.

## Phone acceptance and restoration

The final kernel was **temporarily booted**, with original ramdisk hash preserved,
SELinux **Enforcing**, audio services running and `mi_thermald` active.

- **21/21** checks across 14 stages: SHA-1/256/512, HMAC-SHA256, AES ECB/CBC/XTS
  encrypt/decrypt, accelerated and explicitly generic GCM encrypt/decrypt plus
  bad-tag rejection, LZ4/Zstd round trips, jitterentropy and hardware QRNG API
  reads, and 64-entry sparse radix-tree expansion/tagging/shrink/cleanup.
- Observed providers include SHA/AES Crypto Extensions, generic SHA-512/GCM,
  `fips_hw_qrng`, jitterentropy, generic LZ4 and Zstd. RNG API success is not a
  statistical entropy-quality or FIPS certification claim.
- A **4 MiB generated fixture** round-tripped between task storage and unlocked
  media storage with matching content; it was removed. This confirms that path,
  not every FBE credential mode, wrapped-key failure or storage fault condition.
- **6/6 video** decode/encode and **19/19 PCM** capture/playback cases pass.
- Fresh marked kernel logs have no matching BUG/WARNING/panic/RCU-stall/CFI or
  GPU/SMMU fault signatures. Loading the private module produced the expected
  out-of-tree-module taint notice; the module was unloaded.
- Original installed kernel restored, **boot partition SHA-256 unchanged**,
  original slot preserved, Enforcing retained, exact task staging removed.
  No boot partition was flashed and no user files/keys were used by tests.

## Remaining limits

The baseline QCE character driver does not establish safe arbitrary live unbind
with active descriptors/in-flight mappings. The final narrow clock fix does not
claim to solve that older lifetime design; the rejected cleanup is not shipped.
ICE global-list concurrency and inactive IRQ paths are not certified by host
models. No destructive keyslot, RPMB or trusted-app stress operation was run.
A successful bounded phone test does not prove every fault or all algorithms.

[Prior GPU/techpack scope and open display-PM limits](kernel-gpu-audit-20261026.md)
remain separate; the earlier conditional-SRCU findings were not suppressed here.

## Published feature commits

- [29dc4668eb65](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/29dc4668eb65543316216574ef6054d7f78a6ae7) — crypto: jitter - add header to fix buildwarnings
- [8765b7e63eba](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8765b7e63eba4c0e4f72d52c0966b5022d2211c5) — crypto: msm: Correct engine probe ownership and error returns
- [755ea3ce94b8](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/755ea3ce94b8c81eca99d90ec05d2b0497d166e1) — crypto: msm: Preserve DMA byte order and userspace pointer types
- [e6d546c9d8b7](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e6d546c9d8b7c16016ad5130c0537b8708c9543d) — crypto: msm: Return no engine for unmatched lookups
- [615ad5199017](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/615ad5199017f472bcc08dc9a884ac96cdbc2f0e) — crypto: msm: Stop bandwidth work before removing an engine
- [e301628374f9](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e301628374f91d074663ce8ec98b0529c77a62d3) — crypto: msm: Avoid clock access after closing QCE device
- [4cb1211efe56](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4cb1211efe564607a0737ee0c041375d256430db) — crypto: msm: Correct SPS endpoint documentation
- [33d267263ceb](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/33d267263ceb1c46d04e39611993781ca715c2f8) — crypto: qcom: Balance ICE registration and device lifetime
- [1f9b28a1449a](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1f9b28a1449a3b70d6020a72e23f107f4b3f142e) — crypto: arm64: Share SHA assembly offset declarations
- [a8a65dbf576a](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a8a65dbf576accb7b90a5b888c2cfea89dee203e) — crypto: gcm: Use big-endian types for encoded length blocks
- [48bb826d65f7](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/48bb826d65f70e7711c04df05f174c8275cbf406) — crypto: jitter: Remove unused startup bookkeeping and correct documentation
- [a522f6ecabfc](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a522f6ecabfc59d34acc3918ef68be6df098c721) — crypto: rsa: Include the shared PKCS1 padding declaration
- [5ef053a76efe](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5ef053a76efeebc0c491577396a3e02391bd8630) — crypto: asymmetric_keys: Correct key identifier and trust helper documentation
- [3b40f7d5620f](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3b40f7d5620fdb5f853d87af532440a001b79006) — mm: Keep GFP mask arithmetic in the correct type domain
- `4ff949d3ae6a` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ae9f08479fc5dcaa535f9dd4a6b35e028ce1f8e2)) — lib: radix-tree: Respect RCU and allocator type contracts
- `2cd49bf9bbb8` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0746d59ede8a2fed6f3e4301644da34fbda03984)) — lib: audit: Select compat syscall definitions before shared declarations
- `4938d870e1ad` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/fdcc2cee705c01a6b108c3a8568fb444f9f872bc)) — lib: Use shared declarations and explicit formatting types
- `babf6c57cddd` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d084f2c9a5c95a09d20088732221fdd3e890ed7e)) — lib: zstd: Use NULL for the absent dictionary boundary
- `9b4c43f4a62f` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f2f22bf7f3ceb4369c8b0fb7b30f4d3668f14f93)) — lib: Correct allocator, iterator and utility documentation
- `44e69d94e221` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8ebf4845ebbb7fe6bc5f4492d037d76560373e67)) — soc: qcom: Correct inline crypto diagnostics and storage scope
- `9dd69fccf27a` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4b6d42c6382eb6eacd073bfd166698ad052f0136)) — soc: qcom: Free wrapped-key buffers after derivation failures
- `8a2c0522e9d6` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ebfff32bd38c80a3f6beac69827978efedd90ed6)) — crypto: Correct secure-call and UFS parameter documentation
- `b6d2026b1bab` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ee854a518671d27427ceae42bcdf2c303f19e74f)) — misc: qseecom: Preserve userspace types and helper linkage
- `cd0591f150f4` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/265a29b3c593432467e8ab33a61c105bba35d8ae)) — misc: qseecom: Balance locks on application error paths
- `9d7af2934bc7` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9232b04b47c28fcd08c10d3babd3757928395654)) — hwrng: msm: Keep helper state private and remove unused locals
- `0da10242c063` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9232b04b47c28fcd08c10d3babd3757928395654)) — hwrng: msm: Unwind registration and serialize retired handles
- `7c791f0b0e10` ([final history](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8f8e268ff28d5ab26108a19d0615c4ab5c1a2244)) — hwrng: msm: Undo platform registration if crypto setup fails
