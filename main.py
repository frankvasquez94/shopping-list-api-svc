from fastapi import FastAPI, Request, Body, Response, Header
from fastapi.responses import JSONResponse
from kit.orm.model import Base
from kit.orm.database import engine
from shopping_list.infrastructure.storage.relational_database.item_repository_impl import ItemRepositoryImpl
from shopping_list.item.operations.add.service import Service as AddItemService
from shopping_list.infrastructure.rest.item.add_endpoint import AddEndpoint as AddItemEndpoint
from shopping_list.infrastructure.rest.item.item import Item
from shopping_list.infrastructure.rest.custom_http_exception import CustomHttpException
from fastapi.middleware.cors import CORSMiddleware
from shopping_list.item.operations.update.service import Service as UpdateItemService
from shopping_list.infrastructure.rest.item.update_endpoint import UpdateEndpoint as UpdateItemEndpoint
import yaml
import kit.log.log as log
from typing import Annotated
from shopping_list.domain import model
from pydantic import ValidationError
from shopping_list.item.operations.retrieve.service import Service as RetrieveItemService
from shopping_list.infrastructure.rest.item.get_endpoint import GetEndpoint as GetItemEndpoint
from shopping_list.item.operations.delete.service import Service as DeleteItemService
from shopping_list.infrastructure.rest.item.delete import DeleteEndpoint as DeleteItemEndpoint
from shopping_list.item.operations.retrieve_all.service import Service as RetrieveAllItemsService
from shopping_list.infrastructure.rest.item.get_all_endpoint import GetAllEndpoint as GetAllItemsEndpoint

from shopping_list.infrastructure.storage.relational_database.shopping_list_repository_impl import ShoppingListRepositoryImpl
from shopping_list.shopping_list.operations.add.service import Service as AddShoppingListService
from shopping_list.infrastructure.rest.shopping_list.add_endpoint import AddEndpoint as AddShoppingListEndpoint
from shopping_list.infrastructure.rest.shopping_list.shopping_list import ShoppingList, ShoppingListResponse

from shopping_list.shopping_list.operations.delete.service import Service as DeleteShoppingListService
from shopping_list.infrastructure.rest.shopping_list.delete_endpoint import DeleteEndpoint as DeleteShoppingListEndpoint

from shopping_list.shopping_list.operations.update.service import Service as UpdateShoppingListService
from shopping_list.infrastructure.rest.shopping_list.update_endpoint import UpdateEndpoint as UpdateShoppingListEndpoint

from shopping_list.shopping_list.operations.retrieve.service import Service as RetrieveShoppingListService
from shopping_list.infrastructure.rest.shopping_list.get_endpoint import GetEndpoint as GetShoppingListEndpoint


from shopping_list.shopping_list.operations.retrieve_all.service import Service as RetrieveAllShoppingListService
from shopping_list.infrastructure.rest.shopping_list.get_all_endpoint import GetAllEndpoint as GetAllShoppingListEndpoint




# Inicializamos el logger
log.init()

# yaml configs
file = open('application-local.yml', 'r')
config = yaml.load(file, Loader=yaml.FullLoader)

# Se encarga de inicializar la base de datos.
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ============= exception handler ==========================

# Define la representacion json del error
# {
#      "code": "001",
#      "description": "an error has occurred"
# }
@app.exception_handler(CustomHttpException)
def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "description": exc.description},
    )


# =======================================================

# ============= CORS ==========================


app.add_middleware(
    CORSMiddleware,
    allow_origins=config["cors"]["allow_origins"],
    allow_credentials=config["cors"]["allow_credentials"],
    allow_methods=config["cors"]["allow_methods"],
    allow_headers=config["cors"]["allow_headers"],
)
# ["*"] -> wildcard for all http methods, header and origins

# =============================================


item_repository_impl = ItemRepositoryImpl()
add_item_service = AddItemService(item_repository=item_repository_impl)
add_item_endpoint = AddItemEndpoint(add_service=add_item_service)


@app.get("/")
def home(response: Response, version: Annotated[str | None, Header()] = 1.0):
    return {
        "version": version,
        "description": "Welcome to shopping list API"
    }

@app.post("/items")
def add_item(item: Annotated[Item, Body(example={"name": "Desktop"})], response: Response, version: Annotated[str | None, Header()] = 1.0) -> Item:
    return add_item_endpoint.add(item, response, version)


update_item_service = UpdateItemService(item_repository=item_repository_impl)
update_item_endpoint = UpdateItemEndpoint(update_service=update_item_service)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Annotated[Item, Body(example={"name": "Desktop"})], response: Response, version: Annotated[str | None, Header()] = 1.0) -> Item:
    item.id = item_id
    return update_item_endpoint.update(item, response, version)


get_item_service = RetrieveItemService(item_repository=item_repository_impl)
get_item_endpoint = GetItemEndpoint(get_service=get_item_service)


@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response, version: Annotated[str | None, Header()] = 1.0) -> Item:
    return get_item_endpoint.get(item_id, response, version)


delete_item_service = DeleteItemService(item_repository=item_repository_impl)
delete_item_endpoint = DeleteItemEndpoint(delete_service=delete_item_service)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, response: Response, version: Annotated[str | None, Header()] = 1.0):
    return delete_item_endpoint.delete(item_id=item_id, response=response, version=version)


get_all_items_service = RetrieveAllItemsService(item_repository=item_repository_impl)
get_all_items_endpoint = GetAllItemsEndpoint(get_all_service=get_all_items_service)


