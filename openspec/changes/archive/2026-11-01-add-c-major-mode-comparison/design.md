## Context

This is a new project with no existing code (see proposal.md for motivation). The design has to stay small, but it should not block later additions: other tunings, other roots and arbitrary scales.

## Goals / Non-Goals

**Goals:**
- Keep music theory, rendering and UI in separate layers so that the theory and rendering layers can be tested without a browser.
- Represent modes and tunings as data, so that adding a scale or tuning later needs no new logic.

**Non-Goals:**
- A general scale-comparison engine that handles arbitrary roots or two arbitrary scales.
- Interactive SVG (click or hover on notes).
- Persisting the user's selection between sessions.

## Decisions

### 1. Three layers

```
theory.py  (pure)      render.py  (pure)          app.py  (NiceGUI)
-----------------      -------------------        -------------------
pitch classes 0-11     fretboard positions  -->   select: comparison
MAJOR degrees          + classifications           toggle: labels
MODES (alterations)    --> SVG string              ui.html(svg) refresh
classify(mode)                                     legend
```

`theory.py` and `render.py` do not import NiceGUI. `app.py` only connects widgets to `render.py`.

Alternative considered: draw with NiceGUI elements, such as one element per dot. This was rejected because it is harder to test and slower to redraw than one SVG string.

### 2. Modes as alterations of major

The major scale is stored as degree -> semitone: `{1:0, 2:2, 3:4, 4:5, 5:7, 6:9, 7:11}`. A mode is a name plus `{degree: offset}`, for example Dorian is `{3: -1, 7: -1}`. Classification follows from that:
- shared = major degrees without an alteration
- dropped = altered major degrees, at their major pitch
- altered = the same degrees at major pitch + offset, labelled `b`/`#` + degree

Alternative considered: store modes as interval sets and derive the difference with set operations. This loses which degree an alteration belongs to, so it can't produce `b3` labels or correct spelling without extra inference. The alteration form matches how the user wants to learn ("Dorian is major with b3 b7").

For all seven diatonic modes, altered pitches never coincide with a C major pitch. That keeps each fret position in exactly one state. Section 3 covers scales where this would not hold.

### 3. One state per pitch class

The classification result is a map `pitch_class -> (state, degree_label)`. Rendering looks up `(open_string_midi + fret) % 12` for each position. If a later scale makes an altered pitch equal a major pitch (for example a #2 that matches b3 in a non-diatonic scale), the map would need a combined state. That is deferred, and this change only includes the diatonic modes.

### 4. Note-name spelling from the degree

With the root fixed at C, spelling is a lookup: take the natural letter for the degree (C D E F G A B), then add `b` or `#` from the alteration. This avoids a general enharmonic algorithm, which can be added when other roots arrive.

### 5. Tuning as data

The tuning is a list of MIDI numbers, low to high: `[40, 45, 50, 55, 59, 64]`. The renderer reads its length and frets from parameters (default 12), so 7-string guitars, bass and alternative tunings only need new data.

### 6. Visual styles

| State | Style |
|---|---|
| root | filled, dark/accent colour, white label |
| shared | filled, neutral colour |
| dropped | no fill, dashed light outline, faded label |
| altered | filled highlight colour **and** thick outline (so it doesn't rely on colour alone) |

Open-string (fret 0) dots are drawn left of the nut. Colours are defined as constants in `render.py`.

### 7. UI wiring

The app uses `ui.select` for the comparison option, `ui.toggle` for degrees/notes and `ui.html` holding the SVG. A `@ui.refreshable` function or a direct `content` update rebuilds the SVG when either control changes. The legend is a small static SVG or HTML row that shows the states relevant to the current selection.

### 8. Tooling

Python 3.12+, with a `pyproject.toml` installed into a plain virtual environment (`python3 -m venv .venv` + `pip install -e ".[dev]"`) and `pytest` for tests. `uv` was considered but is not installed on the development machine, and a venv needs no extra tooling. The app runs with `.venv/bin/python -m fretboard.app` on NiceGUI's default port.

## Risks / Trade-offs

- [Full SVG redraw on each change] -> The SVG is small (about 78 positions), so the redraw is not noticeable.
- [The alteration model only covers "major + alterations"] -> That is the intended learning model. Arbitrary scales can be added later by deriving alterations from interval sets.
- [Fixed root C hard-coded in spelling] -> Keep the root as a parameter in `theory.py` with a default of C. Other roots then only need a better speller, not a rewrite.
- [Ghost dots could clutter the view] -> Use subdued styling. A "hide ghosts" toggle can be added later if needed.
