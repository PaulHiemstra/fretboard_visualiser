# Fretboard scale visualiser

Learn the C major scale on the guitar fretboard, then learn the other C modes as small
alterations of it. C major is always the reference; pick a mode and the fretboard shows
exactly which notes move.

| Option | Alterations of C major |
|---|---|
| C major alone | none |
| Lydian | #4 |
| Mixolydian | b7 |
| Dorian | b3 b7 |
| Aeolian / natural minor | b3 b6 b7 |
| Phrygian | b2 b3 b6 b7 |
| Locrian | b2 b3 b5 b6 b7 |

## Running

Requires Python 3.12 or newer.

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m fretboard.app
```

Then open <http://localhost:8080>.

Run the tests with:

```bash
.venv/bin/pytest
```

## Reading the fretboard

Standard tuning, frets 0-15, high E string on top. Labels can show scale degrees
(default) or note names.

- **Dark dot**: the root, C.
- **Grey dot**: a note shared by C major and the selected mode.
- **Orange dot with a thick outline**: the mode's altered note.
- **Arrow**: a C major note that the mode moves. The small dot marks where the C major note
  was; the arrow slides along the string to the altered note, one fret towards the nut for a
  `b` and one fret away from it for a `#`. Near the nut, where a flat would fall below
  fret 0, no arrow is drawn; the same degree appears elsewhere on the neck.

## Chord table

Below the fretboard, a table lists the triad on each scale degree with its chord name and
Roman numeral (for example `Dm ii`). With a mode selected, it adds the mode's triads next to
the C major ones. Rows where the chord changes are highlighted and show an arrow, and the
"Why" column names the altered notes in that chord (for example `E → Eb, B → Bb`). The
table ignores the degrees/note-names toggle: chords are always named by note.

## Triad shapes

Click a chord in the table (C major column or mode column) to show where to play it. The
scale fades into the background and every compact triad shape of that chord is drawn on top:
three notes on three neighbouring strings, within one octave, at most five frets wide (open
strings don't count). Each shape is coloured by inversion and its notes are connected by a line:

- **Blue**: root position (root in the bass)
- **Green**: 1st inversion (3rd in the bass)
- **Purple**: 2nd inversion (5th in the bass)

Dots are labelled with chord tones (`R`, `3`/`b3`, `5`/`b5`). Pick the string set with the
toggle next to the legend (default 3-2-1). With "all", a note shared by shapes of different
inversions gets a grey outline. Click the chord again to clear it. The selection keeps its
degree and column when you switch modes, so you can compare, say, the chord on degree 3
across modes.

## Layout

- `fretboard/theory.py`: scales, modes as alterations of major, note classification, spelling and triads.
- `fretboard/render.py`: SVG fretboard and legend, HTML chord table.
- `fretboard/app.py`: NiceGUI page.
