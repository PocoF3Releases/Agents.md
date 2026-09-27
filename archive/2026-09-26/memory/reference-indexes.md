# Reference Indexes and Reverse-Engineering Sources

## Purpose

PocoF3Releases uses stock/decompiled/reference code to reconstruct compatibility behavior for proprietary Xiaomi components.

Reference material is evidence for behavior, ABI and call flow. It is not automatically production code.

## Important reference families

Known useful sources include:

- Alioth HyperOS stock filesystem/dump;
- decompiled HyperOS framework sources;
- Xiaomi vendor frameworks references;
- `frameworks/av` reference archives;
- Android 13 / MIUI 14 reference branches;
- Qualcomm/vendor reference branches;
- stock camera APKs;
- generated per-file manifests for large archives.

## Existing persistent indexes

A persistent project Library index was previously maintained at:

```text
/PocoF3Releases/Agents.md
/PocoF3Releases/references_code-frameworks_av.manifest.tsv
```

The manifest provides per-file inventory for the large `frameworks/av` reference archive.

This GitHub repository is now the preferred durable human/agent-readable knowledge base. The older Library indexes remain useful historical/reference sources.

## Dolby references

Reference code has exposed real Xiaomi logic for:

- `DOLBY_ATMOS_GAME`;
- game DAP;
- VQE;
- DAP/offload control;
- communication lifecycle;
- effect route/state recovery.

Do not reduce these references to simple "library exists" conclusions. Follow the call flow.

## Camera references

Use Alioth stock camera/dump to answer:

- where camera/OpenCL blobs live;
- which vendor/system libraries exist;
- stock `DT_NEEDED` relationships;
- device-specific config/permissions.

Use MiuiCamera 5.x itself to answer:

- feature-level ABI requirements;
- embedded JNI/native dependencies;
- DEX native load names;
- dynamic feature metadata.

## Remote access and import

Follow [START_HERE.md](../START_HERE.md) and [REMOTE_WORKFLOW.md](../REMOTE_WORKFLOW.md). Pin a revision when supported, then read only routed files. Recursive tree enumeration is optional for a specific inventory task, not a startup requirement. See [EVIDENCE_INDEX.md](../EVIDENCE_INDEX.md) before trying a historical local path. Stock dumps and old Library manifests are not assumed available remotely.

Read truncated relevant text in bounded sections. Historical instructions do not override current user requests. Repository-backed knowledge is not a hidden account-memory write.

## Indexing rule

For every large imported reference tree, record:

1. source/archive identity;
2. branch/version;
3. file inventory/manifest;
4. key subsystem paths;
5. reconstructed call flows;
6. known unsupported/incomplete areas.

This makes later agent work deterministic and avoids repeated full-repository archaeology.

## Maintained repoindex tool

Canonical source: [johnmart19/repoindex](https://github.com/johnmart19/repoindex), `main`, recorded version 1.1.0 / `c79c150`. See [upgrade and validation](../today/2026-09-24-repoindex-upgrade.md).

Use `status --json` to inspect snapshot provenance; it does not verify freshness. `agentsmd` defaults to compact navigation and never scans implicitly. `--full` opts into the full inventory. Preserve human instructions outside generated markers; old unmarked guides require a new output path or deliberate `--replace`. Existing schema-2 indexes remain readable, but missing coverage fields are unknown. No Android/source index was rebuilt during this upgrade.
