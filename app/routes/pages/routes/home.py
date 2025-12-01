from flask import render_template
from ..blueprint import core_bp 

@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")
