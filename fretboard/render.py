"""Render the fretboard and legend as SVG strings. No UI imports."""

from html import escape
from typing import Literal

from .theory import (
    COMPARISONS_BY_KEY,
    ROOT_PC,
    STANDARD_TUNING,
    Comparison,
    PitchInfo,
    State,
    Triad,
    Voicing,
    classify,
    triads,
    voicings,
)

LabelMode = Literal["degrees", "notes"]

# String sets for triad shapes, as tuning indices (0 = lowest string), low to high.
STRING_SETS: dict[str, list[tuple[int, int, int]]] = {
    "6-5-4": [(0, 1, 2)],
    "5-4-3": [(1, 2, 3)],
    "4-3-2": [(2, 3, 4)],
    "3-2-1": [(3, 4, 5)],
    "all": [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)],
}
DEFAULT_STRING_SET = "3-2-1"

# Inversion colours (Okabe-Ito: blue, bluish green, reddish purple).
INVERSION_COLORS = {"root": "#0072B2", "1st": "#009E73", "2nd": "#CC79A7"}
INVERSION_NAMES = {"root": "root position", "1st": "1st inversion", "2nd": "2nd inversion"}
SHARED_SHAPE_OUTLINE = "#4b5563"
SCALE_FADE = 0.2

# Geometry (SVG user units).
NUT_X = 70
OPEN_X = 34
FRET_W = 64
TOP_Y = 30
STRING_GAP = 34
DOT_R = 13
DEFAULT_FRETS = 15
INLAY_FRETS = (3, 5, 7, 9, 15)
DOUBLE_INLAY_FRET = 12

# Colours.
BOARD = "#f3e9d8"
FRET_LINE = "#a8977a"
NUT = "#2b2b2b"
STRING = "#6b6b6b"
INLAY = "#d9cbb2"
TEXT_MUTED = "#6b6b6b"

# Dot styles: fill, stroke, stroke width, label colour.
STYLES: dict[str, dict[str, str]] = {
    "root": {"fill": "#1f2937", "stroke": "#1f2937", "sw": "1.5", "text": "#ffffff"},
    "shared": {"fill": "#d1d5db", "stroke": "#4b5563", "sw": "1.5", "text": "#111827"},
    "altered": {"fill": "#f59e0b", "stroke": "#9a3412", "sw": "3", "text": "#111827"},
}

# Arrow from a dropped C major note to its altered note.
ARROW = "#9a3412"
ARROW_WIDTH = 2.5
ARROW_START_R = 5.5
ARROW_GAP = 3  # space between the arrowhead and the altered dot's outline
ARROW_MARKER_ID = "move-arrowhead"


def position_pc(tuning: tuple[int, ...], string_index: int, fret: int) -> int:
    """Pitch class at a string (0 = lowest string) and fret."""
    return (tuning[string_index] + fret) % 12


def style_name(pc: int, info: PitchInfo) -> str:
    if info.state is State.SHARED and pc == ROOT_PC:
        return "root"
    return info.state.value


def _dot(x: float, y: float, style: str, label: str, attrs: str = "") -> str:
    s = STYLES[style]
    return (
        f'<g class="dot dot-{style}"{attrs}>'
        f'<circle cx="{x}" cy="{y}" r="{DOT_R}" fill="{s["fill"]}" stroke="{s["stroke"]}" '
        f'stroke-width="{s["sw"]}"/>'
        f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
        f'font-family="sans-serif" font-size="12" font-weight="bold" fill="{s["text"]}">'
        f"{escape(label)}</text></g>"
    )


def _arrow_defs(marker_id: str) -> str:
    """An arrowhead marker; each SVG defines its own so ids stay unique on the page."""
    return (
        f'<defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ARROW}"/></marker></defs>'
    )


def _arrow(x_from: float, x_to: float, y: float, marker_id: str, attrs: str = "") -> str:
    """Straight arrow from a start dot at x_from to the edge of the note dot at x_to."""
    direction = 1 if x_to > x_from else -1
    x_end = x_to - direction * (DOT_R + ARROW_GAP)
    return (
        f'<g class="move"{attrs}>'
        f'<circle cx="{x_from}" cy="{y}" r="{ARROW_START_R}" fill="{ARROW}"/>'
        f'<line x1="{x_from}" y1="{y}" x2="{x_end}" y2="{y}" stroke="{ARROW}" '
        f'stroke-width="{ARROW_WIDTH}" marker-end="url(#{marker_id})"/></g>'
    )


def _fret_x(fret: int) -> float:
    """Centre x of a note at a fret (fret 0 is left of the nut)."""
    return OPEN_X if fret == 0 else NUT_X + (fret - 0.5) * FRET_W


