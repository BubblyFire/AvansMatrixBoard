# Backend Architecture

## Overview

The backend handles requests from the web interface and converts them into commands for the LED matrix. It is built using **Flask** and follows the **Application Factory pattern**, allowing flexible configuration and clean separation of responsibilities.

---

## Entry Point

- **server.py**  
  - Starts the Flask server  
  - Calls `create_app()` from `app/__init__.py`

---

## Application Factory

**File:** `app/__init__.py`  
**Function:** `create_app(debug: bool = False)`

### Responsibilities

- Create Flask application instance
- Load configuration (DevConfig / ProdConfig)
- Initialize extensions
- Register blueprints
- Create database tables

The following extensions are imported and initialized inside the factory:

```python
from .db import db
from .cors import cors
from .matrixpi import matrixpi
```

Each extension is then activated using:

```python
db.init_app(app)
cors.init_app(app)
matrixpi.init_app(app)
```

---

## Configuration System

The configuration is dynamically selected based on the debug state:

### Development Configuration

**File:** `app/config/dev.py`

- DEBUG = True
- TESTING = True
- Auto template & static reload enabled
- Environment file: `.env.dev`
- Database: SQLite (`sqlite:///database.db`)

### Production Configuration

**File:** `app/config/prod.py`

- DEBUG = False
- TESTING = False
- Reload disabled for performance
- Environment file: `.env`
- Database: SQLite (`sqlite:///database.db`)

Configuration selection logic:

- If `FLASK_DEBUG` is set → DevConfig
- Otherwise → ProdConfig

---

## Extensions Layer

### Database (db)

File: `app/extensions/db.py`

Provides SQLAlchemy ORM integration for:

- Database connections
- Model management
- Query execution

### CORS (cors)

File: `app/extensions/cors.py`

Handles Cross-Origin Resource Sharing for API routes:

```python
cors = CORS(resources={r"/api/*": {"origins": "*"}})
```

This allows external clients (such as browsers) to call API routes without CORS errors.

### matrixpi Extension

File: `app/extensions/matrixpi.py`

Responsible for initializing the physical LED matrix controller.

Key actions:

- Instantiates `MatrixBoard(30, 30)`
- Calls `matrixboard.init()`
- Attaches the board to the Flask app context

This allows any route to access the matrix using:

```python
matrixpi.matrixboard
```

---

## Matrix Hardware Layer

### MatrixBoard

File: `app/extensions/matrixboard.py`

Responsibilities:

- Initialize NeoPixel LEDs on GPIO 18
- Translate coordinates to LED indexes
- Render text and graphics
- Scroll text smoothly across the display

Important methods:

- `scroll_text(text, color)`
- `render_text(x, row, text, color)`
- `clear()`
- `show()`

Text rendering uses:

- `bitmapfont.py` for pixel-based character drawing

---

## Routing Structure

### API Blueprint

- **api_bp** → `app/routes/api.py`  
  Handles JSON-based requests for matrix control.

### Pages Blueprint

- **pages_bp** → `app/routes/pages.py`  
  Serves frontend HTML pages.

---

## Real Data Flow

1. User submits a command via web interface
2. API route receives the request
3. Route calls `matrixpi.matrixboard`
4. MatrixBoard converts data into pixel instructions
5. NeoPixel driver updates LEDs
6. LED panel displays the result

---

## Architecture Summary

``` python
Browser
   ↓
Flask Routes (api_bp)
   ↓
matrixpi Extension
   ↓
MatrixBoard class
   ↓
NeoPixel GPIO 18
   ↓
LED Matrix (30x30)
```
