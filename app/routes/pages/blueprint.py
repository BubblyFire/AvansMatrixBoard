from flask import Blueprint

# This is the blueprint all page routes attach to
core_bp = Blueprint("core", __name__)

__all__ = ["core_bp"]
