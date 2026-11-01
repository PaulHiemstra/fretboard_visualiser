import xml.etree.ElementTree as ET

from fretboard.render import render_chord_table
from fretboard.theory import COMPARISONS
from fretboard.theory import COMPARISONS_BY_KEY as BY_KEY

ARROW = "→"


def parse(key):
    return ET.fromstring(render_chord_table(BY_KEY[key]))


def rows(table):
    return table.findall("./tbody/tr")


def cell(row, cls):
    return next((td for td in row.findall("td") if td.get("class") == cls), None)


def text(el):
    return "".join(el.itertext()) if el is not None else None


def test_well_formed_for_all_options():
    for c in COMPARISONS:
        ET.fromstring(render_chord_table(c))


def test_major_alone_single_column():
    t = parse("major")
    assert [text(th) for th in t.findall("./thead/tr/th")] == ["Degree", "C major"]
    r = rows(t)
    assert len(r) == 7
    assert [text(cell(row, "major")) for row in r][:3] == ["CI", "Dmii", "Emiii"]
    assert all(cell(row, "arrow") is None and cell(row, "why") is None for row in r)
    assert all(row.get("data-changed") == "false" for row in r)


def test_dorian_columns_and_arrows():
    t = parse("dorian")
    assert [text(th) for th in t.findall("./thead/tr/th")] == ["Degree", "C major", "", "C Dorian", "Why"]
    arrows = [int(row.get("data-degree")) for row in rows(t) if text(cell(row, "arrow")) == ARROW]
    assert arrows == [1, 3, 5, 6, 7]
    r = rows(t)
    assert text(cell(r[0], "major")) == "CI" and text(cell(r[0], "mode")) == "Cmi"
    assert text(cell(r[2], "why")) == f"E {ARROW} Eb, B {ARROW} Bb"
    assert text(cell(r[4], "why")) == f"B {ARROW} Bb"
    assert text(cell(r[1], "why")) == "" and text(cell(r[3], "arrow")) == ""


def changed(key):
    return [int(row.get("data-degree")) for row in rows(parse(key)) if row.get("data-changed") == "true"]


def test_highlighting():
    assert changed("mixolydian") == [3, 5, 7]
    assert changed("aeolian") == [1, 2, 3, 4, 5, 6, 7]
    t = parse("mixolydian")
    styles = {int(r.get("data-degree")): r.get("style") for r in rows(t)}
    assert "background" in styles[3]
    assert "background" not in styles[1]
    degree_cells = {int(r.get("data-degree")): cell(r, "degree").get("style") for r in rows(t)}
    assert "solid #9a3412" in degree_cells[3]  # marker that does not rely on fill colour
    assert "solid transparent" in degree_cells[1]


# --- selectable chords (add-triad-inversions) ---------------------------------


def chord_cells(table):
    return [td for row in rows(table) for td in row.findall("td") if td.get("data-column")]


def test_every_chord_cell_is_clickable():
    for key in ("major", "dorian"):
        cells = chord_cells(parse(key))
        assert len(cells) == (7 if key == "major" else 14)
        for td in cells:
            col, deg = td.get("data-column"), td.get("data-degree")
            assert td.get("onclick") == f"emitEvent('chord_click', {{column: '{col}', degree: {deg}}})"


def test_only_selected_cell_is_framed():
    t = ET.fromstring(render_chord_table(BY_KEY["dorian"], selected=("mode", 3)))
    framed = [(td.get("data-column"), td.get("data-degree")) for td in chord_cells(t)
              if td.get("data-selected") == "true"]
    assert framed == [("mode", "3")]
    assert "outline:2px solid" in next(td for td in chord_cells(t) if td.get("data-selected") == "true").get("style")
    assert all("outline" not in td.get("style") for td in chord_cells(t) if td.get("data-selected") == "false")
