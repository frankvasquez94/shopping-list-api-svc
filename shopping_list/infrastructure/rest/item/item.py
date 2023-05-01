from shopping_list.infrastructure.rest.camel_case_model import CamelCaseModel
from pydantic import Field
from typing import List


class Item(CamelCaseModel):
    id: int = Field(default=0, example="1", description="Item identifier")
    name: str = Field(example="Desktop", description="Item name")


class ItemResponse(CamelCaseModel):
    items: List[Item]


