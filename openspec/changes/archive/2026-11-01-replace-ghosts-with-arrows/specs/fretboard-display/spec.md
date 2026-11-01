## MODIFIED Requirements

### Requirement: Note dots at scale positions
The system SHALL draw a labelled note dot at every string/fret position (frets 0-12) whose pitch is shared or altered. Dropped positions SHALL have no note dot. They are marked by arrows (see the mode-comparison capability). Positions whose pitch is in neither the reference scale nor the comparison scale SHALL have no dot.

#### Scenario: Non-scale positions are empty
- **WHEN** C major alone is displayed
- **THEN** a position whose pitch is C#, D#, F#, G# or A# has no dot

#### Scenario: Open-string notes
- **WHEN** C major alone is displayed
- **THEN** the open low E string (fret 0) shows a dot for E

#### Scenario: Dropped positions have no note dot
- **WHEN** C Dorian is selected
- **THEN** no note dot is drawn on any E or B position

### Requirement: Legend
The system SHALL display a legend explaining the root, shared and altered dot styles and the arrow from a dropped C major note to its altered note. Entries that do not apply to the current selection MAY be hidden.

#### Scenario: Legend present
- **WHEN** a mode other than C major alone is selected
- **THEN** the legend shows the shared and altered styles and an arrow entry

#### Scenario: Legend for C major alone
- **WHEN** C major alone is selected
- **THEN** the legend shows no arrow or altered entry
