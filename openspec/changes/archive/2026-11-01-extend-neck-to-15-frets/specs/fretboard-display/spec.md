## MODIFIED Requirements

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
