import os
import mimetypes

from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename 

from ..blueprint import core_bp
from ..utils.config import FILE_BROWSER_ROOT
from ..utils.utils import safe_join_under_root, show_file


@core_bp.route("/pi/files", methods=["POST"])
def pi_files_list():
    data = request.get_json(silent=True) or {}
    rel_path = (data.get("path") or "").strip("/")

    try:
        abs_path = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.isdir(abs_path):
        return jsonify({"error": "not a directory"}), 400

    dirs = []
    files = []

    for name in sorted(os.listdir(abs_path)):
        full = os.path.join(abs_path, name)
        if os.path.isdir(full):
            dirs.append(name)
        elif os.path.isfile(full):
            files.append(name)

    return jsonify(
        {
            "path": rel_path,
            "dirs": dirs,
            "files": files,
        }
    )


@core_bp.route("/pi/dir/mkdir", methods=["POST"])
def pi_files_mkdir():
    data = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")
    name = (data.get("name") or "").strip("/")

    if not name:
        return jsonify({"error": "missing name"}), 400

    try:
        target_dir = safe_join_under_root(FILE_BROWSER_ROOT, rel_path, name)
        os.makedirs(target_dir, exist_ok=True)
        return jsonify({"ok": True})
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    except OSError as e:
        return jsonify({"error": str(e)}), 500


@core_bp.route("/pi/file/preview", methods=["GET"])
def pi_files_preview():
    rel_path = (request.args.get("path") or "").strip("/")

    try:
        abs_path = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return "invalid path", 400

    if not os.path.isfile(abs_path):
        return "not found", 404

    mime, _ = mimetypes.guess_type(abs_path)
    return send_file(abs_path, mimetype=mime or "application/octet-stream")


@core_bp.route("/pi/file/display", methods=["POST"])
def pi_files_use():
    data = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")

    if not rel_path:
        return jsonify({"error": "missing path"}), 400

    try:
        abs_path = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.isfile(abs_path):
        return jsonify({"error": "file not found"}), 404

    show_file(abs_path)

    return jsonify({"ok": True})

@core_bp.route("/pi/file/upload", methods=["POST"])
def pi_file_upload():
    if "file" not in request.files:
        return jsonify({"error": "missing file"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400

    rel_path = (request.form.get("path") or "").strip("/")
    filename = secure_filename(f.filename)

    try:
        target_dir = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError as e:
        return jsonify({"error": str(e)}), 500

    target_abs = os.path.join(target_dir, filename)
    try:
        f.save(target_abs)
    except OSError as e:
        return jsonify({"error": str(e)}), 500

    rel_saved = "/".join(p for p in [rel_path, filename] if p)

    return jsonify({"ok": True, "path": rel_saved})