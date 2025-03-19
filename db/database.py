from sqlalchemy import and_, create_engine, delete, select, update
from sqlalchemy.orm import sessionmaker
import datetime
import os

from typing import List

from . import models
from . import schemas

def _new_drone(drone : schemas.CreateDrone):
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
  drone = schemas.Drone.model_validate(info.__dict__ | location.__dict__)
  drone._id = info.id
  return drone

class DatabaseServer:
  DATABASE_URL = os.getenv("DATABASE_URL")

  def __init__(self):
    engine = create_engine(self.DATABASE_URL)
    Session = sessionmaker(engine)
    self.Session = Session

  # Drone Services
  def create_drone(self, drone : schemas.CreateDrone):
    try:
      drone_info, drone_location = _new_drone(drone)

      with self.Session.begin() as session:
        session.add(drone_info)
        session.flush()

        if drone_info.name == None:
          drone_info.name = f"Drone{drone_info.id:06}"

        session.execute(
          update(models.DroneInfo)
          .where(models.DroneInfo.id == drone_info.id)
          .values(name=drone_info.name)
        )
      
        drone_location.drone_id = drone_info.id

        session.add(drone_location)

        session.add(
          models.Program_Drone_Swarm(
            drone_id=drone_info.id
          )
        )

        session.commit()
    except:
      print("Drone with same name is already defined.")
  
  def get_all_drones(self) -> List[str]:
    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo)
      ).all()

      drone_names = [drone[0].name for drone in result]

    return drone_names
  
  def get_drone_by_name(self, name : str):

    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo, models.DroneLocation)
        .join(models.DroneLocation, models.DroneInfo.id == models.DroneLocation.drone_id)
        .where(models.DroneInfo.name==name)
        ).first()
      
      return _drone(*result)

  def get_drone_by_location(self, long: float, lat: float, alt: float):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo, models.DroneLocation)
        .join(models.DroneLocation, models.DroneInfo.id == models.DroneLocation.drone_id)
        .where(
          and_(models.DroneLocation.current_long==long,
               models.DroneLocation.current_lat == lat,
               models.DroneLocation.current_alt == alt)
        )
      ).first()
      
      return _drone(*result)

  # Pass the updated drone
  def update_drone_location(self, drone: schemas.Drone):
    with self.Session.begin() as session:
      session.execute(
        update(models.DroneLocation)
        .where(models.DroneLocation.drone_id==drone._id)
        .values(
          current_long=drone.current_long,
          current_lat=drone.current_lat,
          current_alt=drone.current_alt,
          current_yaw=drone.current_yaw
        )
      )
      session.commit()

  # Pass the updated drone
  def update_drone_info(self, drone: schemas.Drone):
    with self.Session.begin() as session:
      session.execute(
        update(models.DroneInfo)
        .where(models.DroneInfo.drone_id==drone._id)
        .values(
          name=drone.name,
          model=drone.model,
          state=drone.state,
          updated_at=datetime.datetime.utcnow()
        )
      )
      session.commit()
  
  def delete_drone(self, drone: schemas.Drone):
    with self.Session.begin() as session:
      session.execute(
        delete(models.Program_Drone_Swarm)
        .where(models.Program_Drone_Swarm.drone_id==drone._id)
      )
      session.execute(
        delete(models.DroneLocation)
        .where(models.DroneLocation.drone_id==drone._id)
      )
      session.execute(
        delete(models.DroneInfo)
        .where(models.DroneInfo.id==drone._id)
      )
      session.commit()

  # Swarm Services
  def create_swarm(self, swarm: schemas.CreateSwarm):
    try:
      new_swarm = models.Swarm(
        name=swarm.name,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
      )
      
      with self.Session.begin() as session:
        session.add(new_swarm)
        session.flush()

        if new_swarm.name == None:
          new_swarm.name = f"Drone{new_swarm.id:06}"

        session.execute(
          update(models.Swarm)
          .where(models.Swarm.id == new_swarm.id)
          .values(name=new_swarm.name)
          )
        
        for drone in swarm.drones:
          session.add(
            models.Program_Drone_Swarm(
              drone_id=drone._id,
              swarm_id=new_swarm.id
            )
          )

        session.commit()
    except:
      print("Swarm with same name is already defined.")

  # Currently all swarms are returned with drone lists empty but the name
  # can be used for getting that info
  def get_all_swarms(self) -> List[str]:
    with self.Session.begin() as session:
      result = session.execute(select(models.Swarm)).all()

      swarms = [swarm.name for swarm in result]
    
    return swarms
  
  def get_drones_in_swarm(self, swarm: schemas.Swarm) -> List[str]:
    drones = []
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Program_Drone_Swarm.drone_id)
        .where(models.Program_Drone_Swarm.swarm_id==swarm.id)
      ).all()

      for id in result:
        drone_name = session.execute(
          select(models.DroneInfo.name)
          .where(models.DroneInfo.id==id)
        ).first()

        drones.append(drone_name)
    
    return drones

  def add_drone_to_swarm(self, swarm: schemas.Swarm, drone: schemas.Drone):
    swarm.drones.append(drone.name)

    with self.Session.begin() as session:
      session.add(
        models.Program_Drone_Swarm(
          drone_id=drone._id,
          swarm_id=swarm.id
        )
      )

      session.commit()
  
  def remove_drone_from_swarm(self, swarm: schemas.Swarm, drone: schemas.Drone):
    swarm.drones.remove(drone.name)
    
    with self.Session.begin() as session:
      session.execute(
        delete(models.Program_Drone_Swarm)
        .where(
          and_(models.Program_Drone_Swarm.drone_id==drone._id,
          models.Program_Drone_Swarm.swarm_id==swarm._id)
          )
      )

      session.commit()

  def update_swarm_name(self, swarm: schemas.Swarm):
    with self.Session.begin() as session:
      session.execute(
        update(models.Swarm)
        .where(models.Swarm.id==swarm._id)
        .values(name=swarm.name)
      )

      session.commit()
  
  def delete_swarm(self, swarm: schemas.Swarm):
    with self.Session.begin() as session:
      session.execute(
        delete(models.Program_Drone_Swarm)
        .where(models.Program_Drone_Swarm.swarm_id==swarm._id)
      )
      session.execute(
        delete(models.Swarm)
        .where(models.Swarm.id==swarm._id)
      )
      session.commit()