from flask import render_template, request, redirect, url_for, flash

from ..blueprint import core_bp
from app.extensions.config import load_matrix_config, save_matrix_config


@core_bp.route("/config", methods=["GET"])
def config_page():
    cfg = load_matrix_config()
    return render_template("pages/config.html", cfg=cfg)


@core_bp.route("/config/save", methods=["POST"])
def config_save():
    cfg = load_matrix_config()

    pin = request.form.get("pin", cfg.get("pin"))
    brightness = request.form.get("brightness", cfg.get("brightness"))
    auto_write = request.form.get("auto_write")
    scroll_delay = request.form.get("scroll_delay", cfg.get("scroll_delay"))
    font_offset = request.form.get("font_baseline_offset", cfg.get("font_baseline_offset"))
    gif_delay = request.form.get("gif_delay", cfg.get("gif_delay", 1.0))

    cfg["pin"] = pin.strip() if pin else "D18"

    try:
        cfg["brightness"] = max(0.0, min(1.0, float(brightness)))
    except (TypeError, ValueError):
        flash("Brightness must be a number between 0 and 1.", "danger")

    cfg["auto_write"] = bool(auto_write)

    try:
        cfg["scroll_delay"] = max(0.0, float(scroll_delay))
    except (TypeError, ValueError):
        flash("Scroll delay must be a positive number.", "danger")

    try:
        cfg["font_baseline_offset"] = int(font_offset)
    except (TypeError, ValueError):
        flash("Font offset must be an integer.", "danger")

    try:
        cfg["gif_delay"] = max(0.1, float(gif_delay))
    except (TypeError, ValueError):
        flash("GIF delay must be a positive number.", "danger")

    save_matrix_config(cfg)

    flash("Matrix configuration saved.", "success")

    return redirect(url_for("core.config_page"))
