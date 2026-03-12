from flask import render_template, request, redirect, url_for, flash

from ..blueprint import core_bp
from app.extensions.config import load_matrix_config, save_matrix_config


@core_bp.route("/config", methods=["GET"])
def config_page():
    """Render the config form with the current settings loaded from config.json."""
    cfg = load_matrix_config()
    return render_template("pages/config.html", cfg=cfg)


@core_bp.route("/config/save", methods=["POST"])
def config_save():
    """Validate all form fields, update the config dict, save it to disk, and redirect."""
    cfg = load_matrix_config()
    f = request.form

    # ── Hardware ─────────────────────────────────────────────────────
    pin = f.get("pin", cfg["pin"])
    cfg["pin"] = pin.strip() if pin else "D18"

    try:
        cfg["brightness"] = max(0.0, min(1.0, float(f.get("brightness", cfg["brightness"]))))
    except (TypeError, ValueError):
        flash("Brightness must be a number between 0 and 1.", "danger")

    cfg["auto_write"] = bool(f.get("auto_write"))

    # ── Text scrolling ───────────────────────────────────────────────
    try:
        cfg["scroll_delay"] = max(0.0, float(f.get("scroll_delay", cfg["scroll_delay"])))
    except (TypeError, ValueError):
        flash("Scroll delay must be a positive number.", "danger")

    try:
        cfg["font_baseline_offset"] = int(f.get("font_baseline_offset", cfg["font_baseline_offset"]))
    except (TypeError, ValueError):
        flash("Font offset must be an integer.", "danger")

    # ── GIF playback ─────────────────────────────────────────────────
    try:
        cfg["gif_delay"] = max(0.1, float(f.get("gif_delay", cfg["gif_delay"])))
    except (TypeError, ValueError):
        flash("GIF delay must be a positive number.", "danger")

    # ── Image processing ─────────────────────────────────────────────
    try:
        cfg["contrast"] = max(0.0, float(f.get("contrast", cfg["contrast"])))
    except (TypeError, ValueError):
        flash("Contrast must be a positive number.", "danger")

    try:
        cfg["saturation"] = max(0.0, float(f.get("saturation", cfg["saturation"])))
    except (TypeError, ValueError):
        flash("Saturation must be a positive number.", "danger")

    try:
        cfg["gamma"] = max(0.01, float(f.get("gamma", cfg["gamma"])))
    except (TypeError, ValueError):
        flash("Gamma must be a positive number.", "danger")

    try:
        cfg["posterize_bits"] = max(1, min(8, int(f.get("posterize_bits", cfg["posterize_bits"]))))
    except (TypeError, ValueError):
        flash("Posterize bits must be an integer between 1 and 8.", "danger")

    try:
        cfg["black_level"] = max(0, min(255, int(f.get("black_level", cfg["black_level"]))))
    except (TypeError, ValueError):
        flash("Black level must be an integer between 0 and 255.", "danger")

    try:
        cfg["black_threshold"] = max(0, min(765, int(f.get("black_threshold", cfg["black_threshold"]))))
    except (TypeError, ValueError):
        flash("Black threshold must be an integer between 0 and 765.", "danger")

    cfg["auto_crop"] = bool(f.get("auto_crop"))

    save_matrix_config(cfg)
    flash("Matrix configuration saved.", "success")

    return redirect(url_for("pages.core.config_page"))
