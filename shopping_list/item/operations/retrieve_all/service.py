import logging
from kit.log.log import LOGGER_NAME
from logging import Logger
from shopping_list.domain.repository import ItemRepository
from typing import List
from .dto import ItemDTO
from shopping_list.domain.model import Item

RETRIEVE_ALL_ITEM_SERVICE = "Retrieve all Item service, "
RETRIEVE_ALL_ITEM_SERVICE_ERROR = "Retrieve all Item service, error description: "


class Service:
    logger: Logger
    item_repository: ItemRepository

    def __init__(self, item_repository: ItemRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.item_repository = item_repository

    def retrieve_all(self) -> List[ItemDTO]:
        try:
            items = self.item_repository.find_all()
        except Exception as e:
            self.logger.error(f'{RETRIEVE_ALL_ITEM_SERVICE_ERROR} {e}')
            raise e
        else:
            return self.__items_to_items_dto(items)

    def __items_to_items_dto(self, items: List[Item]) -> List[ItemDTO]:
        response: List[ItemDTO] = []
        for item in items:
            item_dto = ItemDTO(id=item.id, name=item.name)
            response.append(item_dto)
        return response
