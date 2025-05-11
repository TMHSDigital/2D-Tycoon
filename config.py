"""
config.py

Central configuration file for the Business Tycoon game.
This file holds all game balance parameters, initial settings, and constants
to make tweaking and difficulty adjustments easier.
"""

# === Initial Game State ===
INITIAL_MONEY = 100
INITIAL_REPUTATION = 50
INITIAL_DAY = 1
INITIAL_STORAGE_CAPACITY = 50
WIN_CONDITION_MONEY = 1000
MAX_LOAN_TOTAL = 1000 # Overall cap on how much loan principal a player can have
ANNUAL_LOAN_INTEREST_RATE = 0.10 # 10% annual

# === Supplies ===
# Prices player PAYS for supplies
SUPPLY_PRICES = {
    "basic_supplies": 25,
    "premium_supplies": 50,
    "equipment": 150 
}
# Income bonuses or characteristics when SELLING/USING supplies
SUPPLY_USAGE_EFFECTS = {
    "basic_supplies": {"income_multiplier": 1.0, "description": "Standard supplies."},
    "premium_supplies": {"income_multiplier": 1.5, "description": "High-quality supplies, 50% income bonus."},
    "equipment": {"income_multiplier": 1.3, "description": "Reusable equipment, 30% income bonus per use."}
}

# === Work Action ===
BASE_WORK_INCOME_MIN = 40
BASE_WORK_INCOME_MAX = 80
REPUTATION_LOSS_WORK_MIN = 3
REPUTATION_LOSS_WORK_MAX = 8

# === Rest Action ===
BASE_REPUTATION_GAIN_REST = 10
MARKETING_REST_BONUS_PER_LEVEL = 2

# === Employees ===
EMPLOYEE_HIRE_COST = 0 # Cost to hire (can be > 0 if we want a hiring fee)
EMPLOYEE_DAILY_SALARY = 150
EMPLOYEE_PRODUCTIVITY_BONUS_PER_EMPLOYEE = 0.4 # 40% boost per employee
MAX_EMPLOYEES = 3 # Visual limit on map, can be a gameplay limit too

# === Upgrades (Direct Purchases) ===
# game_state.upgrades dictionary stores current level or boolean status
UPGRADE_SPECS = {
    "automation": {
        "name": "Automation System",
        "cost": 400,
        "max_level": 1, # Effectively a boolean purchase
        "description": "Increases daily income from work by a fixed multiplier.",
        "income_bonus_multiplier": 1.5 # If automation is True, base work income x1.5
    },
    "marketing": {
        "name": "Marketing Campaign",
        "cost_per_level": 250,
        "max_level": 3,
        "description": "Improves reputation gain from rest and reduces reputation loss from work.",
        "rep_loss_reduction_per_level": 1, # Reduces rep loss from work by 1 per level
        "rest_bonus_per_level": MARKETING_REST_BONUS_PER_LEVEL # Defined above
    },
    "storage": {
        "name": "Storage Expansion",
        "cost_per_level": 150,
        "max_level": 2,
        "description": "Increases storage capacity.",
        "storage_increase_per_level": 50
    }
}

# === Market & Events ===
MARKET_TREND_INITIAL = 1.0
MARKET_TREND_MIN = 0.5
MARKET_TREND_MAX = 2.0
MARKET_TREND_DAILY_FLUCTUATION_RANGE = (-0.2, 0.2) # (min_change, max_change)
AGGRESSIVE_COMPETITOR_MARKET_PRESSURE = -0.1 # Additional negative pressure from aggressive competitors
COMPETITOR_INFLUENCE_FACTOR_ON_DEMAND = 0.5 # How much competitor market share reduces overall demand
MARKET_BOOM_THRESHOLD = 1.2
MARKET_DECLINE_THRESHOLD = 0.8

SPECIAL_EVENT_CHANCE = 0.2 # Chance for a special event to occur each day (from EventManager)

COMPETITOR_ACTION_CHANCE = 0.3
COMPETITOR_EFFECTS = {
    "price_war": {"message_template": "{} started a price war!", "market_trend_effect": -0.2},
    "marketing_campaign": {"message_template": "{} launched a major marketing campaign!", "market_trend_effect": -0.1},
    "expansion": {"message_template": "{} expanded their business!", "market_trend_effect": -0.15}
}

# EventManager Random Events (bonus, penalty, opportunity, employee_event)
RANDOM_EVENT_TYPES_CHANCES = [
    {"type": "bonus", "chance": 0.4, "min_amount": 20, "max_amount": 50},
    {"type": "penalty", "chance": 0.3, "min_amount": 10, "max_amount": 30},
    {"type": "opportunity", "chance": 0.2, "market_boost": 0.3},
    {"type": "employee_event", "chance": 0.1}
]
EMPLOYEE_SUB_EVENTS = [
    {"effect": "productivity_boost", "name": "High Morale", "value": 1.5, "duration": 2, "message": "Employee morale is high! Productivity boosted!"},
    {"effect": "productivity_drop", "name": "Employee Strike", "value": 0.5, "duration": 1, "message": "Employees are on strike! Productivity halved!"},
    {"effect": "training_pay", "name": "Training Seminar", "value": 1.2, "duration": 3, "message": "Employees attended a training seminar! Slightly boosted productivity."}
]

# === Research Projects ===
# Managed by EventManager, effects applied in GameState
RESEARCH_PROJECTS_SPECS = {
    "efficient_storage": {
        "name": "Efficient Storage Solutions", 
        "cost": 400, 
        "duration": 5, # in days
        "description": "Advanced logistics increase total storage capacity by 75 units.",
        "effect_description": "+75 Storage Capacity"
        # effect handled in GameState.apply_research_completion
    },
    "smart_automation": {
        "name": "Smart Automation Systems", 
        "cost": 600, 
        "duration": 7, 
        "description": "Cutting-edge AI boosts income from automated processes by an additional 10%.",
        "effect_description": "+10% Automation Efficiency"
    },
    "eco_friendly_practices": { # Renamed key for consistency
        "name": "Eco-Friendly Practices", 
        "cost": 300, 
        "duration": 4, 
        "description": "Sustainable operations improve public image, granting a permanent +10 reputation boost.",
        "effect_description": "+10 Reputation"
    }
}

# === UI & Display ===
# (Could add CLI colors, GUI theme preferences here later)
FIGLET_FONT = "slant"

# === For Future Difficulty Settings ===
DIFFICULTY_LEVELS = {
    "easy": {
        "initial_money_multiplier": 1.5, 
        "reputation_loss_modifier": 0.75, 
        "loan_interest_modifier": 0.8
    },
    "normal": {
        "initial_money_multiplier": 1.0,
        "reputation_loss_modifier": 1.0,
        "loan_interest_modifier": 1.0
    },
    "hard": {
        "initial_money_multiplier": 0.75,
        "reputation_loss_modifier": 1.25,
        "loan_interest_modifier": 1.2
    }
}
SELECTED_DIFFICULTY = "normal" # Default difficulty 