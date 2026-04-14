from flask import Blueprint

from .blueprint import core_bp 
from .routes import home, draw, text, image_uploads, imagepicker, pi_files, status, slideshow, portal, clear, preview

# This is the parent blueprint under which all pages live
pages_bp = Blueprint("pages", __name__, url_prefix="/")

# Mount the core blueprint under the pages blueprint
pages_bp.register_blueprint(core_bp)
