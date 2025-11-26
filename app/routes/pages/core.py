import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from app.extensions import matrixpi
from werkzeug.utils import secure_filename
from PIL import Image

core_bp = Blueprint("core", __name__, url_prefix="/")

UPLOAD_FOLDER = '/opt/matrixpi'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")

@core_bp.route("/draw")
def draw_route():
    return render_template("pages/draw.html")

@core_bp.route('/sendtoboard', methods=['POST'])
def callback_route():
    data = request.get_json()
    data = data['value']

    matrixpi.matrixboard.clear()
    for i in range(len(data)):
        y = i // 30
        x = i % 30
        color_string = data[i]
        color_values = color_string[color_string.find("(")+1:color_string.find(")")]
        color_values = color_values.replace(" ", "")
        color_values_list = color_values.split(",")
        if len(color_values_list) == 3:
            cl = (int(color_values_list[0]), int(color_values_list[1]), int(color_values_list[2]))
            matrixpi.matrixboard._draw_pixel(x, y, cl)
        else:
            matrixpi.matrixboard._draw_pixel(x, y, (0, 0, 0))

    matrixpi.matrixboard.show()
    return ""

@core_bp.route("/text")
def text_route():
    return render_template("pages/text.html")

@core_bp.route("/text2", methods=['POST'])
def text_route_post():
    json_request = request.get_json()
    text, hex_color, line = json_request['text'], json_request['color'], json_request['line']
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    matrixpi.matrixboard.clear_line(line)
    matrixpi.matrixboard.render_text(0, line, text, rgb_color)
    matrixpi.matrixboard.show()
    return ""

@core_bp.route("/image", methods=['GET', 'POST'])
def image_route():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('pages.core.download_file', name=filename))
    return render_template("pages/image.html")


@core_bp.route('/uploads/<name>')
def download_file(name):
    img = Image.open(UPLOAD_FOLDER + "/" + name)
    img.thumbnail((30, 30), Image.LANCZOS)
    matrixpi.matrixboard.clear()
    for y in range(0,img.size[1]):
        for x in range(0,img.size[0]):
            pixel = img.getpixel( (x,y) )
            matrixpi.matrixboard._draw_pixel(x, y, pixel[:3])
    print(UPLOAD_FOLDER)
    matrixpi.matrixboard.show()
    return send_from_directory(UPLOAD_FOLDER, name)
