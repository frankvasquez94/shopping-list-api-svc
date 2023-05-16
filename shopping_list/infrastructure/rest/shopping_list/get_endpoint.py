from .shopping_list import ShoppingList
from shopping_list.shopping_list.operations.retrieve.service import Service
from shopping_list.shopping_list.operations.retrieve.dto import ShoppingListResponse
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException, INTERNAL_SERVER_ERROR, \
    RESOURCE_NOT_FOUND
from shopping_list.domain.exc import PersistenceError, ResourceNotFound
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import Response

GET_ENDPOINT = "Get shopping list endpoint,"
GET_ENDPOINT_ERROR = "Get shopping list endpoint, error description: "


class GetEndpoint:
    get_service: Service

    def __init__(self, get_service: Service):
        self.get_service = get_service
        self.logger: logging.Logger = logging.getLogger(LOGGER_NAME)

    def get(self, shopping_list_id: int, response: Response, version: str) -> ShoppingList:
        self.logger.info(f'{GET_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{GET_ENDPOINT} request: shopping_list_id- > {shopping_list_id}')
            resp: ShoppingListResponse = self.get_service.retrieve(shopping_list_id)
            shopping_list_response = self.__to_shopping_list(resp)
            self.logger.info(f'{GET_ENDPOINT} response: {str(json.dumps(shopping_list_response.dict()))}')
            return shopping_list_response
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

    def __to_shopping_list(self, shopping_list_response: ShoppingListResponse) -> ShoppingList:
        shopping_list: ShoppingList = ShoppingList(id=shopping_list_response.id, name=shopping_list_response.name)
        return shopping_list
