# November 28 Alioth source and build refresh

Synced the current EvoX manifest and all 1,265 checked-out projects. Verified
46 maintained branches, refreshed 681 committer dates, and read back 45 updated
branches after leased force-pushes. All 43 upstream route tips are ancestors.
Authorship, author dates and commit messages were preserved.

Rebased frameworks/base, frameworks/av, native recovery, recovery system
sepolicy and Redline. Redline is based on LineageOS qcom/sm8250 lineage-20
`cc6eef7535ac7d0ffeeb1f6927d7d11bfde3cedc`. Three kernel fixes matched upstream patches by
stable patch ID. The generated Alioth defconfig matched, and all four local
recovery patches reapplied with zero pending.

## Release-signed user OTA

EvoX's upstream OmniJaws resources and SystemUI client migration replaced
the temporary local fixes. The final build includes the matching upstream
Evolver migration. The refreshed framework branch was published and the
recovery patch reapplied.

- `~/evo/out/target/product/alioth/EvolutionX-17.0-20261128-alioth-12.4-Unofficial.zip`
- Android 17, SDK 37, `user`, `release-keys`
- SHA-256 `ac2982ca3c4d7c1c5f31e73664cb49f0c32a467aace0478170d5dce009804812`
- Pinned manifest SHA-256 `24b4d1855c02499482962fee3b95d2556a4a40038b62aadd1a3f6b68cc9e2a5b`
- Kernel `4.19.325-Redline-576e259-cip137`, `#2 SMP PREEMPT Sat Nov 28 07:45:20 UTC 2026`

Verified the whole ZIP and A/B payload signatures, the recovery trust store,
the platform APK signature and the three boot image hashes. Device acceptance
is pending.
