# Frontend Structure

## Overview

The frontend is built with Flask/Jinja2 templates, Bootstrap 4, jQuery, and vanilla JavaScript. All pages extend `base.html` which provides the navbar, flash messages, toast notifications, and shared scripts.

## Templates (`templates/`)

| Template | Route | Description |
|----------|-------|-------------|
| `base.html` | — | Shared layout, navbar, language switcher, toast system |
| `pages/home.html` | `/` | Welcome screen |
| `pages/text.html` | `/text` | Send up to 3 lines of colored text to the matrix |
| `pages/draw.html` | `/draw` | Paint pixels on a 30×30 grid |
| `pages/image.html` | `/image` | Upload an image or browse the Pi file system |
| `pages/imagepicker.html` | `/imagepicker` | Browse predefined image assets |
| `pages/slideshow.html` | `/slideshow` | Cycle through a folder of images or a playlist |
| `pages/preview.html` | `/preview` | Live 30×30 browser render of what's on the matrix |
| `pages/config.html` | `/config` | Adjust hardware settings |

## JavaScript Files (`static/js/`)

| File | Used on | Purpose |
|------|---------|---------|
| `main.js` | Draw page | Grid rendering, mouse/touch drawing, pixel sending, save to PNG |
| `server.js` | Image page | Pi file browser, upload, display file on matrix |
| `imagepicker.js` | Image picker page | Folder tree, image selection |
| `api.js` | Image page | Shared `postJSON()` fetch wrapper and URL constants |
| `ui.js` | Image page | DOM element accessors and UI builders |
| `menu.js` | Image page | Context menu behaviour |
| `actions.js` | Image page | File actions (rename, delete, move) |
| `functions.js` | Image page | Path utilities (`joinPath`, `parentPath`) |
| `modal.js` | Image page | Modal dialog helpers (confirm, input) |
| `slideshow.js` | Slideshow page | Folder/playlist selection, start/stop, status polling |
| `preview.js` | Preview page | Builds the pixel grid and polls `/preview/state` a few times per second |

## Pages

### Text Page (`text.html`)

Sends text to the matrix on one of three lines. Each line has a color picker, text input, and send button. Uses jQuery AJAX to `POST /text2`. Shows a success or error toast on completion.

### Draw Page (`draw.html`)

Provides an interactive 30×30 pixel grid. Features:
- **Mouse and touch support** — works on desktop and mobile
- **Dynamic cell sizing** — grid scales to fit the screen width
- **Draw / Erase / Clear** modes
- **Save image** — downloads the current drawing as a PNG (30×30 pixels)

Sends all pixel data as a flat array of CSS `rgb()` strings to `POST /sendtoboard`.

### Image Upload Page (`image.html`)

Two sections:

**Local File Picker** — Select an image from your computer and upload it to the Pi. Supports jpg, jpeg, png, gif, bmp. Shows a preview before uploading.

**Raspberry Pi File Browser** — Browse files already stored on the Pi at `/home/avans/user_uploads`. Supports:
- Navigate folders
- Create folders
- Upload files to the current folder
- Preview images
- Display a selected file on the matrix
- Rename, move, and delete files/folders (via context menu)

### Image Picker Page (`imagepicker.html`)

Browses predefined image assets stored in `static/assets/`. Folders are loaded lazily on first open. Clicking an image sends it to the matrix via `POST /imagelist_show`.

### Slideshow Page (`slideshow.html`)

Plays a sequence of images on the matrix, switching every N seconds. Two modes:

- **Folder mode** — pick a folder under `uploads/`, `user_uploads/`, or `drawings/`; every image in it is shown in order.
- **Playlist mode** — hand-pick individual files across folders.

Controlled via `POST /slideshow/start`, `POST /slideshow/stop`, and polls `GET /slideshow/status`.

### Preview Page (`preview.html`)

A live 30×30 grid of `<div>` cells that mirrors the matrix shadow buffer in the browser. Polls `GET /preview/state` every 250 ms and only touches the DOM when a cell's colour actually changes. Polling pauses while the tab is hidden.

Especially useful with `DISABLE_MATRIX=1` — the whole app is usable without LED hardware.

> **Auto-hidden when hardware is attached.** When `matrixpi.matrixboard.hardware` is `True`, the preview nav-link disappears and both `/preview` and `/preview/state` return `404`. The physical LEDs are the source of truth in that case — a second on-screen copy would just lag behind. This is driven by the `hardware_enabled` template flag injected by `inject_hardware_state()` in `app/__init__.py`.

### Config Page (`config.html`)

Form that saves to `app/config/config.json`. Settings:

| Setting | Description |
|---------|-------------|
| Brightness | 0.0 – 1.0 |
| auto_write | If true, LEDs update immediately on each pixel set (slower) |

> The `pin` (GPIO data line) is intentionally not exposed on this page — see [Config.md](Config.md) for why and how to change it.
| Scroll delay | Seconds between scroll frames |
| Font baseline offset | Vertical pixel offset for text rendering |
| GIF speed multiplier | 1.0 = normal speed; lower = faster |

## Language Switcher

The navbar includes an EN/NL toggle that calls `GET /set-language/<lang>`. The chosen language is stored in the Flask session. All UI strings come from `app/i18n.py`.

## Toast Notifications

A global `showToast(message, type)` function is available on every page (defined in `base.html`). It shows a Bootstrap toast in the top-right corner.

```javascript
showToast('File sent to matrix.');             // green
showToast('Failed to connect.', 'error');      // red
```

## Communication With Backend

| Page | Endpoint | Method | Purpose |
|------|----------|--------|---------|
| Text | `/text2` | POST | Send a line of text to the matrix |
| Draw | `/sendtoboard` | POST | Send full pixel grid to the matrix |
| Image | `/image` | POST | Upload an image file |
| Image | `/uploads/<name>` | GET | Display uploaded image on matrix |
| Image | `/pi/files` | POST | List Pi directory contents |
| Image | `/pi/file/display` | POST | Display a Pi file on the matrix |
| Image | `/pi/file/upload` | POST | Upload a file to the Pi |
| Image | `/pi/file/preview` | GET | Preview a Pi file in the browser |
| Image | `/pi/dir/mkdir` | POST | Create a folder on the Pi |
| Image | `/pi/path/delete` | POST | Delete a file or folder |
| Image | `/pi/path/rename` | POST | Rename a file or folder |
| Image | `/pi/path/move` | POST | Move a file or folder |
| Image picker | `/imagelist` | POST | Get image directory listing |
| Image picker | `/imagelist_show` | POST | Display a predefined image |
| Slideshow | `/slideshow/start` | POST | Start a folder or playlist slideshow |
| Slideshow | `/slideshow/stop` | POST | Stop the current slideshow |
| Slideshow | `/slideshow/status` | GET | Current slideshow state |
| Preview | `/preview/state` | GET | Current shadow pixel buffer for the live preview |
| Navbar badge | `/status` | GET | What is currently playing on the matrix |
| Navbar clear | `/clear` | POST | Stop everything and turn off all LEDs |
