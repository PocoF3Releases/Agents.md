# Installed rebuild: short smoke test

Observation: 2026-10-25. User reports the rebuild installed; device-tested.
Android 17 / SDK 37, build timestamp 1792904755. Boot completed; SELinux enforcing.

Installed component identities match the accepted build artifacts:
- XiaomiParts: 8d4daaeaeb784e5a04eabb3ffcaced87540ef35acb78c87667e3cfcaed7f1da6
- XiaomiDolby: a80121867b3d98de284975202aaa9bf395a5ca4594b296a1eb24e8e49d98be9a
- FM_CAM.bin: 5493b05bf10d5f768a1511e521a9d69820d4c592953562d7901b948cb3cbad5a

Settings, MiSound and Dolby activities all returned launch Status ok. Wi-Fi was
connected and a two-packet internet connectivity check had zero packet loss.
Battery was present with health GOOD. USB/ADB stayed available.

The user's saved MiSound Off, Dolby On and communication-pause preferences were
preserved. Short MIC/recognition/communication capture and silent playback,
rapid start/stop, communication duplex, actual earpiece/speaker selection and
normal-mode restoration passed. Exact preference hashes matched before/after.
Capture buffers were discarded. Audioserver PID stayed unchanged.

Installed 32-bit FCSAM initialization returned zero using the packaged vendor
library and stock parameter file. The file has vendor_configs_file context.
An initial ordinary-shell attempt could not access the vendor library; root
diagnostic execution succeeded. This is initialization/readback acceptance, not
acoustic audio-zoom or production HAL-domain access proof. Native game-backend
selector reads qcom-qdsp under the permitted diagnostic context.

The current boot crash buffer was empty and no ANR-in matches were found in the
available ActivityManager log. No source change was needed. Temporary probes and
copied preference files were removed; saved settings were not changed.

This was a short installed-build smoke test. Recovery boot/decryption, factory
reset, phone calls, Bluetooth/USB audio, every camera mode, long-term stability
and subjective sound quality were not rerun. Earlier targeted acceptance keeps
its recorded scope; no exhaustive or bug-free certification is implied.
