# Claude Code on the Alioth workspace

**2026-10-31 — configuration and host checks, not model/device acceptance.**
Claude Code and Codex share AGENTS.md, CURRENT_STATE.md and topic records. The
small [Claude entrypoint](../CLAUDE.md) imports the first two; no copied project
history, automatic builds, permission bypass or credentials are needed.

## Start in WSL

Open Ubuntu, then `cd ~/evo`. For Claude Desktop, select this WSL folder as the
project. For a separately installed Linux CLI:

```bash
cd ~/evo
claude --model claude-sonnet-5-5
# Or:
claude --model claude-opus-5-5
```

Official model documentation lists minimum Claude Code versions 2.1.284 for
Sonnet 5.5 and 2.1.280 for Opus 5.5. Check `claude --version` when a CLI is
installed. Use `/model` or `/status` to confirm the actual model/provider; account
entitlements and host-managed settings can override project preferences. These
model-independent instructions work with either model. No account login or paid
inference was performed during setup.

The local root settings start standalone Claude Code on `claude-sonnet-5-5`;
`/model claude-opus-5-5` switches a session. Do not impose a public model allowlist
or overwrite user/global authentication, provider, proxy or permissions. On this
host Claude Desktop's WSL remote service was present, but a standalone `claude`
was not on the Linux login PATH. Desktop access and CLI installation are separate.
If a CLI is wanted, follow the official Linux/WSL installation guide, install in
user scope, then verify its version and sign in interactively. Do not copy Codex
credentials or assume its MCP connectors are available in Claude.

## Instruction and skill discovery

- `~/evo/CLAUDE.md` imports the root AGENTS.md and `.workhub/CLAUDE.md`.
  Relative imports resolve from their containing file. `~/evo` is a Repo checkout,
  not one Git repository; keep instructions outside production component commits.
- The workhub CLAUDE.md imports shared rules and current routing. Reference
  checkout CLAUDE.md imports its own AGENTS.md. This also supports clients without
  native AGENTS.md discovery. Keep the case exactly `CLAUDE.md` on Linux.
- After resume/compaction, reread the resume skill and relevant topic; historical
  evidence is not proof of the currently installed image.
- `.claude/skills/` links existing resume/Leanrea skill directories rather than
  duplicating them. In the local Android workspace, AOSP/WSL and kernel skill
  links point to installed Codex skill bodies; use kernel guidance only for
  kernel work. External Windows plugin links are machine-specific and may need
  repair after a plugin update. Do not publish third-party skill copies.
- Start from `~/evo`, not a detached worktree of just one component: its parent
  entrypoint supplies workspace context. For standalone component clones outside
  it, explicitly read the workhub and that component's instructions first.
- Run `/context` and `/memory` in an authenticated Claude session to confirm loaded
  instructions; `/skills` confirms skill discovery. Static checks cannot certify
  client loading or model availability. External imports can require trust.

## Claude auto memory and history

Claude auto memory (`~/.claude/projects/-home-johnmart19-evo/memory/`) is local
to one machine/account: pointers, preferences and attribution only. Facts,
heads, tests and releases belong in workhub owners. `~/Agents.md` is the same
repo: `git pull --ff-only` before reading; edit one copy per task.

For earlier work search `INDEX.yaml`, V-* anchors and `evidence/`, then Git
(`git log -S '<term>'`, `git show <rev>:<path>`). Removed dated logs exist only
in Git history and stay historical.

Recreate a relocated checkout using the [root template](../templates/android-root-CLAUDE.md)
and [optional model settings](../templates/claude-settings.json), after confirming
`.workhub` exists and preserving any existing files. No general home-directory
CLAUDE.md or hooks are installed. Shared skill links work in WSL; on native
Windows, enable Git symlink support or read the original skill files explicitly.

## Locations and ownership

Paths below are local conventions, checked for existence on this host unless
marked optional. They do not exist just because someone cloned this workhub.

