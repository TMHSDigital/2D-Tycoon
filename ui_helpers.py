from colorama import Fore, Style

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

def display_business_map() -> None:
    """Display an ASCII map of the business."""
    print(f"\n{Fore.CYAN}Your Business Layout:{Style.RESET_ALL}")
    print("""
    ╔════════════════════════════╗
    ║      BUSINESS TYCOON       ║
    ╠════════════════════════════╣
    ║ ┌──────┐    ╭─────────╮   ║
    ║ │Office│    │ Storage │   ║
    ║ └──────┘    ╰─────────╯   ║
    ║                            ║
    ║ ╔══════╗    ┌──────────┐  ║
    ║ ║Market║    │ Research │  ║
    ║ ╚══════╝    └──────────┘  ║
    ║                            ║
    ║   ▣ ▣ ▣     ╔════════╗    ║
    ║ Employees   ║Upgrades║    ║
    ║             ╚════════╝    ║
    ╚════════════════════════════╝
    """) 