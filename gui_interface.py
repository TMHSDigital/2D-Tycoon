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

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                         relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class TycoonGUI:
    def __init__(self, game_state: GameState):
        """Initialize the GUI with a GameState instance."""
        self.game = game_state  # Keep the same attribute name for compatibility
        self.root = tk.Tk()
        self.root.title("Business Tycoon Adventure")
        self.root.geometry("800x600")
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
        dialog.title("Help")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        text = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
        text.insert("1.0", help_text)
        text.config(state="disabled")
        text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def show_business_map(self, event=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Business Map")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create map instance with current game state
        map_instance = BusinessMap({
            'day': self.game.day,
            'money': self.game.money,
            'reputation': self.game.reputation,
            'loan': self.game.loan,
            'inventory': self.game.inventory,
            'storage_capacity': self.game.storage_capacity,
            'employees': self.game.employees,
            'upgrades': self.game.upgrades
        })
        
        # Display the map
        map_label = ttk.Label(dialog, text=map_instance.get_map_with_status(), 
                            font=("Courier", 12), justify=tk.LEFT)
        map_label.pack(padx=20, pady=20)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Status Display with Progress Bars
        self.status_frame = ttk.LabelFrame(main_frame, text="Business Status", padding="10")
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        # Money and Reputation Progress Bars
        money_frame = ttk.Frame(self.status_frame)
        money_frame.pack(fill="x", pady=2)
        ttk.Label(money_frame, text="Money:").pack(side="left")
        self.money_progress = ttk.Progressbar(money_frame, length=200, mode='determinate')
        self.money_progress.pack(side="left", padx=5)
        self.money_label = ttk.Label(money_frame, text="$0")
        self.money_label.pack(side="left")

        rep_frame = ttk.Frame(self.status_frame)
        rep_frame.pack(fill="x", pady=2)
        ttk.Label(rep_frame, text="Reputation:").pack(side="left")
        self.rep_progress = ttk.Progressbar(rep_frame, length=200, mode='determinate')
        self.rep_progress.pack(side="left", padx=5)
        self.rep_label = ttk.Label(rep_frame, text="0")
        self.rep_label.pack(side="left")

        # Inventory Display
        self.inventory_text = tk.Text(self.status_frame, height=6, width=40)
        self.inventory_text.pack(pady=5)
        self.inventory_text.config(state='disabled')

        # Action Buttons Frame with Tooltips
        actions_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

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
        self.money_progress['value'] = (self.game.money / 1000) * 100  # Goal is $1000
        self.money_label['text'] = f"${self.game.money}"
        
        self.rep_progress['value'] = self.game.reputation
        self.rep_label['text'] = str(self.game.reputation)

        # Update inventory display
        self.inventory_text.config(state='normal')
        self.inventory_text.delete(1.0, tk.END)
        
        inventory_text = f"Day: {self.game.day}\n\nInventory:\n"
        for item, amount in self.game.inventory.items():
            inventory_text += f"  {item.replace('_', ' ').title()}: {amount}\n"
        
        inventory_text += "\nUpgrades:\n"
        for upgrade, level in self.game.upgrades.items():
            if isinstance(level, bool):
                status = "Enabled" if level else "Disabled"
            else:
                status = f"Level {level}"
            inventory_text += f"  {upgrade.replace('_', ' ').title()}: {status}\n"
        
        self.inventory_text.insert(1.0, inventory_text)
        self.inventory_text.config(state='disabled')

    def buy_supplies(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Supplies")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        supply_var = tk.StringVar()
        amount_var = tk.StringVar()
        
        ttk.Label(dialog, text="Select supply type:").pack(pady=5)
        supply_combo = ttk.Combobox(dialog, textvariable=supply_var)
        supply_combo['values'] = ['Basic Supplies', 'Premium Supplies', 'Equipment']
        supply_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog, textvariable=amount_var)
        amount_entry.pack(pady=5)
        
        # Price display
        price_label = ttk.Label(dialog, text="")
        price_label.pack(pady=5)
        
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
        
        ttk.Button(dialog, text="Purchase", command=handle_purchase).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)

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
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Current employees: {len(self.game.employees)}").pack(pady=5)
        ttk.Label(dialog, text=f"Daily cost per employee: $150").pack(pady=5)
        ttk.Label(dialog, text=f"Productivity boost per employee: 40%").pack(pady=5)
        
        def hire():
            if self.game.money >= 150:
                self.game.employees.append({"salary": 150})
                messagebox.showinfo("Success", "New employee hired!")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Not enough money to hire!")
        
        def fire():
            if self.game.employees:
                self.game.employees.pop()
                messagebox.showinfo("Notice", "Employee fired.")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "No employees to fire!")
        
        ttk.Button(dialog, text="Hire Employee ($150)", command=hire).pack(pady=5)
        ttk.Button(dialog, text="Fire Employee", command=fire).pack(pady=5)
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def handle_upgrades(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Purchase Upgrades")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        upgrades = {
            "automation": {"cost": 400, "name": "Automation System", "description": "Increases daily income by 50%"},
            "marketing": {"cost": 250, "name": "Marketing Campaign", "description": "Improves reputation gain and reduces loss"},
            "storage": {"cost": 150, "name": "Storage Expansion", "description": "Increases storage capacity by 50 units"}
        }
        
        for upgrade_key, upgrade_info in upgrades.items():
            frame = ttk.LabelFrame(dialog, text=upgrade_info["name"], padding=5)
            frame.pack(pady=5, fill="x", padx=10)
            
            current_level = self.game.upgrades[upgrade_key]
            if isinstance(current_level, bool):
                status = "Enabled" if current_level else "Disabled"
            else:
                status = f"Level {current_level}"
            
            ttk.Label(frame, text=f"{upgrade_info['description']}").pack(anchor="w")
            ttk.Label(frame, text=f"Cost: ${upgrade_info['cost']}").pack(anchor="w")
            ttk.Label(frame, text=f"Current: {status}").pack(anchor="w")
            
            def make_upgrade_handler(key, cost):
                def handler():
                    if self.game.money >= cost:
                        if isinstance(self.game.upgrades[key], bool):
                            if not self.game.upgrades[key]:
                                self.game.money -= cost
                                self.game.upgrades[key] = True
                                messagebox.showinfo("Success", f"{upgrades[key]['name']} purchased!")
                                self.update_status()
                                dialog.destroy()
                            else:
                                messagebox.showinfo("Notice", "Already purchased!")
                        else:
                            if self.game.upgrades[key] < 3:  # Max level 3
                                self.game.money -= cost
                                self.game.upgrades[key] += 1
                                messagebox.showinfo("Success", f"{upgrades[key]['name']} upgraded to level {self.game.upgrades[key]}!")
                                self.update_status()
                                dialog.destroy()
                            else:
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
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Current loan: ${self.game.loan}").pack(pady=5)
        ttk.Label(dialog, text=f"Annual interest rate: {self.game.loan_interest * 100}%").pack(pady=5)
        daily_interest = self.game.loan_interest / 365
        ttk.Label(dialog, text=f"(Daily rate: {daily_interest:.6f}%)").pack(pady=2)
        
        if self.game.loan > 0:
            daily_cost = int(self.game.loan * daily_interest)
            ttk.Label(dialog, text=f"Daily interest cost: ${daily_cost}").pack(pady=5)
        
        # Calculate income potential
        income_potential = 0
        if sum(self.game.inventory.values()) > 0:
            base_income = 60  # Average of random 40-80
            automation_bonus = 1.5 if self.game.upgrades["automation"] else 1.0
            employee_bonus = 1 + (len(self.game.employees) * 0.2)
            income_potential = int(base_income * automation_bonus * employee_bonus)
        
        # Calculate safe maximum loan
        max_loan = 1000 - self.game.loan
        safe_max_loan = min(max_loan, income_potential * 10)
        
        if income_potential > 0:
            recommendation_text = f"Recommended max loan: ${safe_max_loan}"
            if safe_max_loan < max_loan:
                recommendation_text += " (based on income)"
            ttk.Label(dialog, text=recommendation_text, foreground="blue").pack(pady=5)
        
        amount_var = tk.StringVar()
        ttk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog, textvariable=amount_var)
        amount_entry.pack(pady=5)
        
        def take_loan():
            try:
                amount = int(amount_var.get())
                max_loan = 1000 - self.game.loan
                if amount <= max_loan:
                    if income_potential > 0 and amount > safe_max_loan:
                        if not messagebox.askyesno("Warning", 
                                                 f"This loan exceeds the recommended amount based on your income.\nAre you sure you want to proceed?"):
                            return
                    
                    self.game.loan += amount
                    self.game.money += amount
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
                if amount <= self.game.money and amount <= self.game.loan:
                    self.game.loan -= amount
                    self.game.money -= amount
                    messagebox.showinfo("Success", f"Paid ${amount} towards loan!")
                    self.update_status()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Not enough money or amount exceeds loan!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        ttk.Button(dialog, text="Take Loan", command=take_loan).pack(pady=5)
        ttk.Button(dialog, text="Pay Loan", command=pay_loan).pack(pady=5)
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def rest(self):
        self.game.rest()
        self.update_status()
        
        # Visual feedback for reputation gain
        self.rep_label.config(foreground="green")
        self.root.after(1000, lambda: self.rep_label.config(foreground="black"))
        
        messagebox.showinfo("Rest", "You rested and improved your reputation.")

    def save_game(self):
        self.game.save_game()
        messagebox.showinfo("Save Game", "Game saved successfully!")

    def quit_game(self):
        if messagebox.askyesno("Quit", "Do you want to save before quitting?"):
            self.save_game()
        self.root.destroy()

    def run(self):
        self.root.mainloop() 