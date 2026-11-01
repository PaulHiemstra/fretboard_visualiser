"""Music theory for comparing C major with the other C modes.

Pure Python, no UI imports. Pitch classes are integers 0-11 with C = 0.
"""

from dataclasses import dataclass, field
from enum import Enum
from itertools import product

ROOT_PC = 0  # C

# Major scale: degree -> semitones above the root.
MAJOR: dict[int, int] = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}

# Natural letter for each degree of C major. Spelling is only defined for root C.
C_MAJOR_LETTERS: dict[int, str] = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "A", 7: "B"}

# Standard guitar tuning as MIDI note numbers, low string to high string: E2 A2 D3 G3 B3 E4.
STANDARD_TUNING: tuple[int, ...] = (40, 45, 50, 55, 59, 64)


def accidental(alteration: int) -> str:
    """Return the accidental prefix for an alteration in semitones (-1 -> 'b', +1 -> '#')."""
    return "b" * -alteration if alteration < 0 else "#" * alteration


@dataclass(frozen=True)
class Comparison:
    """A scale compared with C major, defined by its alterations of the major degrees."""

    key: str
    name: str
    alterations: dict[int, int] = field(default_factory=dict)

    @property
    def is_reference_only(self) -> bool:
        return not self.alterations

    @property
    def alteration_text(self) -> str:
        """For example 'b3 b7'."""
        return " ".join(
            f"{accidental(offset)}{degree}" for degree, offset in sorted(self.alterations.items())
        )

    @property
    def label(self) -> str:
        """Text for the selector, for example 'Dorian (b3 b7)'."""
        if self.is_reference_only:
            return self.name
        return f"{self.name} ({self.alteration_text})"


# Comparison options, ordered brightest to darkest after the reference-only view.
COMPARISONS: tuple[Comparison, ...] = (
    Comparison("major", "C major alone"),
    Comparison("lydian", "Lydian", {4: +1}),
    Comparison("mixolydian", "Mixolydian", {7: -1}),
    Comparison("dorian", "Dorian", {3: -1, 7: -1}),
    Comparison("aeolian", "Aeolian / natural minor", {3: -1, 6: -1, 7: -1}),
    Comparison("phrygian", "Phrygian", {2: -1, 3: -1, 6: -1, 7: -1}),
    Comparison("locrian", "Locrian", {2: -1, 3: -1, 5: -1, 6: -1, 7: -1}),
)

COMPARISONS_BY_KEY: dict[str, Comparison] = {c.key: c for c in COMPARISONS}


class State(Enum):
    SHARED = "shared"  # in C major and in the comparison scale
    DROPPED = "dropped"  # C major note that the comparison scale alters
    ALTERED = "altered"  # the comparison scale's replacement note


@dataclass(frozen=True)
class PitchInfo:
    state: State
    degree: int
    alteration: int = 0

    @property
    def degree_label(self) -> str:
        return f"{accidental(self.alteration)}{self.degree}"

    @property
    def note_name(self) -> str:
        return note_name(self.degree, self.alteration)


def note_name(degree: int, alteration: int = 0) -> str:
    """Spell a degree of C major with an alteration, for example (3, -1) -> 'Eb', (4, +1) -> 'F#'."""
    return f"{C_MAJOR_LETTERS[degree]}{accidental(alteration)}"


def classify(comparison: Comparison) -> dict[int, PitchInfo]:
    """Map each pitch class in C major or the comparison scale to its state.

    Pitch classes in neither scale are absent from the result.
    """
    result: dict[int, PitchInfo] = {}
    for degree, semitones in MAJOR.items():
        pc = (ROOT_PC + semitones) % 12
        offset = comparison.alterations.get(degree, 0)
        if offset == 0:
            result[pc] = PitchInfo(State.SHARED, degree)
        else:
            result[pc] = PitchInfo(State.DROPPED, degree)
            altered_pc = (pc + offset) % 12
            # Diatonic modes never put an altered note on a major pitch (see design.md, decision 3).
            if any(altered_pc == (ROOT_PC + s) % 12 for s in MAJOR.values()):
                raise ValueError(
                    f"{comparison.key}: altered degree {degree} collides with a major pitch"
                )
            result[altered_pc] = PitchInfo(State.ALTERED, degree, offset)
    return result


# --- Chords -------------------------------------------------------------------

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII"}

