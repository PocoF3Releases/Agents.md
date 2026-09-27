# Release, Changelog and Visual Asset Conventions

## Release naming

Typical release header:

```text
POCO F3 (alioth) — Evolution X
Android 17 | Evolution X v12.2
```

Android 16 maintenance releases have used Evolution X v11.x naming.

## Changelog style

Prefer concise grouped release notes rather than raw commit dumps.

Useful sections:

- Device
- XiaomiParts
- Dolby
- MiuiCamera
- Frameworks/av
- Kernel/Input when relevant
- ROM-side
- Highlights
- Download / mirror
- Installation
- Support

Keep Telegram mirror changelogs shorter than the full release post.

## Changelog generation workflow

Use `memory/android16-android17-release-state.md` as the release cutoff ledger. A new changelog must describe the **delta since the previous shipped build**, not every recent-looking commit.

### 1. Establish the previous shipped baseline

Before collecting changes, identify:

- Android version and Evolution X version;
- previous build date;
- the last release's recorded feature baseline;
- exact included branch heads when recorded.

Do not infer the release boundary from commit timestamps alone. This project rewrites/rebases history, so an old feature may later appear under a newer commit date or SHA.

If history was rewritten after a release, the recorded **feature baseline** is authoritative for deciding whether a change was already shipped. Do not list the same user-visible change twice just because its commit was rebased, squashed, renamed, or recreated.

### 2. Resolve current source heads

For normal device-side release work, start from the repositories/branches routed by `INDEX.yaml` and the expected heads in `memory/repositories/TRACKED_HEADS.yaml`, then query the live branch heads.

Typical Android 17 device-side scope includes:

```text
device_xiaomi_alioth:aosp-17
device_xiaomi_sm8250-common:aosp-17
device_xiaomi_camera:aosp-17
decompiled_miui_camera:aosp-17
hardware_xiaomi:cnb
frameworks_base:cnb
frameworks_av:cnb
kernel_xiaomi_sm8250:aosp-16
hardware_qcom-caf_sm8250_audio:cnb
hardware_qcom-caf_sm8250_display:cnb
hardware_qcom-caf_sm8250_media:cnb
android_hardware_nxp_nfc:lineage-24.0
vendor_xiaomi_alioth:aosp-17
vendor_xiaomi_sm8250-common:aosp-17
```

Only add other repositories when the release actually includes a relevant device-side change.

### 3. Build a semantic delta, not a commit dump

Group related commits into one user-facing item.

Examples:

- several XiaomiParts thermal/profile/UI commits -> one XiaomiParts overhaul section;
- several Dolby transport/routing/UI commits -> one Dolby section;
- JNI packaging, HIDL cleanup and camera cache work -> concise MiuiCamera compatibility items.

Omit from normal release notes:

- README/banner/documentation-only commits;
- temporary experiments later reverted;
- history-cleanup-only rewrites;
- duplicated changes moved between repositories;
- validation-only commits that do not alter the shipped result.

When a framework or ROM-wide commit is not meaningfully device-specific, keep it out of a **device-side** changelog unless the user explicitly asks for complete ROM-side changes.

### 4. Match wording to evidence

Use evidence-sensitive language:

- **runtime-validated:** `Fixed`, `Restored`, `Improved` are appropriate;
- **built/static/source validated only:** prefer `Added support`, `Added path`, `Prepared`, or describe the implementation without claiming runtime success;
- **pending runtime validation:** state that limitation when the feature is prominent enough that readers could otherwise assume it is confirmed.

Do not turn source presence, string matches, successful compilation, or static analysis into a claim that the feature works on-device.

### 5. Prefer user-visible grouping

Recommended full-post ordering:

```text
📱 device / ROM header
📷 MiuiCamera
🎛️ XiaomiParts
🔊 Dolby / Audio
🖥️ Display / Media
🔋 Kernel / Power
📡 NFC
⚙️ System / Frameworks
⚙️ ROM-side
✨ Highlights
📥 Download
🛠 Images
⚠️ Installation
❤️ Support
```

Skip empty sections. If only a few subsystems changed, keep the post compact.

### 6. Produce two changelog sizes

**Big changelog:** concise grouped detail for the main release post.

**Small changelog:** Telegram/file-mirror version with only the strongest user-visible changes, normally 1-4 bullets per active subsystem.

The small changelog should not simply copy every full-post bullet.

### 7. Select highlights

Use 3-4 short highlights that represent the most visible or important improvements in that build.

Good examples:

```text
Camera Runtime & SAT
XiaomiParts Overhaul
Dolby / Game Audio
NFC Fix
```

Avoid highlighting an unverified feature as fully working. For a pending SAT implementation, for example, prefer `SAT Path` or `Logical SAT Support` until runtime acceptance is complete.

### 8. Record the new release cutoff

