import tkinter as tk
from tkinter import ttk, messagebox

class TycoonGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Business Tycoon Adventure")
        self.root.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Status Display
        self.status_frame = ttk.LabelFrame(main_frame, text="Business Status", padding="10")
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.status_label = ttk.Label(self.status_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=0, column=0)

        # Action Buttons Frame
        actions_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

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

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        # Update initial status
        self.update_status()

    def update_status(self):
        status = (
            f"Day: {self.game.day}\n"
            f"Money: ${self.game.money}\n"
            f"Reputation: {self.game.reputation}\n\n"
            "Inventory:\n"
        )
        for item, amount in self.game.inventory.items():
            status += f"  {item.replace('_', ' ').title()}: {amount}\n"

        status += "\nUpgrades:\n"
        for upgrade, level in self.game.upgrades.items():
            if isinstance(level, bool):
                status += f"  {upgrade.replace('_', ' ').title()}: {'Enabled' if level else 'Disabled'}\n"
            else:
                status += f"  {upgrade.replace('_', ' ').title()}: Level {level}\n"

        self.status_label.config(text=status)

    def buy_supplies(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Supplies")
        dialog.geometry("300x200")
        
        supply_var = tk.StringVar()
        amount_var = tk.StringVar()
        
        ttk.Label(dialog, text="Select supply type:").pack(pady=5)
        supply_combo = ttk.Combobox(dialog, textvariable=supply_var)
        supply_combo['values'] = ['Basic Supplies', 'Premium Supplies', 'Equipment']
        supply_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog, textvariable=amount_var)
        amount_entry.pack(pady=5)
        
        def handle_purchase():
            supply_type = supply_var.get()
            try:
                amount = int(amount_var.get())
                # Call game's buy supplies method
                # self.game.buy_supplies(supply_type.lower().replace(' ', '_'), amount)
                self.update_status()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        ttk.Button(dialog, text="Purchase", command=handle_purchase).pack(pady=10)

    def work(self):
        result = self.game.handle_work()
        self.update_status()
        messagebox.showinfo("Work Result", f"You earned ${result}!")

    def manage_employees(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Employees")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text=f"Current employees: {self.game.employees}").pack(pady=5)
        
        def hire():
            # self.game.hire_employee()
            self.update_status()
            dialog.destroy()
        
        def fire():
            # self.game.fire_employee()
            self.update_status()
            dialog.destroy()
        
        ttk.Button(dialog, text="Hire Employee", command=hire).pack(pady=5)
        ttk.Button(dialog, text="Fire Employee", command=fire).pack(pady=5)

    def handle_upgrades(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Purchase Upgrades")
        dialog.geometry("300x200")
        
        for upgrade, level in self.game.upgrades.items():
            frame = ttk.Frame(dialog)
            frame.pack(pady=5, fill="x", padx=10)
            
            ttk.Label(frame, text=f"{upgrade.replace('_', ' ').title()}:").pack(side="left")
            if isinstance(level, bool):
                status = "Enabled" if level else "Disabled"
            else:
                status = f"Level {level}"
            ttk.Label(frame, text=status).pack(side="right")

    def handle_loans(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Loans")
        dialog.geometry("300x200")
        
        amount_var = tk.StringVar()
        
        ttk.Label(dialog, text=f"Current loan: ${self.game.loan}").pack(pady=5)
        ttk.Label(dialog, text="Loan amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog, textvariable=amount_var)
        amount_entry.pack(pady=5)
        
        def take_loan():
            try:
                amount = int(amount_var.get())
                # self.game.take_loan(amount)
                self.update_status()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        def pay_loan():
            try:
                amount = int(amount_var.get())
                # self.game.pay_loan(amount)
                self.update_status()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        ttk.Button(dialog, text="Take Loan", command=take_loan).pack(pady=5)
        ttk.Button(dialog, text="Pay Loan", command=pay_loan).pack(pady=5)

    def rest(self):
        self.game.handle_rest()
        self.update_status()
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