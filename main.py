import sys
from colorama import init

from game_state import GameState
from view import CLIView
from controller import GameController
from gui_interface import TycoonGUI

# Initialize colorama for colored text
init()

def main():
    """Main entry point for the game."""
    # Create the game state (Model)
    game_state = GameState()
    
    # Check if GUI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        # Use GUI interface
        # Create controller first if GUI needs it for initialization or direct calls
        controller = GameController(game_state, None) # Temporarily None for view, will be GUI
        gui = TycoonGUI(game_state, controller) 
        controller.view = gui # Assign GUI as the view for the controller
        gui.run()
    else:
        # Use CLI interface with MVC pattern
        view = CLIView()
        controller = GameController(game_state, view)
        view.set_controller_reference(controller)
        controller.start_game()

if __name__ == "__main__":
    main() 