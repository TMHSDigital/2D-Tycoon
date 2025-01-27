import random
import json
import os
from time import sleep
from typing import Dict, Any
from colorama import init, Fore, Style
from pyfiglet import figlet_format
import sys
from gui_interface import TycoonGUI

# Initialize colorama
init()

class TycoonGame:
    def __init__(self):
        self.money = 100
        self.reputation = 50
        self.day = 1
        self.inventory = {
            "basic_supplies": 0,
            "premium_supplies": 0,
            "equipment": 0
        }
        self.prices = {
            "basic_supplies": 30,
            "premium_supplies": 60,
            "equipment": 200
        }
        self.upgrades = {
            "automation": False,
            "marketing": 0,  # Level 0-3
            "storage": 0     # Level 0-2
        }
        self.employees = []
        self.market_trend = 1.0
        self.storage_capacity = 50
        self.loan = 0
        self.loan_interest = 0.1  # 10% interest rate

    def validate_input(self, prompt: str, valid_options: list) -> str:
        """Validate user input against a list of valid options."""
        while True:
            choice = input(prompt).lower()
            if choice in valid_options:
                return choice
            print(f"\n{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")

    def validate_number(self, prompt: str, min_val: int = 0, max_val: int = 1000) -> int:
        """Validate numeric input within a range."""
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"\n{Fore.RED}Please enter a number between {min_val} and {max_val}.{Style.RESET_ALL}")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    def save_game(self) -> None:
        """Save the current game state to a file."""
        game_state = {
            "money": self.money,
            "reputation": self.reputation,
            "day": self.day,
            "inventory": self.inventory,
            "upgrades": self.upgrades,
            "employees": self.employees,
            "loan": self.loan
        }
        with open("savegame.json", "w") as f:
            json.dump(game_state, f)
        print(f"\n{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")

    def load_game(self) -> bool:
        """Load the game state from a file."""
        try:
            with open("savegame.json", "r") as f:
                game_state = json.load(f)
                self.money = game_state["money"]
                self.reputation = game_state["reputation"]
                self.day = game_state["day"]
                self.inventory = game_state["inventory"]
                self.upgrades = game_state["upgrades"]
                self.employees = game_state["employees"]
                self.loan = game_state.get("loan", 0)  # Backward compatibility
            print(f"\n{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
            return True
        except FileNotFoundError:
            print(f"\n{Fore.YELLOW}No saved game found.{Style.RESET_ALL}")
            return False

    def display_status(self) -> None:
        """Display the current game status."""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}Day {self.day}{Style.RESET_ALL}")
        print(f"Money: ${self.money}")
        print(f"Reputation: {self.reputation}")
        if self.loan > 0:
            print(f"{Fore.RED}Loan: ${self.loan}{Style.RESET_ALL}")
        print("\nInventory:")
        for item, amount in self.inventory.items():
            print(f"  {item.replace('_', ' ').title()}: {amount}")
        print("\nUpgrades:")
        for upgrade, level in self.upgrades.items():
            if isinstance(level, bool):
                status = "Enabled" if level else "Disabled"
            else:
                status = f"Level {level}"
            print(f"  {upgrade.replace('_', ' ').title()}: {status}")
        if self.employees:
            print("\nEmployees:", len(self.employees))
        print("="*60)

    def get_daily_events(self) -> Dict[str, Any]:
        """Generate random daily events with market trends."""
        self.market_trend = max(0.5, min(2.0, self.market_trend + random.uniform(-0.2, 0.2)))
        events = {
            "market_demand": self.market_trend,
            "special_event": random.random() < 0.2,
            "market_message": ""
        }
        if self.market_trend > 1.2:
            events["market_message"] = f"{Fore.GREEN}The market is booming!{Style.RESET_ALL}"
        elif self.market_trend < 0.8:
            events["market_message"] = f"{Fore.RED}The market is in decline.{Style.RESET_ALL}"
        return events

    def handle_upgrades(self) -> None:
        """Handle business upgrades."""
        print("\nAvailable Upgrades:")
        print("[1] Automation System ($500) - Increases daily income")
        print("[2] Marketing Campaign Level Up ($300) - Improves reputation gain")
        print("[3] Storage Expansion ($200) - Increases storage capacity")
        print("[4] Back to main menu")

        choice = self.validate_input("Choose an upgrade (1-4): ", ["1", "2", "3", "4"])
        
        if choice == "1" and not self.upgrades["automation"]:
            if self.money >= 500:
                self.money -= 500
                self.upgrades["automation"] = True
                print(f"\n{Fore.GREEN}Automation system installed!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Not enough money!{Style.RESET_ALL}")
        elif choice == "2" and self.upgrades["marketing"] < 3:
            if self.money >= 300:
                self.money -= 300
                self.upgrades["marketing"] += 1
                print(f"\n{Fore.GREEN}Marketing level increased to {self.upgrades['marketing']}!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Not enough money!{Style.RESET_ALL}")
        elif choice == "3" and self.upgrades["storage"] < 2:
            if self.money >= 200:
                self.money -= 200
                self.upgrades["storage"] += 1
                self.storage_capacity += 50
                print(f"\n{Fore.GREEN}Storage capacity increased to {self.storage_capacity}!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Not enough money!{Style.RESET_ALL}")

    def handle_employees(self) -> None:
        """Handle employee management."""
        print("\nEmployee Management:")
        print(f"Current employees: {len(self.employees)}")
        print("[1] Hire employee ($200/day)")
        print("[2] Fire employee")
        print("[3] Back to main menu")

        choice = self.validate_input("Choose an action (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            if self.money >= 200:
                self.employees.append({"salary": 200})
                print(f"\n{Fore.GREEN}New employee hired!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Not enough money to hire!{Style.RESET_ALL}")
        elif choice == "2" and self.employees:
            self.employees.pop()
            print(f"\n{Fore.YELLOW}Employee fired.{Style.RESET_ALL}")

    def handle_loans(self) -> None:
        """Handle loan management."""
        print("\nLoan Management:")
        print(f"Current loan: ${self.loan}")
        print("[1] Take loan")
        print("[2] Repay loan")
        print("[3] Back to main menu")

        choice = self.validate_input("Choose an action (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            max_loan = 1000 - self.loan
            if max_loan > 0:
                amount = self.validate_number(f"Enter loan amount (max ${max_loan}): ", 0, max_loan)
                self.loan += amount
                self.money += amount
                print(f"\n{Fore.GREEN}Loan of ${amount} received!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}You've reached your maximum loan limit!{Style.RESET_ALL}")
        elif choice == "2" and self.loan > 0:
            max_repay = min(self.loan, self.money)
            if max_repay > 0:
                amount = self.validate_number(f"Enter repayment amount (max ${max_repay}): ", 0, max_repay)
                self.loan -= amount
                self.money -= amount
                print(f"\n{Fore.GREEN}Loan repayment of ${amount} processed!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Not enough money to repay loan!{Style.RESET_ALL}")

    def display_menu(self) -> None:
        """Display the main menu options."""
        print(f"\n{Fore.CYAN}Actions:{Style.RESET_ALL}")
        print("[1] Buy supplies")
        print("[2] Work (Sell supplies)")
        print("[3] Manage employees")
        print("[4] Purchase upgrades")
        print("[5] Manage loans")
        print("[6] Rest")
        print("[7] Save game")
        print("[8] Quit")

    def run(self) -> None:
        """Main game loop."""
        print(figlet_format("Business Tycoon", font="slant"))
        print("Welcome to Business Tycoon Adventure!")
        print("Your goal is to reach $1000 while maintaining your reputation.")
        
        if os.path.exists("savegame.json"):
            load = self.validate_input("Would you like to load your saved game? (y/n): ", ["y", "n"])
            if load == "y":
                self.load_game()

        while self.money < 1000 and self.reputation > 0:
            events = self.get_daily_events()
            self.display_status()
            if events["market_message"]:
                print(events["market_message"])
            self.display_menu()
            
            choice = self.validate_input("\nWhat would you like to do? (1-8): ", 
                                      ["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":  # Buy supplies
                print("\nAvailable supplies:")
                print("[1] Basic Supplies ($30)")
                print("[2] Premium Supplies ($60)")
                print("[3] Equipment ($200)")
                print("[4] Back")
                
                supply_choice = self.validate_input("Choose supply type (1-4): ", ["1", "2", "3", "4"])
                if supply_choice != "4":
                    supply_type = ["basic_supplies", "premium_supplies", "equipment"][int(supply_choice) - 1]
                    current_total = sum(self.inventory.values())
                    max_purchase = min(
                        self.storage_capacity - current_total,
                        self.money // self.prices[supply_type]
                    )
                    
                    if max_purchase > 0:
                        amount = self.validate_number(
                            f"How many {supply_type.replace('_', ' ')} would you like to buy? (0-{max_purchase}): ",
                            0, max_purchase
                        )
                        cost = amount * self.prices[supply_type]
                        self.money -= cost
                        self.inventory[supply_type] += amount
                        print(f"\n{Fore.GREEN}Bought {amount} {supply_type.replace('_', ' ')} for ${cost}{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.RED}Not enough money or storage space!{Style.RESET_ALL}")
                    
            elif choice == "2":  # Work
                total_supplies = sum(self.inventory.values())
                if total_supplies > 0:
                    base_income = random.randint(40, 80)
                    market_modifier = events["market_demand"]
                    automation_bonus = 1.5 if self.upgrades["automation"] else 1.0
                    employee_bonus = 1 + (len(self.employees) * 0.2)
                    
                    income = int(base_income * market_modifier * automation_bonus * employee_bonus)
                    
                    # Use premium supplies first if available
                    if self.inventory["premium_supplies"] > 0:
                        income = int(income * 1.5)  # 50% bonus for premium supplies
                        self.inventory["premium_supplies"] -= 1
                    elif self.inventory["basic_supplies"] > 0:
                        self.inventory["basic_supplies"] -= 1
                    
                    self.money += income
                    rep_loss = random.randint(3, 8)
                    rep_loss = max(1, rep_loss - self.upgrades["marketing"])  # Marketing reduces reputation loss
                    self.reputation -= rep_loss
                    
                    print(f"\n{Fore.GREEN}You earned ${income}!{Style.RESET_ALL}")
                    
                    # Pay employees
                    employee_cost = sum(emp["salary"] for emp in self.employees)
                    if employee_cost > 0:
                        self.money -= employee_cost
                        print(f"{Fore.YELLOW}Paid ${employee_cost} in employee salaries.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}You need supplies to work!{Style.RESET_ALL}")
                    
            elif choice == "3":  # Manage employees
                self.handle_employees()
                
            elif choice == "4":  # Purchase upgrades
                self.handle_upgrades()
                
            elif choice == "5":  # Manage loans
                self.handle_loans()
                
            elif choice == "6":  # Rest
                rep_gain = 10 + (self.upgrades["marketing"] * 2)
                self.reputation += rep_gain
                print(f"\n{Fore.GREEN}You rested and improved your reputation by {rep_gain} points.{Style.RESET_ALL}")
                
            elif choice == "7":  # Save game
                self.save_game()
                
            elif choice == "8":  # Quit
                save = self.validate_input("\nWould you like to save before quitting? (y/n): ", ["y", "n"])
                if save == "y":
                    self.save_game()
                print("\nThanks for playing!")
                break
            
            # Special events
            if events["special_event"]:
                event_type = random.choice(["bonus", "penalty", "opportunity"])
                if event_type == "bonus":
                    bonus = random.randint(20, 50)
                    self.money += bonus
                    print(f"\n{Fore.GREEN}SPECIAL EVENT: You received a bonus of ${bonus}!{Style.RESET_ALL}")
                elif event_type == "penalty":
                    penalty = random.randint(10, 30)
                    self.money -= penalty
                    print(f"\n{Fore.RED}SPECIAL EVENT: You had to pay ${penalty} in unexpected costs!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.YELLOW}SPECIAL EVENT: Market prices are especially favorable tomorrow!{Style.RESET_ALL}")
                    self.market_trend = min(2.0, self.market_trend + 0.3)
            
            # Apply loan interest daily
            if self.loan > 0:
                interest = int(self.loan * self.loan_interest / 30)  # Daily interest
                self.loan += interest
                print(f"\n{Fore.RED}Daily loan interest: ${interest}{Style.RESET_ALL}")
            
            self.day += 1
            sleep(1)  # Short pause for better readability

        # End game
        if self.money >= 1000:
            print(f"\n{Fore.GREEN}" + figlet_format("You Won!", font="slant"))
            print(f"Congratulations! You've reached ${self.money} in {self.day} days!{Style.RESET_ALL}")
        elif self.reputation <= 0:
            print(f"\n{Fore.RED}" + figlet_format("Game Over", font="slant"))
            print(f"Your reputation hit zero. Better luck next time!{Style.RESET_ALL}")

def main():
    game = TycoonGame()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        gui = TycoonGUI(game)
        gui.run()
    else:
        game.run()

if __name__ == "__main__":
    main() 