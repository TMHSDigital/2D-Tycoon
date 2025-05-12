# Business Tycoon Adventure

A text-based business simulation game where you manage resources, build reputation, and try to reach $1000 in profit while maintaining your business reputation.

## Features
- Resource management (money, supplies, reputation)
- Employee management system
- Business upgrades (automation, marketing, storage)
- Research and development system
- Competitor businesses that affect market prices
- Dynamic market conditions with supply and demand
- Loan system with interest
- Random events and opportunities
- Employee events and morale system
- Save/load game functionality
- Colorful text interface with ASCII art
- Progress bars and business map
- Comprehensive help system

## How to Play
1. Make sure you have Python 3.7 or higher installed
2. Create and activate a virtual environment:

   For Windows:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

   For macOS/Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the game:

   For Command Line Interface:
   ```
   python main.py
   ```

   For Graphical User Interface (recommended for the best experience):
   ```
   python main.py --gui
   ```

## Game Controls

### Command Line Interface
- Use number keys to select actions from menus
- Follow on-screen prompts
- Type 'help' at any time to view game tips
- Press 'M' to view business map

### Graphical User Interface
- Click buttons to perform actions
- Use dialog windows for detailed interactions
- All game features accessible through intuitive GUI elements

## Game Mechanics

### Resource Management
- Buy and sell different types of supplies
- Manage storage capacity
- Balance inventory levels

### Employee System
- Hire employees to increase productivity
- Manage employee salaries
- Handle employee events and morale

### Research & Development
- Research new technologies
- Unlock business improvements
- Gain competitive advantages

### Market System
- Dynamic pricing based on supply and demand
- Competitor actions affect market conditions
- Special market events and opportunities

### Business Upgrades
- Automation system for increased efficiency
- Marketing campaigns to improve reputation
- Storage expansions for inventory management

## Game Tips
- Start with basic supplies as they provide good early-game returns
- Equipment is a significant investment ($200) - plan accordingly
- Your reputation decreases when working, so use rest to recover it
- The market can have "booming" periods - take advantage of these
- Save your game regularly using the save function
- Try to maintain a balance between profits and reputation
- Special events can provide bonuses like extra money or favorable market conditions

# Architecture

This project uses a clear **MVC (Model-View-Controller)** architecture for both CLI and GUI modes:

- **Model:** `GameState` (in `game_state.py`) holds all game data, business logic, and state transitions. It is config-driven and contains no UI code.
- **View:** `CLIView` (in `view.py`) and `TycoonGUI` (in `gui_interface.py`) provide the user interface. The CLI uses text and colorama; the GUI uses Tkinter with a modern theme.
- **Controller:** `GameController` (in `controller.py`) manages the game loop, user actions, and communication between Model and View. It is UI-agnostic.
- **Event System:** `EventManager` (in `game_events.py`) handles market, competitor, and random events, as well as research project progress.
- **Config:** `config.py` centralizes all game parameters, making balancing and extension easy.

**Game Loop:**
- The controller runs the main loop, updating the market, processing user actions, handling events, and advancing the day.
- Both CLI and GUI modes use the same core logic and state, only differing in how input/output is handled.

**Extensibility:**
- New features (supplies, upgrades, research, events) can be added by updating `config.py` and implementing logic in the relevant Model/Controller methods.
- The architecture is designed for easy testing, refactoring, and UI swaps.

# File Overview

- `main.py`: Entry point. Parses CLI args, launches CLI or GUI, wires up MVC.
- `game_state.py`: The Model. All business logic, state, and save/load.
- `controller.py`: The Controller. Main game loop, user action handling, event processing.
- `view.py`: Abstract View base class and CLIView implementation.
- `gui_interface.py`: TycoonGUI class (Tkinter-based), all dialogs and GUI logic.
- `game_events.py`: EventManager for market, competitor, random, and research events.
- `config.py`: All game constants, prices, upgrade specs, research, and difficulty settings.
- `ui_helpers.py`: Shared UI utilities (used by GUI).
- `business_map.py`: ASCII/GUI business map rendering.
- `requirements.txt`: Python dependencies.
- `TODO.md`: Roadmap and changelog.

# Extending the Game

- **Add a new supply:**
  1. Add to `SUPPLY_PRICES` and `SUPPLY_USAGE_EFFECTS` in `config.py`.
  2. Update any relevant logic in `GameState` (e.g., how it's used in work).
- **Add a new upgrade:**
  1. Add to `UPGRADE_SPECS` in `config.py`.
  2. Implement its effect in `GameState.purchase_upgrade` and/or other methods.
- **Add a new research project:**
  1. Add to `RESEARCH_PROJECTS_SPECS` in `config.py`.
  2. Implement its effect in `GameState.apply_research_completion`.
- **Add a new event:**
  1. Update `EventManager` in `game_events.py` and/or event config in `config.py`.
  2. Add any new event effects to `GameState`.
- **Add a new UI feature:**
  1. For CLI, update `CLIView` in `view.py`.
  2. For GUI, update `TycoonGUI` in `gui_interface.py`.

## Development
The game is structured into multiple modules:
- `main.py`: Core game logic and main loop
- `game_events.py`: Event management and random occurrences
- `ui_helpers.py`: UI components and visual elements

## Contributing
Feel free to contribute to the game by:
1. Adding new features
2. Improving game balance
3. Enhancing the UI
4. Fixing bugs
5. Adding more events and content
