
INTERNAL_SERVER_ERROR = 500
BAD_REQUEST = 400
RESOURCE_NOT_FOUND = 404

class CustomHttpException(Exception):
    def __init__(self, status_code: int, code: str, description: str):
        self.description = description
        self.code = code
        self.status_code = status_code
