from shopping_list.infrastructure.rest.camel_case_model import CamelCaseModel
from pydantic import Field
from typing import List

class ShoppingList(CamelCaseModel):
    id: int = Field(default=0, example="1", description="Shopping list identifier")
    name: str = Field(example="My shopping list", description="Shopping list name")

class ShoppingListResponse(CamelCaseModel):
    shopping_lists: List[ShoppingList]


