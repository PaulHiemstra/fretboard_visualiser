import json
import xml.etree.ElementTree as ET

import pytest
from nicegui import ui
from nicegui.testing import User
from nicegui.testing.user_simulation import user_simulation

from fretboard.app import root

NS = "{http://www.w3.org/2000/svg}"


@pytest.fixture
async def user():
    async with user_simulation(root=root) as u:
        yield u


def board_dots(user: User) -> dict[tuple[int, int], ET.Element]:
    html = next(e for e in user.find(ui.html).elements if "data-fret" in e.content and "nut" in e.content)
    root = ET.fromstring(html.content)
    return {
        (int(g.get("data-string")), int(g.get("data-fret"))): g
        for g in root.iter(f"{NS}g")
        if g.get("data-state")
    }


def board_moves(user: User) -> set[tuple[int, int, int]]:
    html = next(e for e in user.find(ui.html).elements if "data-fret" in e.content and "nut" in e.content)
    root = ET.fromstring(html.content)
    return {
        (int(g.get("data-string")), int(g.get("data-from")), int(g.get("data-to")))
        for g in root.iter(f"{NS}g")
        if g.get("class") == "move"
    }


def controls(user: User) -> tuple[ui.select, ui.toggle]:
    """The comparison select and the degrees/notes label toggle."""
    toggles = user.find(ui.toggle).elements
    label_toggle = next(t for t in toggles if "degrees" in t.options)
    return user.find(ui.select).elements.pop(), label_toggle


def string_set_toggle(user: User) -> ui.toggle:
    # Looked up via the client: user.find() skips hidden elements, and this toggle is hidden without a chord.
    return next(
        e for e in user.client.elements.values() if isinstance(e, ui.toggle) and "3-2-1" in e.options
    )


async def test_page_loads_with_major_alone_and_degrees(user: User) -> None:
    await user.open("/")
    await user.should_see("Compare C major with")
    select, toggle = controls(user)
    assert select.value == "major"
    assert toggle.value == "degrees"
    d = board_dots(user)
    assert {g.get("data-state") for g in d.values()} == {"shared"}
    assert d[(5, 3)].get("data-label") == "1"


async def test_option_labels(user: User) -> None:
    await user.open("/")
    select, _ = controls(user)
    labels = list(select.options.values())
    assert labels[0] == "C major alone"
    assert "Dorian (b3 b7)" in labels
    assert any("natural minor" in label for label in labels)


async def test_controls_update_board(user: User) -> None:
    await user.open("/")
    select, toggle = controls(user)

    select.value = "dorian"
    d = board_dots(user)
    assert d[(2, 4)].get("data-label") == "b3"

    select.value = "phrygian"
    d = board_dots(user)
    assert (3, 7) not in d  # D on the G string is dropped: no note dot
    assert d[(3, 6)].get("data-label") == "b2"  # Db on the G string
    assert (3, 7, 6) in board_moves(user)  # arrow from D to Db

    select.value = "lydian"
    toggle.value = "notes"
    d = board_dots(user)
    assert d[(1, 2)].get("data-label") == "F#"


def chord_table(user: User) -> str:
    return next(e for e in user.find(ui.html).elements if "chord-table" in e.content).content


def changed_degrees(user: User) -> list[int]:
    table = ET.fromstring(chord_table(user))
    return [int(r.get("data-degree")) for r in table.iter("tr") if r.get("data-changed") == "true"]


async def test_chord_table_follows_selection(user: User) -> None:
    await user.open("/")
    select, toggle = controls(user)
    assert changed_degrees(user) == []

    select.value = "dorian"
    assert changed_degrees(user) == [1, 3, 5, 6, 7]

    select.value = "mixolydian"
    assert changed_degrees(user) == [3, 5, 7]

    before = chord_table(user)
    toggle.value = "notes"
    assert chord_table(user) == before



# --- chord selection and triad shapes (add-triad-inversions) -------------------


def click_chord(user: User, column: str, degree: int) -> None:
    """Send the same event the table cell's onclick sends from the browser."""
    layout = user.client.layout
    listener_id = next(lid for lid, lst in layout._event_listeners.items() if lst.type == "chord_click")
    user.client.handle_event(
        {"id": layout.id, "listener_id": listener_id, "args": [json.dumps({"column": column, "degree": degree})]}
    )


def selected_cell(user: User) -> tuple[str, int] | None:
    table = ET.fromstring(chord_table(user))
    for td in table.iter("td"):
        if td.get("data-selected") == "true":
            return td.get("data-column"), int(td.get("data-degree"))
    return None


def chord_controls_visible(user: User) -> bool:
    """The string-set toggle and inversion legend share a row that is hidden without a chord."""
    return string_set_toggle(user).parent_slot.parent.visible


def board_root(user: User) -> ET.Element:
    html = next(e for e in user.find(ui.html).elements if "data-fret" in e.content and "nut" in e.content)
    return ET.fromstring(html.content)


def shape_lines(user: User) -> list[ET.Element]:
    return [e for e in board_root(user).iter(f"{NS}polyline") if e.get("class") == "shape-line"]


def shape_frets(user: User) -> set[tuple[int, int]]:
    return {
        (int(g.get("data-string")), int(g.get("data-fret")))
        for g in board_root(user).iter(f"{NS}g")
        if g.get("class") == "shape-dot"
    }


async def test_select_and_deselect(user: User) -> None:
    await user.open("/")
    assert shape_lines(user) == [] and not chord_controls_visible(user)

    click_chord(user, "major", 2)
    assert selected_cell(user) == ("major", 2)
    assert len(shape_lines(user)) == 4  # Dm on 3-2-1, frets 0-15
    assert chord_controls_visible(user)
    await user.should_see("Dm:")

    click_chord(user, "major", 2)
    assert selected_cell(user) is None
    assert shape_lines(user) == []
    assert not chord_controls_visible(user)


async def test_selection_follows_mode(user: User) -> None:
    await user.open("/")
    select, _ = controls(user)
    select.value = "dorian"
    click_chord(user, "mode", 3)
    await user.should_see("Eb:")

    select.value = "mixolydian"
    assert selected_cell(user) == ("mode", 3)
    await user.should_see("Edim:")


async def test_mode_selection_cleared_on_major_alone(user: User) -> None:
    await user.open("/")
    select, _ = controls(user)
    select.value = "dorian"
    click_chord(user, "mode", 1)
    select.value = "major"
    assert selected_cell(user) is None
    assert shape_lines(user) == []


async def test_major_selection_kept_on_major_alone(user: User) -> None:
    await user.open("/")
    select, _ = controls(user)
    select.value = "dorian"
    click_chord(user, "major", 1)
    select.value = "major"
    assert selected_cell(user) == ("major", 1)
    assert len(shape_lines(user)) == 4  # C on 3-2-1, frets 0-15


async def test_string_set_change_redraws(user: User) -> None:
    await user.open("/")
    click_chord(user, "major", 1)  # C major
    assert shape_frets(user) == {
        (3, 0), (2, 1), (1, 0), (3, 5), (2, 5), (1, 3), (3, 9), (2, 8), (1, 8), (3, 12), (2, 13), (1, 12)
    }

    string_set_toggle(user).value = "5-4-3"
    assert {s for s, _ in shape_frets(user)} == {5, 4, 3}

    string_set_toggle(user).value = "all"
    assert len(shape_lines(user)) == 16
