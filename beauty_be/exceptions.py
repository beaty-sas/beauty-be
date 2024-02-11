import ujson


class AuthError(Exception):
    pass


class HTTPClientError(Exception):
    def __init__(self, url: str, status_code: int | None, response_text: str):
        self.url = url
        self.status_code = status_code
        self.response_text = response_text

    def json(self) -> dict | None:
        try:
            return ujson.loads(self.response_text)

        except ValueError:
            return None

    def __str__(self) -> str:
        return f'URL {self.url} responded with {self.status_code}. RESPONSE: {self.response_text}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} status_code={self.status_code}>'


class BaseServiceError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

    def __str__(self):
        return self.detail


class ValidationError(Exception):
    pass


class DoesNotExistError(Exception):
    pass


class AlreadyExistError(Exception):
    pass