@app.get("/items")
def get_all_items(response: Response, version: Annotated[str | None, Header()] = 1.0, pagesize: int = 0, pagestartindex: int = 0):
    return get_all_items_endpoint.get_all(response, version, pagesize, pagestartindex)


# SHOPPING LIST

shopping_list_repository = ShoppingListRepositoryImpl()
add_shopping_list_service = AddShoppingListService(shopping_list_repository=shopping_list_repository)
add_shopping_list_endpoint = AddShoppingListEndpoint(add_shopping_list_service=add_shopping_list_service)


@app.post("/shopping-lists")
def add_shopping_list(shopping_list: Annotated[ShoppingList, Body(example={"name": "Celebration shopping list"})], response: Response, version: Annotated[str | None, Header()] = 1.0) -> ShoppingList:
    return add_shopping_list_endpoint.add(shopping_list_request=shopping_list, response=response, version=version)


delete_shopping_list_service = DeleteShoppingListService(shopping_list_repository=shopping_list_repository)
delete_shopping_list_endpoint = DeleteShoppingListEndpoint(delete_service=delete_shopping_list_service)


@app.delete("/shopping-lists/{shopping_list_id}")
def delete_shopping_list(shopping_list_id: int, response: Response, version: Annotated[str | None, Header()] = 1.0) -> None:
    return delete_shopping_list_endpoint.delete(shopping_list_id, response, version)


update_shopping_list_service = UpdateShoppingListService(shopping_list_repository=shopping_list_repository)
update_shopping_list_endpoint = UpdateShoppingListEndpoint(update_service=update_shopping_list_service)

@app.put("/shopping-lists/{shopping_list_id}")
def update_shopping_list(shopping_list_id: int, shopping_list: Annotated[ShoppingList, Body(example={"name": "Celebration shopping list updated"})], response: Response, version: Annotated[str | None, Header()] = 1.0) -> ShoppingList:
    shopping_list.id = shopping_list_id
    return update_shopping_list_endpoint.update(shopping_list, response, version)


get_shopping_list_service = RetrieveShoppingListService(shopping_list_repository=shopping_list_repository)
get_shopping_list_endpoint = GetShoppingListEndpoint(get_service=get_shopping_list_service)


@app.get("/shopping-lists/{shopping_list_id}")
def get_shopping_list(shopping_list_id: int, response: Response, version: Annotated[str | None, Header()] = 1.0) -> ShoppingList:
    return get_shopping_list_endpoint.get(shopping_list_id, response, version)



get_all_shopping_list_service = RetrieveAllShoppingListService(shopping_list_repository=shopping_list_repository)
get_all_shopping_list_endpoint = GetAllShoppingListEndpoint(get_all_service=get_all_shopping_list_service)
@app.get("/shopping-lists")
def get_shopping_list(response: Response, version: Annotated[str | None, Header()] = 1.0, pagesize: int = 0, pagestartindex: int = 0) -> ShoppingListResponse:

    return get_all_shopping_list_endpoint.get_all(response, version, pagesize, pagestartindex)





# Test del dominio

kg_measure = model.Measure(id=1, name="kg")
pkg_measure = model.Measure(id=2, name="pkg")
unit_measure = model.Measure(id=3, name="unit")
# print("==================== measures ===============")
# print(kg_measure)
# print(pkg_measure)


general_category = model.Category(id=1, name="general")
electronic_category = model.Category(id=2, name="electronic")

# print("================ categories ================")
# print(general_category)
# print(electronic_category)


laptop_item = model.Item(id=1, name="HP laptop")
pencil_item = model.Item(id=1, name="pencil")
rice_item = model.Item(id=1, name="rice")

# print(laptop_item)
# print(pencil_item)
# print(rice_item)

shopping_list = model.ShoppingList(id=1, name="april shopping list")

# print("=========== item details =============")

laptop_item_details = model.Detail(id=1, measure=unit_measure, category=electronic_category, item=laptop_item)
laptop_item_details.quantity = 2
laptop_item_details.price = 500.00

pencil_item_details = model.Detail(id=2, measure=pkg_measure, category=general_category, item=pencil_item)
pencil_item_details.quantity = 5
pencil_item_details.price = 5.50
pencil_item_details.checked = True
#
rice_item_details = model.Detail(id=3, measure=unit_measure, category=general_category, item=rice_item)
try:
    rice_item_details.quantity = -25
except ValidationError as e:
    print("Errores")
    for err in e.errors():
        print(f'Field {err["loc"][0]}')
        print(f'Error description {err["msg"]}')
    print(e.errors())

rice_item_details.price = 0.60
#
# print("=========== shopping list =============")
#
shopping_list.add_item_detail(laptop_item_details)
shopping_list.add_item_detail(pencil_item_details)
shopping_list.add_item_detail(rice_item_details)
#
# print(shopping_list)
#
for item_detail in shopping_list.item_details:
    print("========= ", item_detail.item.name, " =========")
    print("quantity: ", item_detail.quantity)
    print("price: ", item_detail.price)
    print("measure: ", item_detail.measure.name)
    print("category: ", item_detail.category.name)
    print("Checked: ", item_detail.checked)
    print("Sub total: ", item_detail.get_total())
#
# print()
print("Total: ", shopping_list.get_total())
print("Checked total: ", shopping_list.get_checked_total())
print("Unchecked total: ", shopping_list.get_unchecked_total())

# item_repo = ItemRepositoryImpl()
# test_item = model.Item(name="HP laptop")
# resp = item_repo.create(test_item)
# print("ITEM FROM DATABASE")
# print(resp.id)
# print(resp.name)
#
#
# print("Listar todos los items")
# print(item_repo.find_all())
