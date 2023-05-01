import logging
from logging import Logger
from kit.log.log import LOGGER_NAME
from shopping_list.domain.repository import ItemRepository

RETRIEVE_ITEM_SERVICE = "Retrieve Item service, "
RETRIEVE_ITEM_SERVICE_ERROR = "Retrieve Item service, error description:  "
from shopping_list.domain.model import Item
from .dto import RetrieveItemResponse
from shopping_list.domain.exc import ResourceNotFound


class Service:
    logger: Logger
    item_repository: ItemRepository

    def __init__(self, item_repository: ItemRepository):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.item_repository = item_repository

    def retrieve(self, item_id: int) -> RetrieveItemResponse:
        try:
            item: Item = self.item_repository.find(item_id)
            if not item:
                self.logger.info(f'{RETRIEVE_ITEM_SERVICE} item not found, id: {item_id}')
                raise ResourceNotFound
        except Exception as e:
            self.logger.error(f'{RETRIEVE_ITEM_SERVICE_ERROR} {e}')
            raise e
        else:
            return self.domain_item_to_retrieve_item_respomse(item)


    def domain_item_to_retrieve_item_respomse(self, item: Item) -> RetrieveItemResponse:
        return RetrieveItemResponse(id=item.id, name=item.name)
