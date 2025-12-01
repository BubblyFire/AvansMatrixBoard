from flask import render_template, request
from app.extensions import matrixpi
from ..blueprint import core_bp 

@core_bp.route("/text")
def text_route():
    return render_template("pages/text.html")

@core_bp.route("/text2", methods=["POST"])
def text_route_post():
    json_request = request.get_json()
    text = json_request["text"]
    hex_color = json_request["color"]
    line = json_request["line"]

    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    matrixpi.matrixboard.clear_line(line)
    matrixpi.matrixboard.render_text(0, line, text, rgb_color)
    matrixpi.matrixboard.show()
    return ""