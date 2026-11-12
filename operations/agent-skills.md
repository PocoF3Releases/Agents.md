# Skills for internal agents

All assigned agents may use any relevant skill and exposed tool in their current
runtime, within the user's authorization. This is a workflow permission, not an
installation, credential grant or bypass of runtime controls. Discover the live
catalogue before reporting a capability unavailable; the catalogue can change.

## Include in every delegation

Give the agent this guide, its owning topic and applicable AGENTS chain; specify
its question, source/HEAD, output, allowed edits/tests and shared-file ownership.
Read the matching SKILL.md before using it. Load only relevant references rather
than every skill body. Do not restart completed lanes just to acknowledge a guide.
Keep the requested Codex model/concurrency in [maintenance](maintenance.md#internal-agents).

Use skills to resolve the assigned question, not to open unrelated investigations.
Root coordinates Git/publication, shared builds and device changes unless those
operations are explicitly delegated. Keep headless PC tests and hidden helpers;
phone interaction remains governed by the current task. Preserve paused work.

## Choose the matching workflow

| Assignment | Best fit | Boundary or evidence needed |
| --- | --- | --- |
| Android platform, HAL, native Parts/Dolby integration | `aosp-wsl` and the owning workhub topic | Resolve actual WSL component/worktree, source/config/toolchain; separate host, build and phone evidence. |
| APK, smali, stock framework or native ELF behavior | `leanrea`; available REA/CLI tools where useful | Use ready source indexes and hash the real stock artifacts. Correlate callers, API IDs, payloads, return values, routes and lifetimes before a port. A decompiler guess is not proof. |
| Kernel/driver, DTS, Kconfig, warning or lifetime audit | `kernel-development-skills` plus `aosp-wsl` | Only if kernel work is in scope; preserve thermal/security/ABI behavior. This guide does not resume paused kernel investigations. |
| Review an implementation or candidate before publication | Review plugin's `code-review-and-quality`; `code-review` for a fixed baseline; `entry-review` when the plugin is selected | Give reviewers exact source/candidate and acceptance criteria. Use adversarial, performance or security skills for a concrete need; do not invent findings or weaken checks. |
| Specific API or library documentation gap | Context7 tool | Reuse the resolved version/ID. Platform/private API implementation and stock evidence remain authoritative. |
| Codex skill/tool/model configuration | `openai-docs` | Follow its current source-order instructions and official documentation; distinguish documented capability from this session's availability. |
| Install or author a requested skill | `skill-installer` or `skill-creator` | Check provenance and requested scope. Merely using available skills requires no reinstall. |
| TokenEconomizer status or requested settings | Matching `tokeneconomizer:*` skill | Inspect actual state; do not claim savings/activation or silently change pruning/configuration. |
| Browser or desktop evidence | Built-in browser and the relevant browser/testing skill; computer-use when applicable | Prefer service tools when sufficient, honor explicit browser choice, and avoid visible PC test windows. |
| Native Compose Settings UI | Actual checked-out Settings, SettingsLib/Spa, Compose resources and targeted docs | ExpoKit is for Expo/React Native and does not replace native Compose. Verify accessibility, RTL, font scale, screen bounds and real screenshots. |
| Release artwork or requested artifacts | `imagegen`, document/PDF/presentation/spreadsheet/visualization skill matching the output | Respect existing assets and export/visual verification requirements. Do not create cloud pages/sites or publish artifacts without task authorization. |
| Host AMD compute failure | `rocm-doctor` | Does not diagnose the phone's Adreno GPU. Keep Android driver work separate. |
| Actual Hugging Face or local-model work | `hf-cli`, model selection/memory/local-model, datasets/papers, eval/training or Gradio/Spaces skill matching the task | These are optional tools for a relevant ML assignment, not a requirement for Android reverse engineering. Preserve evidence and avoid unsolicited downloads/uploads. |
| Actual AWS/SageMaker work | AWS context discovery first; isolated Python, deployment planner, image selection, IAM preflight and production-default skills as needed | Discover the real profile/account/region and authorized spend. Availability alone authorizes no cloud resource or deployment. |

Other installed skills remain available when their descriptions match the task.
Do not load or invoke a skill solely because it is listed here.

## Context7 for Parts and Dolby

Reuse these already-resolved IDs when they answer the specific question:

- `/websites/developer_android_reference`: AudioManager, AudioFocusRequest,
  TileService, lifecycle and documented Android API contracts.
- `/websites/developer_android_develop_ui_compose`: Compose layout, accessibility,
  effects, state and adaptive UI guidance.
- `/websites/developer_android_reference_kotlin_androidx_compose`: exact Compose
  Kotlin API/semantics behavior; compare with the version actually in the checkout.

If the required library/version is different, resolve it once. Record the relevant
claim and source, not a bulk documentation dump. Smali syntax documentation helps
read bytecode; it does not establish Alioth DSP support or a hidden API contract.

## Report and hand off

Report the source/artifact identities, demonstrated failure or no-defect result,
exact checks/results and remaining limits. Mark unavailable hardware and blocked
checks explicitly. Do not retry or work around a platform safety restriction.
Maintain only the agent's own private checkpoint; update shared fact owners through
the parent to avoid conflicting writes. See [continuity](continuity.md).

Official background: [skill workflows](https://developers.openai.com/plugins/concepts/skills)
complement tool/runtime access; [multi-agent tools](https://developers.openai.com/api/docs/guides/agents-api/multi-agent)
describe inherited configured tools. Runtime exposure and higher-priority controls
remain authoritative for this session.
