## MODIFIED Requirements

### Requirement: Dropped notes are shown as arrows
For every dropped note position (frets 0-15) where the altered note lies one fret away on the same string within frets 0-15, the system SHALL draw a straight arrow along the string. The arrow SHALL start with a small start dot at the dropped position and end with an arrowhead at the edge of the altered note. The start dot SHALL be clearly smaller than a note dot and carry no label. No note dot SHALL be drawn at a dropped position. If the altered note would fall outside frets 0-15, nothing SHALL be drawn at that dropped position.

#### Scenario: Flat arrow points towards the nut
- **WHEN** C Dorian is selected
- **THEN** on the B string, an arrow runs from a start dot at fret 5 to the altered `b3` dot at fret 4, and no note dot is drawn at fret 5

#### Scenario: Sharp arrow points away from the nut
- **WHEN** C Lydian is selected
- **THEN** on the high E string, an arrow runs from a start dot at fret 1 to the altered `#4` dot at fret 2

#### Scenario: Altered note outside the fretboard
- **WHEN** C Dorian is selected
- **THEN** the open low E string (fret 0) shows neither a note dot nor an arrow, because its b3 would be at fret -1

#### Scenario: Arrow independent of label mode
- **WHEN** C Dorian is selected with note-name labels
- **THEN** the same arrows are drawn as with degree labels

#### Scenario: Arrows above fret 12
- **WHEN** C Dorian is selected
- **THEN** on the A string (string 5), an arrow runs from a start dot at fret 14 (B) to the altered `b7` dot at fret 13 (Bb)
