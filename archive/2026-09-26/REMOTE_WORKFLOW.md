# Working without the maintainer's PC

## Access modes

- **GitHub/GitLab read access:** recover recorded results, inspect accessible source and draft a changelog or patch. Resolve only relevant branch heads. GitLab camera delivery is a separate host and may require separate access.
- **Write connector available:** review the exact changed files and commit/push within the user's authorized scope. A connector is sufficient; a local clone is optional.
- **No write capability:** provide the exact proposed file content/patch and say it was not committed. Continue useful read-only work.
- **No device or raw dump:** do not claim fresh runtime/binary verification. Recorded tests remain usable with their dates, source identities and limitations.

GitHub browser source pattern: `https://github.com/PocoF3Releases/<repo>/blob/<ref>/<path>`; commit pattern: `https://github.com/PocoF3Releases/<repo>/commit/<sha>`. Prefer a resolved immutable SHA for consistent multi-file reads. Raw content can be obtained with the available connector or `https://raw.githubusercontent.com/PocoF3Releases/<repo>/<sha>/<path>` when access permits. A 404 may mean lack of access; do not infer deletion of a private resource from that alone.

## Source roles

[TRACKED_HEADS.yaml](memory/repositories/TRACKED_HEADS.yaml) provides URLs, branches, pinned observations and Android source-tree paths. It is not an instruction to clone everything. There is no assumption that `~/evo17` exists for the reader.

Camera APK delivery: [GitLab vendor tree](https://gitlab.com/johnmart19/vendor_xiaomi_camera). Patch rationale and maintained patches: [GitHub device tree](https://github.com/PocoF3Releases/device_xiaomi_camera/tree/aosp-17/patches). Do not reconstruct the app from an old decompiled experiment just because the delivery binary cannot be fetched.

## When evidence is missing

First use [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) and the routed dated record. State what they establish. If the next question requires a fresh log, binary, screenshot or source file not hosted here, request the smallest specific artifact and explain what it will distinguish. Supply one targeted collection step if helpful; do not ask for root, a ROM rebuild or a whole dump by default.

For remote patch/test work: inspect source, prepare one concrete change, provide exact repository/branch/path and test expectations, then wait for the maintainer's result before dependent changes. Never pretend to execute ADB through GitHub tools.

## Limits

This repository preserves conclusions and selected decisive evidence, not every private dump or original log. It cannot guarantee future hardware diagnosis without new evidence. Remote source inspection cannot establish current root access, flashed partitions, audio quality, camera operation or thermal behavior.
