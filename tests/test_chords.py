import pytest

from fretboard.theory import COMPARISONS, Triad, triads
from fretboard.theory import COMPARISONS_BY_KEY as BY_KEY


def names(key):
    return [t.name for t in triads(BY_KEY[key])]


def numerals(key):
    return [t.numeral for t in triads(BY_KEY[key])]


# --- 1.1 triads ---------------------------------------------------------------


def test_c_major_triads():
    assert names("major") == ["C", "Dm", "Em", "F", "G", "Am", "Bdim"]


def test_dorian_triads():
    assert names("dorian") == ["Cm", "Dm", "Eb", "F", "Gm", "Adim", "Bb"]


def test_lydian_triads():
    assert names("lydian") == ["C", "D", "Em", "F#dim", "G", "Am", "Bm"]


@pytest.mark.parametrize("comparison", COMPARISONS, ids=lambda c: c.key)
def test_all_modes_build(comparison):
    result = triads(comparison)
    assert [t.degree for t in result] == list(range(1, 8))
    assert all(t.quality in {"major", "minor", "diminished"} for t in result)


def test_unknown_quality_raises():
    weird = Triad(1, ((1, 0), (3, -1), (5, 1)))  # C Eb G#: no triad quality
    with pytest.raises(ValueError):
        weird.name


# --- 1.2 labels and why -------------------------------------------------------


def test_c_major_numerals():
    assert numerals("major") == ["I", "ii", "iii", "IV", "V", "vi", "vii°"]


def test_altered_root_numerals():
    t = triads(BY_KEY["dorian"])
    assert (t[2].name, t[2].numeral) == ("Eb", "bIII")
    assert (t[6].name, t[6].numeral) == ("Bb", "bVII")


def test_sharp_root_numeral():
    t = triads(BY_KEY["lydian"])
    assert (t[3].name, t[3].numeral) == ("F#dim", "#iv°")


def test_why_entries():
    t = triads(BY_KEY["dorian"])
    assert t[2].altered_notes == [("E", "Eb"), ("B", "Bb")]
    assert t[4].altered_notes == [("B", "Bb")]
    assert t[0].altered_notes == [("E", "Eb")]  # root stays C, third changes


def test_changed_rows():
    assert [t.changed for t in triads(BY_KEY["dorian"])] == [True, False, True, False, True, True, True]
    assert [t.degree for t in triads(BY_KEY["mixolydian"]) if t.changed] == [3, 5, 7]
    assert all(t.changed for t in triads(BY_KEY["aeolian"]))
    assert not any(t.changed for t in triads(BY_KEY["major"]))
