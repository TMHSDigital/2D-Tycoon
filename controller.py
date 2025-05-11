import os
import random
from time import sleep
from typing import Dict, Any

from game_state import GameState
from view import View
from game_events import EventManager

class GameController:
    """Controller class in MVC architecture to handle game flow."""
    
    def __init__(self, game_state: GameState, view: View):
        self.game_state = game_state
        self.view = view
        self.event_manager = EventManager()
        self.game_state.market_trend = self.event_manager.market_trend
    
    def start_game(self) -> None:
        """Start the game and handle main game loop."""
        self.view.display_welcome()
        
        if os.path.exists("savegame.json"):
            load_choice = self.view.get_input("Would you like to load your saved game? (y/n): ", ["y", "n"])
            if load_choice == "y":
                if self.game_state.load_game():
                    self.view.show_message("Game loaded successfully!", "success")
                else:
                    self.view.show_message("Failed to load game.", "error")
        
        while not self.game_state.is_game_over():
            market_data = self.event_manager.update_market()
            self.game_state.market_trend = self.event_manager.market_trend
            self.game_state.current_market_demand = market_data.get("market_demand", 1.0)
            
            self.view.display_status(self.game_state)
            
            if market_data.get("market_message"):
                self.view.display_market_message(market_data["market_message"])
            
            if market_data.get("competitor_action"):
                action_details = market_data["competitor_action"]
                message, effect = self.event_manager.handle_competitor_action(action_details)
                self.view.show_message(f"COMPETITOR NEWS: {message}", "warning")
                self.game_state.apply_competitor_effect(effect)
            
            self.view.display_menu()
            choice = self.view.get_input("\nWhat would you like to do? (1-8): ", 
                                     ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            
            if choice == "1": self.handle_buy_supplies()
            elif choice == "2": self.handle_work()
            elif choice == "3": self.handle_employees()
            elif choice == "4": self.handle_upgrades()
            elif choice == "5": self.handle_loans()
            elif choice == "6": self.handle_rest()
            elif choice == "7": self.handle_save_game()
            elif choice == "8": 
                if self.handle_quit_game(): break
            elif choice == "9": self.handle_start_research()
            
            if market_data.get("special_event"):
                random_event_details = self.event_manager.get_random_event()
                event_type = random_event_details.get("type", "none")
                
                if event_type != "none":
                    self.view.show_message(random_event_details["message"])
                    self.game_state.apply_random_event_effect(random_event_details)
            
            interest = self.game_state.apply_daily_interest()
            if interest > 0:
                self.view.show_message(f"Daily loan interest: ${interest}", "error")
            
            self.game_state.advance_day()
            
            # === Research Progress Update ===
            if self.event_manager.active_research:
                research_status = self.event_manager.update_research() # This updates progress internally in EventManager
                # Sync GameState's active_research_project, in case EventManager clears it on completion
                self.game_state.active_research_project = self.event_manager.active_research 
                
                if research_status.get("status") == "completed":
                    completed_project_key = research_status.get("project")
                    if completed_project_key:
                        project_name = self.event_manager.research_projects[completed_project_key]['name']
                        self.view.show_message(f"RESEARCH COMPLETE: '{project_name}'! Effects applied.", "success")
                        self.game_state.apply_research_completion(completed_project_key)
                        # EventManager.update_research already sets its active_research to None and progress to 0 on completion.
                        self.game_state.active_research_project = None # Also clear in GameState
                # Optionally, display in-progress message or update a persistent status
                # else:
                #    progress = research_status.get("progress",0)
                #    current_project_name = self.event_manager.research_projects[self.event_manager.active_research]['name']
                #    self.view.show_message(f"Research on {current_project_name} is now {progress:.0f}% complete.", "info")
            # === Research Progress Update: End ===
            
            sleep(0.5)
        
        self.view.display_game_over(self.game_state, self.game_state.is_win())

    def handle_save_game(self):
        if self.game_state.save_game():
            self.view.show_message("Game saved successfully!", "success")
        else:
            self.view.show_message("Failed to save game.", "error")

    def handle_quit_game(self) -> bool:
        save_choice = self.view.get_input("\nWould you like to save before quitting? (y/n): ", ["y", "n"])
        if save_choice == "y":
            self.handle_save_game()
        self.view.show_message("Thanks for playing!")
        return True
    
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

    def handle_start_research(self) -> None:
        """Handle starting a new research project."""
        # Pass event_manager attributes directly for the view to use
        research_choice_key = self.view.display_research_menu(
            self.event_manager.research_projects,
            self.game_state.completed_research,
            self.event_manager.active_research,
            self.event_manager.research_progress
        )

        if not research_choice_key: # Player chose to go back
            return

        if research_choice_key in self.game_state.completed_research:
            self.view.show_message("This research project has already been completed.", "warning")
            return

        if self.event_manager.active_research is not None:
            self.view.show_message(f"Research for '{self.event_manager.research_projects[self.event_manager.active_research]['name']}' is already in progress.", "warning")
            return

        project_details = self.event_manager.research_projects.get(research_choice_key)
        if not project_details:
            self.view.show_message("Invalid research project selected.", "error") # Should not happen with proper menu
            return

        cost = project_details["cost"]
        if self.game_state.money < cost:
            self.view.show_message(f"Not enough money to start research for '{project_details['name']}'. Cost: ${cost}", "error")
            return

        # Start the research
        self.game_state.money -= cost
        self.event_manager.active_research = research_choice_key
        self.game_state.active_research_project = research_choice_key # Sync to GameState for saving
        self.event_manager.research_progress = 0 # Reset progress for the new project
        self.view.show_message(f"Research started for '{project_details['name']}'! It will take {project_details['duration']} days.", "success") 