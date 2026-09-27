# NFC Durable Knowledge

## Active implementation

Alioth uses the source-built NXP NFC stack from:

```text
PocoF3Releases/android_hardware_nxp_nfc
```

The relevant Alioth implementation is the SNxxx HAL path:

```text
snxxx/halimpl/hal/phNxpNciHal.cc
```

## September 2026 teardown regression

A LineageOS NXP NFC security change introduced on 2026-09-19:

```text
ad16c5c95a8613cc7ef8890c243068633e8d2f83
Fix Use-After-Free in NXP NFC HAL timer teardown
```

correctly clears the global NFC message-queue client ID before timer cleanup so delayed timer callbacks cannot access a freed queue.

The teardown sequence effectively became:

```text
save nClientId
global nClientId = 0
timer cleanup
HAL shutdown
join client thread
release saved queue
```

The security intent is valid and must not be reverted.

## Verified failure mode

The existing SNxxx client thread still read the global queue ID on every receive:

```cpp
phDal4Nfc_msgrcv(p_nxpncihal_ctrl->gDrvCfg.nClientId, ...)
```

After teardown set the global ID to zero, `phDal4Nfc_msgrcv(0, ...)` returned `-1`. The thread handled that with:

```text
NFC client received bad message
continue
```

which created a tight log/CPU loop.

Runtime logcat from the affected build contained approximately 183,784 matches in the captured boot log and overwhelmed unrelated camera debugging.

## Active fix

Current PocoF3Releases fix:

```text
8be75516d6d3cfff3a95ca2f249f0b36ceededb9
nfc: nxp: Keep client queue valid during teardown
```

The SNxxx client thread now snapshots the queue ID before entering its receive loop:

```cpp
const intptr_t client_id = p_nxpncihal_ctrl->gDrvCfg.nClientId;
```

and receives from that stable local handle:

```cpp
phDal4Nfc_msgrcv(client_id, ...)
```

This preserves both required properties:

1. the global `nClientId` can still become zero before timer cleanup, preserving the UAF mitigation;
2. the already-running client thread can still receive the close-complete message and terminate normally before the saved queue is released.

Do not fix this by reverting the security commit or by leaving the global queue ID valid during timer cleanup.

## Scope

The Alioth fix intentionally modifies only:

```text
snxxx/halimpl/hal/phNxpNciHal.cc
```

Do not widen it to PN8x or SNxxx v2 without a target that actually uses those implementations or equivalent runtime evidence.

## Validation state

A rebuild containing `8be75516...` completed on 2026-09-22.

Runtime validation on the rebuilt image succeeded on 2026-09-22. The previous tight `NFC client received bad message` loop is absent from both the fresh boot log and fresh camera log.

The primary regression check remains:

```bash
adb logcat -d | grep -F "NFC client received bad message"
```

Expected and observed result after normal NFC shutdown/restart: no tight repeated error loop. The Alioth SNxxx fix is runtime-validated.
