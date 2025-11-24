from flask import Blueprint, request
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException

import logging

from app.utils.api import error_response

from .tests import tests_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        logging.error(error)
        return error_response()


api_bp.register_blueprint(tests_bp)
