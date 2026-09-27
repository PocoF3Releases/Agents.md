# Localization Workflow

## Scope

Project applications such as XiaomiParts and Dolby include maintained translations.

## Translation rules

- Read repository-local translation instructions (for example `AGENTS.md` / `TRANSLATING.md`) before editing.
- Translate all missing user-visible strings for the target locale.
- Preserve Android formatting placeholders exactly.
- Preserve XML escaping and resource names.
- Do not translate package names, technical identifiers or format tokens.
- Avoid machine/API-token workflows when local/manual translation is requested.
- Re-fetch the target branch before a translation update so newly added strings are included.

## Review

Before commit:

1. compare base `values/strings.xml` against the locale;
2. find all missing resource names;
3. validate XML;
4. check placeholders such as `%1$s`, `%d`, escaped apostrophes and markup;
5. avoid duplicate keys.

Translation commits should contain translation/resource changes only unless the task explicitly includes code/UI changes.
