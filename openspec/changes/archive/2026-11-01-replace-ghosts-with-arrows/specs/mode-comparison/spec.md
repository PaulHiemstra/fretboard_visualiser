## ADDED Requirements

### Requirement: Dropped notes are shown as arrows
For every dropped note position (frets 0-12) where the altered note lies one fret away on the same string within frets 0-12, the system SHALL draw a straight arrow along the string. The arrow SHALL start with a small start dot at the dropped position and end with an arrowhead at the edge of the altered note. The start dot SHALL be clearly smaller than a note dot and carry no label. No note dot SHALL be drawn at a dropped position. If the altered note would fall outside frets 0-12, nothing SHALL be drawn at that dropped position.

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

## MODIFIED Requirements

### Requirement: Altered notes are highlighted
The system SHALL draw altered notes in a highlight style that is distinct from shared and root styles, and that does not rely on colour alone (for example by also using a different outline or shape).

#### Scenario: Altered style distinct
- **WHEN** C Aeolian is selected
- **THEN** the Eb, Ab and Bb dots are drawn in the altered style and can be told apart from shared dots without relying on colour

## REMOVED Requirements

### Requirement: Dropped notes are shown as ghosts
**Reason**: Ghost dots next to every altered note clutter the fretboard. They are replaced by arrows that show the same information, and the direction of the move, with less ink.
**Migration**: See "Dropped notes are shown as arrows". Dropped positions now show the start dot of an arrow instead of a labelled ghost dot.
