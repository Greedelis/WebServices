# PC Parts List

## Launching app
App runs on port 5000, to run:
``` docker-compose up ```
App comunicates with another service, that runs on port 5001
(another service, that i used https://git.mif.vu.lt/arci4647/webhomework)
## Usage

### GET

**Get all parts**

```http://localhost:5000/api/parts ```

**Get specific part by id**

```http://localhost:5000/api/parts/<id> ```

**Response**
- On success - returns part/parts and status `200`
- On failure - status `404`

### POST

**Posting new part**

``` 
{
"manufacturer": "X",
"name": "Y",
"price": "Z",
"type": "D",
"phone" : "C"
}
```
It will create new part:
```
{"id": max_id+1,
"manufacturer": "X",
"name": "Y",
"type": "Z",
"price": "D",
"phone" : "C"
}
```
if put request dosent have one of manufaturer, name, price or type, web service will respond with error.

***Example***
```
{"manufacturer": "AMD",
 "name": "Ryzen 3 2200G",
 "price": "96.19",
 "type": "CPU",
 "phone": "1"
}
```

**Response**
- On success - Address to new part and status `201`
- On failure - status `400`

### DELETE

**Removing part by part id**

```http://localhost:5000/api/parts/<id> ```

**Response**
- On success - status `204`
- On failure - status `404`

### PUT

**Changing values of specific part**


```http://localhost:5000/api/parts/<id>```

You can change any value, by sending it as json, for example, to change <id> parts name, you need to send put request with:

```{"name": "new_name"}```

This will change <id> parts name to "new_name"

Same goes with manufacturer, price and type. You can change two or more fields at the same time. For example, chaging name and type of part, you need to send:

```
{ 
"name": "new_name", 
"type": "new_type"
}
```

**Response**
- On success - status `201`
- On failure - status `400`

**Cheking phone on specific part**

```http://localhost:5000/api/parts/<id>/phone```

### GET

**Response**
- On success - status `201` and returns info about phone
- On failure - status `400`
**Getting all phones**

### GET

**Posting phone**

```http://localhost:5000/api/phones ```

Response returns all phones

### POST

```http://localhost:5000/api/phones ```

```
{"brand": "A",
"model": "B",
"price": "C"
}
```

New phone will be created with auto generated ID
Responses
- 201 on success
- 404 on failure

**Getting/Adding Parts info with full phone info**

### GET

```http://localhost:5000/api/fullParts```

Response returns parts with full phone info

### POST

```
{
  "manufacturer": "A", 
  "name": "B", 
  "phone": {
    "brand": "C", 
    "model": "D", 
    "price": "E"
  }, 
  "price": "F", 
  "type": "G"
}```

Creates new part and new phone

- On success - Address to new part and phone and returns status `201`
- On failure - status `400`