def render_fretboard(
    comparison: Comparison,
    labels: LabelMode = "degrees",
    tuning: tuple[int, ...] = STANDARD_TUNING,
    frets: int = DEFAULT_FRETS,
    chord: Triad | None = None,
    string_set: str = DEFAULT_STRING_SET,
) -> str:
    """Return an SVG of the fretboard with the comparison drawn on it.

    With a chord, the scale is faded and the chord's triad shapes on the given
    string set are drawn on top: lines carry class="shape-line" and
    data-inversion; shape dots carry data-string, data-fret, data-tone and
    data-inversions.

    The highest string is drawn at the top. Dropped C major notes are drawn as
    arrows to their altered note, not as dots. For testing, note dots carry
    data-string (1 = highest string), data-fret, data-state and data-label;
    arrows carry data-string, data-from, data-to and data-degree.
    """
    n = len(tuning)
    bottom_y = TOP_Y + (n - 1) * STRING_GAP
    mid_y = (TOP_Y + bottom_y) / 2
    width = NUT_X + frets * FRET_W + 20
    height = bottom_y + 45
    neck_end = NUT_X + frets * FRET_W
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" style="max-width:{width}px" role="img" '
        f'aria-label="Fretboard: C major compared with {escape(comparison.name)}">',
        _arrow_defs(ARROW_MARKER_ID),
        f'<rect x="{NUT_X}" y="{TOP_Y - 14}" width="{neck_end - NUT_X}" '
        f'height="{bottom_y - TOP_Y + 28}" fill="{BOARD}"/>',
    ]

    # Inlays.
    for f in INLAY_FRETS:
        if f <= frets:
            parts.append(
                f'<g class="inlay" data-fret="{f}"><circle cx="{_fret_x(f)}" cy="{mid_y}" '
                f'r="7" fill="{INLAY}"/></g>'
            )
    if DOUBLE_INLAY_FRET <= frets:
        x = _fret_x(DOUBLE_INLAY_FRET)
        y1, y2 = TOP_Y + 1.5 * STRING_GAP, bottom_y - 1.5 * STRING_GAP
        parts.append(
            f'<g class="inlay inlay-double" data-fret="{DOUBLE_INLAY_FRET}">'
            f'<circle cx="{x}" cy="{y1}" r="7" fill="{INLAY}"/>'
            f'<circle cx="{x}" cy="{y2}" r="7" fill="{INLAY}"/></g>'
        )

    # Frets, nut and fret numbers.
    for f in range(1, frets + 1):
        x = NUT_X + f * FRET_W
        parts.append(
            f'<line class="fret" x1="{x}" y1="{TOP_Y - 14}" x2="{x}" y2="{bottom_y + 14}" '
            f'stroke="{FRET_LINE}" stroke-width="2"/>'
        )
    parts.append(
        f'<line class="nut" x1="{NUT_X}" y1="{TOP_Y - 14}" x2="{NUT_X}" y2="{bottom_y + 14}" '
        f'stroke="{NUT}" stroke-width="6"/>'
    )
    for f in range(0, frets + 1):
        parts.append(
            f'<text class="fret-number" x="{_fret_x(f)}" y="{bottom_y + 36}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="12" fill="{TEXT_MUTED}">{f}</text>'
        )

    # Strings: row 0 (top) is the highest string. Lower strings are drawn thicker.
    for row in range(n):
        y = TOP_Y + row * STRING_GAP
        parts.append(
            f'<line class="string" x1="{OPEN_X - DOT_R - 4}" y1="{y}" x2="{neck_end}" y2="{y}" '
            f'stroke="{STRING}" stroke-width="{1 + row * 0.4:.1f}"/>'
        )

    # Note dots, and arrows for dropped notes (drawn last, on top).
    if chord is not None:
        parts.append(f'<g class="scale" opacity="{SCALE_FADE}">')
    pitches = classify(comparison)
    arrows: list[str] = []
    for row in range(n):
        string_index = n - 1 - row
        y = TOP_Y + row * STRING_GAP
        for f in range(0, frets + 1):
            pc = position_pc(tuning, string_index, f)
            info = pitches.get(pc)
            if info is None:
                continue
            if info.state is State.DROPPED:
                target = f + comparison.alterations[info.degree]
                if 0 <= target <= frets:
                    attrs = (
                        f' data-string="{row + 1}" data-from="{f}" data-to="{target}" '
                        f'data-degree="{info.degree}"'
                    )
                    arrows.append(_arrow(_fret_x(f), _fret_x(target), y, ARROW_MARKER_ID, attrs))
                continue
            style = style_name(pc, info)
            label = info.degree_label if labels == "degrees" else info.note_name
            attrs = (
                f' data-string="{row + 1}" data-fret="{f}" data-state="{info.state.value}" '
                f'data-label="{escape(label)}"'
            )
            parts.append(_dot(_fret_x(f), y, style, label, attrs))
    parts.extend(arrows)
    if chord is not None:
        parts.append("</g>")
        shapes = voicings(chord, tuning, frets, STRING_SETS[string_set])
        parts.append(_shapes_overlay(shapes, n))

    parts.append("</svg>")
    return "".join(parts)


