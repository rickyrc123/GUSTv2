
import random
from typing import Union
import db.database
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymavlink import mavutil

from api_models import DronePositionRequest         as DronePositionRequest
from api_models import PositionResponse             as PositionResponse
from api_models import MultiPositionResponse        as ViewPosReponse
from api_models import DroneCreateRequest           as DroneCreate

from db import models
from db import schemas
from db import database

from db.database import DatabaseServer

import db

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

#the data
db = DatabaseServer

engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/postgres')



def _mavlink_init():
    # Connect to ArduPilot SITL
    master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    print("waiting for heartbeat")
    master.wait_heartbeat()
    print("Heartbeat received!")
    return master

#initializes db tables on startup
@app.on_event("startup")
async def startup():
    print("starting up")
    ## ESTABLISH MAVLINK CONNECTION
    


#does things, eventually...
@app.on_event("shutdown")
async def shutdown():
    #do stuff 
    print("Shutting down")
#sending stuff with the API
#DEPRECIATED
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

@app.post("/drones/create")
async def create_drone(
    drone : schemas.Drone
):
    db = database.DatabaseServer()

    try:
        db.create_drone(drone=drone)
    except Exception as e:
        return {"Status" : f"db.create_drone failed! \n\n\n {e}"} 
    
    return {"Status" : "Success!"}

@app.post("/drones/{drone_name}/delete")
async def delete_drone(drone_name : str):
    db = database.DatabaseServer()
    db.delete_drone_by_name(name=drone_name)

    return {"Status" : "Success!"}


@app.get("/drones/positions", 
         response_model=ViewPosReponse, 
         response_description = """
            Returns the last 50 positions of the drone_id given.
        """)
async def view_positions(drone_id : int):
    db = database.DatabaseServer()
    return {"Positions" : db.get_drone_position_history()} 


@app.post("/drones/{drone_id}/post_position", 
         response_description = """
            Adds point to database and updates the drones last position.
         """
)
async def add_drone_position(
    position : schemas.Waypoint 
):
    db = database.DatabaseServer()

    try:
        db.add_position(position)
    except Exception as e:
        return {"Failure" : f"db.add_position failed \n\n\n {e}"}
    
    #THIS IS WHERE THE MAGIC WILL HAPPEN

    return {"Status" : "Success"}

#simply gives all the tables in the db, ensures it is properly setup
@app.get("/")
async def read_root():
    inspector = inspect(engine)
    return {"Page": inspector.get_table_names()}    