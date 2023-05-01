import logging

from shopping_list.domain.repository import ItemRepository
from logging import Logger
from kit.log.log import LOGGER_NAME
from .dto import UpdateItemRequest, UpdateItemResponse
from shopping_list.domain.model import Item
from pydantic import ValidationError

UPDATE_ITEM_SERVICE = "Update Item service, "
UPDATE_ITEM_SERVICE_ERROR = "Update Item service, error description: "


class Service:
    item_repository: ItemRepository
    logger: Logger

    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
        self.logger = logging.getLogger(LOGGER_NAME)

    def update(self, request: UpdateItemRequest) -> UpdateItemResponse:
        item = self.__update_item_request_to_domain_item(request)
        try:
            updated_item = self.item_repository.update(item)
        except Exception as e:
            self.logger.error(f'{UPDATE_ITEM_SERVICE_ERROR} {e}')
            raise e
        else:
            return self.__domain_item_to_update_item_response(updated_item)

    def __update_item_request_to_domain_item(self, request: UpdateItemRequest) -> Item:
        try:
            item = Item(id=request.id, name=request.name)
            return item
        except ValidationError as e:
            self.logger.error(f'{UPDATE_ITEM_SERVICE_ERROR} {e}')
            raise e

    def __domain_item_to_update_item_response(self, item: Item) -> UpdateItemResponse:
        return UpdateItemResponse(id=item.id, name=item.name)
