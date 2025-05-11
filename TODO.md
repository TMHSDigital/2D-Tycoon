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
- [x] **"Buy Max" for Supplies**
  - [x] Add a "Buy Max" button to the buy supplies dialog (GUI).
  - [x] Implement calculation for max affordable/storable quantity (GUI).
  - [x] Add "max" input option for amount in CLI.
  - [x] Implement calculation for "max" in controller for CLI.
- [ ] **"Work/Rest Again" Quick Action**
  - [ ] After work/rest, offer an option to repeat the action immediately.
- [x] **Keyboard Shortcuts in Dialogs**
  - [x] Implement `Enter` for primary dialog actions (where appropriate).
  - [x] Implement `Escape` to close/cancel dialogs.
- [ ] **Smart Defaults in Dialog Input Fields**
  - [x] Pre-fill loan/repayment amounts with sensible defaults (GUI).
  - [x] Suggest sensible default loan/repayment amounts in prompts (CLI).

## Future Ideas
- [ ] Add multiplayer/competitive mode
- [ ] Create mobile-friendly UI version
- [ ] Add sound effects and music
- [ ] Implement different business types/industries
- [ ] Create an expanded narrative with character interactions

---

# Research-Driven Roadmap & Advanced TODOs

## Architecture & Extensibility
- [ ] Refactor event system to be fully event-driven (decouple systems via event manager/observer pattern)
- [ ] Evaluate/experiment with ECS (Entity-Component-System) for businesses, employees, etc.
- [ ] Add plugin architecture for new business types, events, or mechanics
- [ ] Move more game data to external config (JSON/YAML) for easier balancing/modding
- [ ] Modularize simulation logic (distinct subsystems: economy, employees, research, events, customers)
- [ ] Use state machines for business/research/employee processes where appropriate

## Economy & System Balancing
- [ ] Centralize all economic formulas and feedback loops in config or a dedicated module
- [ ] Add exponential/curve-based upgrade and research costs
- [ ] Implement more feedback loops (e.g., reputation affects market, employee morale affects productivity)
- [ ] Add tools/scripts for balancing and simulating the economy outside the main game

## UI/UX & Visualization
- [ ] Add tabbed interface to GUI for business, employees, research, marketing, stats
- [ ] Add data visualization (charts/graphs) for business growth, employee stats, etc. (matplotlib or similar)
- [ ] Improve CLI color coding and menu hierarchy for clarity
- [ ] Add more contextual tooltips and help in GUI
- [ ] Implement detailed statistics/analytics screens

## Save/Load & Data Integrity
- [ ] Add save file versioning and migration support
- [ ] Add save file validation with checksums/hash
- [ ] Support for multiple save slots and autosave
- [ ] Document save format for modders

## Performance & Scalability
- [ ] Profile and batch simulation updates (avoid per-frame recalculation)
- [ ] Use object pooling/flyweight for frequently created/destroyed objects
- [ ] Experiment with async game loop (asyncio) for parallel systems
- [ ] Use NumPy for heavy numerical calculations if scaling up

## Automated Testing
- [ ] Add unit tests for all core systems (economy, employees, events, research)
- [ ] Add property-based tests for economic formulas
- [ ] Add automated UI tests (Tkinter and CLI)
- [ ] Mock time-based functions for fast simulation in tests

## Modding & Plugins
- [ ] Implement mod loader for external content (businesses, events, upgrades)
- [ ] Expose clear APIs for modders (documented hooks, data formats)
- [ ] Provide example mods and documentation

## Advanced/Innovative Features
- [ ] Integrate AI-powered competitors (basic ML for market/competitor behavior)
- [ ] Add cloud save support (optional)
- [ ] Add procedural content generation (unique scenarios, markets)
- [ ] Integrate pandas for in-game data analysis/visualization
- [ ] Add async/parallel processing for large simulations

## Psychological Engagement & Player Enjoyment
- [ ] Add variable reward systems (random events, rare upgrades, surprise bonuses)
- [ ] Implement milestone achievements and unlocks (e.g., new features, business expansions)
- [ ] Enhance progress feedback: visual (charts, bars), audio (sfx), and narrative (story beats, notifications)
- [ ] Design meaningful choices with real trade-offs (risk/reward, staff vs. morale, investment dilemmas)
- [ ] Layer complexity gradually—start simple, unlock new mechanics as player progresses
- [ ] Support multiple viable strategies and playstyles (not just one optimal path)
- [ ] Add daily/return incentives (login bonuses, rotating challenges, streak rewards)
- [ ] Integrate narrative hooks (story events, evolving scenarios, character-driven events)
- [ ] Add FOMO/habit features (limited-time events, time-limited opportunities)
- [ ] Provide clear, incremental feedback for every action (stat changes, popups, animations)
- [ ] Implement a system for player agency and experimentation (sandbox/test mode, creative options)
- [ ] Use case study features: e.g., sales/review charts (Game Dev Tycoon), exponential growth (AdVenture Capitalist), creative freedom (RollerCoaster Tycoon)
- [ ] Regularly playtest for fun and engagement, not just balance 