# ChatGPT Repository-Memory Import Workflow (2026-09-22)

## Scope

This record captures a full repository-memory import performed from the private `PocoF3Releases/Agents.md` GitHub repository.

The purpose was to reconstruct project context for a fresh ChatGPT session without relying on the smaller product-provided memory summary.

## Source revision

The import was pinned to:

```text
b7c1d1229ee7dd83b5dc778d28fed3df565c6676
docs: archive complete Codex memory snapshot
```

The recursive tree at that revision contained:

```text
38 tracked blob files
```

All reads were performed against that immutable commit rather than the moving `main` ref.

## Files covered

The import covered the complete tracked tree, including:

- repository rules: `AGENTS.md`, `README.md`, `OFFLOAD_PROTOCOL.md`;
- all durable `memory/*.md` subsystem records;
- the chat-offload template;
- the complete dated Codex memory archive;
- `MEMORY.md`, `memory_summary.md`, and `raw_memories.md`;
- all archived ad-hoc notes and rollout summaries;
- all newer 2026-09-22 MiuiCamera / ExtraPhoto dated records.

## Large-file handling

A normal connector fetch of `today/2026-09-22-codex-memory-snapshot/MEMORY.md` was truncated.

The file was therefore re-read explicitly as:

```text
lines 1-160
lines 161-320
lines 321-414
```

`raw_memories.md` was likewise read in explicit ranges to ensure complete coverage.

Durable lesson: a successful fetch call is not proof that a large file was fully returned. Detect truncation and continue with bounded line reads.

## Precedence used during import

The repository itself establishes that imported historical snapshots are not automatically current state.

The import therefore used this ordering:

1. current verified repository/device state when available;
2. durable `memory/` conclusions;
3. newer dated `today/` records;
4. older Codex/raw/ad-hoc/rollout snapshots as historical evidence.

Examples:

- the old static MiuiCamera conclusion that JPEG utility JNI was unnecessary is superseded by runtime evidence proving `libcamera_jpegutil_jni.xiaomi.so` is directly loaded;
- historical "Turnip only" and "Dolby only" focus notes describe past sessions and do not constrain a new request.

## Product-memory boundary

Reading this repository reconstructed the full project context inside the active ChatGPT conversation.

It did **not** directly write the 38 files into ChatGPT's hidden/account-level memory database, because no product memory-write capability was available in the session.

Future agents must keep these concepts separate:

```text
GitHub knowledge repository
    !=
ChatGPT/Codex hidden product memory
```

Do not claim the latter was updated merely because the former was read successfully.

## Reusable procedure

For future fresh-session imports:

1. resolve latest branch head;
2. pin the immutable commit SHA;
3. enumerate the complete recursive tree;
4. record the expected file count;
5. read operating rules first;
6. read files from the pinned SHA;
7. chunk any truncated large file by line range;
8. reconcile current/durable records against historical snapshots;
9. report the exact commit and coverage count;
10. recheck live repository/device state before executing historical implementation instructions.

## Result

At the end of this import, all 38 tracked files from the pinned commit had been read, including the complete large memory exports.

This procedure should be used whenever the GitHub knowledge base is newer or more complete than the agent's built-in remembered context.
