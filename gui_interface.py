import tkinter as tk
from tkinter import ttk, messagebox
from business_map import BusinessMap
from game_state import GameState

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
    def __init__(self, game_state: GameState):
        """Initialize the GUI with a GameState instance."""
        self.game = game_state
        self.root = tk.Tk()
        self.root.title("Business Tycoon Adventure")
        self.root.geometry("900x700") # Increased window size
        self.root.configure(bg="#f0f0f0") # Light grey background

        # --- Style Configuration ---
        self.style = ttk.Style(self.root)
        available_themes = self.style.theme_names()
        # print(f"Available themes: {available_themes}") # To check available themes
        if "clam" in available_themes:
            self.style.theme_use("clam") 
        elif "alt" in available_themes:
            self.style.theme_use("alt")
        
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, relief="flat")
        self.style.map("TButton",
            foreground=[('pressed', 'white'), ('active', 'white')],
            background=[('pressed', '!disabled', '#00529B'), ('active', '#0078D4'), ('!disabled', '#0078D4')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
            
        self.style.configure("TLabelframe", background="#f0f0f0", font=("Segoe UI", 12, "bold"), borderwidth=1, relief="groove")
        self.style.configure("TLabelframe.Label", background="#f0f0f0", foreground="#00529B", font=("Segoe UI", 12, "bold"))
        
        self.style.configure("TProgressbar", thickness=20, background="#0078D4")
        self.style.configure("Green.Horizontal.TProgressbar", background="green")
        self.style.configure("Red.Horizontal.TProgressbar", background="red")
        self.style.configure("Yellow.Horizontal.TProgressbar", background="orange")

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
        
        ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton").pack(pady=(10,0))

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
        
        ttk.Button(main_dialog_frame, text="Close", command=dialog.destroy, style="Dialog.TButton").pack(pady=(10,0))

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame") # Increased padding
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.configure(style="Background.TFrame")
        self.style.configure("Background.TFrame", background="#f0f0f0")

        # Status Display with Progress Bars
        self.status_frame = ttk.LabelFrame(main_frame, text="Business Status", padding="15")
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 20)) # Increased padding

        # Money and Reputation Progress Bars
        money_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        money_frame.pack(fill="x", pady=5)
        ttk.Label(money_frame, text="Money:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0,5))
        self.money_progress = ttk.Progressbar(money_frame, length=250, mode='determinate', style="Green.Horizontal.TProgressbar")
        self.money_progress.pack(side="left", padx=5, fill="x", expand=True)
        self.money_label = ttk.Label(money_frame, text="$0", font=("Segoe UI", 11, "bold"))
        self.money_label.pack(side="left", padx=(5,0))

        rep_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        rep_frame.pack(fill="x", pady=5)
        ttk.Label(rep_frame, text="Reputation:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0,5))
        self.rep_progress = ttk.Progressbar(rep_frame, length=250, mode='determinate', style="Green.Horizontal.TProgressbar")
        self.rep_progress.pack(side="left", padx=5, fill="x", expand=True)
        self.rep_label = ttk.Label(rep_frame, text="0", font=("Segoe UI", 11, "bold"))
        self.rep_label.pack(side="left", padx=(5,0))

        # Inventory Display (Improved with labels and a frame)
        inventory_outer_frame = ttk.Frame(self.status_frame, style="Background.TFrame")
        inventory_outer_frame.pack(pady=10, fill="x")
        
        ttk.Label(inventory_outer_frame, text="Current Day & Inventory:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,5))
        
        self.inventory_text_frame = ttk.Frame(inventory_outer_frame, borderwidth=1, relief="sunken", style="TFrame")
        self.inventory_text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.inventory_text = tk.Text(self.inventory_text_frame, height=7, width=45, font=("Consolas", 10), 
                                      bg="#ffffff", fg="#333333", relief="flat", borderwidth=0,
                                      padx=10, pady=10) # Increased height and padding
        self.inventory_text.pack(fill="both", expand=True)
        self.inventory_text.config(state='disabled')

        # Action Buttons Frame with Tooltips
        actions_frame = ttk.LabelFrame(main_frame, text="Game Actions", padding="15") # Changed title
        actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

        tooltips = {
            "Buy Supplies": "Purchase supplies to sell for profit",
            "Work": "Sell supplies to earn money",
            "Manage Employees": "Hire or fire employees",
            "Upgrades": "Purchase business upgrades",
            "Loans": "Take or pay back loans",
            "Rest": "Rest to improve reputation",
            "Save Game": "Save your progress (Ctrl+S)",
            "Quit": "Exit the game (Ctrl+Q)"
        }

        actions = [
            ("Buy Supplies", self.buy_supplies),
            ("Work", self.work),
            ("Manage Employees", self.manage_employees),
            ("Upgrades", self.handle_upgrades),
            ("Loans", self.handle_loans),
            ("Rest", self.rest),
            ("Save Game", self.save_game),
            ("Quit", self.quit_game)
        ]

        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_frame, text=text, command=command)
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew")
            ToolTip(btn, tooltips[text])

        # Add Map Button
        map_btn = ttk.Button(actions_frame, text="Show Map", command=self.show_business_map)
        map_btn.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
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
        
        inventory_text_content = f"Day: {self.game.day}\n\n"
        inventory_text_content += "Inventory:\n"
        for item, amount in self.game.inventory.items():
            inventory_text_content += f"  {item.replace('_', ' ').title()}: {amount}\n"
        
        inventory_text_content += "\nUpgrades:\n"
        for upgrade, level in self.game.upgrades.items():
            if isinstance(level, bool):
                status_text = "Enabled" if level else "Disabled"
            else:
                status_text = f"Level {level}"
            inventory_text_content += f"  {upgrade.replace('_', ' ').title()}: {status_text}\n"
        
        if self.game.employees:
             inventory_text_content += f"\nEmployees: {len(self.game.employees)}\n"
        if self.game.loan > 0:
            inventory_text_content += f"Loan: ${self.game.loan}\n"

        self.inventory_text.insert(1.0, inventory_text_content)
        self.inventory_text.config(state='disabled')

    def buy_supplies(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Supplies")
        dialog.geometry("350x300") # Adjusted size
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
        supply_combo = ttk.Combobox(main_dialog_frame, textvariable=supply_var, style="Dialog.TCombobox", width=25)
        supply_combo['values'] = ['Basic Supplies', 'Premium Supplies', 'Equipment']
        supply_combo.pack(pady=5, fill="x")
        
        ttk.Label(main_dialog_frame, text="Amount:", style="Dialog.TLabel").pack(pady=(10,5), anchor="w")
        amount_entry = ttk.Entry(main_dialog_frame, textvariable=amount_var, style="Dialog.TEntry", width=27)
        amount_entry.pack(pady=5, fill="x")
        
        price_label = ttk.Label(main_dialog_frame, text="Total Cost: $0", style="Dialog.TLabel") # Initial text
        price_label.pack(pady=(10,5))
        
        def update_price(*args):
            supply_type = supply_var.get().lower().replace(' ', '_')
            try:
                amount = int(amount_var.get() or 0)
                if supply_type in self.game.prices:
                    total = amount * self.game.prices[supply_type]
                    price_label['text'] = f"Total Cost: ${total}"
            except ValueError:
                price_label['text'] = "Enter a valid amount"
        
        supply_var.trace('w', update_price)
        amount_var.trace('w', update_price)
        
        def handle_purchase():
            supply_type = supply_var.get().lower().replace(' ', '_')
            try:
                amount = int(amount_var.get())
                if supply_type not in self.game.prices:
                    messagebox.showerror("Error", "Please select a valid supply type")
                    return
                
                cost = amount * self.game.prices[supply_type]
                if cost > self.game.money:
                    messagebox.showerror("Error", "Not enough money!")
                    return
                
                current_total = sum(self.game.inventory.values())
                if current_total + amount > self.game.storage_capacity:
                    messagebox.showerror("Error", "Not enough storage space!")
                    return
                
                self.game.money -= cost
                self.game.inventory[supply_type] += amount
                messagebox.showinfo("Success", f"Bought {amount} {supply_type.replace('_', ' ')} for ${cost}")
                self.update_status()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        button_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        button_frame.pack(pady=(15,0), fill="x")

        ttk.Button(button_frame, text="Purchase", command=handle_purchase, style="Dialog.TButton").pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy, style="Dialog.TButton").pack(side=tk.RIGHT, expand=True, padx=5)

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
        dialog.geometry("350x250") # Adjusted size
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
        ttk.Label(main_dialog_frame, text=f"Daily cost per employee: $150", style="Dialog.TLabel").pack(pady=5, anchor="w")
        ttk.Label(main_dialog_frame, text=f"Productivity boost per employee: 40%", style="Dialog.TLabel").pack(pady=(5,10), anchor="w")
        
        def hire():
            if self.game.hire_employee():
                messagebox.showinfo("Success", "New employee hired!")
                self.update_status()
                dialog.destroy()
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
        button_frame.pack(pady=(15,0), fill="x", side=tk.BOTTOM)

        ttk.Button(button_frame, text="Hire Employee ($150)", command=hire, style="Dialog.TButton").pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        ttk.Button(button_frame, text="Fire Employee", command=fire, style="Dialog.TButton").pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    def handle_upgrades(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Purchase Upgrades")
        dialog.geometry("450x350") # Adjusted size
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        style = ttk.Style(dialog)
        if "clam" in style.theme_names(): style.theme_use("clam")
        style.configure("Dialog.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("Dialog.TLabelframe", background="#f0f0f0", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TLabelframe.Label", background="#f0f0f0", foreground="#00529B", font=("Segoe UI", 11, "bold"))
        style.configure("Dialog.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        
        upgrades = {
            "automation": {"cost": 400, "name": "Automation System", "description": "Increases daily income by 50%"},
            "marketing": {"cost": 250, "name": "Marketing Campaign", "description": "Improves reputation gain and reduces loss"},
            "storage": {"cost": 150, "name": "Storage Expansion", "description": "Increases storage capacity by 50 units"}
        }
        
        main_dialog_frame = ttk.Frame(dialog, padding=10, style="Dialog.TFrame")
        main_dialog_frame.pack(fill="both", expand=True)
        style.configure("Dialog.TFrame", background="#f0f0f0")

        for upgrade_key, upgrade_info in upgrades.items():
            frame = ttk.LabelFrame(main_dialog_frame, text=upgrade_info["name"], padding=10, style="Dialog.TLabelframe")
            frame.pack(pady=10, fill="x", padx=10)
            
            current_level = self.game.upgrades[upgrade_key]
            if isinstance(current_level, bool):
                status = "Enabled" if current_level else "Disabled"
            else:
                status = f"Level {current_level}"
            
            ttk.Label(frame, text=f"{upgrade_info['description']}", style="Dialog.TLabel", wraplength=380).pack(anchor="w", pady=2)
            ttk.Label(frame, text=f"Cost: ${upgrade_info['cost']}", style="Dialog.TLabel").pack(anchor="w", pady=2)
            ttk.Label(frame, text=f"Current: {status}", style="Dialog.TLabel").pack(anchor="w", pady=2)
            
            def make_upgrade_handler(key, cost):
                def handler():
                    if self.game.purchase_upgrade(key):
                        messagebox.showinfo("Success", f"{upgrades[key]['name']} purchased!")
                        self.update_status()
                        dialog.destroy()
                    else:
                        # Check why it failed
                        if isinstance(self.game.upgrades[key], bool) and self.game.upgrades[key]:
                            messagebox.showinfo("Notice", "Already purchased!")
                        elif not isinstance(self.game.upgrades[key], bool) and self.game.upgrades[key] >= 3:
                            messagebox.showinfo("Notice", "Maximum level reached!")
                        else:
                            messagebox.showerror("Error", "Not enough money!")
                return handler
            
            ttk.Button(frame, text="Purchase", 
                      command=make_upgrade_handler(upgrade_key, upgrade_info["cost"])).pack(pady=5)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def handle_loans(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Loans")
        dialog.geometry("380x400") # Adjusted size
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
        
        # Calculate income potential
        income_potential = 0
        if sum(self.game.inventory.values()) > 0:
            base_income = 60  # Average of random 40-80
            automation_bonus = 1.5 if self.game.upgrades["automation"] else 1.0
            employee_bonus = 1 + (len(self.game.employees) * 0.4)  # Updated to 0.4 to match new bonus
            income_potential = int(base_income * automation_bonus * employee_bonus)
        
        # Calculate safe maximum loan
        safe_max_loan = self.game.get_safe_loan_amount()
        max_loan = 1000 - self.game.loan
        
        if income_potential > 0:
            recommendation_text = f"Recommended max loan: ${safe_max_loan}"
            if safe_max_loan < max_loan:
                recommendation_text += " (based on current income)"
            ttk.Label(main_dialog_frame, text=recommendation_text, foreground="#00529B", font=("Segoe UI", 10, "italic"), style="Dialog.TLabel").pack(pady=(10,5), anchor="w")
        
        amount_var = tk.StringVar()
        ttk.Label(main_dialog_frame, text="Amount:", style="Dialog.TLabel").pack(pady=(10,5), anchor="w")
        amount_entry = ttk.Entry(main_dialog_frame, textvariable=amount_var, style="Dialog.TEntry", width=27)
        amount_entry.pack(pady=5, fill="x")
        
        def take_loan():
            try:
                amount = int(amount_var.get())
                # Warn if amount exceeds recommended
                if income_potential > 0 and amount > safe_max_loan:
                    if not messagebox.askyesno("Warning", 
                                            f"This loan exceeds the recommended amount based on your income.\nAre you sure you want to proceed?"):
                        return
                
                if self.game.take_loan(amount):
                    messagebox.showinfo("Success", f"Loan of ${amount} received!")
                    self.update_status()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Maximum additional loan allowed: ${max_loan}")
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
                    messagebox.showerror("Error", "Not enough money or amount exceeds loan!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        button_frame = ttk.Frame(main_dialog_frame, style="Dialog.TFrame")
        button_frame.pack(pady=(15,0), fill="x", side=tk.BOTTOM)

        ttk.Button(button_frame, text="Take Loan", command=take_loan, style="Dialog.TButton").pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        ttk.Button(button_frame, text="Pay Loan", command=pay_loan, style="Dialog.TButton").pack(side=tk.LEFT, expand=True, padx=5, pady=5)

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

    def run(self):
        self.root.mainloop() 