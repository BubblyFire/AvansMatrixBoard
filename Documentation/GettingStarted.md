# Getting Started (on your own laptop)

You do **not** need a Raspberry Pi or the LED matrix to work on this project. The app can run on any computer (Windows, Mac, Linux). When `DISABLE_MATRIX=1` is set, the web interface still works — it just doesn't talk to real LEDs.

## 1. Install the tools you need

- **Python 3.11+** — [python.org/downloads](https://www.python.org/downloads/)
- **Git** — [git-scm.com](https://git-scm.com/)
- A code editor — VS Code is a good default.

Check that everything is installed:

```bash
python --version     # should print 3.11 or higher
git --version
```

## 2. Clone the project

```bash
git clone <repository-url>
cd AvansMatrixBoard
```

## 3. Create a virtual environment

A virtual environment (`venv`) keeps this project's Python packages separate from the rest of your computer. Create it once:

```bash
python -m venv .venv
```

Activate it (you need to do this every new terminal):

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash / WSL) and macOS / Linux
source .venv/bin/activate
```

You'll know it worked because your prompt starts with `(.venv)`.

## 4. Install the Python packages

```bash
pip install -r requirements.txt
```

> If you see errors about `rpi_ws281x`, that's the LED driver — it only builds on Linux. You can ignore those errors on Windows/Mac; the app still runs with `DISABLE_MATRIX=1`.

## 5. Run the app without hardware

```bash
# macOS / Linux / Git Bash
DISABLE_MATRIX=1 python server.py

# Windows PowerShell
$env:DISABLE_MATRIX=1; python server.py
```

Open **http://localhost** (port 80) in your browser. You should see the home page.

> **Port 80 already in use?** Change the port in `server.py` (`app.run(..., port=5000)`) and open `http://localhost:5000`.

## 6. Make a change and see it

Flask's debug mode auto-reloads the server when you save a Python file. For HTML/CSS/JS, just refresh the browser.

Try this as a first change:

1. Open `templates/pages/home.html`.
2. Change any text you see.
3. Save the file.
4. Refresh your browser — the new text appears.

## Running with Docker instead (optional)

If Python setup gives you trouble, Docker works too:

```bash
docker compose up --build
```

Then open **http://localhost**. See [DOCKER.md](DOCKER.md) for details.

## What next?

- Read **[Overview.md](Overview.md)** if you haven't yet.
- Check **[HowTo.md](HowTo.md)** for recipes on adding pages, translations, and settings.
- When you're ready to work on real hardware, see **[SETUP.md](SETUP.md)**.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3` instead, or install Python and add it to PATH. |
| `pip install` fails on `rpi_ws281x` | Expected on Windows/Mac. The app still runs with `DISABLE_MATRIX=1`. |
| `Address already in use` on port 80 | Another program is using port 80. Change the port in `server.py`. |
| `PermissionError` on port 80 (Linux/Mac) | Ports below 1024 need admin rights. Change the port in `server.py` to 5000. |
| Browser shows old code after a change | Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac). |
| `.venv` activate says "scripts disabled" (Windows) | Run PowerShell as admin once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. |
