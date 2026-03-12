# API Endpoints

## Matrix Control Endpoints

These routes are served by the `core_bp` blueprint under `/`.

---

### POST /text2

Send a line of text to the LED matrix.

**Request body:**
```json
{ "text": "Hello", "color": "#ff0000", "line": 0 }
```

`line` is 0-indexed (0 = top line, 1 = middle, 2 = bottom).

**Response:** `200 OK`

---

### POST /sendtoboard

Send a full pixel frame to the LED matrix.

**Request body:**
```json
{ "value": ["rgb(255,0,0)", "rgb(0,0,0)", ...] }
```

`value` is a flat array of 900 CSS `rgb()` color strings (30×30), in row-major order (left to right, top to bottom).

**Response:** `200 OK`

---

### GET/POST /image

`GET` — Returns the image upload page.

`POST` — Uploads an image file from a form. On success, redirects to `/uploads/<filename>`.

---

### GET /uploads/\<filename\>

Displays an uploaded image on the LED matrix and serves the file to the browser.

---

### POST /imagelist

Returns the directory listing for the image picker, based on `info.json` files in `static/assets/`.

**Request body:**
```json
{ "path": "traffic" }
```

**Response:**
```json
{
  "dirs": [{ "ico": "...", "src": "...", "desc": "..." }],
  "imgs": [{ "src": "...", "alt": "...", "desc": "..." }]
}
```

---

### POST /imagelist_show

Displays a predefined image from `static/assets/` on the LED matrix.

**Request body:**
```json
{ "path": "assets/traffic/example.png" }
```

**Response:** `200`

---

### GET /config

Returns the configuration page.

---

### POST /config/save

Saves the matrix hardware configuration to `app/config/config.json`.

**Form fields:** `pin`, `brightness`, `auto_write`, `scroll_delay`, `font_baseline_offset`, `gif_delay`

**Response:** Redirects to `GET /config`

---

## Pi File Browser Endpoints

These routes allow managing files in `/home/avans/user_uploads` on the Raspberry Pi.

---

### POST /pi/files

List the contents of a directory.

**Request body:**
```json
{ "path": "subfolder" }
```

**Response:**
```json
{ "path": "subfolder", "dirs": ["folder1"], "files": ["image.png"] }
```

---

### POST /pi/dir/mkdir

Create a new directory.

**Request body:**
```json
{ "path": "subfolder", "name": "new_folder" }
```

---

### GET /pi/file/preview?path=\<path\>

Serve a file for preview in the browser.

---

### POST /pi/file/display

Display a file from the Pi on the LED matrix.

**Request body:**
```json
{ "path": "subfolder/image.png" }
```

---

### POST /pi/file/upload

Upload a file to a directory on the Pi. Sent as `multipart/form-data`.

**Form fields:** `file` (the file), `path` (target directory)

---

### POST /pi/path/delete

Delete a file or empty directory.

**Request body:**
```json
{ "path": "subfolder/image.png" }
```

---

### POST /pi/path/rename

Rename a file or directory.

**Request body:**
```json
{ "path": "subfolder/old.png", "new_name": "new.png" }
```

---

### POST /pi/path/move

Move a file or directory to a different folder.

**Request body:**
```json
{ "src": "folder/image.png", "dst_dir": "other_folder" }
```

---

## Test Endpoints

These routes are only accessible from `127.0.0.1` or `::1` (localhost).

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tests/hello` | GET | Returns `{ "message": "Hello World!!" }` |
| `/api/tests/success` | GET | Returns a structured success response |
| `/api/tests/bad-request` | GET | Simulates a 400 error |
| `/api/tests/forbidden` | GET | Simulates a 403 error |
| `/api/tests/internal-server-error` | GET | Simulates a 500 error |
| `/api/tests/unknown-exception` | GET | Simulates an unhandled exception |

---

## Language

### GET /set-language/\<lang\>

Switch the UI language. Stores the choice in the session and redirects back to the previous page.

Supported values: `en`, `nl`
