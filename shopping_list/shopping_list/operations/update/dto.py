

class UpdateShoppingListDto:
    id: int
    name: str
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


