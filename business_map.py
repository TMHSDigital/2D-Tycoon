from typing import Dict, Any
from colorama import Fore, Style

class BusinessMap:
    def __init__(self, game_state: Dict[str, Any]):
        self.game_state = game_state

    def generate_map(self) -> str:
        """Generate the ASCII map with current game state."""
        map_template = """
┌──────────────────────────┐
│     BUSINESS TYCOON      │
├──────────────────────────┤
│┌─────────┐  ┌─────────┐ │
││{office:<9}│  │{storage:<9}│ │
│└─────────┘  └─────────┘ │
│                         │
│┌─────────┐  ┌─────────┐ │
││{market:<9}│  │{research:<9}│ │
│└─────────┘  └─────────┘ │
│                         │
│ {employees:<11} ┌─────────┐ │
│ Employees    │{upgrades:<9}│ │
│              └─────────┘ │
└──────────────────────────┘"""
        return map_template.format(
            office=self.get_office_status(),
            storage=self.get_storage_status(),
            market=self.get_market_status(),
            research=self.get_research_status(),
            employees=self.get_employees_status(),
            upgrades=self.get_upgrades_status()
        )

    def get_office_status(self) -> str:
        """Get the office status display."""
        return "Office"

    def get_storage_status(self) -> str:
        """Get the storage status with capacity."""
        used = sum(self.game_state['inventory'].values())
        capacity = self.game_state['storage_capacity']
        return f"{used}/{capacity}"

    def get_market_status(self) -> str:
        """Get the market status display."""
        return "Market"

    def get_research_status(self) -> str:
        """Get the research status display."""
        return "Research"

    def get_employees_status(self) -> str:
        """Get the employee status with icons."""
        count = len(self.game_state['employees'])
        return "■ " * count + "□ " * (3 - count)  # Max 3 employees

    def get_upgrades_status(self) -> str:
        """Get the upgrades status display."""
        upgrades = self.game_state['upgrades']
        status = []
        if upgrades['automation']:
            status.append("AUTO")
        if upgrades['marketing'] > 0:
            status.append(f"MKT {upgrades['marketing']}")
        if upgrades['storage'] > 0:
            status.append(f"STR {upgrades['storage']}")
        return "\n".join(status) if status else "NONE"

    def get_map_with_status(self) -> str:
        """Return the map with additional status information."""
        map_art = self.generate_map()
        status = f"""
Current Status:
--------------
Day: {self.game_state['day']}
Money: ${self.game_state['money']}
Reputation: {self.game_state['reputation']}
Loan: ${self.game_state.get('loan', 0)}

Storage Usage: {sum(self.game_state['inventory'].values())}/{self.game_state['storage_capacity']}
Employees: {len(self.game_state['employees'])}
Automation: {"Enabled" if self.game_state['upgrades']['automation'] else "Disabled"}
Marketing Level: {self.game_state['upgrades']['marketing']}"""
        return f"{map_art}{status}"

    def get_cli_colored_map(self) -> str:
        """Return the map with colorama colors for CLI display."""
        map_art = self.generate_map()
        status = f"""
{Fore.CYAN}Current Status:{Style.RESET_ALL}
--------------
Day: {self.game_state['day']}
Money: {Fore.GREEN}${self.game_state['money']}{Style.RESET_ALL}
Reputation: {Fore.YELLOW}{self.game_state['reputation']}{Style.RESET_ALL}
Loan: {Fore.RED}${self.game_state.get('loan', 0)}{Style.RESET_ALL}

Storage Usage: {sum(self.game_state['inventory'].values())}/{self.game_state['storage_capacity']}
Employees: {len(self.game_state['employees'])}
Automation: {Fore.GREEN if self.game_state['upgrades']['automation'] else Fore.RED}{"Enabled" if self.game_state['upgrades']['automation'] else "Disabled"}{Style.RESET_ALL}
Marketing Level: {self.game_state['upgrades']['marketing']}"""
        return f"{Fore.CYAN}{map_art}{Style.RESET_ALL}{status}" 