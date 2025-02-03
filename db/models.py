import enum

from sqlalchemy import Column, Double, Enum, ForeignKey, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DroneModels(enum.Enum):
  model1 = 1
  model2 = 2

# FastAPI post
class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default='TRUE')
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

# Drone information table
class Drone(Base):
  __tablename__ = 'drones'

  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String, unique=True)
  longitude = Column(Double, nullable=False)
  latitude = Column(Double, nullable=False)
  altitude = Column(Double, nullable=False)
  direction = Column(Double, nullable=False)
  model = Column(Enum(DroneModels), nullable=False)
  # state = Column(Enum, nullable=False, server_default="off")

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

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
  last_updated = Column(TIMESTAMP(timezone=True), server_default=text('now()'))