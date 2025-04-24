import os
import json
from datetime import datetime

POSITION_DIR = "positions"
os.makedirs(POSITION_DIR, exist_ok=True)

def _get_position_file(ticker, strategy=None):
    suffix = f"-{strategy}" if strategy else ""
    return os.path.join(POSITION_DIR, f"{ticker}{suffix}.json")

def _default_position():
    return {
        "has_position": False,
        "avg_buy_price": 0,
        "entry_time": None,
        "entry_strategy": None,
        "split_level": 0,
        "position_size": 0,
        "stop_loss": 0,
        "take_profit_levels": [],
        "trailing_max": 0,
        "trailing_stop_gap": 0
    }

def load_position(ticker, strategy=None):
    path = _get_position_file(ticker, strategy)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return _default_position()

def save_position(ticker, position, strategy=None):
    path = _get_position_file(ticker, strategy)
    with open(path, "w") as f:
        json.dump(position, f, indent=2)

def reset_position(ticker, strategy=None):
    save_position(ticker, _default_position(), strategy)

def record_entry(ticker, price, strategy, level, size, stop_loss, take_profit_levels, trailing_gap):
    pos = load_position(ticker, strategy)
    pos.update({
        "has_position": True,
        "avg_buy_price": price,
        "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "entry_strategy": strategy,
        "split_level": level,
        "position_size": size,
        "stop_loss": stop_loss,
        "take_profit_levels": take_profit_levels,
        "trailing_max": price,
        "trailing_stop_gap": trailing_gap
    })
    save_position(ticker, pos, strategy)

def update_trailing_max(ticker, current_price, strategy=None):
    pos = load_position(ticker, strategy)
    if current_price > pos.get("trailing_max", 0):
        pos["trailing_max"] = current_price
        save_position(ticker, pos, strategy)

def increase_split_level(ticker, strategy=None):
    pos = load_position(ticker, strategy)
    pos["split_level"] += 1
    save_position(ticker, pos, strategy)
