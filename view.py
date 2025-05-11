from abc import ABC, abstractmethod
from typing import Dict, Any, List
from colorama import Fore, Style

class View(ABC):
    """Abstract base class for views in MVC architecture."""
    
    @abstractmethod
    def display_welcome(self) -> None:
        """Display welcome message."""
        pass
    
    @abstractmethod
    def display_status(self, game_state: Any) -> None:
        """Display current game status."""
        pass
    
    @abstractmethod
    def display_menu(self) -> None:
        """Display main menu options."""
        pass
    
    @abstractmethod
    def display_game_over(self, game_state: Any, is_win: bool) -> None:
        """Display game over screen."""
        pass
    
    @abstractmethod
    def get_input(self, prompt: str, valid_options: List[str] = None) -> str:
        """Get user input with validation."""
        pass
    
    @abstractmethod
    def get_number_input(self, prompt: str, min_val: int = 0, max_val: int = 1000) -> int:
        """Get numeric input with range validation."""
        pass
    
    @abstractmethod
    def show_message(self, message: str, message_type: str = "info") -> None:
        """Show a message to the user."""
        pass


class CLIView(View):
    """Command Line Interface View implementation."""
    
    def __init__(self):
        """Initialize the CLI View."""
        from pyfiglet import figlet_format
        self.figlet_format = figlet_format
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        print(self.figlet_format("Business Tycoon", font="slant"))
        print("Welcome to Business Tycoon Adventure!")
        print("Your goal is to reach $1000 while maintaining your reputation.")
    
    def display_status(self, game_state: Any) -> None:
        """Display current game status."""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}Day {game_state.day}{Style.RESET_ALL}")
        print(f"Money: ${game_state.money}")
        print(f"Reputation: {game_state.reputation}")
        
        if game_state.loan > 0:
            print(f"{Fore.RED}Loan: ${game_state.loan}{Style.RESET_ALL}")
        
        print("\nInventory:")
        for item, amount in game_state.inventory.items():
            print(f"  {item.replace('_', ' ').title()}: {amount}")
        
        print("\nUpgrades:")
        for upgrade, level in game_state.upgrades.items():
            if isinstance(level, bool):
                status = "Enabled" if level else "Disabled"
            else:
                status = f"Level {level}"
            print(f"  {upgrade.replace('_', ' ').title()}: {status}")
        
        if game_state.employees:
            print("\nEmployees:", len(game_state.employees))
        
        print("="*60)
    
    def display_menu(self) -> None:
        """Display main menu options."""
        print(f"\n{Fore.CYAN}Actions:{Style.RESET_ALL}")
        print("[1] Buy supplies")
        print("[2] Work (Sell supplies)")
        print("[3] Manage employees")
        print("[4] Purchase upgrades")
        print("[5] Manage loans")
        print("[6] Rest")
        print("[7] Save game")
        print("[8] Quit")
    
    def display_game_over(self, game_state: Any, is_win: bool) -> None:
        """Display game over screen."""
        if is_win:
            print(f"\n{Fore.GREEN}" + self.figlet_format("You Won!", font="slant"))
            print(f"Congratulations! You've reached ${game_state.money} in {game_state.day} days!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}" + self.figlet_format("Game Over", font="slant"))
            print(f"Your reputation hit zero. Better luck next time!{Style.RESET_ALL}")
    
    def get_input(self, prompt: str, valid_options: List[str] = None) -> str:
        """Get user input with validation."""
        while True:
            user_input = input(prompt).lower()
            if valid_options is None or user_input in valid_options:
                return user_input
            print(f"\n{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")
    
    def get_number_input(self, prompt: str, min_val: int = 0, max_val: int = 1000) -> int:
        """Get numeric input with range validation."""
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"\n{Fore.RED}Please enter a number between {min_val} and {max_val}.{Style.RESET_ALL}")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def show_message(self, message: str, message_type: str = "info") -> None:
        """Show a message to the user."""
        if message_type == "success":
            print(f"\n{Fore.GREEN}{message}{Style.RESET_ALL}")
        elif message_type == "error":
            print(f"\n{Fore.RED}{message}{Style.RESET_ALL}")
        elif message_type == "warning":
            print(f"\n{Fore.YELLOW}{message}{Style.RESET_ALL}")
        else:
            print(f"\n{message}")
    
    def display_buy_supplies_menu(self, game_state: Any) -> None:
        """Display menu for buying supplies."""
        print("\nAvailable supplies:")
        print(f"[1] Basic Supplies (${game_state.prices['basic_supplies']})")
        print(f"[2] Premium Supplies (${game_state.prices['premium_supplies']})")
        print(f"[3] Equipment (${game_state.prices['equipment']})")
        print("[4] Back")
    
    def display_employee_menu(self, game_state: Any) -> None:
        """Display employee management menu."""
        print("\nEmployee Management:")
        print(f"Current employees: {len(game_state.employees)}")
        print("[1] Hire employee ($150/day)")
        print("[2] Fire employee")
        print("[3] Back to main menu")
    
    def display_upgrade_menu(self, game_state: Any) -> None:
        """Display upgrades menu."""
        print("\nAvailable Upgrades:")
        print("[1] Automation System ($400) - Increases daily income by 50%")
        print("[2] Marketing Campaign Level Up ($250) - Improves reputation gain and reduces reputation loss")
        print("[3] Storage Expansion ($150) - Increases storage capacity by 50 units")
        print("[4] Back to main menu")
    
    def display_loan_menu(self, game_state: Any) -> None:
        """Display loan management menu."""
        print("\nLoan Management:")
        print(f"Current loan: ${game_state.loan}")
        print(f"Annual interest rate: {game_state.loan_interest * 100}%")
        print(f"Daily interest rate: {game_state.loan_interest / 365:.6f}%")
        
        if game_state.loan > 0:
            daily_interest = int(game_state.loan * game_state.loan_interest / 365)
            print(f"Daily interest cost: ${daily_interest}")
        
        print("[1] Take loan")
        print("[2] Repay loan")
        print("[3] Back to main menu")
        
        # Display recommended loan amount
        income_potential = game_state.get_income_potential()
        if income_potential > 0:
            safe_max_loan = game_state.get_safe_loan_amount()
            if safe_max_loan < (1000 - game_state.loan):
                print(f"\n{Fore.YELLOW}Recommended maximum loan: ${safe_max_loan} (based on income){Style.RESET_ALL}")
    
    def display_market_message(self, message: str) -> None:
        """Display market trend message."""
        if "booming" in message:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        elif "decline" in message:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        else:
            print(message) 