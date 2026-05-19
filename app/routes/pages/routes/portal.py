from flask import redirect
from ..blueprint import core_bp
from app.extensions.config import load_matrix_config


def _portal_target() -> str:
    """Return the captive-portal redirect URL, falling back to the local root."""
    return load_matrix_config().get("portal_redirect") or "/"

# iOS and macOS check this URL
@core_bp.route('/hotspot-detect.html')
def portal_ios():
    return redirect(_portal_target())

# Android and Chrome check this URL
@core_bp.route('/generate_204')
def portal_android():
    return redirect(_portal_target())

# Windows checks this URL
@core_bp.route('/ncsi.txt')
def portal_windows():
    return redirect(_portal_target())
