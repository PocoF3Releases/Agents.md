# Initial-build changelog implementation audit

**2026-10-09 — source-checked.** Enumerated the current PocoF3Releases organization,
rechecked selected remote heads and inspected local final code/product wiring,
maintainer change families and recorded validation. All listed tracked trees clean.
No ROM build, flash or new app/device test was performed.

## Source coverage

| Build source path | Verified local/remote head | Final behavior grouped in notes |
| --- | --- | --- |
| `device/xiaomi/sm8250-common` | `6574ae0d2c27cc73ee572bc8556bf77267bfff17` | Parts/touch/refresh/thermal, modem cache, power/memory/audio integration |
| `device/xiaomi/alioth` | `6ac76e6fe906a5f6b313b5b588b3bf3b700b1283` | Product selection, brightness/HBM, proximity, stock haptics, camera input/recording gates |
| `vendor/xiaomi/alioth` | `d9c52cf131edbe5786c1092b52e10c04902cb994` | Stock audio/camera/sensor firmware, patched MIUS/CHI, waveform samples |
| `vendor/xiaomi/sm8250-common` | `62304de551fd9e5a63c8811123b9a5ddad8a40ea` | Stock HAL dependencies, tuning, media/graphics/thermal services and task profiles |
| `kernel/xiaomi/sm8250` | `bd43bde102a829c744620aa3df8ea7df4891485c` | 4.19.325, stock AW8697, display/audio/battery/touch guards, WireGuard |
| `hardware/xiaomi` | `ec8831d20942ea2acdbda2fbedc08e4d09874fa0` | Dolby/volume engine, sensor/fingerprint lifetime, stock HAL and LOW_TICK |
| `device/xiaomi/camera` | `6ecedef10389060750bb8c7ce13e81e8e734492d` | Product/permissions/JNI/shim/cache/SAT/recording integration |
| `frameworks/av` | `5c3e93ebef3c20c5d8ab32453db00b7d91706458` | AC-4/DAP opt-ins, camera tags, effect reply and MediaCodec safeguards |
| `frameworks/base` | `3eaa985f38805138d417aa2f64fd67efd71c66ee` | Xiaomi camera inputs, recording FPS/blur, HBM opt-in, controller restoration |
| `hardware/qcom-caf/sm8250/display` | `385a1c2fa09b9f1ab1d566afa14727e54b6f57dc` | Legacy camera DisplayConfig endpoint and buffer allocation guards |
| `hardware/qcom-caf/sm8250/audio` | `147f4aae7eb3148baae6c992594a278630b09909` | AIDL Health battery listener with HIDL fallback |
| `hardware/qcom-caf/sm8250/media` | `6b3d466f134ef3b3f8b1da5c7ffa8bb234249292` | C2D color/layout refresh and surface/GPU mapping lifetime |
| `hardware/nxp/nfc` | `05b56f439e52a32198749f39b57b7dfb326b5071` | Snapshot client queue during teardown; superseded timer fix excluded |
| `vendor/qcom/opensource/usb` | `f96fae951fbeb9d897b82a721583808022c5902b` | Platform configfs ownership/controller readiness |
| `vendor/xiaomi/camera` | `f13797ef3d93508756e06a4a185c9208dbc3ee88` | Final APK, ExtraPhoto/gson and matching native runtime |
| `external/tinycompress` | `ff62357d346d31cea3e90fb11755bbdefdb41a23` | Full capture-read semantics, poll state and EOF termination |

## Inclusion and finality

Alioth device.mk selects AW8697 and includes camera/miuicamera.mk; the common
product installs XiaomiParts/XiaomiDolby/DSPVolumeSynchronizer and opt-ins for
legacy DAP/AC-4. Alioth overlays enable high-refresh recording and independent
blur handling; normal cap is 60, selected maximum mode remains codec-limited.
Kernel Alioth config enables WireGuard. Audio HAL links libtinycompress; capture
loop/poll/EOF fixes are present in the complete final library source.

Camera APK is a real LFS payload, 223517496 bytes, SHA256
`29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`.
Both camera sources remain required. Current repo list includes tinycompress;
custom device/camera/hardware trees are manually supplied and absent from that
manifest inventory. Product inclusion was checked separately. No immutable full
included-commit manifest or matching release ZIP was available.

Finality means code is present on the selected branch and wired where applicable;
it does not certify every route/device or exact released artifact. Semantic
families are listed once: camera/display buffers, Dolby/framework lifecycle,
modem/cache, Parts/thermal and stock haptics each combine multiple repositories.

## Exclusions and wording limits

Reference-code/profile/workhub repositories are not ROM features. PBRP is a
separate recovery product. A16 and experimental refs are excluded. AAC renderer
is a development target, not full RichTap; no PWLE/Android spatializer claim.
No generic game/FPS/battery-life improvement or donor GPU port is established.

Tinycompress host/ARM/ARM64 tests are reported in commits; new library was not
installed into the ROM. Do not claim all messaging-app voice recording fixed.
C2D layout checks were host-tested; target build was blocked in the original
record, so describe implementation rather than proven screen/video symptom repair.
Dolby ACKs/profile transport are not listening proof for all effects/routes.
ExtraPhoto is packaged; full editor flows lack comprehensive acceptance.

The latest refresh APK, modem image, fuel-gauge change and thermal helper need
matching rebuilt acceptance. No replacement-battery boot cure, unlimited 120 FPS
recording, ultrawide true 60 FPS or complete biometric certification is claimed.
See [validation](validation.md) for historical scope and the final
[large](telegram-initial-full.md) / [small](telegram-initial-short.md) posts.

## Complete organization inventory and companion pass

All 19 current organization repositories were rechecked in a subsequent October 9
pass. The 15 organization ROM inputs above plus required GitLab camera make 16
custom ROM inputs. Their heads remained unchanged. Four remaining repositories:

| Repository | Head | Classification |
| --- | --- | --- |
| `.github` | `e9cfbbe3ae4c9e02285fc5f392798d39dc19e8d9` | Organization profile/artwork; excluded from ROM features |
| `references_code` | `d301665e4c8d442a98cdc636c9f12e260bd1de0b` | Reference code only; no production inclusion assumed |
| `Agents.md` | `enclosing commit` | This knowledge workhub; revision is the enclosing commit |
| `device_xiaomi_alioth-pbrp` | `6fee5a070ba1aeb4742f345486d12bbe2c36994c` | Separate recovery build; unchanged source and excluded from ROM notes |

Companion Settings gesture/clipboard screens and controllers were inspected as
build integration evidence. Settings is an upstream dependency, excluded from
our maintained repository tracking. Current frameworks/base implements
independent wake/ambient double-tap arming, automatic-mode AOD clamp correction
and off-main-thread QS usage queries. Clipboard controller/resources and framework
setting coexist. Those are source-backed everyday controls, not new runtime tests.

Alioth vendor.prop overrides the common optional default to enable stock Dolby
speaker tuning; Android spatializer remains disabled. Final code gates tuning
by that property. Do not confuse this with audible certification of every profile.
GitLab camera head was reverified; camera/artifact validation from the first pass
remains valid because its source head and payload have not changed.

Upstream dependencies are excluded from the source ledger; this audit retains
only the integration findings needed to assess the changelog. Reverted NFC timer
work, optional AAC renderer, build-only changes and irrelevant other-device HAL
changes remain excluded. No attempt was made to certify every upstream project
in the 1257-project manifest or all historical commit effects; this audit covers
the requested organization sources and relevant companion integration.
