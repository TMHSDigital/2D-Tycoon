from colorama import Fore, Style
from typing import Dict, Any
from business_map import BusinessMap

def create_progress_bar(progress: float, width: int = 20) -> str:
    """Create a colored progress bar."""
    filled = int(width * progress / 100)
    bar = '█' * filled + '░' * (width - filled)
    color = Fore.GREEN if progress >= 66 else Fore.YELLOW if progress >= 33 else Fore.RED
    return f"{color}{bar}{Style.RESET_ALL} {progress:.1f}%"

def create_resource_bar(current: float, maximum: float, width: int = 20) -> str:
    """Create a resource bar (e.g., for storage capacity)."""
    progress = (current / maximum) * 100 if maximum > 0 else 0
    return create_progress_bar(progress, width)

def display_help() -> None:
    """Display game help and tips."""
    print(f"\n{Fore.CYAN}=== Business Tycoon Help ==={Style.RESET_ALL}")
    print("\nBasic Mechanics:")
    print("- Buy supplies to sell for profit")
    print("- Manage your reputation through work and rest")
    print("- Hire employees to increase productivity")
    print("- Research new technologies for advantages")
    
    print("\nAdvanced Strategies:")
    print("1. Resource Management")
    print("   - Keep a balance of basic and premium supplies")
    print("   - Monitor storage capacity")
    print("   - Maintain cash reserves for opportunities")
    
    print("\n2. Employee Management")
    print("   - Each employee increases productivity by 20%")
    print("   - Balance employee costs with income")
    print("   - Watch for employee events")
    
    print("\n3. Research & Upgrades")
    print("   - Prioritize research based on your strategy")
    print("   - Automation helps with efficiency")
    print("   - Marketing reduces reputation loss")
    
    print("\n4. Market Strategy")
    print("   - Watch for market trends")
    print("   - Monitor competitor actions")
    print("   - Use loans strategically")
    
    print(f"\n{Fore.YELLOW}Remember: The goal is to reach $1000 while keeping reputation above 0!{Style.RESET_ALL}")

def display_business_map(game_state: Dict[str, Any]) -> None:
    """Display an ASCII map of the business with colored CLI output."""
    map_instance = BusinessMap(game_state)
    print(f"\n{Fore.CYAN}Your Business Layout:{Style.RESET_ALL}")
    print(map_instance.get_cli_colored_map())

def display_header() -> None:
    """Display the game header with ASCII art."""
    header = """
    ____             _                     
   / __ )__  _______(_)___  ___  __________
  / __  / / / / ___/ / __ \/ _ \/ ___/ ___/
 / /_/ / /_/ (__  ) / / / /  __(__  |__  ) 
/_____/\__,_/____/_/_/ /_/\___/____/____/  
                                           
  ______                                    
 /_  __/_  ___________  ____  ____         
  / / / / / / ___/ __ \/ __ \/ __ \        
 / / / /_/ / /__/ /_/ / /_/ / / / /        
/_/  \__, /\___/\____/\____/_/ /_/         
    /____/                                  
"""
    print(f"{Fore.CYAN}{header}{Style.RESET_ALL}")

def display_menu() -> None:
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

def display_status(game_state: Dict[str, Any]) -> None:
    """Display the current game status."""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}Day {game_state['day']}{Style.RESET_ALL}")
    print(f"Money: ${game_state['money']}")
    print(f"Reputation: {game_state['reputation']}")
    
    if game_state.get('loan', 0) > 0:
        print(f"{Fore.RED}Loan: ${game_state['loan']}{Style.RESET_ALL}")
    
    print("\nInventory:")
    for item, amount in game_state['inventory'].items():
        print(f"  {item.replace('_', ' ').title()}: {amount}")
    
    print("\nUpgrades:")
    for upgrade, level in game_state['upgrades'].items():
        if isinstance(level, bool):
            status = f"{Fore.GREEN}Enabled{Style.RESET_ALL}" if level else f"{Fore.RED}Disabled{Style.RESET_ALL}"
        else:
            status = f"Level {level}"
        print(f"  {upgrade.replace('_', ' ').title()}: {status}")
    
    if game_state['employees']:
        print(f"\nEmployees: {len(game_state['employees'])}")
    
    print("="*60) 