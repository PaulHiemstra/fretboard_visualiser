# fretboard-display Specification

## Purpose

Draws a guitar fretboard and places labelled note dots on it so a learner can see where scale notes are located across the neck.

## Requirements

### Requirement: Standard-tuning fretboard layout
The system SHALL display a 6-string guitar fretboard in standard tuning (E2 A2 D3 G3 B3 E4), with frets 0 (open strings) through 15. The high E string SHALL be at the top and the low E string at the bottom, with fret numbers increasing from left to right.

#### Scenario: Fretboard is shown on page load
- **WHEN** the user opens the app
- **THEN** a fretboard with 6 strings and fret positions 0 through 15 is displayed

#### Scenario: String order
- **WHEN** the fretboard is displayed
- **THEN** the top string is high E (E4) and the bottom string is low E (E2)

### Requirement: Fret position markers
The system SHALL show inlay markers at frets 3, 5, 7, 9 and 15, and a double marker at fret 12. Fret numbers SHALL be visible.

#### Scenario: Inlay markers
- **WHEN** the fretboard is displayed
- **THEN** single markers appear at frets 3, 5, 7, 9 and 15 and a double marker appears at fret 12

### Requirement: Note dots at scale positions
The system SHALL draw a labelled note dot at every string/fret position (frets 0-15) whose pitch is shared or altered. Dropped positions SHALL have no note dot. They are marked by arrows (see the mode-comparison capability). Positions whose pitch is in neither the reference scale nor the comparison scale SHALL have no dot.

#### Scenario: Non-scale positions are empty
- **WHEN** C major alone is displayed
- **THEN** a position whose pitch is C#, D#, F#, G# or A# has no dot

#### Scenario: Open-string notes
- **WHEN** C major alone is displayed
- **THEN** the open low E string (fret 0) shows a dot for E

#### Scenario: Dropped positions have no note dot
- **WHEN** C Dorian is selected
- **THEN** no note dot is drawn on any E or B position

#### Scenario: Notes above fret 12
- **WHEN** C major alone is displayed
- **THEN** the low E string shows dots at frets 13 (F) and 15 (G), and none at fret 14 (F#)

### Requirement: Root emphasis
The system SHALL draw dots whose pitch is the root (C) so that they are visually distinct from other dots.

#### Scenario: Root dots stand out
- **WHEN** any comparison option is displayed
- **THEN** every C position (for example A string fret 3, B string fret 1) is drawn in the root style

### Requirement: Switchable labels
The system SHALL label each dot with either its scale degree or its note name, selected by the user. Scale degrees SHALL be the default. Degree labels SHALL use `b` and `#` prefixes (for example `b3`, `#4`). Note names SHALL be spelled from the degree, so a flattened degree uses a flat name and a sharpened degree uses a sharp name (for example b3 = Eb, #4 = F#).

#### Scenario: Default degree labels
- **WHEN** the user opens the app
- **THEN** the dots are labelled with scale degrees (for example `1` on C, `3` on E)

#### Scenario: Switch to note names
- **WHEN** the user selects note-name labels with Dorian selected
- **THEN** the altered third is labelled `Eb` and the altered seventh is labelled `Bb`

#### Scenario: Sharp spelling for raised degrees
- **WHEN** the user selects note-name labels with Lydian selected
- **THEN** the altered fourth is labelled `F#`, not `Gb`

### Requirement: Legend
The system SHALL display a legend explaining the root, shared and altered dot styles and the arrow from a dropped C major note to its altered note. Entries that do not apply to the current selection MAY be hidden.

#### Scenario: Legend present
- **WHEN** a mode other than C major alone is selected
- **THEN** the legend shows the shared and altered styles and an arrow entry

#### Scenario: Legend for C major alone
- **WHEN** C major alone is selected
- **THEN** the legend shows no arrow or altered entry