| Location | Purpose |
| --- | --- |
| `~/evo` | Active Evolution X Android 17 Repo checkout; Linux source/build commands |
| `~/evo/.workhub` | Primary shared knowledge checkout, PocoF3Releases/Agents.md |
| `~/Agents.md` | Separate mirror of the same GitHub repo; fast-forward before reading; edit one owner at a time |
| `~/evo/device/xiaomi/alioth` | Product, display overlays, audio tuning, health and device policy |
| `~/evo/device/xiaomi/sm8250-common` | Common init/fstab/SELinux, power hints, XiaomiParts |
| `~/evo/hardware/xiaomi` | Dolby/Xiaomi HAL implementations and common hardware helpers |
| `~/evo/kernel/xiaomi/sm8250` | Redline 4.19 kernel, drivers, DT/defconfig; use scripts/update_defconfig for requested config generation |
| `~/evo/vendor/xiaomi/alioth`, `~/evo/vendor/xiaomi/sm8250-common` | Packaged vendor binaries/configuration; preserve exact provenance |
| `~/evo/hardware/qcom-caf/sm8250/display`, `~/evo/hardware/qcom-caf/sm8250/audio` | Current Qualcomm display/audio integration; verify per-project remotes |
| `~/evo/device/xiaomi/camera`, `~/evo/vendor/xiaomi/camera` | Finalized camera integration; do not reopen without task scope |
| `~/evo/frameworks/base`, `~/evo/frameworks/av`, `~/evo/frameworks/native` | Current framework and media source; honor kernel-only task boundaries |
| `~/evo/bootable/recovery`, `~/evo/system/vold`, `~/evo/system/sepolicy` | Native ROM recovery/storage integration, not a standalone PBRP tree |
| `~/evo/out/target/product/alioth` | Existing build artifacts; obj/KERNEL_OBJ is kernel output, not source |
| `~/evo/.repo/research` | Private research, tests and raw diagnostics; IQ-8275 work is iq8275-20261028 |
| `~/references_code` | Ready historical Android/Qualcomm indexes; use its pinned tools/repoindex CLI |
| `~/tools/repoindex` | Independent canonical index-tool development; not needed for consumer queries |
| `~/miui/out` | Exact stock dump/prebuilts for reverse engineering; never publish raw proprietary files |
| `~/alioth-r-oss` | Historical Xiaomi stock kernel comparison, not active build source |
| `~/mesa` | Mesa research only; installed phone uses stock graphics; Turnip work was stopped |
| `/mnt/d/platform-tools/adb.exe`, `/mnt/d/platform-tools/fastboot.exe` | Windows-owned USB tools from WSL; one ADB server owner |

Old paths such as `~/pbrp-alioth-a17`, `~/kernel_devicetree_alioth-r-oss` and
`~/miui/decompiled/jadx-frameworks` were absent here. Reuse actual private extracts
under `.repo/research` after identifying inputs; do not silently create or replace
missing reference trees. Optional JADX/Ghidra records are historical until their
installed commands/paths are rechecked. See [tooling](android-tooling.md) and
[RE workflow](alioth-reverse-engineering.md).

Local `.claude/settings.local.json` lists only existing adjacent research folders
as additionalDirectories. This grants file access, not authorization to edit them,
and does not automatically import their CLAUDE.md. Read the relevant instructions
when crossing into a repository. CLI `--add-dir PATH` is the per-session alternative.
Keep personal paths/settings local; never grant the whole home or disable approvals.

## Build, search and evidence

Use [repository identities](../state/repositories.yaml) and `repo list` for actual
project-to-checkout mapping; inspect each project's status/remote before changes.
Use [subsystem map](../memory/alioth-subsystems.md) to route a task. Do not fetch all
legacy branches of references_code just to update documentation: fetch main with
`--filter=blob:none --no-tags`, preserving local edits.

Release workflow, only when requested:

```bash
cd ~/evo
. build/envsetup.sh
lunch lineage_alioth-cp2a-user
m installclean
m evolution
```

Development rebuilds omit installclean. Repo sync may use -j50; builds must not
inherit that count. Recent kernel verification used -j4, W=1 and KCFLAGS=-Werror;
select the current recorded command/toolchain rather than a generic system Clang.
Never weaken warnings, thermal protection or SELinux to claim acceptance.

Historical search, without rebuilding indexes:

```bash
cd ~/references_code
python3 tools/repoindex workspace files '*AudioFlinger*' --limit 5
python3 tools/repoindex workspace impl 'AudioFlinger::checkAttributionSourcePackage' --limit 3
```

Use both datasets by default, then bounded indexed source ranges. [Search guide](repoindex.md).
For an external library API gap, use Context7 only if actually configured in this
client, resolve once and reuse the ID/version. Otherwise consult official docs;
do not claim a connector or Codex plugin is installed in Claude.

Update the relevant workhub fact owner, keep translations separate from feature
commits, preserve upstream authorship and approved behavior. Record source, build
and runtime evidence separately. Shared commits from this Codex setup retain the
actual Codex attribution; future Claude contributions must not falsely claim that
identity. Run `python3 scripts/check.py` in the workhub; reference docs use their
own check, with no source scan/reindex. No Android build, reboot or flash is a
setup step.

## Official references

- [Claude project memory/imports](https://code.claude.com/docs/en/memory)
- [Model IDs and minimum client versions](https://code.claude.com/docs/en/model-config)
- [Project/user/local settings](https://code.claude.com/docs/en/settings)
- [Skills and directory links](https://code.claude.com/docs/en/skills)
- [Linux and WSL installation](https://code.claude.com/docs/en/setup)
