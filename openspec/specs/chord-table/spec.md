# chord-table Specification

## Purpose

Shows the diatonic triads of C major and of the selected C mode side by side, so a learner sees which chords a mode changes and which altered notes cause each change.

## Requirements

### Requirement: Diatonic triads
The system SHALL build one triad on each scale degree 1-7 by stacking the scale's own 3rd and 5th above that degree (degrees d, d+2, d+4, wrapping around after 7). The chord quality SHALL follow from the intervals above the root: major (4 + 7 semitones), minor (3 + 7), diminished (3 + 6) or augmented (4 + 8).

#### Scenario: C major triads
- **WHEN** the triads of C major are built
- **THEN** they are C, Dm, Em, F, G, Am and Bdim

#### Scenario: Dorian triads
- **WHEN** the triads of C Dorian are built
- **THEN** they are Cm, Dm, Eb, F, Gm, Adim and Bb

#### Scenario: Lydian triads
- **WHEN** the triads of C Lydian are built
- **THEN** they are C, D, Em, F#dim, G, Am and Bm

### Requirement: Chord labels
Each chord SHALL be labelled with its name and its Roman numeral. The name is the root spelled from its degree (as on the fretboard) followed by "" (major), "m" (minor), "dim" (diminished) or "aug" (augmented). The Roman numeral SHALL carry the root's accidental (`b` or `#`), be upper case for major and augmented chords and lower case for minor and diminished chords, and end in `°` (diminished) or `+` (augmented).

#### Scenario: C major numerals
- **WHEN** the C major column is shown
- **THEN** the numerals are I, ii, iii, IV, V, vi and vii°

#### Scenario: Altered roots carry an accidental
- **WHEN** C Dorian is selected
- **THEN** the third-degree chord is labelled `Eb` with numeral `bIII`, and the seventh-degree chord is `Bb` with numeral `bVII`

#### Scenario: Sharp root
- **WHEN** C Lydian is selected
- **THEN** the fourth-degree chord is labelled `F#dim` with numeral `#iv°`

### Requirement: Table for C major alone
When C major alone is selected, the system SHALL show the chord table below the fretboard with one row per degree 1-7 and a single chord column for C major. No arrow column, mode column or why column SHALL be shown.

#### Scenario: Single column
- **WHEN** the user opens the app
- **THEN** the chord table lists the seven C major triads with their numerals and has no comparison columns

### Requirement: Comparison columns
When a mode is selected, the system SHALL show, per degree row: the C major chord, an arrow column, the mode's chord and a why column. The arrow and the why text SHALL appear only on rows where the chord changes. A chord changes when any of its three notes is altered by the mode.

#### Scenario: Dorian changes
- **WHEN** C Dorian is selected
- **THEN** rows 1, 3, 5, 6 and 7 show an arrow, and rows 2 and 4 (Dm and F) show no arrow and no why text

#### Scenario: Chord changes without root change
- **WHEN** C Dorian is selected
- **THEN** row 1 shows `C  I` -> `Cm  i`, because its third is altered while its root stays C

### Requirement: Why column
For each changed chord, the why column SHALL list each altered note of that chord as `<C major note> → <mode note>` (a right-arrow character), in chord order (root, 3rd, 5th), using note names. Multiple entries SHALL be separated by commas.

#### Scenario: Two altered notes
- **WHEN** C Dorian is selected
- **THEN** row 3 shows `E → Eb, B → Bb`

#### Scenario: One altered note
- **WHEN** C Dorian is selected
- **THEN** row 5 shows `B → Bb`

### Requirement: Changed rows highlighted
Rows whose chord changes SHALL be highlighted in a style that matches the altered style of the fretboard. Unchanged rows SHALL have no highlight.

#### Scenario: Highlighted rows
- **WHEN** C Mixolydian is selected
- **THEN** rows 3, 5 and 7 (Edim, Gm, Bb) are highlighted and rows 1, 2, 4 and 6 (C, Dm, F, Am) are not

#### Scenario: Every chord can change
- **WHEN** C Aeolian is selected
- **THEN** all seven rows are highlighted, because every triad contains Eb, Ab or Bb

### Requirement: Table updates with the selection
The chord table SHALL update immediately when the comparison option changes, without a page reload. The degrees/note-names label toggle SHALL NOT change the chord table.

#### Scenario: Switching modes
- **WHEN** the user changes the selection from Dorian to Mixolydian
- **THEN** the table shows only rows 3, 5 and 7 as changed (Edim, Gm, Bb)

#### Scenario: Label toggle does not affect table
- **WHEN** the user switches the labels between degrees and note names
- **THEN** the chord table stays the same

### Requirement: Selectable chords
Each chord cell in the C major column and in the mode column SHALL be clickable. Clicking a cell SHALL select that chord, and clicking the selected cell again SHALL deselect it. At most one chord SHALL be selected, and the selected cell SHALL be framed. The selection is identified by its column (C major or mode) and its degree. When the comparison option changes, the selection SHALL keep its column and degree, so it shows the chord on that degree in the new mode. If the mode column disappears (C major alone), a mode-column selection SHALL be cleared.

#### Scenario: Select and deselect
- **WHEN** the user clicks the `Dm` cell in the C major column, then clicks it again
- **THEN** Dm is selected and framed after the first click, and nothing is selected after the second

#### Scenario: Selection follows the mode
- **WHEN** the mode-column chord on degree 3 is selected in Dorian (`Eb`) and the user switches to Mixolydian
- **THEN** the mode-column chord on degree 3 (`Edim`) is selected

#### Scenario: Selection cleared with the column
- **WHEN** a mode-column chord is selected and the user switches to C major alone
- **THEN** no chord is selected

#### Scenario: C major column selection survives
- **WHEN** a C major column chord is selected and the user switches to C major alone
- **THEN** that chord stays selected
