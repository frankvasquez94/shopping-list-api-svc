
import abc
from .model import Item, Category, Detail, Measure, ShoppingList
from typing import List


class CategoryRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, category: Category) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, category_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, category: Category) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, category_id: int) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self) -> List["Category"]:
        raise NotImplementedError


class ItemRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, item: Item) -> Item:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, item_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, item: Item) -> Item:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, item_id: int) -> Item:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self) -> List[Item]:
        raise NotImplementedError


class MeasureRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, measure: Measure) -> Measure:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, measure_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, measure: Measure) -> Measure:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, measure_id: int) -> Measure:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self) -> List[Measure]:
        raise NotImplementedError


class ShoppingListRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, shopping_list: ShoppingList) -> ShoppingList:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, shopping_list_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, shopping_list: ShoppingList) -> ShoppingList:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, shopping_list_id: int) -> ShoppingList:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self) -> List[ShoppingList]:
        raise NotImplementedError


class ItemDetailChecker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check(self, shopping_list_id: int, item_id: int, checked: bool) -> None:
        raise NotImplementedError



# recupera el detalle de un item
class ItemDetailRetriever(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def retrieve(self, shopping_list_id: int, item_id: int) -> Detail:
        raise NotImplementedError


# Elimina un item de una lista de compra
class ItemDetailDeleter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def delete(self, id_shopping_list_id: int, item_id: int) -> None:
        raise NotImplementedError

# Actualiza el detalle de un item
class ItemDetailUpdater(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, detail: Detail) -> Detail:
        raise NotImplementedError


# Agrega un nuevo item a la lista de compras
class ItemDetailAdder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, detail: Detail) -> Detail:
        raise NotImplementedError


# Devuelve el detalle de los items del shopping list
class ShoppingListDetails(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, shopping_list_id: int) -> ShoppingList:
        raise NotImplementedError
