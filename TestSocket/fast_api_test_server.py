
import random
from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api_models import DronePositionRequest         as DronePositionRequest
from api_models import PositionResponse             as PositionResponse
from api_models import MultiPositionResponse        as ViewPosReponse

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
    inspector = inspect(engine)
    tables    = inspector.get_table_names() 

    #checks if new db to init the tables, is pretty bad
    if 'drones' not in tables:
        models.Base.metadata.drop_all(engine)
        models.Base.metadata.create_all(engine)

#initializes db tables on startup
@app.on_event("startup")
async def startup():
    build()


#does things, eventually...
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
async def get_all_drones():
    db = database.DatabaseServer()
    return {"Drones" : db.get_all_drones()}

@app.get("/drones/create") #change this to post
async def create_drone(
    lat      : float = 23.5, #pos may be removed for this part
    long     : float = 33.1,
    alt      : float = 23.2,
    bearing  : float = 33.1,
    name     : str = "test",
    model    : str = "TestDrone", # TODO : Make these enums 
):
    data = {
        'longitude' : long,
        'latitude'  : lat,
        'altitude'  : alt,
        'direction' : bearing,
        'model'     : model,
        'name'      : name
    }

    db = database.DatabaseServer()

    try:
        db.create_drone(drone = schemas.CreateDrone(**data))
    except:
        return {f"Status" : "500 - Failed to create drone with id {drone_id}"}
    
    return await get_all_drones()


@app.get("/drones/{drone_id}/view_position", 
         response_model=ViewPosReponse, 
         response_description = """
            Returns the last 50 positions of the drone_id given.
        """)
async def view_positions(drone_id : int):
    db = database.DatabaseServer()
    return db.get_positions_by_drone(drone_id=drone_id)


@app.get("/drones/{drone_id}/post_position", 
         response_model=PositionResponse,
         response_description = """
            Adds point to database and updates the drones last position.
            """)
async def add_drone_position(
    drone_id : int,
    position : DronePositionRequest 
):
    data = {
        "id"        : drone_id,
        "longitude" : position.long,
        "latitude"  : position.lat,
        "altitude"  : position.alt,
        "direction" : position.bearing
    }

    db = database.DatabaseServer()

    db.update_drone_table_position(drone_id=drone_id, **data)
    try:
        db.add_position(**data)
    except:
        return {"Failure" : "500 - Failed to add position"}
    
    #THIS IS WHERE THE MAGIC WILL HAPPEN

    return db.get_positions_by_drone(drone_id=drone_id)

#simply gives all the tables in the db, ensures it is properly setup
@app.get("/")
async def read_root():
    inspector = inspect(engine)
    return {"Page": inspector.get_table_names()}    