from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json, time
import datetime
import os

from db import models
from db import schemas

#TODO: connect drone to swarm, update drone, rename drone, diconnect from swarm, swarm programs vs drone programs

class DatabaseServer:
  DATABASE_URL = os.getenv("DATABASE_URL")

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

  def create_drone(self, **kwargs):
    drone_id = self.next_drone_id
    new_drone = models.Drone(

      id         = drone_id,
      name       = f'Drone{drone_id:06}',
      last_long  = kwargs.get("longitude"),
      last_lat   = kwargs.get("latitude"),
      last_alt   = kwargs.get('altitude'),
      last_dir   = kwargs.get('direction'),
      model      = kwargs.get('model'),
      state      = 0,
      created_at = datetime.datetime.utcnow()

    )

    with self.Session.begin() as session:
      session.add(new_drone)
      session.commit()
    
    self.next_drone_id += 1
  
  def get_drone_by_name(self, name:str) -> int:
    with self.Session.begin() as session:
      result = session.execute(select(text('drones')).where(models.Drone.name==name)).scalar()
    
    return result
  
  def get_all_drones(self):
    with self.Session.begin() as session:
      
      #this returns a weird type that fastapi doesnt like
      #TODO : properly parse this so it can get passed to the api server....
      results = session.execute(text('SELECT * FROM drones;')).fetchall() 
      strings = []
      
      for row in results:
          strings.append(str(row))
      
      payload = {
        "data" : strings
      }
      return json.dumps(payload)

  def get_drone_by_position(self, pos: tuple[float, float, float], return_name=False):
    with self.Session.begin() as session:
      result = session.execute(select(models.Drone.id, models.Drone.name).where(models))  
      session.close()

  def add_position(self,**kwargs): #kwargs is a dict of params btw
    
    new_position = models.DronePositions(
      id          = kwargs.get("id"),
      longitude   = kwargs.get("longitude"),
      latitude    = kwargs.get("latitude"),
      altitude    = kwargs.get("altitude"),
      direction   = kwargs.get("direction"),
      timestamp   = datetime.datetime.utcnow()
    )

    with self.Session.begin() as session:
      session.add(new_position)
      session.commit()
      session.close()
  
  def get_positions_by_drone(self, drone_id, num_positions : int = 50): 
      query = text("""
                      SELECT * 
                      FROM positions 
                      WHERE id = :drone_id
                      ORDER BY timestamp DESC 
                      LIMIT :num_positions
                  """)
      with self.Session.begin() as session:
        result = session.execute(query, {'drone_id' : drone_id, 'num_positions' : num_positions})
      
      strings = []
      for row in result:
        strings.append(str(row))
      
      payload = {
        "data" : strings
      }
      return json.dumps(payload)
  
  #updates drone table last positions
  def update_drone_table_position(
      self, 
      drone_id,
      **kwargs
  ):
    query = text("""
      UPDATE drones
      SET last_lat  = :lat,
          last_long = :long,
          last_alt  = :alt,
          last_dir  = :dir 
      WHERE id = :drone_id;
    """)

    with self.Session.begin() as session:
      session.execute(query, {
            'drone_id' : drone_id, 
            'lat'      : kwargs.get("latitude"),
            'long'     : kwargs.get("longitude"),
            'alt'      : kwargs.get("altitude"),
            'dir'      : kwargs.get("direction")})
      
      session.commit()