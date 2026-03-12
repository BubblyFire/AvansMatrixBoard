import os
from datetime import datetime
from flask import render_template, request, jsonify, send_from_directory
from PIL import Image
from app.extensions import matrixpi
from ..blueprint import core_bp
from ..utils.utils import clear_matrix
from ..utils.state import set_now_playing
from ..utils.config import DRAWINGS_FOLDER, MATRIX_SIZE


@core_bp.route("/draw")
def draw_route():
    """Render the interactive 30×30 pixel-art editor."""
    return render_template("pages/draw.html")


def parse_rgb_string(color_string: str) -> tuple:
    # Parse a CSS rgb() string like 'rgb(255, 0, 0)' into an (r, g, b) tuple.
    inner = color_string[color_string.find("(") + 1 : color_string.find(")")]
    parts = inner.replace(" ", "").split(",")
    if len(parts) == 3:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    return (0, 0, 0)


@core_bp.route("/sendtoboard", methods=["POST"])
def send_to_board():
    """
    Receive the canvas pixel data from the browser and push it to the matrix.

    Expects JSON: {"value": ["rgb(r,g,b)", …]}  — a flat array of 900 colour strings,
    row-major order (left-to-right, top-to-bottom).
    The frontend debounces calls to this endpoint (150 ms) to avoid flooding the Pi.
    """
    # Skip if running without physical hardware
    if matrixpi.matrixboard is None:
        return "", 200

    pixels = request.get_json()["value"]
    board_width = matrixpi.matrixboard._width

    clear_matrix()

    for i, color_string in enumerate(pixels):
        x = i % board_width
        y = i // board_width
        color = parse_rgb_string(color_string)
        matrixpi.matrixboard._draw_pixel(x, y, color)

    matrixpi.matrixboard.show()
    set_now_playing("drawing")
    return ""


@core_bp.route("/draw/save", methods=["POST"])
def draw_save():
    """Save the current canvas as a PNG to the drawings folder."""
    body   = request.get_json()
    pixels = body.get("pixels", [])
    name   = (body.get("name") or "").strip()

    if len(pixels) != MATRIX_SIZE * MATRIX_SIZE:
        return jsonify({"error": "Invalid pixel data"}), 400

    # Build a safe filename: use provided name or fall back to timestamp
    if name:
        safe_name = "".join(c for c in name if c.isalnum() or c in " _-").strip()
        safe_name = safe_name.replace(" ", "_") or "drawing"
    else:
        safe_name = "drawing_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = safe_name + ".png"
    save_path = os.path.join(DRAWINGS_FOLDER, filename)

    if os.path.exists(save_path):
        base = safe_name + "_" + datetime.now().strftime("%H%M%S")
        filename = base + ".png"
        save_path = os.path.join(DRAWINGS_FOLDER, filename)

    img = Image.new("RGB", (MATRIX_SIZE, MATRIX_SIZE))
    for i, hex_color in enumerate(pixels):
        x = i % MATRIX_SIZE
        y = i // MATRIX_SIZE
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        img.putpixel((x, y), (r, g, b))

    img.save(save_path)
    return jsonify({"ok": True, "filename": filename})


@core_bp.route("/draw/list", methods=["GET"])
def draw_list():
    """Return saved drawings, newest first."""
    files = sorted(
        (f for f in os.listdir(DRAWINGS_FOLDER) if f.endswith(".png")),
        reverse=True,
    )
    return jsonify({"drawings": files})


@core_bp.route("/draw/file/<filename>")
def draw_file(filename):
    """Serve a saved drawing file."""
    return send_from_directory(DRAWINGS_FOLDER, filename)


@core_bp.route("/draw/delete/<filename>", methods=["DELETE"])
def draw_delete(filename):
    """Delete a saved drawing."""
    path = os.path.join(DRAWINGS_FOLDER, filename)
    if not os.path.isfile(path):
        return jsonify({"error": "Not found"}), 404
    os.remove(path)
    return jsonify({"ok": True})
