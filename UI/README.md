# User Interface Documentation

Business Tycoon Adventure offers two interface options: a Command Line Interface (CLI) and a Graphical User Interface (GUI).

## Command Line Interface (CLI)

The CLI provides a classic text-based gaming experience with colored output and ASCII art.

![CLI Screenshot](cli-screenshot.png)

### CLI Features
- Colored text for better readability
- ASCII art title and game over screens
- Clear menu structure with numbered options
- Real-time status updates
- Easy-to-navigate inventory system

## Graphical User Interface (GUI)

The GUI offers a modern, point-and-click experience using tkinter.

![GUI Screenshot](gui-screenshot.png)

### GUI Features
- Clean, modern window layout
- Real-time business status display
- Easy-to-use dialog windows for:
  - Buying supplies
  - Managing employees
  - Handling upgrades
  - Managing loans
- Visual feedback for actions
- Save/load functionality with confirmation dialogs

## Switching Between Interfaces

- For CLI: `python main.py`
- For GUI: `python main.py --gui`

Both interfaces share the same game logic and save file format, allowing players to switch between them at will.