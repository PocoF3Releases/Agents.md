# Full Dolby and MiSound follow-up — October 25, 2026

**Source-checked, host-tested, build-tested and device-tested within the scope
below.** The diagnostic fix is pushed; temporary device artifacts were restored.
[Existing accepted audio work](../memory/dolby-audio.md) remains the baseline.

## Requested scope

Trace the complete Qualcomm/Alioth subsystem through historical framework/vendor
code, the provided stock extraction, current AOSP sources, packaging/configuration
and actual device behavior. Find useful missing integrations, implement compatible
fixes, test affected paths, preserve saved settings and approved behavior, and
publish verified source changes. Keep translation changes separate. No questions
are needed for routine choices; no blanket optional DSP activation is justified.

## Coverage expansion

- The user's shorthand `~/references_code/vendor/xiaomi/frameworks/av` resolves
  to `~/references_code/android-t-qcom/vendor/xiaomi/frameworks/av`: 170 files,
  including AudioFlinger/policy/client/media extensions and Dolby implementation
  headers. Search this in addition to the two ready indexed source trees.
- The earlier [87-path audit](audio-complete-20261025.md) covered shipped vendor
  ELFs and selected DSP programs, not this entire framework layer. Reuse its
  private pseudocode and limitations instead of repeating blanket decompilation.
- Fresh MiSound APK and `miui-services.jar` JADX passes finished with 15 and 12
  reported errors respectively. Useful bodies exist, but the errors are not
  silently counted as successful decompilation. The stock framework MiSound
  wrapper was separately extracted from `miui-framework.jar`.
- Current relevant ROM source repositories started clean. Device/root were
  available; SELinux was enforcing. This observation is not installed-source
  hash verification or new functional acceptance.

## Investigation order and acceptance

1. Build a component/caller/property/ABI coverage matrix for framework AV/base,
   stock apps/JARs, DMS/native effects, HAL/GEF, DSP resources and product policy.
2. Correlate every proposed integration with the actual shipped Alioth binary,
   required callback/parameter contract, configuration gate and current owner.
3. Reproduce a real missing behavior or defect before changing sources. Keep
   optional/OZO/spatializer/voice/hearing paths explicitly qualified; compatible
   code presence alone is not activation authority or acoustic proof.
4. Implement small independent changes, add meaningful private/host regressions,
   compile affected production modules, and test reversible phone deployments.
   Preserve exact preferences, effect states and original artifacts for rollback.
5. Recheck normal playback, recording/VoIP, route/lifecycle/server recovery for
   affected changes; keep endpoint-specific limits explicit. Review, push and
   update final evidence only after passing relevant checks.

## Integration findings and boundaries

- The shipped MiSound descriptor has flags `0x07460208`; it advertises Xiaomi
  app/standby/stream-volume hints. Its stream-volume command handler validates
  eight input bytes but otherwise does nothing. Do not import that hook merely
  because the reference advertises it. Blacklist entries require parameter 6 values beginning with `*`; app hints only
  affect configured entries. Standby clears aggregate state. No missing configured
  caller was established, so these are not blanket integration requirements.
- Alioth DMS `notifyAudioTrackChange` forwards to its registered VQE callback.
  The reference calls it for non-fast playback/record lifetimes. This is not by
  itself proof that an owner registers the callback or that global VQE should
  be enabled. A scan of stock libraries, service executables and 693 APK/JAR DEX entries
  found no concrete IVqeCallbacks owner. Existing libswvqe uses IDmsCallbacks;
  adding a dead bridge or enabling global VQE is not justified.
- The stock Java services contain route/orientation/volume Dolby tuning and
  effect-implementer/spatializer policy. Current XiaomiDolby already owns several
  corresponding controls; avoid creating a competing framework controller.

Private inputs, hashes, JADX errors, native pseudocode references and stage results
remain under `~/evo/.repo/audio-full-subsystem-20261025/`. No proprietary source,
private logs or original binaries are included in this knowledge record.

## Completed coverage and checks

- Revalidated all 87 ELF and 38 data/firmware inputs against the earlier audit: all
  125 hashes match. Inventoried 46 stock framework audio ELF inputs.
- Newly decompiled five selected implementations: AudioFlinger (80 functions),
  audio client (189), policy manager (63), policy service (23) and media (118).
  All 473 selected functions completed without reported decompiler failures; this
  does not establish semantic correctness or complete firmware coverage.
- [Component/caller decisions](audio-subsystem-components-20261025.csv) cover 38
  groups. Native Alioth ABI wins over incompatible reference interfaces: retain
  one U8.24 QDSP pregain scalar and skip unsupported private metadata commands.
- Dolby OTT control belongs to Dolby Vision/video, not Atmos audio. OZO, hearing
  calibration and spatializer interfaces do not establish supported Alioth UI.
