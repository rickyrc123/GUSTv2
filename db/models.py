from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKey, Integer, Sequence, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# FastAPI post
class Post(Base):
  __tablename__ = 'posts'

  id          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  title       = Column(String, nullable=False )
  content     = Column(String, nullable=False)
  published   = Column(Boolean, server_default='TRUE')
  created_at  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


# Drone information table
#
# id          - unique id, maintained and incremented by database
# name        - unique name, defaults to "DRONE" + id
# model       - name of drone's model
# state       - Current state (off/on)
# created_at  - the date and time of creation
# accessed_at - the date and time of last access

class DroneInfo(Base):
  __tablename__ = 'drone_info'

  id         = Column(Integer,  primary_key=True, autoincrement=True)
  name       = Column(String,   unique=True, nullable=True)
  model      = Column(String,   nullable=True)
  state      = Column(String,   nullable=False, server_default="0")
  created_at = Column(DateTime, nullable=False, server_default='now()')
  updated_at = Column(DateTime, nullable=False, server_default='now()')

# Drone location table
#
# long       - the drone's current longitude
# lat        - the drone's current longitude
# alt        - the drone's current altitude
# yaw        - the drone's current yaw / direction
# maybe velocity

class DroneLocation(Base):
  __tablename__ = 'drone_locations'

  drone_id     = Column(Integer, ForeignKey('drone_info.id'), primary_key=True)
  current_long = Column(Double,   nullable=True)
  current_lat  = Column(Double,   nullable=True)
  current_alt  = Column(Double,   nullable=True)
  current_yaw  = Column(Double,   nullable=True)


# Drone swarm table
class Swarm(Base):
  __tablename__ = 'swarms'

  id         = Column(Integer,  primary_key=True, autoincrement=True)
  name       = Column(String,   unique=True)
  created_at = Column(DateTime, nullable=False, server_default='now()')
  updated_at = Column(DateTime, nullable=False, server_default='now()')

# Table that relates programs to drones depending on their swarm
#
# drone_id   - Only non nullable key, relates the specific drone that is running the program
# program_id - nullable, if this value is null this means that the drone does not have any
#              specific program related to it
# swarm_id   - relates the drone to a swarm allowing one drone to have different programs
#              depending on the swarm it is in, a null value means the program is for the
#              drone on its own with no swarm relation 

class Program_Drone_Swarm(Base):
  __tablename__ = 'droneswarms'

  drone_id   = Column(Integer, ForeignKey('drone_info.id'), primary_key=True, nullable=False)
  program_id = Column(Integer, ForeignKey('programs.id'),   nullable=True)
  swarm_id   = Column(Integer, ForeignKey('swarms.id'),     nullable=True)

# Waypoint table
#
# id   - unique id, maintained and incremented by database
# long - waypoint longitude value
# lat  - waypoint latitude value
# alt  - waypoint altitude value

class Waypoint(Base):
  __tablename__ = 'waypoints'

  id   = Column(Integer, primary_key=True, autoincrement=True)
  long = Column(Double, nullable=True)
  lat  = Column(Double, nullable=True)
  alt  = Column(Double, nullable=True)

# Table for User made programs
#
# content - a string representation of waypoints and the speed
class Program(Base):
  __tablename__ = 'programs'

  id            = Column(Integer, primary_key=True, nullable=False)
  name          = Column(String, nullable=False)
  content       = Column(String, nullable=False)
  created_at    = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
  last_updated  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))