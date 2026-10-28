# Voice-message and VoIP capture recovery — October 25, 2026

## Reproduced native integration defect

The shipped primary HAL's cin_read (ELF VA 0x92140) expects the requested byte
count from compress_read and returns errno on a mismatch. The library could
return a short count after blocking poll timeout or EOF with errno still zero.
That made incomplete data appear successful. The attached compressed-capture
error path in in_read (0x5a8b8) can still return the requested frame size without
clearing the unread tail, so error reporting alone is insufficient protection.

A fake backend exercised the actual production read implementation and a minimal
legacy mismatch/errno check. The original installed 32-bit shared library failed
nine of thirteen early-exit/buffer cases. This is controlled fault injection into
library operations, not a claim that a physical DSP timeout was triggered.

[The capture fix](https://github.com/PocoF3Releases/external_tinycompress/commit/6e5f9422ece80862ad578ddf5e07d2c1e6fdd6c9) supplies ETIMEDOUT on blocking poll timeout and ENODATA on blocking
EOF. On blocking early termination it clears only the unread buffer remainder,
including hard-error and pause exits. Captured bytes and returned byte counts/
negative errors are preserved. Full reads do no additional clearing; nonblocking
short/zero/EOF behavior and errno remain unchanged. No DSP tuning, ACDB, input
profile, gain or recording-source policy is changed.

## Verification

- Thirteen production-source cases pass on the host and under ASan/UBSan, including
  prefix/tail bytes and guard checks: zero/partial timeout and EOF, availability/
  poll/read errors, read/poll EBADFD, full reads with pre-existing errno, and
  nonblocking partial/zero/EOF behavior.
- The rebuilt ARM32 and ARM64 shared libraries each pass those thirteen cases on
  the enforcing phone through dlopen/dlsym. These tests exercise the built library,
  not merely a separately reimplemented algorithm.
- Both platform library variants build and retain their exported interfaces.
- A temporary Magisk library overlay was loaded after reboot. The audio HAL's
  mapped library and installed hashes were checked before runtime tests.
- Before and after the overlay, microphone AAC at 16 kHz and voice-recognition
  Opus at 48 kHz each captured 16000/48000 samples, emitted encoded packets with
  nondecreasing timestamps and completed EOS. Encoded bytes stayed in memory;
  no captured or encoded audio file was saved or transmitted.
- Eight same-object voice-recording start/stop cycles pass on each build.
- Updated-library 48 kHz duplex voice capture with AEC/NS passes; silent playback
  renders 139200 frames with zero underruns. The crash buffer is empty.

The two independent GPT-6.1-Sol agents used low reasoning. One established the
capture error contract and reviewed the final patch; the other found no proven
new Dolby/MiSound lifecycle regression. An inherited STOP-running-state concern
was not changed because normal standby closes the native handle and no affected
phone path was established. No speculative global VQE insertion was added.

These are targeted native/API/codec smoke tests, not validation of every messaging
application, remote calls, packet transport, acoustic AEC quality, physical
headsets or every hardware compressed-capture route. No outgoing call/SMS was used.

## Temporary deployment and source separation

Original versus tested candidate library SHA-256:

| Variant | Original | Candidate |
| --- | --- | --- |
| ARM32 | 7ca2bc349338a9c3274df327e74ba6a498000bfc61c210de1c3275debef73ac0 | 72a637d78bb496ea36f9d5be24c2aa3512f0d643cd23b165cd8287089a69caa2 |
| ARM64 | e2e75639b24979a85a54d4dba13b51ec7a1879ffcd04b9ff4dbe943a7746d04e | 11b3f19c2801491cb52d8843bf681a4c25e96c939d04db77f967f7f18d4f60cd |

The capture fix is a standalone tinycompress commit. The hardware/xiaomi
[translation/resource cleanup](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b653ae1cbb59c26410eae3b1b22e0029781d254a)
remains separate and unchanged. Recovery source overlays and other audio features
are not modified. Permanent inclusion requires the next full ROM build; the
phone overlay is diagnostic only. After the overlay was removed, Android booted,
both original library hashes were restored exactly, requested/actual audio mode
was MODE_NORMAL and SELinux remained Enforcing. All diagnostic files were removed;
no package or saved preference was changed.

## Final capture, VoIP and playback recheck

Two new independent GPT-6.1-Sol agents using low reasoning found no actionable
API or downstream-caller regression. Only compress_read changes; compressed
playback write/start/drain/offload handling remains unchanged. They identified
one coverage gap rather than a source defect: successful poll with POLLERR
following a captured prefix. This added case passes with -1/EIO, preserved
captured bytes, a cleared unread tail and intact guards.

The expanded fourteen-case suite passes on the host, under ASan/UBSan and through
each actual rebuilt ARM32/ARM64 shared library on the enforcing phone. The shared
library loaded by the audio HAL was verified by mapped/installed inode equality.
No new source edit or library rebuild was needed for this recheck.

Before and with the temporary updated-library overlay, two normal 48 kHz stereo
PCM runs with pause/flush/resume pass, each reporting 88320 frames after the flush
and zero underruns. Hardware-offloaded MP3 playback also passes on both libraries:
48384 synthetic-silence bytes drain through an explicitly offloaded AudioTrack,
with presentation-ended acknowledgment and zero underruns. No global volume
setting was changed. This validates playback operation, not subjective sound.

Updated-library AAC/Opus capture-to-encode/EOS, eight same-object recording restart
cycles and 48 kHz AEC/NS duplex capture/playback pass again. Duplex playback
reports 139200 frames and zero underruns; requested/actual mode returns to normal
and the crash buffer remains empty. After this recheck the temporary module was
removed and both original library hashes were verified again. Android booted,
audio mode was MODE_NORMAL and SELinux was Enforcing. All device diagnostic
files, including the generated silent MP3, were removed.

The [capture commit](https://github.com/PocoF3Releases/external_tinycompress/commit/6e5f9422ece80862ad578ddf5e07d2c1e6fdd6c9) is unchanged; translation/resource changes remain solely
in their existing separate hardware/xiaomi commit. No additional production
correction was needed after this review.
