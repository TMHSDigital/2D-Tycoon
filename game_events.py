import random
from typing import Dict, Any
from colorama import Fore, Style
import config # Import the config file

class EventManager:
    def __init__(self):
        self.market_trend = config.MARKET_TREND_INITIAL
        self.competitors = [
            {"name": "SmallBiz Inc.", "market_share": 0.2, "aggressive": False},
            {"name": "MegaCorp", "market_share": 0.4, "aggressive": True}
        ]
        # Research projects are now primarily defined in config.RESEARCH_PROJECTS_SPECS
        # EventManager will use it for names, costs, durations but won't store its own full copy for effects.
        self.research_projects_data = config.RESEARCH_PROJECTS_SPECS.copy()
        # Add a 'completed' flag for EventManager's internal tracking if needed for its own logic,
        # but GameState.completed_research is the source of truth for player progression.
        for key in self.research_projects_data:
            self.research_projects_data[key]['completed'] = False # Initial runtime state
            
        self.active_research: Optional[str] = None
        self.research_progress = 0

    def update_market(self) -> Dict[str, Any]:
        """Update market conditions based on competitor actions."""
        competitor_influence = sum(c["market_share"] for c in self.competitors)
        market_pressure = random.uniform(config.MARKET_TREND_DAILY_FLUCTUATION_RANGE[0], config.MARKET_TREND_DAILY_FLUCTUATION_RANGE[1])
        
        for competitor in self.competitors:
            if competitor["aggressive"]:
                market_pressure += config.AGGRESSIVE_COMPETITOR_MARKET_PRESSURE
        
        self.market_trend = max(config.MARKET_TREND_MIN, min(config.MARKET_TREND_MAX, self.market_trend + market_pressure))
        
        events = {
            "market_demand": self.market_trend * (1 - competitor_influence * config.COMPETITOR_INFLUENCE_FACTOR_ON_DEMAND),
            "special_event": random.random() < config.SPECIAL_EVENT_CHANCE,
            "market_message": "",
            "competitor_action": None
        }

        if random.random() < config.COMPETITOR_ACTION_CHANCE:
            acting_competitor = random.choice(self.competitors)
            action_type = random.choice(list(config.COMPETITOR_EFFECTS.keys()))
            events["competitor_action"] = {
                "competitor": acting_competitor["name"],
                "action": action_type
            }

        if self.market_trend > config.MARKET_BOOM_THRESHOLD:
            events["market_message"] = f"{Fore.GREEN}The market is booming!{Style.RESET_ALL}"
        elif self.market_trend < config.MARKET_DECLINE_THRESHOLD:
            events["market_message"] = f"{Fore.RED}The market is in decline.{Style.RESET_ALL}"
        return events

    def handle_competitor_action(self, action_details: Dict[str, str]) -> tuple[str, float]:
        """Handle competitor actions and their effects."""
        competitor_name = action_details["competitor"]
        action_type = action_details["action"]
        effect_spec = config.COMPETITOR_EFFECTS.get(action_type)
        if effect_spec:
            message = effect_spec["message_template"].format(competitor_name)
            return message, effect_spec["market_trend_effect"]
        return f"{competitor_name} did something unexpected!", 0.0

    def update_research(self) -> Dict[str, Any]:
        """Update research progress and return research status."""
        if not self.active_research:
            return {"status": "no_research"}
            
        self.research_progress += 1
        # Use self.research_projects_data which refers to config specs
        project_config = self.research_projects_data[self.active_research]
        project_duration = project_config["duration"]
        
        if self.research_progress >= project_duration:
            # The 'completed' flag in self.research_projects_data is just for EventManager's internal reference if needed.
            # GameState.completed_research is the canonical list of *player completed* projects.
            # If we want to mark it here for some reason: 
            # self.research_projects_data[self.active_research]['completed'] = True
            
            completed_project_key = self.active_research
            self.active_research = None
            self.research_progress = 0
            return {
                "status": "completed",
                "project": completed_project_key
            }
            
        return {
            "status": "in_progress",
            "progress": (self.research_progress / project_duration) * 100 if project_duration > 0 else 0
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