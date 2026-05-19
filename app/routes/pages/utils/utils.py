import os
import threading
import time
from PIL import Image, ImageSequence, ImageEnhance, ImageChops, ImageOps
from app.extensions import matrixpi
from .config import ALLOWED_EXTENSIONS
from .state import set_now_playing, set_slideshow_state
from app.extensions.config import load_matrix_config

_STOP_TIMEOUT_S     = 1.0   # seconds to wait for GIF thread to stop
_GIF_DEFAULT_MS     = 100   # fallback frame duration when GIF has no duration metadata
_GIF_MIN_DELAY_S    = 0.02  # minimum frame delay to prevent runaway loops

_gif_thread = None
_gif_stop = threading.Event()
_gif_lock = threading.Lock()

_slideshow_thread = None
_slideshow_stop   = threading.Event()
_slideshow_lock   = threading.Lock()

def composite_on_black(img: Image.Image) -> Image.Image:
    """Convert an image to RGB, compositing transparency onto a black background.
    Without this, transparent pixels in PNGs would show as black artifacts."""
    if img.mode == 'P':
        img = img.convert('RGBA')
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (0, 0, 0))
        alpha = img.getchannel('A')
        background.paste(img.convert('RGB'), mask=alpha)
        return background
    return img.convert('RGB')


