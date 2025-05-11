import random
import json
from typing import Dict, Any, List, Optional

class GameState:
    """
    GameState class represents the Model in MVC architecture.
    Encapsulates all game state and business logic.
    """
    def __init__(self):
        # Game state variables
        self.money = 100
        self.reputation = 50
        self.day = 1
        self.inventory = {
            "basic_supplies": 0,
            "premium_supplies": 0,
            "equipment": 0
        }
        self.prices = {
            "basic_supplies": 25,  # Slightly reduced price for better early game
            "premium_supplies": 50,  # Better value compared to basic supplies
            "equipment": 150  # Reduced price to make it more attainable
        }
        self.upgrades = {
            "automation": False,
            "marketing": 0,  # Level 0-3
            "storage": 0     # Level 0-2
        }
        self.employees: List[Dict[str, Any]] = []
        self.market_trend = 1.0 # Initial value, will be synced with EventManager
        self.current_market_demand = 1.0 # Actual demand after competitor/event effects
        self.storage_capacity = 50
        self.loan = 0
        self.loan_interest = 0.1  # 10% annual interest rate
        
        # Research related - for future integration with EventManager.research_projects
        self.research_points = 0
        self.active_research_project: Optional[str] = None
        self.completed_research: List[str] = []
        self.research_progress_today = 0 # Tracks progress made today for display
        self.employee_productivity_modifier = 1.0 # For employee events
        self.employee_event_duration = 0
        
    def save_game(self) -> bool:
        """Save the current game state to a file."""
        game_data = {
            "money": self.money,
            "reputation": self.reputation,
            "day": self.day,
            "inventory": self.inventory,
            "upgrades": self.upgrades,
            "employees": self.employees,
            "loan": self.loan,
            "market_trend": self.market_trend,
            "current_market_demand": self.current_market_demand,
            "storage_capacity": self.storage_capacity,
            # Add research state for saving
            "active_research_project": self.active_research_project,
            "completed_research": self.completed_research,
            "research_points": self.research_points # If EventManager.research_progress is used for this
        }
        try:
            with open("savegame.json", "w") as f:
                json.dump(game_data, f)
            return True
        except IOError:
            return False

    def load_game(self) -> bool:
        """Load the game state from a file."""
        try:
            with open("savegame.json", "r") as f:
                game_data = json.load(f)
                self.money = game_data["money"]
                self.reputation = game_data["reputation"]
                self.day = game_data["day"]
                self.inventory = game_data["inventory"]
                self.upgrades = game_data["upgrades"]
                self.employees = game_data["employees"]
                self.loan = game_data.get("loan", 0)
                self.market_trend = game_data.get("market_trend", 1.0)
                self.current_market_demand = game_data.get("current_market_demand", 1.0)
                self.storage_capacity = game_data.get("storage_capacity", 50)
                # Load research state
                self.active_research_project = game_data.get("active_research_project")
                self.completed_research = game_data.get("completed_research", [])
                self.research_points = game_data.get("research_points", 0)
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False

    def update_daily_market(self) -> Dict[str, Any]:
        """Generate random daily events with market trends."""
        self.market_trend = max(0.5, min(2.0, self.market_trend + random.uniform(-0.2, 0.2)))
        events = {
            "market_demand": self.market_trend,
            "special_event": random.random() < 0.2,
            "market_message": ""
        }
        if self.market_trend > 1.2:
            events["market_message"] = "The market is booming!"
        elif self.market_trend < 0.8:
            events["market_message"] = "The market is in decline."
        return events

    def buy_supplies(self, supply_type: str, amount: int) -> bool:
        """Buy supplies and add to inventory."""
        if supply_type not in self.prices:
            return False
            
        cost = amount * self.prices[supply_type]
        if cost > self.money:
            return False
            
        current_total = sum(self.inventory.values())
        if current_total + amount > self.storage_capacity:
            return False
            
        self.money -= cost
        self.inventory[supply_type] += amount
        return True

    def work(self) -> int:
        """Process one unit of work and return income earned."""
        total_supplies = sum(self.inventory.values())
        if total_supplies <= 0:
            return 0

        base_income = random.randint(40, 80)
        market_modifier = self.current_market_demand 
        
        automation_base_bonus = 1.5 if self.upgrades["automation"] else 1.0
        # Check for research-enhanced automation
        automation_efficiency_bonus = self.upgrades.get("automation_efficiency", 1.0)
        automation_bonus = automation_base_bonus * automation_efficiency_bonus

        employee_bonus = (1 + (len(self.employees) * 0.4)) * self.employee_productivity_modifier
        
        income = int(base_income * market_modifier * automation_bonus * employee_bonus)
        
        if self.inventory["premium_supplies"] > 0:
            income = int(income * 1.5)
            self.inventory["premium_supplies"] -= 1
        elif self.inventory["basic_supplies"] > 0:
            self.inventory["basic_supplies"] -= 1
        elif self.inventory["equipment"] > 0:
            income = int(income * 1.3)
            self.inventory["equipment"] -= 1
        else: # Should not happen if total_supplies > 0, but as a safeguard
            return 0
        
        self.money += income
        rep_loss = random.randint(3, 8)
        rep_loss = max(1, rep_loss - self.upgrades["marketing"])
        self.reputation -= rep_loss
        
        employee_cost = len(self.employees) * 150
        if employee_cost > 0:
            self.money -= employee_cost
        
        return income

    def rest(self) -> int:
        """Handle resting to recover reputation."""
        rep_gain = 10 + (self.upgrades["marketing"] * 2)
        self.reputation += rep_gain
        return rep_gain

    def hire_employee(self) -> bool:
        """Hire a new employee."""
        if self.money >= 150:
            self.employees.append({"salary": 150, "id": random.randint(1000,9999)})
            # self.money -= 150 # Decided that salary is paid daily during work/end of day
            return True
        return False

    def fire_employee(self) -> bool:
        """Fire the most recently hired employee."""
        if self.employees:
            self.employees.pop()
            return True
        return False

    def purchase_upgrade(self, upgrade_type: str) -> bool:
        """Purchase a business upgrade."""
        upgrade_costs = {
            "automation": 400,
            "marketing": 250,
            "storage": 150
        }
        
        if upgrade_type not in upgrade_costs:
            return False
            
        cost = upgrade_costs[upgrade_type]
        if self.money < cost:
            return False
            
        if upgrade_type == "automation" and not self.upgrades["automation"]:
            self.money -= cost
            self.upgrades["automation"] = True
            return True
        elif upgrade_type == "marketing" and self.upgrades["marketing"] < 3:
            self.money -= cost
            self.upgrades["marketing"] += 1
            return True
        elif upgrade_type == "storage" and self.upgrades["storage"] < 2:
            self.money -= cost
            self.upgrades["storage"] += 1
            self.storage_capacity += 50
            return True
            
        return False

    def take_loan(self, amount: int) -> bool:
        """Take a loan."""
        max_loan = 1000 - self.loan
        if amount <= 0 or amount > max_loan:
            return False
            
        self.loan += amount
        self.money += amount
        return True

    def repay_loan(self, amount: int) -> bool:
        """Repay a portion of the loan."""
        if amount <= 0 or amount > self.loan or amount > self.money:
            return False
            
        self.loan -= amount
        self.money -= amount
        return True

    def apply_daily_interest(self) -> int:
        """Apply daily interest to the loan and return the interest amount."""
        if self.loan <= 0:
            return 0
            
        interest = int(self.loan * self.loan_interest / 365)
        self.loan += interest # Interest adds to principal
        # self.money -= interest # Interest is not automatically paid from cash, it increases loan amount
        return interest

    def handle_special_event(self, event_type: str) -> Dict[str, Any]:
        """Handle a special event and return its effects."""
        results = {"message": "", "effect": 0}
        
        if event_type == "bonus":
            bonus = random.randint(20, 50)
            self.money += bonus
            results["message"] = f"You received a bonus of ${bonus}!"
            results["effect"] = bonus
        elif event_type == "penalty":
            penalty = random.randint(10, 30)
            self.money -= penalty
            results["message"] = f"You had to pay ${penalty} in unexpected costs!"
            results["effect"] = -penalty
        elif event_type == "opportunity":
            self.market_trend = min(2.0, self.market_trend + 0.3)
            results["message"] = "Market prices are especially favorable tomorrow!"
            results["effect"] = 0.3
            
        return results

    def advance_day(self) -> None:
        """Advance to the next day and handle daily decay/updates."""
        self.day += 1
        self.research_progress_today = 0 # Reset for next day
        if self.employee_event_duration > 0:
            self.employee_event_duration -=1
            if self.employee_event_duration == 0:
                self.employee_productivity_modifier = 1.0 # Reset modifier

    def get_income_potential(self) -> int:
        """Calculate potential income based on current stats."""
        if sum(self.inventory.values()) <= 0:
            return 0
            
        base_income = 60  # Average of random 40-80
        automation_bonus = 1.5 if self.upgrades["automation"] else 1.0
        employee_bonus = (1 + (len(self.employees) * 0.4)) * self.employee_productivity_modifier
        return int(base_income * automation_bonus * employee_bonus)

    def get_safe_loan_amount(self) -> int:
        """Calculate a safe loan amount based on income potential."""
        income_potential = self.get_income_potential()
        max_loan_cap = 1000 # Absolute max loan
        max_allowed_based_on_current_loan = max_loan_cap - self.loan
        safe_max_loan = min(max_allowed_based_on_current_loan, income_potential * 10)
        return max(0, safe_max_loan) # Ensure it's not negative

    def is_game_over(self) -> bool:
        """Check if the game is over (win or lose)."""
        return self.money >= 1000 or self.reputation <= 0

    def is_win(self) -> bool:
        """Check if player has won."""
        return self.money >= 1000 

    # --- New methods for EventManager Integration ---
    def apply_competitor_effect(self, effect_value: float) -> None:
        """Apply effects from competitor actions."""
        # Example: Competitor action might negatively impact market trend further or player reputation
        self.market_trend = max(0.3, min(2.5, self.market_trend + effect_value)) # Adjust market trend limits slightly
        # Could also impact reputation directly: self.reputation = max(0, self.reputation + int(effect_value * 50))

    def apply_random_event_effect(self, event_details: Dict[str, Any]) -> None:
        """Apply effects of a random event from EventManager."""
        event_type = event_details.get("type")
        if event_type == "bonus":
            self.money += event_details.get("amount", 0)
        elif event_type == "penalty":
            self.money -= event_details.get("amount", 0)
            self.money = max(0, self.money) # Prevent negative money from this event alone
        elif event_type == "opportunity":
            self.market_trend = min(2.5, self.market_trend + event_details.get("market_boost", 0))
        elif event_type == "employee_event":
            emp_event = event_details.get("event", {})
            self.employee_productivity_modifier = emp_event.get("value", 1.0)
            self.employee_event_duration = emp_event.get("duration", 0)
            # The message is in event_details["message"]

    def apply_research_completion(self, project_key: Optional[str]) -> None:
        """Apply benefits of a completed research project."""
        if not project_key or project_key in self.completed_research:
            return
        
        # Effects based on the updated research_projects in EventManager
        if project_key == "efficient_storage":
            self.storage_capacity += 75 # Changed from 50 to 75 to match description
            self.completed_research.append(project_key)
        elif project_key == "smart_automation":
            self.upgrades["automation_efficiency"] = self.upgrades.get("automation_efficiency", 1.0) * 1.1 
            self.completed_research.append(project_key)
        elif project_key == "eco_friendly":
            self.reputation = min(100, self.reputation + 10)
            self.completed_research.append(project_key)
        # Add more elif blocks here for future research projects
        
        if project_key in self.completed_research: # Check if it was successfully processed
            self.active_research_project = None # Clear active project in GameState 