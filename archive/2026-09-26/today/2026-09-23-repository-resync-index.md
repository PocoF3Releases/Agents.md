# Repository resync checkpoint

## Scope and evidence

Live GitHub organization metadata, branch heads, and commit comparisons refreshed at 2026-09-23T11:07:23.156750+00:00. All 22 current repositories are indexed. Unchanged saved heads were skipped; changed heads were compared against the saved baseline. Newly tracked repositories use at most 20 latest commits, not an exhaustive history audit. No builds, device tests, source migrations or source resets were performed.

Machine-readable evidence: [latest commits](../memory/repositories/LATEST_COMMITS.json). Current head routing: [tracked heads](../memory/repositories/TRACKED_HEADS.yaml).

## Current remote heads

| Repository | Branch | Head | Comparison / indexed commits |
|---|---|---|---|
| device_xiaomi_sm8250-common | aosp-17 | [cbd5d4122d88](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/cbd5d4122d885b9015f6c220048169bcd76c7616) | ahead; 39 |
| device_xiaomi_alioth | aosp-17 | [c6c2e9834d0a](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/c6c2e9834d0ab940791f5aac2067927f1b1466ae) | ahead; 5 |
| vendor_xiaomi_alioth | aosp-17 | [a3972583b004](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/a3972583b004e3964766a48e681e007b9335ef67) | ahead; 2 |
| vendor_xiaomi_sm8250-common | aosp-17 | [ff4a56a52f50](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/ff4a56a52f50211e0d6a6147dabe5a1017faa95c) | ahead; 2 |
| kernel_xiaomi_sm8250 | aosp-16 | [10f8a106de65](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/10f8a106de65d4fb5cd9c2f2fe2714f11d97bcd5) | ahead; 8 |
| .github | main | [75585c8ae5df](https://github.com/PocoF3Releases/.github/commit/75585c8ae5df3696a2a5ac70f5b148b2250b200d) | newly tracked; latest 20 commits only; 14 |
| references_code | android13-miui14-cn_beta | [d301665e4c8d](https://github.com/PocoF3Releases/references_code/commit/d301665e4c8d442a98cdc636c9f12e260bd1de0b) | newly tracked; latest 20 commits only; 1 |
| hardware_xiaomi | cnb | [cab7a5210518](https://github.com/PocoF3Releases/hardware_xiaomi/commit/cab7a52105183c03ed90f219250e88fb6e7d36db) | unchanged; 0 |
| device_xiaomi_camera | aosp-17 | [d7356c295a57](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/d7356c295a5794a9af362e4553a745213da6e2d9) | ahead; 1 |
| frameworks_av | cnb | [8fc27178f6fa](https://github.com/PocoF3Releases/frameworks_av/commit/8fc27178f6fa4a1a1eb0cc3df66b33109f0ed300) | unchanged; 0 |
| frameworks_base | cnb | [315a6cb52f29](https://github.com/PocoF3Releases/frameworks_base/commit/315a6cb52f29f058238c6c6633866e19983134c7) | diverged; 13 |
| hardware_qcom-caf_sm8250_display | cnb | [0e25857599b3](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_display/commit/0e25857599b3a609e957a0d0418ec2b3dd264480) | unchanged; 0 |
| hardware_qcom-caf_sm8250_audio | cnb | [0782faad5715](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_audio/commit/0782faad5715864c62912fda9749836d3f1cdd70) | unchanged; 0 |
| hardware_qcom-caf_sm8250_media | cnb | [6b3d466f134e](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media/commit/6b3d466f134ef3b3f8b1da5c7ffa8bb234249292) | unchanged; 0 |
| Agents.md | main | [4e32d245f312](https://github.com/PocoF3Releases/Agents.md/commit/4e32d245f312871f0104c7f5bb922d40d35497db) | newly tracked; latest 20 commits only; 20 |
| android_hardware_nxp_nfc | lineage-24.0 | [8be75516d6d3](https://github.com/PocoF3Releases/android_hardware_nxp_nfc/commit/8be75516d6d3cfff3a95ca2f249f0b36ceededb9) | unchanged; 0 |
| decompiled_miui_camera | aosp-17 | [5d44b65a9220](https://github.com/PocoF3Releases/decompiled_miui_camera/commit/5d44b65a922060da4e6af10566bb4fd8e29b5f7b) | ahead; 2 |
| decompiled_stock_camera | hyperos | [1142e5c6793b](https://github.com/PocoF3Releases/decompiled_stock_camera/commit/1142e5c6793b1a07991267430ab569795f4cd988) | newly tracked; latest 20 commits only; 1 |
| system_core | aosp-17 | [49332070280a](https://github.com/PocoF3Releases/system_core/commit/49332070280a25dedec0373e9f4237a2babd4d57) | newly tracked; latest 20 commits only; 20 |
| vendor_qcom_opensource_usb | aosp-17 | [e6c812452801](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/e6c812452801a1d18445d31a08344ae72df25c04) | newly tracked; latest 20 commits only; 20 |
| system_memory_libmeminfo | alioth-dmabuf-fallback | [f0f3040dbe74](https://github.com/PocoF3Releases/system_memory_libmeminfo/commit/f0f3040dbe74aaa13c8d8a763661a873acd77798) | newly tracked; latest 20 commits only; 20 |

## Resync findings

- frameworks_base diverged: 13 commits on the new side and 4 on the saved side. HBM, screen recording, and Camera2 compatibility commits have new SHAs; the NFC svc fix is now 315a6cb52f29. Use current heads, not old cherry-pick IDs.
- Local frameworks/av is 726c7d331f58, while remote cnb is 8fc27178f6fa.
- Local system/memory/libmeminfo is d3872e43f685, while the remote default branch alioth-dmabuf-fallback is f0f3040dbe74. Do not assume the pushed fallback fix is present in the current checkout.
- A separate ~/hardware_xiaomi checkout differs from remote; the ROM hardware/xiaomi checkout must be considered separately.
- The earlier organization index contained repositories not listed now. Absence is not proof of deletion; preserve their ledgers as historical references.
- Commit indexing verifies Git state only, not implementation correctness or device behavior.

## Ownership and next work

hardware/xiaomi is a standalone reusable hardware integration repository. Do not relocate Dolby or DSPVolumeSynchronizer into a device tree simply to change their directory. The user rejected that approach before any changes were made. Future portability work concerns platform-source dependencies that can genuinely be replaced by device configuration, overlays, modules or existing extension points. No such migration was completed in this refresh.

## Constraints

Use user builds only. Do not rebuild unless requested. Push completed authorized changes. Add the requested Codex attribution only to changes authored by the agent, not picked upstream commits. Keep preserved local work intact.

## Active-index cleanup

Removed six dropped repository ledgers from active tracking. Checked 306 recorded commit candidates against current default heads; removed 20 non-ancestor candidates. Remaining counts are bounded verified records, not all-history totals. Historical release records and Git history are retained but must not be used as current dependency lists.
