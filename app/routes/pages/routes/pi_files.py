import os
import mimetypes
import shutil

from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename

from ..blueprint import core_bp
from ..utils.config import VIRTUAL_MOUNTS
from ..utils.utils import safe_join_under_root, show_file


def _split_virtual(rel_path: str) -> tuple[str, str]:
    """Split 'mount/sub/path' into (mount_name, sub_path). Raises ValueError for unknown mounts."""
    rel_path = (rel_path or "").strip("/")
    parts = rel_path.split("/", 1)
    mount = parts[0]
    sub   = parts[1] if len(parts) > 1 else ""
    if mount not in VIRTUAL_MOUNTS:
        raise ValueError(f"Unknown mount: {mount!r}")
    return mount, sub


def _resolve(rel_path: str) -> tuple[str, str]:
    """
    Resolve a virtual path to (abs_path, real_root).
    real_root is the mount's base directory; used for safe-join validation.
    """
    mount, sub = _split_virtual(rel_path)
    real_root  = os.path.realpath(VIRTUAL_MOUNTS[mount])
    abs_path   = safe_join_under_root(real_root, sub) if sub else real_root
    return abs_path, real_root


@core_bp.route("/pi/files", methods=["POST"])
def pi_files_list():
    data     = request.get_json(silent=True) or {}
    rel_path = (data.get("path") or "").strip("/")

    # Virtual root: list the mount points themselves
    if not rel_path:
        dirs = [name for name, path in VIRTUAL_MOUNTS.items() if os.path.isdir(path)]
        return jsonify({"path": "", "dirs": dirs, "files": []})

    try:
        abs_path, _ = _resolve(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.isdir(abs_path):
        return jsonify({"error": "not a directory"}), 400

    dirs, files = [], []
    for name in sorted(os.listdir(abs_path)):
        full = os.path.join(abs_path, name)
        if os.path.isdir(full):
            dirs.append(name)
        elif os.path.isfile(full):
            files.append(name)

    return jsonify({"path": rel_path, "dirs": dirs, "files": files})


@core_bp.route("/pi/dir/mkdir", methods=["POST"])
def pi_files_mkdir():
    data     = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")
    name     = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "missing name"}), 400
    if not rel_path:
        return jsonify({"error": "cannot create folder at root"}), 400

    try:
        mount, sub = _split_virtual(rel_path)
        real_root  = os.path.realpath(VIRTUAL_MOUNTS[mount])
        new_sub    = f"{sub}/{name}" if sub else name
        target     = safe_join_under_root(real_root, new_sub)
        os.makedirs(target, exist_ok=True)
        return jsonify({"ok": True})
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    except OSError as e:
        return jsonify({"error": str(e)}), 500


@core_bp.route("/pi/file/preview", methods=["GET"])
def pi_files_preview():
    rel_path = (request.args.get("path") or "").strip("/")

    try:
        abs_path, _ = _resolve(rel_path)
    except ValueError:
        return "invalid path", 400

    if not os.path.isfile(abs_path):
        return "not found", 404

    mime, _ = mimetypes.guess_type(abs_path)
    return send_file(abs_path, mimetype=mime or "application/octet-stream")


@core_bp.route("/pi/file/display", methods=["POST"])
def pi_files_use():
    data     = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")

    if not rel_path:
        return jsonify({"error": "missing path"}), 400

    try:
        abs_path, _ = _resolve(rel_path)
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

    # Default to "uploads" mount when at the virtual root
    if not rel_path:
        rel_path = "uploads"

    try:
        target_dir, _ = _resolve(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    try:
        os.makedirs(target_dir, exist_ok=True)
        f.save(os.path.join(target_dir, filename))
    except OSError as e:
        return jsonify({"error": str(e)}), 500

    rel_saved = f"{rel_path}/{filename}"
    return jsonify({"ok": True, "path": rel_saved})


@core_bp.route("/pi/path/delete", methods=["POST"])
def pi_path_delete():
    data     = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")

    if not rel_path:
        return jsonify({"error": "missing path"}), 400

    # Prevent deleting a mount root
    if rel_path in VIRTUAL_MOUNTS:
        return jsonify({"error": "cannot delete a root folder"}), 400

    try:
        abs_path, _ = _resolve(rel_path)
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
    data     = request.get_json() or {}
    rel_path = (data.get("path") or "").strip("/")
    new_name = (data.get("new_name") or "").strip().strip("/")

    if not rel_path or not new_name:
        return jsonify({"error": "missing path or new_name"}), 400
    if rel_path in VIRTUAL_MOUNTS:
        return jsonify({"error": "cannot rename a root folder"}), 400

    try:
        src_abs, real_root = _resolve(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400

    if not os.path.exists(src_abs):
        return jsonify({"error": "not found"}), 404

    mount, sub   = _split_virtual(rel_path)
    parent_sub   = os.path.dirname(sub)
    new_sub      = f"{parent_sub}/{new_name}" if parent_sub else new_name

    try:
        dst_abs = safe_join_under_root(real_root, new_sub)
    except ValueError:
        return jsonify({"error": "invalid target"}), 400

    if os.path.exists(dst_abs):
        return jsonify({"error": "target exists"}), 400

    os.rename(src_abs, dst_abs)
    dst_rel = f"{mount}/{new_sub}"
    return jsonify({"ok": True, "path": dst_rel})


@core_bp.route("/pi/path/move", methods=["POST"])
def pi_path_move():
    data    = request.get_json() or {}
    src     = (data.get("src")     or "").strip("/")
    dst_dir = (data.get("dst_dir") or "").strip("/")

    if not src:
        return jsonify({"error": "missing src"}), 400
    if src in VIRTUAL_MOUNTS:
        return jsonify({"error": "cannot move a root folder"}), 400

    try:
        src_abs, _ = _resolve(src)
    except ValueError:
        return jsonify({"error": "invalid src"}), 400

    # dst_dir can be a mount root or a subfolder within a mount
    if not dst_dir:
        return jsonify({"error": "missing dst_dir"}), 400

    try:
        dst_dir_abs, _ = _resolve(dst_dir)
    except ValueError:
        return jsonify({"error": "invalid dst_dir"}), 400

    if not os.path.exists(src_abs):
        return jsonify({"error": "src not found"}), 404
    if not os.path.isdir(dst_dir_abs):
        return jsonify({"error": "dst_dir is not a directory"}), 400

    name    = os.path.basename(src_abs)
    dst_abs = os.path.join(dst_dir_abs, name)
    if os.path.exists(dst_abs):
        return jsonify({"error": "target exists"}), 400

    shutil.move(src_abs, dst_abs)
    dst_rel = f"{dst_dir}/{name}"
    return jsonify({"ok": True, "path": dst_rel})
