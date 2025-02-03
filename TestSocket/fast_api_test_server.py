
import random
from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db import models
from db import schemas
from db import database

#db tables

DRONE_TABLE = "drones"

# fake drone list
DRONE_IDS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]

#states?
STATES = {
   -1 : "UNKNOWN",
    1 : "f",
    2 : "a",
    3 : " ",
    4 : "",
    5 : "",
    6 : "",
    7 : ""
}

#the app
app = FastAPI()

engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/postgres')

def build():
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

#initializes db tables on startup
@app.on_event("startup")
async def startup():
    build()


#saves db on shutdown
@app.on_event("shutdown")

#sending stuff with the API
@app.get("/test_data/get_generated_data")
async def generate_data():
    position_array = []
    num_positions = None

    #if no range specified, make it random
    if num_positions is None: 
        num_positions = random.randint(1,25)

    for _ in range(0, num_positions):

        # random position coordinates, longitude, latitude, and Altitude
        rand_long  =  random.uniform( -180,  180 )
        rand_lat   =  random.uniform(  -90,  90  )
        rand_alt   =  random.uniform(    0,  50  )
        rand_dir   =  random.uniform(    0,  360 )
 
        position_array.append({
           "long"           : rand_long, 
           "lat"            : rand_lat,
           "alt_meters"     : rand_alt,
           "direction"      : rand_dir
        })
    
    # convert to json payload
    # websocket messages must be btyes or strings

    payload = {
        "coordinates" : position_array,
        "drone_id"    : random.choice(DRONE_IDS),
        "message"     : "WARNING!: This is randomly generated data!"
    }

    return payload

@app.get("/drones")
async def post_drone_position():

    drone_id : int = 1,
    lat      : float = 23.5,
    long     : float = 33.1,
    alt      : float = 23.2,
    name     : str = "test",
    bearing  : float = 33.1,
    model    : str = "test", # TODO : Make these enums 
    state    : int = 0 #  here too

    data = {
        'longitude' : 32,
        'latitude'  : 32,
        'altitude'  : 12,
        'direction' : 11,
        'model'     : models.DroneModels.model1

    }

    db = database.DatabaseServer()
    db.create_drone(drone = schemas.CreateDrone(**data))

    return {"Page" : db.get_all_drones()}

@app.get("/")
async def read_root():
    inspector = inspect(engine)
    return {"Page": inspector.get_table_names()}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}