# October 25 release-copy review

Publication was subsequently confirmed by the maintainer on October 28; October
25 is now the baseline for later copy. The historical drafting review below
retains the information available at that time.

Draft copy/artwork only; no Telegram message was sent.
The published baseline remains October 20, as confirmed by the maintainer.
Saved posts, the semantic release ledger, pinned baseline/net diffs and later
audio fixes were compared. Exact October 20 ZIP/source identity is unproven;
previously announced topics are excluded conservatively.

## Current artifact

EvolutionX-17.0-20261025-alioth-12.3-Unofficial.zip, recomputed SHA-256:
bbb4730e6f4e2440f09202490ceef7b660574ee44e6df7a9641f9f92338a4426.
It matches the checksum sidecar. The installed
[smoke check](release-smoke-20261025.md) keeps its short-test scope.
Installed tinycompress hashes additionally match build output:
32-bit 72a637d78bb496ea36f9d5be24c2aa3512f0d643cd23b165cd8287089a69caa2;
64-bit 11b3f19c2801491cb52d8843bf681a4c25e96c939d04db77f967f7f18d4f60cd.

## Eligible groups

- Native Qualcomm game backend, Dolby restart, MiSound EQ and control/native-state
  recovery: [audit and installed identities](audio-complete-20261025.md).
- Interrupted compressed reads and legacy audio callback compatibility:
  [regressions](voice-message-recovery-20261025.md). No universal messaging-app cure.
- Exact stock FCSAM parameter packaging; native 32-bit initialization and copy
  target passed. No acoustic-zoom or 64-bit initialization claim.
- Thermal failure/retry status, actuator correction and thermal-status strings.
- New freeform gesture, face-animation toggle, status-bar/media-art option and
  Now Playing saved songs.
- App Lock fields/dialogs and scrollbars, NFC settings entry, selected-font/
  emoji fallback, blur, media-art swipe and primary-session fixes.
- Zstd/zRAM, Bluetooth bounds, USB short reads, UFS handling, JPEG buffers,
  CamX session guards and empty fingerprint-removal completion.

## Exclusions

No rebase/import/config regeneration, test, documentation or tooling is a feature.
Existing recovery/PIN/installers, Parts/Dolby redesigns, AC-4, haptics, WireGuard,
camera modes, Wi-Fi startup and October 20 feature announcements are omitted.
No new security patch date, generic FPS/battery gain or Wallet guarantee is claimed.
Unused other-device/TV/foldable modules are excluded.

The maintainer says refresh-rate work is still imperfect. It is omitted from
both posts and the banner without changing the underlying technical record.
The initial three-strip banner was rejected. Final direction keeps the earlier
phone render, uses only the supplied example's two-column/six-card arrangement,
and generates a new industrial canyon, viaduct and harbor environment.

## Visual sources and deliverables

Inspiration research:
[official Endfield visuals](https://endfield.gryphline.com/en-us) and
[developer environment presentation](https://blog.playstation.com/2026/01/16/arknights-endfield-hits-ps5-on-january-22-new-action-rpg-gameplay-details-revealed/).
No external image pixels were incorporated. The built-in imagegen tool was used.
Three optical cameras, separate rimmed microphone, flash/punch-hole, spelling,
date, six-card hierarchy and new feature copy were visually inspected.

[Full post](../state/telegram-20261025-full.md) ·
[short post](../state/telegram-20261025-short.md) ·
[banner](../state/assets/evolutionx-alioth-20261025-banner-v2.png) ·
[exact prompt](../state/assets/evolutionx-alioth-20261025-banner-v2-prompt.txt).
