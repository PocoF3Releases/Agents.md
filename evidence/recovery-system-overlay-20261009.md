# Recovery System-overlay diagnosis


User temporarily booted the release-candidate image; UI works, Magisk install
and decryption fail. Read-only Windows ADB sync found dm-1 mounted at both
/system_root and /system. The visible /system/bin/sh exists (310272 bytes), but
its ELF interpreter /system/bin/linker64 is absent. Thus the ADB shell reports
ENOENT despite the executable being present. Staged recovery has its own shell
and linker; the System mount hides that runtime. This explains command-launch
failure; specific decryption/Magisk logs and active slot remain inaccessible.
Do not attribute all failures to slot mismatch or claim a confirmed repair.
Recovery logs and dm-name/cmdline reads are permission-denied; do not weaken
policy. A reversible UI System unmount is the next diagnostic comparison.
`~/pbrp-alioth/out` is allowed; `~/evo/out` must never be accessed.
