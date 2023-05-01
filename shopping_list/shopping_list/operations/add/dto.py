

class AddShoppingListRequest:
    name: str

    def __init__(self, name: str):
        self.name = name


class AddShoppingListResponse:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
