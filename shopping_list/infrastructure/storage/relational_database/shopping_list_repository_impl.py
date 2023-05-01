import json
import logging
from typing import List

from shopping_list.domain.model import ShoppingList
from shopping_list.domain.repository import ShoppingListRepository
from kit.orm.model import ShoppingList as DbShoppingList, Detail as DbDetail
from kit.orm.database import SessionLocal
from sqlalchemy.orm import Session
from logging import Logger
from kit.log.log import LOGGER_NAME
from shopping_list.domain.exc import PersistenceError

SHOPPING_LIST_REPOSITORY = "Shopping list repository,"
SHOPPING_LIST_REPOSITORY_ERROR = "Shopping list repository, error description: "


class ShoppingListRepositoryImpl(ShoppingListRepository):
    logger: Logger

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        super().__init__()

    def create(self, shopping_list: ShoppingList) -> ShoppingList:
        self.logger.info(f'{SHOPPING_LIST_REPOSITORY} creating shopping list: {shopping_list.name}')
        try:
            db: Session = SessionLocal()
            db_shopping_list = DbShoppingList(name=shopping_list.name)
            db.add(db_shopping_list)
            db.commit()
            db.refresh(db_shopping_list)
            self.logger.info(f'{SHOPPING_LIST_REPOSITORY} shopping list: {shopping_list.name} created successfully')
            return db_shopping_list.to_domain_shopping_list()
        except Exception as e:
            self.logger.error(f'{SHOPPING_LIST_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def delete(self, shopping_list_id: int) -> None:
        self.logger.info(f'{SHOPPING_LIST_REPOSITORY} deleting shopping list with id: {shopping_list_id}')
        try:
            db: Session = SessionLocal()
            db.query(DbDetail).where(DbDetail.shopping_list_id == shopping_list_id).delete(synchronize_session=False)
            db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list_id)
            self.logger.info(f'{SHOPPING_LIST_REPOSITORY} deleting shopping list: {db_shopping_list.name}')
            db.delete(db_shopping_list)
            db.commit()
            self.logger.info(
                f'{SHOPPING_LIST_REPOSITORY} shopping list with id: {shopping_list_id} deleted successfully')
            return
        except Exception as e:
            self.logger.error(f'{SHOPPING_LIST_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def update(self, shopping_list: ShoppingList) -> ShoppingList:
        self.logger.info(f'{SHOPPING_LIST_REPOSITORY} updating shopping list to: {json.dumps(shopping_list.dict())}')
        try:
            db: Session = SessionLocal()
            db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list.id)
            self.logger.info(
                f'{SHOPPING_LIST_REPOSITORY} shopping list to update, id: {db_shopping_list.id}, name: {db_shopping_list.name}')
            db_shopping_list.name = shopping_list.name
            db.commit()
            db.refresh(db_shopping_list)
            self.logger.info(
                f'{SHOPPING_LIST_REPOSITORY} shopping list: {json.dumps(shopping_list.dict())} updated successfully')
            return db_shopping_list.to_domain_shopping_list()
        except Exception as e:
            self.logger.error(f'{SHOPPING_LIST_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def find(self, shopping_list_id: int) -> ShoppingList | None:
        self.logger.info(f'{SHOPPING_LIST_REPOSITORY} finding shopping list with id: {shopping_list_id}')
        try:
            db: Session = SessionLocal()
            db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list_id)
            if db_shopping_list:
                shopping_list = db_shopping_list.to_domain_shopping_list()
                self.logger.info(
                    f'{SHOPPING_LIST_REPOSITORY} shopping list: {json.dumps(shopping_list.dict())} found successfully')
                return shopping_list
            self.logger.info(f'{SHOPPING_LIST_REPOSITORY} shopping list with id: {shopping_list_id} not found')
            return None

        except Exception as e:
            self.logger.error(f'{SHOPPING_LIST_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def find_all(self) -> List[ShoppingList]:
        self.logger.info(f'{SHOPPING_LIST_REPOSITORY} retrieving all shopping lists')
        try:
            db: Session = SessionLocal()
            result: List[ShoppingList] = []
            db_shopping_lists = db.query(DbShoppingList).offset(0).all()
            for db_shopping_list in db_shopping_lists:
                result.append(db_shopping_list.to_domain_shopping_list())
            return result
        except Exception as e:
            self.logger.error(f'{SHOPPING_LIST_REPOSITORY_ERROR} {e}')
            raise PersistenceError