After a build is published or explicitly declared as the new build baseline:

1. update `memory/android16-android17-release-state.md`;
2. record the build date/version;
3. record exact included branch heads where useful;
4. record the semantic feature baseline;
5. mark prominent pending-runtime features explicitly.

This prevents the next changelog from re-listing already shipped work.

## Installation guidance

When a clean install is required/recommended, say so directly and identify the previous Android base when relevant.

## Banner dimensions

Primary ROM banners:

- 16:9 landscape;
- high-resolution / 4K-target composition;
- readable device/version text;
- consistent padding and alignment.

## Visual direction

Established banner theme:

- OG Arknights / Terra-inspired industrial cityscape;
- colossal mobile-city / brutalist-industrial architecture;
- charcoal/black/desaturated gray;
- intense crimson emergency lighting / dark-red atmospheric glow;
- rain, fog, ash, reflective streets;
- no generic neon cyberpunk;
- no blue/purple/violet-dominant palette;
- no unreadable signage/logos in the environment.

For Evolution X branding:

- white `Evolution`;
- red `X`;
- device text should follow the same deliberate grid/typographic system.

Avoid gratuitous repeated X motifs.

## PocoF3Releases logo/avatar

GitHub avatar art must remain legible at small size.

Keep POCO F3 context visible but avoid over-detailed elements that collapse when rendered as a small avatar.

## Support section

Use a simple Support label without embedding personal payment/account identifiers into project-memory documentation.


## ROM update banner generation workflow

Use this section when generating a new POCO F3 / Evolution X release banner for a later build. The goal is to make consecutive releases look like the same visual series while updating the content to match the new changelog.

### Source information

Before generating the banner, first build the release changelog using the workflow above and `memory/android16-android17-release-state.md`.

The banner is a **visual summary of the already-decided release delta**. Do not independently invent features from commit names while drawing the banner.

Required release inputs:

```text
Device: POCO F3 (alioth)
Android version
Evolution X version
Build date
3-4 release highlights
3-6 compact subsystem groups
installation guidance
support label
```

If an implementation is included but runtime validation is still pending, use neutral wording such as:

```text
Logical SAT Support
VideoSAT Path
SAT Camera Integration
```

Do not put `VideoSAT Fixed`, `Seamless Zoom Fixed`, or similar completed-sounding text on the banner until runtime validation supports it.

### Prefer continuity with the previous banner

For an update release, use the most recent successful banner as the composition/style reference when it is available.

Preserve the visual family:

- same 16:9 landscape format;
- same overall left-phone / right-information composition;
- same Evolution X identity;
- same black / white / crimson palette;
- same angular red-framed information panels;
- same hierarchy between header, build date, changelog and highlights;
- same restrained footer/support language.

Do **not** treat every update as a completely unrelated poster unless the user explicitly requests a redesign.

When editing an existing banner, update:

1. build date;
2. Android / Evolution X version if changed;
3. changelog section names;
4. compact bullet content;
5. highlight chips;
6. installation wording when the migration base changed.

Keep device identity and the general release-series layout stable.

### Canonical layout

A proven layout for the POCO F3 update banners is:

```text
┌────────────────────────────────────────────────────────────────────┐
│ small "BEYOND STOCK." mark                                         │
│                                                                    │
│  POCO F3 phone render(s)     POCO F3 (alioth) —                    │
│  front + back               [large Evolution X logo]               │
│                              Android 17 | Evolution X v12.2         │
│                              [ Build: DD.MM.YYYY ]                  │
│                                                                    │
│                              ┌──────────────┬──────────────┐        │
│                              │ subsystem A  │ subsystem B  │        │
│                              │ short bullets│ short bullets│        │
│                              ├──────────────┼──────────────┤        │
│                              │ subsystem C  │ subsystem D  │        │
│                              └──────────────┴──────────────┘        │
│                                                                    │
│                              [ highlight ][ highlight ][ highlight ]│
│                                                                    │
│                              [ Support ] [ Installation ]           │
│                                                                    │
│                  THE EVOLUTION OF ANDROID.                          │
└────────────────────────────────────────────────────────────────────┘
```

Another acceptable dense-release variant uses three primary feature cards across the center and a narrow lower row for Kernel / Audio / System / ROM-side. Use it when there are too many meaningful subsystems for the standard two-column layout.

### Information density

Do not paste the full release changelog into the image.

Banner copy should be shorter than even the Telegram changelog.

Good banner bullet lengths:

```text
Fixed capability caching
Added ExtraPhoto support
Improved thermal profiles
Reworked Dolby routing
Fixed NFC teardown
```

Avoid long implementation prose, exact SELinux types, file paths, hashes, or commit subjects.

A useful target is:

