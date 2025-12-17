import json
import os
from flask import current_app

DEFAULT_MATRIX_CONFIG = {
    "pin": "D18",
    "brightness": 0.3,
    "auto_write": False,
    "scroll_delay": 0.1,
    "font_baseline_offset": 3
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config", "config.json") 

def load_matrix_config():
    cfg = DEFAULT_MATRIX_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                cfg.update(data)
    except (OSError, ValueError):
        pass

    return cfg

def save_matrix_config(cfg: dict):
    filtered = {k: cfg.get(k, v) for k, v in DEFAULT_MATRIX_CONFIG.items()}

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(filtered, f, indent=4)
        print(f"[MatrixConfig] Saved config to {CONFIG_FILE}")
    except Exception as e:
        print(f"[MatrixConfig] Failed to save config: {e}")
