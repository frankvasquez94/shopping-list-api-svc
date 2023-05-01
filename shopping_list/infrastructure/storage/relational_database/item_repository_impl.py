import json
import logging
import sqlite3
from typing import List

from sqlalchemy.exc import IntegrityError
from kit.orm.model import Item as DbItem
from shopping_list.domain.model import Item
from shopping_list.domain.repository import ItemRepository
from kit.orm.database import get_db, SessionLocal
from sqlalchemy.orm import Session
from shopping_list.domain.exc import ItemAlreadyExist, PersistenceError
from kit.log.log import LOGGER_NAME

ITEM_REPOSITORY = "Item repository,"
ITEM_REPOSITORY_ERROR = "Item repository, error description: "


class ItemRepositoryImpl(ItemRepository):

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        super().__init__()

    def create(self, item: Item) -> Item:
        self.logger.info(f'{ITEM_REPOSITORY} creating item with name: {item.name}')
        try:
            db: Session = SessionLocal()
            item_db = DbItem(name=item.name)
            db.add(item_db)
            db.commit()
            db.refresh(item_db)
            self.logger.info(f'{ITEM_REPOSITORY} item: {item.name} created successfully')
            return item_db.to_domain_item()
        except IntegrityError as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise ItemAlreadyExist
        except Exception as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def delete(self, item_id: int) -> None:
        self.logger.info(f'{ITEM_REPOSITORY} deleting item with id: {item_id}')
        try:
            db: Session = SessionLocal()
            item_db: DbItem = db.query(DbItem).get(item_id)
            db.delete(item_db)
            db.commit()
            self.logger.info(f'{ITEM_REPOSITORY} item with id: {item_id} deleted successfully')
            return
        except Exception as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def update(self, item: Item) -> Item:
        self.logger.info(f'{ITEM_REPOSITORY} updating item to {json.dumps(item.dict())}')
        try:
            db: Session = SessionLocal()
            item_db: DbItem = db.query(DbItem).get(item.id)
            self.logger.info(f'{ITEM_REPOSITORY} item to update id: {item_db.id}, name: {item_db.name}')
            item_db.name = item.name
            db.commit()
            db.refresh(item_db)
            self.logger.info(f'{ITEM_REPOSITORY} item {json.dumps(item.dict())} updated successfully')
            return item_db.to_domain_item()
        except IntegrityError as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise ItemAlreadyExist
        except Exception as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def find(self, item_id: int) -> Item | None:
        self.logger.info(f'{ITEM_REPOSITORY} finding item with id: {item_id}')
        try:
            db: Session = SessionLocal()
            item_db: DbItem = db.query(DbItem).get(item_id)
            if item_db:
                item = item_db.to_domain_item()
                self.logger.info(f'{ITEM_REPOSITORY} item found successfully: {item} ')
                return item
            self.logger.info(f'{ITEM_REPOSITORY} item not found, id: {item_id}')
            return None
        except Exception as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise PersistenceError

    def find_all(self) -> List[Item]:
        self.logger.info(f'{ITEM_REPOSITORY} getting all items')
        try:
            db: Session = SessionLocal()
            result: List[Item] = []

            items_db = db.query(DbItem).offset(0).all()
            for item_db in items_db:
                result.append(item_db.to_domain_item())
            return result
        except Exception as e:
            self.logger.error(f'{ITEM_REPOSITORY_ERROR} {e}')
            raise PersistenceError
