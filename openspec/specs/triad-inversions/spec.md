# triad-inversions Specification

## Purpose

Shows where a selected triad can be played: every compact three-string shape of the chord on the chosen string set, coloured by inversion and connected by lines, on top of a faded scale.

## Requirements

### Requirement: Playable triad shapes
For a selected triad, the system SHALL find every shape on the displayed frets that meets all of these rules:
- three notes on three neighbouring strings, one note per string;
- the three notes are the chord's root, 3rd and 5th, each used once;
- pitch rises from the lowest to the highest string, and the highest note is less than an octave above the lowest (close position);
- the fretted notes (fret > 0) span at most 4 frets between the lowest and highest fret, which is 5 fret positions. Open strings do not count towards the span.

#### Scenario: C major on strings 3-2-1
- **WHEN** C major is selected with string set 3-2-1 on frets 0-12
- **THEN** exactly these shapes are shown: frets (0, 1, 0), (5, 5, 3) and (9, 8, 8) on strings 3, 2, 1

#### Scenario: C major on strings 5-4-3
- **WHEN** C major is selected with string set 5-4-3 on frets 0-12
- **THEN** exactly these shapes are shown: frets (3, 2, 0), (7, 5, 5) and (10, 10, 9) on strings 5, 4, 3

#### Scenario: Five-fret stretch allowed
- **WHEN** Bdim (C major, degree 7) is selected with string set 6-5-4
- **THEN** the root-position shape at frets (7, 5, 3) is shown

#### Scenario: Six-fret stretch not allowed
- **WHEN** any chord is selected
- **THEN** no shape is shown whose fretted notes span more than 4 frets

### Requirement: Inversion classification
Each shape SHALL be classified by its lowest note: root position (root in the bass), 1st inversion (3rd in the bass) or 2nd inversion (5th in the bass).

#### Scenario: Inversions of C major on strings 3-2-1
- **WHEN** C major is selected with string set 3-2-1
- **THEN** (0, 1, 0) is 2nd inversion, (5, 5, 3) is root position and (9, 8, 8) is 1st inversion

### Requirement: Shape drawing
Each shape SHALL be drawn as three note dots connected by a line from the lowest to the highest string, both in the colour of its inversion: root position, 1st inversion and 2nd inversion each have a distinct colour that stays distinguishable for colour-blind viewers. The dots SHALL be labelled with chord tones: `R` for the root, `3` or `b3` for the third and `5`, `b5` or `#5` for the fifth. The root dot SHALL keep the dark root fill.

#### Scenario: Labels for a minor chord
- **WHEN** Cm (C Dorian, degree 1) is selected
- **THEN** the shape dots are labelled `R`, `b3` and `5`

#### Scenario: Line per shape
- **WHEN** a chord is selected with a single string set
- **THEN** each shape has exactly one line, through its three notes, in its inversion colour

### Requirement: String-set selection
The system SHALL offer a string-set choice of 6-5-4, 5-4-3, 4-3-2, 3-2-1 and all, with 3-2-1 as the default. Only shapes on the chosen string set SHALL be drawn. "All" draws the shapes of all four string sets. A note dot that belongs to shapes of different inversions SHALL be drawn with a neutral outline instead of an inversion colour.

#### Scenario: Default string set
- **WHEN** the user selects a chord without changing the string set
- **THEN** only shapes on strings 3-2-1 are drawn

#### Scenario: All string sets with a shared note
- **WHEN** C major is selected with string set "all"
- **THEN** the open G string (string 3, fret 0) belongs to a root-position shape on 5-4-3, a 1st-inversion shape on 4-3-2 and a 2nd-inversion shape on 3-2-1, and is drawn with a neutral outline

### Requirement: Faded scale while a chord is shown
While a chord is selected, the system SHALL keep the scale dots and arrows visible but clearly faded, and draw the chord shapes on top of them at full strength. When no chord is selected, the fretboard SHALL look exactly as without this feature.

#### Scenario: Fade on selection
- **WHEN** the user selects a chord
- **THEN** the scale dots and arrows are faded and the chord shapes are drawn on top

#### Scenario: No selection
- **WHEN** no chord is selected
- **THEN** no shapes are drawn and the scale is not faded

### Requirement: Inversion legend
While a chord is selected, the system SHALL show a legend naming the selected chord and the colours of root position, 1st inversion and 2nd inversion.

#### Scenario: Legend on selection
- **WHEN** the user selects Dm
- **THEN** a legend shows "Dm" and the three inversion colours

#### Scenario: Legend hidden
- **WHEN** no chord is selected
- **THEN** no inversion legend is shown
