import logging

from shopping_list.shopping_list.operations.add.service import Service
from logging import Logger
from kit.log.log import LOGGER_NAME
from .shopping_list import ShoppingList
from fastapi import Response, status
from shopping_list.shopping_list.operations.add.dto import AddShoppingListRequest, AddShoppingListResponse
import json
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from shopping_list.domain.exc import PersistenceError

ADD_ENDPOINT = "Add shopping list endpoint, "
ADD_ENDPOINT_ERROR = "Add shopping list endpoint, error description: "


class AddEndpoint:
    logger: Logger
    add_shopping_list_service: Service

    def __init__(self, add_shopping_list_service: Service):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.add_shopping_list_service = add_shopping_list_service

    def add(self, shopping_list_request: ShoppingList, response: Response, version: str) -> ShoppingList:
        self.logger.info(f'{ADD_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{ADD_ENDPOINT} creating shopping list: {json.dumps(shopping_list_request.dict())}')
            service_resp = self.add_shopping_list_service.add(
                request=self.__to_shopping_list_request(shopping_list_request))
            endppoint_resp = self.__to_shopping_list(service_resp)
            self.logger.info(f'{ADD_ENDPOINT} shopping list created successfully: {json.dumps(endppoint_resp.dict())}')
            response.status_code = status.HTTP_201_CREATED
            return endppoint_resp
        except PersistenceError as e:
            self.logger.error(f'{ADD_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code,
                                      description=e.description)
        except Exception as e:
            self.logger.error(f'{ADD_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_shopping_list_request(self, shopping_list: ShoppingList) -> AddShoppingListRequest:
        return AddShoppingListRequest(name=shopping_list.name)

    def __to_shopping_list(self, add_shopping_list_response: AddShoppingListResponse) -> ShoppingList:
        return ShoppingList(id=add_shopping_list_response.id, name=add_shopping_list_response.name)
