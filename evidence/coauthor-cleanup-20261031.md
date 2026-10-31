# Codex co-author trailer cleanup — 2026-10-31

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
| [github.com/PocoF3Releases-Recovery/android_bootable_recovery](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery) | `9f67850ac4a5` | [b7d818a1df52](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery/commit/b7d818a1df52537646a73963885106c5a9e09505) |
| [github.com/PocoF3Releases-Recovery/android_build](https://github.com/PocoF3Releases-Recovery/android_build) | `2014d256ff73` | [862350971ca3](https://github.com/PocoF3Releases-Recovery/android_build/commit/862350971ca32fdcfbb6f032487d9531ab94e80f) |
| [github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um](https://github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um) | `657627c7d1b1` | [c1cb198db7a8](https://github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um/commit/c1cb198db7a80b30a6338f48a22315ec3d5d9d31) |
| [github.com/PocoF3Releases-Recovery/android_external_boringssl](https://github.com/PocoF3Releases-Recovery/android_external_boringssl) | `454c1f6cd3ec` | [21b7b20184c6](https://github.com/PocoF3Releases-Recovery/android_external_boringssl/commit/21b7b20184c60a8653452e13c8bfcbcc1f9ea5d3) |
| [github.com/PocoF3Releases-Recovery/android_external_bzip2](https://github.com/PocoF3Releases-Recovery/android_external_bzip2) | `935eff0e8e0f` | [db60114736fc](https://github.com/PocoF3Releases-Recovery/android_external_bzip2/commit/db60114736fcd25df65f0c12871bd69dd9ac31d5) |
| [github.com/PocoF3Releases-Recovery/android_external_ntfs-3g](https://github.com/PocoF3Releases-Recovery/android_external_ntfs-3g) | `833845e0c751` | [be07b5ebb189](https://github.com/PocoF3Releases-Recovery/android_external_ntfs-3g/commit/be07b5ebb1893193d1b682b50133e3ab461594c6) |
| [github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io](https://github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io) | `3a1cdbc67903` | [623f387a512d](https://github.com/PocoF3Releases-Recovery/android_external_rust_android-crates-io/commit/623f387a512dce4017bc792ff860f95f7825291d) |
| [github.com/PocoF3Releases-Recovery/android_external_rust_cxx](https://github.com/PocoF3Releases-Recovery/android_external_rust_cxx) | `d74e4086c81b` | [e79d0f8a15f2](https://github.com/PocoF3Releases-Recovery/android_external_rust_cxx/commit/e79d0f8a15f292951c7444b1842ffd0ca5ecaec8) |
| [github.com/PocoF3Releases-Recovery/android_external_selinux](https://github.com/PocoF3Releases-Recovery/android_external_selinux) | `1bf27a46b9da` | [be44cb1d1b60](https://github.com/PocoF3Releases-Recovery/android_external_selinux/commit/be44cb1d1b6026ce9aa9d73dbede2414c46829d0) |
| [github.com/PocoF3Releases-Recovery/android_external_sqlite](https://github.com/PocoF3Releases-Recovery/android_external_sqlite) | `08a06f88fa58` | [208e726b43ce](https://github.com/PocoF3Releases-Recovery/android_external_sqlite/commit/208e726b43ce1218a07979532b5f551c1ee19772) |
| [github.com/PocoF3Releases-Recovery/android_hardware_interfaces](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces) | `0b8a8b3905eb` | [0c71d78397e2](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/0c71d78397e25642c6113fc88fdbe8ec3e9e49c1) |
| [github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy](https://github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy) | `b9f2a816a626` | [2c7b16990d39](https://github.com/PocoF3Releases-Recovery/android_hardware_libhardware_legacy/commit/2c7b16990d393165c7e347adb35f51e4f8ffd03f) |
| [github.com/PocoF3Releases/android_hardware_nxp_nfc](https://github.com/PocoF3Releases/android_hardware_nxp_nfc) | `53a125ca706a` | [f1300e6f5e42](https://github.com/PocoF3Releases/android_hardware_nxp_nfc/commit/f1300e6f5e426c012656a18db98e0ab0fa972199) |
| [github.com/PocoF3Releases-Recovery/android_system_apex](https://github.com/PocoF3Releases-Recovery/android_system_apex) | `22980ea950fc` | [390727e35e90](https://github.com/PocoF3Releases-Recovery/android_system_apex/commit/390727e35e900478432815b6a77a510a965e2e87) |
| [github.com/PocoF3Releases-Recovery/android_system_extras](https://github.com/PocoF3Releases-Recovery/android_system_extras) | `798f94453720` | [e5b2888a93a9](https://github.com/PocoF3Releases-Recovery/android_system_extras/commit/e5b2888a93a9c78779beec10b736bcdb203a553b) |
| [github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces](https://github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces) | `19e36e5f367f` | [c7992d2edc56](https://github.com/PocoF3Releases-Recovery/android_system_hardware_interfaces/commit/c7992d2edc56c6449f3c001dcb1c96b32c5fafe4) |
| [github.com/PocoF3Releases-Recovery/android_system_hwservicemanager](https://github.com/PocoF3Releases-Recovery/android_system_hwservicemanager) | `8c1363ab53ca` | [c09958e6974c](https://github.com/PocoF3Releases-Recovery/android_system_hwservicemanager/commit/c09958e6974cd933913978c817d9c6b1ef297ed6) |
| [github.com/PocoF3Releases-Recovery/android_system_incremental_delivery](https://github.com/PocoF3Releases-Recovery/android_system_incremental_delivery) | `c5fcfdf32d87` | [1cb3901a1ca1](https://github.com/PocoF3Releases-Recovery/android_system_incremental_delivery/commit/1cb3901a1ca173abc0b5275d249602b26b39aae9) |
| [github.com/PocoF3Releases-Recovery/android_system_keymaster](https://github.com/PocoF3Releases-Recovery/android_system_keymaster) | `2e30ba6d356a` | [35d808641acd](https://github.com/PocoF3Releases-Recovery/android_system_keymaster/commit/35d808641acdaf3563029f4556f0ddda84ac0010) |
| [github.com/PocoF3Releases-Recovery/android_system_libcppbor](https://github.com/PocoF3Releases-Recovery/android_system_libcppbor) | `54c03dfd7d24` | [c24c18e5e111](https://github.com/PocoF3Releases-Recovery/android_system_libcppbor/commit/c24c18e5e11106a0df1e78b4e76ad5854e61a21e) |
| [github.com/PocoF3Releases-Recovery/android_system_libhidl](https://github.com/PocoF3Releases-Recovery/android_system_libhidl) | `d81743602448` | [99226330971a](https://github.com/PocoF3Releases-Recovery/android_system_libhidl/commit/99226330971ab596240d6efaad8dee92e457ab13) |
| [github.com/PocoF3Releases-Recovery/android_system_librustutils](https://github.com/PocoF3Releases-Recovery/android_system_librustutils) | `5f8f3e11e8ce` | [8c21d66429e4](https://github.com/PocoF3Releases-Recovery/android_system_librustutils/commit/8c21d66429e42dffe7cbc56aac54796d9d6d8177) |
| [github.com/PocoF3Releases-Recovery/android_system_libvintf](https://github.com/PocoF3Releases-Recovery/android_system_libvintf) | `f06c81ce7cf0` | [8f2d46d8de33](https://github.com/PocoF3Releases-Recovery/android_system_libvintf/commit/8f2d46d8de33be85f92084ad2bf49538207a32db) |
| [github.com/PocoF3Releases-Recovery/android_system_logging](https://github.com/PocoF3Releases-Recovery/android_system_logging) | `8af2cd3d340b` | [fd0b6192b701](https://github.com/PocoF3Releases-Recovery/android_system_logging/commit/fd0b6192b70186fea5e65bd0f90cc5c9ba850337) |
| [github.com/PocoF3Releases-Recovery/android_system_security](https://github.com/PocoF3Releases-Recovery/android_system_security) | `fa9b001dc7f2` | [3b28da961170](https://github.com/PocoF3Releases-Recovery/android_system_security/commit/3b28da961170c7192b0ff6a5d2b2f2dc3eafb5f8) |
| [github.com/PocoF3Releases-Recovery/android_system_sepolicy](https://github.com/PocoF3Releases-Recovery/android_system_sepolicy) | `abbbf28774b4` | [39adc027c66c](https://github.com/PocoF3Releases-Recovery/android_system_sepolicy/commit/39adc027c66cb4b61b768ebef993c60f4c9b24ff) |
| [github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags](https://github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags) | `5217f99f1551` | [e8d5ba401470](https://github.com/PocoF3Releases-Recovery/android_system_server_configurable_flags/commit/e8d5ba401470fb8a982f8db775fc9747b3f22131) |
| [github.com/PocoF3Releases-Recovery/android_system_tools_aidl](https://github.com/PocoF3Releases-Recovery/android_system_tools_aidl) | `de11b4ee3da3` | [fcbf49d306a2](https://github.com/PocoF3Releases-Recovery/android_system_tools_aidl/commit/fcbf49d306a2fa99d90c2626a8a1363799cf31a1) |
| [github.com/PocoF3Releases-Recovery/android_system_vold](https://github.com/PocoF3Releases-Recovery/android_system_vold) | `51ede7310adb` | [e64e54fcee0e](https://github.com/PocoF3Releases-Recovery/android_system_vold/commit/e64e54fcee0e4172a21b38d5090e49b9c54458d9) |
| [github.com/PocoF3Releases/device_xiaomi_alioth](https://github.com/PocoF3Releases/device_xiaomi_alioth) | `041a88702340` | [749a229f36b0](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/749a229f36b05bf08254b287b7f1b7c297df0bd3) |
| [github.com/PocoF3Releases/device_xiaomi_camera](https://github.com/PocoF3Releases/device_xiaomi_camera) | `a72242890b4a` | [4c953d2a5255](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/4c953d2a5255ec84742f935f8af0fa5a86c3cbf2) |
| [github.com/PocoF3Releases/device_xiaomi_sm8250-common](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common) | `381d2673a31a` | [b53a218daacd](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/b53a218daacd4242a54fa5d5067a6a0299fe7f2e) |
| [github.com/PocoF3Releases/external_tinycompress](https://github.com/PocoF3Releases/external_tinycompress) | `6e5f9422ece8` | [f55142aedd63](https://github.com/PocoF3Releases/external_tinycompress/commit/f55142aedd6392c667b5f9b48880641867100488) |
| [github.com/PocoF3Releases/frameworks_av](https://github.com/PocoF3Releases/frameworks_av) | `eecb939f5835` | [0c471ea794d9](https://github.com/PocoF3Releases/frameworks_av/commit/0c471ea794d999884744c0843c73a70320ed44d1) |
| [github.com/PocoF3Releases/frameworks_base](https://github.com/PocoF3Releases/frameworks_base) | `faeec1083640` | [f154e5aa0c50](https://github.com/PocoF3Releases/frameworks_base/commit/f154e5aa0c5001385be9bf37e28246bac697a0ac) |
| [github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media) | `60f362cedc69` | [009aea140157](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media/commit/009aea140157fc7a1bc419b14bae080bac6139d6) |
| [github.com/PocoF3Releases/hardware_xiaomi](https://github.com/PocoF3Releases/hardware_xiaomi) | `8119f09b8af1` | [4e25bc3a2a42](https://github.com/PocoF3Releases/hardware_xiaomi/commit/4e25bc3a2a4297f4b6b858c1d5f66d147be37457) |
| [github.com/PocoF3Releases/kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250) | `7d559e98d4d9` | [830fb30974c8](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/830fb30974c82ef91080e9295b90169bb97661da) |
| [github.com/PocoF3Releases/vendor_qcom_opensource_usb](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb) | `34a2c8bb9b07` | [7dbc815ad052](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/7dbc815ad052d113eaf63e2bb0f172b3bb232452) |
| [github.com/PocoF3Releases/vendor_xiaomi_alioth](https://github.com/PocoF3Releases/vendor_xiaomi_alioth) | `3b312ac9d0a3` | [e83c84d6cf30](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/e83c84d6cf306fc2cce649a088b9761ac0f28cef) |
| [github.com/PocoF3Releases/vendor_xiaomi_sm8250-common](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common) | `1e11ce1c7634` | [bae0e794c9d6](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/bae0e794c9d6c96d45b8310b47e5f49448b45a75) |
| [github.com/PocoF3Releases/android_hardware_interfaces](https://github.com/PocoF3Releases/android_hardware_interfaces) | `810a827dcdfb` | [379ef3334b3a](https://github.com/PocoF3Releases/android_hardware_interfaces/commit/379ef3334b3a2a0a0ea70647dc1d82df9810cb72) |
| [github.com/pbrp-alioth/device_xiaomi_alioth-pbrp](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp) | `1dcf2e2e1a26` | [824cfd3200ad](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp/commit/824cfd3200ad329559830dd98c2e355ca4eed6ca) |
| [github.com/PocoF3Releases/.github](https://github.com/PocoF3Releases/.github) | `c48fe9bdb16f` | [9554477eb992](https://github.com/PocoF3Releases/.github/commit/9554477eb992b86115de4e4194953f8e30ba0c19) |
| [github.com/PocoF3Releases/references_code](https://github.com/PocoF3Releases/references_code) | `f78ee3106b1d` | [81f4ad1ca8e3](https://github.com/PocoF3Releases/references_code/commit/81f4ad1ca8e32f251e30dd33d64b945a4a37a021) |
| [github.com/johnmart19/repoindex](https://github.com/johnmart19/repoindex) | `549b2eec1cdf` | [bcaf362ea23a](https://github.com/johnmart19/repoindex/commit/bcaf362ea23a755a296cc2a2c8cbeab59aa15c69) |
| [github.com/pbrp-alioth/android_bootable_recovery](https://github.com/pbrp-alioth/android_bootable_recovery) | `ef490e810b0a` | [3a9b3e7c0759](https://github.com/pbrp-alioth/android_bootable_recovery/commit/3a9b3e7c0759e88cad7916ca5ce4460a9972f5fb) |
| [github.com/pbrp-alioth/vendor_pb](https://github.com/pbrp-alioth/vendor_pb) | `4f5dc08aafdb` | [b259e9b1eaae](https://github.com/pbrp-alioth/vendor_pb/commit/b259e9b1eaae0ffc0de6881dbf4c821b44156a7f) |
| [github.com/pbrp-alioth/android_system_sepolicy](https://github.com/pbrp-alioth/android_system_sepolicy) | `edc77e62099a` | [d9fb04f29f93](https://github.com/pbrp-alioth/android_system_sepolicy/commit/d9fb04f29f9326f053578a6d9fd279d7e510a411) |
| [github.com/pbrp-alioth/android_external_f2fs-tools](https://github.com/pbrp-alioth/android_external_f2fs-tools) | `efd0dc9a3a58` | [ae3425c2b760](https://github.com/pbrp-alioth/android_external_f2fs-tools/commit/ae3425c2b7606f4bc1f95ee9bb32f0cf8b91d2a7) |
| [github.com/PocoF3Releases-Recovery/local_manifests](https://github.com/PocoF3Releases-Recovery/local_manifests) | `1816695ed87b` | [a553a449d6a5](https://github.com/PocoF3Releases-Recovery/local_manifests/commit/a553a449d6a5881b6f3bda762320ba14121c3f2e) |
| [github.com/PocoF3Releases-Recovery/.github](https://github.com/PocoF3Releases-Recovery/.github) | `917c225d6ce7` | [269ea619b7de](https://github.com/PocoF3Releases-Recovery/.github/commit/269ea619b7deffe5fbc20db1a7dfa3c3b6d11b48) |
| [gitlab.com/johnmart19/vendor_xiaomi_camera](https://gitlab.com/johnmart19/vendor_xiaomi_camera) | `607c5b881ccf` | [b44ae434d825](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/b44ae434d8257ed282dca59b0fa72c6b97ea9662) |

The workhub’s normalized historical tip is recorded in the enclosing commit’s
parent; this evidence/ledger update is an additional documentation commit.

All 54 affected repositories are published and remote-verified, including the
GitLab camera `aosp-17` branch after authentication was restored. Its local
push transport uses GitLab SSH over port 443; no keys or credentials are stored
in this workhub. The camera source tree remains identical.
