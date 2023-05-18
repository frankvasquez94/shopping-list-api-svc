from .item import Item
from shopping_list.item.operations.retrieve_all.service import Service
from shopping_list.item.operations.retrieve_all.dto import ItemDTO
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from shopping_list.domain.exc import PersistenceError
import logging
import json
from kit.log.log import LOGGER_NAME
from fastapi import status, Response
from shopping_list.infrastructure.rest.item.item import ItemResponse
from typing import List

GET_ALL_ENDPOINT = "Get all items endpoint"
GET_ALL_ENDPOINT_ERROR = "Get all items endpoint, error description: "


class GetAllEndpoint:
    logger: logging.Logger
    get_all_service: Service

    def __init__(self, get_all_service: Service):
        self.get_all_service = get_all_service
        self.logger = logging.getLogger(LOGGER_NAME)

    def get_all(self, response: Response, version: str, page_size: int, page_start_index: int) -> ItemResponse:
        self.logger.info(f'{GET_ALL_ENDPOINT} version: {version}, page size: {page_size}, page start index: {page_start_index}')
        try:
            self.logger.info(f'{GET_ALL_ENDPOINT}')
            resp: List[ItemDTO] = self.get_all_service.retrieve_all()
            item_response = self.__to_response_items(resp)
            self.logger.info(f'{GET_ALL_ENDPOINT} response: {str(json.dumps(item_response.dict()))}')
            return item_response
        except PersistenceError as e:
            self.logger.error(f'{GET_ALL_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code=e.code,
                                      description=e.description)
        except Exception as e:
            self.logger.error(f'{GET_ALL_ENDPOINT_ERROR} {e}')
            raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, code="001",
                                      description="internal server error")

    def __to_response_items(self, items: List[ItemDTO]) -> ItemResponse:
        items_response: List[Item] = []
        for item in items:
            item_response: Item = Item(id=item.id, name=item.name)
            items_response.append(item_response)
        return ItemResponse(items=items_response)
