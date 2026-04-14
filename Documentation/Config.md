# Configuration Reference

This project has **three** layers of configuration. Knowing which layer does what saves a lot of time.

| Layer | Where | What it controls | Who edits it |
|---|---|---|---|
| 1. Matrix runtime config | `app/config/config.json` | Hardware and image rendering settings that change often | The `/config` page (most keys) or you, by hand |
| 2. Flask app config | `app/config/dev.py`, `app/config/prod.py` | Flask behaviour (debug, secret key, DB URI) | Developer, in code |
| 3. Environment variables | OS env, `.env`, `.env.dev`, Dockerfile | Where files live and whether hardware is enabled | Developer or sysadmin |

---

## Layer 1 — `app/config/config.json`

Runtime settings for the LED matrix. Loaded on demand by `load_matrix_config()` in `app/extensions/config.py`. Missing keys fall back to defaults from `DEFAULT_MATRIX_CONFIG` in that same file. Saving via the `/config` page (or `save_matrix_config()`) triggers `matrixpi.reload()` so changes take effect without a restart.

### Hardware

| Key | Type | Default | Range / Valid values | Purpose |
|---|---|---|---|---|
| `pin` | string | `"D18"` | A `board` module pin name (`D10`, `D12`, `D18`, `D21`) | NeoPixel data pin. Changing this requires the Pi to be rewired. |
| `brightness` | float | `0.3` | `0.0` – `1.0` | Global LED brightness. Higher = brighter but more current/heat. |
| `auto_write` | bool | `false` | — | If `true`, the LED strip updates immediately on every pixel change (slower but simpler). If `false`, the code calls `show()` explicitly after drawing a full frame. Leave `false` for normal use. |

### Text scrolling

| Key | Type | Default | Range | Purpose |
|---|---|---|---|---|
| `scroll_delay` | float | `0.1` | `≥ 0.0` (seconds) | Delay between scroll frames. Lower = faster scrolling. |
| `font_baseline_offset` | int | `3` | any int | Vertical pixel offset when rendering text. Increase to push text down, decrease to push it up. |

### GIF playback

| Key | Type | Default | Range | Purpose |
|---|---|---|---|---|
| `gif_delay` | float | `1.0` | `≥ 0.1` | Multiplier applied to each GIF frame's own `duration`. `1.0` = original speed, `0.5` = 2× faster, `2.0` = half speed. |

### Image processing

Applied by `draw_to_screen()` in `app/routes/pages/utils/utils.py` before pushing pixels to the matrix. Tuning these dramatically changes how uploaded images look on a 30×30 grid.

| Key | Type | Default | Range | Purpose |
|---|---|---|---|---|
| `contrast` | float | `1.2` | `≥ 0.0` (`1.0` = no change) | Pillow `ImageEnhance.Contrast` factor. |
| `saturation` | float | `1.2` | `≥ 0.0` (`1.0` = no change) | Pillow `ImageEnhance.Color` factor. |
| `gamma` | float | `0.7` | `> 0.0` (`1.0` = no change, `< 1` brightens midtones) | Gamma correction applied per channel. |
| `posterize_bits` | int | `5` | `1` – `8` | Bits kept per color channel. Lower = fewer colors, more banding. `8` disables posterization. |
| `black_level` | int | `6` | `0` – `255` | RGB value written when a pixel is clamped to "near-black" (keeps the LED slightly on for visibility). |
| `black_threshold` | int | `28` | `0` – `765` | Sum-of-channels below which a pixel is treated as black and snapped to `black_level`. Prevents dim pixels from looking noisy. |
| `auto_crop` | bool | `true` | — | If `true`, transparent/black borders are cropped before resizing to 30×30. |

### Captive portal

| Key | Type | Default | Purpose |
|---|---|---|---|
| `portal_redirect` | string | *(none)* | URL that the captive-portal routes redirect to when a device joins the Wi-Fi. Usually set to the Pi's IP on the SoftAP, e.g. `http://192.168.50.5/`. Only used by `app/routes/pages/routes/portal.py`. |


### Editing config.json

**Option A — the web UI (recommended).** Go to `/config` in the browser. Every key above except `portal_redirect` has a form field. Hitting **Save** calls `POST /config/save`, which validates and clamps each value.

