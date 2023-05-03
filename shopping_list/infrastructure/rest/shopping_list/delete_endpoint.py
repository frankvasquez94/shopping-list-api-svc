import logging
from logging import Logger
from shopping_list.shopping_list.operations.delete.service import Service
from kit.log.log import LOGGER_NAME
from fastapi import status, Response
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from shopping_list.domain.exc import PersistenceError, ResourceNotFound

DELETE_ENDPOINT = "Delete shopping list endpoint, "
DELETE_ENDPOINT_ERROR = "Delete shopping list endpoint, error description: "


class DeleteEndpoint:
    logger: Logger
    delete_service: Service

    def __init__(self, delete_service: Service):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.delete_service = delete_service

    def delete(self, shopping_list_id: int, response: Response, version: str) -> None:
        self.logger.info(f'{DELETE_ENDPOINT} deleting shopping list with id: {shopping_list_id}, version: {version}')
        try:
            self.delete_service.delete(shopping_list_id)
            response.status_code = status.HTTP_204_NO_CONTENT
            self.logger.info(
                f'{DELETE_ENDPOINT} shopping list with id: {shopping_list_id} deleted successfully')
            return
        except PersistenceError as e:
            self.logger.error(f'{DELETE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code,
                                      description=e.description)
        except ResourceNotFound as e:
            self.logger.error(f'{DELETE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND, code=e.code,
                                      description=e.description)
        except ResourceNotFound as e:
            self.logger.error(f'{DELETE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")
