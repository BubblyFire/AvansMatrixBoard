import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

from matrixboard import MatrixBoard

BOARD_WIDTH = 30
BOARD_HEIGHT = 30

# Setup Matrixboard
matrixboard = MatrixBoard(BOARD_WIDTH, BOARD_HEIGHT)
matrixboard.init()

# Setup Flask
UPLOAD_FOLDER = '/opt/matrixpi'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    img = Image.open(app.config["UPLOAD_FOLDER"] + "/" + name)
    img.thumbnail((30, 30), Image.LANCZOS)
    matrixboard.clear()
    for y in range(0,img.size[1]):
        for x in range(0,img.size[0]):
            pixel = img.getpixel( (x,y) )
            matrixboard._draw_pixel(x, y, pixel[:3])
    print(app.config["UPLOAD_FOLDER"])
    matrixboard.show()
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/text/<name>")
def send_text(name):
    matrixboard.clear()
    matrixboard.render_text(0, 0, name, (255, 0, 0))
    matrixboard.render_text(0, 1, name, (255, 0, 0))
    matrixboard.render_text(0, 2, name, (255, 0, 0))
    matrixboard.show()
    return "Hello World!"

@app.route("/text/weather")
def display_weather():
    matrixboard.clear()
    matrixboard.render_text(0, 0, "Weather", (255, 0, 0))
    matrixboard.render_text(0, 1, "3 C", (255, 0, 0))
    matrixboard.render_text(0, 2, " Rain", (255, 0, 0))
    matrixboard.show()
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
