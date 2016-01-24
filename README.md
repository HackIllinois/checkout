HackIllinois Equipment/Hardware Checkout API
============================================
## GET /items
Returns a list of items currently in the inventory with name, description, and the remaining quantity. For use with the Hardware overview screen.

### Authentication
None

### Parameters
None

### Sample Response
```json
{
  "items": [
    {
      "description": "Particle is a prototype-to-production platform for developing an Internet of Things product.",
      "name": "Particle Core",
      "quantity_left": 50
    },
    {
      [...]
    }
  ]
}
```

## GET /hacker/# (hacker-id)
Returns information about the hardware checked out by a specific hacker.

### Authentication
None

### Parameters
Hacker Barcode (ID) # in the URL

### Sample Response
```json
{
  "barcode": 783942,
  "id": 1,
  "items_checked_out": "472840"
}
```

## POST /items/new
Add equipment/hardware to the database. 

## Authentication
The following, encoded into the `form-data` of the POST request body:
```python
'secret': 'secret_key_here'
```

## Parameters
The following, encoded into the `form-data` of the POST request body:
```python
'name': 'item_name_here'
'description': 'description_here'
'quantity_left': '100'
'item_barcodes': '123456,789012,345678,901234,567890'
```

### Sample Response
```json
{
  "description": "Particle is a prototype-to-production platform for developing an Internet of Things product.",
  "id": 2,
  "item_barcodes": "123456,472840,584302,690325,863274,012843,958230",
  "name": "Particle Core",
  "quantity_left": 50
}
```

## POST /items/checkout
Check out an item for use by a hacker.

### Authentication
The following, encoded into the `form-data` of the POST request body:
```python
'secret': 'secret_key_here'
```

### Parameters
The following, encoded into the `form-data` of the POST request body:
```python
'item_barcode': '123456'
'hacker_barcode': '123456'
```

### Sample Response
```json
{
  "info": [
    {
      "barcode": 783944,
      "id": 2,
      "items_checked_out": "472840472840,"
    },
    {
      "description": "Particle is a prototype-to-production platform for developing an Internet of Things product.",
      "id": 2,
      "item_barcodes": "123456,472840,584302,690325,863274,012843,958230",
      "name": "Particle Core",
      "quantity_left": 49
    }
  ]
}
```

## POST /items/return
Return an item that a hacker was using

### Authentication
The following, encoded into the `form-data` of the POST request body:
```python
'secret': 'secret_key_here'
```

### Parameters
The following, encoded into the `form-data` of the POST request body:
```python
'item_barcode': '123456'
'hacker_barcode': '123456'
```

### Sample Response
```json
{
  "barcode": 783945,
  "id": 3,
  "items_checked_out": ""
}
```