# XiaomiParts and Device UX Durable Knowledge

## Latest Thermal Profiles dialog fix — September 24

Common-tree `3c30e7d` clips the shared profile list between the actual title and button panels and adds padding only for their measured overlap. It supersedes the insufficient fixed-inset removal in `db27251`, which let rows draw under the title and Cancel. Source checks passed. The maintainer subsequently confirmed the fix works as intended, with a screenshot showing the System Profile list contained between the title and Cancel panels. This is user validation; a separate per-app screenshot/test was not supplied. Preserve existing touch-profile behavior.

See [the detailed checkpoint](../today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## Functional areas

XiaomiParts work has covered:

- thermal profiles;
- per-app profile assignment;
- gaming touch controls;
- display/refresh controls;
- Smooth Display integration;
- charging control;
- GPU/KGSL information;
- ZRAM/task-profile/power-related controls;
- Clear Speaker and device utilities.

## Thermal profiles

Legacy thermal profile behavior should be preserved while presenting clearer user-facing names.

Avoid profile names that expose internal shorthand without explaining behavior.

Per-app thermal/profile settings must survive lifecycle transitions and should not silently reset.

## Touch settings

Guard unsupported touch nodes/settings rather than assuming every stock control exists on the AOSP target.

UI must degrade safely when a device node is unavailable.

## Android 17 UI direction

Recent redesign work favors Android 17 / Material 3 expressive components:

- reduced unnecessary card padding;
- tonal selector pills/dialogs;
- consistent SettingsLib-style sliders;
- externally positioned value labels where useful;
- clean list scrolling without visual clipping artifacts.

## Main-screen density

Large sections such as system profiles should be collapsible/expandable instead of permanently consuming most of the screen.

App lists benefit from:

- top-right search;
- nearby information/help affordance;
- stable item sizing while scrolling.

## Smooth Display

Alioth overlays wire Smooth Display into Settings.

Keep overlay ownership device-appropriate and avoid duplicating the same setting in multiple layers.

## General UX rule

Do not trade functionality for visual redesign. Preserve working legacy behavior first, then modernize presentation.

## Per-app touch and MiSound guardrails

Preserve Benchmark/Gaming touch controls end to end: enable/disable, response, sensitivity and edge resistance. Historical package routing uses `appName`/`packageName` and `gameMode,response,sensitivity,resistant`; confirm current source before editing. Avoid accidental global persistence and duplicate activity-owned system-bar padding.

MiSound headphone profiles do not establish speaker-mode support. Reference speaker switches guarded for `thyme` must not be assumed valid for Alioth merely because `isSupportSpeaker` or a product property exists.

See [reconciled rework evidence](../today/2026-09-24-rework-memory-reconciliation.md) for failure signatures, historical validation and superseded status.
