import os
from flask import render_template, request, jsonify
from ..blueprint import core_bp
from ..utils.utils import start_slideshow, start_slideshow_playlist, stop_slideshow, safe_join_under_root
from ..utils.state import get_slideshow_state
from ..utils.config import VIRTUAL_MOUNTS

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}


def _resolve_virtual(virtual_path: str):
    """Resolve a virtual path like 'uploads/sub/file.png' to an absolute path, or None on error."""
    parts = virtual_path.strip("/").split("/", 1)
    mount = parts[0]
    sub   = parts[1] if len(parts) > 1 else ""
    if mount not in VIRTUAL_MOUNTS:
        return None
    real_root = os.path.realpath(VIRTUAL_MOUNTS[mount])
    try:
        return safe_join_under_root(real_root, sub) if sub else real_root
    except ValueError:
        return None


@core_bp.route("/slideshow")
def slideshow_route():
    return render_template("pages/slideshow.html")


@core_bp.route("/slideshow/start", methods=["POST"])
def slideshow_start():
    data     = request.get_json()
    mode     = data.get("mode", "folder")
    interval = max(1.0, min(300.0, float(data.get("interval", 5))))

    if mode == "folder":
        virtual_path = (data.get("path") or "").strip("/")
        abs_folder   = _resolve_virtual(virtual_path)
        if not abs_folder or not os.path.isdir(abs_folder):
            return jsonify({"error": "Folder not found"}), 404
        start_slideshow(abs_folder, interval)

    elif mode == "playlist":
        virtual_files = data.get("files", [])

        # Resolve each virtual path to an absolute path and keep only valid image files
        abs_files = []
        for vp in virtual_files:
            p = _resolve_virtual(vp.strip("/"))
            if p and os.path.isfile(p) and os.path.splitext(p)[1].lower() in IMAGE_EXTENSIONS:
                abs_files.append(p)

        if not abs_files:
            return jsonify({"error": "No valid image files in playlist"}), 400
        start_slideshow_playlist(abs_files, interval)

    else:
        return jsonify({"error": "Unknown mode"}), 400

    return jsonify({"ok": True})


@core_bp.route("/slideshow/stop", methods=["POST"])
def slideshow_stop_route():
    stop_slideshow()
    return jsonify({"ok": True})


@core_bp.route("/slideshow/status")
def slideshow_status():
    return jsonify(get_slideshow_state())
