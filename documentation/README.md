# Documentation

This folder contains extra documentation like source files with diagrams, images, etc.

## Diagrams

Diagrams are in the file shopping-list-api-svc.simp, this project was created by using [software ideas modeler](https://www.softwareideas.net/).

## Class diagram

![Class diagram](/images/ClassDiagram.png "Class Diagram")

## API Design

This section contains API specification design. It is important that this is base on the following guide [REST API bestpractices](https://github.com/frankvasquez94/REST-API-best-practices).

The practices bellow are aplicable to all endpoints:

- application/json media type is supported by default.
- The *version* header is used for versioning. The default version is 1.0.

Each endpoint specification has the following format:

```text
{HTTP Method} {base path} {http response code} 
```

for example, to persist a new category:

```text
POST /categories 201
```

### Category design

#### Base path

```text
/categories
```

#### Persist a category

```text
POST /categories [201]
```

##### Request body

```json
{
  "name": "food"
}
```

##### Response

```json
{
  "id": 1,
  "name": "food"
}
```

#### Retrieve all categories

```text
GET /categories [200]
```

##### Headers

```text
pagesize: 0 by default
pagestartindex: 0 by deafult
```

##### Response

```json
{
  "categories": [
    {
      "id": 1,
      "name": "food"
    },
    {
      "id": 2,
      "name": "drinks"
    }
  ]
}
```

#### Retrieve a specific category

```text
GET /categories/{categoryID} [200]
```

##### Response

```json
{
  "id": 1,
  "name": "food"
}
```

#### Update a category

```text
PUT /categories/{categoryID}  [200]
```

##### Request body

```json
{
  "name": "food updated"
}
```

##### Response

```json
{
  "id": 1,
  "name": "food updated"
}
```

#### Delete a category

```text
DELETE /categories/{categoryID}  [204]
```


### measure design

#### Base path

```text
/measures
```

#### Persist a measure

```text
POST /measures [201]
```

##### Request body

```json
{
  "name": "unit"
}
```

##### Response

```json
{
  "id": 1,
  "name": "unit"
}
```

#### Retrieve all measures

```text
GET /measures [200]
```

##### Headers

```text
pagesize: 0 by default
pagestartindex: 0 by deafult
```

##### Response

```json
{
  "measures": [
    {
      "id": 1,
      "name": "unit"
    },
    {
      "id": 2,
      "name": "pkg"
    }
  ]
}
```

#### Retrieve a specific measure

```text
GET /measures/{measureID} [200]
```

##### Response

```json
{
  "id": 1,
  "name": "unit"
}
```

#### Update a measure

```text
PUT /measures/{measureID}  [200]
```

##### Request body

```json
{
  "name": "unit updated"
}
```

##### Response

```json
{
  "id": 1,
  "name": "unit updated"
}
```

#### Delete a measure

```text
DELETE /measures/{measureID}  [204]
```

### item design

#### Base path

```text
/items
```

#### Persist an item

```text
POST /items [201]
```

##### Request body

```json
{
  "name": "meat"
}
```

##### Response

```json
{
  "id": 1,
  "name": "meat"
}
```

#### Retrieve all items

```text
GET /items [200]
```

##### Headers

```text
pagesize: 0 by default
pagestartindex: 0 by deafult
```

##### Response

```json
{
  "items": [
    {
      "id": 1,
      "name": "meat"
    },
    {
      "id": 2,
      "name": "water"
    }
  ]
}
```

#### Retrieve a specific item

```text
GET /items/{itemID} [200]
```

##### Response

```json
{
  "id": 1,
  "name": "meat"
}
```

#### Update an item

```text
PUT /items/{itemID}  [200]
```

##### Request body

```json
{
  "name": "meat updated"
}
```

##### Response

```json
{
  "id": 1,
  "name": "meat updated"
}
```

#### Delete an item

```text
DELETE /items/{itemID}  [204]
```

### shopping lists design

#### Base path

```text
/shopping-lists
```

#### Persist an shopping-lists

```text
POST /shopping-lists [201]
```

##### Request body

```json
{
  "name": "my shopping list"
}
```

##### Response

```json
{
  "id": 1,
  "name": "my shopping list"
}
```

#### Retrieve all shopping-lists

```text
GET /shopping-lists [200]
```

##### Headers

```text
pagesize: 0 by default
pagestartindex: 0 by deafult
```

##### Response

```json
{
  "shopping-lists": [
    {
      "id": 1,
      "name": "my shopping list"
    },
    {
      "id": 2,
      "name": "birthday shopping list"
    }
  ]
}
```

#### Retrieve a specific shopping-list

```text
GET /shopping-lists/{shoppingListID} [200]
```

##### Response

```json
{
  "id": 1,
  "name": "my shopping list"
}
```

#### Update a shopping-lists

```text
PUT /shopping-lists/{shoppingListID}  [200]
```

##### Request body

```json
{
  "name": "my shopping list updated"
}
```

##### Response

```json
{
  "id": 1,
  "name": "my shopping list updated"
}
```

#### Delete a shopping-lists

```text
DELETE /shopping-lists/{shoppingListID}  [204]
```

### item details design

#### Base path

```text
/shopping-lists/{shoppingListID}/items/{shoppingListID}/items
```

#### Add a shopping list item

If an item id is provided, an existing item will be added to the shopping list, if not an item with the given name will be created and added.

```text
POST /shopping-lists/{shoppingListID}/items [201]
```

##### Request body

```json
{
  "id": 1,
  "name": "meat"
}
```

##### Response

```json
{
  "shoppingListId": 1,
  "itemId": 1,
  "name": "meat"
}
```

#### Retrieve all item details

```text
GET /shopping-lists/{shoppingListID}/items [200]
```

##### Headers

```text
pagesize: 0 by default
pagestartindex: 0 by deafult
```

##### Response

```json
{
  "id": 1,
  "name": "my shopping list",
  "items": [
    {
      "id": 1,
      "name": "meat",
      "category": "food",
      "measure": "lbs",
      "total": 20.00,
      "quantity": "2",
      "price": 10.00,
      "checked": false
    },
    {
      "id": 2,
      "name": "chicken",
      "category": "food",
      "measure": "lbs",
      "total": 10.00,
      "quantity": "4",
      "price": 2.50,
      "checked": true
    }
  ],
  "total": 30.00,
  "checkedTotal": 10.00,
  "uncheckedTotal": 20.00
}
```

#### Retrieve a specific item details

```text
GET /shopping-lists/{shoppingListID}/items/{itemID} [200]
```

##### Response

```json
{
  "shoppingListId": 1,
  "itemId": 1,
  "name": "meat",
  "category": {
    "id": 1,
    "name": "food"
  },
  "measure": {
    "id": 1,
    "name": "lbs"
  },
  "total": 20.00,
  "quantity": "2",
  "price": 10.00,
  "checked": false
}
```

#### Update a shopping-lists

```text
PUT /shopping-lists/{shoppingListID}/items/{itemID}  [200]
```

##### Request body

```json
{  
  "name": "meat",
  "category": {
    "id": 1,
    "name": "food"
  },
  "measure": {
    "id": 1,
    "name": "lbs"
  },
  "total": 20.00,
  "quantity": "2",
  "price": 10.00  
}
```

##### Response

```json
{
  "shoppingListId": 1,
  "itemId": 1,
  "name": "meat",
  "category": {
    "id": 1,
    "name": "food"
  },
  "measure": {
    "id": 1,
    "name": "lbs"
  },
  "total": 20.00,
  "quantity": "2",
  "price": 10.00  
}
```

#### Delete an item details

```text
DELETE /shopping-lists/{shoppingListID}/items/{itemID}  [204]
```


#### Check/ uncheck item details controller

```text
POST /shopping-lists/{shoppingListID}/items/{itemID} [200]
```

##### Request body

```json
{  
  "checked": true
}
```

##### Response

```json
{
  "shoppingListId": 1,
  "itemId": 1,
  "checked": true
}
```


### error design

#### Simple error

```json
{
  "code": "33",
  "description": "an error has occurred"
}
```

#### Multiple errors

If an error list is necessary.

```json
{
  "errors": [
    {
      "code": "33",
      "description": "an error has occurred"
    },
    {
      "code": "34",
      "description": "this field should have at least three characters"
    }
  ]
}
```
