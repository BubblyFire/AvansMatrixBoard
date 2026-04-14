from flask import render_template, jsonify
from app.extensions import matrixpi
from ..blueprint import core_bp


@core_bp.route("/preview")
def preview_route():
    """Render the live matrix-preview page."""
    return render_template(
        "pages/preview.html",
        width=matrixpi.matrixboard._width,
        height=matrixpi.matrixboard._height,
    )


@core_bp.route("/preview/state")
def preview_state():
    """
    Return the current shadow pixel buffer for the browser to render.

    Response:
      {
        "width":  30,
        "height": 30,
        "pixels": [[r, g, b], [r, g, b], ...]   # row-major, top-left first
      }
    """
    board = matrixpi.matrixboard
    return jsonify({
        "width":  board._width,
        "height": board._height,
        "pixels": board.get_pixels(),
    })
