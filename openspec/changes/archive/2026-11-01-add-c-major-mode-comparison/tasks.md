## 1. Project setup

- [x] 1.1 Create `pyproject.toml` (Python 3.12+, `nicegui` dependency, `pytest` dev dependency) and a `fretboard/` package with `theory.py`, `render.py`, `app.py`; verify `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"` succeeds and `.venv/bin/pytest` runs (0 tests is fine)

## 2. Theory layer

- [x] 2.1 Define the C major degree map, the standard tuning (MIDI `[40, 45, 50, 55, 59, 64]`) and the ordered comparison options (C major alone, Lydian, Mixolydian, Dorian, Aeolian, Phrygian, Locrian) with their alterations; verify with a test that the order and alterations match the mode-comparison spec table
- [x] 2.2 Implement classification (pitch class -> state shared/dropped/altered + degree label); verify with tests for C major alone, Dorian (E/B dropped, Eb/Bb altered), Lydian (F dropped, F# altered) and that C is always shared
- [x] 2.3 Implement note-name spelling from degree + alteration; verify with tests that b3 -> Eb, b7 -> Bb, #4 -> F#, b5 -> Gb, b2 -> Db

## 3. Rendering layer

- [x] 3.1 Implement fretboard position mapping (string, fret 0-12 -> pitch class); verify with tests that the open low E is E, A string fret 3 is C and B string fret 1 is C
- [x] 3.2 Render the fretboard SVG: 6 strings (high E on top), nut, frets 1-12, fret numbers, inlays at 3/5/7/9 and a double inlay at 12; verify the SVG contains 6 string lines and 5 inlay groups with a test
- [x] 3.3 Draw note dots in root/shared/dropped/altered styles with degree or note-name labels; verify with tests that Dorian's SVG has a ghost dot at B string fret 5 and an altered dot labelled `b3` (or `Eb` in note mode) at B string fret 4, and no dot on C# positions
- [x] 3.4 Render the legend for the states relevant to the current selection; verify with a test that C major alone omits the dropped/altered entries and Dorian includes them

## 4. NiceGUI app

- [x] 4.1 Build the page: a comparison select (options labelled with alterations, e.g. "Dorian (b3 b7)", Aeolian also showing "natural minor", default C major alone), a degrees/notes toggle (default degrees), the fretboard SVG and the legend; verify by running the app and checking that the page loads with C major alone and degree labels
- [x] 4.2 Wire the controls so that changing either one re-renders the fretboard without a page reload; verify manually by switching Dorian -> Phrygian (D ghosted, Db altered) and toggling to note names (Lydian shows F#)

## 5. Wrap-up

- [x] 5.1 Add a README with run instructions (venv + `pip install -e ".[dev]"`, `python -m fretboard.app`) and a short explanation of the visual states; verify the instructions start the app from a clean checkout
