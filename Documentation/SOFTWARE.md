# Software

This application is a python webserver that controls a local neopixel.

This project uses Flask for the webserver. Flask is a lightweight WSGI web application framework in Python.
Flask serves the web pages and calls the appropriate Python neopixel functions when required.
The entrypoint for the Flask application is written in `app/__init__.py`.

The Flask application has four main parts:
- Templates
- Extensions
- Routes
- Static files

## Templates

Templates are the HTML files that will be served on different routes. Flask uses the Jinja template library to render templates.
There are currently four templates:

| Path | Description |
|---|---|
| app/templates/base.html | Template that is included by all other templates. Defines HTML head and includes relevant CSS and JS. |
| app/templates/pages/draw.html | Page for drawing functionalities. Contains buttons and grid. |
| app/templates/pages/home.html | Empty home page |
| app/templates/pages/image.html | Page for image functionalities. Contains file upload and submit buttons. |
| app/templates/pages/text.html | Page for text functionalities. Contains three textboxes and buttons, one for each line on the matrixboard. |

## Extensions

Extension add functionality that can be used in the entire Flask application.
There only extension added is the MatrixpiExtension (`app/extensions/matrixpi.py`).
This extension initializes a MatrixBoard (`app/extensions/matrixboard.py`) that can be used to control the neopixels. There should only be one MatrixBoard instance in the entire application.

## Routes

Flask routes map URLs to specific templates. Currently all routes are defined in `app/routes/pages/core.py`. These routes also contains most of the Python logic.

## Static files

The static files are chosen when the app is created in `app/__init__.py`.
Currently, the only static files are:

| Path | Description |
|---|---|
| app/static/css/main.css | Basic styling |
| app/static/js/jquery-3.7.1.js | jQuery library for Ajax calls |
| app/static/js/main.js | JavaScript code for drawing logic |
