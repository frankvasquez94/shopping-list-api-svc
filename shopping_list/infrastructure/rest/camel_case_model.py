from pydantic import BaseModel
from humps import camelize


def to_camel_case(string):
    return camelize(string)


# El standar de python define que los campos deben de ser snake_case
# al exportar estos modelos a json, nos encontramos que los campos siguen este modelo,
# sin embargo las buenas practicas de escribir una REST API nos dicta que los
# campos deben de ser camelCaae.
# Para resolverlo, manteniendo las buenas practicas de escribir codigo en python
# y escribir una REST API, se define este modelo base a partir del cual se puede
# heredar su comportamiento con el cual se pueden definir modelos usando snake_case
# y exportarlos a json usando camelCase.
# ejemplo:
# model
# class User(CamelCaseModel):
#     id: int
#     first_name: str
#     last_name: str
# json generado del modelo
#
# {
#    "id": 1,
#    "firstName": "John",
#	 "lastName": "Aguilar"
# }
class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
