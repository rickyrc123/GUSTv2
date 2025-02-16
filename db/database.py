from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
import datetime
import os

import models
import schemas

def _new_drone(drone : schemas.Drone):
  drone_info = models.DroneInfo(
    name=drone.name,
    model=drone.model,
    created_at=datetime.datetime.utcnow(),
    updated_at=datetime.datetime.utcnow()
  )

  drone_location = models.DroneLocation(
    current_long = drone.current_long,
    current_lat = drone.current_lat,
    current_alt = drone.current_alt,
    current_yaw = drone.current_yaw
  )

  return drone_info, drone_location

def _drone(info: models.DroneInfo, location: models.DroneLocation):
  return schemas.Drone.model_validate(info.__dict__ | location.__dict__)

class DatabaseServer:
  DATABASE_URL = os.getenv("DATABASE_URL")

  def __init__(self):
    engine = create_engine(self.DATABASE_URL)
    Session = sessionmaker(engine)
    self.Session = Session

  def create_drone(self, drone : schemas.Drone):
    try:
      drone_info, drone_location = _new_drone(drone)

      with self.Session.begin() as session:
        session.add(drone_info)
        session.flush()

        if drone_info == None:
          drone_info.name = f"Drone{drone_info.id:06}"

        session.execute(
          update(models.DroneInfo)
          .where(models.DroneInfo.id == drone_info.id)
          .values(name=drone_info.name)
          )
      
        drone_location.drone_id = drone_info.id

        session.add(drone_location)
        session.commit()
    except:
      print("Drone with same name is already defined.")
  
  def get_all_drones(self):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo, models.DroneLocation)
        .join(models.DroneLocation, models.DroneInfo.id == models.DroneLocation.drone_id)
      ).all()

      drones = [_drone(*drone.tuple()) for drone in result]

    return drones
  
  def get_drone_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo, models.DroneLocation)
        .join(models.DroneLocation, models.DroneInfo.id == models.DroneLocation.drone_id)
        .where(models.DroneInfo.name==name)
        ).first()
      
      return _drone(*result)