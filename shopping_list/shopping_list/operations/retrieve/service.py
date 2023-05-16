import logging
from logging import Logger
from kit.log.log import LOGGER_NAME
from shopping_list.domain.repository import ShoppingListRepository
from shopping_list.domain.model import ShoppingList
from .dto import ShoppingListResponse
from shopping_list.domain.exc import ResourceNotFound

RETRIEVE_SHOPPING_LIST_SERVICE = "Retrieve Shopping list service, "
RETRIEVE_SHOPPING_LIST_SERVICE_ERROR = "Retrieve Shopping list service`, error description:  "

class Service:
    logger: Logger
    shopping_list_repository: ShoppingListRepository

    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.shopping_list_repository = shopping_list_repository

    def retrieve(self, shopping_list_id: int) -> ShoppingListResponse:
        try:
            shopping_list_domain: ShoppingList = self.shopping_list_repository.find(shopping_list_id)
            if not shopping_list_domain:
                self.logger.info(f'{RETRIEVE_SHOPPING_LIST_SERVICE} shopping list not found, id: {shopping_list_id}')
                raise ResourceNotFound
        except Exception as e:
            self.logger.error(f'{RETRIEVE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
        else:
            return self.shopping_list_to_shopping_list_response(shopping_list_domain)

    def shopping_list_to_shopping_list_response(self, shopping_list: ShoppingList) -> ShoppingListResponse:
        return ShoppingListResponse(id=shopping_list.id, name=shopping_list.name)
