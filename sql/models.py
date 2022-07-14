from sqlalchemy import Column, String, Boolean

from sql.db import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    vin = Column(String(255), primary_key=True, index=True)
    make = Column(String(255))
    model = Column(String(255))
    model_year = Column(String(255))
    body_class = Column(String(255))
    cached = Column(Boolean)