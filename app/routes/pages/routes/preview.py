from flask import render_template, jsonify, abort
from app.extensions import matrixpi
from ..blueprint import core_bp


@core_bp.route("/preview")
def preview_route():
    """Render the live matrix-preview page. Hidden when real LEDs are attached."""
    board = matrixpi.matrixboard

    if board.hardware:
        abort(404)

    return render_template(
        "pages/preview.html",
        width=board._width,
        height=board._height,
    )


@core_bp.route("/preview/state")
def preview_state():
    """
    Return the current shadow pixel buffer for the browser to render.

    Returns 404 when real LEDs are attached — the web preview is a no-hardware
    development aid, not a mirror of the physical board.

    Response:
      {
        "width":  30,
        "height": 30,
        "pixels": [[r, g, b], [r, g, b], ...]   # row-major, top-left first
      }
    """

    board = matrixpi.matrixboard
    
    if board.hardware:
        abort(404)

    return jsonify({
        "width":  board._width,
        "height": board._height,
        "pixels": board.get_pixels(),
    })
