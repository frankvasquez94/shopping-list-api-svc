from pydantic import BaseModel, validator
from typing import List


# contiene el modelo del dominio

class ShoppingList(BaseModel):
    id: int = 0
    name: str
    # No se permiten items repetidos
    item_details: List["Detail"] = []

    #class Config:
        #validate_assignment = True

    def get_total(self) -> float:
        total = 0.00
        for item_detail in self.item_details:
            total += item_detail.get_total()
        return total

    def get_unchecked_total(self) -> float:
        total = 0.00
        for item_detail in self.item_details:
            if not item_detail.checked:
                total += item_detail.get_total()
        return total

    def get_checked_total(self) -> float:
        total = 0.00
        for item_detail in self.item_details:
            if item_detail.checked:
                total += item_detail.get_total()
        return total

    def add_item_detail(self, item_detail) -> None:
        self.item_details.append(item_detail)

    def remove_item_detail(self, item_detail) -> None:
        self.item_details.remove(item_detail)


class Item(BaseModel):
    id: int = 0
    name: str


class Category(BaseModel):
    id: int = 0
    name: str


class Measure(BaseModel):
    id: int = 0
    name: str


class Detail(BaseModel):
    id: int = 0
    quantity: int = 0
    price: float = 0.00
    checked: bool = False
    comment: str = None
    measure: Measure
    category: Category
    item: Item

    def get_total(self):
        return self.quantity * self.price

    @validator("price", pre=True, always=True)
    def valid_price(cls, val):
        if val < 0.00:
            raise ValueError("price must be greater or equals than 0.00")
        return val

    @validator("quantity", pre=True, always=True)
    def valid_quantity(cls, val):
        if val < 0:
            raise ValueError("quantity must be greater or equals than 0")
        return val

    class Config:
        # Asegura que cuando se le setea un valor de manera explicita
        # se valida el valor. De forma contraria, solo se validaria al
        # invocar el constructor
        validate_assignment = True

    # Getter and setter validations
    # @property
    # def price(self):
    #     return self._price
    #
    # @price.setter
    # def price(self, val):
    #     if val < 0.00:
    #         raise ValueError("quantity must be greater or equals than 0")
    #     self._price = val

