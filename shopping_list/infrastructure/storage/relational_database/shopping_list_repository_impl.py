from typing import List

from shopping_list.domain.model import ShoppingList
from shopping_list.domain.repository import ShoppingListRepository
from kit.orm.model import ShoppingList as DbShoppingList, Detail as DbDetail
from kit.orm.database import SessionLocal
from sqlalchemy.orm import Session

class ShoppingListRepositoryImpl(ShoppingListRepository):

    def create(self, shopping_list: ShoppingList) -> ShoppingList:
        db: Session = SessionLocal()
        db_shopping_list = DbShoppingList(name=shopping_list.name)
        db.add(db_shopping_list)
        db.commit()
        db.refresh(db_shopping_list)
        return db_shopping_list.to_domain_shopping_list()

    def delete(self, shopping_list_id: int) -> None:
        db: Session = SessionLocal()
        db.query(DbDetail).where(DbDetail.shopping_list_id == shopping_list_id).delete(synchronize_session=False)
        db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list_id)
        db.delete(db_shopping_list)
        db.commit()
        return

    def update(self, shopping_list: ShoppingList) -> ShoppingList:
        db: Session = SessionLocal()
        db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list.id)
        db_shopping_list.name = shopping_list.name
        db.commit()
        db.refresh(db_shopping_list)
        return db_shopping_list.to_domain_shopping_list()

    def find(self, shopping_list_id: int) -> ShoppingList:
        db: Session = SessionLocal()
        db_shopping_list: DbShoppingList = db.query(DbShoppingList).get(shopping_list_id)
        return db_shopping_list.to_domain_shopping_list()

    def find_all(self) -> List[ShoppingList]:
        db: Session = SessionLocal()
        result: List[ShoppingList] = []
        db_shopping_lists = db.query(DbShoppingList).offset(0).all()
        for db_shopping_list in db_shopping_lists:
            result.append(db_shopping_list.to_domain_shopping_list())
        return result
