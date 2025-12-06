import math

COST_GROWTH = 1.15

BUILDINGS = {
    "cursor":          {"label": "Cursor",          "emoji": "🖱️", "base_cost": 10,      "base_income": 0.1},
    "clicker":         {"label": "Clicker",         "emoji": "👆", "base_cost": 25,      "base_income": 0.2},
    "small_farm":      {"label": "Small Farm",      "emoji": "🌱", "base_cost": 100,     "base_income": 1},
    "big_farm":        {"label": "Big Farm",        "emoji": "🌾", "base_cost": 350,     "base_income": 4},
    "mine":            {"label": "Mine",            "emoji": "⛏️", "base_cost": 900,     "base_income": 10},
    "factory":         {"label": "Factory",         "emoji": "🏭", "base_cost": 2500,    "base_income": 30},
    "bank":            {"label": "Bank",            "emoji": "🏦", "base_cost": 8000,    "base_income": 80},
    "lab":             {"label": "Research Lab",    "emoji": "🔬", "base_cost": 20000,   "base_income": 200},
    "city":            {"label": "City",            "emoji": "🏙️", "base_cost": 75000,   "base_income": 700},
    "megacity":        {"label": "Megacity",        "emoji": "🌆", "base_cost": 200000,  "base_income": 2000},
    "power_plant":     {"label": "Power Plant",     "emoji": "⚡", "base_cost": 450000,  "base_income": 5000},
    "server_room":     {"label": "Server Room",     "emoji": "🖥️", "base_cost": 900000,  "base_income": 10000},
    "datacenter":      {"label": "Datacenter",      "emoji": "📡", "base_cost": 2000000, "base_income": 25000},
    "ai_core":         {"label": "AI Core",         "emoji": "🤖", "base_cost": 5000000, "base_income": 75000},
    "portal":          {"label": "Portal",          "emoji": "🌀", "base_cost": 15000000,"base_income": 200000},
    "space_station":   {"label": "Space Station",   "emoji": "🛰️", "base_cost": 35000000,"base_income": 500000},
    "time_machine":    {"label": "Time Machine",    "emoji": "⌛", "base_cost": 90000000,"base_income": 1500000},
    "multiverse":      {"label": "Multiverse Gate","emoji": "🌌","base_cost": 250000000,"base_income": 5000000},
    "omniforge":       {"label": "Omniforge",       "emoji": "🔥", "base_cost": 1000000000,"base_income": 20000000},
}


def building_cost(key: str, owned_count: int) -> int:
    info = BUILDINGS[key]
    return int(info["base_cost"] * (COST_GROWTH ** owned_count))