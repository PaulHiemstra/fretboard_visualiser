## 1. Rendering

- [x] 1.1 Stop drawing note dots for dropped positions and remove the `dropped` style; verify with a test that Dorian has no note dot on any E or B position and that C major alone is unchanged
- [x] 1.2 Draw straight arrows (start dot r=5.5, line, arrowhead marker) from each dropped position to the altered note at `fret + offset` when that fret is within 0-12, as `<g class="move">` groups with data attributes; verify with tests for Dorian B string 5 -> 4, Lydian high E 1 -> 2, no arrow on Dorian open low E, and identical arrows in note-name mode
- [x] 1.3 Replace the legend's ghost entry with an arrow entry ("moved from C major"); verify with tests that Dorian's legend is root, shared, altered, moved and that C major alone shows only root and shared

## 2. App, docs and checks

- [x] 2.1 Update `tests/test_app.py` for arrows instead of dropped dots (Phrygian: arrow on the G string from fret 7 to fret 6); verify the full test suite passes
- [x] 2.2 Update the README's "Reading the fretboard" section to describe arrows instead of ghost dots; verify by reading it against the specs
- [x] 2.3 Render Dorian and Lydian boards to PNG and compare them with the approved mockup; verify that the arrows are straight, have the larger start dot and point the right way
