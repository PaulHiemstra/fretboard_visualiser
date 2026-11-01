## Context

`render_fretboard` currently draws one note dot per scale position, with a separate `dropped` style for ghosts. Classification in `theory.py` already distinguishes shared, dropped and altered pitches. Only the rendering changes. The visual direction was chosen from scratchpad mockups (straight arrows with a start dot, over curved arrows and ghost dots).

## Goals / Non-Goals

**Goals:**
- Replace ghost dots with straight arrows as in the chosen mockup.
- Keep the SVG testable through data attributes.

**Non-Goals:**
- A toggle between ghosts and arrows.
- Curved or animated arrows.
- Changes to classification or labels.

## Decisions

### 1. Pair arrows by position, not by pitch

For each dropped position `(string, fret)`, look at `fret + offset` on the same string, where `offset` is the degree's alteration (-1 for a flat, +1 for a sharp). The renderer gets it from the classification: the altered `PitchInfo` for the same degree. If that fret lies within 0..frets, draw the arrow. Otherwise draw nothing.

Alternative considered: search both neighbouring frets for any altered dot. This was rejected because it could pair with the wrong altered note if two alterations were ever adjacent. Using the degree's own offset is exact.

### 2. Geometry and style

```
   (b3) <|------*
         ^      ^
         |      start dot r=5.5, at the centre of the dropped position
         arrowhead touches the altered dot's edge (DOT_R + 3 from its centre)
```

- A straight line on the string's y coordinate, stroke width 2.5, in the altered outline colour (`#9a3412`).
- An SVG `<marker>` arrowhead in the same colour, defined once per SVG in `<defs>`.
- The start dot is a filled circle with r=5.5, in the same colour.
- Arrows are drawn after the note dots so they sit on top of strings and inlays.
- The `dropped` entry is removed from `STYLES`.

### 3. Test hooks

Each arrow is a `<g class="move" data-string data-from data-to data-degree>` group. Tests assert on these attributes, the same way they do on note dots.

### 4. Legend

The legend entry "C major note, dropped" (ghost) is replaced by a small arrow drawing (start dot + arrow) with the text "moved from C major". The order becomes root, shared, altered, moved. It is still hidden for C major alone.

## Risks / Trade-offs

- [Alterations on open strings that would go below fret 0 disappear silently] -> The same degree is always visible elsewhere on a 12-fret neck (the octave at fret 12, with its arrow to fret 11). This is accepted and specified.
- [The arrow covers part of the string line] -> It is thicker and coloured, so it stays readable. This was confirmed in the mockup.
- [Losing the dropped note's label (for example "3")] -> The altered label (`b3`) already names the degree, and the arrow direction shows the alteration.
