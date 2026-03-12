from flask import render_template, request
from app.extensions import matrixpi
from ..blueprint import core_bp
from ..utils.state import set_now_playing

@core_bp.route("/text")
def text_route():
    """Render the text-input page."""
    return render_template("pages/text.html")

@core_bp.route("/text2", methods=["POST"])
def send_text():
    """
    Write a single line of text on the matrix at the requested row.

    Expects JSON: {"text": "Hello", "color": "#ff0000", "line": 0}
    Clears only the target row before rendering so other rows are untouched.
    """
    # Skip if running without physical hardware
    if matrixpi.matrixboard is None:
        return "", 200

    json_request = request.get_json()
    text = json_request["text"]
    hex_color = json_request["color"]
    line = json_request["line"]

    # Convert hex color (e.g. "#ff0000") to an (r, g, b) tuple.
    # lstrip removes the leading "#", then each pair of characters is
    # a hex byte: positions 0-1 = red, 2-3 = green, 4-5 = blue.
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    rgb_color = (r, g, b)

    matrixpi.matrixboard.clear_line(line)
    matrixpi.matrixboard.render_text(0, line, text, rgb_color)
    matrixpi.matrixboard.show()
    set_now_playing("text", text[:30])
    return ""