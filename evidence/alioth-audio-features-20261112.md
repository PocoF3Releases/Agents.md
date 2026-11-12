# Alioth Dolby and MiSound feature ownership — 2026-11-12

**Checkpoint:** the MiSound, Dolby and opt-in AudioFlinger scene-preservation changes are published, with host/build and bounded temporary phone validation. All original native/app artifacts, preference bytes and temporary test settings were restored. Physical headphone, acoustic and DSP-execution acceptance remain unverified. Historical results keep their original [audio](../memory/dolby-audio.md) and [validation](../state/validation.md#v-dolby) scope.

## Ownership and processing

Alioth retains Audio HAL HIDL 6.0 and the legacy effects ABI: the selected primary HAL/effect loader is 32-bit, while DMS service/implementation is 64-bit. Static dependency closure covered 116 ELFs from 18 roots with no missing dependency, plus 18 selected, stock-identical DSP/tuning inputs. All six inspected installed core libraries matched source bytes; five matched stock exactly. The primary HAL's code/rodata matched stock with the documented `libaudioroute-v34` dependency rewrite. No required missing package was demonstrated; unused stock 64-bit copies are not prerequisites for this loader.

| Control and owner | Transport and processing boundary |
| --- | --- |
| Dolby master, profiles, GEQ and scalar IDs 101–116: `hardware/xiaomi/dolby` `DolbyEngine` | Session-zero DAP effect `9d4921da-8225-4f29-aefa-39537a04bcaa` → DMS parameter/profile adapter → `libhwdap.so` → GEF/primary-HAL QDSP calibration. The ARM wrapper does not process PCM; a reply is not DSP proof. |
| Dolby attachment: `frameworks/av` `DolbyDapController` and app endpoint policy | Tuning parameter 4 selects a supported endpoint; standard `EFFECT_CMD_OFFLOAD` carries the I/O handle for `qdsp`. Private parameters `0x14`/`0x15` belong to another legacy contract and stay suppressed here. |
| MiSound master, headset, EQ, scene and optional controls: common-device Parts `MiSoundUtils` | `MiSoundEffect` implementation `5b8e36a5-144a-4c38-b1d7-0002a5d5c51b` → `libmisoundfx.so` → asynchronous `audio_hw_socket` packets → primary-HAL calibration for the active endpoint. Queue/socket acknowledgements do not establish processing. |
| Existing game mode and codec opt-ins | Alioth game mode uses its separate `qcom-qdsp` switch/package contract. AC-4/DDP uses the existing 32-bit OMX software decoder/plugin path; decoding success does not establish hardware decoding or compressed offload. |

Dolby and MiSound stay independently switchable. Saved requests remain distinct from temporary bypass. Preserve control-loss/server-restart recovery, communication bypass, custom EQ and factory tuning; do not import stock policy that creates competing global owners. Effect registration, `OFFLOAD_SUPPORTED` and compressed-stream offload are different contracts. Software DAP, game DAP and VQE contain ARM algorithms, so there is no universal hardware-acceleration claim.

## Published MiSound changes

The common-device `aosp-17` series ends at [a1c89c7](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/a1c89c7569931a157a262b416602fc8116263ac4): five independent implementation commits followed by a separate translation commit.

| Change | Behavior and source |
| --- | --- |
| Shared choice dialog | Stops accepting actions when its enabled gate changes: [a84cfca](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/a84cfca6cac436e9783826d6ef73a298e2757728). |
| Headphone 3D | Normalized `SET_PARAM 20`, saved request, default Off. Requires exactly one eligible wired, opted-in USB or explicitly opted-in A2DP route. Unknown/multiple routes or observer failure fail closed. Legacy spatial bit `0x2` is required; supported platform Spatializer suppresses it even when inactive: [a0cd651](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/a0cd6515c60b0b2fc1b2d16eff5b88cc8d1cb1fa). |
| Factory volume presets | Stock examples 1–3 use `SET_PARAM 14` before normalized enable 9, with ear-adjustment capability and headphone-route gates; default Off. Labels are Under 30, 30–60 and Over 60. No personal gains, hearing diagnosis or calibration are synthesized. The selector uses the existing headphone-choice icon: [1a5f0f1](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/1a5f0f1e2e725860baafea4639e2d2a0d1947ef7). |
| Scene recovery | Native music-mode activation can reset scene 15 to Auto while requested-enable is false. Replay the saved scene after `SET_PARAM 4` and before enable, including startup and communication resume: [2297767](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/2297767575935aa1e07a7f861d27a784ad1ea703). |
| Existing HiFi ordering | Send HAL routing before FX8 rereads the changed property, inside the existing support gate. Alioth HiFi remains disabled: [200e78f](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/200e78f1079d9c611435953361e67ff3e10ef498). |

Optional 3D/ear flags clear on master Off, communication bypass, ineligible routes and owned teardown while saved requests survive. Lost control causes no foreign writes. Failed optional changes retain accepted preferences; observer retries do not consume the core owner's contention budget. Route eligibility reflects policy-selected media routing, not attribution of every playing track.

Alioth [40b03d6](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/40b03d69edcb2db57cbdd91e455cc3ff7c8239b4) advertises only the proven legacy 3D bit `0x2` (value 2) and stock Bluetooth capability. It does not copy unknown stock bits `0x1`/`0x4`; platform spatializer support stays false. Existing ear-adjustment/USB gates remain. Two common-device and one alioth recovery overlays remain separate local commits with original authors/messages, excluded from the published audio series.

The separate Parts translation commit adds 792 strings in 88 locale resource sets; nine regional variants inherit Android fallback. Structural checks and two independent AI wording reviews passed after one Frisian correction. Native-speaker signoff is unavailable.

## Published Dolby queued-readback correction

The `hardware/xiaomi:cnb` series was fast-forward published at [cb7ab6c](https://github.com/PocoF3Releases/hardware_xiaomi/commit/cb7ab6c33b4bf96fbc0493602d08ac9e102ca621), from `ffd58fa1453077fbcf25321da321979d490d9a9e`. Its five commits are four implementation topics—Bass preservation, queued confirmation, dialogue range and GEQ units—followed by the separate 78-locale gain-format update. Fresh remote-tip verification matched the published identity.

- **Bass/Virtual Bass:** DMS copies public Bass 111 into Virtual Bass 112. The setter reapplies only an explicitly saved Virtual Bass override and checks both readbacks before saving Bass. No override retains OEM coupling; failure invalidates the applied-profile cache for recovery.
- **Dialogue:** setter, restore and UI bounds become 0–16, matching the DMS/native bounds; factory defaults stay unchanged.
- **GEQ labels:** DMS110 sends raw gains unchanged through `gebs`; ARM/QDSP normalize by 2080 before logarithmic gain. Display units become 1/16 dB, giving ±6.25 dB at raw ±100. Stored gains, presets, twenty bands and graph geometry stay unchanged. The 78 localized format updates are separate from the implementation/default English change.

The initial APK (`a75dcc3b0108ad487383fc3e8770f40d468253132d54f612e1837c30fb476494`) failed the requested Bass1/VirtualBass0 transition: the UI could retain an unconfirmed intermediate state after an error while Bass was not saved. Complete APK/OAT redeployment reproduced the failure; a controlled native probe excluded reverse coupling from Virtual Bass Off in the tested setup. DMS `SET` posts an asynchronous `AMessage`, while `GET` reads directly without a queue barrier. An immediate snapshot can therefore straddle Bass and its companion write, then disagree with later native state.

The correction uses one canonical native snapshot and read-only confirmation delays of 5/10/20 ms for all fifteen user controls. Requested value and saved Virtual Bass must agree in the same snapshot; persistence precedes publication of that exact confirmed snapshot. Rejection/read/transport failure remains visible, invalidates loaded state and the applied-profile acknowledgement, and requests recovery from accepted preferences. The controller logs the transaction exception. No SET is replayed to obtain confirmation and no exception is suppressed. The 35-ms sleep budget is app policy, not a vendor completion guarantee.

The final temporary APK passed all eight changed Bass/Virtual Bass saved/native pairs and retained 1/0 after process restart. Dialogue 16, 0 and 4 matched native readback and saved state. A fresh EQ image shows ±6.25-dB axes and −2.63 dB for existing raw −42; the curve was not edited.

## Verification and artifact scope

- **Host:** complete production `MiSoundUtils`/`MiSoundEffect` compiled unchanged against scripted Android boundaries: 42 actual-source groups plus two native-model consistency guards, including 52 route/gate points. Scene vectors changed from 9/9 mismatches to 0/9; gated HiFi vectors from 3/3 to 0/3. These model native side effects without executing proprietary DSP code.
- **Independent Dolby review:** 172 current actual-method cases passed: 54 retained Bass/dialogue cases, 51 queued successes, 33 bounded rejections and 34 failure/guard cases. Two old actual-method counterexamples reproduce intermediate publication and delayed-write rejection. The canonical snapshot, 33 unchanged methods and wire transport were checked separately. The earlier 33 serializer/ViewModel/saved-state groups and ARMv7/AArch64 `effect_param_t` layout checks retain their unchanged-source scope.
- **GEQ:** 201 raw scalar values and graph points, twenty bands, 15,879 localized gain formats, 79 descriptions and 395 locale-axis outputs passed. Nullable-locale fallback passed two cases; standalone AAPT2 compiled all 79 changed XML files. These do not establish TalkBack pronunciation or endpoint response.
- **App builds:** `lineage_alioth-cp2a-user`, `XiaomiDolby` plus `XiaomiParts`, passed in 491.84 seconds with source unchanged. Parts selector-icon polish passed in 244.3 seconds. The final queued-readback Dolby module passed in 261.85 seconds, also with source unchanged. No full ROM/kernel build or flash formed part of this validation.

| Built APK | SHA-256 |
| --- | --- |
| Final XiaomiParts | `fa4665d55d12a15eaf34c9c03b0e275b25d9195b7cefcfa72fb42a84f3e4c846` |
| Final XiaomiDolby | `151d0964f54c81fb229a4b2017edc555dd35e37e9a77ca75f0a54d1108cc5a4d` |

The final Dolby engine source SHA-256 is `2da5ea01c95cf3fd5a13724d765afa53d8ec72fe1250fbc748a621c4ddc4331f`; Parts owner SHA-256 is `2326116f3606cdd0168bc78df0b924f53ee7a787664bad5a8a0243fbba2696c3`. Temporary phone checks passed all seven MiSound steps: Auto On, select Music (scene 15=1), two Off/On cycles and process restart. Off legitimately reported native Auto4; each On/restart restored Music1. A fresh capture/readback of the final polished APK also retained Music1. Translated optional controls and the factory selector rendered under SELinux Enforcing and were disabled without compatible headphones. The non-owning readback diagnostics used supported GETs, never SET/enabled or owned control. These checks establish tested control/state behavior, not acoustic processing.

A normal application UID/target-SDK37 fixture passed three MIC-recording and three `VOICE_COMMUNICATION` duplex cycles, each with 650-ms active/idle intervals. Captures returned data; duplex playback had zero underruns, cleanup succeeded and audio mode returned to normal. A separate 650-ms silent-media check rendered 28,800 frames with zero underruns. No captured PCM was retained.

This stress run was not error-free: two transient Dolby enable-confirmation rejections occurred during rapid communication re-entry. Existing fail-closed cleanup and bounded reconciliation retained requested preferences; final media state recovered native/framework enable and control, with Bass/Virtual Bass 1/0. Independent source/native review did not establish the precise native cause of those two rejections, so no speculative mode-policy fix or warning suppression was added.

The final app session restored all six original APK/OAT artifact hashes and all three preference files exactly, removed both temporary capability properties, restored stay-awake state, removed the lifecycle fixture and retained SELinux Enforcing. Earlier sessions also restored their originals. Temporary deployment is not installed-ROM acceptance. Physical wired/USB/A2DP effects, acoustic benefit and actual new DSP execution remain unverified.

## SoundID is unsafe to reuse

The exact stock AArch64 helper (`libnative-lib.so`, SHA-256 `7ee2e39d3a1b940f228733fd6b3cd3c64aa4789a697b62bd25f205419a0ef94a`) passed a bounded SDK37 compute diagnostic: four valid six-question sequences and reverse replays, 48 choices, guarded buffers, finite outputs and determinism. It invoked no audio/effect or profile APIs. Normal `dlclose` then aborted with Scudo at the Soundapp destructor, ELF VA `0x1bcac` (exit 134).

Independent ownership review confirmed two defects: scalar Crossfade destroyed as an array, and an uninitialized/borrowed coefficient cache redundantly freed by its parent. Six OEM JNI wrappers also violate array ownership/release contracts. The observed crash is not repaired by correcting only Crossfade or suppressing unload. No helper import, binary patch, crash retry or unload bypass was performed; diagnostic scratch files were removed and absence verified.

Personal SoundID `SET_PARAM 23/24` needs a real matching headset/profile, validated finite gains and a recoverable write sequence; GET23 is absent. Factory zeros, age presets and another device's profile are not personal calibration.

## Published native scene preservation

Ordinary media output changes can move an active output-mix effect chain. Its synthetic DISABLE resets legacy MiSound's selected scene to Auto even though the saved request remains Music. Frameworks/av [6b8c30f](https://github.com/PocoF3Releases/frameworks_av/commit/6b8c30f24b18f50bc28f6d9f24f98c33ec6e7e07) preserves the exact opted-in, session-zero, offload-capable MiSound type/implementation during that move. It omits only the native synthetic DISABLE, retaining status checks, volume handling and HAL detachment. State is rechecked under the effect mutex; ordinary Off, stopping and release still disable. Preservation stays in the current move's local disposition, with rollback/terminal-failure cleanup, instead of arming stock SET22's uncancellable one-shot flag.

Alioth [3af8173](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/3af817361852077b31944a37fe030608382eded3) enables `ro.vendor.audio.misound.preserve_on_move`; other devices default Off. Both pushes were fast-forward and fresh remote refs matched. Alioth's original authored 120-Hz recovery overlay was reparented locally, preserving author, committer, message and patch bytes; it was not published to the ROM branch.

The actual-source C++ sanitizer fixture passed 53/53 cases, covering state/Off races, rollback and terminal cleanup; the old implementation fails nineteen fixture expectations, not nineteen independent production defects. Seven frozen source files match the final commit. The `audioserver`/unchanged-Parts build passed in 249.9 seconds, producing tested audioserver SHA-256 `edefe5b5558d650de77ae3e0d0b0488b33c5772129f290adae62f4697bb6760f` from frozen patch SHA-256 `ed65c2d581d135ab56fed271c55928909f81f559cb604dfbd33748563cecaf6e`. Publication metadata does not represent another build.

With one persistent non-owning observer, opt-out reproduced Music1→Auto4 after one 650-ms media cycle; opt-in retained Music1 and enabled native/framework gates in 10/10 cycles. Explicit master Off cleared native gates and framework enable; On restored Music1. Three normal-UID MIC and three VoIP duplex cycles passed. Restarting both app owners, then audioserver, retained all three semantic preference maps and restored MiSound Music1 plus Dolby profile0/dialogue4/Bass0/VirtualBass1. Post-restart media also passed. These are control/lifecycle results, not acoustic or DSP-execution proof.

The first deployment failed before candidate execution because the original test location could not perform the required execution transition. A private labelled 8-MiB tmpfs enabled temporary testing, with no SELinux policy/enforcement relaxation; the local test-file label was changed. Final checks restored the original audioserver, all six APK/OAT artifacts and three preference files byte-for-byte, removed all three temporary properties, restored stay-awake 0, uninstalled the fixture and removed the private native mount. SELinux remained Enforcing. The two earlier Dolby rapid-reentry rejections retain the separate limit recorded above.

## Mapped stock paths retained as optional work

| Path and source boundary | Required evidence before enabling |
| --- | --- |
| Raw effect commands 23/24; track lifecycle | Standby/app-identity counters need trusted attribution and balanced concurrent start/stop/pause/destruction events. Raw25 is a no-op. Raw IDs are distinct from SoundID SET23/24 and master SET25. |
| VQE notifications; DMS consumer | Track callbacks do not create a processor. Prove consumer, enable policy, call/format gates and service lifecycle. |
| Software game-DAP mixer | Requires a real 5.1.2 producer, processed marker, enumerated descriptor, compatible buffers, route/teardown, CPU and endpoint acceptance; preserve downmix fallback. Separate from Alioth QDSP game mode. |
| Wired remote; reference `KeyLayoutMap::mapKey` | Legacy `persist.audio.button_jack.*` consumes mapped keys 257/258; the stock UI's vendor-prefixed bridge is unresolved. Require exact property ownership, headset/keymap filtering and a physical remote. |
| FX4 and stale `hw_acc` registration | FX4 is separately gated client CPU filtering, not a global MiSound prerequisite. The stale stock UUID lacks an implementation in the actual seven-entry qcompostproc factory; XML/build flags cannot create one. |

The current ARM32 MiSound input is SHA-256 `8a8cb2b953d296697db7ff3024661126e0c4932920b0e13778fbd016aa9c00d6`. Both pinned historical reference trees were searched and selected live/indexed hashes matched; this is scoped semantic coverage, not complete stock parity. Existing [framework closure](audio-framework-closure-20261025.md), [DAP](dolby-dap-params-20261031.md) and [MiSound](misound-params-20261101.md) maps retain further contracts. Raw proprietary sources, ELFs, decompilations, diagnostic logs and device identifiers remain private.
