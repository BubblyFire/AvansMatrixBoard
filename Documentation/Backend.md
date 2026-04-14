# Backend Architecture

> **New to Flask?** A few terms used on this page:
> - **Route** — a URL + a Python function that runs when someone visits it.
> - **Blueprint** — a group of routes. This project has two: `api_bp` (`/api/*`) and `pages_bp` (the rest).
> - **Application factory** — the `create_app()` function that builds the Flask app. This pattern makes the app easier to configure and test.
> - **Extension** — a reusable piece of functionality (e.g. database, CORS, matrix controller).
> - **Context processor** — code that injects variables into every template automatically. We use one for translations.
>
> For more terms, see the glossary in [HowTo.md](HowTo.md#glossary).

## Entry Point

`server.py` creates the Flask app by calling `create_app(debug=True)` and starts the server on `0.0.0.0:80`.

## Application Factory

**File:** `app/__init__.py`
**Function:** `create_app(debug: bool = False)`

Responsibilities:
- Creates the Flask application instance
- Loads the correct config (dev or prod)
- Initializes extensions (db, cors, matrixpi)
- Registers blueprints
- Registers the i18n context processor and `/set-language/<lang>` route

## Configuration

| File | Used when | Key settings |
|------|-----------|-------------|
| `app/config/dev.py` | `debug=True` or `FLASK_DEBUG` env var | DEBUG=True, auto-reload, reads `.env.dev` |
| `app/config/prod.py` | default | DEBUG=False, reads `.env` |

Both configs use SQLite at `instance/database.db`.

> For every config key (matrix runtime, Flask, environment variables) see **[Config.md](Config.md)**.

## Extensions (`app/extensions/`)

| File | Purpose |
|------|---------|
| `db.py` | SQLAlchemy instance |
| `cors.py` | Flask-CORS, allows all origins on `/api/*` |
| `matrixpi.py` | Wraps `MatrixBoard`, initializes hardware on startup |
| `matrixboard.py` | Controls the NeoPixel LED matrix |
| `bitmapfont.py` | Renders text using `font5x8.bin` |
| `config.py` | Loads/saves hardware settings from `app/config/config.json` |

### Running Without Hardware

`MatrixpiExtension` checks the `DISABLE_MATRIX` environment variable on startup:

```bash
DISABLE_MATRIX=1 python server.py
```

When set, a `MatrixBoard` is still created but it skips the NeoPixel / `board` imports — all drawing calls update the shadow buffer only. `matrixpi.matrixboard` is never `None` (a previous version used `None` for no-hardware mode; that's gone).

### MatrixBoard

The `MatrixBoard` class (`matrixboard.py`) controls the 30×30 NeoPixel grid.

- LEDs are wired in a **serpentine pattern** — even rows go left-to-right, odd rows go right-to-left. `_coord_to_index(x, y)` handles this translation.
- Text is rendered using `BitmapFont` with the `font5x8.bin` font file (5×8 pixels per character).
- Hardware settings (pin, brightness, scroll delay, etc.) are read from `app/config/config.json` at startup.
- A **shadow buffer** (plain Python list, visual row-major order, top-left = index 0) tracks every pixel change. `get_pixels()` exposes it so the `/preview` page can render a live copy of the matrix, and so every feature keeps working with `DISABLE_MATRIX=1`.

## Routing Structure

Two top-level blueprints are registered in `create_app()`:

```
api_bp      → /api
pages_bp    → /
  └── core_bp  (all page routes)
```

### API Blueprint (`app/routes/api/`)

Handles JSON API routes. All errors are caught by a global error handler and returned as JSON.

| Blueprint | Prefix | File |
|-----------|--------|------|
| `api_bp` | `/api` | `app/routes/api/__init__.py` |
| `tests_bp` | `/api/tests` | `app/routes/api/tests.py` |

### Pages Blueprint (`app/routes/pages/`)

Serves HTML pages and handles matrix control requests.

| File | Routes |
|------|--------|
| `routes/home.py` | `GET /` |
| `routes/text.py` | `GET /text`, `POST /text2` |
| `routes/draw.py` | `GET /draw`, `POST /sendtoboard` |
| `routes/image_uploads.py` | `GET/POST /image`, `GET /uploads/<name>` |
| `routes/imagepicker.py` | `GET /imagepicker`, `POST /imagelist`, `POST /imagelist_show` |
| `routes/pi_files.py` | `POST /pi/files`, `POST /pi/dir/mkdir`, `GET /pi/file/preview`, `POST /pi/file/display`, `POST /pi/file/upload`, `POST /pi/path/delete`, `POST /pi/path/rename`, `POST /pi/path/move` |
| `routes/config.py` | `GET /config`, `POST /config/save` |
| `routes/slideshow.py` | `GET /slideshow`, `POST /slideshow/start`, `POST /slideshow/stop`, `GET /slideshow/status` |
| `routes/status.py` | `GET /status` (current "now playing" state) |
| `routes/clear.py` | `POST /clear` (stop everything and turn off all LEDs) |
| `routes/preview.py` | `GET /preview`, `GET /preview/state` (live browser preview of the matrix) |
| `routes/portal.py` | Captive-portal redirects: `GET /hotspot-detect.html`, `GET /generate_204`, `GET /ncsi.txt` |

Route modules are imported in `app/routes/pages/__init__.py` — adding a new route file means importing it there so its handlers attach to `core_bp`.

## Image Processing (`app/routes/pages/utils/utils.py`)

`show_file(path)` displays an image on the matrix:
- For **GIFs**, a daemon thread is started that loops through frames (`play_gif_loop`). A `threading.Event` is used to stop the animation when a new image is requested.
- For **static images**, `draw_to_screen()` applies contrast, saturation, gamma correction, and posterization before rendering pixels.
- **Transparency** is handled by `composite_on_black()`, which composites RGBA/palette images onto a black background before rendering.

`safe_join_under_root(root, *paths)` is used for all user-supplied file paths to prevent directory traversal attacks.

## Internationalisation (`app/i18n.py`)

All UI strings are stored as a Python dictionary in `app/i18n.py` under `TRANSLATIONS`. Supported languages are `en` and `nl`.

A `t('key')` function is injected into every template via a context processor. The current language is stored in the Flask session and can be changed via `GET /set-language/<lang>`.

To add a new language, add a new key to `TRANSLATIONS` in `app/i18n.py`.

## API Response Format

All `/api/*` routes return JSON in this format:

```json
{ "status": "success", "message": "...", "data": {} }
{ "status": "error",   "message": "..." }
```

Helper functions `success_response()` and `error_response()` in `app/utils/api.py` build these responses.
