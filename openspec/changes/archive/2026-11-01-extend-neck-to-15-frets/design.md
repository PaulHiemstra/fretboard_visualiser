## Context

`render_fretboard` already takes `frets` as a parameter (default 12), and all geometry is derived from it. Inlays are the constants `INLAY_FRETS = (3, 5, 7, 9)` and `DOUBLE_INLAY_FRET = 12`.

## Goals / Non-Goals

**Goals:**
- Make 15 frets the default everywhere the app renders the neck.

**Non-Goals:**
- A user setting for the number of frets.
- Changing the fret spacing to a realistic (logarithmic) scale.

## Decisions

### 1. One default, defined once

Add `DEFAULT_FRETS = 15` in `render.py` and use it as the default of `render_fretboard` (and of the voicing search call from the app, if `add-triad-inversions` has landed). The app passes nothing extra.

### 2. Inlays

`INLAY_FRETS` becomes `(3, 5, 7, 9, 15)`. They are filtered with `f <= frets` as now, so a 12-fret render (used in tests) stays correct.

### 3. Width

With equal fret spacing the viewBox grows from 858 to 1050 units. The SVG keeps `width="100%"` with `max-width` equal to its natural width, so on narrow screens it scales down. Dots then shrink to about 80% of their current size on a 1000px-wide page. This is acceptable, and fret spacing can be revisited if it feels cramped.

## Risks / Trade-offs

- [Smaller dots on narrow screens] -> Scale stays proportional, and labels remain legible at 12px x 0.8. Check this in the visual task.
- [Order relative to `add-triad-inversions`] -> The changes are independent. The voicing search uses whatever `frets` value it receives, so either order works.
