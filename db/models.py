import enum

from sqlalchemy import Column, Double, Enum, ForeignKey, Integer, String, TIMESTAMP, Boolean, text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DroneModels(enum.Enum):
  model1 = 1
  model2 = 2

# FastAPI post
class Post(Base):
  __tablename__ = 'posts'

  id          = Column(Integer, primary_key=True, nullable=False)
  title       = Column(String, nullable=False )
  content     = Column(String, nullable=False)
  published   = Column(Boolean, server_default='TRUE')
  created_at  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

# Drone information table
class Drone(Base):
  __tablename__ = 'drones'

  id        = Column(Integer,  primary_key=True, nullable=False        )
  name      = Column(String,   unique=True                             )
  last_long = Column(Double,   nullable=True                           )
  last_lat  = Column(Double,   nullable=True                           )
  last_alt  = Column(Double,   nullable=True                           )
  last_dir  = Column(Double,   nullable=True                           )
  model     = Column(String,   nullable=True                           )
  state     = Column(Integer,  nullable=False,  server_default="0"     )
  created_at= Column(DateTime, nullable=False, server_default='now()'  )

class DronePositions(Base):
  __tablename__ = 'positions'
  
  id        = Column(Integer, primary_key=True, nullable=False         )
  longitude = Column(Double, nullable=False                                                     )
  latitude  = Column(Double, nullable=False                                                     )
  altitude  = Column(Double, nullable=False                                                     )
  direction = Column(Double, nullable=False                                                     )
  timestamp = Column(DateTime, primary_key=True, nullable=False, server_default='now()'         )


class Swarm(Base):
  __tablename__ = 'swarms'

  id = Column(Integer, primary_key=True, nullable=False)
  # Add more info as needed

class Drone_Swarms(Base):
  __tablename__ = 'droneswarms'

  drone_id = Column(Integer, ForeignKey('drones.id'), primary_key=True, nullable=False)
  swarm_id = Column(Integer, ForeignKey('swarms.id'), primary_key=True, nullable=False)

# Table for User made programs
class Program(Base):
  __tablename__ = 'programs'

  id            = Column(Integer, primary_key=True, nullable=False)
  title         = Column(String, nullable=False)
  content       = Column(String, nullable=False)
  created_at    = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
  last_updated  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))