# (semitones root->3rd, root->5th) -> (quality, name suffix, upper-case numeral, numeral suffix)
TRIAD_QUALITIES: dict[tuple[int, int], tuple[str, str, bool, str]] = {
    (4, 7): ("major", "", True, ""),
    (3, 7): ("minor", "m", False, ""),
    (3, 6): ("diminished", "dim", False, "°"),
    (4, 8): ("augmented", "aug", True, "+"),
}


@dataclass(frozen=True)
class Triad:
    """A triad built on a scale degree; notes are (degree, alteration) pairs: root, 3rd, 5th."""

    degree: int
    notes: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]

    @property
    def root_alteration(self) -> int:
        return self.notes[0][1]

    @property
    def _quality_row(self) -> tuple[str, str, bool, str]:
        root, third, fifth = (MAJOR[d] + a for d, a in self.notes)
        intervals = ((third - root) % 12, (fifth - root) % 12)
        try:
            return TRIAD_QUALITIES[intervals]
        except KeyError:
            raise ValueError(f"no triad quality for intervals {intervals}") from None

    @property
    def quality(self) -> str:
        return self._quality_row[0]

    @property
    def name(self) -> str:
        """For example 'Eb', 'Dm', 'F#dim'."""
        return note_name(self.degree, self.root_alteration) + self._quality_row[1]

    @property
    def numeral(self) -> str:
        """For example 'bIII', 'ii', '#iv°'."""
        _, _, upper, suffix = self._quality_row
        roman = ROMAN[self.degree] if upper else ROMAN[self.degree].lower()
        return f"{accidental(self.root_alteration)}{roman}{suffix}"

    @property
    def altered_notes(self) -> list[tuple[str, str]]:
        """(C major note, altered note) for each altered note, in chord order."""
        return [(note_name(d, 0), note_name(d, a)) for d, a in self.notes if a != 0]

    @property
    def changed(self) -> bool:
        return bool(self.altered_notes)


def triads(comparison: Comparison) -> list[Triad]:
    """The seven diatonic triads of the comparison scale, on degrees 1-7."""
    result = []
    for degree in range(1, 8):
        degrees = (degree, (degree + 1) % 7 + 1, (degree + 3) % 7 + 1)
        notes = tuple((d, comparison.alterations.get(d, 0)) for d in degrees)
        result.append(Triad(degree, notes))  # type: ignore[arg-type]
    return result


# --- Triad shapes on the fretboard ------------------------------------------------

THIRD_LABELS = {3: "b3", 4: "3"}
FIFTH_LABELS = {6: "b5", 7: "5", 8: "#5"}
INVERSIONS = ("root", "1st", "2nd")  # bass note is the root, 3rd or 5th


def chord_tone_labels(triad: Triad) -> dict[int, str]:
    """Pitch class -> chord-tone label ('R', '3'/'b3', '5'/'b5'/'#5')."""
    root, third, fifth = ((MAJOR[d] + a) % 12 for d, a in triad.notes)
    return {
        root: "R",
        third: THIRD_LABELS[(third - root) % 12],
        fifth: FIFTH_LABELS[(fifth - root) % 12],
    }


@dataclass(frozen=True)
class Voicing:
    """A triad shape: one note on each of three neighbouring strings.

    strings are tuning indices (0 = lowest string), low to high; frets match them.
    """

    strings: tuple[int, int, int]
    frets: tuple[int, int, int]
    inversion: str
    tones: tuple[str, str, str]


def voicings(
    triad: Triad,
    tuning: tuple[int, ...],
    frets: int,
    string_sets: list[tuple[int, int, int]],
    max_span: int = 4,
) -> list[Voicing]:
    """All close-position shapes of the triad on the given string sets.

    A shape uses each chord tone once, rises in pitch from the lowest string,
    stays within an octave, and its fretted notes (fret > 0) span at most
    max_span frets.
    """
    chord_pcs = [(MAJOR[d] + a) % 12 for d, a in triad.notes]  # root, 3rd, 5th
    labels = chord_tone_labels(triad)
    result = []
    for strings in string_sets:
        for combo in product(range(frets + 1), repeat=3):
            pitches = [tuning[s] + f for s, f in zip(strings, combo)]
            pcs = [p % 12 for p in pitches]
            if sorted(pcs) != sorted(chord_pcs):
                continue
            if not (pitches[0] < pitches[1] < pitches[2]) or pitches[2] - pitches[0] >= 12:
                continue
            fretted = [f for f in combo if f > 0]
            if fretted and max(fretted) - min(fretted) > max_span:
                continue
            inversion = INVERSIONS[chord_pcs.index(pcs[0])]
            result.append(Voicing(strings, combo, inversion, tuple(labels[pc] for pc in pcs)))
    return result
