class CustomException(Exception):
    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description

    def __str__(self):
        return f'code: {self.code}, description: {self.description}'


class ItemAlreadyExist(CustomException):
    def __init__(self, code="002", description="item already exist"):
        self.code = code
        self.description = description
        super().__init__(code=self.code, description=self.description)


class PersistenceError(CustomException):
    def __init__(self, code="003", description="an error has occurred with persistence component"):
        self.code = code
        self.description = description
        super().__init__(code=self.code, description=self.description)


class ResourceNotFound(CustomException):
    def __init__(self, code="004", description="resource not found"):
        self.code = code
        self.description = description
        super().__init__(code=self.code, description=self.description)
