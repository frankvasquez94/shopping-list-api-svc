import logging

from shopping_list.domain.repository import ShoppingListRepository
from logging import Logger
from kit.log.log import LOGGER_NAME
from .dto import AddShoppingListRequest, AddShoppingListResponse
from shopping_list.domain.model import ShoppingList
from pydantic import ValidationError

ADD_SHOPPING_LIST_SERVICE = "Add shopping list service, "
ADD_SHOPPING_LIST_SERVICE_ERROR = "Add shopping list service, error description: "


class Service:
    logger: Logger
    shopping_list_repository: ShoppingListRepository

    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.shopping_list_repository = shopping_list_repository

    def add(self, request: AddShoppingListRequest) -> AddShoppingListResponse:
        try:
            shopping_list = self.shopping_list_repository.create(
                self.__add_shopping_list_request_to_shopping_list(request))
            return self.__shopping_list_to_shopping_list_response(shopping_list)
        except Exception as e:
            self.logger.error(f'{ADD_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e

    def __add_shopping_list_request_to_shopping_list(self,
                                                     add_shopping_list_request: AddShoppingListRequest) -> ShoppingList:
        try:
            shopping_list = ShoppingList(name=add_shopping_list_request.name)
            return shopping_list
        except ValidationError as e:
            self.logger.error(f'{ADD_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e

    def __shopping_list_to_shopping_list_response(self, shopping_list: ShoppingList) -> AddShoppingListResponse:
        return AddShoppingListResponse(id=shopping_list.id, name=shopping_list.name)
