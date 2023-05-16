from .shopping_list import ShoppingList
from shopping_list.shopping_list.operations.retrieve_all.service import Service
from shopping_list.shopping_list.operations.retrieve_all.dto import ShoppingListResponse as ShoppingListDTO
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from shopping_list.domain.exc import PersistenceError
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import status, Response
from shopping_list.infrastructure.rest.shopping_list.shopping_list import ShoppingListResponse
from typing import List

GET_ALL_ENDPOINT = "Get all shopping list endpoint"
GET_ALL_ENDPOINT_ERROR = "Get all shopping list endpoint, error description: "


class GetAllEndpoint:
    logger: logging.Logger
    get_all_service: Service

    def __init__(self, get_all_service: Service):
        self.get_all_service = get_all_service
        self.logger = logging.getLogger(LOGGER_NAME)

    def get_all(self, response: Response, version: str) -> ShoppingListResponse:
        self.logger.info(f'{GET_ALL_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{GET_ALL_ENDPOINT}')
            resp: List[ShoppingListDTO] = self.get_all_service.retrieve_all()
            shopping_lists = self.__to_shopping_list_response(resp)
            self.logger.info(f'{GET_ALL_ENDPOINT} response: {str(json.dumps(shopping_lists.dict()))}')
            return shopping_lists
        except PersistenceError as e:
            self.logger.error(f'{GET_ALL_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code,
                                      description=e.description)
        except Exception as e:
            self.logger.error(f'{GET_ALL_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_shopping_list_response(self, shopping_lists_dto: List[ShoppingListDTO]) -> ShoppingListResponse:
        shopping_lists_response: List[ShoppingList] = []
        for shopping_list_dto in shopping_lists_dto:
            shopping_list: ShoppingList = ShoppingList(id=shopping_list_dto.id, name=shopping_list_dto.name)
            shopping_lists_response.append(shopping_list)
        return ShoppingListResponse(shopping_lists=shopping_lists_response)
