"""
app/extensions/config.py — Persistent configuration for the LED matrix.

Settings are stored in app/config/config.json (created on first save).
DEFAULT_MATRIX_CONFIG defines all supported keys and their default values.

Use load_matrix_config() to get the current settings (merges file with defaults).
Use save_matrix_config(cfg) to persist a new set of settings to disk.

All route and extension code should call load_matrix_config() instead of
reading the JSON file directly, so defaults are always applied correctly.
"""

import json
import os
from flask import current_app

DEFAULT_MATRIX_CONFIG = {
    # Hardware
    "pin": "D18",
    "brightness": 0.3,
    "auto_write": False,

    # Text scrolling
    "scroll_delay": 0.1,
    "font_baseline_offset": 3,

    # GIF playback
    "gif_delay": 1.0,

    # Captive portal redirect URL (SoftAP IP)
    "portal_redirect": "http://192.168.50.5/",
    
    # Image processing
    "contrast": 1.20,
    "saturation": 1.20,
    "gamma": 0.70,
    "posterize_bits": 5,
    "black_level": 6,
    "black_threshold": 28,
    "auto_crop": True,
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config", "config.json") 

def load_matrix_config() -> dict:
    """
    Return the current matrix config as a dict.

    Starts from DEFAULT_MATRIX_CONFIG and overlays any values found in the
    JSON file, so missing keys always fall back to a safe default.
    """
    cfg = DEFAULT_MATRIX_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                cfg.update(data)
    except (OSError, ValueError):
        # File doesn't exist yet or is corrupt — use defaults silently
        pass

    return cfg

def save_matrix_config(cfg: dict) -> None:
    """
    Write cfg to disk, keeping only the known keys from DEFAULT_MATRIX_CONFIG.

    Unknown/extra keys are stripped to keep the config file clean.
    """
    # Only persist keys that belong to the known schema
    filtered = {k: cfg.get(k, v) for k, v in DEFAULT_MATRIX_CONFIG.items()}

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(filtered, f, indent=4)
        print(f"[MatrixConfig] Saved config to {CONFIG_FILE}")
    except Exception as e:
        print(f"[MatrixConfig] Failed to save config: {e}")
