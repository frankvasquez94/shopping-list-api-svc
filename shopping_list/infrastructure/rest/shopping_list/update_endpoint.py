from .shopping_list import ShoppingList
from shopping_list.shopping_list.operations.update.service import Service
from shopping_list.shopping_list.operations.update.dto import UpdateShoppingListDto
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from shopping_list.domain.exc import PersistenceError, ResourceNotFound
import json
from kit.log.log import LOGGER_NAME
from fastapi import Response, status
import logging

UPDATE_ENDPOINT = "Update shopping list endpoint,"
UPDATE_ENDPOINT_ERROR = "Update shopping list endpoint, error description: "


class UpdateEndpoint:
    logger: logging.Logger
    update_service: Service

    def __init__(self, update_service: Service):
        self.update_service = update_service
        self.logger = logging.getLogger(LOGGER_NAME)

    def update(self, shopping_list: ShoppingList, response: Response, version: str) -> ShoppingList:
        self.logger.info(f'{UPDATE_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{UPDATE_ENDPOINT} request: {str(json.dumps(shopping_list.dict()))}')
            update_request_service = self.__to_shopping_list_update_request(shopping_list)
            resp: UpdateShoppingListDto = self.update_service.update(update_request_service)
            shopping_list_response = self.__to_shopping_list(resp)
            self.logger.info(f'{UPDATE_ENDPOINT} response: {str(json.dumps(shopping_list_response.dict()))}')
            return shopping_list_response
        except ResourceNotFound as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND, code=e.code, description=e.description)
        except PersistenceError as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        except Exception as e:
            self.logger.error(f'{UPDATE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_shopping_list_update_request(self, shopping_list: ShoppingList) -> UpdateShoppingListDto:
        return UpdateShoppingListDto(id=shopping_list.id, name=shopping_list.name)

    def __to_shopping_list(self, update_shopping_list_dto: UpdateShoppingListDto) -> ShoppingList:
        return ShoppingList(id=update_shopping_list_dto.id, name=update_shopping_list_dto.name)

