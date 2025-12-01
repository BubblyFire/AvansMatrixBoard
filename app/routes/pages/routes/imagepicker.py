# app/core/imagepicker.py
import os
import json
from pprint import pprint

from flask import render_template, request

from ..blueprint import core_bp 
from ..utils.config import IMAGEPICKER_ROOT_FOLDER, IMAGEPICKER_ROOT_URL
from ..utils.utils import show_file

# iterates through directories and files
# generates linear list of files and directories
def dir_iter(parent, img_struct):
    print(img_struct)
    fle_list = os.listdir(parent)
    print(fle_list)
    for fle in fle_list:
        pth = os.path.join(parent, fle)
        if os.path.islink(pth):
            continue
        elif os.path.isdir(pth):
            img_struct.append(
                {"isdir": True, "parent": parent, "url": pth, "name": fle}
            )
            dir_iter(pth, img_struct)
        elif os.path.isfile(pth) and fle.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        ):
            img_struct.append({"parent": parent, "url": pth, "name": fle})
        # else: 
            # ignore the rest
    if len(img_struct) >= 1:
        img_struct[len(img_struct) - 1]["last_in_dir"] = True

@core_bp.route("/imagelist", methods=["POST"])
def imagelist_route():
    pprint(vars(request))
    if request.method == "POST" and request.is_json:
        pth = request.get_json()["path"]
        inf = IMAGEPICKER_ROOT_FOLDER + pth + "/" + "info.json"  # proj dir
        print(inf)
        dat = {"dirs": [], "imgs": []}
        if os.path.isfile(inf):
            with open(inf) as f_in:
                dat = json.load(f_in)
                for d in dat["dirs"]:
                    d["ico"] = IMAGEPICKER_ROOT_URL + pth + "/" + d["ico"]  # url dir
                    d["src"] = pth + "/" + d["src"]  # url dir
                for d in dat["imgs"]:
                    d["src"] = IMAGEPICKER_ROOT_URL + pth + "/" + d["src"]  # url image
        print(dat)
        return dat
    return {}, 400

@core_bp.route("/imagelist_show", methods=["POST"])
def imagelist_show():
    pprint(vars(request))
    if request.method == "POST" and request.is_json:
        pth = request.get_json()["path"]
        inf = "./static/" + pth  # proj dir
        print(inf)
        show_file(inf)
    return "200"

@core_bp.route("/imagepicker")
def imagepicker_route():
    # img_struct = []
    # dir_iter(ROOT_FOLDER, img_struct)
    # print(img_struct)
    return render_template("pages/imagepicker.html")
