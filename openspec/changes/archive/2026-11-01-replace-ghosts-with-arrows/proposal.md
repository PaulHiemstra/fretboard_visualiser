## Why

With a mode selected, the fretboard currently shows both a ghost dot for every dropped C major note and the altered note right next to it. That doubles the number of circles around each alteration and makes the board look cluttered. A straight arrow along the string, from where the C major note was to its replacement, carries the same information with less ink. The arrow also shows the physical movement: slide back one fret for a flat, forward one fret for a sharp.

## What Changes

- **BREAKING (visual)**: dropped C major notes are no longer drawn as ghost dots.
- Each dropped note becomes a straight arrow along its string. It has a small start dot at the dropped position and an arrowhead at the edge of the altered note one fret away.
- The arrows point towards the nut for flats and away from it for sharps.
- If the altered note would fall outside frets 0-12 (for example the b3 of an open E string), nothing is drawn at that position. That alteration remains visible elsewhere on the board.
- The legend replaces the "dropped" ghost entry with an arrow entry.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mode-comparison`: dropped notes are shown as arrows instead of ghosts, and the altered-style requirement no longer mentions ghosts.
- `fretboard-display`: note dots are only drawn for shared and altered notes, and the legend shows the arrow instead of the ghost.

## Impact

- `fretboard/render.py`: arrow drawing, removal of the ghost style, legend entry.
- `tests/test_render.py` and `tests/test_app.py`: ghost assertions are replaced with arrow assertions.
- `README.md`: the "Reading the fretboard" section.
- `fretboard/theory.py` is unchanged, because the classification still produces shared, dropped and altered states.