def allowed_file(filename: str) -> bool:
    """Return True if filename has an extension in ALLOWED_EXTENSIONS."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def safe_join_under_root(root: str, *paths: str) -> str:
    # Filter empty parts and strip leading/trailing slashes
    clean_parts = [p.strip("/").strip("\\") for p in paths if p]
    joined = os.path.join(root, *clean_parts)

    # Resolve to absolute paths to detect directory traversal attempts
    real_root = os.path.realpath(root)
    real_path = os.path.realpath(joined)

    # Use a path-segment check, not a plain prefix check: a bare startswith()
    # would wrongly accept e.g. "/data/uploads_evil" as inside "/data/uploads".
    if real_path != real_root and not real_path.startswith(real_root + os.sep):
        raise ValueError("Path escapes restricted root")

    return real_path

def draw_to_screen(img: Image.Image, width: int, height: int) -> None:
    """
    Resize img to (width, height), apply image-processing corrections from
    config, then push the result pixel-by-pixel to the physical matrix.

    Processing pipeline (each step can be tuned via /config):
      1. Resize to matrix size
      2. Auto-crop: remove solid-colour borders
      3. Contrast boost
      4. Saturation boost
      5. Gamma correction  (brightens mid-tones for better LED visibility)
      6. Posterize         (reduces colour depth to smooth out noisy images)
      7. Black-level lift  (very dark pixels become a dim grey instead of off)
    """
    cfg = load_matrix_config()
    black_level     = cfg.get("black_level",     6)
    black_threshold = cfg.get("black_threshold", 28)
    contrast        = cfg.get("contrast",        1.20)
    saturation      = cfg.get("saturation",      1.20)
    gamma           = cfg.get("gamma",           0.70)
    posterize_bits  = cfg.get("posterize_bits",  5)
    auto_crop       = cfg.get("auto_crop",       True)

    img = img.resize((width, height))

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
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            brightness = r + g + b

            if brightness <= black_threshold:
                r = g = b = black_level

            matrixpi.matrixboard._draw_pixel(x, y, (r, g, b))

    matrixpi.matrixboard.show()

def show_file(path: str, width: int = 30, height: int = 30, _from_slideshow: bool = False) -> None:
    """
    Display an image or GIF file on the matrix.

    - Static images (PNG/JPG/BMP) are drawn immediately in the calling thread.
    - GIFs are played in a background daemon thread that loops until stopped.
    - Any previously running GIF or slideshow is stopped first, unless this
      call comes from the slideshow runner itself (_from_slideshow=True).
    """
    if not _from_slideshow:
        stop_slideshow()
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
        set_now_playing("gif", os.path.basename(path))
        return

    img = composite_on_black(Image.open(path))
    draw_to_screen(img, width, height)
    set_now_playing("image", os.path.basename(path))

def stop_animation() -> None:
    """Signal the GIF thread to stop and wait up to _STOP_TIMEOUT_S for it to finish."""
    global _gif_thread

    with _gif_lock:
        _gif_stop.set()
        thread = _gif_thread

    if thread and thread.is_alive():
        thread.join(timeout=_STOP_TIMEOUT_S)

    with _gif_lock:
        _gif_thread = None
        _gif_stop.clear()

def play_gif_loop(path: str, width: int, height: int) -> None:
    """
    Background thread target: loop a GIF until _gif_stop is set.

    Each frame is drawn with draw_to_screen().  The per-frame delay comes from
    the GIF metadata (frame.info["duration"] in ms) multiplied by gif_delay
    from config, allowing playback speed to be tuned without re-uploading.
    """
    img = Image.open(path)

    while not _gif_stop.is_set():
        for frame in ImageSequence.Iterator(img):
            if _gif_stop.is_set():
                break

            rgb = composite_on_black(frame)
            draw_to_screen(rgb, width, height)

            cfg = load_matrix_config()
            speed = cfg.get("gif_delay", 1.0)

            delay_ms = frame.info.get("duration", _GIF_DEFAULT_MS)
            delay = (delay_ms / 1000.0) * speed

            time.sleep(max(_GIF_MIN_DELAY_S, delay))

def clear_matrix() -> None:
    """Stop any running slideshow/GIF, turn off all LEDs, and set state to idle."""
    stop_slideshow()
    stop_animation()
    set_now_playing("idle")
    matrixpi.matrixboard.clear()
    matrixpi.matrixboard.show()


def start_slideshow(abs_folder: str, interval: float) -> None:
    """Start a slideshow that cycles through all images in abs_folder every interval seconds."""
    _launch_slideshow(os.path.basename(abs_folder), interval, abs_folder=abs_folder)


def start_slideshow_playlist(abs_files: list, interval: float) -> None:
    """Start a slideshow using a specific ordered list of image file paths."""
    _launch_slideshow("playlist", interval, file_list=abs_files)


def _launch_slideshow(label: str, interval: float, abs_folder=None, file_list=None) -> None:
    """Internal helper: stop any existing slideshow and start a new one in a background thread."""
    global _slideshow_thread
    stop_slideshow()
    set_slideshow_state(running=True, folder=label, interval=interval, current="")
    with _slideshow_lock:
        _slideshow_stop.clear()
        _slideshow_thread = threading.Thread(
            target=_play_slideshow,
            args=(abs_folder, interval, file_list),
            daemon=True,
        )
        _slideshow_thread.start()


def stop_slideshow() -> None:
    """Signal the slideshow thread to stop and wait up to 2 s for it to finish."""
    global _slideshow_thread
    with _slideshow_lock:
        _slideshow_stop.set()
        thread = _slideshow_thread
    if thread and thread.is_alive():
        thread.join(timeout=2.0)
    with _slideshow_lock:
        _slideshow_thread = None
        _slideshow_stop.clear()
    set_slideshow_state(running=False, current="")


def _play_slideshow(abs_folder, interval: float, file_list=None) -> None:
    """
    Background thread target: display images one by one, waiting interval seconds between each.

    If abs_folder is given, the directory is rescanned each loop cycle so newly
    added files appear without restarting the slideshow.
    If file_list is given, that fixed list is used instead.
    """
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}

    while not _slideshow_stop.is_set():
        if file_list is not None:
            files = list(file_list)
        else:
            try:
                files = sorted(
                    os.path.join(abs_folder, f)
                    for f in os.listdir(abs_folder)
                    if os.path.isfile(os.path.join(abs_folder, f))
                    and os.path.splitext(f)[1].lower() in extensions
                )
            except OSError:
                break

        if not files:
            break

        for path in files:
            if _slideshow_stop.is_set():
                return
            name = os.path.basename(path)
            set_slideshow_state(current=name)
            set_now_playing("slideshow", name)
            show_file(path, _from_slideshow=True)

            deadline = time.time() + interval
            while time.time() < deadline:
                if _slideshow_stop.is_set():
                    return
                time.sleep(0.1)

    set_slideshow_state(running=False, current="")
    set_now_playing("idle")
