## Why

Altering a scale note also changes every chord that contains it. For example, Dorian's two flats change five of the seven triads. The fretboard shows which notes move, but not what that does to the harmony. A chord table under the fretboard, using the same "C major, then what changes" view, connects the modes to the chords you play with them.

## What Changes

- New chord table below the fretboard and legend, with one row per scale degree (1-7).
- For C major alone, the table shows a single column of C major triads, each with its chord name and Roman numeral (for example `Dm  ii`).
- When a mode is selected, the table also shows:
  - a column with the mode's triads,
  - an arrow between the two columns on every row where the chord changes,
  - a "why" column naming the altered note(s) in that chord (for example `E → Eb`).
- Changed rows are highlighted in the same altered style as the fretboard.
- The table updates together with the fretboard when the selection changes. The degrees/note-names toggle does not affect it, because chords are always named by note.
- Triads only. Seventh chords and clicking a chord to highlight its notes are out of scope.

## Capabilities

### New Capabilities

- `chord-table`: the diatonic triads of C major and of the selected mode, how each chord changes, and why.

### Modified Capabilities

None. The fretboard and comparison requirements are unchanged; the table is an addition to the page.

## Impact

- `fretboard/theory.py`: triad construction, chord quality, chord naming and Roman numerals.
- `fretboard/render.py` (or a new module): an HTML chord table.
- `fretboard/app.py`: the table is placed below the legend and updated together with the fretboard.
- New tests for the theory and the table, and a README update.
