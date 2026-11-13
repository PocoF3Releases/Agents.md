# Codex co-author trailer cleanup — 2026-10-31

Historical procedure; superseded by the [attribution/history integrity record](assisted-by-migration-20261113.md).
The old trailer and EOF rule below describe October 31, not current instructions.

`source-checked`, `metadata-verified`. Normalized only messages containing the
exact `Co-authored-by: codex <noreply@openai.com>` attribution. The Codex line is
last and the final byte is `>`: no trailing space, newline or later metadata.
Other trailers were retained and moved before Codex when necessary. No new
Codex attribution was added to commits that lacked it.

Audited 56 maintained repository/branch tips, including the workhub. Corrected
1,118 existing messages across 54 repositories. Rewrote 1,580 affected commit
objects including descendants whose parent IDs necessarily changed. Five
kernel messages previously failed Git trailer parsing; corrected messages all
parse successfully. A terminal newline alone is normally accepted by Git; this
cleanup additionally implements the owner’s stricter exact-ending convention.
The subsequent [full recheck](coauthor-recheck-20261031.md) verifies GitHub API
recognition and corrects four shared upstream identities. The exact-ending
convention applies to fork-local commits; valid upstream formatting stays intact.

For every rewritten object, checked identical tree, author/committer fields and
dates, subject and non-Codex message content. Parent links are mapped without
reordering or dropping commits. Every branch-tip tree is identical to its old
tip. No source, translation, defconfig or runtime behavior changed, so no build
or device test was repeated. The source-refresh graph/regression results remain
applicable to these identical trees.

Backups and complete old/new maps remain private in
`~/evo/.repo/coauthor-cleanup-20261031/`. Published updates use exact expected-head
`--force-with-lease`. Historical evidence keeps the original tested IDs; this
record establishes tree equivalence rather than relabelling those old tests.
The repository ledger tracks the new current tips. Local recovery overlays were
normalized and retained separately from ROM public branches.

## Updated public tips

