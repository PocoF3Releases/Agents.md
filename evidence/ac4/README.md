# Recorded AC-4 diagnostic

[Ac4Test.java](Ac4Test.java) and [decode-result.txt](decode-result.txt) are unchanged source/output from the accepted test, not a new execution. The Java diagnostic takes an input MP4 path and an output PCM path, selects OMX.dolby.ac4.decoder and checks completion/nonzero PCM; it does not play sound.

[V-AC4](../../memory/validation.md#v-ac4) owns the observed result, separate listening confirmation and limits. The [original record](../../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md) identifies the official sample and historical collection steps. Running diagnostics needs actual authorized device access; a repository read does not provide it.
