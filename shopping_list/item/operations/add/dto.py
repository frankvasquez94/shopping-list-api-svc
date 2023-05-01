class AddItemRequest:
    name: str

    def __init__(self, name: str):
        self.name = name


class AddItemResponse:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
