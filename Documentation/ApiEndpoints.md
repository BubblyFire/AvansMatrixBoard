# API Endpoints

## Base URL

Backend API routes are exposed under:

    /api

This blueprint handles system and test-related endpoints.

---

## Core System API (api blueprint)

### GET /api/tests/hello

Description:
Returns a simple test response to verify the API is reachable.

Response:

```json
{
  "message": "Hello World!!"
}
```

---

### GET /api/tests/success

Description:
Returns a structured successful JSON response.

Response example:

```json
{
  "title": "riad-azz",
  "content": "Successful API response"
}
```

---

### GET /api/tests/bad-request

Description:
Simulates a bad request error.

Response:

- 400 Bad Request

---

### GET /api/tests/forbidden

Description:
Simulates a forbidden access error.

Response:

- 403 Forbidden

---

### GET /api/tests/internal-server-error

Description:
Simulates a server error.

Response:

- 500 Internal Server Error

---

### GET /api/tests/unknown-exception

Description:
Simulates an unknown exception.

Response:

- 500 Internal Server Error

Access restriction:
These endpoints are only accessible from `localhost` or `127.0.0.1`.

---

## Frontend-Controlled Matrix Endpoints

### POST /text2

Description:
Sends text to the LED matrix and renders it on a specific line.

Request body:

```json
{
  "text": "Hello",
  "color": "#ff0000",
  "line": 0
}
```

Response:

- 200 OK

---

### POST /sendtoboard

Description:
Receives pixel data and renders it onto the LED matrix.

Request body:

```json
{
  "value": ["rgb(255,0,0)", "rgb(0,0,0)"]
}
```

Response:

- 200 OK

---

### POST /image

Description:
Uploads an image and displays it on the LED matrix.

Response:

- Redirect to `/uploads/<filename>`

---

### GET /uploads/`<filename>`{=html}

Description:
Displays the uploaded image on the LED matrix.

---

### POST /imagelist

Description:
Returns available image directories and files.

Request body:

```json
{
  "path": "subfolder"
}
```

---

### POST /imagelist_show

Description:
Displays a selected image on the matrix.

Request body:

```json
{
  "path": "assets/example.png"
}
```

---

## Summary Table

| Purpose               | Endpoint                | Method |
|-----------------------|-------------------------|--------|
| Send text to matrix   | /text2                  | POST   |
| Draw pixels           | /sendtoboard            | POST   |
| Upload image          | /image                  | POST   |
| Show uploaded image   | /uploads/<filename>     | GET    |
| List images           | /imagelist              | POST   |
| Show selected image   | /imagelist_show         | POST   |
| API test hello        | /api/tests/hello        | GET    |
