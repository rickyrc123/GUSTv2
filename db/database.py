from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models
import schemas

#TODO: connect drone to swarm, update drone, rename drone, diconnect from swarm, swarm programs vs drone programs

class DatabaseServer:
  DATABASE_URL = 'postgresql+psycopg2://@localhost/fastapi'

  def __init__(self):
    engine = create_engine(self.DATABASE_URL)
    Session = sessionmaker(engine)
    self.Session = Session

    # Obtain last used id's for continuity
    with Session.begin() as session:
      self.next_drone_id = session.execute(select(models.Drone.id).order_by(models.Drone.id.desc()).limit(1)).scalar()
      self.next_program_id = session.execute(select(models.Program.id).order_by(models.Program.id.desc()).limit(1)).scalar()
      
        
      if self.next_drone_id == None:
        self.next_drone_id = 1
      else:
        self.next_drone_id += 1
      
      if self.next_program_id == None:
        self.next_program_id = 1
      else:
        self.next_program_id += 1

  def create_drone(self, drone:schemas.CreateDrone):
    drone_id = self.next_drone_id
    new_drone = models.Drone(**drone.model_dump())
    new_drone.id = drone_id
    
    if new_drone.name == None:
      new_drone.name = f'Drone{drone_id:06}'

    with self.Session.begin() as session:
      session.add(new_drone)
      session.commit()
    
    self.next_drone_id += 1
  
  def get_drone_by_name(self, name:str) -> int:
    with self.Session.begin() as session:
      result = session.execute(select(text('drones')).where(models.Drone.name==name)).scalar()
    
    return result

  def get_drone_by_position(self, pos: tuple[float, float, float], return_name=False):
    with self.Session.begin() as session:
      result = session.execute(select(models.Drone.id, models.Drone.name).where(models))  


