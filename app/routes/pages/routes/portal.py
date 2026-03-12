from flask import redirect
from ..blueprint import core_bp
from app.extensions.config import load_matrix_config

# iOS and macOS check this URL
@core_bp.route('/hotspot-detect.html')
def portal_ios():
    return redirect(load_matrix_config()["portal_redirect"])

# Android and Chrome check this URL
@core_bp.route('/generate_204')
def portal_android():
    return redirect(load_matrix_config()["portal_redirect"])

# Windows checks this URL
@core_bp.route('/ncsi.txt')
def portal_windows():
    return redirect(load_matrix_config()["portal_redirect"])
