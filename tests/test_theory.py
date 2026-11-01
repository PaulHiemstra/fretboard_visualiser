import pytest

from fretboard.theory import (
    COMPARISONS,
    MAJOR,
    STANDARD_TUNING,
    State,
    classify,
    note_name,
)
from fretboard.theory import COMPARISONS_BY_KEY as BY_KEY

C, Db, D, Eb, E, F, Fs, G, Ab, A, Bb, B = range(12)


# --- 2.1 data -----------------------------------------------------------------


def test_major_degrees():
    assert MAJOR == {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def test_standard_tuning():
    assert STANDARD_TUNING == (40, 45, 50, 55, 59, 64)


def test_comparison_order_and_alterations_match_spec():
    expected = [
        ("major", {}),
        ("lydian", {4: 1}),
        ("mixolydian", {7: -1}),
        ("dorian", {3: -1, 7: -1}),
        ("aeolian", {3: -1, 6: -1, 7: -1}),
        ("phrygian", {2: -1, 3: -1, 6: -1, 7: -1}),
        ("locrian", {2: -1, 3: -1, 5: -1, 6: -1, 7: -1}),
    ]
    assert [(c.key, c.alterations) for c in COMPARISONS] == expected


def test_labels_show_alterations():
    assert BY_KEY["major"].label == "C major alone"
    assert BY_KEY["dorian"].label == "Dorian (b3 b7)"
    assert BY_KEY["lydian"].label == "Lydian (#4)"
    assert "natural minor" in BY_KEY["aeolian"].label


# --- 2.2 classification -------------------------------------------------------


def states(key):
    return {pc: info.state for pc, info in classify(BY_KEY[key]).items()}


def test_major_alone_is_all_shared():
    result = classify(BY_KEY["major"])
    assert set(result) == {C, D, E, F, G, A, B}
    assert all(info.state is State.SHARED for info in result.values())
    assert [result[pc].degree_label for pc in (C, D, E, F, G, A, B)] == list("1234567")


def test_dorian_classification():
    s = states("dorian")
    assert {pc for pc, st in s.items() if st is State.SHARED} == {C, D, F, G, A}
    assert {pc for pc, st in s.items() if st is State.DROPPED} == {E, B}
    assert {pc for pc, st in s.items() if st is State.ALTERED} == {Eb, Bb}
    result = classify(BY_KEY["dorian"])
    assert result[Eb].degree_label == "b3"
    assert result[Bb].degree_label == "b7"
    assert result[E].degree_label == "3"


def test_lydian_classification():
    s = states("lydian")
    assert s[F] is State.DROPPED
    assert s[Fs] is State.ALTERED
    assert classify(BY_KEY["lydian"])[Fs].degree_label == "#4"
    assert {pc for pc, st in s.items() if st is State.SHARED} == {C, D, E, G, A, B}


@pytest.mark.parametrize("comparison", COMPARISONS, ids=lambda c: c.key)
def test_root_always_shared(comparison):
    assert classify(comparison)[C].state is State.SHARED


def test_phrygian_adds_b2():
    s = states("phrygian")
    assert s[D] is State.DROPPED
    assert s[Db] is State.ALTERED


# --- 2.3 spelling -------------------------------------------------------------


@pytest.mark.parametrize(
    "degree, alteration, expected",
    [(3, -1, "Eb"), (7, -1, "Bb"), (4, 1, "F#"), (5, -1, "Gb"), (2, -1, "Db"), (1, 0, "C")],
)
def test_note_name_spelling(degree, alteration, expected):
    assert note_name(degree, alteration) == expected
