## 1. Neck

- [x] 1.1 Add `DEFAULT_FRETS = 15`, use it as the `render_fretboard` default and add fret 15 to `INLAY_FRETS`; verify with updated tests: 15 fret lines, fret numbers 0-15, inlays at 3/5/7/9/15 plus the double at 12, low E dots at 13 and 15 but not 14 for C major alone, and the Dorian arrow 14 -> 13 on the A string
- [x] 1.2 If `add-triad-inversions` is implemented, make sure the app passes the same fret count to the voicing search; verify that F major on 6-5-4 now shows a root-position shape at (13, 12, 10)

## 2. Checks

- [x] 2.1 Run the full test suite and render C major and Dorian to PNG; verify that all tests pass and that the wider neck stays legible
