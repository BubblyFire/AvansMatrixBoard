import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp"}
MATRIX_SIZE = 30

# Absolute project root, regardless of where the server is started from
_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

IMAGEPICKER_ROOT_FOLDER = os.path.join(_PROJECT_ROOT, "static", "assets")
IMAGEPICKER_ROOT_URL    = "assets/"

UPLOAD_FOLDER     = os.environ.get("UPLOAD_FOLDER",      os.path.join(_PROJECT_ROOT, "uploads"))
FILE_BROWSER_ROOT = os.environ.get("FILE_BROWSER_ROOT",  os.path.join(_PROJECT_ROOT, "user_uploads"))
DRAWINGS_FOLDER   = os.environ.get("DRAWINGS_FOLDER",    os.path.join(_PROJECT_ROOT, "drawings"))

# Virtual mount points shared by the file browser and slideshow
VIRTUAL_MOUNTS = {
    "uploads":      UPLOAD_FOLDER,
    "user_uploads": FILE_BROWSER_ROOT,
    "drawings":     DRAWINGS_FOLDER,
}

# Ensure directories exist at startup
os.makedirs(UPLOAD_FOLDER,     exist_ok=True)
os.makedirs(FILE_BROWSER_ROOT, exist_ok=True)
os.makedirs(DRAWINGS_FOLDER,   exist_ok=True)