- Stock MiSound UUID/parameters match current Parts. Separate native/framework
  enable gates and current recovery ownership remain necessary; no competing
  service or optional DSP activation was introduced.

## Diagnostic correction and outstanding acceptance

The [published frameworks/av correction](https://github.com/PocoF3Releases/frameworks_av/commit/eecb939f5835ad998f04f34e3b760c9511b920f0) casts the libcutils int8_t support
property to bool before ostream output. Previously the dump emitted a control
byte instead of numeric 0/1. This changes diagnostic formatting only. A host
regression compiled the actual production expression: baseline failed, corrected
expression passed for both states. Independent review found no behavior change.

Incremental `libaudioflinger` and `audioserver` builds both exited successfully.
AudioFlinger is statically linked into audioserver in this build; a nonexistent
shared-library replacement would not verify it. Candidate/original audioserver
DT_NEEDED sets match (70 libraries). No production test files were added.

The installed baseline passed saved MiSound Off / Dolby On readback, rapid
voice-message and communication transitions, and acknowledged earpiece/speaker
routing. These are baseline results, not candidate acceptance or acoustic proof.
The final candidate ran under enforcing SELinux and printed numeric `support=1`
with `control=qdsp`. Accepted checks:

- Saved Dolby On / MiSound Off readback after the server restart.
- Rapid record/playback start-stop, capture-only/playback-only communication
  bypass, duplex mode and actual earpiece/speaker route acknowledgments recovered
  processing state; final audio mode was normal.
- Six MIC/voice-recognition/voice-communication recording cases at 16/48 kHz
  passed with advancing timestamps; AEC/NS were enabled for communication.
- AAC and Opus in-memory voice-message encoding reached EOS; eight capture
  restarts passed. Samples were discarded without writing recordings.
- Silent 48 kHz PCM playback rendered 180480 frames with zero underruns. This
  does not prove audible speaker quality.

The first deployment failed because a bind from the nosuid data filesystem
blocked init's SELinux transition (`nosuid_transition` / `execute_no_trans`). This
was a diagnostic deployment problem, not an audio-policy defect. A RAM-backed
executable mount allowed the ordinary audioserver transition with enforcing
policy unchanged. An early state read also preceded app recovery; the final run
waited for recovery and passed. No permissive setting or production policy
exception was introduced.

The rollback guard restored the original executable SHA-256 and removed both
temporary mounts. Both preference-file hashes remained identical, normal saved
Off/On readback returned, Android remained booted and SELinux enforcing. Initial
property reads from shell were incomplete: vendor-property access is restricted,
and root reads reveal values hidden from shell. Therefore blank shell values
were not treated as valid originals, overwritten, or claimed as an exact property
restoration check. No test explicitly wrote those properties.

All nine tracked source worktrees remained clean; only frameworks/av advanced by
the one-line diagnostic fix. Approved Parts/Dolby implementation and separate
translation history are unchanged. The phone retains its original executable;
the pushed change needs inclusion in the next ROM build. Physical Bluetooth,
USB/headset, remote-call acoustics and optional DSP tuning retain prior limits.
No claim of exhaustive hardware/firmware correctness follows from this audit.

## Final rebuild-readiness review

A second source review of the same final heads found no actionable regression
or proven unused code to remove. Independent MiSound and Dolby reviews checked
saved Off intent, profile/custom variant isolation, EQ/reset persistence, native
readback, bounded control recovery, server-monitor ownership, communication and
Qualcomm game routing. Keep the legacy activity/tile aliases: existing shortcuts
and pinned Quick Settings tiles still use them. No implementation or translation
resource was changed during this review.

The incremental combined target check passed for `XiaomiParts XiaomiDolby
libtinycompress audioserver` with `lineage_alioth-cp2a-user` and six build jobs.
Ninja found the targets current (zero compile steps); this confirms graph and
artifact freshness, not a new full ROM build. Parts and Dolby APK hashes still
match the accepted installed-build identities; both tinycompress ABIs and the
corrected audioserver artifact are present. All 637 scoped Parts/Dolby XML files
parsed successfully. Reviewed translation commits remain resource-only and
separate from implementation history. Source worktrees are clean and maintained
Dolby/AudioFlinger/tinycompress remote heads match.

No phone was visible to Windows ADB during this final review, including after
reconnect/server restart, so there is no new runtime claim. The preceding
enforcing candidate acceptance and exact saved-preference restoration remain
the applicable device evidence. Sources are ready for the requested ROM rebuild;
the rebuilt release itself still needs its normal install/smoke acceptance.
Private review/build/artifact receipts: `~/evo/.repo/audio-final-recheck-20261025/`.
