import os
import json

from flask import render_template, request

from ..blueprint import core_bp
from ..utils.config import IMAGEPICKER_ROOT_FOLDER, IMAGEPICKER_ROOT_URL
from ..utils.utils import show_file


def collect_image_entries(parent, entries):
    """Recursively collect image files and subdirectories into a flat list."""
    for file in os.listdir(parent):
        path = os.path.join(parent, file)
        if os.path.islink(path):
            continue
        elif os.path.isdir(path):
            entries.append({"isdir": True, "parent": parent, "url": path, "name": file})
            collect_image_entries(path, entries)
        elif os.path.isfile(path) and file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            entries.append({"parent": parent, "url": path, "name": file})

    # Mark the last entry added so far as the last item in this directory.
    # The frontend uses this flag to decide where to draw visual separators.
    if len(entries) >= 1:
        entries[-1]["last_in_dir"] = True


@core_bp.route("/imagelist", methods=["POST"])
def imagelist_route():
    """
    Return the contents of an asset subfolder as JSON.

    Expects JSON: {"path": "emoticons"}
    Reads the folder's info.json (if present) and resolves icon/image URLs
    so the frontend can render thumbnails without knowing server paths.
    Returns: {"dirs": [...], "imgs": [...]}
    """
    if not request.is_json:
        return {}, 400

    path = request.get_json()["path"]
    info_path = os.path.join(IMAGEPICKER_ROOT_FOLDER, path, "info.json")
    data = {"dirs": [], "imgs": []}

    if os.path.isfile(info_path):
        with open(info_path) as f:
            data = json.load(f)
            # Resolve relative icon/image paths to full URL paths served by Flask
            for d in data["dirs"]:
                d["ico"] = os.path.join(IMAGEPICKER_ROOT_URL, path, d["ico"])
                d["src"] = os.path.join(path, d["src"])
            for d in data["imgs"]:
                d["src"] = os.path.join(IMAGEPICKER_ROOT_URL, path, d["src"])

    return data


@core_bp.route("/imagelist_show", methods=["POST"])
def imagelist_show():
    """Display a selected asset image on the matrix. Expects JSON: {"path": "assets/..."}."""
    if not request.is_json:
        return "400", 400

    path = request.get_json()["path"]
    show_file(os.path.join("./static", path))
    return "200"

@core_bp.route("/imagepicker")
def imagepicker_route():
    """Render the image-picker browser page."""
    return render_template("pages/imagepicker.html")
