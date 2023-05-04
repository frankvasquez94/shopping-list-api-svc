import json
import logging
from kit.log.log import LOGGER_NAME
from shopping_list.domain.exc import PersistenceError, ResourceNotFound
from shopping_list.domain.repository import ShoppingListRepository
from shopping_list.domain.model import ShoppingList
from .dto import UpdateShoppingListDto
from pydantic import ValidationError

UPDATE_SHOPPING_LIST_SERVICE = "Update shopping list service, "
UPDATE_SHOPPING_LIST_SERVICE_ERROR = "Update shopping list service, error description: "


class Service:
    logger: logging.Logger
    shopping_list_repository: ShoppingListRepository

    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.shopping_list_repository = shopping_list_repository

    def update(self, update_shopping_list_dto: UpdateShoppingListDto) -> UpdateShoppingListDto:
        self.logger.info(
            f'{UPDATE_SHOPPING_LIST_SERVICE} updating shopping list: {json.dumps(update_shopping_list_dto.__dict__)}')
        shopping_list_found: ShoppingList
        try:
            shopping_list_found = self.shopping_list_repository.find(update_shopping_list_dto.id)
        except PersistenceError as e:
            self.logger.error(f'{UPDATE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
        except Exception as e:
            self.logger.error(f'{UPDATE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
        else:
            if not shopping_list_found:
                self.logger.info(
                    f'{UPDATE_SHOPPING_LIST_SERVICE} shopping list with id: {update_shopping_list_dto.id} not found')
                raise ResourceNotFound

        try:
            self.logger.info(
                f'{UPDATE_SHOPPING_LIST_SERVICE} shopping list to update: {json.dumps(shopping_list_found.dict())}')
            shopping_list_found.name = update_shopping_list_dto.name
            self.shopping_list_repository.update(shopping_list_found)
            self.logger.info(
                f'{UPDATE_SHOPPING_LIST_SERVICE} shopping_list: {shopping_list_found} updated successfully')
            return update_shopping_list_dto
        except PersistenceError as e:
            self.logger.error(f'{UPDATE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
        except ValidationError as e:
            self.logger.error(f'{UPDATE_SHOPPING_LIST_SERVICE_ERROR} {e}')
            raise e
