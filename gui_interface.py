import tkinter as tk
from tkinter import ttk, messagebox
from business_map import BusinessMap
from game_state import GameState
from colorama import Fore, Style
from typing import Optional, Any
import config # Import config

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", foreground="black",
                         relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class TycoonGUI:
    def __init__(self, game_state: GameState, controller: Optional[Any] = None):
        """Initialize the GUI with a GameState instance and optional controller reference."""
        self.game = game_state
        self.controller_ref = controller
        self.root = tk.Tk()
        self.root.title("Business Tycoon Adventure")
        self.root.geometry("900x700") # Increased window size
        self.root.configure(bg="#f0f0f0") # Light grey background

        # --- Style Configuration ---
        self.style = ttk.Style(self.root)
        available_themes = self.style.theme_names()
        if "clam" in available_themes:
            self.style.theme_use("clam") 
        elif "alt" in available_themes:
            self.style.theme_use("alt")
        # Modern font and color palette
        base_font = ("Segoe UI", 11)
        header_font = ("Segoe UI", 14, "bold")
        subheader_font = ("Segoe UI", 12, "bold")
        light_font = ("Segoe UI", 10, "normal")
        # Fallbacks for non-Windows
        try:
            self.root.option_add("*Font", "Segoe UI 11")
        except:
            self.root.option_add("*Font", "Arial 11")
        # Backgrounds
        self.style.configure("TFrame", background="#f7f9fa")
        self.style.configure("Background.TFrame", background="#f7f9fa")
        self.style.configure("TLabel", background="#f7f9fa", foreground="#222", font=base_font)
        self.style.configure("Header.TLabel", background="#f7f9fa", foreground="#00529B", font=header_font)
        self.style.configure("SubHeader.TLabel", background="#f7f9fa", foreground="#0078D4", font=subheader_font)
        self.style.configure("Light.TLabel", background="#f7f9fa", foreground="#666", font=light_font)
        # Button style: rounded, soft blue, drop shadow, hover effect
        self.style.configure("Modern.TButton", font=base_font, padding=12, relief="flat", borderwidth=0,
            background="#2196F3", foreground="#fff")
        self.style.map("Modern.TButton",
            background=[('active', '#42a5f5'), ('!active', '#2196F3')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        # Add rounded corners and shadow via tk widget config (ttk doesn't support natively, so use tk.Button for extra polish if desired)
        # Progress bars: rounded, gradient, icon at end
        self.style.layout("Rounded.Horizontal.TProgressbar",
            [('Horizontal.Progressbar.trough', {'children': [
                ('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'}),
                ('Horizontal.Progressbar.label', {'sticky': ''})], 'sticky': 'nswe'})])
        self.style.configure("Rounded.Horizontal.TProgressbar", thickness=22, background="#4fc3f7", troughcolor="#e3eaf0", borderwidth=0)
        self.style.configure("Green.Horizontal.TProgressbar", thickness=22, background="#66bb6a", troughcolor="#e3eaf0", borderwidth=0)
        self.style.configure("Red.Horizontal.TProgressbar", thickness=22, background="#ef5350", troughcolor="#e3eaf0", borderwidth=0)
        self.style.configure("Yellow.Horizontal.TProgressbar", thickness=22, background="#ffd54f", troughcolor="#e3eaf0", borderwidth=0)
        # Section/card style
        self.style.configure("Card.TLabelframe", background="#f7f9fa", borderwidth=0, relief="flat", font=subheader_font)
        self.style.configure("Card.TLabelframe.Label", background="#f7f9fa", foreground="#00529B", font=subheader_font)
        
        self.setup_keyboard_shortcuts()
        self.setup_ui()

    def setup_keyboard_shortcuts(self):
        self.root.bind("<Control-s>", lambda e: self.save_game())
        self.root.bind("<Control-q>", lambda e: self.quit_game())
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<F2>", lambda e: self.show_business_map())

    def show_help(self, event=None):
        help_text = """
Keyboard Shortcuts:
------------------
Ctrl+S: Save Game
Ctrl+Q: Quit Game
F1: Show Help
F2: Show Business Map

Game Tips:
---------
• Buy supplies to start making money
• Rest when reputation is low
• Hire employees to increase productivity
• Use loans carefully - interest adds up!
• Upgrade your business for better returns
"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Help & Game Tips") # Updated title
        dialog.geometry("450x350") # Adjusted size
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TFrame", background="#f0f0f0")

        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill=tk.BOTH, expand=True)
        
        text_frame = ttk.Frame(main_dialog_frame, borderwidth=1, relief="sunken", style="Dialog.TFrame") # Added frame for text
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        text = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10, font=("Segoe UI", 10), 
                       bg="#ffffff", fg="#333333", relief="flat", borderwidth=0)
        text.insert("1.0", help_text)
        text.config(state="disabled")
        text.pack(fill=tk.BOTH, expand=True)
        
        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0))

        # Key bindings
        dialog.bind("<Escape>", lambda e: close_button.invoke())
        dialog.bind("<Return>", lambda e: close_button.invoke())
        dialog.focus_set()

    def show_business_map(self, event=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Business Map Overview") # Updated title
        dialog.geometry("480x550") # Adjusted size
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Courier", 11)) # Courier for map
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TFrame", background="#f0f0f0")

        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create map instance with current game state
        game_state_dict = {
            'day': self.game.day,
            'money': self.game.money,
            'reputation': self.game.reputation,
            'loan': self.game.loan,
            'inventory': self.game.inventory,
            'storage_capacity': self.game.storage_capacity,
            'employees': self.game.employees,
            'upgrades': self.game.upgrades
        }
        map_instance = BusinessMap(game_state_dict)
        
        map_frame = ttk.Frame(main_dialog_frame, borderwidth=1, relief="sunken", style="Dialog.TFrame")
        map_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        map_label = ttk.Label(map_frame, text=map_instance.get_map_with_status(), 
                            style="Dialog.TLabel", justify=tk.LEFT, padding=10)
        map_label.pack(fill=tk.BOTH, expand=True)
        
        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0))

        # Key bindings
        dialog.bind("<Escape>", lambda e: close_button.invoke())
        dialog.bind("<Return>", lambda e: close_button.invoke())
        dialog.focus_set()

    # Method to show generic messages, similar to CLIView
    def show_message(self, message: str, message_type: str = "info") -> None:
        """Show a message to the user using a messagebox."""
        # Sanitize Colorama codes for GUI display
        clean_message = message.replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Fore.CYAN, "").replace(Style.RESET_ALL, "")
        
        if message_type == "success":
            messagebox.showinfo("Success", clean_message)
        elif message_type == "error":
            messagebox.showerror("Error", clean_message)
        elif message_type == "warning":
            messagebox.showwarning("Warning", clean_message)
        else: # info and other types
            messagebox.showinfo("Information", clean_message)

    def display_market_message(self, message: str) -> None:
        """Display market trend message (could be a status bar update or temp label in GUI)."""
        # For now, use the generic show_message. Can be enhanced later.
        # Sanitize Colorama codes for GUI display
        clean_message = message.replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "")
        message_type = "info"
        if "booming" in clean_message.lower(): message_type = "success"
        if "decline" in clean_message.lower(): message_type = "error"
        self.show_message(f"Market Update: {clean_message}", message_type)

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="32 32 32 32", style="Background.TFrame") # More padding
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.configure(style="Background.TFrame")
        self.style.configure("Background.TFrame", background="#f7f9fa")

        # Status Display with Progress Bars
        self.status_frame = ttk.LabelFrame(main_frame, text="Business Status", padding="20 20 20 20", style="Card.TLabelframe")
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 28))

        # Money and Reputation Progress Bars
        money_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        money_frame.pack(fill="x", pady=10)
        ttk.Label(money_frame, text="Money:", style="SubHeader.TLabel").pack(side="left", padx=(0,8))
        self.money_progress = ttk.Progressbar(money_frame, length=250, mode='determinate', style="Green.Horizontal.TProgressbar")
        self.money_progress.pack(side="left", padx=8, fill="x", expand=True)
        self.money_icon = ttk.Label(money_frame, text="💰", style="Light.TLabel")
        self.money_icon.pack(side="left", padx=(8,0))
        self.money_label = ttk.Label(money_frame, text="$0", style="SubHeader.TLabel")
        self.money_label.pack(side="left", padx=(8,0))

        rep_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        rep_frame.pack(fill="x", pady=10)
        ttk.Label(rep_frame, text="Reputation:", style="SubHeader.TLabel").pack(side="left", padx=(0,8))
        self.rep_progress = ttk.Progressbar(rep_frame, length=250, mode='determinate', style="Yellow.Horizontal.TProgressbar")
        self.rep_progress.pack(side="left", padx=8, fill="x", expand=True)
        self.rep_icon = ttk.Label(rep_frame, text="⭐", style="Light.TLabel")
        self.rep_icon.pack(side="left", padx=(8,0))
        self.rep_label = ttk.Label(rep_frame, text="0", style="SubHeader.TLabel")
        self.rep_label.pack(side="left", padx=(8,0))

        # Inventory Display (Improved with labels and a frame)
        inventory_outer_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        inventory_outer_frame.pack(pady=16, fill="x")
        
        ttk.Label(inventory_outer_frame, text="Current Day & Inventory:", style="SubHeader.TLabel").pack(anchor="w", pady=(0,8))
        
        self.inventory_text_frame = ttk.Frame(inventory_outer_frame, borderwidth=1, relief="groove", style="TFrame")
        self.inventory_text_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        self.inventory_text = tk.Text(self.inventory_text_frame, height=7, width=45, font=("Consolas", 11), 
                                      bg="#ffffff", fg="#333333", relief="flat", borderwidth=0,
                                      padx=14, pady=14) # Increased height and padding
        self.inventory_text.pack(fill="both", expand=True)
        self.inventory_text.config(state='disabled')

        # Action Buttons Frame with Tooltips
        actions_frame = ttk.LabelFrame(main_frame, text="Game Actions", padding="20 20 20 20", style="Card.TLabelframe")
        actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=18)

        # Define actions and their commands
        # Upgrades and Research will use data from config
        action_definitions = [
            {"text": "Buy Supplies", "command": self.buy_supplies, "tooltip": "Purchase supplies to sell for profit"},
            {"text": "Work", "command": self.work, "tooltip": "Sell supplies to earn money"},
            {"text": "Manage Employees", "command": self.manage_employees, "tooltip": "Hire or fire employees"},
            {"text": f"Upgrades ({config.UPGRADE_SPECS['automation']['name']}, etc.)", "command": self.handle_upgrades_dialog, "tooltip": "Purchase business improvements"},
            {"text": "Loans", "command": self.handle_loans_dialog, "tooltip": "Take or pay back loans"},
            {"text": "Rest", "command": self.rest, "tooltip": "Rest to improve reputation"},
            {"text": f"Research ({config.RESEARCH_PROJECTS_SPECS[next(iter(config.RESEARCH_PROJECTS_SPECS))]['name']}, etc.)", "command": self.handle_research_dialog, "tooltip": "Manage R&D projects"}, # Updated text for Research
            {"text": "Save Game", "command": self.save_game, "tooltip": "Save your progress (Ctrl+S)"},
            {"text": "Quit", "command": self.quit_game, "tooltip": "Exit the game (Ctrl+Q)"}
        ]

        row, col = 0, 0
        for i, action_spec in enumerate(action_definitions):
            btn = ttk.Button(actions_frame, text=action_spec["text"], command=action_spec["command"], style="Modern.TButton")
            btn.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
            ToolTip(btn, action_spec["tooltip"])
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Map Button - ensure it's placed correctly after dynamic buttons
        if col == 0: # starts a new row
            map_btn_row = row
            map_btn_col = 0
        else: # place on current row, next column
            map_btn_row = row 
            map_btn_col = col

        map_btn = ttk.Button(actions_frame, text="Show Map", command=self.show_business_map, style="Modern.TButton")
        map_btn.grid(row=map_btn_row, column=map_btn_col, padx=14, pady=10, sticky="ew")
        ToolTip(map_btn, "View business layout (F2)")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        # Update initial status
        self.update_status()

    def update_status(self):
        # Update progress bars
        money_percent = (self.game.money / 1000) * 100 if self.game.money < 1000 else 100
        self.money_progress['value'] = money_percent
        self.money_label['text'] = f"${self.game.money}"
        if money_percent < 33: self.money_progress.configure(style="Red.Horizontal.TProgressbar")
        elif money_percent < 66: self.money_progress.configure(style="Yellow.Horizontal.TProgressbar")
        else: self.money_progress.configure(style="Green.Horizontal.TProgressbar")
        
        rep_percent = self.game.reputation
        self.rep_progress['value'] = rep_percent
        self.rep_label['text'] = str(self.game.reputation)
        if rep_percent < 33: self.rep_progress.configure(style="Red.Horizontal.TProgressbar")
        elif rep_percent < 66: self.rep_progress.configure(style="Yellow.Horizontal.TProgressbar")
        else: self.rep_progress.configure(style="Green.Horizontal.TProgressbar")

        # Update inventory display
        self.inventory_text.config(state='normal')
        self.inventory_text.delete(1.0, tk.END)
        inventory_text_content = f"Day: {self.game.day}\n\nInventory:\n"
        for item, amount in self.game.inventory.items():
            inventory_text_content += f"  {item.replace('_', ' ').title()}: {amount}\n"
        inventory_text_content += f"  Storage: {sum(self.game.inventory.values())}/{self.game.storage_capacity}\n"
        
        inventory_text_content += "\nUpgrades:\n"
        for ug_key, ug_spec in config.UPGRADE_SPECS.items():
            level_or_status = self.game.upgrades.get(ug_key, False if ug_spec["max_level"] == 1 else 0)
            status_text = ""
            if ug_spec["max_level"] == 1:
                status_text = "Enabled" if level_or_status else "Disabled"
            else:
                status_text = f"Level {level_or_status}/{ug_spec['max_level']}"
            inventory_text_content += f"  {ug_spec['name']}: {status_text}\n"
        # Researched automation efficiency
        if self.game.upgrades.get("automation_efficiency", 1.0) > 1.0:
            inventory_text_content += f"    └ Smart Automation Bonus: {((self.game.upgrades['automation_efficiency'] - 1) * 100):.0f}%\n"

        if self.game.employees:
             inventory_text_content += f"\nEmployees: {len(self.game.employees)}/{config.MAX_EMPLOYEES}\n"
        if self.game.loan > 0:
            inventory_text_content += f"Loan: ${self.game.loan}\n"

        if self.game.active_research_project and self.controller_ref:
            event_mngr = self.controller_ref.event_manager
            active_proj_spec = config.RESEARCH_PROJECTS_SPECS.get(self.game.active_research_project)
            if active_proj_spec:
                progress = event_mngr.research_progress
                duration = active_proj_spec['duration']
                progress_percent = (progress / duration) * 100 if duration > 0 else 0
                inventory_text_content += f"\nActive Research: {active_proj_spec['name']} ({progress}/{duration} - {progress_percent:.0f}%)\n"

        self.inventory_text.insert(1.0, inventory_text_content)
        self.inventory_text.config(state='disabled')

    def buy_supplies(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Supplies")
        dialog.geometry("380x350") # Adjusted size for new button
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TCombobox", font=("Segoe UI", 10))
        style.configure("Dialog.TEntry", font=("Segoe UI", 10))
        style.configure("Dialog.TFrame", background="#f0f0f0")

        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)
        
        supply_var = tk.StringVar()
        amount_var = tk.StringVar()
        
        ttk.Label(main_dialog_frame, text="Select supply type:", style="Dialog.TLabel").pack(pady=(0,5), anchor="w")
        supply_combo = ttk.Combobox(main_dialog_frame, textvariable=supply_var, style="Dialog.TCombobox", width=30, state="readonly")
        supply_combo['values'] = [s.replace('_',' ').title() for s in config.SUPPLY_PRICES.keys()]
        supply_combo.pack(pady=5, fill="x")
        
        amount_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        amount_frame.pack(fill="x", pady=(10,0))

        ttk.Label(amount_frame, text="Amount:", style="Dialog.TLabel").pack(side=tk.LEFT, anchor="w")
        amount_entry = ttk.Entry(amount_frame, textvariable=amount_var, style="Dialog.TEntry", width=10)
        amount_entry.pack(side=tk.LEFT, padx=(5,10), fill="x", expand=True)

        def calculate_and_set_max(*args):
            selected_supply_display = supply_var.get()
            if not selected_supply_display:
                self.show_message("Please select a supply type first.", "warning")
                return

            supply_type_key = selected_supply_display.lower().replace(' ', '_')
            
            if supply_type_key not in self.game.prices:
                self.show_message("Invalid supply type selected for max calculation.", "error")
                return

            price_per_unit = self.game.prices[supply_type_key]
            if price_per_unit <= 0: # Avoid division by zero
                 amount_var.set("0")
                 update_price() # Update total cost to $0
                 return

            max_affordable = self.game.money // price_per_unit
            
            current_storage_used = sum(self.game.inventory.values())
            available_storage = self.game.storage_capacity - current_storage_used
            max_storable = max(0, available_storage)
            
            actual_max = min(max_affordable, max_storable)
            amount_var.set(str(actual_max))
            update_price() # Ensure total cost updates after setting max

        buy_max_button = ttk.Button(amount_frame, text="Buy Max", command=calculate_and_set_max, style="Dialog.TButton")
        buy_max_button.pack(side=tk.LEFT, padx=5)
        
        price_label = ttk.Label(main_dialog_frame, text="Total Cost: $0", style="Dialog.TLabel")
        price_label.pack(pady=(10,5))
        
        def update_price(*args):
            supply_type_display = supply_var.get()
            supply_type_key = supply_type_display.lower().replace(' ', '_')
            try:
                amount = int(amount_var.get() or 0)
                if supply_type_key in self.game.prices:
                    total = amount * self.game.prices[supply_type_key]
                    price_label['text'] = f"Total Cost: ${total}"
                else:
                    price_label['text'] = "Total Cost: $--"
            except ValueError:
                price_label['text'] = "Enter a valid amount"
        
        supply_var.trace_add('write', update_price) # Use trace_add
        amount_var.trace_add('write', update_price) # Use trace_add
        if supply_combo['values']:
            supply_combo.current(0) # Select first item by default and trigger update_price
        
        def handle_purchase():
            supply_type_key = supply_var.get().lower().replace(' ', '_')
            try:
                amount = int(amount_var.get())
                if not supply_type_key or supply_type_key not in self.game.prices:
                    messagebox.showerror("Error", "Please select a valid supply type.")
                    return
                
                # GameState.buy_supplies handles the logic for cost, money, storage checks
                if self.game.buy_supplies(supply_type_key, amount):
                    cost = amount * self.game.prices[supply_type_key] # For display message only
                    messagebox.showinfo("Success", f"Bought {amount} {supply_type_key.replace('_',' ').title()} for ${cost}.")
                    self.update_status()
                    dialog.destroy()
                else:
                    # More specific error based on why it might have failed
                    price_per_unit = self.game.prices.get(supply_type_key, 0)
                    cost = amount * price_per_unit if price_per_unit > 0 else float('inf')
                    current_storage_used = sum(self.game.inventory.values())
                    available_storage = self.game.storage_capacity - current_storage_used

                    if self.game.money < cost and available_storage < amount:
                        messagebox.showerror("Error", "Not enough money AND storage space!")
                    elif self.game.money < cost:
                        messagebox.showerror("Error", "Not enough money!")
                    elif available_storage < amount:
                        messagebox.showerror("Error", "Not enough storage space!")
                    else:
                        messagebox.showerror("Error", "Could not complete purchase. Unknown reason.")

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount for supplies.")
        
        button_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        button_frame.pack(pady=(15,0), fill="x")

        # Store buttons for key binding
        purchase_button = ttk.Button(button_frame, text="Purchase", command=handle_purchase, style="Dialog.TButton")
        purchase_button.pack(side=tk.LEFT, expand=True, padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=dialog.destroy, style="Dialog.TButton")
        cancel_button.pack(side=tk.RIGHT, expand=True, padx=5)

        # Key bindings
        dialog.bind("<Escape>", lambda e: cancel_button.invoke())
        dialog.bind("<Return>", lambda e: purchase_button.invoke())
        amount_entry.bind("<Return>", lambda e: purchase_button.invoke()) # Also allow enter from amount entry
        
        # Ensure one of the input fields gets focus initially
        supply_combo.focus_set()

    def work(self):
        if sum(self.game.inventory.values()) > 0:
            result = self.game.work()
            self.update_status()
            
            # Visual feedback for money earned
            self.money_label.config(foreground="green")
            self.root.after(1000, lambda: self.money_label.config(foreground="black"))
            
            # Visual feedback for reputation loss
            self.rep_label.config(foreground="red")
            self.root.after(1000, lambda: self.rep_label.config(foreground="black"))
            
            messagebox.showinfo("Work Result", f"You earned ${result}!")
        else:
            messagebox.showerror("Error", "You need supplies to work!")

    def manage_employees(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Employees")
        dialog.geometry("350x280") # Adjusted size for close button
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TFrame", background="#f0f0f0")
        
        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)

        ttk.Label(main_dialog_frame, text=f"Current employees: {len(self.game.employees)}", style="Dialog.TLabel").pack(pady=5, anchor="w")
        ttk.Label(main_dialog_frame, text=f"Daily cost per employee: ${config.EMPLOYEE_DAILY_SALARY}", style="Dialog.TLabel").pack(pady=5, anchor="w")
        ttk.Label(main_dialog_frame, text=f"Productivity boost per employee: 40%", style="Dialog.TLabel").pack(pady=(5,10), anchor="w")
        
        def hire():
            if self.game.hire_employee():
                messagebox.showinfo("Success", "New employee hired!")
                self.update_status()
                dialog.destroy()
            else:
                # Check for max employees specifically
                if len(self.game.employees) >= config.MAX_EMPLOYEES:
                    messagebox.showerror("Error", f"Cannot hire more than {config.MAX_EMPLOYEES} employees.")
                else:
                    messagebox.showerror("Error", "Not enough money to hire!")
        
        def fire():
            if self.game.fire_employee():
                messagebox.showinfo("Notice", "Employee fired.")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "No employees to fire!")
        
        button_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        button_frame.pack(pady=(15,5), fill="x") # Adjusted padding

        hire_button = ttk.Button(button_frame, text=f"Hire Employee (${config.EMPLOYEE_HIRE_COST if config.EMPLOYEE_HIRE_COST > 0 else 'Free'})", command=hire, style="Dialog.TButton")
        hire_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        fire_button = ttk.Button(button_frame, text="Fire Employee", command=fire, style="Dialog.TButton")
        fire_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        
        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0), side=tk.BOTTOM)

        # Key bindings
        dialog.bind("<Escape>", lambda e: close_button.invoke())
        # For <Return>, it's ambiguous. Let's make it trigger hire by default for now.
        dialog.bind("<Return>", lambda e: hire_button.invoke())
        dialog.focus_set() # Set focus to the dialog itself

    def handle_upgrades_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Business Upgrades") # Updated title
        dialog.geometry("500x400") 
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TLabelframe", background="#f0f0f0", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TLabelframe.Label", background="#f0f0f0", foreground="#00529B", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        
        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)

        for upgrade_key, spec in config.UPGRADE_SPECS.items():
            frame = ttk.LabelFrame(main_dialog_frame, text=spec["name"], padding=10, style="Dialog.TLabelframe")
            frame.pack(pady=10, fill="x", padx=10)
            
            current_level_or_status = self.game.upgrades.get(upgrade_key, False if spec["max_level"] == 1 else 0)
            status_text = ""
            button_text = "Purchase"
            button_state = tk.NORMAL
            cost_text = f"Cost: ${spec['cost'] if spec['max_level'] == 1 else spec['cost_per_level']}"

            if spec["max_level"] == 1: # Boolean (automation)
                if current_level_or_status:
                    status_text = "Enabled"
                    button_state = tk.DISABLED
                    cost_text = "(Purchased)"
                else:
                    status_text = "Disabled"
            else: # Level-based (marketing, storage)
                status_text = f"Level {current_level_or_status}/{spec['max_level']}"
                if current_level_or_status >= spec['max_level']:
                    button_state = tk.DISABLED
                    cost_text = "(Max Level)"
                else:
                    cost_text = f"Cost: ${spec['cost_per_level']} (for Lvl {current_level_or_status + 1})"

            ttk.Label(frame, text=spec['description'], style="Dialog.TLabel", wraplength=430).pack(anchor="w", pady=2)
            ttk.Label(frame, text=cost_text, style="Dialog.TLabel").pack(anchor="w", pady=2)
            ttk.Label(frame, text=f"Current: {status_text}", style="Dialog.TLabel").pack(anchor="w", pady=2)
            
            def make_upgrade_handler(key_to_upgrade):
                def handler():
                    # Logic now uses GameState.purchase_upgrade which uses config
                    if self.game.purchase_upgrade(key_to_upgrade):
                        self.show_message(f"{config.UPGRADE_SPECS[key_to_upgrade]['name']} upgraded/purchased!", "success")
                        self.update_status()
                        dialog.destroy()
                    else:
                        # More specific error based on why purchase_upgrade might fail (already owned, max level, or insufficient funds)
                        current_val = self.game.upgrades.get(key_to_upgrade, 0)
                        spec_check = config.UPGRADE_SPECS[key_to_upgrade]
                        cost_check = spec_check['cost'] if spec_check['max_level'] == 1 else spec_check['cost_per_level']
                        if self.game.money < cost_check:
                            self.show_message("Not enough money!", "error")
                        elif (spec_check['max_level'] == 1 and current_val) or \
                             (spec_check['max_level'] > 1 and current_val >= spec_check['max_level']):
                            self.show_message("Already at maximum or purchased!", "warning")
                        else: # General fail, should be rare
                             self.show_message("Upgrade failed for an unknown reason.", "error")
                return handler
            
            purchase_button = ttk.Button(frame, text=button_text, state=button_state, 
                      command=make_upgrade_handler(upgrade_key), style="Dialog.TButton")
            purchase_button.pack(pady=5, anchor="e")
        
        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0))

        # Key bindings
        dialog.bind("<Escape>", lambda e: close_button.invoke())
        # <Return> is not bound to a specific purchase, user must click or tab and press space/enter on a focused button.
        dialog.focus_set()

    def handle_loans_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Loans")
        dialog.geometry("380x450") # Adjusted for potentially more text
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TEntry", font=("Segoe UI", 10))
        style.configure("Dialog.TFrame", background="#f0f0f0")

        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_dialog_frame, text=f"Current loan: ${self.game.loan}", style="Dialog.TLabel").pack(pady=5, anchor="w")
        ttk.Label(main_dialog_frame, text=f"Annual interest rate: {self.game.loan_interest * 100:.1f}%", style="Dialog.TLabel").pack(pady=5, anchor="w")
        daily_interest_rate_val = self.game.loan_interest / 365
        ttk.Label(main_dialog_frame, text=f"(Daily rate: {daily_interest_rate_val:.4f}%)", style="Dialog.TLabel").pack(pady=(0,5), anchor="w")
        
        if self.game.loan > 0:
            daily_cost = int(self.game.loan * daily_interest_rate_val)
            ttk.Label(main_dialog_frame, text=f"Approx. daily interest cost: ${daily_cost}", style="Dialog.TLabel").pack(pady=5, anchor="w")
        
        income_potential = self.game.get_income_potential()
        safe_max_loan_to_take = self.game.get_safe_loan_amount()
        max_loan_player_can_take = config.MAX_LOAN_TOTAL - self.game.loan
        
        if income_potential > 0 and max_loan_player_can_take > 0:
            recommendation_text = f"Recommended max additional loan: ${safe_max_loan_to_take}"
            if safe_max_loan_to_take < max_loan_player_can_take:
                recommendation_text += " (based on current income)"
            ttk.Label(main_dialog_frame, text=recommendation_text, foreground="#00529B", font=("Segoe UI", 10, "italic"), style="Dialog.TLabel").pack(pady=(10,5), anchor="w")
        elif max_loan_player_can_take <= 0:
             ttk.Label(main_dialog_frame, text="Maximum loan limit reached.", foreground="orange", font=("Segoe UI", 10, "italic"), style="Dialog.TLabel").pack(pady=(10,5), anchor="w")

        amount_var = tk.StringVar()
        ttk.Label(main_dialog_frame, text="Amount:", style="Dialog.TLabel").pack(pady=(10,5), anchor="w")
        amount_entry = ttk.Entry(main_dialog_frame, textvariable=amount_var, style="Dialog.TEntry", width=27)
        amount_entry.pack(pady=5, fill="x")

        # Smart Default Logic
        # Determine if primary action is likely taking or repaying to set smart default
        if max_loan_player_can_take > 0 and (self.game.loan == 0 or safe_max_loan_to_take > 0):
            # Default to suggesting taking a loan if possible and either no loan or safe amount > 0
            if safe_max_loan_to_take > 0:
                amount_var.set(str(safe_max_loan_to_take))
        elif self.game.loan > 0:
            # Default to repaying if there's a loan and cannot take more (or safe amount is 0)
            amount_to_repay = min(self.game.loan, self.game.money)
            if amount_to_repay > 0:
                amount_var.set(str(amount_to_repay))
        # else, leave blank or 0 if no clear action

        def take_loan():
            try:
                amount = int(amount_var.get())
                current_safe_max = self.game.get_safe_loan_amount() # Re-check at time of action
                if income_potential > 0 and amount > current_safe_max and amount <= (config.MAX_LOAN_TOTAL - self.game.loan) :
                    if not messagebox.askyesno("Warning", 
                                            f"This loan (${amount}) exceeds the recommended safe amount of ${current_safe_max} based on your income.\nAre you sure you want to proceed?"):
                        return
                if self.game.take_loan(amount):
                    messagebox.showinfo("Success", f"Loan of ${amount} received!")
                    self.update_status()
                    dialog.destroy()
                else:
                    max_loan_possible = config.MAX_LOAN_TOTAL - self.game.loan
                    if amount <= 0:
                        messagebox.showerror("Error", "Loan amount must be positive.")
                    elif amount > max_loan_possible:
                        messagebox.showerror("Error", f"Cannot take loan. Amount exceeds maximum possible additional loan of ${max_loan_possible}.")
                    else: 
                        messagebox.showerror("Error", "Failed to process loan. Ensure amount is positive and within limits.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        def pay_loan():
            try:
                amount = int(amount_var.get())
                if self.game.repay_loan(amount):
                    messagebox.showinfo("Success", f"Paid ${amount} towards loan!")
                    self.update_status()
                    dialog.destroy()
                else:
                    if amount <=0:
                        messagebox.showerror("Error", "Repayment amount must be positive.")
                    elif amount > self.game.money:
                        messagebox.showerror("Error", "Not enough money to make this repayment.")
                    elif amount > self.game.loan:
                        messagebox.showerror("Error", "Repayment exceeds outstanding loan amount.")
                    else:
                        messagebox.showerror("Error", "Not enough money or amount exceeds loan!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        button_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        button_frame.pack(pady=(15,5), fill="x")

        take_loan_button = ttk.Button(button_frame, text="Take Loan", command=take_loan, style="Dialog.TButton")
        take_loan_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        pay_loan_button = ttk.Button(button_frame, text="Pay Loan", command=pay_loan, style="Dialog.TButton")
        pay_loan_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        
        # Disable take_loan_button if at max total loan
        if max_loan_player_can_take <= 0:
            take_loan_button.config(state=tk.DISABLED)
        # Disable pay_loan_button if no loan or no money to pay
        if self.game.loan <= 0 or self.game.money <= 0:
            pay_loan_button.config(state=tk.DISABLED)

        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0), side=tk.BOTTOM)

        dialog.bind("<Escape>", lambda e: close_button.invoke())
        amount_entry.bind("<Return>", lambda e: take_loan_button.invoke() if amount_var.get() and take_loan_button['state'] == tk.NORMAL else (pay_loan_button.invoke() if amount_var.get() and pay_loan_button['state'] == tk.NORMAL else None))
        dialog.bind("<Return>", lambda e: take_loan_button.invoke() if not amount_entry.focus_get() and take_loan_button['state'] == tk.NORMAL else None)

        amount_entry.focus_set()

    def rest(self):
        self.game.rest()
        self.update_status()
        
        # Visual feedback for reputation gain
        self.rep_label.config(foreground="green")
        self.root.after(1000, lambda: self.rep_label.config(foreground="black"))
        
        messagebox.showinfo("Rest", "You rested and improved your reputation.")

    def save_game(self):
        result = self.game.save_game()
        messagebox.showinfo("Save Game", "Game saved successfully!")

    def quit_game(self):
        if messagebox.askyesno("Quit", "Do you want to save before quitting?"):
            self.save_game()
        self.root.destroy()

    def handle_research_dialog(self):
        """Open a dialog to manage research projects."""
        if not self.controller_ref: # Should not happen if initialized correctly
            self.show_message("Controller not available for research.", "error")
            return

        event_manager = self.controller_ref.event_manager

        dialog = tk.Toplevel(self.root)
        dialog.title("Research & Development")
        dialog.geometry("550x450") # Adjusted size for more info
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Dialog.TLabelframe", background="#f0f0f0", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TLabelframe.Label", background="#f0f0f0", foreground="#00529B", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TFrame", background="#f0f0f0")

        main_dialog_frame = ttk.Frame(dialog, padding=15, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)

        # Display Active Research
        active_research_frame = ttk.LabelFrame(main_dialog_frame, text="Active Project", padding=10, style="Dialog.TLabelframe")
        active_research_frame.pack(pady=10, fill="x")
        if event_manager.active_research:
            active_project_spec = config.RESEARCH_PROJECTS_SPECS.get(event_manager.active_research)
            if active_project_spec:
                progress_percent = (event_manager.research_progress / active_project_spec['duration']) * 100 if active_project_spec['duration'] > 0 else 0
                ttk.Label(active_research_frame, 
                          text=f"{active_project_spec['name']} ({event_manager.research_progress}/{active_project_spec['duration']} days - {progress_percent:.0f}% complete)", 
                          style="Dialog.TLabel", font=("Segoe UI", 10, "italic")).pack(anchor="w")
        else:
            ttk.Label(active_research_frame, text="No active research project.", style="Dialog.TLabel", font=("Segoe UI", 10, "italic")).pack(anchor="w")

        # Available Projects List
        projects_frame = ttk.LabelFrame(main_dialog_frame, text="Available Projects", padding=10, style="Dialog.TLabelframe")
        projects_frame.pack(pady=10, fill="both", expand=True)

        # Use a Canvas and Frame for scrollable list of projects
        canvas = tk.Canvas(projects_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(projects_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Dialog.TFrame")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for key, project_spec in config.RESEARCH_PROJECTS_SPECS.items():
            project_info_frame = ttk.Frame(scrollable_frame, padding=(0,0,0,10), style="Dialog.TFrame") # Padding at bottom of each item
            project_info_frame.pack(fill="x")

            status_text = ""
            button_text = "Start Research"
            button_state = tk.NORMAL

            if key in self.game.completed_research:
                status_text = "(Completed)"
                button_state = tk.DISABLED
            elif key == event_manager.active_research:
                status_text = "(In Progress)"
                button_state = tk.DISABLED
            
            ttk.Label(project_info_frame, text=f"{project_spec['name']} {status_text}", style="Dialog.TLabel", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(project_info_frame, text=f"Cost: ${project_spec['cost']} | Duration: {project_spec['duration']} days", style="Dialog.TLabel").pack(anchor="w")
            # Display project description
            if project_spec.get('description'):
                ttk.Label(project_info_frame, text=project_spec['description'], style="Dialog.TLabel", wraplength=450, justify=tk.LEFT).pack(anchor="w", pady=(2,0))

            def make_start_research_handler(p_key, p_cost, p_name, p_duration):
                def handler():
                    if event_manager.active_research is not None:
                        self.show_message(f"Another research '{event_manager.research_projects[event_manager.active_research]['name']}' is already active.", "warning")
                        return
                    if self.game.money < p_cost:
                        self.show_message(f"Not enough money to start '{p_name}'. Cost: ${p_cost}", "error")
                        return
                    
                    self.game.money -= p_cost
                    event_manager.active_research = p_key
                    self.game.active_research_project = p_key
                    event_manager.research_progress = 0
                    self.show_message(f"Research started for '{p_name}'! It will take {p_duration} days.", "success")
                    self.update_status() # Update main UI
                    dialog.destroy() # Close research dialog
                return handler

            start_button = ttk.Button(project_info_frame, text=button_text, state=button_state,
                       command=make_start_research_handler(key, project_spec['cost'], project_spec['name'], project_spec['duration']), 
                       style="Dialog.TButton")
            start_button.pack(anchor="e", pady=5)
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)

        close_button = ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton")
        close_button.pack(pady=(10,0))

        # Key bindings
        dialog.bind("<Escape>", lambda e: close_button.invoke())
        # <Return> not bound globally due to multiple start buttons.
        dialog.focus_set()

    def run(self):
        self.root.mainloop() 