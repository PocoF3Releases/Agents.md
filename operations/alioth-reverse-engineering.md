# Reverse engineering Alioth with historical references

Use the installed leanrea and AOSP/WSL skills, then the pinned tools in
~/references_code. Historical Android T/Qualcomm code helps identify contracts;
active Android 17 sources and exact shipped binaries decide compatibility.
Read the reference checkout's AGENTS.md and relevant search guide. Current tool
versions and interface details belong in [ready indexes](repoindex.md).

## Working sequence

1. Identify the actual input: source/extraction path, SHA-256, ELF build ID, ABI,
   dependencies/exports, or APK package/version/native libraries. Reuse existing
   private extracts. Confirm product selection, init service and runtime owner:
   an available blob need not be active. Follow [binary tooling](android-tooling.md).
2. Extract distinctive demangled names, log strings, property keys, ioctl names,
   UUIDs, modules and configuration paths. Search both trees by default. Alioth
   often shares kona/sm8250 code; an alioth-only query misses shared implementations.
3. Find candidate paths first, then use impl for literal .cpp/.cc bodies and source
   for bounded indexed ranges. Symbol queries are heuristic header declarations.
   C HAL functions, Java/Kotlin, XML and scripts need scoped live text or rg;
   they are not in the C++ implementation index.
4. Read callers, configuration gates and error handling, not only declarations.
   Confirm ABI/struct sizes, command IDs, return semantics, sample formats, actual
   board/sensor/amplifier and required tuning. A shared SoC name or transport ACK
   does not establish compatibility, active processing or acoustic quality.
5. Decompile remaining private behavior needed for the current question. Check
   instruction bytes, relocations and callers against the source hypothesis.
   Separate ELF virtual addresses from decompiler image-base offsets; honor Thumb
   metadata, endianness and pointer width. A truncated body, guessed prototype or
   isolated probe crash is not a proven production defect.
6. Compare with current ~/evo source and installed/build identities, then the
   relevant acceptance record. Adapt historical APIs rather than importing old
   framework code or enabling every optional property. Missing hits remain unknown.
7. Implement only useful compatible fixes within the authorized task; preserve
   settings, modes, tuning and attribution. Select affected checks and restore
   temporary device changes. This guide grants no new build/flash/sync authority.
8. Record sanitized input identity, matched reference path/range, binary address/
   symbol, caller/gate, observed versus inferred behavior and validation limits.
   Keep proprietary code/logs private and source/build/runtime evidence separate.

## Bounded lookup examples

Run from ~/references_code with its canonical v2 CLI:

```bash
python3 tools/repoindex workspace files '*AudioEffect*' --scope audio --limit 5
python3 tools/repoindex workspace impl 'AudioEffect::controlStatusChanged' --scope audio --limit 3
python3 tools/repoindex workspace impl 'EffectHandle::setEnabled' --scope audio --limit 3
python3 tools/repoindex workspace source android-t-qcom/frameworks/av/media/libaudioclient/AudioEffect.cpp --line 554 --limit 18
python3 tools/repoindex workspace files '*acdb*' --tree LA.UM.8.12.r1-11900-sm8250.0 --limit 5
python3 tools/repoindex workspace impl 'BPSNode::ExecuteProcessRequest' --scope camera --limit 3
```

The control callback and EffectHandle searches were found in framework AV; CamX
and Qualcomm ACDB paths were also located. These are lookup checks, not a new
audio/camera investigation or device acceptance. Indexed line numbers belong to
the snapshot; compare live content before editing. Source JSON includes its hash.

## Scope without hiding relevant code

| Investigation | Reference starting point and compatibility check |
| --- | --- |
| Dolby/MiSound, capture, VoIP | Framework AV; locate C hardware HAL paths before live text; mm-audio/calibration/Bluetooth helpers |
| Camera | CamX/CHI, device tree and tuning; actual sensor/usecase, not any sm8250 preset |
| Display/GPU | Qualcomm display/devicetree and framework native; current panel/kernel/userspace ABI |
| Thermal/power | thermal-engine/android-perf/configuration; private mi_thermald still needs its exact prebuilt |
| Sensors, haptics, charging | Locate hardware/vendor/prebuilt paths; actual service, node and board |
| Firmware/calibration | Paths and matching loaders; opaque tuning is not ordinary ARM code |

Scopes are filters, not complete subsystem inventories. The current audio scope
omits some hardware HAL and mm-audio-auto-cal paths. If a scoped query is empty,
try bounded files across both trees, then --path-prefix for the discovered
component. Impl is case-sensitive and suffix-limited; do not rebuild for a scope
or language mismatch. Private MiSound/FCSAM functions need not appear in either
snapshot. Other-device calibration is not an Alioth replacement.

## Reuse ready data

Do not index, implement, optimize, benchmark, deep-verify or clone all source just
to start reverse engineering. Cold caches restore from committed bundles. Indexed
files/impl/source work in an index-only checkout; materialize only the component
needed for live C/Java/XML searches. These are partial historical snapshots, not
a complete Alioth ROM source tree or proof of current hardware acceptance.

The packaged tool's implementation/refactor and fresh-clone acceptance are already
recorded in the reference repository and ready-index guide. Keep ordinary RE on
that pinned consumer copy. Generic tool improvements belong in ~/tools/repoindex,
then a reviewed vendor refresh; do not fork search logic into Alioth helper scripts.
Fresh-clone acceptance is explicit maintenance, not a normal lookup prerequisite.