def _shapes_overlay(shapes: list[Voicing], n_strings: int) -> str:
    """Lines first, then one dot per position, so lines never cover dots."""
    def point(string_index: int, fret: int) -> tuple[float, float]:
        return _fret_x(fret), TOP_Y + (n_strings - 1 - string_index) * STRING_GAP

    parts = ['<g class="chord-shapes">']
    dots: dict[tuple[int, int], tuple[str, set[str]]] = {}
    for v in shapes:
        color = INVERSION_COLORS[v.inversion]
        pts = " ".join(f"{x},{y}" for x, y in (point(s, f) for s, f in zip(v.strings, v.frets)))
        parts.append(
            f'<polyline class="shape-line" data-inversion="{v.inversion}" points="{pts}" '
            f'fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" '
            f'stroke-linecap="round"/>'
        )
        for s, f, tone in zip(v.strings, v.frets, v.tones):
            dots.setdefault((s, f), (tone, set()))[1].add(v.inversion)
    for (s, f), (tone, inversions) in sorted(dots.items()):
        x, y = point(s, f)
        outline = (
            INVERSION_COLORS[next(iter(inversions))] if len(inversions) == 1 else SHARED_SHAPE_OUTLINE
        )
        fill, text = (STYLES["root"]["fill"], "#ffffff") if tone == "R" else ("#ffffff", "#111827")
        parts.append(
            f'<g class="shape-dot" data-string="{n_strings - s}" data-fret="{f}" '
            f'data-tone="{escape(tone)}" data-inversions="{" ".join(sorted(inversions))}">'
            f'<circle cx="{x}" cy="{y}" r="{DOT_R}" fill="{fill}" stroke="{outline}" stroke-width="3"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="sans-serif" font-size="12" font-weight="bold" fill="{text}">'
            f"{escape(tone)}</text></g>"
        )
    parts.append("</g>")
    return "".join(parts)


LEGEND_ARROW_LEN = 36
LEGEND_MARKER_ID = "legend-arrowhead"


def render_legend(comparison: Comparison) -> str:
    """Return an SVG legend for the dot styles and arrows relevant to the comparison."""
    entries = [
        ("root", "1", "root (C)"),
        ("shared", "5", "in C major" if comparison.is_reference_only else "shared"),
    ]
    if not comparison.is_reference_only:
        entries += [
            ("altered", "b3", f"altered in {comparison.name.split(' /')[0]}"),
            ("moved", "", "moved from C major"),
        ]
    y = DOT_R + 2
    parts: list[str] = [_arrow_defs(LEGEND_MARKER_ID)]
    x = DOT_R + 2
    for style, sample, text in entries:
        parts.append(f'<g class="legend-entry" data-style="{style}">')
        if style == "moved":
            # Start dot aligned with where a note dot would begin; the arrowhead tip lands
            # LEGEND_ARROW_LEN further on, followed by the text.
            x_from = x - DOT_R + ARROW_START_R
            tip = x_from + LEGEND_ARROW_LEN
            parts.append(_arrow(x_from, tip + DOT_R + ARROW_GAP, y, LEGEND_MARKER_ID))
            text_x = tip + 6
        else:
            parts.append(_dot(x, y, style, sample))
            text_x = x + DOT_R + 6
        parts.append(
            f'<text x="{text_x}" y="{y}" dominant-baseline="central" '
            f'font-family="sans-serif" font-size="13" fill="#374151">{escape(text)}</text></g>'
        )
        x = text_x + len(text) * 6.8 + 18 + DOT_R  # centre of the next entry's dot
    width = int(x - DOT_R)
    height = DOT_R * 2 + 4
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" style="max-width:{width}px" role="img" aria-label="Legend">'
        + "".join(parts)
        + "</svg>"
    )


# --- Chord table ----------------------------------------------------------------

CHANGED_ROW_FILL = "rgba(245, 158, 11, 0.18)"  # the altered dot fill, softened
TABLE_BORDER = "#e5e7eb"


