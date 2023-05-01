import logging
from logging import Logger
from kit.log.log import LOGGER_NAME
from shopping_list.domain.repository import ItemRepository

DELETE_ITEM_SERVICE = "Delete Item service, "
DELETE_ITEM_SERVICE_ERROR = "Delete Item service, error description: "


class Service:
    logger: Logger
    item_repository: ItemRepository

    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
        self.logger = logging.getLogger(LOGGER_NAME)

    def delete(self, item_id) -> None:
        try:
            self.item_repository.delete(item_id)
            return
        except Exception as e:
            self.logger.error(f'{DELETE_ITEM_SERVICE_ERROR} {e}')
            raise e
