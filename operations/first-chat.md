# First chat on an existing or restored workstation

Use the task prompt in [README](../README.md), then the relevant record.
The workhub provides context, not PC/device access.

## Install the optional AOSP skill

October 9: the local skill was installed for Windows Codex and WSL Codex.
This is a host checkpoint, not proof of discovery in every client/session.

[skills/aosp-wsl/SKILL.md](../skills/aosp-wsl/SKILL.md) covers WSL quoting, bounded
search, backport attribution and validation scope. Install in the active Codex
host's skill folder; Windows and a WSL CLI may have different homes.

From PowerShell in this repository:

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex/skills' }
$destination = Join-Path $skillRoot 'aosp-wsl'
if (Test-Path -LiteralPath $destination) { throw 'Compare the installed skill before replacing it.' }
New-Item -ItemType Directory -Path $destination | Out-Null
Copy-Item -LiteralPath './skills/aosp-wsl/SKILL.md' -Destination $destination
```

For WSL Codex CLI, copy into `${CODEX_HOME:-$HOME/.codex}/skills`. Installation on
one host does not update another. Check discovery in a new chat. Review/OpenAI
Docs plugins are optional; source work needs no extra MCP server.

## Verify access once

- Confirm distro/checkout. Latest observed A17 root is `~/evo` (older: `~/evo17`);
  verify the effective manifest rather than inferring Android version from a path.
- Check relevant repos for branch, HEAD and local changes. Use [repoindex](repoindex.md)
  when useful, checking freshness.
- Verify needed [host tools](host-tooling.md)/[Android tools](android-tooling.md).
  Checkout Clang/LLVM/JDK remain authoritative for builds.
- Device work: select the ADB server seeing the phone and verify its installed
  revision. Source review needs no device.
- Verify authentication without exposing tokens. Record missing dumps/credentials
  as limits; retain public references.

## Keep context small

Discover filenames/symbols before reading; bound logs and JSON output. Pin
base/head for reviews/backports and inspect cumulative diff/dependencies. Run
affected checks, expanding for failures/concerns. Update existing fact owners,
not transcripts in startup files. See [OpenAI guidance](../references/openai-guidance.md).

Retain selected model/effort and existing prompt/approval/sandbox settings.
Skill installation changes no account memory and authorizes no builds, flashing,
history rewrites or unrelated work. Token savings are not measured.
