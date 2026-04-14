from flask import jsonify
from ..blueprint import core_bp
from ..utils.utils import clear_matrix


@core_bp.route("/clear", methods=["POST"])
def clear_route():
    """Stop any running animation/slideshow and turn off all LEDs."""
    clear_matrix()
    return jsonify({"ok": True})
