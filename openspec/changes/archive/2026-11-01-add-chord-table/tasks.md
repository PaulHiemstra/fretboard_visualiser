## 1. Theory

- [x] 1.1 Add `Triad` and `triads(comparison)` to `theory.py` (degree stacking, quality from intervals, `ValueError` on unknown quality); verify with tests that C major, Dorian and Lydian produce the triads in the chord-table spec, and that all seven modes build without error
- [x] 1.2 Add chord `name`, Roman `numeral` and `altered_notes` (why entries); verify with tests for C major numerals (I ii iii IV V vi vii°), Dorian `Eb`/`bIII` and `Bb`/`bVII`, Lydian `F#dim`/`#iv°`, Dorian row 3 why = `E -> Eb, B -> Bb`, and Dorian rows 2 and 4 unchanged

## 2. Rendering

- [x] 2.1 Add `render_chord_table(comparison)` producing the HTML table (single column for C major alone; degree, C major, arrow, mode, why for modes; changed rows highlighted with fill and left border; data attributes); verify with tests that C major alone has 7 rows and no comparison columns, Dorian has arrows exactly on rows 1, 3, 5, 6, 7, Mixolydian highlights only rows 3, 5, 7 and Aeolian highlights all rows

## 3. App and docs

- [x] 3.1 Place the chord table below the legend and update it in `update()`; verify with user-simulation tests that switching Dorian -> Mixolydian changes the table and toggling labels does not
- [x] 3.2 Update the README with a short description of the chord table; verify by reading it against the spec
- [x] 3.3 Render the Dorian page table and look at it (screenshot or HTML preview); verify that the arrows, why text and row highlighting read clearly
