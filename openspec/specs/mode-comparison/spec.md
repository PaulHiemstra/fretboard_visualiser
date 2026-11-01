# mode-comparison Specification

## Purpose

Lets a learner see each C mode as a set of alterations of the C major scale, by overlaying the mode on the C major reference and marking which notes stay, which drop out and which replace them.

## Requirements

### Requirement: C major reference
The system SHALL always use C major (C D E F G A B, degrees 1-7) as the reference scale.

#### Scenario: Reference is fixed
- **WHEN** any comparison option is selected
- **THEN** the comparison is made against C major

### Requirement: Comparison options
The system SHALL offer exactly these comparison options, in this order, ordered from brightest to darkest. Each mode is defined by its alterations of the major degrees:

| Option | Alterations |
|---|---|
| C major alone | none (no comparison) |
| C Lydian | #4 |
| C Mixolydian | b7 |
| C Dorian | b3, b7 |
| C Aeolian (natural minor) | b3, b6, b7 |
| C Phrygian | b2, b3, b6, b7 |
| C Locrian | b2, b3, b5, b6, b7 |

Each option SHALL show its alterations next to its name (for example "Dorian (b3 b7)"). The default selection SHALL be C major alone.

#### Scenario: Default selection
- **WHEN** the user opens the app
- **THEN** C major alone is selected

#### Scenario: Option order
- **WHEN** the user opens the comparison selector
- **THEN** the options appear in the order of the table above

#### Scenario: Natural minor is identifiable
- **WHEN** the user looks for the natural minor scale
- **THEN** the Aeolian option is also labelled "natural minor"

### Requirement: C major alone view
When C major alone is selected, the system SHALL show every C major note as a shared-style dot (root in root style), with no dropped or altered dots.

#### Scenario: Only major notes
- **WHEN** C major alone is selected
- **THEN** dots appear only on C, D, E, F, G, A and B positions, all in shared or root style

### Requirement: Note classification
When a mode is selected, the system SHALL classify each pitch as follows:
- **shared**: in both C major and the mode; labelled with its degree (for example `5`).
- **dropped**: in C major but altered by the mode; labelled with its major degree (for example `3`).
- **altered**: the mode's replacement for a dropped degree; labelled with the altered degree (for example `b3`).

Pitches in neither scale SHALL not be shown.

#### Scenario: Dorian classification
- **WHEN** C Dorian is selected
- **THEN** C, D, F, G and A are shared; E and B are dropped; Eb (b3) and Bb (b7) are altered

#### Scenario: Lydian classification
- **WHEN** C Lydian is selected
- **THEN** F is dropped and F# (#4) is altered; all other C major notes are shared

#### Scenario: Root is always shared
- **WHEN** any mode is selected
- **THEN** C is classified as shared and drawn in root style

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

### Requirement: Altered notes are highlighted
The system SHALL draw altered notes in a highlight style that is distinct from shared and root styles, and that does not rely on colour alone (for example by also using a different outline or shape).

#### Scenario: Altered style distinct
- **WHEN** C Aeolian is selected
- **THEN** the Eb, Ab and Bb dots are drawn in the altered style and can be told apart from shared dots without relying on colour

### Requirement: Live update
The system SHALL update the fretboard immediately when the user changes the comparison option or the label mode, without reloading the page.

#### Scenario: Switching modes
- **WHEN** the user changes the selection from Dorian to Phrygian
- **THEN** the fretboard updates to show D as dropped and Db (b2) as altered, in addition to the Dorian alterations
