---
name: alioth-resume
description: Resume the alioth Android platform workhub after handoff or context compaction, restoring the correct source, verification scope and topic guidance without launching a build.
license: CC0-1.0
---

# Resume alioth platform work

After resume/compaction, reread this file and the repository-root AGENTS.md, then CURRENT_STATE.md and only the topic owner relevant to the user's task. Do not reload the entire history or assume previously loaded skill bodies survived compaction.

This repository is the instruction/evidence workhub, not an Android source checkout. Resolve the actual Linux repo workspace from the current user's task and maintained source map; on this PC the existing workspace is ~/evo. Keep Git/repo/toolchain commands in the Linux filesystem and preserve existing output and unrelated changes. Read the existing `skills/aosp-wsl/SKILL.md` for Android platform mechanics rather than copying it.

Before a requested code change, establish the relevant component root, branch/head, existing edits and specific acceptance scope. Keep source-checked, build-tested and device-tested evidence distinct. A historical artifact/head is not proof of what is running on a device. Use the checkout-provided toolchain and affected checks; do not weaken existing constraints or repeat passed checks without a relevant change or unresolved concern.

For kernel/driver work, use the installed kernel-development skill if available, and read only its relevant workflow. That external skill is not vendored here. For a requested release banner, use imagegen only within the current user's scope. Context7 may fill a specific versioned dependency API gap; checkout source and maintained project evidence remain authoritative for platform behavior.

This skill does not authorize sync, builds, installation, device operations, publication, commits or pushes. Follow current scoped permission for those actions. Report missing tools/access and exact checks honestly; possessing this skill is not proof of build or runtime success.

Provenance: original project workflow text authored for this user's workhub on 2026-10-23, CC0-1.0. No third-party skill text or executable code is included; existing repository and dependency licenses are unchanged.
