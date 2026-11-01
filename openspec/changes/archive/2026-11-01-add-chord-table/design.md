## Context

`theory.py` already models each mode as alterations of the C major degrees and spells notes from degree + alteration. Chords can be derived from that same model. The page currently has the controls, the fretboard SVG and the legend. The table goes below the legend.

## Goals / Non-Goals

**Goals:**
- Derive chords from the existing degree/alteration model so that spelling stays consistent with the fretboard.
- Keep the table renderable and testable without a browser, the same way as the fretboard.

**Non-Goals:**
- Seventh chords, inversions, voicings.
- Interaction between the table and the fretboard (clicking a chord). This is noted for later.

## Decisions

### 1. Triads in degree space

A triad on degree `d` uses degrees `d, d+2, d+4` (1-based, wrapping after 7). Each note is `(degree, alteration)`, with `alteration = comparison.alterations.get(degree, 0)`. Pitch classes come from `MAJOR[degree] + alteration`, and the quality from the semitone intervals root->3rd and root->5th:

| 3rd | 5th | quality | name suffix | numeral |
|---|---|---|---|---|
| 4 | 7 | major | `` | upper |
| 3 | 7 | minor | `m` | lower |
| 3 | 6 | diminished | `dim` | lower + `°` |
| 4 | 8 | augmented | `aug` | upper + `+` |

Any other combination raises `ValueError`. Diatonic modes never produce one, but this guards future scales.

A chord is changed if any of its three degrees has a non-zero alteration. The why entries are `note_name(degree, 0) -> note_name(degree, alteration)` for those degrees, in chord order.

Alternative considered: compute chords from pitch-class sets and name them with a chord-recognition routine. That is overkill, and it would lose the degree-based spelling (it could produce D# instead of Eb).

### 2. Data model

`theory.py` gets a frozen `Triad` dataclass (degree, root alteration, quality, notes as (degree, alteration) tuples) with `name`, `numeral` and `altered_notes` properties. It also gets `triads(comparison) -> list[Triad]`. `COMPARISONS_BY_KEY["major"]` provides the reference column.

### 3. Rendering: HTML table string

`render.py` gets `render_chord_table(comparison) -> str`, which returns an HTML `<table>` that the app shows in a `ui.html(sanitize=False)` element, the same pattern as the SVGs.

- Columns: `Degree | C major | -> | <mode name> | Why`. With C major alone, only `Degree | C major`.
- Each chord cell shows the name in bold and the numeral after it in a muted colour.
- Changed rows get the altered fill (`#f59e0b` at reduced opacity) and a left border in the altered outline colour (`#9a3412`), so they don't rely on colour alone. The arrow cell shows `→`.
- Rows carry `data-degree` and `data-changed`, and cells carry classes (`major`, `mode`, `arrow`, `why`) for tests.

Alternative considered: NiceGUI's `ui.table`. Styling individual rows needs Quasar slot templates, and testing it needs the browser-side model. A plain HTML string is simpler and matches the existing approach.

### 4. App wiring

The table is placed below the legend. It is updated in the existing `update()` callback, so it follows the comparison select. It ignores the label toggle (spec: chord names are always note names).

## Risks / Trade-offs

- [Wide table on small screens] -> Five short columns fit easily. The table width is set to auto rather than full width.
- [The `°` and `→` characters] -> These are plain UTF-8 in HTML, which NiceGUI serves as UTF-8, so they display correctly.
