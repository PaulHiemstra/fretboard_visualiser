## ADDED Requirements

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
