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
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```

## Game Controls
- Use number keys to select actions from menus
- Follow on-screen prompts
- Type 'help' at any time to view game tips
- Press 'M' to view business map

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
