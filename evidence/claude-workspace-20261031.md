# Claude workspace preparation — 2026-10-31

Host/configuration checks only. No Android source edits, build, sync, flash or device operation.

- Added portable CLAUDE.md imports in the workhub and reference repository. Root ~/evo entrypoint imports root instructions and the workhub entrypoint. The maintained rules/current state remain authoritative.
- Installed a local Sonnet 5.5 default project setting, with Opus 5.5 selectable explicitly; no global settings, login, account/model entitlement or paid inference was changed/tested.
- Added local additional-directory paths only for existing reference, stock-dump, stock-kernel, index-tool and Mesa research locations. These are access paths, not permission to alter unrelated material. No whole-home grant or permission bypass.
- Linked resume and Leanrea skill folders from the workhub; local AOSP/WSL and kernel links reuse installed Windows Codex skill bodies. No third-party skill source was republished. All four local links resolve to SKILL.md.
- Verified root/workhub/reference instruction import targets and depth. Expanded root context is about 6 KiB; reference context is about 2.6 KiB. This is a byte count, not measured tokens or proof of client loading.
- Validated both local JSON settings files and every additional directory. Workhub structural/unit checks and reference docs/config/chunk checks pass without index restoration or source scans.
- Updated the separate clean ~/Agents.md mirror from its older head using fast-forward only. Primary workspace knowledge remains ~/evo/.workhub. Updated reference checkout uses a filtered main-only fetch; an unnecessary all-branch fetch was stopped without changing its source checkout.
- Claude Desktop's WSL remote service was observed; a standalone claude executable was absent from the Linux login PATH. No duplicate CLI was installed or credentials inspected. Authenticated /context, /skills and actual model selection remain client checks, not claimed completed.

The [setup/location guide](../operations/claude-code.md) owns commands, paths,
model/client requirements and official sources. Reference source bytes and ready
bundles are unchanged. Do not infer current hardware behavior from these checks.
