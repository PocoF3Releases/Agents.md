# AC-4 playback validation and Thermal Profiles checkpoint

## Final state

AC-4 decoding and audible playback are confirmed on the rebuilt Alioth Android 17 `user` build dated September 24, 05:07:46 UTC. The device was non-rooted for this test. The user explicitly confirmed audible playback of the supplied video. This supersedes the earlier failed AC-4 tests, not unrelated Dolby effect validation.

Source heads at documentation time:

- `frameworks/av`, branch `cnb`: `ae242b56da334c3b1605bbbc526cc4e8a47cce45`.
- `device/xiaomi/sm8250-common`, branch `aosp-17`: `3c30e7d416cd91e51c1c95ce81d55b20e60c570c`.
- The latter includes the Thermal Profiles UI fix subsequently approved by the maintainer as working as intended.

## AC-4 implementation and failure progression

1. `801d9c6ecd`: default-off `media.dolby_ac4_21_entry_tables` build option; Alioth B/C tables have 21 entries (84 bytes).
2. `6c0db963ed5111efb8d6e9820de7b19dc241ab05`: opted-in private OMX request is 452 bytes, with tables A/B/C at offsets `0x1c`, `0x11c`, `0x170`. Legacy request remains 444 bytes. Size checks and error propagation guard the opted-in path.
3. `ae242b56da`: opted-in stock table index `0x6f400009`; default remains `OMX_IndexParamAudioAndroidAc4Tbl` (`0x6f400008`). Do not change the shared OMX enum or Codec2 behavior. Option-on/off 32/64-bit syntax checks passed.
4. Common-tree `428db4a` enables the option for this device family.
5. Common-tree `e019493` installs `dolby_ac4_omx_legacy_path`: `/vendor/lib/vndk/libstagefright_omx.so` points to `/vendor/lib/libstagefright_omx.so`, and explicitly packages `libstagefright_omx.vendor`.

The first rebuilt test rejected index `0x6f400008` with `UnsupportedIndex` (`0x8000101a`, configure -1010). After correcting the index, `Error 4 in dlb_ac4dec_input_stage_open` remained. Disassembly showed the decoder loads an XOR-obfuscated legacy OMX helper path and resolves `function_a`, `function_b`, `function_c`; return 4 covers missing library/symbols. The current vendor OMX helper exports these functions. Restoring its lookup path resolved decoding. Do not misdiagnose this as bad table bytes or import an entire old VNDK stack.

## Runtime evidence

Official [Dolby sample](https://ott.dolby.com/OnDelKits/AC-4/Dolby_AC-4_Online_Delivery_Kit_1.5/Test_Signals/muxed_streams/MP4/Example/Audio_ID_720p_25fps_h264_2ch_64kbps_ac4.mp4): 32 seconds, stereo, 48 kHz. A shell `app_process` diagnostic explicitly selected `OMX.dolby.ac4.decoder`, extracted samples and checked decoded PCM:

```text
CREATED OMX.dolby.ac4.decoder
OUTPUT {sample-rate=48000, pcm-encoding=2, mime=audio/raw, channel-count=2}
RESULT input=800 outputBuffers=800 pcmBytes=6144000 nonzeroBytes=5970795 eos=true
PASS
```

Checked-in [diagnostic source and decisive output](../evidence/ac4/README.md) are available without WSL. The following local paths are optional raw-evidence provenance, not remote-access prerequisites.

Local evidence: `~/evo17/out/ac4-device-test/symlink-retest.txt` and `symlink-retest-logcat.txt`; helper source `Ac4Test.java`. Earlier `decode-result.txt` and `retest-result.txt` document the two failures. The diagnostic itself is silent. The original video was separately uploaded to `/sdcard/Download/Dolby-AC4-stereo-test.mp4` and opened for listening; the user confirmed it works. Player identity was not established. This validates the tested stream, not every AC-4 presentation, multichannel configuration, application or offload path. The agent did not rebuild the ROM; the user supplied rebuilt installations.

## Stock, Marble and VNDK audit conclusions

- Alioth stock and shipped decoder code/rodata match; dependency rewriting accounts for differences. Stock table A is 256 bytes and B/C are 84 bytes; the current values match stock. Evidence: `~/evo17/out/dolby-stock-audit`.
- Marble uses a 64-bit Codec2 AC-4 component, not this OMX ABI. Selected `hardware_dolby:cnb-aospa` even comments out AC-4 registration. Its A table matched; searches did not establish B/C dimensions. It is not a drop-in replacement or evidence for changing the global OMX table layout. Evidence: `~/evo17/out/marble-ac4-audit/README.md`.
- Stock `vendor/lib/vndk` contains regular OMX, foundation and xlog libraries; no stock `lib64/vndk` directory was found. Only the OMX compatibility path required restoration.
- Dolby dependencies already use shipped `libstagefright_foundation-v33.so`; current OMX uses current `libstagefright_foundation.so`. Do not redirect it to v33. No additional absolute foundation lookup was found.
- Stock audio/sound-trigger HALs in both ABIs reference `vendor/lib/vndk/libxlog.so`. Shipped proprietary lists use the 32-bit HALs and already include this xlog file; the source-built 64-bit audio HAL does not reference it. No further symlink was warranted. Evidence: `~/evo17/out/vndk-path-audit`.
- Audio and OMX services remain 32-bit. Removing all 32-bit support would break existing dependencies; no 64-bit-only migration was implemented.

## Thermal Profiles regression and current fix

`db27251` removed a fixed bottom inset that caused excessive space above Cancel. The next user screenshots showed rows drawing under both the title and Cancel panel, so that revision was insufficient.

`3c30e7d` updates the shared `showProfileDialog` in `parts/src/org/lineageos/settings/thermal/ThermalSettingsFragment.java`: measure actual overlap with `topPanel` and `buttonPanel`, clip rows between the panels, and apply only the required padding while retaining original padding. Padding is changed only when necessary to avoid a layout loop. System and per-app dialogs share the fix. Touch profile behavior is unchanged.

Validation: source review and `git diff --check`, followed by maintainer approval: "Parts fix approved, works as intended." The supplied `Screenshot_20260924-090438_Settings.png` (original filename has a localized Settings suffix) shows the System Profile list clipped between its title and Cancel panels. No new build or device test was run by the agent for this acceptance update. The screenshot documents the system dialog; do not infer separately executed per-app testing. The changelog item is no longer awaiting visual acceptance.
