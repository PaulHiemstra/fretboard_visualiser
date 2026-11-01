## 1. Theory

- [x] 1.1 Add `Voicing` and `voicings(triad, tuning, frets, string_sets, max_span=4)` plus chord-tone labels to `theory.py`; verify with tests for C major on 3-2-1 and 5-4-3 (exact shapes and inversions from the spec), Bdim root position (7, 5, 3) on 6-5-4, Cm labels `R b3 5`, and that no shape spans more than 4 fretted frets for any chord in any mode

## 2. Rendering

- [x] 2.1 Extend `render_fretboard` with `chord` and `string_set`: fade the scale group, draw one polyline per shape and the deduplicated shape dots (inversion colour or neutral outline when shared by different inversions, `R` dark fill, data attributes); verify with tests that no chord means an unchanged SVG, C major 3-2-1 has 3 lines in the 3 inversion colours, and C major "all" draws the open G dot with a neutral outline
- [x] 2.2 Add `render_inversion_legend(triad)`; verify with a test that it names the chord and contains the three inversion colours
- [x] 2.3 Make chord-table cells clickable (`data-column`, `data-degree`, `onclick` with `emitEvent('chord_click', ...)`) and frame the selected cell; verify with tests that every chord cell has the handler and only the selected cell is framed

## 3. App

- [x] 3.1 Add selection state, the `chord_click` handler (toggle), the string-set toggle (default 3-2-1, shown only with a selection) and the inversion legend to `app.py`; verify with user-simulation tests: select/deselect Dm, Dorian degree 3 mode -> Mixolydian keeps degree 3 (Edim), mode selection cleared on C major alone, major-column selection kept, string-set change redraws the shapes
- [x] 3.2 Update the README with how to select a chord and read the inversion shapes; verify by reading it against the specs
- [x] 3.3 Render C major (3-2-1 and all) and Cm in Dorian (5-4-3) to PNG and compare with the approved mockups; verify the colours, lines, fade and neutral shared dots
