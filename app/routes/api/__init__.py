from flask import Blueprint
from werkzeug.exceptions import HTTPException
import logging
from app.utils.api import error_response
from .tests import tests_bp

# Main API blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


# Global error handler for all API routes
@api_bp.errorhandler(Exception)
def api_error_handler(error):
    if isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        logging.error(error)
        return error_response()


# Register submodules under /api
api_bp.register_blueprint(tests_bp)