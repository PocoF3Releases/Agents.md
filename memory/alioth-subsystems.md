# Alioth and SM8250 subsystem map

**2026-10-25 — source/build-artifact checked; scoped read-only device observations.**
The [105-entry inventory](../evidence/subsystems-20261025.csv) maps systems to
current checkout paths. [Evidence and limits](../evidence/subsystem-inventory-20261025.md)
separate configured, shipped, registered and physically bound components.
Repository identities belong in the [source ledger](../state/repositories.yaml).
This is discovery guidance, not permission to build, flash or alter a device.

| Area | Main components |
| --- | --- |
| Platform | Kona/SM8250, arm64 plus arm32, Alioth/aliothin variants, vendor kernel, libinit and DTB/DTBO |
| Kernel | WALT/core_ctl/schedtune, cpufreq/cpuidle, cgroups/PSI, zram/zsmalloc, LZ4/Zstd, ION/DMA-BUF/SMMU, Binder, buses/clocks/regulators and SSR |
| Storage and boot | UFS/ICE, F2FS userdata, ext4 partitions, fscrypt/wrapped keys/metadata encryption, AVB, dynamic super, virtual A/B, OTA and native recovery |
| Graphics/display | Stock A650 KGSL/GMU/EGL/GLES/Vulkan; SDE/DSI/DSC, 60/120 Hz, composer, allocator/mapper, HDR/color processing, HBM/DC/AOD and refresh scheduling |
| Audio | HIDL 6.0, ALSA/tinycompress/ACDB/QDSP, CS35L41 amps, playback/capture/VoIP, sound trigger, MiSound, Dolby DAP/game/VQE, USB/Bluetooth audio and speaker cleaning |
| Camera/media | Camera provider 2.4, CamX/CHI/ISP, module tuning/firmware, MIUI Camera/ExtraPhoto, C2/OMX/Venus/JPEG, AC-4, VPP and DRM |
| DSP/AI | ADSP/CDSP/SLPI, FastRPC, Hexagon, NNAPI/SNPE-related/HTA and vision libraries |
| Cellular | QMI/RIL, dual-slot radio, IMS/RTP, UIM, CNE/DPM, IWLAN, RMNET/IPA/IPACM and carrier provisioning |
| Connectivity | QCA6390/CNSS/CLD3, supplicant/hostapd, P2P/hotspot/Aware/RTT/LOWI, Bluetooth, GNSS, Miracast, USB Type-C/PD/OTG/gadgets, NFC/eSE and IR |
| Input/sensors | FocalTech touch/game tuning, GPIO/HID/uinput, side fingerprint, AW8697, SSC sensor registry/calibration and physical/virtual sensor streams |
| Power | PMIC/SMB5, BQ2597x, FG Gen4/battery authentication, Health/charging control, libperfmgr/DCVS, mi_thermald and kernel protection |
| Security | Gatekeeper, Keymaster, QSEE/QTEE, Widevine/ClearKey/CAS, Soter/IFAA/Mlipay/TUI, SELinux/seccomp/VINTF and property/file labels |
| Vendor support | RTC/time/alarm, configuration stores/QCC, firmware/persist/NV helpers, peripheral managers and diagnostic bridges |
| Device UX | XiaomiParts/Dolby, Compose screens, thermal/touch/display/sound controls, tiles, translations and resource overlays |
| Inherited Android | Bionic/ART/Zygote/APEX, init and service managers, framework/media/network/storage services and product applications |

## Avoid false hardware claims

- The product is a phone with virtual A/B and a **side** fingerprint sensor.
  Common tablet, non-A/B and UDFPS branches are not active Alioth selections.
- Global/China variants enable NFC; Mi 11X/aliothin disables it through variant
  initialization. Do not promise NFC from a shared manifest alone.
- Bound devices observed: FocalTech SPI touch, two CS35L41 amplifiers, AW8697,
  NXP NCI, BQ2597x, FSA4480 and SPI IR. This is one phone, not all supplier variants.
- P9415/LN8282/RX1619 client nodes existed without driver bindings. Their DTS/sysfs
  names do not establish working wireless charging.
- Registered sensors include LSM6DSO, AK0991x, TCS3701, BU27030 and SX932x families,
  plus Xiaomi proximity. The 70 descriptors include wakeup/virtual/algorithm
  variants; they are not 70 physical chips. FOD/knuckle descriptors do not prove
  UDFPS or a corresponding user feature.
- Generic wired/HDMI audio ports, FM blobs and LPA interfaces do not establish a
  physical 3.5 mm jack, HDMI output, FM receiver or eSIM. Declared codecs/NN/DRM
  backends do not establish certification or successful execution.
- Charging control selects `input_suspend`; true battery/charger bypass is
  explicitly disabled. A `thermal-nolimits.conf` file is not a protection bypass
  authorization. Keep thermal protection enabled.
- No Android Thermal HAL is shipped by design: stock Kona HAL has no SKIN entry,
  so headroom/status reporting was absent on stock too; mi_thermald remains the
  authority. [Decision and stock RE](../evidence/thermal-hal-decision-20261031.md).

## Evidence boundaries

Device-tree package requests preserve conditions. Build manifests include
inherited applications and partition/recovery variants; their file rows are not
all unique files or running processes. The observed local trees include native
recovery overlays that must remain distinct from their public device baselines.
`lshal` reported unavailable legacy/framework entries and a nonzero result;
registration must not be relabelled as a passing functional test.

Raw complete appendices remain local under
`~/evo/.repo/alioth-subsystem-inventory-20261025/`. They were not uploaded as
public logs. The portable CSV and evidence record are available in this repo.
