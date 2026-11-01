import xml.etree.ElementTree as ET

import pytest

from fretboard.render import position_pc, render_fretboard, render_legend
from fretboard.theory import COMPARISONS, STANDARD_TUNING
from fretboard.theory import COMPARISONS_BY_KEY as BY_KEY

NS = "{http://www.w3.org/2000/svg}"
LOW_E, A_STR, D_STR, G_STR, B_STR, HIGH_E = range(6)  # tuning index, low to high


def parse(svg: str) -> ET.Element:
    return ET.fromstring(svg)


def dots(root: ET.Element) -> dict[tuple[int, int], ET.Element]:
    """(string number 1 = high E, fret) -> dot group."""
    return {
        (int(g.get("data-string")), int(g.get("data-fret"))): g
        for g in root.iter(f"{NS}g")
        if g.get("data-state")
    }


# --- 3.1 position mapping -----------------------------------------------------


def test_position_mapping():
    assert position_pc(STANDARD_TUNING, LOW_E, 0) == 4  # E
    assert position_pc(STANDARD_TUNING, A_STR, 3) == 0  # C
    assert position_pc(STANDARD_TUNING, B_STR, 1) == 0  # C
    assert position_pc(STANDARD_TUNING, HIGH_E, 12) == 4  # E


# --- 3.2 fretboard layout -----------------------------------------------------


def test_board_layout():
    root = parse(render_fretboard(BY_KEY["major"]))
    strings = [e for e in root.iter(f"{NS}line") if e.get("class") == "string"]
    assert len(strings) == 6
    frets = [e for e in root.iter(f"{NS}line") if e.get("class") == "fret"]
    assert len(frets) == 15
    inlays = [g for g in root.iter(f"{NS}g") if "inlay" in (g.get("class") or "")]
    assert sorted(int(g.get("data-fret")) for g in inlays) == [3, 5, 7, 9, 12, 15]
    double = next(g for g in inlays if g.get("data-fret") == "12")
    assert len(list(double.iter(f"{NS}circle"))) == 2
    numbers = [e.text for e in root.iter(f"{NS}text") if e.get("class") == "fret-number"]
    assert numbers == [str(f) for f in range(16)]


def test_high_e_on_top():
    d = dots(parse(render_fretboard(BY_KEY["major"])))
    # String 1 (top) is high E: fret 1 is F. String 6 (bottom) is low E: fret 3 is G.
    assert d[(1, 1)].get("data-label") == "4"
    assert d[(6, 3)].get("data-label") == "5"
    assert d[(1, 0)].get("data-label") == d[(6, 0)].get("data-label") == "3"


# --- 3.3 dots -----------------------------------------------------------------


@pytest.mark.parametrize("comparison", COMPARISONS, ids=lambda c: c.key)
def test_svg_is_well_formed(comparison):
    parse(render_fretboard(comparison, "notes"))


def test_major_alone_dots():
    d = dots(parse(render_fretboard(BY_KEY["major"])))
    assert {g.get("data-state") for g in d.values()} == {"shared"}
    # 7 of 12 pitch classes, 13 frets per string -> no dot on C# (A string fret 4).
    assert (5, 4) not in d
    assert d[(5, 3)].get("class") == "dot dot-root"  # C on the A string
    assert d[(2, 1)].get("class") == "dot dot-root"  # C on the B string


def moves(root: ET.Element) -> set[tuple[int, int, int]]:
    """(string number, from fret, to fret) for every arrow."""
    return {
        (int(g.get("data-string")), int(g.get("data-from")), int(g.get("data-to")))
        for g in root.iter(f"{NS}g")
        if g.get("class") == "move"
    }


def test_dorian_has_no_dots_on_dropped_notes():
    E, B = 4, 11
    d = dots(parse(render_fretboard(BY_KEY["dorian"])))
    assert {g.get("data-state") for g in d.values()} == {"shared", "altered"}
    for (string, fret), g in d.items():
        pc = position_pc(STANDARD_TUNING, 6 - string, fret)
        assert pc not in (E, B), f"note dot on dropped note at string {string} fret {fret}"


def test_dorian_arrow_on_b_string():
    root = parse(render_fretboard(BY_KEY["dorian"]))
    d = dots(root)
    assert (2, 5) not in d
    assert d[(2, 4)].get("data-state") == "altered" and d[(2, 4)].get("data-label") == "b3"
    assert (2, 5, 4) in moves(root)


def test_lydian_arrow_points_away_from_nut():
    root = parse(render_fretboard(BY_KEY["lydian"]))
    assert (1, 1, 2) in moves(root)
    assert dots(root)[(1, 2)].get("data-label") == "#4"


def test_no_arrow_when_target_is_off_the_board():
    root = parse(render_fretboard(BY_KEY["dorian"]))
    d, m = dots(root), moves(root)
    for string in (1, 6):  # open E strings: b3 would be at fret -1
        assert (string, 0) not in d
        assert not any(s == string and start == 0 for s, start, _ in m)
    # the same degree still shows an arrow at the octave
    assert (6, 12, 11) in m


def test_every_arrow_ends_on_an_altered_dot():
    for comparison in COMPARISONS:
        root = parse(render_fretboard(comparison))
        d = dots(root)
        for string, start, end in moves(root):
            assert abs(end - start) == 1
            assert d[(string, end)].get("data-state") == "altered"


def test_major_alone_has_no_arrows():
    assert moves(parse(render_fretboard(BY_KEY["major"]))) == set()


def test_arrows_independent_of_label_mode():
    for comparison in COMPARISONS:
        degrees = moves(parse(render_fretboard(comparison, "degrees")))
        notes = moves(parse(render_fretboard(comparison, "notes")))
        assert degrees == notes