- 2-4 bullets for a major section;
- 1-2 bullets for a minor section;
- 3 highlight chips;
- no more than about 20 changelog lines total unless using the dense variant.

### Section selection

Choose sections based on the release, not a fixed list.

Examples:

```text
MiuiCamera
XiaomiParts
Dolby
Audio
Display
Power
Kernel
NFC
Input
System
ROM-side
```

For the 22.09.2026 Android 17 style of release, a suitable banner grouping is:

```text
MiuiCamera
XiaomiParts
Dolby / Audio
Kernel / Power
Display / Media
NFC
ROM-side
```

The banner should favor user-visible improvements over internal maintenance.

### Highlight chips

Use three compact highlight chips near the lower center.

Examples from the established style:

```text
Native 48MP
Macro Restored
Front Video Fixed

Smooth Display
Dolby Fix
Bluetooth Fix

Screen Recording
Brightness Fix
Dolby Routing

Camera Runtime & SAT
XiaomiParts Overhaul
Dolby / Game Audio
```

Highlights must reflect the current release only. Do not retain a highlight from the previous banner after that feature is no longer new.

### Phone presentation

Use a realistic POCO F3 render on the left.

Preferred composition:

- one rear view and one front view, slightly overlapped;
- realistic black/graphite materials;
- correct POCO F3 camera-module proportions;
- no invented extra camera modules;
- no foldable/curved-screen reinterpretation;
- no duplicate or malformed buttons;
- front display should visually match the city/background theme.

The front screen can show the same cityscape from a slightly different perspective so it feels integrated with the poster.

Do not let the phone consume so much width that the changelog becomes unreadable.

### Evolution X branding

The established brand treatment is:

- `Evolution` in white;
- the final `X` in vivid red;
- large, clean and centered within the information side;
- `POCO F3 (alioth) —` above it;
- Android/version line directly below it;
- build date in a small red-outlined badge beneath.

Keep the Evolution X wordmark readable. Avoid distorted letters, accidental duplicated characters, malformed X shapes or generated pseudo-text.

### Background: functional Terra-inspired city

The background should be inspired by the large-scale industrial urbanism of Arknights / Terra, but it must look like a city **people could actually live and work in**.

Prefer:

- occupied high-rise residential/commercial towers;
- coherent floor spacing and window grids;
- visible service floors;
- realistic structural cores;
- elevated roadways with plausible supports;
- rail/transit lines and stations;
- pedestrian skybridges;
- maintenance platforms with access routes;
- ground-level streets and loading areas;
- drainage, pipes and utility infrastructure with plausible routing;
- cranes attached to real construction/maintenance areas;
- human-scale doors, railings, balconies and service corridors;
- layered foreground / midground / distant skyline;
- wet asphalt and concrete reflections;
- rain, mist, smoke and Catastrophe-like storm clouds;
- limited red emergency/industrial lighting.

The city can be monumental and oppressive, but individual structures need believable purpose and circulation.

Avoid:

- random towers made only from pipes/scaffolding;
- impossible floating slabs;
- bridges that terminate in empty space;
- buildings with no windows, floors, entrances or access;
- decorative machinery with no plausible function;
- excessive vertical red laser pillars;
- generic neon cyberpunk streets;
- flying cars;
- giant unrelated logos or Evolution X signs embedded in the city;
- unreadable/generated background signage;
- blue, violet or purple-dominant lighting.

Palette:

```text
deep black
charcoal
desaturated steel gray
warm dirty white
crimson / vermilion red accents
```

The red light should feel like emergency, brake, signal, industrial or architectural accent lighting rather than arbitrary neon everywhere.

### Human-scale realism

Even when background people are tiny, architecture should imply a believable human scale.

Useful cues:

- lit windows at regular floor heights;
- railings sized for people;
- train doors/platform edges;
- vehicles on actual roads;
- pedestrian bridges connected to building floors;
- maintenance stairs/ladders;
- streetlights and traffic signals;
- storefront/service entrances only where the perspective supports them.

Do not add crowds merely for detail. The banner's UI/text remains the priority.

### UI panel styling

Use:

- dark nearly-black translucent/solid panels;
- thin crimson outlines;
- chamfered/angular corners;
- restrained red glow;
- white headings;
- red section icons and bullet dots;
- thin dividers;
- compact technical typography;
- consistent internal padding.

Avoid:

- rounded mobile-app cards;
- glassmorphism;
- rainbow gradients;
- generic blue holographic UI;
- excessive red glow that reduces legibility;
- inconsistent panel sizes or margins.

### Typography

Typography should feel like a carefully typeset ROM release card, not generated sci-fi text.

Hierarchy:

1. POCO F3 / Evolution X;
2. Android/version/build date;
3. section headers;
4. bullets;
5. highlights/footer.

Use a bold condensed or geometric sans for headings and a clean sans for small copy.

