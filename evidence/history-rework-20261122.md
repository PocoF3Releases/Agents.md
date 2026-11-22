# Alioth source history rework (2026-11-22)

LLM-assisted commits in seven alioth repositories were combined per topic,
keeping only the latest implementation, with `Assisted-by: LLM - GPT-6.1 Sol Max`
or `Assisted-by: LLM - Opus 5.5 High` trailers. Human and third-party commits were
replayed unchanged (patch-id, author, date and message verified identical).
No device or vendor fork commit targeted another device; kernel removals are listed below.

| Repository | Old `aosp-17` | New `aosp-17` | Commits |
| --- | --- | --- | --- |
| device_xiaomi_alioth | c006ca4 | 038e686 | 47 → 20 over lineage-23.2 |
| device_xiaomi_sm8250-common | c7b4e34 | 5ca08d7 | 262 → 176 over lineage-23.2 |
| device_xiaomi_camera | 435fa20 | 3997dcf | 11 → 9 |
| vendor_xiaomi_alioth | 32afcdf | 3b1e171 | 30 → 22 |
| vendor_xiaomi_sm8250-common | 1bfaaab | 7585890 | 77 → 71 |
| vendor_xiaomi_camera (GitLab) | 61876c6 | 280f5ba | 6 → 5 |
| kernel_xiaomi_sm8250 | 264bc8e | fe16246 | 796 → 350 over abd144b |

The `<branch>-pre-rework-20261122` backup branches were removed from the
remotes later that day (see [Branch cleanup](#branch-cleanup)). Old hashes cited
in earlier evidence now resolve only in the local archives.

Final trees are identical to the old tips except one intentional change in
device_xiaomi_alioth: the gsm-mode route uses the stock `GSM mode Enable` control
again (the RX macro variant had a wrong premise; alioth has no WSA amplifiers,
`wsa-max-devs = 0`, so neither bit affects the cs35l41 speakers).
The recovery patch series applies with zero pending patches on the new heads.
No build or device run is claimed for these heads.

A follow-up on the same day dropped `TARGET_USES_MINI_GAPPS` from the alioth
overlay topic, so the product uses the default full GMS preset again.

## Kernel

493 LLM commits became 47 subsystem topics. 303 human and third-party
commits (including 72 third-party commits adapted under their original
authors) were kept verbatim. Each topic was placed only where its members
commute at hunk level with every crossed commit, and the replay applied with
no conflicts. Five LLM commits for code that alioth does not build were
dropped: the Goodix FOD fingerprint driver, the Dagu/NU2105 `bq2597x`
variant and the tablet camera request helpers. LLM changes to other-device
paths were also removed:

- other-device defconfigs (generated only by LLM commits);
- the unused `camera`, `camera-bengal`, `camera-xiaomi-tablet` and
  `camera-xiaomi-cas` techpacks;
- the retained `aw8697_haptic_legacy` copy and its Kconfig/Makefile switch,
  so the stock alioth AW8697 driver is selected unconditionally;
- the k81 `cs35l41_k81` DSP copy.

All 185 differing files from the old tip fall inside that list. Generic
kernel fixes in code that alioth does not currently enable, and the original
human commits, stay. No kernel build is claimed for the new head.

A same-day amendment of the defconfig topic (26cf9dd → fe16246) changes only
`scripts/update_defconfig`. With no arguments it now generates and checks only
the tracked device defconfigs. Its help no longer points to a missing
`scripts/update_defconfig.md`. `--check` matches `alioth_defconfig`.
`lineage-20` had no commits newer than the `abd144b` base. The
[fork rebase procedure](../operations/fork-rebase.md) covers later updates.

## Other organization repositories

The same rules were applied to every other PocoF3Releases and
PocoF3Releases-Recovery repository with Assisted-by commits. The code was
rechecked before squashing, with no new defects found in:

- fingerprint lockout and lifetime handling, legacy sensors and
  DSPVolumeSynchronizer;
- C2D surfaces, the USB gadget and tinycompress capture;
- the effect-parameter bounds, the recovery signature check, recovery
  sepolicy and the build/interfaces changes.

| Repository | Old | New | Commits |
| --- | --- | --- | --- |
| hardware_xiaomi | 30655e9 | 3f9c1f1 | 88 → 56 over lineage-24.0 |
| frameworks_av | e5febc2 | 804371e | 6 → 4 |
| frameworks_base | d66ae3d | a1bd3e6 | 11 → 8 |
| hardware_qcom-caf_sm8250_media | b21134c | 48bbfa6 | 2 → 1 |
| vendor_qcom_opensource_usb | 3141c31 | 89fe78f | 3 → 1 |
| external_tinycompress | f5f975c | 531b021 | 2 → 1 |
| Recovery android_bootable_recovery | d8e7603 | 0d55163 | 13 → 4 |
| Recovery android_build | 9171eee | b854a1d | 2 → 1 |
| Recovery android_system_sepolicy | 691cfd5 | c35aa6e | 2 → 1 |
| Recovery android_system_vold | 8058882 | 2484e98 | 2 → 1 |
| Recovery local_manifests | 734da3b | c21776d | 6 → 1 |
| .github (ROM) | fbf07ee | 828c52b | 12 → 3 |
| .github (Recovery) | 0e82a02 | fea05aa | 3 → 1 |
| references_code | 041e06e | afb115c | 7 → 1 |
| Agents.md (this workhub) | 32fff8b | df180f0 | 230 → 8 |

Counts above the upstream base exclude upstream commits. Every new tree equals
its old tip. In hardware_xiaomi, the twelve commits credited with
`Co-Authored-By: Claude` now sit in the Dolby, vibrator and DSPVolumeSynchronizer
topics with `Assisted-by: LLM - Opus 5.5 High`. Third-party commits and human
commits (including the 2025 Dolby links and translations and the human `.github`
update) keep their patch, author, date and message. Single-commit forks with the
standard trailer, display, hardware/interfaces and nxp_nfc needed no rewrite.
The frameworks/base recovery
patch was replayed onto the new head with zero pending patches. No build is
claimed.

The workhub's LLM commits were combined into one commit per run between the
four human commits (October 14 artwork; October 28 display audits; October 30
platform audit), which keep their patch, author, date and message. The 24
commits that credited `Co-Authored-By: Claude` are in the last run, which carries
both Assisted-by trailers. Workhub hashes cited in older evidence, such as
`0f12ead`, resolve in the local workhub archive ref.

## Branch cleanup

Stale branches were deleted from both organizations: 49 in all, kept as
local `refs/archive/<branch>` refs first. They were the 22 rework backups and
the superseded development branches: frameworks_av `bka` (every patch is in
`aosp-16`), frameworks_base `ozo-unimplemented`, kernel `aosp-17-old_base` and
recovery `legacy-native-recovery`. Also removed were the upstream mirror branches
left in the recovery forks (`main`, `main-kernel`, `lineage-24.0`,
`lineage-24.0-caf-sm8450`) and the references_code `LA.UM.8.12` branch, which
`main` already contains. No manifest selected any of them.

Each ROM repository now keeps its default Android 17 branch and, where one
existed, `aosp-16`. The local archive refs sit in the matching `~/evo` checkout,
in `~/references_code` and in the workhub, and the two organization profiles
use bare archives in the private rework task directory. Pending a separate
decision: the references_code reference-source branches (art, bionic, CLO/AOSP
frameworks, external_dng_sdk, vendor_xiaomi_* and the MIUI 14 output) and the
signing-key branches (`aosp-14`, `aosp-15`, `aosp-16-qpr2`, `aosp-17-old`),
whose contents differ and exist nowhere else.
