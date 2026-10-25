# Alioth subsystem inventory — October 25, 2026

**Source/build-artifact checked; scoped device observation.** No source edits,
sync, ROM build or flashing were performed for the inventory.

The portable [105-entry CSV](subsystems-20261025.csv) contains grouped components,
implementation names, source paths and qualifications. Its technical owner is
[the subsystem map](../memory/alioth-subsystems.md).

## Coverage and verification

Eight relevant repositories were clean, with heads rechecked at completion:
device Alioth/common, vendor Alioth/common, kernel, hardware/xiaomi and camera
device/vendor inputs. Exact maintained revisions remain in the
[source ledger](../state/repositories.yaml); local detached recovery overlays are
not silently treated as public device heads.

| Captured input | Count and meaning |
| --- | --- |
| Direct device-tree package requests | 150 distinct names, with conditional Make context |
| Proprietary input entries | 1,196 across both device trees and phone input list; each matched its file/line |
| Kernel settings | 752 defconfig and 1,952 resolved build-config scalar assignments; each matched its file/line |
| Installed-file manifests | 11,796 rows across 11 existing partition/ramdisk/recovery manifests; every count reconciled; not a unique-file count |
| Device properties | 298 entries from prop files; selection/override order still applies |
| Overlay values | 143 named resource values; source presence does not establish selection |
| Audio declarations | 130 policy/effect/library/route declarations |
| Alioth overlay include closure | 73 files; separate base SoC DTB is not included by pretending the overlay is the entire live tree |
| Sensor descriptors | 70 registered descriptors, including wakeup/virtual variants |

Source/built HAL and init-service declarations were also enumerated, retaining
interfaces, versions, overrides and origins. Some are optional or duplicated
across inputs. Empty VINTF overrides are not active service instances.

Read-only runtime checks captured features, sensor descriptors and I2C/SPI driver
bindings. `lshal` returned warnings/nonzero status for services it could not
fetch. No all-HAL success claim follows from that output. No application data,
credentials or raw process/service dumps are included here.

## Important distinctions

Audio/effects use HIDL 6.0 and the camera provider uses HIDL 2.4, alongside newer
AIDL power/health/USB/Wi-Fi/fingerprint services. A newer OS does not imply every
legacy HAL was upgraded. SKU NFC, side fingerprint, unbound charger clients,
virtual sensors and charging-bypass limits are retained in the topic owner.

The private snapshot, CSV/JSON appendices, report and hash-verified ZIP remain in
`~/evo/.repo/alioth-subsystem-inventory-20261025/`. That path is provenance, not a
public download. The inventory is not exhaustive functional acceptance, hardware
teardown, DRM certification or a guarantee for every regional/supplier variant.
