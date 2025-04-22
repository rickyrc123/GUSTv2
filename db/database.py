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
          models.Program_Drone_Maneuver(
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
        delete(models.Program_Drone_Maneuver)
        .where(models.Program_Drone_Maneuver.drone_id==drone._id)
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
            models.Program_Drone_Maneuver(
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
        select(models.Program_Drone_Maneuver.drone_id)
        .where(models.Program_Drone_Maneuver.maneuver_id==maneuver.id)
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
        models.Program_Drone_Maneuver(
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
        delete(models.Program_Drone_Maneuver)
        .where(
          and_(models.Program_Drone_Maneuver.drone_id==drone._id,
          models.Program_Drone_Maneuver.maneuver_id==maneuver._id)
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
        delete(models.Program_Drone_Maneuver)
        .where(models.Program_Drone_Maneuver.maneuver_id==maneuver._id)
      )
      session.execute(
        delete(models.Maneuver)
        .where(models.Maneuver.id==maneuver._id)
      )
      session.commit()

  # Program Services
  def create_program(self, program : schemas.CreateProgram):
      new_program = models.Program(
        name=program.name,
        content=program.content,
        created_at=datetime.datetime.utcnow(),
        last_updated=datetime.datetime.utcnow()
      )

      with self.Session.begin() as session:
        session.add(new_program)
        session.flush()
        
        if new_program.name == None:
          new_program.name = f"Program{new_program.id:06}"

        session.execute(
          update(models.Program)
          .where(models.Program.id == new_program.id)
          .values(name=new_program.name)
        )

        session.commit()

  def get_program_by_name(self, name : str):
    with self.Session.begin() as session:
      result = session.execute(
        select(models.Program)
        .where(models.Program.name==name)
        ).first()
      
      return result[0]

  def update_program_name(self, program: schemas.Program):
    with self.Session.begin() as session:
      session.execute(
        update(models.Program)
        .where(models.Maneuver.id==program._id)
        .values(name=program.name)
      )
  
  def update_program_content(self, program: schemas.Program):
     with self.Session.begin() as session:
        # Get the program within the same session
        db_program = session.execute(
            select(models.Program)
            .where(models.Program.name == program.name)
        ).scalar_one_or_none()
        
        if db_program:
            
            updated_content = db_program.content + program.content

            session.execute(
                update(models.Program)
                .where(models.Program.id == db_program.id)
                .values(content=updated_content)
            )
        # Session will auto-commit when exiting the context

  def delete_program(self, program: schemas.Program):
    with self.Session.begin() as session:
        # First, retrieve the program_id based on the program name
        program_id = session.execute(
            select(models.Program.id)
            .where(models.Program.name == program.name)
        ).scalar()

        # If the program with the specified name exists, proceed with deletion
        if program_id:
            # Delete from Program_Drone_Maneuver where program_id matches
            session.execute(
                delete(models.Program_Drone_Maneuver)
                .where(models.Program_Drone_Maneuver.program_id == program_id)
            )

            # Delete from the Program table where program_id matches
            session.execute(
                delete(models.Program)
                .where(models.Program.id == program_id)
            )

            # Commit the transaction
            session.commit()
        else:
            # If no program was found, handle it (optional)
            raise ValueError(f"Program with name {program.name} not found.")
  
  def assign_program_to_drone(self, drone : schemas.Drone, program : schemas.Program, maneuver : schemas.Maneuver = None):
    with self.Session.begin() as session:
      if maneuver is None:
        session.execute(
          update(models.Program_Drone_Maneuver)
          .where(
            and_(models.Program_Drone_Maneuver.drone_id==drone._id,
                 models.Program_Drone_Maneuver.maneuver_id.is_(None))
          )
          .values(models.Program_Drone_Maneuver.program_id==program._id)
        )
      else:
        session.execute(
          update(models.Program_Drone_Maneuver)
          .where(
            and_(models.Program_Drone_Maneuver.drone_id==drone._id,
                 models.Program_Drone_Maneuver.maneuver_id==maneuver._id)
          )
          .values(models.Program_Drone_Maneuver.program_id==program._id)
        )
      
      session.commit()

  def get_all_programs(self):
    with self.Session.begin() as session:
      result = session.execute(select(models.Program)).all()

      #this is dumb, needs a cool function
      programs = [{"name": program[0].name,
                   "path": program[0].content} for program in result]

    return programs