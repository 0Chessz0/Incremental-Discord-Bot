import math
from typing import Dict, Any

BASE_MULTIPLIER = 1.0

CLICK_BASE_GAIN = 1.0

BOOST_PER_LEVEL = 0.10
BOOST_BASE_COST = 100
BOOST_COST_GROWTH = 1.75

REINCARNATION_MIN_RESOURCES = 10_000
REINCARNATION_POINT_BONUS = 0.05

REINC_REWARD_MULTIPLIER = 10.0

COST_GROWTH = 1.18

BUILDINGS: Dict[str, Dict[str, float | str]] = {
    "cursor":        {"label": "Cursor",          "emoji": "🖱️", "base_cost": 10,           "base_income_money": 0.1,      "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "clicker":       {"label": "Clicker",        "emoji": "👆", "base_cost": 25,           "base_income_money": 0.2,      "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "tiny_farm":     {"label": "Tiny Farm",      "emoji": "🥕", "base_cost": 75,           "base_income_money": 0.8,      "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "small_farm":    {"label": "Small Farm",     "emoji": "🌱", "base_cost": 150,          "base_income_money": 1.6,      "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "big_farm":      {"label": "Big Farm",       "emoji": "🌾", "base_cost": 400,          "base_income_money": 4.5,      "base_income_gems": 0.0,        "base_income_dark": 0.0},

    "mine":          {"label": "Mine",             "emoji": "⛏️", "base_cost": 900,          "base_income_money": 11.0,     "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "quarry":        {"label": "Quarry",           "emoji": "🪨", "base_cost": 2_000,        "base_income_money": 28.0,     "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "sawmill":       {"label": "Sawmill",        "emoji": "🪵", "base_cost": 4_000,        "base_income_money": 65.0,     "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "windmill":      {"label": "Windmill",       "emoji": "🌬️", "base_cost": 8_000,        "base_income_money": 140.0,    "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "factory":       {"label": "Factory",        "emoji": "🏭", "base_cost": 18_000,       "base_income_money": 320.0,    "base_income_gems": 0.0,        "base_income_dark": 0.0},

    "bank":          {"label": "Bank",             "emoji": "🏦", "base_cost": 40_000,       "base_income_money": 820.0,    "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "stock_market":  {"label": "Stock Market",   "emoji": "📈", "base_cost": 90_000,       "base_income_money": 1_900.0,  "base_income_gems": 0.0,        "base_income_dark": 0.0},
    "casino":        {"label": "Casino",           "emoji": "🎰", "base_cost": 180_000,      "base_income_money": 4_800.0,  "base_income_gems": 0.02,        "base_income_dark": 0.0},
    "lab":           {"label": "Research Lab",   "emoji": "🔬", "base_cost": 380_000,      "base_income_money": 12_000.0, "base_income_gems": 0.05,        "base_income_dark": 0.0},
    "data_center":   {"label": "Data Center",    "emoji": "🖥️", "base_cost": 900_000,      "base_income_money": 32_000.0, "base_income_gems": 0.1,         "base_income_dark": 0.0},

    "city":          {"label": "City",             "emoji": "🏙️", "base_cost": 2_000_000,    "base_income_money": 85_000.0, "base_income_gems": 0.2,         "base_income_dark": 0.0},
    "megacity":      {"label": "Megacity",         "emoji": "🌆", "base_cost": 6_000_000,    "base_income_money": 240_000.0,"base_income_gems": 0.4,         "base_income_dark": 0.0},
    "fusion_plant":  {"label": "Fusion Plant",   "emoji": "⚛️", "base_cost": 18_000_000,   "base_income_money": 700_000.0,"base_income_gems": 0.8,         "base_income_dark": 0.0},
    "spaceport":     {"label": "Spaceport",        "emoji": "🚀", "base_cost": 50_000_000,   "base_income_money": 2_000_000.0,"base_income_gems": 1.5,        "base_income_dark": 0.0},
    "orbital_ring":  {"label": "Orbital Ring",   "emoji": "🛸", "base_cost": 120_000_000,  "base_income_money": 5_500_000.0,"base_income_gems": 3.0,        "base_income_dark": 0.0},

    "gem_mine":      {"label": "Gem Mine",         "emoji": "💎", "base_cost": 300_000,      "base_income_money": 500.0,    "base_income_gems": 0.2,         "base_income_dark": 0.0},
    "crystal_cavern":{"label": "Crystal Cavern","emoji": "💠","base_cost": 1_500_000,    "base_income_money": 3_000.0,  "base_income_gems": 0.8,         "base_income_dark": 0.0},
    "gem_factory":   {"label": "Gem Factory",    "emoji": "🏭", "base_cost": 8_000_000,    "base_income_money": 15_000.0, "base_income_gems": 2.5,         "base_income_dark": 0.0},
    "gem_world":     {"label": "Gem World",      "emoji": "🌍", "base_cost": 45_000_000,   "base_income_money": 80_000.0, "base_income_gems": 8.0,         "base_income_dark": 0.0},

    "dark_orb":      {"label": "Dark Orb",         "emoji": "🪐", "base_cost": 250_000_000,  "base_income_money": 300_000.0,"base_income_gems": 12.0,        "base_income_dark": 0.0003},
    "void_lab":      {"label": "Void Lab",         "emoji": "🕳️", "base_cost": 900_000_000,"base_income_money": 900_000.0,"base_income_gems": 30.0,        "base_income_dark": 0.0015},
    "dark_forge":    {"label": "Dark Forge",     "emoji": "⚙️", "base_cost": 3_000_000_000,"base_income_money": 3_000_000.0,"base_income_gems": 80.0,    "base_income_dark": 0.006},
    "void_engine":   {"label": "Void Engine",    "emoji": "♾️", "base_cost": 10_000_000_000,"base_income_money": 9_000_000.0,"base_income_gems": 200.0,"base_income_dark": 0.02},

    "time_lab":      {"label": "Time Lab",         "emoji": "⌛", "base_cost": 40_000_000_000,"base_income_money": 25_000_000.0,"base_income_gems": 320.0,"base_income_dark": 0.06},
    "time_rift":     {"label": "Time Rift",        "emoji": "🌀", "base_cost": 150_000_000_000,"base_income_money": 80_000_000.0,"base_income_gems": 800.0,"base_income_dark": 0.15},
    "quantum_core":  {"label": "Quantum Core",   "emoji": "🧬", "base_cost": 600_000_000_000,"base_income_money": 230_000_000.0,"base_income_gems": 2000.0,"base_income_dark": 0.45},
    "multiverse":    {"label": "Multiverse Gate","emoji": "🌌", "base_cost": 2_000_000_000_000,"base_income_money": 800_000_000.0,"base_income_gems": 6000.0,"base_income_dark": 1.5},
}

GEM_UPGRADES: Dict[str, Dict[str, float | str | int]] = {
    "click_power": {
        "label": "Click Power",
        "description": "Increase resources gained per click.",
        "base_cost": 10,
        "cost_growth": 1.4,
        "max_level": 100,
        "click_mult_per_level": 0.05,
    },
    "income_boost": {
        "label": "Production Boost",
        "description": "Increase all income from buildings.",
        "base_cost": 50,
        "cost_growth": 1.5,
        "max_level": 100,
        "income_mult_per_level": 0.03,
    },
    "cost_discount": {
        "label": "Shop Discount",
        "description": "Reduce building costs.",
        "base_cost": 75,
        "cost_growth": 1.6,
        "max_level": 50,
        "discount_per_level": 0.01,
    },
}

DARK_UPGRADES: Dict[str, Dict[str, float | str | int]] = {
    "reinc_boost": {
        "label": "Reincarnation Boost",
        "description": "Multiply reincarnation rewards.",
        "base_cost": 1.0,
        "cost_growth": 2.5,
        "max_level": 50,
        "reinc_mult_per_level": 0.5,
    },
    "global_mult": {
        "label": "Reality Warp",
        "description": "Multiply all production and clicks.",
        "base_cost": 2.0,
        "cost_growth": 3.0,
        "max_level": 50,
        "global_mult_per_level": 0.25,
    },
}

def compute_upgrade_effects(user: Dict[str, Any]) -> Dict[str, float]:
    effects = {
        "click_mult": 1.0,
        "income_mult": 1.0,
        "cost_discount": 0.0,
        "reinc_mult": 1.0,
        "global_mult": 1.0,
    }

    gem_upgrades = user.get("gem_upgrades", {})
    dark_upgrades = user.get("dark_upgrades", {})

    for key, lvl in gem_upgrades.items():
        cfg = GEM_UPGRADES.get(key)
        if not cfg or lvl <= 0:
            continue
        lvl = int(lvl)
        if "click_mult_per_level" in cfg:
            effects["click_mult"] += lvl * float(cfg["click_mult_per_level"])
        if "income_mult_per_level" in cfg:
            effects["income_mult"] += lvl * float(cfg["income_mult_per_level"])
        if "discount_per_level" in cfg:
            effects["cost_discount"] += lvl * float(cfg["discount_per_level"])

    effects["cost_discount"] = min(effects["cost_discount"], 0.9)

    for key, lvl in dark_upgrades.items():
        cfg = DARK_UPGRADES.get(key)
        if not cfg or lvl <= 0:
            continue
        lvl = int(lvl)
        if "reinc_mult_per_level" in cfg:
            effects["reinc_mult"] += lvl * float(cfg["reinc_mult_per_level"])
        if "global_mult_per_level" in cfg:
            effects["global_mult"] += lvl * float(cfg["global_mult_per_level"])

    return effects


def compute_income_all(buildings: Dict[str, int]) -> Dict[str, float]:
    income_money = 0.0
    income_gems = 0.0
    income_dark = 0.0

    for key, count in buildings.items():
        if count <= 0:
            continue
        info = BUILDINGS.get(key)
        if not info:
            continue
        income_money += count * float(info["base_income_money"])
        income_gems += count * float(info["base_income_gems"])
        income_dark += count * float(info["base_income_dark"])

    return {
        "money": income_money,
        "gems": income_gems,
        "dark": income_dark,
    }


def get_effective_incomes(user: Dict[str, Any]) -> Dict[str, float]:
    base = compute_income_all(user.get("buildings", {}))
    eff = compute_upgrade_effects(user)
    money = base["money"] * eff["income_mult"] * eff["global_mult"]
    gems = base["gems"] * eff["income_mult"]
    dark = base["dark"] * eff["income_mult"]
    return {
        "money": money,
        "gems": gems,
        "dark": dark,
    }


def compute_income_per_sec(buildings: Dict[str, int]) -> float:
    return compute_income_all(buildings)["money"]


def building_cost(building_key: str, owned_count: int) -> int:
    info = BUILDINGS[building_key]
    base_cost = float(info["base_cost"])
    return int(base_cost * (COST_GROWTH ** owned_count))


def get_gem_upgrade_cost(key: str, level: int) -> int:
    cfg = GEM_UPGRADES[key]
    base = float(cfg["base_cost"])
    growth = float(cfg["cost_growth"])
    return int(base * (growth ** level))


def get_dark_upgrade_cost(key: str, level: int) -> float:
    cfg = DARK_UPGRADES[key]
    base = float(cfg["base_cost"])
    growth = float(cfg["cost_growth"])
    return float(base * (growth ** level))


def update_multiplier(user: Dict[str, Any]) -> float:
    boost_level = user.get("boost_level", 0)
    r_points = user.get("reincarnation_points", 0)
    m = (
        BASE_MULTIPLIER
        + boost_level * BOOST_PER_LEVEL
        + r_points * REINCARNATION_POINT_BONUS
    )
    user["multiplier"] = m
    return m


def get_click_gain(user: Dict[str, Any]) -> float:
    m = update_multiplier(user)
    eff = compute_upgrade_effects(user)
    return CLICK_BASE_GAIN * m * eff["click_mult"] * eff["global_mult"]


def boost_cost(boost_level: int) -> int:
    return int(BOOST_BASE_COST * (BOOST_COST_GROWTH ** boost_level))


def calc_reincarnation_reward(user: Dict[str, Any]) -> int:
    lifetime = user.get("lifetime_resources", 0.0)

    if lifetime < REINCARNATION_MIN_RESOURCES:
        return 0

    ratio = lifetime / REINCARNATION_MIN_RESOURCES

    raw_points = (ratio ** 0.9) * REINC_REWARD_MULTIPLIER

    eff = compute_upgrade_effects(user)
    raw_points *= eff["reinc_mult"]

    points = int(raw_points)
    return max(points, 1)


def reincarnate_user(user: Dict[str, Any]) -> Dict[str, Any]:
    reward = calc_reincarnation_reward(user)
    if reward <= 0:
        return user

    user["reincarnations"] = user.get("reincarnations", 0) + 1

    user["reincarnation_points"] = user.get("reincarnation_points", 0) + reward

    user["resources"] = 0.0
    user["gems"] = 0.0
    user["dark_matter"] = 0.0
    user["income_per_sec"] = 0.0
    user["gems_per_sec"] = 0.0
    user["dark_per_sec"] = 0.0
    user["total_clicks"] = 0
    user["level"] = 1
    user["buildings"] = {key: 0 for key in BUILDINGS}
    update_multiplier(user)
    return user