CHORD_CLICK_EVENT = "chord_click"
SELECTED_OUTLINE = "#1f2937"


def _chord_cell(triad: Triad, cls: str, selected: bool) -> str:
    """A clickable chord cell; cls is the column ('major' or 'mode')."""
    click = f"emitEvent('{CHORD_CLICK_EVENT}', {{column: '{cls}', degree: {triad.degree}}})"
    frame = f"outline:2px solid {SELECTED_OUTLINE};outline-offset:-2px;" if selected else ""
    return (
        f'<td class="{cls}" data-column="{cls}" data-degree="{triad.degree}" '
        f'data-selected="{str(selected).lower()}" onclick="{click}" '
        f'style="padding:4px 12px;cursor:pointer;{frame}">'
        f'<span style="font-weight:bold">{escape(triad.name)}</span>'
        f'<span style="color:{TEXT_MUTED};margin-left:8px">{escape(triad.numeral)}</span></td>'
    )


def render_chord_table(comparison: Comparison, selected: tuple[str, int] | None = None) -> str:
    """Return an HTML table of the diatonic triads of C major and, for a mode, how they change.

    Rows carry data-degree and data-changed; cells carry the classes
    degree, major, arrow, mode and why for testing.
    """
    reference = triads(COMPARISONS_BY_KEY["major"])
    compare = not comparison.is_reference_only
    mode_triads = triads(comparison) if compare else reference
    mode_name = comparison.name.split(" /")[0]

    th = f'style="text-align:left;padding:4px 12px;border-bottom:2px solid {TABLE_BORDER}"'
    header = [f"<th {th}>Degree</th>", f"<th {th}>C major</th>"]
    if compare:
        header += [f"<th {th}></th>", f"<th {th}>C {escape(mode_name)}</th>", f"<th {th}>Why</th>"]

    rows = []
    for major, mode in zip(reference, mode_triads):
        changed = compare and mode.changed
        style = f"background:{CHANGED_ROW_FILL}" if changed else ""
        # Table rows cannot carry a border reliably, so the marker goes on the first cell.
        marker = f"border-left:4px solid {ARROW}" if changed else "border-left:4px solid transparent"
        cells = [
            f'<td class="degree" style="padding:4px 12px;color:{TEXT_MUTED};{marker}">{major.degree}</td>',
            _chord_cell(major, "major", selected == ("major", major.degree)),
        ]
        if compare:
            arrow = "\u2192" if changed else ""
            why = ", ".join(f"{a} \u2192 {b}" for a, b in mode.altered_notes) if changed else ""
            cells += [
                f'<td class="arrow" style="padding:4px 4px;color:{ARROW};font-weight:bold;font-size:18px">{arrow}</td>',
                _chord_cell(mode, "mode", selected == ("mode", mode.degree)),
                f'<td class="why" style="padding:4px 12px">{escape(why)}</td>',
            ]
        rows.append(
            f'<tr data-degree="{major.degree}" data-changed="{str(changed).lower()}" '
            f'style="border-bottom:1px solid {TABLE_BORDER};{style}">' + "".join(cells) + "</tr>"
        )

    return (
        '<table class="chord-table" style="border-collapse:collapse;font-family:sans-serif;'
        'font-size:14px;width:auto">'
        f"<thead><tr>{''.join(header)}</tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def render_inversion_legend(triad: Triad) -> str:
    """SVG legend: the chord name and the colour of each inversion."""
    y = DOT_R + 2
    title = f"{triad.name}:"
    parts = [
        f'<text x="0" y="{y}" dominant-baseline="central" font-family="sans-serif" '
        f'font-size="14" font-weight="bold" fill="#111827">{escape(title)}</text>'
    ]
    x = len(title) * 9 + 12
    for inversion, color in INVERSION_COLORS.items():
        name = INVERSION_NAMES[inversion]
        parts.append(
            f'<g class="legend-entry" data-inversion="{inversion}">'
            f'<line x1="{x}" y1="{y}" x2="{x + 28}" y2="{y}" stroke="{color}" stroke-width="4" '
            f'stroke-linecap="round"/>'
            f'<text x="{x + 36}" y="{y}" dominant-baseline="central" font-family="sans-serif" '
            f'font-size="13" fill="#374151">{escape(name)}</text></g>'
        )
        x += 36 + len(name) * 6.8 + 22
    width, height = int(x), DOT_R * 2 + 4
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        # Fixed natural size: inside a flex row a 100% width collapses and shrinks the text.
        f'width="{width}" height="{height}" role="img" aria-label="Inversion legend">'
        + "".join(parts)
        + "</svg>"
    )
