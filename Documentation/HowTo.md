# How-To Cookbook

Short recipes for changes you'll probably need to make. Each recipe lists the files you touch and shows a minimal example.

## Add a new page

**Files to touch:**
- `templates/pages/mypage.html` — the HTML
- `app/routes/pages/routes/mypage.py` — the route
- `app/routes/pages/__init__.py` — import your new route file so Flask picks it up
- `templates/base.html` — add a link in the navbar (optional)

**1. Create the template** — copy an existing file like `home.html` and rename it.

**2. Create the route file** `app/routes/pages/routes/mypage.py`:

```python
from flask import render_template
from app.routes.pages.blueprint import core_bp

@core_bp.route("/mypage")
def mypage():
    return render_template("pages/mypage.html")
```

**3. Import it** in `app/routes/pages/__init__.py` so Flask actually knows about it. Add your module to the existing `from .routes import ...` line:

```python
from .routes import home, draw, text, image_uploads, imagepicker, pi_files, status, slideshow, portal, mypage
```

**4. Navbar link** in `templates/base.html`: copy an existing `<li>` and change the `href`.

Restart the server (or just save — debug mode reloads). Visit `http://localhost/mypage`.

## Add a new API endpoint

API routes return JSON and live under `/api/`.

**File:** `app/routes/api/tests.py` (or make a new file next to it and import it in `app/routes/api/__init__.py`).

```python
from app.routes.api import api_bp
from app.utils.api import success_response, error_response

@api_bp.route("/hello/<name>")
def hello(name):
    if not name:
        return error_response("name is required")
    return success_response(data={"greeting": f"Hi {name}"})
```

All `/api/*` responses follow this format:

```json
{ "status": "success", "message": "...", "data": { ... } }
{ "status": "error",   "message": "..." }
```

## Add a translation (English / Dutch)

All UI strings live in **one dictionary** in `app/i18n.py`.

```python
TRANSLATIONS = {
    "en": {
        "my_new_key": "Hello",
        ...
    },
    "nl": {
        "my_new_key": "Hallo",
        ...
    },
}
```

Use it in a template:

```html
<h1>{{ t('my_new_key') }}</h1>
```

Never hard-code English text in templates — always go through `t()`.

## Add a new language

1. Add a `"de": { ... }` block to `TRANSLATIONS` in `app/i18n.py` with every key translated. `SUPPORTED_LANGUAGES` is derived from `TRANSLATIONS` automatically — no separate list to edit.
2. Add a button in the language switcher in `templates/base.html` that links to `/set-language/de`.

## Add a new hardware setting

Hardware settings are stored in `app/config/config.json` and loaded by `app/extensions/config.py`.

**1. Add the setting** in `app/extensions/config.py` (give it a default value).

**2. Use it** in `app/extensions/matrixboard.py` (read it where you need it).

**3. Expose it on the config page:**
- Add a form field in `templates/pages/config.html`.
- Handle the new field in `POST /config/save` in `app/routes/pages/routes/config.py`.

**4. Add translations** for the field label in `app/i18n.py`.

## Show something on the matrix

From Python, go through the `matrixpi` extension:

```python
from app.extensions import matrixpi

if matrixpi.matrixboard is not None:      # always check — might be None in dev
    matrixpi.matrixboard.clear()
    matrixpi.matrixboard.draw_text("Hi", color=(255, 0, 0), line=0)
    matrixpi.matrixboard.show()
```

The `is not None` check lets your code work on a laptop where `DISABLE_MATRIX=1` is set.

## Display an image from disk

`show_file(path)` is the one-stop function — it handles static images **and** GIFs:

```python
from app.routes.pages.utils.utils import show_file

show_file("/path/to/image.png")   # or .gif
```

For GIFs it starts a background thread that loops the animation. Calling `show_file` again cancels the previous one.

## Safely handle a user-supplied file path

Never use a path from a form directly — a malicious user could write `../../etc/passwd`. Always funnel it through `safe_join_under_root`:

```python
from app.routes.pages.utils.utils import safe_join_under_root

safe_path = safe_join_under_root("/home/avans/user_uploads", user_input)
```

This raises an error if the result would escape the root folder.

## Show a toast notification (frontend)

`showToast` is available on every page (defined in `base.html`):

```javascript
showToast("Saved!");                 // green
showToast("Something broke", "error"); // red
```

## Add a new JavaScript file

1. Put it in `static/js/myfile.js`.
2. Include it in the template that needs it:

```html
{% block scripts %}
    {{ super() }}
    <script src="{{ url_for('static', filename='js/myfile.js') }}"></script>
{% endblock %}
```

## Debug tips

- The Flask debug toolbar appears in the browser when there's an error — read the stack trace.
- `print(...)` output shows up in the terminal where the server runs.
- For JavaScript: open the browser DevTools (F12) → Console.
- For network requests (e.g. "my POST isn't working"): DevTools → Network → click the request → Response tab.

## Glossary

| Term | Meaning |
|---|---|
| **Flask** | The Python web framework this app is built on. |
| **Route** | A URL pattern mapped to a Python function (e.g. `@app.route("/text")`). |
| **Blueprint** | A group of related routes. This project has two: `api_bp` (`/api/*`) and `pages_bp` (the rest). |
| **Application factory** | The `create_app()` function that builds and returns the Flask app. |
| **Template** | An HTML file with placeholders (`{{ }}`) that Flask fills in before sending to the browser. |
| **Jinja2** | The template language Flask uses (the `{{ }}` and `{% %}` syntax). |
| **Context processor** | Code that adds variables to every template automatically (we use one for `t()`). |
| **Session** | A per-user storage that survives across page loads (we use it for the language choice). |
| **Daemon thread** | A background thread that Python kills automatically when the main program exits. |
| **NeoPixel** | The brand of addressable RGB LEDs this project uses. |
| **GPIO** | General Purpose Input/Output — the physical pins on the Raspberry Pi. |
| **Serpentine wiring** | Rows of LEDs that snake back and forth: row 0 left→right, row 1 right→left, etc. |
