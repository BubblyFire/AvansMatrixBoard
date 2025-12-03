import os
from PIL import Image
from app.extensions import matrixpi
from .config import ALLOWED_EXTENSIONS

def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def show_file(path: str) -> None:
    img = Image.open(path)
    img.thumbnail((30, 30), Image.LANCZOS)
    matrixpi.matrixboard.clear()
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            pixel = img.getpixel((x, y))
            matrixpi.matrixboard._draw_pixel(x, y, pixel[:3])
    print(path)
    matrixpi.matrixboard.show()


def safe_join_under_root(root: str, *paths: str) -> str:
    # Filter lege stukken, strip slashes
    clean_parts = [p.strip("/").strip("\\") for p in paths if p]
    joined = os.path.join(root, *clean_parts)

    # Canonicaliseer pad
    real_root = os.path.realpath(root)
    real_path = os.path.realpath(joined)

    if not real_path.startswith(real_root):
        raise ValueError("Path escapes restricted root")

    return real_path
