from flask import render_template, request
from app.extensions import matrixpi
from ..blueprint import core_bp 

@core_bp.route("/draw")
def draw_route():
    return render_template("pages/draw.html")

@core_bp.route("/sendtoboard", methods=["POST"])
def callback_route():
    data = request.get_json()
    data = data["value"]

    matrixpi.matrixboard.clear()
    for i in range(len(data)):
        y = i // 30
        x = i % 30
        color_string = data[i]
        color_values = color_string[color_string.find("(") + 1 : color_string.find(")")]
        color_values = color_values.replace(" ", "")
        color_values_list = color_values.split(",")
        if len(color_values_list) == 3:
            cl = (
                int(color_values_list[0]),
                int(color_values_list[1]),
                int(color_values_list[2]),
            )
            matrixpi.matrixboard._draw_pixel(x, y, cl)
        else:
            matrixpi.matrixboard._draw_pixel(x, y, (0, 0, 0))

    matrixpi.matrixboard.show()
    return ""
