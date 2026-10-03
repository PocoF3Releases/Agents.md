# First chat on an existing or restored workstation

Start with the task prompt in [README](../README.md), then read only the relevant
record. The public workhub supplies context, not access to a PC or device.

## Install the optional AOSP skill

[skills/aosp-wsl/SKILL.md](../skills/aosp-wsl/SKILL.md) is the portable source for
the locally validated skill. It covers WSL command quoting, bounded searches,
backport attribution and validation scope. Install in the Codex host's skill
folder; Windows Codex and a separate WSL CLI may use different homes.

From PowerShell in this repository:

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex/skills' }
$destination = Join-Path $skillRoot 'aosp-wsl'
if (Test-Path -LiteralPath $destination) { throw 'Compare the installed skill before replacing it.' }
New-Item -ItemType Directory -Path $destination | Out-Null
Copy-Item -LiteralPath './skills/aosp-wsl/SKILL.md' -Destination $destination
```

For a Codex CLI running inside WSL, copy the same folder into that client's
`${CODEX_HOME:-$HOME/.codex}/skills` instead. Do not assume installing in one host
updates the other. Open a new chat and check skill discovery. Existing Review and
OpenAI Docs plugins are optional; ordinary source work needs no extra MCP server.

## Verify access once

- Confirm the distro and checkout. Latest observed A17 root is `~/evo`; older
  records use `~/evo17`. Inspect the effective manifest instead of inferring the
  Android version from the directory name.
- Check only relevant repositories for branch, HEAD and local changes. Use
  [repoindex](repoindex.md) when useful; check freshness before trusting it.
- Confirm the tools required by the task using [tooling](android-tooling.md).
  Checkout Clang/LLVM/JDK remain authoritative for Android builds.
- For device work, identify the ADB server that sees the phone and verify its
  installed revision. No device is needed for an ordinary source review.
- Check remote authentication without printing tokens. Missing local dumps or
  credentials remain explicit limitations; public references are retained.

## Keep context small

Search filenames/symbols before opening files. Bound log output and retrieve
only relevant JSON fields. Pin the base/head for a review or backport; examine
its cumulative diff and dependencies. Run affected checks, expanding only for
new failures or unresolved risks. Record results and remaining work in their
existing owners rather than copying a transcript into startup instructions.

These practices follow [official OpenAI guidance](../references/openai-guidance.md).
They are not measured token savings or a model-specific configuration. Preserve
the selected model and effort; no global prompt, approval or sandbox changes are
required. Installing this skill does not import account memory or authorize
builds, flashing, repository rewrites or unrelated work.
