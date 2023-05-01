from .database import Base
from sqlalchemy import Integer, String, Column, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from shopping_list.domain.model import Item as DomainItem
from shopping_list.domain.model import Category as DomainCategory
from shopping_list.domain.model import Measure as DomainMeasure
from shopping_list.domain.model import ShoppingList as DomainShoppingList



class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    id = Column(Integer, primary_key=True, index=True, name="id", autoincrement=True)
    name = Column(String(length=100), name="name")
    item_details: Mapped[List["Detail"]] = relationship(back_populates="shopping_list")

    def to_domain_shopping_list(self) -> DomainShoppingList:
        domain_shopping_list = DomainShoppingList(id=self.id, name=self.name)
        return domain_shopping_list


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, index=True, primary_key=True, name="id", autoincrement=True)
    name = Column(String(length=250), name="name", unique=True)
    item_details: Mapped[List["Detail"]] = relationship(back_populates="item")

    # Devuelve el Item del dominio
    def to_domain_item(self) -> DomainItem:
        domain_item = DomainItem(id=self.id, name=self.name)
        return domain_item


class Measure(Base):
    __tablename__ = "measures"

    id = Column(Integer, index=True, primary_key=True, name="id", autoincrement=True)
    name = Column(String(length=25), name="name")
    item_details: Mapped[List["Detail"]] = relationship(back_populates="measure")

    def to_domain_measure(self) -> DomainMeasure:
        domain_measure = DomainMeasure(id=self.id, name=self.name)
        return domain_measure


class Category(Base):
    __tablename__ = "categories"

    # Usamos otra notacion
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, name="id", autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), name="name")
    # id = Column(Integer, index=True, primary_key=True, name="id")
    # name = Column(String(length=100), name="name")

    item_details: Mapped[List["Detail"]] = relationship(back_populates="category")

    def to_domain_category(self) -> DomainCategory:
        domain_category = DomainCategory(id=self.id, name=self.name)
        return domain_category


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, index=True, primary_key=True, name="id", autoincrement=True)
    quantity = Column(Integer, name="quantity")
    price = Column(Float, name="price")
    checked = Column(Boolean, name="checked", default=False)
    comment = Column(String, name="comment")
    # ShoppingList relationship
    shopping_list_id: Mapped[int] = mapped_column(Integer, ForeignKey("shopping_lists.id"), name="shopping_list_is")
    shopping_list: Mapped["ShoppingList"] = relationship(back_populates="item_details")
    # Item relationship
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"), name="item_id")
    item: Mapped["Item"] = relationship(back_populates="item_details")
    ## Measure relationship
    measure_id: Mapped[int] = mapped_column(Integer, ForeignKey("measures.id"), name="measure_id")
    measure: Mapped["Measure"] = relationship(back_populates="item_details")
    ## category relationship
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), name="category_id")
    category: Mapped["Category"] = relationship(back_populates="item_details")
