📱 POCO F3 / Redmi K40 / Mi 11X — Evolution X
Android 17 • Initial build

📷 MIUI Camera
• Native 48 MP capture, ultrawide, macro and front-camera video support.
• Main-camera 4K recording at 30/60 FPS, with fixes for corrupted video and recording-session handling.
• Logical rear-camera switching and corrected camera capability caching.
• Safer recording-mode changes: unsupported ultrawide 4K is blocked and the camera returns to 1x when required.
• Integrated ExtraPhoto companion for document, ID-card and refocus editing, with updated camera permissions and native compatibility.

🎛 XiaomiParts & display
• Redesigned device settings with clearer controls, improved dialogs and expanded translations.
• System/per-app thermal profiles and safer regional thermal-map switching, retaining stock thermal limits.
• Gaming touch controls for response, sensitivity, edge resistance, aim sensitivity, tap stability and expert presets.
• Per-app refresh-rate controls that preserve changes made to Smooth Display.
• Refined MiSound headphone settings and Clear Speaker playback handling.
• Updated brightness transitions, high-brightness and DC-dimming control handling.

🔊 Dolby & audio
• Dolby Atmos settings with custom profiles, a 20-band equalizer, profile reset, Quick Settings and stock speaker-tuning controls.
• Communication-aware processing controls and recovery of saved audio/volume state after service restarts.
• Dolby AC-4 stereo playback compatibility.
• Corrected speaker/headphone routing and audio battery-service integration.
• Restored complete capture-buffer reads for the legacy audio HAL and added safeguards against stalled reads when capture stops.

📳 Haptics
• Stock-backed vibration effects with corrected strength, texture feedback and cancellation handling.
• Stock click, thud and light-tick compositions, plus a light-tick fallback for LOW_TICK system feedback.
• Keyboard feedback follows the selected touch-vibration intensity.

🎥 Screen recording & media
• Maximum-FPS recording option that follows display refresh rate within codec limits.
• Independent recording-blur control, with effects restored after recording ends.
• Updated video-buffer, color-conversion and display compatibility for the existing camera/media stack.

🖥 Everyday controls
• Independent double-tap-to-wake and double-tap ambient-display gestures.
• Corrected AOD brightness handling when automatic brightness is enabled.
• Quick Settings data-usage queries run in the background to avoid blocking the interface.
• Clipboard auto-clear controls with a configurable timeout.

📡 Connectivity & reliability
• Modem configuration setup handles missing optional firmware metadata and preserves cache access across boots.
• Corrected the observed call-proximity timeout path.
• Safer NFC shutdown and USB controller initialization.
• Improved composite Bluetooth controller handling.
• Sensor and fingerprint safeguards for invalid results, service lifetime and authentication lockout.

🔋 Kernel, battery & system
• Linux 4.19.325-based kernel with device-specific display, audio, touch and haptic integration.
• Updated battery reporting/replacement-battery handling and safeguards for failed fuel-gauge readings.
• Consistent charging-control ownership and USB fast-charge error handling.
• Kernel WireGuard support.
• RAM-aware app-runtime defaults, updated compressed-memory setup and power-hint priorities that retain restrictive frequency caps.
• Removed obsolete startup services and reduced unnecessary diagnostic logging.

ℹ️ Scope
Ultrawide video is validated at 1080p30; true ultrawide 60 FPS is not confirmed. Full RichTap is not included. These notes describe final source implementations; complete acceptance of every feature in the matching release build remains pending.
