
import random
from typing import Union
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


@app.get("/drones")
async def get_all_drones():
    return {"Drones" : list(drone_dict.values())}

@app.post("/drones/create") #change this to post
async def create_drone(
    drone : db.CreateDrone
):
    try:
        database.create_drone(drone=drone)
    except Exception as e:
        return {"Status" : f"db.create_drone failed! \n\n\n {e}"} 
    
    drone_dict[drone.name] = drone
    return {"Status" : "Success!"}

@app.get("/drones/{drone_name}")
async def get_drone(
    drone_name : str
):
    drone = drone_dict[drone_name]
    return {"Drone" : drone}


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
    return {"maneuvers" : database.get_all_maneuvers()}

@app.post("/maneuvers/create")
async def create_maneuver(
    manuver : db.schemas.CreateManeuver
):
    try:
        database.create_maneuver(manuver)
    except Exception as e:
        return {"Failure" : f"data.CreateManeuver failed \n\n\n {e}"}
    
    return {"Success" : "Yay!"}
    
@app.post("/maneuvers/delete")
async def delete_maneuver(
    name : str
):  
    try:
        database.delete_maneuver(db.Maneuver(name=name, content=[]))
    except Exception as e:
        return {"Failure" : f"failed \n\n\n {e}"}
    
    return {"Success" : "Yay!"}

@app.post("/maneuvers/assign_to_drone")
async def assign_path_to_drone(
    maneuver_name,
    drone_name,
    path = None
):  
    if path is not None:

        try:
            database.assign_path_to_drone(
                maneuver=database.get_maneuver_by_name(maneuver_name),
                drone=database.get_drone_by_name(drone_name),
                path=db.schemas.Path(name=f"{maneuver_name}{drone_name}", content=path)
            )
        except Exception as e:
            return {"Failure" : f"{e}"}
    else:
        try:
            database.assign_path_to_drone(
                maneuver=database.get_maneuver_by_name(maneuver_name),
                drone=database.get_drone_by_name(drone_name),
            )
        except Exception as e:
            return {"Failure" : f"{e}"}
    return {"Success" : "Yay!"}

@app.post("/programs/update_path")
async def update_path(
    path_name,
    new_path
):
    path = db.schemas.Path(name=path_name, content=new_path)
    print(path.content)
    try:
        database.update_path_content(
            path
        )
    except Exception as e:
        return {"Failure" : f"Failed to update program path {e}"}
    return {"Success" : "Yay!"}

@app.post("/programs/manuevers/get_drones_in_maneuver")
async def get_drones_in_maneuver(
    maneuver_name
):
    try:
        drones = database.get_drones_in_maneuver(maneuver_name)
    except Exception as e:
        return {"Failure" : f"Failed to get drones in maneuver {e}"}
    
    return {"Drones" : drones}

## SINGLE DRONE CONNECTION
s_connect = None

@app.get("/drones/single_connection_init")
async def single_connection_protocol():
    s_connect = dragon_link.connect_to_dragonlink()

    dragon_link.set_flight_mode(s_connect, 'GUIDED')
    dragon_link.arm_vehicle(s_connect)
    dragon_link.set_flight_mode(s_connect, 'LOITER')

@app.get("/drones/single_connection/take_off")
async def single_drone_takeoff(t_alt = 5):
    if s_connect is not None:    
        dragon_link.set_flight_mode(s_connect, 'GUIDED')
        dragon_link.takeoff(s_connect, t_altitude=t_alt)
    else:
        return {"Response" : "No drone connection"}

@app.get("/drones/single_connection/land")
async def single_drone_land():
    if s_connect is not None:
        dragon_link.land(s_connect)
    else:
        return {"Response" : "No drone connection"}
    
### MULIT DRONE CONNECTIONS
connections = []

@app.get("/drones/m_connect/set_flight_mode")
async def m_connect_set_flight_mode(
    drone_id,
    mode = "LOITER"
):
     print("inprogress, beep beep boop") 

@app.get("/drones/m_connect/available_connections")
async def m_connect_available_connections():
    # Scan for available UDP ports and return a list of available connections
    available_connections = dragon_link.scan_for_available_connections()
    return {"Available Connections": available_connections}

@app.get("/drones/m_connect/close_connection")
async def m_connect_close_connection(
    connection_id
):
    # Close the specified connection
    try:
        dragon_link.close_connection(connections[connection_id])
        del connections[connection_id]
    except Exception as e:
        return {"Failure" : f"Failed to close connection {e}"}
    
    return {"Success" : "Yay!"}

@app.get("/drones/m_connect/select_connection")
async def m_connect_select_connection(
    connection_id
):
    # Select the specified connection
    try:
        selected_connection = connections[connection_id]
    except Exception as e:
        return {"Failure" : f"Failed to select connection {e}"}
    
    return {"Success" : "Yay!"}

@app.get("/drones/m_connect/close_all_connections")
async def m_connect_close_all_connections():
    # Close all connections
    for connection in connections:
        try:
            dragon_link.close_connection(connection)
        except Exception as e:
            return {"Failure" : f"Failed to close connection {e}"}
    
    connections.clear()
    return {"Success" : "Yay!"}

@app.get("/drones/m_connect/close_connection")
async def m_connect_close_connection(
    connection_id
):
    # Close the specified connection
    try:
        dragon_link.close_connection(connections[connection_id])
        del connections[connection_id]
    except Exception as e:
        return {"Failure" : f"Failed to close connection {e}"}
    
    return {"Success" : "Yay!"}

@app.get("/drones/m_connect/refresh_connections")
async def m_connect_refresh_connections():
    # Scan for available UDP ports and return a list of available connections
    available_connections = dragon_link.scan_for_available_connections()
    return {"Available Connections": available_connections}

#simply gives all the tables in the db, ensures it is properly setup
@app.get("/")
async def read_root():
    inspector = inspect(engine)
    return {"Page": inspector.get_table_names()}    

## TODO: ADD A PING DRONE FUNCTION, THIS WILL ALLOW USER TO SELECT A DRONE IN THE UI AND HAVE THE HARDWARE MAKE A SOUND