# Business Tycoon TODO List

## Priority 1: Critical Fixes
- [x] **Fix missing GUI methods**
  - [x] Implement `handle_work()` method in TycoonGame class
  - [x] Implement `handle_rest()` method in TycoonGame class
  - [x] Test integration with GUI interface

- [x] **Fix loan system**
  - [x] Adjust daily interest calculation to be more reasonable (currently entire rate/30)
  - [x] Add balance checks to prevent bankruptcy loops

- [x] **Balance game economy**
  - [x] Revise employee cost/benefit ratio to make hiring worthwhile
  - [x] Adjust pricing of supplies and their profit margins
  - [x] Review upgrade costs and benefits

## Priority 2: Architecture Improvements
- [x] **Implement central game state manager**
  - [x] Create GameState class to encapsulate all game state
  - [x] Add validation for state changes
  - [x] Refactor TycoonGame to use the GameState class

- [ ] **Integrate EventManager properly**
  - [x] Connect EventManager (market, competitor, random events) to main game loop
  - [x] Make these events affect GameState consistently
  - [x] Ensure these events work in both CLI and GUI modes (basic GUI message boxes for now)
  - [x] Integrate research system from EventManager (start research, progress, completion effects)
    - [x] Implement starting research (cost, active project check) via CLI
    - [x] Implement daily research progress update in EventManager & GameController
    - [x] Implement research completion (effects on GameState, view notification) for CLI
    - [x] Display research options, status, and active research in CLIView
  - [x] Add UI elements for managing and viewing research (GUI)
    - [x] Add "Research" button and dialog to TycoonGUI
    - [x] Display research projects, status, cost, duration in GUI dialog
    - [x] Allow starting research from GUI dialog with necessary checks
    - [x] Update main GUI status to show active research and progress

- [x] **Refactor to MVC pattern**
  - [x] Separate game logic (Model) from TycoonGame class
  - [x] Create proper Controller classes for CLI and GUI
  - [x] Move display code from TycoonGame to View classes

## Priority 3: Code Quality Improvements
- [ ] **Remove hardcoded values**
  - [x] Create `config.py` with game parameters
  - [ ] Add difficulty settings (easy, normal, hard)
  - [x] Make all magic numbers configurable constants (covered by config.py creation)

- [ ] **Eliminate redundant code**
  - [ ] Consolidate display functions from main.py and ui_helpers.py
  - [ ] Create shared utility functions
  - [ ] Implement DRY principle across codebase

- [ ] **Standardize type hints**
  - [ ] Add consistent type hints to all functions
  - [ ] Fix return type annotations (especially in game_events.py)
  - [ ] Add proper documentation for all classes and methods

- [ ] **Improve error handling**
  - [ ] Add robust error handling for file operations
  - [ ] Add validation for user inputs
  - [ ] Add assertion checks for game state integrity

## Priority 4: Feature Enhancements
- [ ] **Enhance inventory system**
  - [ ] Add item categories with different effects
  - [ ] Implement proper item prioritization logic
  - [ ] Add item decay or expiration

- [ ] **Improve market system**
  - [ ] Add more factors affecting market prices
  - [ ] Implement seasonal trends
  - [ ] Make competitor actions more impactful and visible

- [ ] **Add tutorial system**
  - [ ] Create interactive tutorial for new players
  - [ ] Add contextual help based on game state
  - [ ] Create a "tips" system for game progression

- [ ] **Add statistics and achievements**
  - [ ] Track metrics like total earnings, best day, etc.
  - [ ] Implement achievement system with milestones
  - [ ] Add visualization of business growth over time

## Priority 5: Performance & Security
- [ ] **Improve GUI performance**
  - [ ] Update GUI elements in place instead of recreating
  - [ ] Optimize event handlers and callbacks
  - [ ] Add proper threading for long operations

- [ ] **Optimize game loop**
  - [ ] Remove sleep() calls from main game loop
  - [ ] Implement proper timing system
  - [ ] Add frame rate control for consistent experience

- [ ] **Enhance save system security**
  - [ ] Add save file validation with checksums
  - [ ] Validate all loaded save data before using
  - [ ] Add autosave feature

## Quality of Life Enhancements
- [ ] **"Buy Max" for Supplies**
  - [ ] Add a "Buy Max" button to the buy supplies dialog.
  - [ ] Calculate max affordable and storable quantity.
- [ ] **"Work/Rest Again" Quick Action**
  - [ ] After work/rest, offer an option to repeat the action immediately.
- [ ] **Keyboard Shortcuts in Dialogs**
  - [ ] Implement `Enter` for primary dialog actions.
  - [ ] Implement `Escape` to close/cancel dialogs.
- [ ] **Smart Defaults in Dialog Input Fields**
  - [ ] Pre-fill loan/repayment amounts with sensible defaults.
- [ ] **Streamline Single-Action Day Events**
  - [ ] Auto-advance non-interactive daily messages after a short pause (requires careful design).

## Future Ideas
- [ ] Add multiplayer/competitive mode
- [ ] Create mobile-friendly UI version
- [ ] Add sound effects and music
- [ ] Implement different business types/industries
- [ ] Create an expanded narrative with character interactions 