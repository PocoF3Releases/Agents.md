# Kernel history cleanup — 2026-11-02

`source-checked`, `history-verified`, `build-tested`. Started November 1;
completed November 2. User explicitly authorized dropping documentation-only
changes, topic ordering and force-pushing. No new kernel functionality or CIP
upgrade was introduced.

## Published result

[e26284f54187](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e26284f541876a3f3f9611740db500f00c7f3aea)
is published on `aosp-17` at the same repository URL. The exact expected old
tip `830fb30974c82ef91080e9295b90169bb97661da` protected the force-push.
The Qualcomm/Lineage base `7646fd34cc76f1ff57f020aaa67b8e6a813db723` is unchanged.

953 custom commits become **880**: the original **158-commit vendor bring-up
prefix stays untouched; 73 documentation-only/tooling commits are omitted;
722 retained development/imported commits are replayed. They keep exact author
and committer identities/dates, subjects, bodies and attribution trailers.
No squashing, invented sign-offs, warning suppression or duplicate marker commits.

Removed commits cover kernel-doc comments/markup and four documentation-parser
fixes. Kept functional warning fixes, type/locking annotations, meaningful code
format fixes and mixed code/comment changes. Existing upstream documentation,
licensing text and functional build-helper documentation remain.

## Review order (oldest to newest)

After the unchanged vendor foundation, 57 cross-topic prerequisites precede the
subsystem blocks. They preserve shared-file predecessor ordering rather than
moving callers and declarations blindly. Within each ordinary topic, original
relative order is retained. The [complete commit map](kernel-history-20261102.json)
lists every retained development commit, removed commit and topic boundary.

| Block | Commits |
| --- | ---: |
| Shared cross-subsystem prerequisites | 57 |
| Build and tooling | 16 |
| ARM64 architecture | 19 |
| Core kernel, scheduling and RCU | 52 |
| Memory management | 14 |
| Common libraries | 5 |
| Crypto and compression | 19 |
| Filesystems | 20 |
| Security | 5 |
| Block and storage | 19 |
| Android IPC and ION | 8 |
| Qualcomm platform and buses | 99 |
| Networking | 67 |
| Wi-Fi | 51 |
| Bluetooth | 3 |
| NFC | 1 |
| USB | 30 |
| Power and thermal | 34 |
| GPU, display and IOMMU | 93 |
| Audio | 28 |
| Camera and media | 44 |
| Input, haptics and sensors | 30 |
| Device tree | 6 |
| Device configurations | 2 |

## Preservation checks

- Two independent replays—chronological without the selected docs, and
  dependency/topic-ordered—produce the identical final Git tree.
- Final versus original differs in 222 paths: 221 C/header paths have **2,062,093
  identical Clang raw tokens** after removing whitespace/comments; the sole
  other path is the deliberately restored `scripts/kernel-doc` parser.
- All twelve generated defconfig files are byte-identical. The resolved Alioth
  production config also matches the prior build; CFI, SCS, KFENCE, SELinux
  and thermal protection are retained.
- `scripts/update_defconfig --check --android-root ~/evo -j 4` passes for all
  twelve devices. No gratuitous config regeneration commit was added.
- Makefile, README, version script, localversion-cip and localversion-st are
  byte-identical. The release is `4.19.325-Redline-e26284f-cip136`.
- All retained commits remain reachable; every retained same-file edit keeps its
  original relative order. GitHub API recognizes all 638 remaining Codex
  co-authored commits. Backup ref
  `refs/backup/kernel-history-20261101/original` and a verified custom-history
  Git bundle preserve the previous branch privately.

## Build evidence

Fresh private-output Alioth Image build with checkout Clang r563880c,
`W=1`, `KCFLAGS=-Werror`, existing `CONFIG_CC_WERROR=y` and four build jobs passed.
After the final ordering refinement, the tree was confirmed identical and the
Image rebuilt to embed the final commit identity. Both passes have zero compiler
diagnostics. The fresh pass emitted 5,275 kernel-doc reports after the requested
documentation/parser removals; these are not hidden or claimed fixed. Ordinary
production code and build flags were not weakened.

Final Image SHA-256: `8a9d8d6d131b743a00b9ef585aedc38266adf439ac14c3822f40814cb321213e`.
Resolved config SHA-256: `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`.

No full ROM build, flash, reboot or new device test. Existing ROM output was
not used as the verification output directory. Generated SCM/version strings
and source line metadata naturally change; no binary-identical Image claim.
The historical sparse/phone checks retain their original identities and limits.
The sparse backlog was not re-audited or declared resolved here. Every retained
intermediate commit was not individually full-built; final-tree equivalence and
the complete final Image were checked.

Private plan, exact removed/replayed mappings, bundle, Clang token receipts,
config comparisons and build logs: `~/evo/.repo/kernel-history-20261101/`.
System-side sources and recovery manifests/patches were not modified.
