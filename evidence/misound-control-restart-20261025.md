# MiSound control loss and audio-server recovery

Observation: 2026-10-25. Source-checked, build-tested and device-tested.

## Failure and fix

Two independent internal agent reviews covered MiSound and Dolby lifecycle state.
MiSound lacked a control listener: after a rival held control through five failed
restores, all handles were released and no automatic recovery trigger remained.
On the phone, a twelve-second higher-priority takeover left music disabled and
the low-priority observer owning the effect after the rival released it.
Reopening MiSound repaired the state; a normal callback alone did not.

[consolidated MiSound fix](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/0de236a93b3dc7dbb59e16219d234e7141c6bd87)
retains the effect/control listener while contested. Control regain resets retries
and recreates the effect, restoring saved tuning before enable. Replaced-handle
callbacks are identity-guarded; audio-server down/up still discards dead handles.
Follow-up agent review found no actionable blocker. This predates the previous
readback fix; that implementation remains intact.

Dolby required no source change. Its persistent owner already observes control and
server transitions, invalidates acknowledgments and restores saved state.
[Translations remain separate](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b653ae1cbb59c26410eae3b1b22e0029781d254a).

## Tests

XiaomiParts incremental module build passed, with existing unrelated TouchFeature
deprecation warnings. Final tested APK SHA-256:
8d4daaeaeb784e5a04eabb3ffcaced87540ef35acb78c87667e3cfcaed7f1da6.

Phone checks passed with SELinux enforcing:
- Fourteen-second MiSound takeover, with refresh during contention to exhaust
  retries; release restored processing without reopening UI afterward.
- Parts process startup during a twelve-second existing takeover; control regain
  restored native enable/music, headset, scene and a non-flat EQ preset.
- Seven-second Dolby control takeover restored native/framework gates automatically.
- Three audio-server restarts restored both effects and the non-flat MiSound EQ.
- Another server restart with both effects requested Off kept native/framework
  gates disabled.
- Rapid capture/playback, communication duplex and actual earpiece/speaker route
  changes passed with the final APK.
- Exact preference hashes were unchanged through control and server tests.
  No crash-buffer entries were observed after the final test reboot.

Capture buffers were discarded and playback was silent; no calls/messages were
made. Native readback is not acoustic acceptance. Bluetooth/USB audio endpoints
and individual third-party VoIP applications were not exercised. Tests used
temporary APK overlays, not a rebuilt/flashed ROM; next ROM build is required.

The public source push was read back. Local recovery overlays were replayed with
an identical final tree; all three recovery preflights report zero pending patches.

Original phone APK hashes, exact saved preference hashes and backed-up audio
properties were restored after removing the temporary module and rebooting.
Android boot completed with SELinux enforcing; temporary phone test files were removed.

History: the readback and control-listener fixes were consolidated into one
implementation with an identical final source tree. Original APK hashes above
remain the identities of the corresponding tests. The final consolidation and
fresh phone checks are recorded in [the complete audit](audio-complete-20261025.md).
