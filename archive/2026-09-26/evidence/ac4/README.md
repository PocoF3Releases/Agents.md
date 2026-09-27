# AC-4 diagnostic evidence

`Ac4Test.java` is the actual previously used shell diagnostic, copied unchanged apart from a final newline. `decode-result.txt` is the decisive excerpt from the successful capture, not a fresh run. It explicitly selects the OMX decoder, writes PCM and checks EOS/nonzero output. It does not play sound; audible playback was separately confirmed by the maintainer using the original sample video.

The helper was compiled against Android API 36 and dexed with minimum API 29. It accepts two arguments: device input MP4 path and writable output PCM path. Once compiled/dexed and placed on an authorized device, the execution form is:

```sh
adb shell 'CLASSPATH=/data/local/tmp/classes.dex app_process /system/bin Ac4Test /data/local/tmp/sample.mp4 /data/local/tmp/ac4.pcm'
```

This is a reproduction command, not an instruction to assume a device is connected or rebuild the ROM. Supply the official sample and compiled dex first; no compiled helper or video is bundled here. The source has a 60-second decode deadline, expects both arguments and is a diagnostic rather than a production app/test suite.

See [the complete checkpoint](../../today/2026-09-24-ac4-validation-and-thermal-dialog.md) for source commits, sample URL, failure progression and validation limits. Full device logcat was deliberately not copied into the repository.
