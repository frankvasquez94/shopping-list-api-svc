import logging
from logging import Logger
from shopping_list.domain.repository import ShoppingListRepository
from kit.log.log import LOGGER_NAME
from shopping_list.domain.exc import ResourceNotFound

DELETE_SHOPPING_LIST_SERVICE = "Delete shopping list service, "
DELETE_SHOPPING_LIST_SERVICE_ERROR = "Delete shopping list service, error description: "


class Service:
    logger: Logger
    shopping_list_repository: ShoppingListRepository

    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.shopping_list_repository = shopping_list_repository

    def delete(self, shopping_list_id: int) -> None:
        self.logger.info(f'{DELETE_SHOPPING_LIST_SERVICE} deleting shopping list with id: {shopping_list_id}')
        try:
            shopping_list = self.shopping_list_repository.find(shopping_list_id=shopping_list_id)
            if not shopping_list:
                self.logger.info(f'{DELETE_SHOPPING_LIST_SERVICE} shopping list with id: {shopping_list_id} not found')
                raise ResourceNotFound
            self.shopping_list_repository.delete(shopping_list_id=shopping_list_id)
            self.logger.info(
                f'{DELETE_SHOPPING_LIST_SERVICE} shopping list with id: {shopping_list_id} deleted successfully')
            return
        except Exception as e:
            self.logger.error(f'{DELETE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
