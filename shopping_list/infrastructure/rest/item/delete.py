import logging
from logging import Logger
from shopping_list.item.operations.delete.service import Service
from kit.log.log import LOGGER_NAME
from fastapi import status, Response
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException

DELETE_ENDPOINT = "Delete item endpoint,"
DELETE_ENDPOINT_ERROR = "Delete item endpoint, error description: "

class DeleteEndpoint:
    logger: Logger
    delete_service: Service

    def __init__(self, delete_service: Service):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.delete_service = delete_service

    def delete(self, item_id: int, response: Response, version: str):
        self.logger.info(f'{DELETE_ENDPOINT} version: {version}')
        try:
            self.logger.info(f'{DELETE_ENDPOINT} item_id: {item_id}')
            self.delete_service.delete(item_id)
            self.logger.info(f'{DELETE_ENDPOINT} item with id {item_id} deleted successfully')
        except PermissionError as e:
            self.logger.error(f'{DELETE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        except Exception as e:
            self.logger.error(f'{DELETE_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code, description=e.description)
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return
