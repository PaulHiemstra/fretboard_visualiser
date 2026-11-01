## Why

Many triad shapes do not fit on a 0-12 neck. For example, F major in root position on strings 6-5-4 only exists at frets 13-12-10. Showing three extra frets means every string set shows a full cycle of inversions for almost every chord. It also mirrors the neck below fret 3 above fret 12, which helps you recognise positions.

## What Changes

- The fretboard shows frets 0 through 15 instead of 0 through 12.
- An extra single inlay marker appears at fret 15.
- Scale dots and arrows are drawn on frets 0-15.
- Triad shapes from `add-triad-inversions` use the number of frets shown, so they automatically include shapes up to fret 15 (no requirement change needed there).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `fretboard-display`: the fret range (0-15), the inlay at fret 15 and dots on frets 0-15.
- `mode-comparison`: arrows are drawn within frets 0-15.

## Impact

- `fretboard/render.py`: the default `frets` becomes 15, and fret 15 is added to the inlays.
- Tests that assume 12 frets (fret lines, fret numbers, inlays) are updated.
- The SVG gets wider (its viewBox grows by 3 frets). It already scales to the page width.
