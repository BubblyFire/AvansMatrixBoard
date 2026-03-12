from flask import Response

from app.utils.models import SerializableClass


class APIResponse(SerializableClass):
    def __init__(self, status: str, message: str, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = {"status": self.status}

        if self.message:
            response_dict["message"] = self.message

        if self.data:
            if not SerializableClass.is_serializable(self.data):
                raise TypeError(f"{self.data} is not json serializable")
            response_dict["data"] = self.data

        return response_dict


class SuccessResponse(APIResponse):
    def __init__(self, data=None, message: str = None):
        super().__init__(status="success", message=message, data=data)


class ErrorResponse(APIResponse):
    def __init__(self, message: str = None):
        super().__init__(status="error", message=message)


def _apply_headers_and_cookies(response: Response, headers: dict, cookies: dict) -> None:
    """Attach optional headers and cookies to a response object."""
    if headers:
        response.headers.update(headers)

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)


def success_response(
    data=None,
    status: int = 200,
    message: str = None,
    headers: dict = None,
    cookies: dict = None,
):
    """Build a JSON success response. Returns a (response, status) tuple."""
    response_data = SuccessResponse(data=data, message=message)
    response = Response(response_data.to_json(), mimetype="application/json")
    _apply_headers_and_cookies(response, headers, cookies)
    return response, status


def error_response(
    message: str = "Internal Server Error",
    status: int = 500,
    headers: dict = None,
    cookies: dict = None,
):
    """Build a JSON error response. Returns a (response, status) tuple."""
    response_data = ErrorResponse(message=message)
    response = Response(response_data.to_json(), mimetype="application/json")
    _apply_headers_and_cookies(response, headers, cookies)
    return response, status
