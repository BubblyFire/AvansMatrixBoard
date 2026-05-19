# Wishlist / Feature Backlog

Improvements and ideas for the AvansMatrixBoard project.

**Status legend:** `done` · `partial` · `todo`

## UX & Accessibility

| Status | Item | Notes |
|--------|------|-------|
| `partial` | **Mobile-friendly interface** | Bootstrap handles basic responsiveness. The draw page (canvas with zoom/pan) is not well-suited for touch yet. |
| `done` | **"Clear matrix" button on every page** | `POST /clear` calls `clear_matrix()`; button lives in the navbar in `base.html`. |
| `todo` | **Dark/light mode toggle** | Add a theme toggle to the navbar. Store preference in `localStorage`. |
| `done` | **Toasts / feedback notifications** | `showToast()` is available globally via `base.html` and used across all pages. |
| `todo` | **Keyboard shortcuts** | Useful on the draw page: `E` for erase, `D` for draw, `Ctrl+Z` for undo, `Space` to toggle pan mode. |
| `todo` | **Quick brightness slider in navbar** | A small slider in the navbar that calls `POST /config/save` on change. Right now brightness is only adjustable via the `/config` page. |
| `todo` | **Config restart warning** | Show a warning on the `/config` page when a setting that requires a Pi restart is changed (e.g. GPIO pin). |

---

## Networking / Deployment

| Status | Item | Notes |
|--------|------|-------|
| `done` | **Serve on port 80** | Server binds to `0.0.0.0:80`. Requires `sudo` on the Pi. |
| `todo` | **Captive portal** | Flask routes in `portal.py` intercept OS connectivity checks and redirect to the matrix interface. DNS redirect via dnsmasq. |
| `done` | **Open Wi-Fi (no password)** | Currently the SoftAP requires no password to connect. |

---

## Image Handling

| Status | Item | Notes |
|--------|------|-------|
| `done` | **Upload images to a user directory** | `/image` page saves files to `/opt/matrixpi`. |
| `done` | **Create subfolders in the user directory** | `POST /pi/dir/mkdir` creates folders under `/home/avans/user_uploads`. |
| `done` | **Alpha channel support (PNG transparency)** | `composite_on_black()` in `utils.py` composites RGBA/LA images onto a black background before rendering. |
| `done` | **Animated GIF playback** | `play_gif_loop()` plays GIFs in a daemon thread with configurable speed via `gif_delay` in the config. |
| `done` | **Slideshow mode** | Full slideshow page at `/slideshow`. Supports folder mode and playlist mode, with configurable interval. Routes in `routes/slideshow.py`, logic in `utils/utils.py`. |
| `todo` | **Image search / filter in imagepicker** | The image list is already fetched as JSON via `POST /imagelist`. A client-side text input that filters the displayed items is pure frontend work. |
| `todo` | **Image fit modes** | Currently images are always resized to fill the 30×30 grid. Add options: *fit* (letterbox), *fill* (crop to center), *stretch*. |

---

## Draw Page

| Status | Item | Notes |
|--------|------|-------|
| `done` | **Save drawn images** | Export the current 30×30 canvas as a PNG that gets saved to the Pi or downloaded to the browser. |
| `todo` | **Fill / flood fill tool** | Bucket-fill a contiguous area with a color. |
| `todo` | **Color palette / saved colors** | Let users save frequently used colors to a small swatch strip. |
| `done` | **Import image to canvas** | The draw page can load any image (local file or from the Pi) directly into the 30×30 canvas via the 📂 Load button. |

---

## Text Page

| Status | Item | Notes |
|--------|------|-------|
| `todo` | **Live character counter** | Show how many characters fit per line given the 5px-wide font and 30px matrix width. Simple JS calculation. |
| `todo` | **Preset messages** | A list of saved/favourite messages the user can one-click send. |
| `todo` | **Rainbow / gradient text color** | Cycle hue across the characters of a line instead of a single flat color. |

---

## Scheduling & Automation

| Status | Item | Notes |
|--------|------|-------|
| `todo` | **Scheduled display** | Show a specific image or text at a set time (e.g. every day at 08:00). Could use APScheduler integrated into the Flask app, with schedules stored in the SQLite DB (already set up but unused). |
| `todo` | **Auto-off / sleep timer** | Turn the matrix off after N minutes of inactivity. |
| `todo` | **On/off schedule** | Define daily time windows when the matrix is active (e.g. 08:00–22:00). Useful for saving LED lifetime. |

---

## Live Preview & Status

| Status | Item | Notes |
|--------|------|-------|
| `done` | **Live matrix preview in browser** | `/preview` page polls `/preview/state`, which returns `MatrixBoard.get_pixels()` (shadow buffer in visual row-major order). Works with `DISABLE_MATRIX=1`. |
| `done` | **"Now playing" indicator** | Badge in the navbar polls `/status` every 4 seconds and shows the current type and filename. |
| `todo` | **System stats on home page** | Show Pi CPU temp, memory usage, and uptime on the home page. Useful for knowing if the Pi is struggling. |

---

## Code & Infrastructure

| Status | Item | Notes |
|--------|------|-------|
| `todo` | **Enable the logger** | `setup_flask_logger()` in `app/utils/logger.py` is commented out in `__init__.py`.|
| `todo` | **API authentication** | The `/api/` endpoints are currently restricted to localhost only. |
| `todo` | **Proper test suite** | Improve testing cases |
