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

def _path(path: models.Path):
  new_path = schemas.Path.model_validate(path.__dict__)
  new_path._id = path.id
  return new_path

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
            drone_id=drone_info.id,
            maneuver_id=None,
            path_id=None
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
    except Exception as e:
      raise Exception(f"Maneuver with same name is already {e}")

  # Currently all maneuvers are returned with drone lists empty but the name
  # can be used for getting that info
  def get_all_maneuvers(self) -> List[str]:
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Maneuver)
        ).all()

      maneuvers = [maneuver[0].name for maneuver in result]
    
    return maneuvers
  
  def get_maneuver_id_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Maneuver)
        .where(models.Maneuver.name==name)
      ).first()
      id = result[0].id 
    return id
  
  def get_maneuver_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Maneuver)
        .where(models.Maneuver.name==name)
      ).first()

      return _maneuver(*result)
  
  def get_drones_in_maneuver(self, maneuver) -> List[str]:
    drones = []
    with self.Session.begin() as session:
        # Reattach the maneuver object to the session if necessary
        db_maneuver = session.execute(
            select(models.Maneuver).where(models.Maneuver.id == self.get_maneuver_id_by_name(maneuver))
        ).scalar_one_or_none()

        if not db_maneuver:
            raise ValueError(f"Maneuver with ID {maneuver} not found.")

        # Query drones in the maneuver
        result = session.execute(
            select(models.Path_Drone_Maneuver.drone_id)
            .where(models.Path_Drone_Maneuver.maneuver_id == db_maneuver.id)
        ).all()

        for drone_id in result:
            drone_name = session.execute(
                select(models.DroneInfo.name)
                .where(models.DroneInfo.id == drone_id[0])
            ).scalar_one_or_none()

            if drone_name:
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
      
      return _path(*result)
    
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
            
            session.execute(
                update(models.Path)
                .where(models.Path.id == db_path.id)
                .values(content=path.content)
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
          .values({"path_id": path._id})
        )
      elif path is None:
        session.execute(
          update(models.Path_Drone_Maneuver)
          .where(
            and_(models.Path_Drone_Maneuver.drone_id==drone._id)
          )
          .values({"maneuver_id": maneuver._id})
        )
      else:
        print(f"Path id: {path._id}")
        session.execute(
          update(models.Path_Drone_Maneuver)
          .where(
            and_(models.Path_Drone_Maneuver.drone_id==drone._id,
                 models.Path_Drone_Maneuver.maneuver_id==maneuver._id)
          )
          .values({"path_id": path._id})
        )
      
      session.commit()

  def get_path_by_drone_name(self, drone_name: str):
    with self.Session.begin() as session:

       # First, retrieve the drone_id based on the drone name
      drone_id = session.execute(
            select(models.DroneInfo.id)
            .where(models.DroneInfo.name == drone_name)
      ).scalar()

      print(drone_id)

      #Second, get path id from drone id
      path_id = session.execute(
            select(models.Path_Drone_Maneuver.path_id)
            .where(models.Path_Drone_Maneuver.drone_id == drone_id)
      ).scalar()

      print(path_id)
      #get content
      result = session.execute(
        select(models.Path)
        .where(models.Path.id==path_id)
      ).first()

      print(result)
      path = {"name": result[0].name,
              "path": result[0].content}

    return path
  
  def get_path_by_maneuver_name(self, maneuver_name: str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Path_Drone_Maneuver)
        .join(models.Maneuver, models.Path_Drone_Maneuver.maneuver_id == models.Maneuver.id)
        .join(models.Path, models.Path_Drone_Maneuver.path_id == models.Path.id)
        .where(models.Maneuver.name==maneuver_name)
      ).all()

      paths = [{"name": path[0].name,
                "path": path[0].content} for path in result]

    return paths

  def get_all_paths(self):
    with self.Session.begin() as session:
      result = session.execute(select(models.Path)).all()

      #this is dumb, needs a cool function
      paths = [{"UID" : path[0].id,
                "name": path[0].name,
                "path": path[0].content} for path in result]

    return paths
  
  def get_all_pathdronemanuevers(self):
    with self.Session.begin() as session:
      result = session.execute(select(models.Path_Drone_Maneuver)).all()

      path_drones = [{"drone_id" : path[0].drone_id,
                      "maneuver_id": path[0].maneuver_id,
                      "path_id": path[0].path_id} for path in result]

    return path_drones