📱 **POCO F3 / Redmi K40 / Mi 11X — Evolution X**\
\
**Android 17 • Unofficial**\
**Changes since 25.10.2026**\
\
🔥 **Redline kernel**\
• Renamed the kernel to Redline, with a shorter commit ID and the CIP revision shown in kernel information.\
• Corrected CPU feature and cache handling across the big and little cores.\
\
🖥 **Graphics & display**\
• Tightened GPU buffer-import checks and corrected memory accounting.\
• Improved cleanup and retry handling after GPU clock, power or firmware initialization failures.\
• Fixed display power-reference and fence-descriptor cleanup on failed operations.\
\
🔊 **Audio & voice processing**\
• Hardened DSP reply validation and fixed audio-driver lock and buffer cleanup errors.\
• Corrected sample-width handling in voice and echo-reference paths.\
\
📷 **Camera & video**\
• Safer camera firmware-buffer access, interrupt registration and failure cleanup, preserving existing camera modes.\
• Fixed end-of-stream and stop-request cleanup when hardware video submission fails.\
\
🔌 **USB & networking**\
• Hardened MTP event and transfer-length validation, including 32-bit error handling.\
• Corrected unsafe IPv6 packet reads in the Wi-Fi driver.\
• Fixed a networking resource leak when TCP configuration changes are rejected.\
\
🛡 **Memory & encryption**\
• Fixed lifetime races in swap-cache lookups and memory-status reporting.\
• Fixed hardware random-number requests failing on short or partial reads.\
• Improved hardware crypto-engine cleanup and low-memory handling in kernel control-flow protection.\
\
🔋 **Shutdown reliability**\
• Corrected a permission issue preventing secure-storage unmounting during shutdown.\
• Fixed a performance-counter timer lock cycle in CPU hotplug and shutdown paths.\
\
\#EvolutionX #POCOF3 #Alioth #Android17 #Redline
