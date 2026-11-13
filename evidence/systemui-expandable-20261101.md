# SystemUI ColorOS header build fix — 2026-11-01

`source-checked`, `build-tested`. The ColorOS header imported the Compose `Expandable` function
but omitted the distinct `com.android.systemui.animation.Expandable` class used
by its edit/settings callback signatures. This caused three unresolved type
references and a cascading lambda inference error in QSFragmentCompose.

Added the missing class import, matching the existing footer and shortcut
composables that import both symbols. No callback, layout, styling, animation
or runtime policy was changed. This is an independent framework build fix;
the native-recovery overlay stays separate and byte-for-byte identical.

Published `c500f97ecbbe1b1ead9dd5877b7f42f6709de36a` on `cnb`.
Local framework HEAD `293ec873efba6023f6cd562215eb826569877b7e` includes the unchanged
recovery overlay above that public fix. Its patch diff matches the original
byte-for-byte, and the manifest patch runner reports zero pending patches.
GitHub API confirms Codex co-author recognition on the new public commit.

Validation: `. build/envsetup.sh`, `lunch lineage_alioth-cp2a-user`, then
`m -j4 SystemUI-core` passed, including Kotlin, javac and jar generation.
Module JAR SHA-256: `8ea8c76f70d44719ec8fe6feabac9b8567748b85a3a7f8ed5dd5e76117e71b95`.
Existing compiler warnings were not suppressed. No full ROM build, installclean
or device action was started. Resume the existing ROM build incrementally;
this module result does not claim complete ROM packaging or runtime acceptance.