All visible banner text should be English unless another language is explicitly requested.

No Chinese-like pseudo-glyphs, broken Latin characters, or decorative fake text.

### Footer and support

Established footer treatment:

```text
THE EVOLUTION OF ANDROID.
```

Support panel:

```text
Support
PayPal
```

Do not embed clickable URLs into the image.

The image may contain the word `PayPal`, while the actual clickable support link belongs in the text release post.

Installation wording should be compact, for example:

```text
Clean install from Android 16 recommended
```

### Prompt template for a new update banner

Adapt this template to the actual release:

```text
Create a new high-resolution 16:9 POCO F3 (alioth) Evolution X release
banner, continuing the established PocoF3Releases visual series.

LAYOUT
Left 30-33%: realistic black POCO F3 rear + front renders, overlapped.
Right/top: "POCO F3 (alioth) —", large Evolution X branding with white
"Evolution" and vivid red "X", then "Android <version> | Evolution X
<version>" and a red-outlined "Build: <date>" badge.

Right/center: clean angular black panels with thin crimson borders.
Use these compact release groups:
- <section>: <2-4 short bullets>
- <section>: <2-4 short bullets>
- <section>: <1-3 short bullets>

Lower center: three highlight chips:
<highlight 1> | <highlight 2> | <highlight 3>

Bottom: Support — PayPal; Installation — <short wording>.
Footer: "THE EVOLUTION OF ANDROID."

BACKGROUND
A believable inhabited Terra-inspired industrial megacity at night in rain:
functional occupied towers with coherent floors/windows, service cores,
pedestrian skybridges, elevated roads, grounded rail transit, stations,
maintenance platforms, utility pipes, loading/service streets and realistic
structural supports. Monumental scale but human-usable architecture. Wet
asphalt/concrete reflections, fog, smoke, storm clouds, small crimson
emergency and signal lights.

STYLE
Deep black, charcoal, desaturated gray, white and intense crimson only.
Cinematic anime concept-art realism mixed with premium technical product
advertising. Sharp typography, deliberate grid, consistent margins and
high legibility.

AVOID
Purple/blue/violet dominant color, generic neon cyberpunk, flying cars,
impossible scaffolding, floating structures, meaningless pipes, oversized
city logos, repeated decorative X motifs, unreadable background signage,
malformed phone hardware, fake text, sloppy UI alignment.
```

### Update/edit prompt template

When a previous release banner is attached and should be reworked rather than redesigned:

```text
Use the attached POCO F3 Evolution X banner as the composition and style
reference. Preserve the overall phone placement, typography hierarchy,
Evolution X branding, black/crimson UI language and 16:9 layout.

Update only the release information to:
Android <version> | Evolution X <version>
Build: <date>

Replace the old changelog with:
<section + compact bullets>

Replace the highlight row with:
<highlight 1> | <highlight 2> | <highlight 3>

Also improve the city background so every major building looks functional
and inhabitable: coherent floor levels, windows, access, roads, rail,
pedestrian connections and realistic structural supports. Keep the
Terra-inspired black/charcoal/crimson rainy atmosphere. Do not turn it into
generic neon cyberpunk.

Remove obsolete release text rather than stacking new text over it.
Preserve clean margins and make all final visible text readable English.
```

### Generation / review loop

For each new banner:

1. finalize the changelog first;
2. reduce it to banner-sized copy;
3. select 3 highlights;
4. generate or edit using the latest successful banner as visual reference;
5. inspect the result at full size;
6. verify exact build date/version;
7. verify every section is from the current release delta;
8. verify text spelling and alignment;
9. inspect the POCO F3 hardware shape/camera module;
10. inspect buildings/roads/bridges for functional geometry;
11. regenerate/rework if text artifacts or impossible architecture remain.

Do not accept an image simply because the general atmosphere is attractive. Release-data accuracy and readable typography are part of the acceptance criteria.

### Common failure modes to reject

Reject/rework banners with:

- wrong build date;
- previous-release bullets left behind;
- `Native 12MP` when the intended historical highlight was `Native 48MP`;
- claiming a pending feature is fixed;
- text too close to the left/right canvas edge;
- red `Releases`/Evolution X mark visibly off-center;
- excessive background detail competing with the changelog;
- random unreadable signs;
- city towers that are only abstract machinery with no usable floors;
- phone screen/background mismatch;
- duplicated phone backs or malformed camera arrays;
- excessive repeated X graphics;
- too many changelog panels for the available space.

### Android 16 adaptation

For an Android 16 maintenance banner, keep the same visual identity unless the user requests a different series.

Change:

- header to Android 16;
- Evolution X version to the current v11.x release;
- build date;
- release-delta content;
- installation base wording where appropriate.

Do not copy Android 17-only features into an Android 16 banner unless the corresponding change was actually backported and included in that build.
