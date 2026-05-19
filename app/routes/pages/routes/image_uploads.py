import io
import os
import tempfile
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

from ..blueprint import core_bp
from ..utils.config import UPLOAD_FOLDER, MATRIX_SIZE
from ..utils.utils import allowed_file, show_file, composite_on_black, draw_to_screen, stop_animation


def _get_upload_file():
    """Validate and return the uploaded file, or return an error response tuple."""
    if "file" not in request.files:
        return None, (jsonify({"error": "No file"}), 400)
    file = request.files["file"]
    if not file.filename or not allowed_file(file.filename):
        return None, (jsonify({"error": "Invalid file"}), 400)
    return file, None


def _show_image_from_bytes(data: bytes) -> None:
    """Display a non-GIF image on the matrix directly from bytes."""
    stop_animation()
    img = composite_on_black(Image.open(io.BytesIO(data)))
    draw_to_screen(img, MATRIX_SIZE, MATRIX_SIZE)


@core_bp.route("/image", methods=["GET", "POST"])
def image_route():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "warning")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            return redirect(url_for("pages.core.display_uploaded_file", name=filename))

    return render_template("pages/image.html")


@core_bp.route("/uploads/<name>")
def display_uploaded_file(name):
    full_path = os.path.join(UPLOAD_FOLDER, name)
    show_file(full_path)
    return send_from_directory(UPLOAD_FOLDER, name)


@core_bp.route("/upload_only", methods=["POST"])
def upload_only():
    """Save an uploaded image to the Pi without showing it on the matrix."""
    file, err = _get_upload_file()
    if err:
        return err

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"ok": True})


@core_bp.route("/show_direct", methods=["POST"])
def show_direct():
    """Save an uploaded image to the Pi and show it on the matrix."""
    file, err = _get_upload_file()
    if err:
        return err

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    data = file.read()
    with open(save_path, "wb") as f:
        f.write(data)

    if ext == "gif":
        show_file(save_path)
    else:
        _show_image_from_bytes(data)

    return jsonify({"ok": True})


@core_bp.route("/show_only", methods=["POST"])
def show_only():
    """Show an uploaded image on the matrix without saving it to disk."""
    file, err = _get_upload_file()
    if err:
        return err

    ext = file.filename.rsplit(".", 1)[1].lower()
    data = file.read()

    if ext == "gif":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        show_file(tmp_path)
    else:
        _show_image_from_bytes(data)

    return jsonify({"ok": True})
