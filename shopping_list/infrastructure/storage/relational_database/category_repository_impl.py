from typing import List
from shopping_list.domain.model import Category
from shopping_list.domain.repository import CategoryRepository
from kit.orm.database import get_db, SessionLocal
from kit.orm.model import Category as DbCategory
from sqlalchemy.orm import Session


class CategoryRepositoryImpl(CategoryRepository):
    def create(self, category: Category) -> Category:
        db: Session = SessionLocal()
        db_category = DbCategory(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        db_category.to_domain_category()

    def delete(self, category_id: int) -> None:
        db: Session = SessionLocal()
        db_category = db.query(DbCategory).get(category_id)
        db.delete(db_category)
        db.commit
        return

    def update(self, category: Category) -> Category:
        db: Session = SessionLocal()
        db_category = db.query(DbCategory).get(category.id)
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
        return db_category.to_domain_category()

    def find(self, category_id: int) -> Category:
        db: Session = SessionLocal()

        db_category = db.query(DbCategory).get(category_id)
        return db_category.to_domain_category()

    def find_all(self) -> List[Category]:
        result: List[Category] = []
        db: Session = SessionLocal()

        categories_db = db.query(DbCategory).offset(0).all()
        for category_db in categories_db:
            result.append(category_db.to_domain_category())
        return result
