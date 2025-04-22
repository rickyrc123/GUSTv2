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

def _maneuver(maneuver: models.Maneuver):
  new_maneuver = schemas.Maneuver.model_validate(maneuver.__dict__)
  new_maneuver._id = maneuver.id
  return new_maneuver

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
          models.Path_Drone_Maneuver(
            drone_id=drone_info.id
          )
        )

        session.commit()
    except:
      raise Exception("Drone with same name is already defined.")
  
  def get_all_drones(self) -> List[schemas.Drone]:
    with self.Session.begin() as session:
      result = session.execute(
        select(models.DroneInfo, models.DroneLocation)
        .join(models.DroneLocation, models.DroneInfo.id == models.DroneLocation.drone_id)
      ).all()

      drone_list = [_drone(*drone) for drone in result]

    return drone_list
  
  def get_all_drone_names(self) -> List[str]:
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
        delete(models.Path_Drone_Maneuver)
        .where(models.Path_Drone_Maneuver.drone_id==drone._id)
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

  # Maneuver Services
  def create_maneuver(self, maneuver: schemas.CreateManeuver):
    try:
      new_maneuver = models.Maneuver(
        name=maneuver.name,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
      )
      
      with self.Session.begin() as session:
        session.add(new_maneuver)
        session.flush()

        if new_maneuver.name == None:
          new_maneuver.name = f"Maneuver{new_maneuver.id:06}"

        session.execute(
          update(models.Maneuver)
          .where(models.Maneuver.id == new_maneuver.id)
          .values(name=new_maneuver.name)
          )
        
        for drone in maneuver.drones:
          session.add(
            models.Path_Drone_Maneuver(
              drone_id=drone._id,
              maneuver_id=new_maneuver.id
            )
          )

        session.commit()
    except:
      raise Exception("Maneuver with same name is already defined.")

  # Currently all maneuvers are returned with drone lists empty but the name
  # can be used for getting that info
  def get_all_maneuvers(self) -> List[str]:
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Maneuver)
        ).all()

      maneuvers = [maneuver[0].name for maneuver in result]
    
    return maneuvers
  
  def get_maneuver_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Maneuver)
        .where(models.Maneuver.name==name)
      ).first()

      return _maneuver(*result)
  
  def get_drones_in_maneuver(self, maneuver: schemas.Maneuver) -> List[str]:
    drones = []
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Path_Drone_Maneuver.drone_id)
        .where(models.Path_Drone_Maneuver.maneuver_id==maneuver.id)
      ).all()

      for id in result:
        drone_name = session.execute(
          select(models.DroneInfo.name)
          .where(models.DroneInfo.id==id)
        ).first()

        drones.append(drone_name)
    
    return drones

  def add_drone_to_maneuver(self, maneuver: schemas.Maneuver, drone: schemas.Drone):
    maneuver.drones.append(drone.name)

    with self.Session.begin() as session:
      session.add(
        models.Path_Drone_Maneuver(
          drone_id=drone._id,
          maneuver_id=maneuver._id
        )
      )

      session.commit()
    return maneuver
  
  def remove_drone_from_maneuver(self, maneuver: schemas.Maneuver, drone: schemas.Drone):
    maneuver.drones.remove(drone.name)
    
    with self.Session.begin() as session:
      session.execute(
        delete(models.Path_Drone_Maneuver)
        .where(
          and_(models.Path_Drone_Maneuver.drone_id==drone._id,
          models.Path_Drone_Maneuver.maneuver_id==maneuver._id)
          )
      )

      session.commit()

  def update_maneuver_name(self, maneuver: schemas.Maneuver):
    with self.Session.begin() as session:
      session.execute(
        update(models.Maneuver)
        .where(models.Maneuver.id==maneuver._id)
        .values(name=maneuver.name)
      )

      session.commit()
  
  def delete_maneuver(self, maneuver: schemas.Maneuver):
    with self.Session.begin() as session:
      session.execute(
        delete(models.Path_Drone_Maneuver)
        .where(models.Path_Drone_Maneuver.maneuver_id==maneuver._id)
      )
      session.execute(
        delete(models.Maneuver)
        .where(models.Maneuver.id==maneuver._id)
      )
      session.commit()

  # Path Services
  def create_path(self, path : schemas.CreatePath):
      new_path = models.Path(
        name=path.name,
        content=path.content,
        created_at=datetime.datetime.utcnow(),
        last_updated=datetime.datetime.utcnow()
      )

      with self.Session.begin() as session:
        session.add(new_path)
        session.flush()
        
        if new_path.name == None:
          new_path.name = f"Path{new_path.id:06}"

        session.execute(
          update(models.Path)
          .where(models.Path.id == new_path.id)
          .values(name=new_path.name)
        )

        session.commit()

  def get_path_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Path)
        .where(models.Path.name==name)
        ).first()
      
      return result[0]

  def update_path_name(self, path: schemas.Path):
    with self.Session.begin() as session:
      session.execute(
        update(models.Path)
        .where(models.Maneuver.id==path._id)
        .values(name=path.name)
      )
  
  def update_path_content(self, path: schemas.Path):
     with self.Session.begin() as session:
        # Get the path within the same session
        db_path = session.execute(
            select(models.Path)
            .where(models.Path.name == path.name)
        ).scalar_one_or_none()
        
        if db_path:
            
            updated_content = db_path.content + path.content

            session.execute(
                update(models.Path)
                .where(models.Path.id == db_path.id)
                .values(content=updated_content)
            )
        # Session will auto-commit when exiting the context

  def delete_path(self, path: schemas.Path):
    with self.Session.begin() as session:
        # First, retrieve the path_id based on the path name
        path_id = session.execute(
            select(models.Path.id)
            .where(models.Path.name == path.name)
        ).scalar()

        # If the path with the specified name exists, proceed with deletion
        if path_id:
            # Delete from Path_Drone_Maneuver where path_id matches
            session.execute(
                delete(models.Path_Drone_Maneuver)
                .where(models.Path_Drone_Maneuver.path_id == path_id)
            )

            # Delete from the Path table where path_id matches
            session.execute(
                delete(models.Path)
                .where(models.Path.id == path_id)
            )

            # Commit the transaction
            session.commit()
        else:
            # If no path was found, handle it (optional)
            raise ValueError(f"Path with name {path.name} not found.")
  
  def assign_path_to_drone(self, drone : schemas.Drone, path : schemas.Path = None, maneuver : schemas.Maneuver = None):
    with self.Session.begin() as session:
      if maneuver is None:
        session.execute(
          update(models.Path_Drone_Maneuver)
          .where(
            and_(models.Path_Drone_Maneuver.drone_id==drone._id,
                 models.Path_Drone_Maneuver.maneuver_id.is_(None))
          )
          .values(models.Path_Drone_Maneuver.path_id==path._id)
        )
      elif path is None:
        session.execute(
          update(models.Path_Drone_Maneuver)
          .where(
            and_(models.Path_Drone_Maneuver.drone_id==drone._id,
                 models.Path_Drone_Maneuver.path_id.is_(None))
          )
          .values(models.Path_Drone_Maneuver.maneuver_id==path._id)
        )
      else:
        session.execute(
          update(models.Path_Drone_Maneuver)
          .where(
            and_(models.Path_Drone_Maneuver.drone_id==drone._id,
                 models.Path_Drone_Maneuver.maneuver_id==maneuver._id)
          )
          .values(models.Path_Drone_Maneuver.path_id==path._id)
        )
      
      session.commit()

  def get_all_paths(self):
    with self.Session.begin() as session:
      result = session.execute(select(models.Path)).all()

      #this is dumb, needs a cool function
      paths = [{"name": path[0].name,
                   "path": path[0].content} for path in result]

    return paths