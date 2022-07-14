from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse

import json
import requests
import io
import pyarrow as pa
import pandas as pd
import pyarrow.parquet as pq

from sql import models, crud, schemas
from sql.db import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}

    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.post('/lookup/', response_model=schemas.VehicleModel)
async def root(vin: schemas.VinModel, db: Session=Depends(get_db)):
    db_vehicle = crud.get_vehicle(db=db, vin=vin.vin)

    if db_vehicle:
        return db_vehicle
    
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin.vin}?format=json'
    r = requests.get(url)
    res = r.json()
    
    vehicle = schemas.VehicleModel(vin=res['Results'][0]['VIN'],
                                make=res['Results'][0]['Make'],
                                model=res['Results'][0]['Model'],
                                model_year=res['Results'][0]['ModelYear'],
                                body_class=res['Results'][0]['BodyClass'],
                                cached=True)
    
    return crud.create_vehicle(db=db, vehicle=vehicle)


@app.delete("/remove/", response_model=schemas.DeletionModel)
async def root(vin: schemas.VinModel, db: Session=Depends(get_db)):
    db_vehicle = crud.get_vehicle(db=db, vin=vin.vin)
    
    if db_vehicle:
        item = crud.delete_vehicle(db=db, vin=vin.vin)
        return schemas.DeletionModel(vin=item.vin, deleted=True)
    else:
        raise HTTPException(status_code=400, detail=f'VIN {vin.vin} does not exist')


@app.get("/export")
async def root(db: Session=Depends(get_db)):
    data = crud.get_all(db=db)
    # return data
    # table = pa.table({'n_legs': [2, 2, 4, 4, 5, 100], 'animal': ["Flamingo", "Parrot", "Dog", "Horse",  "Brittle stars", "Centipede"]})
    # pq.write_table(table, 'example.parquet')
    # parquet_file = pq.ParquetFile('example.parquet')
    # return FileResponse(parquet_file)
    # bytes_data = df.to_parquet()
    # buffer = io.BytesIO(bytes_data)
    # return StreamingResponse(buffer)
    df = pd.DataFrame([t.__dict__ for t in data], columns = ['vin', 'make', 'model', 'model_year', 'body_class'])
    df.to_parquet("vehicles.parquet")
    print(df.info())
    headers = {'Content-Disposition': 'attachment; filename="vehicles.parquet"'}
    return FileResponse("vehicles.parquet", headers=headers)
    



