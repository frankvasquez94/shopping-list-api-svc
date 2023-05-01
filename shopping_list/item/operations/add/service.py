from .dto import AddItemRequest, AddItemResponse
from shopping_list.domain.model import Item
from shopping_list.domain.repository import ItemRepository
from pydantic import ValidationError


class Service:

    item_repository: ItemRepository

    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def add(self, request: AddItemRequest) -> AddItemResponse:
        item = self.__add_item_request_to_domain_item(request)
        item_persisted = self.item_repository.create(item)
        add_item_response = self.__item_to_add_item_response(item_persisted)
        return add_item_response

    def __add_item_request_to_domain_item(self, request: AddItemRequest) -> Item:
        try:
            item = Item(name=request.name)
            return item
        except ValidationError as e:
            raise e

    def __item_to_add_item_response(self, item: Item) -> AddItemResponse:
        try:
            add_item_response = AddItemResponse(id=item.id, name=item.name)
            return add_item_response
        except ValidationError as e:
            raise e
