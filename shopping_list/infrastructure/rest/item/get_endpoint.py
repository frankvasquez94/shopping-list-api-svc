from .item import Item
from shopping_list.item.operations.retrieve.service import Service
from shopping_list.item.operations.retrieve.dto import RetrieveItemResponse
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException, INTERNAL_SERVER_ERROR, RESOURCE_NOT_FOUND
from shopping_list.domain.exc import PersistenceError, ResourceNotFound
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import Response

GET_ENDPOINT = "Get item endpoint,"
GET_ENDPOINT_ERROR = "Get item endpoint, error description: "


class GetEndpoint:
    get_service: Service

    def __init__(self, get_service: Service):
        self.get_service = get_service
        self.logger: logging.Logger = logging.getLogger(LOGGER_NAME)

    def get(self, item_id: int, response: Response, version: str) -> Item:
        self.logger.info(f'{GET_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{GET_ENDPOINT} request: item_id- > {item_id}')
            resp: RetrieveItemResponse = self.get_service.retrieve(item_id)
            item_response = self.__to_item(resp)
            self.logger.info(f'{GET_ENDPOINT} response: {str(json.dumps(item_response.dict()))}')
            return item_response
        except ResourceNotFound as e:
            self.logger.error(f'{GET_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=RESOURCE_NOT_FOUND, code=e.code, description=e.description)
        except PersistenceError as e:
            self.logger.error(f'{GET_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        except Exception as e:
            self.logger.error(f'{GET_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_item(self, retrieve_item_response: RetrieveItemResponse) -> Item:
        item: Item = Item(id=retrieve_item_response.id, name=retrieve_item_response.name)
        return item
