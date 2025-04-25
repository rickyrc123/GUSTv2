from pydantic import BaseModel
from typing import List

class DronePositionRequest(BaseModel):
    long: float
    lat: float
    alt: float
    bearing: float
    name: str = "test"
    model: str = "test"

    class Config:
        schema_extra = {
            "example": {
                "long"      : 12.1,
                "lat"       : 21.2,
                "alt"       : 10.2,
                "direction" : 2.1,
                "name"      : "example_drone",
                "model"     : "X100"
            }
        }

class PositionResponse(BaseModel):
    id: str
    longitude: float
    latitude: float
    altitude: float
    direction: float

    class Config:
        schema_extra = {
            "example": {
                "id": "12345",
                "longitude": 12.1,
                "latitude": 21.2,
                "altitude": 10.2,
                "direction": 2.1
            }
        }

class DroneCreateRequest(BaseModel):
    long: float
    lat: float
    alt: float
    bearing: float
    name: str = "test"
    model: str = "test"

    class Config:
        schema_extra = {
            "example": {
                "long"      : 12.1,
                "lat"       : 21.2,
                "alt"       : 10.2,
                "direction" : 2.1,
                "name"      : "example_drone",
                "model"     : "X100"
            }
        }

class MultiPositionResponse(BaseModel):
    id      : str
    data    : List[PositionResponse]