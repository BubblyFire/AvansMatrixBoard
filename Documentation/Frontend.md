# Frontend Structure

## Purpose

The frontend provides a user interface for controlling the
AvansMatrixBoard. It allows users to:

- Display text on specific lines
- Upload images
- Pick predefined images
- Draw directly on a pixel grid
- Navigate between control modes

It is built using Flask templates (Jinja2) combined with JavaScript and
jQuery for real-time interaction.

---

## Location

Frontend files are organised as follows:

- `templates/` → HTML templates rendered by Flask
- `static/` → CSS, JavaScript, and external libraries

Main templates:

- `base.html` - Shared layout and navigation
- `home.html` - Home screen
- `text.html` - Text input control
- `draw.html` - Pixel drawing interface
- `image.html` - Image upload page
- `imagepicker.html` - Image selector interface

---

## Core Layout – base.html

All pages extend `base.html`, which defines:

- Page structure
- Navigation bar
- Shared scripts & styles
- Flash message display

Navigation links include:

- Home
- Text
- Draw
- Image
- Pick an Image

This ensures consistent layout across all pages.

---

## Individual Pages

### Home Page

Template: `home.html`
Displays a simple welcome screen.

### Text Control Page

Template: `text.html`

Allows sending text to 3 separate display lines. Each line has:

- A color picker
- A text box
- A send button

AJAX POST requests are sent to: /text2

Payload example:

```json
{ 
   "text": "Hello", 
   "color": "#ff0000", 
   "line": 0 
}
```

### Draw Page

Template: `draw.html`

Provides an interactive grid for pixel drawing:

- Color picker
- Draw /Erase toggle
- Clear button
- Pixel canvas table

### Image Upload Page

Template: `image.html`

Allows users to upload images using a standard HTML form.

### Image Picker Page

Template: `imagepicker.html`

Provides a visual interface for selecting predefined images using dynamic loading and JavaScript.

---

## Communication With Backend

The frontend communicates using AJAX and form submissions.

| Purpose       | Endpoint | Method |
|---------------|----------|--------|
| Send text     | /text2   | POST   |
| Upload image  | /image   | POST   |
| Draw pixels   | Dynamic  | POST   |

---

## Typical User Flow

1. User navigates using the menu
2. Selects function (Text, Draw, Image)
3. Enters data
4. Sends request
5. Backend processes the input
6. LED Matrix updates

---

## Technologies Used

- HTML5
- CSS3
- JavaScript
- jQuery
- Flask (Jinja2 templates)
- Bootstrap 4.5.2

---

## Frontend Architecture Summary

``` python
User Interface (Browser)
   ↓
Jinja2 Templates
   ↓
JavaScript / jQuery
   ↓
HTTP/ AJAX Requests
   ↓
Flask Backend
   ↓
LED Matrix Output
```
