## Why

The goal is to learn the C major scale on the guitar fretboard, then learn the other modes as small alterations of it (Dorian = major with b3 and b7, and so on), not as unrelated shapes. A visualiser that keeps C major as a fixed reference and shows exactly which notes move, and by how much, makes those relationships easy to see.

## What Changes

- New NiceGUI web app showing a 6-string guitar fretboard in standard tuning, frets 0-12.
- C major is always the reference scale. The user picks one comparison option:
  - **C major alone**: only the reference scale, for learning the base shape.
  - **One of the other six C modes**, ordered brightest to darkest: Lydian, Mixolydian, Dorian, Aeolian (natural minor), Phrygian, Locrian.
- Each mode is defined as a set of alterations of the major degrees (for example, Dorian = b3 b7).
- Every note position is drawn in one of three states:
  - **shared**: in both scales; drawn solid.
  - **dropped**: a C major note that the mode alters; drawn as a ghost dot.
  - **altered**: the mode's replacement note; highlighted, one fret away from its ghost.
- The root (C) is emphasised.
- Labels can be switched between scale degrees (default, e.g. `b3`) and note names (e.g. `Eb`), spelled correctly from the degree.
- A legend explains the visual states.

Out of scope for this change: roots other than C, other tunings or string counts, scales beyond the seven modes, audio, clicking on notes, left-handed view.

## Capabilities

### New Capabilities

- `fretboard-display`: rendering a guitar fretboard (standard tuning, 6 strings, frets 0-12) with note dots, fret markers, and switchable degree/note-name labels.
- `mode-comparison`: comparing the C major reference with a selected C mode (or showing C major alone), and classifying each note as shared, dropped or altered.

### Modified Capabilities

None. There are no existing specs.

## Impact

- New Python project: a pure theory module, an SVG rendering module and a NiceGUI UI module, plus unit tests.
- New dependencies: `nicegui`, with `pytest` for development.
- No existing code is affected because this is the first change.