**Option B — edit the file directly.** Stop the server, edit `app/config/config.json`, restart. Use this for keys not exposed on the page (currently just `portal_redirect`).

---

## Layer 2 — Flask config (`app/config/dev.py`, `prod.py`)

Selected in `create_app()` based on the `debug` argument or the `FLASK_DEBUG` env var.

| Setting | Dev | Prod | Notes |
|---|---|---|---|
| `DEBUG` | `True` | `False` | Shows stack traces in the browser, enables auto-reload. |
| `TESTING` | `True` | `False` | Flask test-mode flag. |
| `TEMPLATES_AUTO_RELOAD` | `True` | `False` | Re-render templates on change without restart. |
| `STATIC_AUTO_RELOAD` | `True` | `False` | Re-serve static files on change. |
| `SECRET_KEY` | from `SECRET_KEY` env var | same | Used to sign session cookies (e.g. language choice). **Set this to something secret in production.** |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///database.db` | same | SQLite file, resolved relative to the `instance/` folder. |

Each config class loads a dotenv file first:

- Dev → `.env.dev`
- Prod → `.env`

These files are not checked in; create them next to `server.py` if you need project-local env vars.

---

## Layer 3 — Environment variables

Read directly by `os.environ.get(...)` in various places. Use these to change behaviour without touching code.

| Variable | Default | Read by | Purpose |
|---|---|---|---|
| `FLASK_DEBUG` | unset | `app/__init__.py` | If truthy, forces dev config even when `create_app(debug=False)`. |
| `SECRET_KEY` | `"YOUR-FALLBACK-SECRET-KEY"` | `app/config/dev.py`, `prod.py` | Flask session signing key. **Must be set for production.** |
| `DISABLE_MATRIX` | unset | `app/extensions/matrixpi.py` | If set (to anything truthy), `matrixpi.matrixboard` is `None` and hardware calls are skipped. Required to run on a laptop without LEDs. |
| `UPLOAD_FOLDER` | `<repo>/uploads` | `app/routes/pages/utils/config.py` | Where `/image` uploads are stored. |
| `FILE_BROWSER_ROOT` | `<repo>/user_uploads` | same | Root folder the `/pi/*` file browser exposes. |
| `DRAWINGS_FOLDER` | `<repo>/drawings` | same | Where drawings saved from the `/draw` page go. |

The Dockerfile sets `FLASK_DEBUG=1`, `DISABLE_MATRIX=1`, `UPLOAD_FOLDER=/opt/matrixpi`, and `FILE_BROWSER_ROOT=/home/avans/user_uploads` — that's why the container runs fine without hardware.

### Virtual mounts

`app/routes/pages/utils/config.py` also exposes a `VIRTUAL_MOUNTS` dict that maps short names to the folders above:

```python
VIRTUAL_MOUNTS = {
    "uploads":      UPLOAD_FOLDER,
    "user_uploads": FILE_BROWSER_ROOT,
    "drawings":     DRAWINGS_FOLDER,
}
```

The slideshow endpoints accept paths like `uploads/myfolder/pic.png` and resolve the leading segment through this map. If you add a new shared folder, add it here so the slideshow (and any future feature) can use it.

---

## Common tasks

**The matrix is too bright / too dim.** Open `/config`, change `brightness` (0.0 – 1.0), save.

**Images look washed out or too dark.** Tune `contrast`, `saturation`, `gamma`, `posterize_bits` on `/config` and preview with an image you know well.

**Text scrolls too fast / slow.** Adjust `scroll_delay` (seconds per frame).

**Changed the GPIO pin and nothing works.** `pin` must be a name from `board` (CircuitPython), not a raw BCM number. Use `"D18"`, `"D21"`, etc. A restart is safest after changing this.

**Captive portal redirects to the wrong address.** Edit `portal_redirect` in `app/config/config.json` by hand and restart. Don't save via `/config` afterwards or the key will be removed (see the quirk above).

**Running in Docker but uploads go to the wrong place.** Set `UPLOAD_FOLDER` and `FILE_BROWSER_ROOT` in the Dockerfile (or `docker-compose.yml` `environment:` block) before rebuilding.
