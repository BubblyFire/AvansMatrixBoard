import os
import threading
import time
from PIL import Image, ImageSequence, ImageEnhance, ImageChops, ImageOps
from app.extensions import matrixpi
from .config import ALLOWED_EXTENSIONS
from app.extensions.config import load_matrix_config

_gif_thread = None
_gif_stop = threading.Event()
_gif_lock = threading.Lock()

def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

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

def draw_to_screen(
    img: Image.Image,
    width: int,
    height: int,
    black_level: int = 6,
    black_threshold: int = 28,
    contrast: float = 1.20,
    saturation: float = 1.20,
    gamma: float = 0.70,
    posterize_bits: int = 5,
    auto_crop: bool = True
):
    img = img.resize((width,height))

    if auto_crop:
        bg = Image.new("RGB", img.size, img.getpixel((0, 0)))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if bbox:
            img = img.crop(bbox)

    if contrast and contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)

    if saturation and saturation != 1.0:
        img = ImageEnhance.Color(img).enhance(saturation)

    if gamma and gamma != 1.0:
        inv = 1.0 / gamma
        lut = [int(pow(i / 255.0, inv) * 255) for i in range(256)]
        img = img.point(lut * 3)

    if posterize_bits and posterize_bits < 8:
        img = ImageOps.posterize(img, posterize_bits)

    matrixpi.matrixboard.clear()
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            r, g, b = img.getpixel((x, y))
            brightness = r + g + b

            if brightness <= black_threshold:
                r = g = b = black_level

            matrixpi.matrixboard._draw_pixel(x, y, (r, g, b))

    matrixpi.matrixboard.show()

def show_file(path: str, width: int = 30, height: int = 30) -> None:
    stop_animation()
    ext = os.path.splitext(path)[1].lower()

    if ext == '.gif':
        global _gif_thread
        with _gif_lock:
            _gif_thread = threading.Thread(
                target=play_gif_loop,
                args=(path, width, height),
                daemon=True
            )
            _gif_thread.start()

    img = Image.open(path).convert("RGB")
    draw_to_screen(img, width, height)

def stop_animation() -> None:
    global _gif_thread

    with _gif_lock:
        _gif_stop.set()
        thread = _gif_thread

    if thread and thread.is_alive():
        thread.join(timeout=1.0)

    with _gif_lock:
        _gif_thread = None
        _gif_stop.clear()

def play_gif_loop(path: str, width: int, height: int):
    img = Image.open(path)

    while not _gif_stop.is_set():
        for frame in ImageSequence.Iterator(img):
            if _gif_stop.is_set():
                break

            rgb = frame.convert("RGB")
            draw_to_screen(rgb, width, height)

            cfg = load_matrix_config()
            speed = cfg.get("gif_delay", 1.0)

            delay_ms = frame.info.get("duration", 100)
            delay = (delay_ms / 1000.0) * speed
            
            time.sleep(max(0.02, delay))

def clear_matrix():
    stop_animation()
    matrixpi.matrixboard.clear()
    matrixpi.matrixboard.show()
