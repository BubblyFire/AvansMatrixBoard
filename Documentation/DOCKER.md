# Running with docker

```bash
# First time (builds the image)
docker compose up --build

# After that
docker compose up
```

The app will be available at http://localhost.

File changes (Python, HTML, JS, CSS) are reflected automatically — no rebuild needed. Flask's reloader will restart the server when it detects changes.

> **Note:** `DISABLE_MATRIX=1` is set in the Dockerfile by default, so the app runs without physical LED hardware.
