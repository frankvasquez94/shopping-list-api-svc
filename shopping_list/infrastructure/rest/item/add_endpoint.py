from .item import Item
from shopping_list.item.operations.add.service import Service
from shopping_list.item.operations.add.dto import AddItemRequest, AddItemResponse
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException, INTERNAL_SERVER_ERROR, BAD_REQUEST
from shopping_list.domain.exc import ItemAlreadyExist, PersistenceError
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import status, Response


ADD_ENDPOINT = "Add item endpoint,"
ADD_ENDPOINT_ERROR = "Add item endpoint, error description: "


class AddEndpoint:
    add_service: Service

    def __init__(self, add_service: Service):
        self.add_service = add_service
        self.logger: logging.Logger = logging.getLogger(LOGGER_NAME)

    def add(self, item_request: Item, response: Response, version: str) -> Item:
        self.logger.info(f'{ADD_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{ADD_ENDPOINT} request: {str(json.dumps(item_request.dict()))}')
            item_request_service = self.__to_add_item_request_dto(item_request)
            resp: AddItemResponse = self.add_service.add(item_request_service)
            item_response = self.__to_item(resp)
            self.logger.info(f'{ADD_ENDPOINT} response: {str(json.dumps(item_response.dict()))}')
            response.status_code = status.HTTP_201_CREATED
            return item_response
        except ItemAlreadyExist as e:
            self.logger.error(f'{ADD_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=BAD_REQUEST, code=e.code, description=e.description)
        except PersistenceError as e:
            self.logger.error(f'{ADD_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        except Exception as e:
            self.logger.error(f'{ADD_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code="001", description="internal server error")

    def __to_add_item_request_dto(self, item_request: Item) -> AddItemRequest:
        add_item_request = AddItemRequest(name=item_request.name)
        return add_item_request

    def __to_item(self, add_item_response: AddItemResponse) -> Item:
        item: Item = Item(name=add_item_response.name)
        item.id = add_item_response.id
        return item


