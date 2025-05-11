import os
import random
from time import sleep
from typing import Dict, Any

from game_state import GameState
from view import View
from game_events import EventManager
import config

class GameController:
    """Controller class in MVC architecture to handle game flow."""
    
    def __init__(self, game_state: GameState, view: View):
        self.game_state = game_state
        self.view = view
        self.event_manager = EventManager()
        self.game_state.market_trend = self.event_manager.market_trend
        self.queued_next_day_action = None
    
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
            
            # --- QoL: Work/Rest Again logic --- 
            # If a repeat action was queued, this variable will be set in the *previous* iteration.
            # We need a way to carry this intent to the current iteration.
            # Let's use a member variable in the controller for this.
            # self.queued_next_day_action = None # Initialize in __init__

            action_repeated_for_today = False
            if hasattr(self, 'queued_next_day_action') and self.queued_next_day_action:
                if self.queued_next_day_action == 'work':
                    if sum(self.game_state.inventory.values()) > 0: # Re-check condition
                        self.view.show_message(f"Automatically working for Day {self.game_state.day}...", "info", delay=0.2)
                        if self.handle_work(): # handle_work now asks if we want to queue *another* repeat
                            self.queued_next_day_action = 'work' # Re-queue if they said yes again
                        else:
                            self.queued_next_day_action = None
                        action_repeated_for_today = True
                    else:
                        self.view.show_message("Cannot auto-work: No supplies!", "warning")
                        self.queued_next_day_action = None
                elif self.queued_next_day_action == 'rest':
                    self.view.show_message(f"Automatically resting for Day {self.game_state.day}...", "info", delay=0.2)
                    if self.handle_rest(): # handle_rest now asks if we want to queue *another* repeat
                        self.queued_next_day_action = 'rest' # Re-queue
                    else:
                        self.queued_next_day_action = None
                    action_repeated_for_today = True
                # Important: Consume the queue for this day if action was attempted
                if not action_repeated_for_today: # If condition failed (e.g. no supplies for work)
                    self.queued_next_day_action = None
            
            if not action_repeated_for_today and not self.game_state.is_game_over():
                self.view.display_menu()
                choice = self.view.get_input("\nWhat would you like to do? (1-9): ", 
                                         ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
                
                if choice == "1": self.handle_buy_supplies()
                elif choice == "2": 
                    if self.handle_work(): self.queued_next_day_action = 'work' 
                    else: self.queued_next_day_action = None
                elif choice == "3": self.handle_employees()
                elif choice == "4": self.handle_upgrades()
                elif choice == "5": self.handle_loans()
                elif choice == "6": 
                    if self.handle_rest(): self.queued_next_day_action = 'rest'
                    else: self.queued_next_day_action = None
                elif choice == "7": self.handle_save_game()
                elif choice == "8": 
                    if self.handle_quit_game(): break
                elif choice == "9": self.handle_start_research()
                
                # If any other action was chosen, clear any queued work/rest
                if choice not in ['2', '6']:
                    self.queued_next_day_action = None
            elif self.game_state.is_game_over(): # If game over after a repeated action
                 pass # Loop will terminate

            # Daily processing happens AFTER the action for the current day
            if not self.game_state.is_game_over():
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
                
                if self.event_manager.active_research:
                    research_status = self.event_manager.update_research()
                    self.game_state.active_research_project = self.event_manager.active_research 
                    if research_status.get("status") == "completed":
                        completed_project_key = research_status.get("project")
                        if completed_project_key:
                            project_name = self.event_manager.research_projects_data[completed_project_key]['name']
                            self.view.show_message(f"RESEARCH COMPLETE: '{project_name}'! Effects applied.", "success")
                            self.game_state.apply_research_completion(completed_project_key)
                            self.game_state.active_research_project = None 
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
        self.view.display_buy_supplies_menu(self.game_state) # CLIView now hints about 'max'
        
        # In CLI, supply_choice is a number string corresponding to index + 1
        # The list of supply keys is ordered from config.SUPPLY_PRICES.keys()
        supply_keys_ordered = list(config.SUPPLY_PRICES.keys())
        back_option_index_str = str(len(supply_keys_ordered) + 1)
        valid_supply_choices = [str(i+1) for i in range(len(supply_keys_ordered))] + [back_option_index_str]

        choice_str = self.view.get_input(f"Choose supply type (1-{len(supply_keys_ordered)}) or {back_option_index_str} for Back: ", valid_supply_choices)
        
        if choice_str == back_option_index_str:
            return
            
        supply_type = supply_keys_ordered[int(choice_str) - 1]
        
        price_per_unit = self.game_state.prices.get(supply_type, 0)
        if price_per_unit <= 0: # Should not happen if supply_type is valid
            self.view.show_message("Selected supply has an invalid price.", "error")
            return

        current_total_inventory = sum(self.game_state.inventory.values())
        max_affordable = self.game_state.money // price_per_unit
        max_storable = self.game_state.storage_capacity - current_total_inventory
        true_max_purchase = max(0, min(max_affordable, max_storable))
        
        if true_max_purchase <= 0:
            self.view.show_message("Not enough money or storage space to buy any!", "error")
            return
            
        amount_input = self.view.get_number_input(
            f"How many {supply_type.replace('_', ' ').title()} would you like to buy? (0-{true_max_purchase}, or 'max'): ",
            0, true_max_purchase, allow_max_str=True
        )
        
        amount_to_buy = 0
        if amount_input == "max":
            amount_to_buy = true_max_purchase
        else:
            amount_to_buy = int(amount_input) # Already validated by get_number_input if not 'max'

        if amount_to_buy > 0:
            if self.game_state.buy_supplies(supply_type, amount_to_buy):
                cost = amount_to_buy * price_per_unit
                self.view.show_message(f"Bought {amount_to_buy} {supply_type.replace('_', ' ').title()} for ${cost}", "success")
            else:
                # GameState.buy_supplies should ideally handle internal logic and return False if failed.
                # This specific error might be redundant if GameState.buy_supplies is robust.
                self.view.show_message("Failed to buy supplies (already checked money/storage).", "error") 
        elif amount_input != "max": # Only show if they didn't type 0 and didn't type max (which might result in 0)
             self.view.show_message("No supplies purchased.", "info")
    
    def handle_work(self) -> bool: # Returns True if a repeat action was taken for the next day cycle
        """Handle the work action."""
        income = self.game_state.work()
        next_day_action_taken = False

        if income > 0:
            self.view.show_message(f"You earned ${income}!", "success")
            employee_cost = len(self.game_state.employees) * config.EMPLOYEE_DAILY_SALARY
            if employee_cost > 0:
                self.view.show_message(f"Paid ${employee_cost} in employee salaries.", "warning")
            
            # Check if can work again (has supplies)
            if sum(self.game_state.inventory.values()) > 0 and not self.game_state.is_game_over():
                repeat_choice = self.view.get_input(f"Work again for Day {self.game_state.day + 1}? (y/n): ", ["y", "n"])
                if repeat_choice == 'y':
                    next_day_action_taken = True 
                    # The actual work for next day will happen in the next loop iteration after daily processing
                    self.view.show_message("Scheduled to work next day...", "info")
        else:
            self.view.show_message("You need supplies to work!", "error")
        return next_day_action_taken
    
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
        # View now returns the direct upgrade_key or None
        upgrade_key_selected = self.view.display_upgrade_menu(self.game_state)
        
        if not upgrade_key_selected:
            return # Player chose to go back
            
        # upgrade_types = ["automation", "marketing", "storage"] # No longer needed
        # upgrade_type = upgrade_types[int(choice) - 1] # Old way
        upgrade_type = upgrade_key_selected # Use the key directly
        
        if self.game_state.purchase_upgrade(upgrade_type):
            spec = config.UPGRADE_SPECS[upgrade_type]
            if upgrade_type == "automation": # Max_level 1 type
                self.view.show_message(f"{spec['name']} purchased!", "success")
            else: # Level based type
                self.view.show_message(f"{spec['name']} upgraded to level {self.game_state.upgrades[upgrade_type]}!", "success")
            # Storage capacity is updated within GameState.purchase_upgrade
            if upgrade_type == "storage":
                 self.view.show_message(f"Storage capacity increased to {self.game_state.storage_capacity}!", "info") # Additional info message

        else:
            # Error messaging improved in GameState.purchase_upgrade or can be handled here based on GameState state
            spec = config.UPGRADE_SPECS[upgrade_type]
            current_level_or_status = self.game_state.upgrades.get(upgrade_type, False if spec["max_level"] == 1 else 0)
            cost = spec['cost'] if spec['max_level'] == 1 else spec['cost_per_level']

            if self.game_state.money < cost:
                self.view.show_message("Not enough money for this upgrade!", "error")
            elif (spec["max_level"] == 1 and current_level_or_status) or \
                 (spec["max_level"] > 1 and current_level_or_status >= spec['max_level']):
                self.view.show_message(f"{spec['name']} is already at maximum or purchased.", "warning")
            else:
                self.view.show_message("Failed to purchase upgrade for an unknown reason.", "error")
    
    def handle_loans(self) -> None:
        """Handle loan management."""
        self.view.display_loan_menu(self.game_state) # Displays current loan, rates, and safe loan recommendation
        
        choice = self.view.get_input("Choose an action (1-Take Loan, 2-Repay Loan, 3-Back): ", ["1", "2", "3"])
        
        if choice == "1":  # Take loan
            max_loan_player_can_take = config.MAX_LOAN_TOTAL - self.game_state.loan
            if max_loan_player_can_take <= 0:
                self.view.show_message("You've reached your maximum loan limit!", "error")
                return
                
            safe_loan_to_take = self.game_state.get_safe_loan_amount()
            prompt_detail = f" (max ${max_loan_player_can_take})"
            if safe_loan_to_take > 0 and safe_loan_to_take <= max_loan_player_can_take:
                prompt_detail += f", recommended: ${safe_loan_to_take}, or type 'max' for ${safe_loan_to_take}"
            else: # If safe loan is 0 or exceeds max_loan_player_can_take, just show max limit
                prompt_detail += f", or type 'max' for ${max_loan_player_can_take}"

            # Use allow_max_str for get_number_input
            amount_input = self.view.get_number_input(f"Enter loan amount{prompt_detail}: ", 0, max_loan_player_can_take, allow_max_str=True)
            
            amount_to_take = 0
            if amount_input == "max":
                # If safe_loan_to_take is positive and within overall limits, prefer it for 'max'
                amount_to_take = safe_loan_to_take if safe_loan_to_take > 0 and safe_loan_to_take <= max_loan_player_can_take else max_loan_player_can_take
            elif isinstance(amount_input, int):
                amount_to_take = amount_input
            
            if amount_to_take > 0:
                # Warning for exceeding safe loan, similar to GUI
                if self.game_state.get_income_potential() > 0 and amount_to_take > safe_loan_to_take and amount_to_take <= max_loan_player_can_take:
                     confirm_risk = self.view.get_input(
                        f"{Fore.YELLOW}Warning: Loan amount ${amount_to_take} exceeds recommended safe loan ${safe_loan_to_take}. Proceed? (y/n):{Style.RESET_ALL} ", 
                        ["y", "n"]
                    )
                     if confirm_risk == 'n':
                         self.view.show_message("Loan cancelled.", "info")
                         return

                if self.game_state.take_loan(amount_to_take):
                    self.view.show_message(f"Loan of ${amount_to_take} received!", "success")
                else:
                    self.view.show_message("Failed to process loan. Ensure amount is positive and within limits.", "error")
            elif amount_input != "max":
                self.view.show_message("No loan taken.", "info")
        
        elif choice == "2":  # Repay loan
            if self.game_state.loan <= 0:
                self.view.show_message("You don't have any outstanding loans.", "warning")
                return
                
            max_repayable_with_money = self.game_state.money
            actual_max_repay = min(self.game_state.loan, max_repayable_with_money)
            
            if actual_max_repay <= 0:
                self.view.show_message("Not enough money to make any repayment!", "error")
                return
            
            # Smart default for CLI repayment: suggest full repayment if possible, else max affordable
            suggested_repay_amount = min(self.game_state.loan, self.game_state.money)
            prompt_detail = f" (max ${actual_max_repay})"
            if suggested_repay_amount > 0:
                prompt_detail += f", suggested: ${suggested_repay_amount}, or type 'max' for ${actual_max_repay}"
            else:
                 prompt_detail += f", or type 'max' for ${actual_max_repay}"

            amount_input = self.view.get_number_input(f"Enter repayment amount{prompt_detail}: ", 0, actual_max_repay, allow_max_str=True)
            
            amount_to_repay = 0
            if amount_input == "max":
                amount_to_repay = actual_max_repay
            elif isinstance(amount_input, int):
                amount_to_repay = amount_input

            if amount_to_repay > 0:
                if self.game_state.repay_loan(amount_to_repay):
                    self.view.show_message(f"Loan repayment of ${amount_to_repay} processed!", "success")
                else:
                    self.view.show_message("Failed to process repayment. Ensure amount is positive and within limits.", "error")
            elif amount_input != "max":
                 self.view.show_message("No repayment made.", "info")

    def handle_rest(self) -> bool: # Returns True if a repeat action was taken for the next day cycle
        """Handle the rest action."""
        rep_gain = self.game_state.rest()
        self.view.show_message(f"You rested and improved your reputation by {rep_gain} points.", "success")
        next_day_action_taken = False

        # Check if can rest again (always possible unless game is over by other means)
        if not self.game_state.is_game_over():
            repeat_choice = self.view.get_input(f"Rest again for Day {self.game_state.day + 1}? (y/n): ", ["y", "n"])
            if repeat_choice == 'y':
                next_day_action_taken = True
                self.view.show_message("Scheduled to rest next day...", "info")
        return next_day_action_taken

    def handle_start_research(self) -> None:
        """Handle starting a new research project."""
        research_choice_key = self.view.display_research_menu(
            config.RESEARCH_PROJECTS_SPECS,
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
            self.view.show_message(f"Research for '{self.event_manager.research_projects_data[self.event_manager.active_research]['name']}' is already in progress.", "warning")
            return

        project_details = self.event_manager.research_projects_data.get(research_choice_key)
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