# AvansMatrixBoard – Project Overview

## What is AvansMatrixBoard?

AvansMatrixBoard is a digital LED matrix display system used within Avans school. It is capable of displaying text, images, GIFs, and custom drawn visuals on a 30×30 NeoPixel LED matrix. The system is controlled through a web-based interface and runs on a Raspberry Pi connected to the LED matrix panel.

## System Components

The project consists of four main parts:

1. **Frontend** — Web interface (HTML, CSS, JavaScript, Bootstrap)
2. **Backend** — Flask application (Python)
3. **Raspberry Pi Controller** — Runs the backend and drives the hardware
4. **LED Matrix Board** — 30×30 NeoPixel LED panel

## High-Level Flow

```
User (Browser)
      ↓
Web Interface (HTML / JS)
      ↓
Flask Backend (Python)
      ↓
MatrixBoard Controller
      ↓
NeoPixel LEDs (GPIO 18)
      ↓
LED Matrix (30×30)
```

## Features

- **Text** — Send up to 3 lines of colored text to the matrix
- **Draw** — Paint pixels on a 30×30 grid and send to the matrix (mouse & touch)
- **Image upload** — Upload an image from your computer and display it
- **Image picker** — Browse and select from predefined images stored on the Pi
- **Pi file browser** — Browse, upload, rename, move and delete files on the Pi
- **Animated GIF** — Display animated GIFs with configurable playback speed
- **Config** — Adjust hardware settings (brightness, pin, scroll speed, etc.)
- **Language switcher** — UI available in English and Dutch

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, SQLAlchemy, Flask-CORS |
| Frontend | HTML5, CSS3, JavaScript, jQuery, Bootstrap 4 |
| Hardware | Raspberry Pi 4, NeoPixel (rpi_ws281x), Adafruit CircuitPython |
| Image processing | Pillow |

## Running Without Hardware

Set the `DISABLE_MATRIX=1` environment variable to run the application on a regular computer without a connected LED matrix. All routes will still work but hardware calls are skipped.

```bash
DISABLE_MATRIX=1 python server.py
```
