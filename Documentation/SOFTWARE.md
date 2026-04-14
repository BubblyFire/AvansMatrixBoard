# Software

## Stack

| Component | Technology |
|-----------|-----------|
| Web framework | Flask 3.0.3 |
| Database ORM | Flask-SQLAlchemy |
| Cross-origin requests | Flask-CORS |
| Image processing | Pillow |
| LED driver | rpi_ws281x, Adafruit NeoPixel, Adafruit Blinka |
| Frontend | Bootstrap 4.5.2, jQuery 3.7.1 |

## Project Structure

```
server.py                  # Entry point
app/
  __init__.py              # Application factory (create_app)
  i18n.py                  # UI translations (English / Dutch)
  config/
    dev.py                 # Development config
    prod.py                # Production config
    config.json            # Runtime hardware settings (auto-generated)
  extensions/
    matrixpi.py            # Flask extension wrapping MatrixBoard
    matrixboard.py         # NeoPixel LED matrix controller
    bitmapfont.py          # Bitmap font renderer (font5x8.bin)
    config.py              # Load/save config.json
    db.py                  # SQLAlchemy instance
    cors.py                # Flask-CORS instance
  routes/
    api/
      __init__.py          # api_bp blueprint (/api)
      tests.py             # Test endpoints (/api/tests/*)
    pages/
      __init__.py          # pages_bp blueprint (/)
      blueprint.py         # core_bp blueprint
      routes/
        home.py            # GET /
        text.py            # GET /text, POST /text2
        draw.py            # GET /draw, POST /sendtoboard
        image_uploads.py   # GET/POST /image, GET /uploads/<name>
        imagepicker.py     # GET /imagepicker, POST /imagelist, POST /imagelist_show
        pi_files.py        # POST /pi/files and related file browser routes
        config.py          # GET /config, POST /config/save
        slideshow.py       # GET /slideshow, POST /slideshow/start|stop, GET /slideshow/status
        status.py          # GET /status ("now playing" badge)
        clear.py           # POST /clear (navbar Clear button)
        preview.py         # GET /preview, GET /preview/state (live matrix preview)
        portal.py          # Captive-portal redirects (/hotspot-detect.html, /generate_204, /ncsi.txt)
      utils/
        config.py          # Upload folder constants and virtual mount points
        utils.py           # Image rendering, GIF playback, slideshow, path safety
        state.py           # "Now playing" and slideshow shared state
  utils/
    api.py                 # JSON response helpers
    models.py              # Shared model utilities
templates/
  base.html                # Shared layout, navbar, toast system
  pages/
    home.html
    text.html
    draw.html
    image.html
    imagepicker.html
    slideshow.html
    preview.html
    config.html
static/
  css/
    main.css               # Global styles
    imagepicker.css        # Image picker styles
  js/
    main.js                # Draw page logic (grid, touch, save)
    server.js              # Pi file browser logic
    imagepicker.js         # Image picker logic
    slideshow.js           # Slideshow page logic
    preview.js             # Live matrix preview (polls /preview/state)
    api.js                 # Shared fetch wrapper
    ui.js                  # DOM helpers for image page
    menu.js                # Context menu
    actions.js             # File actions (rename, delete, move)
    functions.js           # Path utilities
    modal.js               # Modal dialog helpers
  assets/                  # Predefined images (traffic signs, emoticons)
font5x8.bin                # Binary font file for matrix text rendering
```

## Key Design Decisions

- **Application Factory pattern** — `create_app()` in `app/__init__.py` initializes everything. This makes the app configurable and testable.
- **Serpentine LED wiring** — The 30×30 matrix is wired so even rows go left-to-right and odd rows go right-to-left. `_coord_to_index()` in `matrixboard.py` handles this.
- **`DISABLE_MATRIX=1`** — Allows running the app without connected hardware. `MatrixBoard` is still created and tracks pixels in a shadow buffer; hardware calls (`NeoPixel.show()` etc.) are skipped. Routes behave the same and the `/preview` page stays fully functional.
- **i18n via dictionary** — UI translations live in `app/i18n.py`. No external library or compilation step required. Add a language by adding a new key to `TRANSLATIONS`.
- **GIF playback** — Runs in a daemon thread. Controlled via a `threading.Event` so it stops cleanly when a new image is requested.
- **Path safety** — All user-supplied file paths go through `safe_join_under_root()` to prevent directory traversal attacks.
