# Koffie Backend Challenge
> Implement a FastAPI backend to decode VINs. 

## Table of Contents
* [General Info](#general-information)
* [Setup](#setup)
* [Usage](#usage)


## General Information
Implement a simple FastAPI backend to decode VINs, powered by the vPIC API and backed by a SQLite cache.
Check whether or not a VIN is stored in the cache and if not, contact the vPIC API to get details about the vehicle and store it in the database.
Export a file containing all currently cached VINs in a table stored in parquet format.


## Setup
Run server with uvicorn main:app --reload
View Swagger UI at http://127.0.0.1:8000/docs
Run tests with pytest


## Usage

### Decode VIN
> This route will first check the SQLite database to see if a cached result is available. If so, it should be returned from the database. If not, your API should contact the vPIC API to decode the VIN, store the results in the database, and return the result.

#### Request

`POST /lookup/`

curl -X 'POST' \
  'http://127.0.0.1:8000/lookup/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "vin": "1XPWD40X1ED215307"
}'

#### Response

{
  "vin": "1XPWD40X1ED215307",
  "make": "PETERBILT",
  "model": "388",
  "model_year": "2014",
  "body_class": "Truck-Tractor",
  "cached": true
}

### Remove VIN
> This route will remove a entry from the cache. Return the input VIN and deletion success. 

#### Request

`POST /remove/`

curl -X 'POST' \
  'http://127.0.0.1:8000/remove/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "vin": "1XPWD40X1ED215307"
}'

#### Response

{
  "vin": "1XPWD40X1ED215307",
  "deleted": True
}


### Export parquet file
> This route will export the SQLite database cache and return a binary file (parquet format) containing the data in the cache.

#### Request

`POST /remove/`

curl -X 'GET' \
  'http://127.0.0.1:8000/export' \
  -H 'accept: application/json'

#### Response

Downloadable File
