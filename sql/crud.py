from sqlalchemy.orm import Session
from sql import schemas, models


def create_vehicle(db: Session, vehicle: schemas. VehicleModel):
    db_vehicle = models.Vehicle(vin=vehicle.vin,
                                make=vehicle.make,
                                model=vehicle.model,
                                model_year=vehicle.model_year,
                                body_class=vehicle.body_class,
                                cached=vehicle.cached)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def get_vehicle(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin==vin).first()


def get_all(db: Session):
    return db.query(models.Vehicle).all()


def delete_vehicle(db: Session, vin: str):
    item = get_vehicle(db=db, vin=vin)
    db.delete(item)
    db.commit()
    return item