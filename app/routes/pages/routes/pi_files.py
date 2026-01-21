import os
import mimetypes
import shutil

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


@core_bp.route("/pi/path/delete", methods=["POST"])
def pi_path_delete():
    data = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")

    if not rel_path:
        return jsonify({"error": "missing path"}), 400

    try:
        abs_path = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if os.path.isfile(abs_path):
        os.remove(abs_path)
        return jsonify({"ok": True})

    if os.path.isdir(abs_path):
        try:
            os.rmdir(abs_path)
            return jsonify({"ok": True})
        except OSError:
            return jsonify({"error": "directory not empty"}), 400

    return jsonify({"error": "not found"}), 404

@core_bp.route("/pi/path/rename", methods=["POST"])
def pi_path_rename():
    data = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")
    new_name = (data.get("new_name") or "").strip().strip("/")

    if not rel_path or not new_name:
        return jsonify({"error": "missing path or new_name"}), 400

    try:
        src_abs = safe_join_under_root(FILE_BROWSER_ROOT, rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.exists(src_abs):
        return jsonify({"error": "not found"}), 404

    parent_rel = os.path.dirname(rel_path)
    try:
        dst_abs = safe_join_under_root(FILE_BROWSER_ROOT, parent_rel, new_name)
    except ValueError:
        return jsonify({"error": "invalid target"}), 400

    if os.path.exists(dst_abs):
        return jsonify({"error": "target exists"}), 400

    os.rename(src_abs, dst_abs)
    dst_rel = "/".join(p for p in [parent_rel, new_name] if p)
    return jsonify({"ok": True, "path": dst_rel})

@core_bp.route("/pi/path/move", methods=["POST"])
def pi_path_move():
    data = request.get_json() or {}
    src = (data.get("src") or "").strip("/")
    dst_dir = (data.get("dst_dir") or "").strip("/")

    if not src:
        return jsonify({"error": "missing src"}), 400

    try:
        src_abs = safe_join_under_root(FILE_BROWSER_ROOT, src)
        dst_dir_abs = safe_join_under_root(FILE_BROWSER_ROOT, dst_dir)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.exists(src_abs):
        return jsonify({"error": "src not found"}), 404
    if not os.path.isdir(dst_dir_abs):
        return jsonify({"error": "dst_dir not a directory"}), 400

    name = os.path.basename(src_abs)
    dst_abs = os.path.join(dst_dir_abs, name)
    if os.path.exists(dst_abs):
        return jsonify({"error": "target exists"}), 400

    shutil.move(src_abs, dst_abs)
    dst_rel = "/".join(p for p in [dst_dir, name] if p)
    return jsonify({"ok": True, "path": dst_rel})

