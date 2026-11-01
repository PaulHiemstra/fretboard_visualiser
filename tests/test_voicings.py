import pytest

from fretboard.theory import COMPARISONS, STANDARD_TUNING, chord_tone_labels, triads, voicings
from fretboard.theory import COMPARISONS_BY_KEY as BY_KEY

S654, S543, S432, S321 = (0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)
ALL = [S654, S543, S432, S321]


def shapes(key, degree, string_set, frets=12):
    t = triads(BY_KEY[key])[degree - 1]
    return [(v.frets, v.inversion) for v in voicings(t, STANDARD_TUNING, frets, [string_set])]


def test_c_major_on_3_2_1():
    assert shapes("major", 1, S321) == [((0, 1, 0), "2nd"), ((5, 5, 3), "root"), ((9, 8, 8), "1st")]


def test_c_major_on_5_4_3():
    assert shapes("major", 1, S543) == [((3, 2, 0), "root"), ((7, 5, 5), "1st"), ((10, 10, 9), "2nd")]


def test_five_fret_stretch_allowed():
    assert ((7, 5, 3), "root") in shapes("major", 7, S654)  # Bdim


def test_cm_labels():
    cm = triads(BY_KEY["dorian"])[0]
    assert set(chord_tone_labels(cm).values()) == {"R", "b3", "5"}
    v = voicings(cm, STANDARD_TUNING, 12, [S321])
    root_pos = next(x for x in v if x.inversion == "root")
    assert root_pos.tones == ("R", "b3", "5")


def test_bdim_labels():
    assert set(chord_tone_labels(triads(BY_KEY["major"])[6]).values()) == {"R", "b3", "b5"}


@pytest.mark.parametrize("comparison", COMPARISONS, ids=lambda c: c.key)
def test_every_shape_obeys_the_rules(comparison):
    for t in triads(comparison):
        for v in voicings(t, STANDARD_TUNING, 12, ALL):
            fretted = [f for f in v.frets if f > 0]
            assert not fretted or max(fretted) - min(fretted) <= 4
            pitches = [STANDARD_TUNING[s] + f for s, f in zip(v.strings, v.frets)]
            assert pitches[0] < pitches[1] < pitches[2] and pitches[2] - pitches[0] < 12
            assert sorted(v.tones) == sorted(chord_tone_labels(t).values())


def test_inversion_follows_bass_note():
    for v in voicings(triads(BY_KEY["major"])[0], STANDARD_TUNING, 12, ALL):
        assert {"root": "R", "1st": "3", "2nd": "5"}[v.inversion] == v.tones[0]
