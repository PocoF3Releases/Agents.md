---
name: aosp-wsl
description: Work on AOSP repo checkouts through Windows and WSL, including scoped source searches, kernel/HAL diagnosis, and authorship-preserving backports. Use for Android platform development, not ordinary Android application work.
---

# AOSP through WSL

Keep Git, repo, source indexing and builds inside the Linux filesystem. Resolve the active checkout instead of trusting an old chat path. Read applicable AGENTS.md; load only documentation relevant to the subsystem.

For Windows-to-WSL commands, use `wsl -d Ubuntu --` with argument arrays. For complex commands, send a Python script over stdin; use subprocess argument arrays and explicit cwd inside it. Avoid nested PowerShell/Bash quoting. Decode ADB output as UTF-8; filter large logs before returning output. Use the ADB installation that actually sees the device, and do not start competing servers unnecessarily.

Search known repositories with `rg -n` or `git grep`; use `rg --files` for filenames. Exclude out/ and proprietary dump trees unless the task concerns them. Use an existing repoindex only after checking its freshness and CLI help; do not regenerate all indexes for a narrow lookup.

For backports, pin source/base/head, compare final behavior and dependencies, and use patch IDs/range-diff to identify equivalents. Preserve imported authorship and the repository's co-author requirements. Inspect the final cumulative diff, not just commit titles.

Use checkout-provided Clang/LLVM/JDK and build wrappers. Run affected checks or module/kernel targets; a full ROM build needs the user's request. Keep static, compile, and on-device evidence distinct. Root-only diagnostics do not establish production SELinux access. Record the tested revision and restore changed device settings.
