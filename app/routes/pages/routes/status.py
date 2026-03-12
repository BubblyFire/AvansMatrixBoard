from flask import jsonify
from ..blueprint import core_bp
from ..utils.state import get_now_playing


@core_bp.route("/status")
def status_route():
    return jsonify(get_now_playing())