def test_note_name_labels():
    d = dots(parse(render_fretboard(BY_KEY["dorian"], "notes")))
    assert d[(2, 4)].get("data-label") == "Eb"
    assert d[(2, 6)].get("data-label") == "F"
    lydian = dots(parse(render_fretboard(BY_KEY["lydian"], "notes")))
    assert lydian[(1, 2)].get("data-label") == "F#"  # high E fret 2


def test_altered_style_not_colour_only():
    root = parse(render_fretboard(BY_KEY["aeolian"]))
    altered = [g for g in root.iter(f"{NS}g") if g.get("data-state") == "altered"]
    shared = [g for g in root.iter(f"{NS}g") if g.get("class") == "dot dot-shared"]
    a_circle = altered[0].find(f"{NS}circle")
    s_circle = shared[0].find(f"{NS}circle")
    assert float(a_circle.get("stroke-width")) > float(s_circle.get("stroke-width"))
    assert {g.get("data-label") for g in altered} == {"b3", "b6", "b7"}


# --- 3.4 legend ---------------------------------------------------------------


def legend_styles(comparison):
    root = parse(render_legend(comparison))
    return [g.get("data-style") for g in root.iter(f"{NS}g") if g.get("class") == "legend-entry"]


def test_legend_major_alone():
    assert legend_styles(BY_KEY["major"]) == ["root", "shared"]


def test_legend_dorian():
    assert legend_styles(BY_KEY["dorian"]) == ["root", "shared", "altered", "moved"]


# --- triad shapes (add-triad-inversions) --------------------------------------

from fretboard.render import INVERSION_COLORS, SHARED_SHAPE_OUTLINE  # noqa: E402
from fretboard.theory import triads  # noqa: E402

C_MAJOR = triads(BY_KEY["major"])[0]


def test_no_chord_means_unchanged_svg():
    plain = render_fretboard(BY_KEY["dorian"])
    assert render_fretboard(BY_KEY["dorian"], chord=None) == plain
    assert "chord-shapes" not in plain and 'class="scale"' not in plain


def test_chord_fades_scale_and_draws_shapes():
    root = parse(render_fretboard(BY_KEY["major"], chord=C_MAJOR, string_set="3-2-1"))
    scale = [g for g in root.iter(f"{NS}g") if g.get("class") == "scale"]
    assert len(scale) == 1 and float(scale[0].get("opacity")) < 0.5
    lines = [e for e in root.iter(f"{NS}polyline") if e.get("class") == "shape-line"]
    assert len(lines) == 4  # 2nd inversion at frets 0 and 12, root, 1st
    assert {(e.get("data-inversion"), e.get("stroke")) for e in lines} == set(INVERSION_COLORS.items())
    shape_dots = {(int(g.get("data-string")), int(g.get("data-fret"))): g
                  for g in root.iter(f"{NS}g") if g.get("class") == "shape-dot"}
    assert len(shape_dots) == 12
    assert shape_dots[(2, 1)].get("data-tone") == "R"  # C on the B string, 2nd inversion (0,1,0)
    assert shape_dots[(2, 1)].find(f"{NS}circle").get("fill") == "#1f2937"


def test_all_string_sets_shared_dot_is_neutral():
    root = parse(render_fretboard(BY_KEY["major"], chord=C_MAJOR, string_set="all"))
    shape_dots = {(int(g.get("data-string")), int(g.get("data-fret"))): g
                  for g in root.iter(f"{NS}g") if g.get("class") == "shape-dot"}
    open_g = shape_dots[(3, 0)]
    assert open_g.get("data-inversions") == "1st 2nd root"
    assert open_g.find(f"{NS}circle").get("stroke") == SHARED_SHAPE_OUTLINE
    lines = [e for e in root.iter(f"{NS}polyline") if e.get("class") == "shape-line"]
    assert len(lines) == 16


def test_inversion_legend():
    from fretboard.render import render_inversion_legend

    dm = triads(BY_KEY["major"])[1]
    svg = render_inversion_legend(dm)
    root = parse(svg)
    assert "Dm:" in "".join(root.itertext())
    strokes = {e.get("stroke") for e in root.iter(f"{NS}line")}
    assert strokes == set(INVERSION_COLORS.values())
    # Natural size, not 100%: in the app it sits in a flex row where 100% would shrink it.
    assert root.get("width") == root.get("viewBox").split()[2]
    assert root.get("height") == root.get("viewBox").split()[3]


# --- 15-fret neck (extend-neck-to-15-frets) ------------------------------------


def test_default_neck_has_15_frets():
    from fretboard.render import DEFAULT_FRETS

    assert DEFAULT_FRETS == 15
    d = dots(parse(render_fretboard(BY_KEY["major"])))
    assert d[(6, 13)].get("data-label") == "4"  # F
    assert d[(6, 15)].get("data-label") == "5"  # G
    assert (6, 14) not in d  # F#


def test_dorian_arrow_above_fret_12():
    assert (5, 14, 13) in moves(parse(render_fretboard(BY_KEY["dorian"])))


def test_f_major_root_position_on_6_5_4():
    f_major = triads(BY_KEY["major"])[3]
    root = parse(render_fretboard(BY_KEY["major"], chord=f_major, string_set="6-5-4"))
    shape = {(int(g.get("data-string")), int(g.get("data-fret"))): g.get("data-inversions")
             for g in root.iter(f"{NS}g") if g.get("class") == "shape-dot"}
    assert shape[(6, 13)] == shape[(5, 12)] == shape[(4, 10)] == "root"
