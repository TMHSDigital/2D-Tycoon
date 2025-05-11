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
        self.employees = []
        self.market_trend = 1.0
        self.storage_capacity = 50
        self.loan = 0
        self.loan_interest = 0.1  # 10% annual interest rate
        
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
        return True

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
            return True
        except FileNotFoundError:
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
        # Check if supplies are available
        total_supplies = sum(self.inventory.values())
        if total_supplies <= 0:
            return 0

        # Calculate income based on various factors
        base_income = random.randint(40, 80)
        market_modifier = self.market_trend
        automation_bonus = 1.5 if self.upgrades["automation"] else 1.0
        employee_bonus = 1 + (len(self.employees) * 0.4)
        
        income = int(base_income * market_modifier * automation_bonus * employee_bonus)
        
        # Use premium supplies first if available
        if self.inventory["premium_supplies"] > 0:
            income = int(income * 1.5)  # 50% bonus for premium supplies
            self.inventory["premium_supplies"] -= 1
        elif self.inventory["basic_supplies"] > 0:
            self.inventory["basic_supplies"] -= 1
        elif self.inventory["equipment"] > 0:
            # Equipment provides consistency rather than just using up a supply
            income = int(income * 1.3)  # 30% bonus for using equipment
            self.inventory["equipment"] -= 1
        
        self.money += income
        
        # Reputation loss from working
        rep_loss = random.randint(3, 8)
        rep_loss = max(1, rep_loss - self.upgrades["marketing"])  # Marketing reduces reputation loss
        self.reputation -= rep_loss
        
        # Pay employees
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
            self.employees.append({"salary": 150})
            self.money -= 150
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
            
        interest = int(self.loan * self.loan_interest / 365)  # Daily interest
        self.loan += interest
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
        """Advance to the next day."""
        self.day += 1

    def get_income_potential(self) -> int:
        """Calculate potential income based on current stats."""
        if sum(self.inventory.values()) <= 0:
            return 0
            
        base_income = 60  # Average of random 40-80
        automation_bonus = 1.5 if self.upgrades["automation"] else 1.0
        employee_bonus = 1 + (len(self.employees) * 0.4)
        return int(base_income * automation_bonus * employee_bonus)

    def get_safe_loan_amount(self) -> int:
        """Calculate a safe loan amount based on income potential."""
        income_potential = self.get_income_potential()
        max_loan = 1000 - self.loan
        safe_max_loan = min(max_loan, income_potential * 10)
        return safe_max_loan

    def is_game_over(self) -> bool:
        """Check if the game is over (win or lose)."""
        return self.money >= 1000 or self.reputation <= 0

    def is_win(self) -> bool:
        """Check if player has won."""
        return self.money >= 1000 