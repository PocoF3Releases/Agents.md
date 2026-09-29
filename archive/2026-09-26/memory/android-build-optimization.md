# Android Build Optimization and Host Context

## Host context

An unrestricted `-j$(nproc)` MiuiCamera/ROM build previously coincided with an Ubuntu crash. For isolated validation, conservative concurrency such as `-j4` is a safer first step before increasing parallelism.

## Dexpreopt direction

For Android 17 production ROM builds, the preferred global compiler filter is:

```make
PRODUCT_DEX_PREOPT_DEFAULT_COMPILER_FILTER := speed
```

Avoid globally forcing:

```make
PRODUCT_DEX_PREOPT_DEFAULT_COMPILER_FILTER := everything
```

Rationale:

- `speed` already provides full-AOT optimization for normal production use;
- `everything` additionally compiles code that normally does not need full AOT treatment;
- it increases host build work, output size and cache pressure;
- it does not automatically improve real-world app performance.

Use more aggressive filters only for narrowly justified modules.

## Android 17 cleanup already performed

An obsolete:

```make
DEX_PREOPT_DEFAULT := generate-vdex-and-image
```

style override was removed during Android 17 build-flag cleanup.

Keep platform-default dexpreopt/profile behavior unless a measured device problem requires a targeted override.

## Optimization priority

The target device is not a current high-end platform, so host-side compilation is preferred where it produces real startup/runtime benefits without excessive ROM size growth.

Prioritize:

1. correct dexpreopt;
2. profile-guided optimization;
3. ART defaults appropriate to RAM tier;
4. avoiding unnecessary device-side compilation;
5. measured changes rather than cargo-cult flags.

## RAM-tier / ART context

The project has used different ART defaults for 6 GB and 8 GB device variants where appropriate.

Treat device RAM tier separately from the host build machine's RAM.

## Build verification

For a focused module:

```bash
m MiuiCamera -j4
```

For full ROM work, increase parallelism only after confirming system stability.
