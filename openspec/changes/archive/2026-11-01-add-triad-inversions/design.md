## Context

The page has the fretboard SVG (`render_fretboard`), the legend and an HTML chord table (`render_chord_table`), all rendered as strings and placed in `ui.html` elements that `update()` refreshes. `theory.Triad` already knows its notes as (degree, alteration). This change adds chord selection and an overlay of triad shapes. The visual direction comes from scratchpad mockups: one string set at a time works best, and "all" is useful but busy.

## Goals / Non-Goals

**Goals:**
- Find shapes using rules only (no hand-entered shape tables), so they work for any mode, number of frets or, later, tuning.
- Keep rendering pure and testable, and keep the app as thin wiring.

**Non-Goals:**
- Spread (open) voicings, shapes on non-neighbouring strings, four-note chords.
- Fingering numbers or audio.
- Extending the neck (handled by the separate change `extend-neck-to-15-frets`).

## Decisions

### 1. Shape search by brute force

`theory.voicings(triad, tuning, frets, string_sets, max_span=4) -> list[Voicing]`. For each string set (three neighbouring tuning indices) it tries every combination of three frets in `0..frets`. That is 13^3 = 2197 combinations per set at 12 frets (4096 at 15), which is trivial. It keeps a combination when:
- the pitch classes are exactly the chord's three notes,
- the MIDI pitches rise strictly and `top - bottom < 12`,
- the fretted frets span `<= max_span`.

`Voicing` is a frozen dataclass: the string-set indices, the frets, the inversion (`"root" | "1st" | "2nd"`, taken from the bass note) and the chord-tone label for each note.

Alternative considered: hard-coded CAGED-like shape templates per string set. This was rejected because it is fragile with the B string's tuning offset and with future tunings. Brute force is short and verifiably correct.

### 2. Chord-tone labels

These come from the interval above the root: 3 -> `b3`, 4 -> `3`, 6 -> `b5`, 7 -> `5`, 8 -> `#5`. The root gets `R`. A `Triad.tone_labels()` helper or a function in `theory.py` provides them.

### 3. Rendering the overlay

`render_fretboard(..., chord: Triad | None = None, string_set: str = "3-2-1")`:
- With a chord, all existing dot and arrow groups are wrapped in `<g class="scale" opacity="0.2">`. Without a chord there is no wrapper, so the SVG is unchanged.
- The overlay group comes after the scale group. All lines are drawn first (`<polyline>` per shape, width 4, round joins, inversion colour, `class="shape-line"`, `data-inversion`), then the dots, so lines never cover dots.
- Shape dots are deduplicated by position. A dot gets the inversion colour as its outline if all shapes containing it share one inversion. Otherwise it gets a neutral outline (`#4b5563`). The fill is dark for `R` and white otherwise. Data attributes: `data-string`, `data-fret`, `data-tone`, `data-inversions`.
- Colours (Okabe-Ito): root position `#0072B2`, 1st inversion `#009E73`, 2nd inversion `#CC79A7`. These are distinct from the altered orange and readable for common colour-vision deficiencies.

String sets map to tuning indices with the 6-string standard tuning: `6-5-4 -> (0,1,2)`, `5-4-3 -> (1,2,3)`, `4-3-2 -> (2,3,4)`, `3-2-1 -> (3,4,5)`, `all -> all four`.

### 4. Inversion legend

`render_inversion_legend(triad) -> str` is a small SVG: "<chord name>:" followed by three short coloured lines with the labels "root position", "1st inversion" and "2nd inversion". The app shows it only while a chord is selected.

### 5. Clickable table cells

`render_chord_table(comparison, selected: tuple[str, int] | None = None)`. Each chord cell gets `data-column` (`major`/`mode`), `data-degree`, `cursor:pointer` and `onclick="emitEvent('chord_click', {column: '<col>', degree: <n>})"`. The selected cell gets an outline (`outline: 2px solid #1f2937`) and `data-selected="true"`.

Alternative considered: making each cell a NiceGUI element with its own click handler. This was rejected because the table would no longer be a single HTML string, which would break the existing render and test pattern. `emitEvent` is NiceGUI's documented way to send events from custom HTML.

### 6. App state

`app.root()` keeps `selected: tuple[str, int] | None` in a local closure (per page/client):
- `ui.on('chord_click', handler)` toggles the selection (same cell -> `None`) and calls `update()`.
- On a comparison change: if the new comparison is C major alone and `selected[0] == "mode"`, set it to `None`.
- `update()` resolves the triad: `triads(major)[d-1]` for the major column, `triads(comparison)[d-1]` for the mode column.
- A `ui.toggle` for the string set (`6-5-4 / 5-4-3 / 4-3-2 / 3-2-1 / all`, default `3-2-1`) sits next to the inversion legend and also calls `update()`. It is shown only while a chord is selected.

Tests trigger the click handler directly, because the user simulation does not run browser JavaScript.

## Risks / Trade-offs

- [The "all" view is busy: shared notes and lines that form a chain] -> Neutral outlines for shared notes. "All" is an option, not the default.
- [The 12-fret neck misses some shapes, for example F root position on 6-5-4] -> This is accepted. `extend-neck-to-15-frets` covers it, and the search already uses the number of frets shown.
- [`emitEvent` in inline `onclick`] -> It depends on NiceGUI's global JS function. It is verified to exist in NiceGUI 3.18, and the event name and payload are covered by tests on the Python side.
