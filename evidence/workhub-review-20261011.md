# Workhub standards and specification review

October 11, 2026. Reviewed the recent workhub changes from the pre-update base
through the published reference cleanup, then rechecked the corrections.
Review plugin workflows used independent Standards and Spec passes.

## Standards

Resolved one finding: stable recovery patch import bases were erased with
rewritten feature candidates. Restored four linked upstream bases after checking
the canonical recovery patch contract and local ancestry. These are required
replay inputs, not dropped maintained commits. Final pass found no additional
actionable Standards regressions in the corrections.

## Spec

Resolved one finding: a seven-character fingerprint commit abbreviation collided
with a framework translation commit. The link now identifies the retained
hardware lockout implementation by full repository and SHA. Final pass confirmed
the linked diff implements lockout initialization/authentication guards and found
no additional specification regression in the corrections.

## Official guidance and network checks

Refreshed [OpenAI guidance](../references/openai-guidance.md) from the official
GPT-6.1 Sol model page, GPT-6 prompting guide and scoped repository review advice.
No client settings or model performance claims were changed.

Audited 81 distinct Markdown network URLs. Eighty responded HTTP 200; the GitLab
camera commit page responded HTTP 403. Corrected its path to the canonical
/-/commit/ form, but the network still rejects page access. Newly restored
recovery links and the corrected hardware commit returned HTTP 200.
Local Markdown links, context budgets, privacy checks, fixtures and whitespace
checks pass. These checks do not certify Android runtime or all future URLs.

The review adds an ownership invariant to maintenance: resolve abbreviated IDs
inside the owning repository, preserve required upstream import bases, and never
assign historical test evidence to a different commit.