| Repository | Previous tip | Normalized tip |
| --- | --- | --- |
| [github.com/PocoF3Releases-Recovery/android_bootable_recovery](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery) | `9f67850ac4a5` | [e6fae205afde](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery/commit/e6fae205afde9cd02e14f81fdfd87f8b0c589d8f) |
| [github.com/PocoF3Releases-Recovery/android_build](https://github.com/PocoF3Releases-Recovery/android_build) | `2014d256ff73` | [0acbb8a58c05](https://github.com/PocoF3Releases-Recovery/android_build/commit/0acbb8a58c0514bb4c64e754037bd5936db7cd96) |
| [github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um](https://github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um) | `657627c7d1b1` | [bd967a44b894](https://github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um/commit/bd967a44b89483ea35e5e72d712b9c1daa26ed3e) |
| [github.com/PocoF3Releases-Recovery/android_external_boringssl](https://github.com/PocoF3Releases-Recovery/android_external_boringssl) | `454c1f6cd3ec` | [5f86b8ac3dd2](https://github.com/PocoF3Releases-Recovery/android_external_boringssl/commit/5f86b8ac3dd25e4511f2369088bc54e52f412259) |
| [github.com/PocoF3Releases-Recovery/android_external_bzip2](https://github.com/PocoF3Releases-Recovery/android_external_bzip2) | `935eff0e8e0f` | [159033effbb6](https://github.com/PocoF3Releases-Recovery/android_external_bzip2/commit/159033effbb66eb009e4eed0c8cddf2373af7719) |
| [github.com/PocoF3Releases-Recovery/android_external_ntfs-3g](https://github.com/PocoF3Releases-Recovery/android_external_ntfs-3g) | `833845e0c751` | [cb8dcca0e497](https://github.com/PocoF3Releases-Recovery/android_external_ntfs-3g/commit/cb8dcca0e497a752ba8210bc431850489d663cb3) |
| [github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io](https://github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io) | `3a1cdbc67903` | [0d9aff42f02b](https://github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io/commit/0d9aff42f02b9b781966cf09fcd6ea9a4a883475) |
| [github.com/PocoF3Releases-Recovery/android_external_rust_cxx](https://github.com/PocoF3Releases-Recovery/android_external_rust_cxx) | `d74e4086c81b` | [dffda099d995](https://github.com/PocoF3Releases-Recovery/android_external_rust_cxx/commit/dffda099d9952a7e01bcf9e0d9049be447b8f31b) |
| [github.com/PocoF3Releases-Recovery/android_external_selinux](https://github.com/PocoF3Releases-Recovery/android_external_selinux) | `1bf27a46b9da` | [fca71507a536](https://github.com/PocoF3Releases-Recovery/android_external_selinux/commit/fca71507a53690e1e970d51ec52d27b7d6e92e7b) |
| [github.com/PocoF3Releases-Recovery/android_external_sqlite](https://github.com/PocoF3Releases-Recovery/android_external_sqlite) | `08a06f88fa58` | [4004806b69e0](https://github.com/PocoF3Releases-Recovery/android_external_sqlite/commit/4004806b69e0a9c2363bff1571eb3f0765c2cb68) |
| [github.com/PocoF3Releases-Recovery/android_hardware_interfaces](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces) | `0b8a8b3905eb` | `0c71d78397e25642c6113fc88fdbe8ec3e9e49c1` |
| [github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy](https://github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy) | `b9f2a816a626` | [0b89dc8bc609](https://github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy/commit/0b89dc8bc6091dacd2d06de66111256ea8db9a0e) |
| [github.com/PocoF3Releases/android_hardware_nxp_nfc](https://github.com/PocoF3Releases/android_hardware_nxp_nfc) | `53a125ca706a` | `f1300e6f5e426c012656a18db98e0ab0fa972199` |
| [github.com/PocoF3Releases-Recovery/android_system_apex](https://github.com/PocoF3Releases-Recovery/android_system_apex) | `22980ea950fc` | [8e7d52d44715](https://github.com/PocoF3Releases-Recovery/android_system_apex/commit/8e7d52d447156e9a577619caa9a4604677f07fc6) |
| [github.com/PocoF3Releases-Recovery/android_system_extras](https://github.com/PocoF3Releases-Recovery/android_system_extras) | `798f94453720` | [49e4bcf8d350](https://github.com/PocoF3Releases-Recovery/android_system_extras/commit/49e4bcf8d350124d2ecd08c6873980eca58f4071) |
| [github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces](https://github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces) | `19e36e5f367f` | [3b7c5feb9d4f](https://github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces/commit/3b7c5feb9d4fedee0f391953461d192d1f181117) |
| [github.com/PocoF3Releases-Recovery/android_system_hwservicemanager](https://github.com/PocoF3Releases-Recovery/android_system_hwservicemanager) | `8c1363ab53ca` | [e69c3f9288f2](https://github.com/PocoF3Releases-Recovery/android_system_hwservicemanager/commit/e69c3f9288f2cd2a311ae3e9cf1422e3daf490d4) |
| [github.com/PocoF3Releases-Recovery/android_system_incremental_delivery](https://github.com/PocoF3Releases-Recovery/android_system_incremental_delivery) | `c5fcfdf32d87` | [99d803b894cc](https://github.com/PocoF3Releases-Recovery/android_system_incremental_delivery/commit/99d803b894cc1530f87304cf77b9b025feeb470c) |
| [github.com/PocoF3Releases-Recovery/android_system_keymaster](https://github.com/PocoF3Releases-Recovery/android_system_keymaster) | `2e30ba6d356a` | [5d516038ecac](https://github.com/PocoF3Releases-Recovery/android_system_keymaster/commit/5d516038ecacd2de88cba613e466c895fee8fb80) |
| [github.com/PocoF3Releases-Recovery/android_system_libcppbor](https://github.com/PocoF3Releases-Recovery/android_system_libcppbor) | `54c03dfd7d24` | [96ed3744964e](https://github.com/PocoF3Releases-Recovery/android_system_libcppbor/commit/96ed3744964e31a931c802cdc0b176d26dfa2d6d) |
| [github.com/PocoF3Releases-Recovery/android_system_libhidl](https://github.com/PocoF3Releases-Recovery/android_system_libhidl) | `d81743602448` | [e1158fc1db75](https://github.com/PocoF3Releases-Recovery/android_system_libhidl/commit/e1158fc1db7512c7abec728b6776b54d6e034ec2) |
| [github.com/PocoF3Releases-Recovery/android_system_librustutils](https://github.com/PocoF3Releases-Recovery/android_system_librustutils) | `5f8f3e11e8ce` | [680968bcbff2](https://github.com/PocoF3Releases-Recovery/android_system_librustutils/commit/680968bcbff2efba5206403668f0aece026c387e) |
| [github.com/PocoF3Releases-Recovery/android_system_libvintf](https://github.com/PocoF3Releases-Recovery/android_system_libvintf) | `f06c81ce7cf0` | [e65cc713cffe](https://github.com/PocoF3Releases-Recovery/android_system_libvintf/commit/e65cc713cffe97433e0189cc3402a1234f84d97d) |
| [github.com/PocoF3Releases-Recovery/android_system_logging](https://github.com/PocoF3Releases-Recovery/android_system_logging) | `8af2cd3d340b` | [6efca1ea5ec3](https://github.com/PocoF3Releases-Recovery/android_system_logging/commit/6efca1ea5ec3d56583e3d26c2334d9266e06b585) |
| [github.com/PocoF3Releases-Recovery/android_system_security](https://github.com/PocoF3Releases-Recovery/android_system_security) | `fa9b001dc7f2` | [6c7b703a3a80](https://github.com/PocoF3Releases-Recovery/android_system_security/commit/6c7b703a3a804a815dee22f43b2e0a7018da7bf6) |
| [github.com/PocoF3Releases-Recovery/android_system_sepolicy](https://github.com/PocoF3Releases-Recovery/android_system_sepolicy) | `abbbf28774b4` | [35273169a560](https://github.com/PocoF3Releases-Recovery/android_system_sepolicy/commit/35273169a560d934dabba4615dd81108d0b06b67) |
| [github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags](https://github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags) | `5217f99f1551` | [a9292a01b5d9](https://github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags/commit/a9292a01b5d9b70bf04c350096bbf82066c820a7) |
| [github.com/PocoF3Releases-Recovery/android_system_tools_aidl](https://github.com/PocoF3Releases-Recovery/android_system_tools_aidl) | `de11b4ee3da3` | [d1a01c5cfab4](https://github.com/PocoF3Releases-Recovery/android_system_tools_aidl/commit/d1a01c5cfab496a8af29f04e9d766671b0279908) |
| [github.com/PocoF3Releases-Recovery/android_system_vold](https://github.com/PocoF3Releases-Recovery/android_system_vold) | `51ede7310adb` | [b3d25274ed56](https://github.com/PocoF3Releases-Recovery/android_system_vold/commit/b3d25274ed5690296848608e957747b0f5485645) |
| [github.com/PocoF3Releases/device_xiaomi_alioth](https://github.com/PocoF3Releases/device_xiaomi_alioth) | `041a88702340` | [d0e838d2a883](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/d0e838d2a8830c71585cbe22101c534d7129e6b3) |
| [github.com/PocoF3Releases/device_xiaomi_camera](https://github.com/PocoF3Releases/device_xiaomi_camera) | `a72242890b4a` | `4c953d2a5255ec84742f935f8af0fa5a86c3cbf2` |
| [github.com/PocoF3Releases/device_xiaomi_sm8250-common](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common) | `381d2673a31a` | `b53a218daacd4242a54fa5d5067a6a0299fe7f2e` |
| [github.com/PocoF3Releases/external_tinycompress](https://github.com/PocoF3Releases/external_tinycompress) | `6e5f9422ece8` | [1d4f503785d1](https://github.com/PocoF3Releases/external_tinycompress/commit/1d4f503785d13fd5cd081f8bad8a34fab9ccc18b) |
| [github.com/PocoF3Releases/frameworks_av](https://github.com/PocoF3Releases/frameworks_av) | `eecb939f5835` | `0c471ea794d999884744c0843c73a70320ed44d1` |
| [github.com/PocoF3Releases/frameworks_base](https://github.com/PocoF3Releases/frameworks_base) | `faeec1083640` | `f154e5aa0c5001385be9bf37e28246bac697a0ac` |
| [github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media) | `60f362cedc69` | `009aea140157fc7a1bc419b14bae080bac6139d6` |
| [github.com/PocoF3Releases/hardware_xiaomi](https://github.com/PocoF3Releases/hardware_xiaomi) | `8119f09b8af1` | `4e25bc3a2a4297f4b6b858c1d5f66d147be37457` |
| [github.com/PocoF3Releases/kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250) | `7d559e98d4d9` | `830fb30974c82ef91080e9295b90169bb97661da` |
| [github.com/PocoF3Releases/vendor_qcom_opensource_usb](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb) | `34a2c8bb9b07` | [580202cb6cfa](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/580202cb6cfa26cfae88fc6d2ffa3dab9cd75165) |
| [github.com/PocoF3Releases/vendor_xiaomi_alioth](https://github.com/PocoF3Releases/vendor_xiaomi_alioth) | `3b312ac9d0a3` | [06a0ca80b0fd](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/06a0ca80b0fdc3f5f71e9eda30298c6d3c317359) |
| [github.com/PocoF3Releases/vendor_xiaomi_sm8250-common](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common) | `1e11ce1c7634` | `bae0e794c9d6c96d45b8310b47e5f49448b45a75` |
| [github.com/PocoF3Releases/android_hardware_interfaces](https://github.com/PocoF3Releases/android_hardware_interfaces) | `810a827dcdfb` | `379ef3334b3a2a0a0ea70647dc1d82df9810cb72` |
| [github.com/pbrp-alioth/device_xiaomi_alioth-pbrp](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp) | `1dcf2e2e1a26` | [824cfd3200ad](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp/commit/824cfd3200ad329559830dd98c2e355ca4eed6ca) |
| [github.com/PocoF3Releases/.github](https://github.com/PocoF3Releases/.github) | `c48fe9bdb16f` | [37336d796f39](https://github.com/PocoF3Releases/.github/commit/37336d796f398170ac513d72bc544fec0e28c5fa) |
| [github.com/PocoF3Releases/references_code](https://github.com/PocoF3Releases/references_code) | `f78ee3106b1d` | [041e06eccdbd](https://github.com/PocoF3Releases/references_code/commit/041e06eccdbd47330cc940238e379c8a34062986) |
| [github.com/johnmart19/repoindex](https://github.com/johnmart19/repoindex) | `549b2eec1cdf` | [bcaf362ea23a](https://github.com/johnmart19/repoindex/commit/bcaf362ea23a755a296cc2a2c8cbeab59aa15c69) |
| [github.com/pbrp-alioth/android_bootable_recovery](https://github.com/pbrp-alioth/android_bootable_recovery) | `ef490e810b0a` | [3a9b3e7c0759](https://github.com/pbrp-alioth/android_bootable_recovery/commit/3a9b3e7c0759e88cad7916ca5ce4460a9972f5fb) |
| [github.com/pbrp-alioth/vendor_pb](https://github.com/pbrp-alioth/vendor_pb) | `4f5dc08aafdb` | [b259e9b1eaae](https://github.com/pbrp-alioth/vendor_pb/commit/b259e9b1eaae0ffc0de6881dbf4c821b44156a7f) |
| [github.com/pbrp-alioth/android_system_sepolicy](https://github.com/pbrp-alioth/android_system_sepolicy) | `edc77e62099a` | [d9fb04f29f93](https://github.com/pbrp-alioth/android_system_sepolicy/commit/d9fb04f29f9326f053578a6d9fd279d7e510a411) |
| [github.com/pbrp-alioth/android_external_f2fs-tools](https://github.com/pbrp-alioth/android_external_f2fs-tools) | `efd0dc9a3a58` | [ae3425c2b760](https://github.com/pbrp-alioth/android_external_f2fs-tools/commit/ae3425c2b7606f4bc1f95ee9bb32f0cf8b91d2a7) |
| [github.com/PocoF3Releases-Recovery/local_manifests](https://github.com/PocoF3Releases-Recovery/local_manifests) | `1816695ed87b` | [e00be6fe9e11](https://github.com/PocoF3Releases-Recovery/local_manifests/commit/e00be6fe9e11744ea24c922e5f2d1d3f7bec7e89) |
| [github.com/PocoF3Releases-Recovery/.github](https://github.com/PocoF3Releases-Recovery/.github) | `917c225d6ce7` | [0e82a02f633f](https://github.com/PocoF3Releases-Recovery/.github/commit/0e82a02f633f7483c97a38149cb7b4399d4436a2) |
| [gitlab.com/johnmart19/vendor_xiaomi_camera](https://gitlab.com/johnmart19/vendor_xiaomi_camera) | `607c5b881ccf` | `b44ae434d8257ed282dca59b0fa72c6b97ea9662` |

The workhub’s normalized historical tip is recorded in the enclosing commit’s
parent; this evidence/ledger update is an additional documentation commit.

All 54 affected repositories are published and remote-verified, including the
GitLab camera `aosp-17` branch after authentication was restored. Its local
push transport uses GitLab SSH over port 443; no keys or credentials are stored
in this workhub. The camera source tree remains identical.
