import random
from typing import Dict, Any
from colorama import Fore, Style

class EventManager:
    def __init__(self):
        self.market_trend = 1.0
        self.competitors = [
            {"name": "SmallBiz Inc.", "market_share": 0.2, "aggressive": False},
            {"name": "MegaCorp", "market_share": 0.4, "aggressive": True}
        ]
        self.research_projects = {
            "efficient_storage": {
                "name": "Efficient Storage Solutions", 
                "cost": 400, 
                "duration": 5, 
                "description": "Increases your total storage capacity by 75 units.",
                "completed": False # Internal flag for EventManager, GameState.completed_research is canonical for player
            },
            "smart_automation": {
                "name": "Smart Automation Systems", 
                "cost": 600, 
                "duration": 7, 
                "description": "Boosts income from automated processes by an additional 10%.",
                "completed": False
            },
            "eco_friendly": {
                "name": "Eco-Friendly Practices", 
                "cost": 300, 
                "duration": 4, 
                "description": "Improves public image, granting a permanent +10 reputation boost.",
                "completed": False
            },
            # Example of a new research project we could add later
            # "advanced_marketing": {
            #     "name": "Advanced Marketing Campaigns",
            #     "cost": 500,
            #     "duration": 6,
            #     "description": "Significantly reduces reputation loss from working and boosts passive reputation gain.",
            #     "completed": False
            # }
        }
        self.active_research = None
        self.research_progress = 0

    def update_market(self) -> Dict[str, Any]:
        """Update market conditions based on competitor actions."""
        competitor_influence = sum(c["market_share"] for c in self.competitors)
        market_pressure = random.uniform(-0.2, 0.2)
        
        # Aggressive competitors have more impact
        for competitor in self.competitors:
            if competitor["aggressive"]:
                market_pressure -= 0.1
        
        self.market_trend = max(0.5, min(2.0, self.market_trend + market_pressure))
        
        events = {
            "market_demand": self.market_trend * (1 - competitor_influence * 0.5),
            "special_event": random.random() < 0.2,
            "market_message": "",
            "competitor_action": None
        }

        # Competitor actions
        if random.random() < 0.3:  # 30% chance of competitor action
            acting_competitor = random.choice(self.competitors)
            action = random.choice(["price_war", "marketing_campaign", "expansion"])
            events["competitor_action"] = {
                "competitor": acting_competitor["name"],
                "action": action
            }

        # Market status messages
        if self.market_trend > 1.2:
            events["market_message"] = f"{Fore.GREEN}The market is booming!{Style.RESET_ALL}"
        elif self.market_trend < 0.8:
            events["market_message"] = f"{Fore.RED}The market is in decline.{Style.RESET_ALL}"

        return events

    def handle_competitor_action(self, action: Dict[str, str]) -> tuple[str, float]:
        """Handle competitor actions and their effects."""
        effects = {
            "price_war": (f"{action['competitor']} started a price war!", -0.2),
            "marketing_campaign": (f"{action['competitor']} launched a major marketing campaign!", -0.1),
            "expansion": (f"{action['competitor']} expanded their business!", -0.15)
        }
        return effects[action["action"]]

    def update_research(self) -> Dict[str, Any]:
        """Update research progress and return research status."""
        if not self.active_research:
            return {"status": "no_research"}
            
        self.research_progress += 1
        project = self.research_projects[self.active_research]
        
        if self.research_progress >= project["duration"]:
            project["completed"] = True
            completed_project = self.active_research
            self.active_research = None
            self.research_progress = 0
            return {
                "status": "completed",
                "project": completed_project
            }
            
        return {
            "status": "in_progress",
            "progress": (self.research_progress / project["duration"]) * 100
        }

    def get_random_event(self) -> Dict[str, Any]:
        """Generate random events that can affect the business."""
        events = [
            {"type": "bonus", "chance": 0.4},
            {"type": "penalty", "chance": 0.3},
            {"type": "opportunity", "chance": 0.2},
            {"type": "employee_event", "chance": 0.1}
        ]
        
        roll = random.random()
        current_threshold = 0
        
        for event in events:
            current_threshold += event["chance"]
            if roll < current_threshold:
                return self._generate_event_details(event["type"])
        
        return {"type": "none"}

    def _generate_event_details(self, event_type: str) -> Dict[str, Any]:
        """Generate detailed event information based on event type."""
        if event_type == "bonus":
            amount = random.randint(20, 50)
            return {
                "type": "bonus",
                "amount": amount,
                "message": f"{Fore.GREEN}SPECIAL EVENT: You received a bonus of ${amount}!{Style.RESET_ALL}"
            }
        elif event_type == "penalty":
            amount = random.randint(10, 30)
            return {
                "type": "penalty",
                "amount": amount,
                "message": f"{Fore.RED}SPECIAL EVENT: You had to pay ${amount} in unexpected costs!{Style.RESET_ALL}"
            }
        elif event_type == "opportunity":
            return {
                "type": "opportunity",
                "message": f"{Fore.YELLOW}SPECIAL EVENT: Market prices are especially favorable tomorrow!{Style.RESET_ALL}",
                "market_boost": 0.3
            }
        elif event_type == "employee_event":
            event = random.choice([
                {"effect": "productivity", "value": 1.5, "duration": 2},
                {"effect": "strike", "value": 0.5, "duration": 1},
                {"effect": "training", "value": 1.2, "duration": 3}
            ])
            return {
                "type": "employee_event",
                "event": event,
                "message": f"{Fore.CYAN}SPECIAL EVENT: Employee morale affected!{Style.RESET_ALL}"
            }
        
        return {"type": "none"} 