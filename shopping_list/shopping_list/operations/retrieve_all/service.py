import logging
from kit.log.log import LOGGER_NAME
from logging import Logger
from shopping_list.domain.repository import ShoppingListRepository
from typing import List
from .dto import ShoppingListResponse
from shopping_list.domain.model import ShoppingList

RETRIEVE_ALL_SHOPPING_LIST_SERVICE = "Retrieve all shopping list service, "
RETRIEVE_ALL_SHOPPING_LIST_SERVICE_ERROR = "Retrieve all shopping list service, error description: "


class Service:
    logger: Logger
    shopping_list_repository: ShoppingListRepository

    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.shopping_list_repository = shopping_list_repository

    def retrieve_all(self) -> List[ShoppingListResponse]:
        try:
            shopping_lists = self.shopping_list_repository.find_all()
        except Exception as e:
            self.logger.error(f'{RETRIEVE_ALL_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
        else:
            return self.__shopping_lists_to_shopping_lists_response(shopping_lists)

    def __shopping_lists_to_shopping_lists_response(self, shopping_lists: List[ShoppingList]) -> List[
        ShoppingListResponse]:
        response: List[ShoppingListResponse] = []
        for shopping_list in shopping_lists:
            shopping_list_response = ShoppingListResponse(id=shopping_list.id, name=shopping_list.name)
            response.append(shopping_list_response)
        return response
