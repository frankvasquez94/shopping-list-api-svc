

class UpdateItemRequest:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class UpdateItemResponse:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
