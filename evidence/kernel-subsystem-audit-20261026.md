# Configured-kernel audit — October 26, 2026

Scope: Alioth's existing resolved ARM64 configuration, checkout Clang 21,
W=1 plus C=2 sparse, -j6. No configuration, warning flags, thermal limits,
firmware, system-side sources or production test modules were changed.
All selections are built-in; this resolved config has no =m selections.
A diagnostic scan is not functional certification of every compiled supplier
branch. Bound hardware scope is owned by the subsystem inventory.

## Discovery and remaining work

The configured Image diagnostic scan used keep-going after its first blocker.
It **failed** with declaration, format, unused-variable, sparse/address-space,
kernel-doc and include-path diagnostics across core and vendor code. Repeated
header/include errors are not independent runtime bugs. Logs remain private at
`~/evo/.repo/kernel-subsystem-audit-20261026/`; the deduplicated diagnostic map
is discovery input, not a final clean report. Source fixes below are bounded
repairs, not a claim that the full W=1/C=2 tree now passes.

Storage, USB, charging, thermal, GPU, camera/media, networking, input, security,
core kernel and filesystems were traversed where Kbuild could proceed. Failure
in a translation unit limits analysis of that unit. No selected warning was
silenced and no blanket sparse force-casts were added. Remaining diagnostics
need subsystem-specific caller/locking/ABI review, especially legacy user versus
kernel address-space access, RCU comparisons, callback prototypes and vendor
format mismatches. They are not all evidence of broken hardware.

## Separate repairs

- [ACPI: Declare architecture post-init hook without CONFIG_ACPI](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1b4fcaae69685c035018b9396ac84afb09fffc49).
- [seq_file: fix NULL pointer arithmetic warning](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/68b5c164b6dc42734f2063a9f4f245296255bcf7).
- [Input: xiaomi: Validate touch ioctl and debug inputs](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7dbe1011d557c0059eb8678bdc56d69db720cde7).
- [wifi: qcacld-3.0: Correct shared header search paths](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d7dbf5c7babed2e2f7f19144c4bf9caba75d0f4c).
- [soc: qcom: spss: Report failed event result copies](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/52868ae0fd8cf11612a47f1f505d375486d0e80c).

The ACPI repair selects only the two applicable header hunks from Arnd Bergmann's
[upstream consolidation](https://github.com/torvalds/linux/commit/ad1a48301f659a02df5bff0a121d4a5c0411d36b).
The seq_file/kernfs iterator change is Maíra Canal's exact
[upstream patch](https://github.com/torvalds/linux/commit/90b2433edb6d995bd23d6adde753095b4ab26104).
Original authors/dates and existing human sign-offs are retained; the ACPI
selection documents its narrower backport scope. No unrelated architecture
consolidation was imported.

Touch repair: reject incomplete input copies and invalid mode/length bounds,
guard the actual get-all callback, return EFAULT on failed output copies, guard
negative reset indexing and replace int-width sscanf into u8 with kstrtou8.
Valid command layouts and result-in-buffer conventions remain. Two private
exact-handler sanitizer fixtures cover eleven touch and ten SPSS cases; both
old handlers fail their corresponding copy-failure assertion. Fixtures remain
outside production sources. No firmware upgrade test or forced thermal change.

Wi-Fi repair: correct duplicate GPIO include expansion and RX/TX directory typo,
remove four absent header directories. All object/feature selections remain.
The correct directory-target W=1/C=2 retry eliminates the repeated missing-include
errors but **still fails on other vendor source diagnostics**. An initial direct
nested-object attempt lacked its own Makefile and is not acceptance evidence.

SPSS repair: propagate failed output copies without dropping status on an
interrupted wait. Keep copy-before-helper-error ordering, command numbers,
packed structures and event semantics. Correct diagnostic widths and retain
MMIO annotation for the second debug-register read. Alioth's enabled DTS node
and the phone's bound spss_utils driver establish applicability. No link between
this reporting defect and the shutdown hang has been established.

## Validation boundary

The two changed touch objects pass W=1/C=2 with no diagnostics. The SPSS object
passes W=1/C=2; pre-existing header-global/kernel-doc and host Genksyms notices
remain, separate from its repaired format/copy/MMIO diagnostics. The ACPI missing
prototype and iterator NULL-arithmetic diagnostics are gone; unrelated sparse
RCU comparison reports in seq_file remain. Strict patch checking has no errors;
the exact upstream unnamed seq_file prototype retains two style warnings, and
existing CamelCase identifiers/extern style produce checks. These are disclosed,
not renamed out of the ABI or hidden by checker options.

No release-wide bug-free or full-warning-clean claim is established by this audit.

## Final artifact and phone acceptance

Both normal configured-kernel Image builds passed; the final one identifies
b544d9ee5fe2. Final raw Image SHA-256:
`17b3c52cf03381846b3bbd49d8960900086e8bfb9f1c11b85133d0d910492a21`.
The test image round-trip preserved the installed rooted ramdisk hash. No
partition was flashed and no ROM/installclean build was performed.

Device-tested with SELinux enforcing and boot completed: ten native checks pass
for touch open/read, EFAULT on invalid/partial input, rejected negative reset,
rejected upper mode index/oversized long payload, SPSS open/nonmutating event
query, and EFAULT on an unwritable SPSS result mapping. No event signal, wait,
CMAC, firmware or touch-tuning mutation was used. Invalid debug inputs 'invalid',
'-1' and '256' are rejected while its prior value 0 remains unchanged. Proc
meminfo and battery sysfs reads work. Wi-Fi is enabled and reports COMPLETED.
No new WARNING/BUG/call-trace/RCU-stall appeared after the probe marker.

Private handler fixtures establish copy/error-path behavior with mocked kernel
boundaries; native phone checks establish the selected real-device paths.
Neither certifies every possible error, supplier variant or hardware mode.

The temporary kernel restarted through hardware warm reset; retained pstore
identifies candidate b544d9ee5fe2 and successful reset. ADB briefly listed no
phone, then a Windows server restart restored the transport without another
device reboot. The phone returned to installed d2c680, enforcing and
initcall_debug=N; boot partition SHA-256 matches its pre-test backup. Do not
classify this transport episode as a captured kernel hang.

All five commits are pushed on the public kernel aosp-17 branch through
b544d9ee5fe2. Temporary images/probe/unpacked staging were removed from the
phone and Windows temporary folder. Private evidence remains on the host.
The original-kernel observer and narrow SPU unmount live rule are rearmed only
for the current boot, with no persistent module or permissive policy. The
intermittent historical shutdown investigation remains open.

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
