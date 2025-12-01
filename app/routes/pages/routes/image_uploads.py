import os
from flask import render_template, request, flash, redirect,url_for, send_from_directory
from werkzeug.utils import secure_filename

from ..blueprint import core_bp 
from ..utils.config import UPLOAD_FOLDER
from ..utils.utils import allowed_file, show_file

@core_bp.route("/image", methods=["GET", "POST"])
def image_route():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            return redirect(url_for("core.download_file", name=filename))

    return render_template("pages/image.html")

@core_bp.route("/uploads/<name>")
def download_file(name):
    full_path = os.path.join(UPLOAD_FOLDER, name)
    show_file(full_path)
    return send_from_directory(UPLOAD_FOLDER, name)
