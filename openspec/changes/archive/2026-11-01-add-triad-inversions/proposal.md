## Why

The chord table names the triads of each mode, but not where to play them. Learning triad inversions on groups of three neighbouring strings is the standard way to find a chord anywhere on the neck. Showing those shapes for a selected chord, coloured by inversion and connected by lines, turns the table into a map of playable chords.

## What Changes

- Chord cells in the chord table become clickable (both the C major column and the mode column). Clicking selects that chord, and clicking it again deselects it. The selected cell is framed.
- When a chord is selected:
  - the scale on the fretboard (dots and arrows) is faded but stays visible;
  - every playable triad shape of the chord is drawn on the selected string set: three notes on three neighbouring strings, all within one octave, at most 5 frets wide (open strings don't count towards the width);
  - each shape is coloured by inversion (root position, 1st, 2nd), with a line through its three notes;
  - the shape's dots are labelled with chord tones (`R`, `3`/`b3`, `5`/`b5`).
- A string-set selector offers 6-5-4, 5-4-3, 4-3-2, 3-2-1 (default) and "all". In "all", a note shared by shapes of different inversions gets a neutral outline.
- A legend explains the three inversion colours while a chord is selected.
- The selection keeps its degree and column when the mode changes. It is cleared when its column disappears (C major alone).

## Capabilities

### New Capabilities

- `triad-inversions`: finding playable triad shapes for a chord, the string-set selection and drawing the shapes on the fretboard.

### Modified Capabilities

- `chord-table`: chord cells become selectable (new requirement). Existing requirements are unchanged.

## Impact

- `fretboard/theory.py`: voicing search and chord-tone labels.
- `fretboard/render.py`: fading the scale, drawing the shapes and lines, inversion legend, clickable chord cells with a selected state.
- `fretboard/app.py`: selection state, the string-set selector, and click events from the table (`emitEvent`/`ui.on`).
- New tests and a README update. The shape search works with the number of frets shown, so the separate change `extend-neck-to-15-frets` will add shapes without touching this logic.
