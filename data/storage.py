import json
import os
import time
from typing import Dict, Any

from .balance import (
    BUILDINGS,
    GEM_UPGRADES,
    DARK_UPGRADES,
    get_effective_incomes,
    update_multiplier,
)


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USERDATA_DIR = os.path.join(ROOT_DIR, "userdata")


def _ensure_dirs() -> None:
    os.makedirs(USERDATA_DIR, exist_ok=True)


def _user_path(user_id: int) -> str:
    _ensure_dirs()
    return os.path.join(USERDATA_DIR, f"{user_id}.json")


def _new_user() -> Dict[str, Any]:
    user = {
        "resources": 0.0,
        "gems": 0.0,
        "dark_matter": 0.0,
        "income_per_sec": 0.0,
        "gems_per_sec": 0.0,
        "dark_per_sec": 0.0,
        "multiplier": 1.0,
        "total_clicks": 0,
        "level": 1,
        "last_update": None,
        "lifetime_resources": 0.0,
        "buildings": {key: 0 for key in BUILDINGS},
        "boost_level": 0,
        "reincarnations": 0,
        "reincarnation_points": 0,
        "gem_upgrades": {key: 0 for key in GEM_UPGRADES},
        "dark_upgrades": {key: 0 for key in DARK_UPGRADES},
    }
    update_multiplier(user)
    return user


def _load_user(user_id: int) -> Dict[str, Any]:
    path = _user_path(user_id)
    if not os.path.exists(path):
        user = _new_user()
        user["last_update"] = time.time()
        _save_user(user_id, user)
        return user
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    template = _new_user()
    for key, default in template.items():
        if key not in data:
            data[key] = default
    return data


def _save_user(user_id: int, user: Dict[str, Any]) -> None:
    path = _user_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4)


def _apply_passive(user: Dict[str, Any]) -> Dict[str, Any]:
    now = time.time()
    last = user.get("last_update")
    if last is None:
        user["last_update"] = now
        return user

    elapsed = max(0.0, now - last)

    incomes = get_effective_incomes(user)
    user["income_per_sec"] = incomes["money"]
    user["gems_per_sec"] = incomes["gems"]
    user["dark_per_sec"] = incomes["dark"]

    update_multiplier(user)

    gained_money = elapsed * user["income_per_sec"] * user["multiplier"]
    gained_gems = elapsed * user["gems_per_sec"]
    gained_dark = elapsed * user["dark_per_sec"]

    user["resources"] += gained_money
    user["gems"] += gained_gems
    user["dark_matter"] += gained_dark

    user["lifetime_resources"] = user.get("lifetime_resources", 0.0) + gained_money
    user["last_update"] = now

    user["level"] = max(1, int(user["lifetime_resources"] // 1_000) + 1)
    return user


def get_or_create_user(user_id: int) -> Dict[str, Any]:
    user = _load_user(user_id)
    user = _apply_passive(user)
    _save_user(user_id, user)
    return user


def save_user(user_id: int, user: Dict[str, Any]) -> None:
    _save_user(user_id, user)