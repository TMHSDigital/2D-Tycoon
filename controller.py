import os
import random
from time import sleep
from typing import Dict, Any

from game_state import GameState
from view import View

class GameController:
    """Controller class in MVC architecture to handle game flow."""
    
    def __init__(self, game_state: GameState, view: View):
        self.game_state = game_state
        self.view = view
    
    def start_game(self) -> None:
        """Start the game and handle main game loop."""
        self.view.display_welcome()
        
        # Check for existing save game
        if os.path.exists("savegame.json"):
            load_choice = self.view.get_input("Would you like to load your saved game? (y/n): ", ["y", "n"])
            if load_choice == "y":
                if self.game_state.load_game():
                    self.view.show_message("Game loaded successfully!", "success")
                else:
                    self.view.show_message("Failed to load game.", "error")
        
        # Main game loop
        while not self.game_state.is_game_over():
            # Get daily events
            events = self.game_state.update_daily_market()
            
            # Display game status
            self.view.display_status(self.game_state)
            
            # Display market message if any
            if events["market_message"]:
                self.view.display_market_message(events["market_message"])
            
            # Display main menu and get player choice
            self.view.display_menu()
            choice = self.view.get_input("\nWhat would you like to do? (1-8): ", 
                                     ["1", "2", "3", "4", "5", "6", "7", "8"])
            
            # Process player choice
            if choice == "1":  # Buy supplies
                self.handle_buy_supplies()
                
            elif choice == "2":  # Work
                self.handle_work()
                
            elif choice == "3":  # Manage employees
                self.handle_employees()
                
            elif choice == "4":  # Purchase upgrades
                self.handle_upgrades()
                
            elif choice == "5":  # Manage loans
                self.handle_loans()
                
            elif choice == "6":  # Rest
                self.handle_rest()
                
            elif choice == "7":  # Save game
                if self.game_state.save_game():
                    self.view.show_message("Game saved successfully!", "success")
                else:
                    self.view.show_message("Failed to save game.", "error")
                
            elif choice == "8":  # Quit
                save_choice = self.view.get_input("\nWould you like to save before quitting? (y/n): ", ["y", "n"])
                if save_choice == "y":
                    self.game_state.save_game()
                    self.view.show_message("Game saved successfully!", "success")
                self.view.show_message("Thanks for playing!")
                break
            
            # Handle special events
            if events["special_event"]:
                event_type = random.choice(["bonus", "penalty", "opportunity"])
                result = self.game_state.handle_special_event(event_type)
                self.view.show_message(f"SPECIAL EVENT: {result['message']}", 
                                 "success" if event_type != "penalty" else "error")
            
            # Apply loan interest
            interest = self.game_state.apply_daily_interest()
            if interest > 0:
                self.view.show_message(f"Daily loan interest: ${interest}", "error")
            
            # Advance to next day
            self.game_state.advance_day()
            sleep(0.5)  # Short pause for readability
        
        # Game over
        self.view.display_game_over(self.game_state, self.game_state.is_win())
    
    def handle_buy_supplies(self) -> None:
        """Handle the buy supplies action."""
        self.view.display_buy_supplies_menu(self.game_state)
        
        supply_choice = self.view.get_input("Choose supply type (1-4): ", ["1", "2", "3", "4"])
        if supply_choice == "4":
            return
            
        supply_types = ["basic_supplies", "premium_supplies", "equipment"]
        supply_type = supply_types[int(supply_choice) - 1]
        
        current_total = sum(self.game_state.inventory.values())
        max_purchase = min(
            self.game_state.storage_capacity - current_total,
            self.game_state.money // self.game_state.prices[supply_type]
        )
        
        if max_purchase <= 0:
            self.view.show_message("Not enough money or storage space!", "error")
            return
            
        amount = self.view.get_number_input(
            f"How many {supply_type.replace('_', ' ')} would you like to buy? (0-{max_purchase}): ",
            0, max_purchase
        )
        
        if amount > 0:
            cost = amount * self.game_state.prices[supply_type]
            if self.game_state.buy_supplies(supply_type, amount):
                self.view.show_message(f"Bought {amount} {supply_type.replace('_', ' ')} for ${cost}", "success")
            else:
                self.view.show_message("Failed to buy supplies.", "error")
    
    def handle_work(self) -> None:
        """Handle the work action."""
        income = self.game_state.work()
        if income > 0:
            self.view.show_message(f"You earned ${income}!", "success")
            
            # Show employee costs
            employee_cost = len(self.game_state.employees) * 150
            if employee_cost > 0:
                self.view.show_message(f"Paid ${employee_cost} in employee salaries.", "warning")
        else:
            self.view.show_message("You need supplies to work!", "error")
    
    def handle_employees(self) -> None:
        """Handle employee management."""
        self.view.display_employee_menu(self.game_state)
        
        choice = self.view.get_input("Choose an action (1-3): ", ["1", "2", "3"])
        
        if choice == "1":  # Hire
            if self.game_state.hire_employee():
                self.view.show_message("New employee hired!", "success")
            else:
                self.view.show_message("Not enough money to hire!", "error")
        elif choice == "2":  # Fire
            if self.game_state.fire_employee():
                self.view.show_message("Employee fired.", "warning")
            else:
                self.view.show_message("No employees to fire!", "error")
    
    def handle_upgrades(self) -> None:
        """Handle purchasing upgrades."""
        self.view.display_upgrade_menu(self.game_state)
        
        choice = self.view.get_input("Choose an upgrade (1-4): ", ["1", "2", "3", "4"])
        if choice == "4":
            return
            
        upgrade_types = ["automation", "marketing", "storage"]
        upgrade_type = upgrade_types[int(choice) - 1]
        
        if self.game_state.purchase_upgrade(upgrade_type):
            if upgrade_type == "automation":
                self.view.show_message("Automation system installed!", "success")
            elif upgrade_type == "marketing":
                self.view.show_message(f"Marketing level increased to {self.game_state.upgrades['marketing']}!", "success")
            elif upgrade_type == "storage":
                self.view.show_message(f"Storage capacity increased to {self.game_state.storage_capacity}!", "success")
        else:
            # Check if already at max level
            if upgrade_type == "automation" and self.game_state.upgrades["automation"]:
                self.view.show_message("Automation is already enabled!", "warning")
            elif upgrade_type == "marketing" and self.game_state.upgrades["marketing"] >= 3:
                self.view.show_message("Marketing is already at maximum level!", "warning")
            elif upgrade_type == "storage" and self.game_state.upgrades["storage"] >= 2:
                self.view.show_message("Storage is already at maximum level!", "warning")
            else:
                self.view.show_message("Not enough money for this upgrade!", "error")
    
    def handle_loans(self) -> None:
        """Handle loan management."""
        self.view.display_loan_menu(self.game_state)
        
        choice = self.view.get_input("Choose an action (1-3): ", ["1", "2", "3"])
        
        if choice == "1":  # Take loan
            max_loan = 1000 - self.game_state.loan
            if max_loan <= 0:
                self.view.show_message("You've reached your maximum loan limit!", "error")
                return
                
            safe_loan = self.game_state.get_safe_loan_amount()
            if safe_loan < max_loan:
                self.view.show_message(f"Warning: Based on your income, we recommend a maximum loan of ${safe_loan}.", "warning")
                
            amount = self.view.get_number_input(f"Enter loan amount (max ${max_loan}): ", 0, max_loan)
            
            if amount > 0:
                if self.game_state.take_loan(amount):
                    self.view.show_message(f"Loan of ${amount} received!", "success")
                else:
                    self.view.show_message("Failed to process loan.", "error")
        
        elif choice == "2":  # Repay loan
            if self.game_state.loan <= 0:
                self.view.show_message("You don't have any outstanding loans.", "warning")
                return
                
            max_repay = min(self.game_state.loan, self.game_state.money)
            if max_repay <= 0:
                self.view.show_message("Not enough money to repay loan!", "error")
                return
                
            amount = self.view.get_number_input(f"Enter repayment amount (max ${max_repay}): ", 0, max_repay)
            
            if amount > 0:
                if self.game_state.repay_loan(amount):
                    self.view.show_message(f"Loan repayment of ${amount} processed!", "success")
                else:
                    self.view.show_message("Failed to process repayment.", "error")
    
    def handle_rest(self) -> None:
        """Handle the rest action."""
        rep_gain = self.game_state.rest()
        self.view.show_message(f"You rested and improved your reputation by {rep_gain} points.", "success") 