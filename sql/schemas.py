from pydantic import BaseModel, validator


class VinModel(BaseModel):
    vin: str
    
    @validator('vin')
    def check_validity(cls, v):
        if not v.isalnum():
            raise ValueError('Invalid VIN: Must contain all alphanumeric characters')
        elif len(v) != 17:
            raise ValueError('Invalid VIN: Must be exactly 17 characters')
        return v


class VehicleModel(VinModel):
    make: str
    model: str
    model_year: str
    body_class: str
    cached: bool
    
    class Config:
        orm_mode = True
    
    
class DeletionModel(VinModel):
    deleted: bool