
import random
from typing import Union
import db.database
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from pymavlink import mavutil

from api_models import DronePositionRequest         as DronePositionRequest
from api_models import PositionResponse             as PositionResponse
from api_models import MultiPositionResponse        as ViewPosReponse
from api_models import DroneCreateRequest           as DroneCreate

import dragon_link

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
    3 : "",
    4 : "",
    5 : "",
    6 : "",
    7 : ""
}

#the app
app = FastAPI()

##TODO ADD VALIDATION
origins = [
        "http://localhost:8000",
        "http://localhost:5173"
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/postgres')

database = db.DatabaseServer()

# Hashmap of drones
drone_dict = {}

def _mavlink_init():
    # Connect to ArduPilot SITL
    master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    print("waiting for heartbeat")
    master.wait_heartbeat()
    print("Heartbeat received!")
    return master

THREADS = []
#initializes db tables on startup
@app.on_event("startup")
async def startup():
    db.build()
    drone_list = database.get_all_drones()
    for drone in drone_list:
        drone_dict[drone.name] = drone
    print("starting up")

    ## CHECK UDP CONNECTION

    ## SCAN UDP FOR OPEN PORTS

        ## CREATE CONNECTIONS TO EACH PORT

        ## GET INFORMATION FROM DB

            ## IF NONE FOUND, ADD AVAILABLE INFORMATION
    
    ## AWAIT ACTIVATION
    ## CREATE THREADS FOR EACH ACTIVE DRONE ON ACTIVATION

    


## UPDATES DRONE INFORMATION IN THE DB, LAST_POS, ETC....
@app.on_event("shutdown")
async def shutdown():
    for _, drone in drone_dict.items():
        database.update_drone_info(drone=drone)
        database.update_drone_location(drone=drone)
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
    # websocket messages must be bytes or strings

    payload = {
        "coordinates" : position_array,
        "drone_id"    : random.choice(DRONE_IDS),
        "message"     : "WARNING!: This is randomly generated data!"
    }

    return payload

@app.get("/drones")
async def get_all_drones():
    return {"Drones" : list(drone_dict.values())}

@app.post("/drones/create") #change this to post
async def create_drone(
    drone : db.Drone
):
    try:
        database.create_drone(drone=drone)
    except Exception as e:
        return {"Status" : f"db.create_drone failed! \n\n\n {e}"} 
    
    drone_dict[drone.name] = drone
    return {"Status" : "Success!"}


@app.post("/drones/{drone_name}/delete")
async def delete_drone(drone_name : str):
    database.delete_drone(drone=drone_dict[drone_name])
    
    del drone_dict[drone_name]

    return {"Status" : "Success!"}


# get data from mavlink
@app.post("/drones/{drone_name}/update_position", 
         response_description = """
            Updates the drones last position.
         """
)
async def update_drone_position(
    drone_name : str
):
    try:
        db.update_drone(drone_dict[drone_name])
    except Exception as e:
        return {"Failure" : f"db.update_position failed \n\n\n {e}"}
    
    #THIS IS WHERE THE MAGIC WILL HAPPEN

    return {"Status" : "Success"}

@app.get("/maneuvers")
async def get_maneuvers():
    return {"maneuvers" : database.get_all_programs()}

@app.post("/maneuvers/create")
async def create_maneuver(
    manuver : db.Program
):
    try:
        database.create_program(manuver)
    except Exception as e:
        return {"Failure" : f"data.CreateProgram failed \n\n\n {e}"}
    
    return {"Success" : "Yay!"}
    
@app.post("/maneuvers/delete")
async def delete_maneuver(
    name : str
):  
    try:
        database.delete_program(db.Program(name=name, content=[]))
    except Exception as e:
        return {"Failure" : f"failed \n\n\n {e}"}
    
    return {"Success" : "Yay!"}

@app.post("/maneuvers/assign_to_drone")
async def assign_path_to_drone(
    program_name,
    drone_name
):
    database.assign_program_to_drone(
        drone=database.get_drone_by_name(drone_name),
        program=database.get_program_by_name(program_name)
    )
    
    return {"Success" : "Yay!"}

@app.post("/maneuvers/update_path")
async def update_path(
    program_name,
    paths
):
    program = db.Program(name="temp", content=[])
    program.content.append(paths)
    program.name = program_name
    print(program.content)
    database.update_program_content(
        program
    )
    return {"Success" : "Yay!"}

## SINGLE DRONE CONNECTION
s_connect = None

@app.get("/drones/single_connection_init")
async def single_connection_protocol():
    s_connect = dragon_link.connect_to_dragonlink()

    dragon_link.set_flight_mode(s_connect, 'LOITER')
    dragon_link.arm_vehicle(s_connect)
    dragon_link.set_flight_mode(s_connect, 'LOITER')

@app.get("/drones/single_connection/take_off")
async def single_drone_takeoff(t_alt = 5):
    if s_connect is not None:    
        dragon_link.takeoff(s_connect, t_altitude=t_alt)
    else:
        return {"Response" : "No drone connection"}

@app.get("/drones/single_connection/land")
async def single_drone_land():
    if s_connect is not None:
        dragon_link.land(s_connect)
    else:
        return {"Response" : "No drone connection"}

@app.post("/drones/single_connection/execute_path")
async def execute_path(
    drone_name : str
):
    ## get drone object
    drone = drone_dict[drone_name]
    
    ## check connection
    if s_connect is None:
        return {"Failure" : "No drone connection"}

    ## get drone path
    database.get_program_by_name(drone_name)
    path = None

    
    for x in path:
        dragon_link.seek_pos(
            s_connect, 
            lat=x["lat"],
            lon=x["lon"],
            alt=x["alt"]
        )
    

@app.post("/drones/single_connection/seek_point")
async def single_drone_seek(
    x_pos, y_pos, alt
):
    if s_connect is not None:
        dragon_link.seek_pos(
            s_connect,
            x_pos,
            y_pos,
            alt
        )   
    else:
        return {"Response" : "No drone connection"}

#simply gives all the tables in the db, ensures it is properly setup
@app.get("/")
async def read_root():
    inspector = inspect(engine)
    return {"Page": inspector.get_table_names()}    

## TODO: ADD A PING DRONE FUNCTION, THIS WILL ALLOW USER TO SELECT A DRONE IN THE UI AND HAVE THE HARDWARE MAKE A SOUND