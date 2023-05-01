from .item import Item
from shopping_list.item.operations.update.service import Service
from shopping_list.item.operations.update.dto import UpdateItemRequest, UpdateItemResponse
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException, INTERNAL_SERVER_ERROR, \
    BAD_REQUEST
from shopping_list.domain.exc import ItemAlreadyExist, PersistenceError
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import Response

UPDATE_ENDPOINT = "Update item endpoint,"
UPDATE_ENDPOINT_ERROR = "Update item endpoint, error description: "


class UpdateEndpoint:
    update_service: Service

    def __init__(self, update_service: Service):
        self.update_service = update_service
        self.logger: logging.Logger = logging.getLogger(LOGGER_NAME)

    def update(self, item_request: Item, response: Response, version: str) -> Item:
        self.logger.info(f'{UPDATE_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{UPDATE_ENDPOINT} request: {str(json.dumps(item_request.dict()))}')
            item_request_service = self.__to_update_item_request_dto(item_request)
            resp: UpdateItemResponse = self.update_service.update(item_request_service)
            item_response = self.__to_item(resp)
            self.logger.info(f'{UPDATE_ENDPOINT} response: {str(json.dumps(item_response.dict()))}')
            return item_response
        except ItemAlreadyExist as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=BAD_REQUEST, code=e.code, description=e.description)
        except PersistenceError as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        except Exception as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_update_item_request_dto(self, item_request: Item) -> UpdateItemRequest:
        update_item_request = UpdateItemRequest(id=item_request.id, name=item_request.name)
        return update_item_request

    def __to_item(self, update_item_response: UpdateItemResponse) -> Item:
        item: Item = Item(id=update_item_response.id, name=update_item_response.name)
        return item
