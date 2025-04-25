from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKey, Integer, PickleType, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
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

class DroneInfo(Base):
  """Model representing information about a drone.

  Attributes:
    id (int): Unique identifier for the drone, auto-incremented by the database.
    name (str): Display name of the drone, must be unique, defaults to "DRONE" + id.
    model (str): Model/type identifier of the drone.
    state (str): Current state of the drone (e.g., "0" for off, "1" for on).
    created_at (datetime): Timestamp of when the drone was created.
    updated_at (datetime): Timestamp of the last update to the drone's information.
  """
  __tablename__ = 'drone_info'

  id         = Column(Integer,  primary_key=True, autoincrement=True)
  name       = Column(String,   unique=True, nullable=True)
  model      = Column(String,   nullable=True)
  state      = Column(String,   nullable=False, server_default="0")
  created_at = Column(DateTime, nullable=False, server_default='now()')
  updated_at = Column(DateTime, nullable=False, server_default='now()')
  location  = relationship(
    "DroneLocation", 
    cascade="all, delete", 
    passive_deletes=True)

class DroneLocation(Base):
  """Model representing the current location of a drone.

  Attributes:
    drone_id (int): Foreign key referencing the associated drone in the drone_info table.
    current_long (float): Current longitude of the drone.
    current_lat (float): Current latitude of the drone.
    current_alt (float): Current altitude of the drone in meters.
    current_yaw (float): Current yaw angle of the drone in degrees.
  """
  __tablename__ = 'drone_locations'

  drone_id     = Column(Integer, ForeignKey('drone_info.id', ondelete='CASCADE'), primary_key=True)
  current_long = Column(Double,   nullable=True)
  current_lat  = Column(Double,   nullable=True)
  current_alt  = Column(Double,   nullable=True)
  current_yaw  = Column(Double,   nullable=True)


class Maneuver(Base):
  """Model representing a drone maneuver that contains drones and related paths.

  Attributes:
    id (int): Unique identifier for the maneuver, auto-incremented by the database.
    name (str): Display name of the maneuver, must be unique.
    created_at (datetime): Timestamp of when the maneuver was created.
    updated_at (datetime): Timestamp of the last update to the maneuver's information.
  """
  __tablename__ = 'maneuvers'

  id         = Column(Integer,  primary_key=True, autoincrement=True)
  name       = Column(String,   unique=True, nullable=True)
  created_at = Column(DateTime, nullable=False, server_default='now()')
  updated_at = Column(DateTime, nullable=False, server_default='now()')

class Path_Drone_Maneuver(Base):
  """Table that relates paths to drones depending on their Maneuver

  Attributes:
    drone_id (int): Only non nullable key, relates the specific drone that is running the path
    path_id (int): nullable, if this value is null this means that the drone does not have any specific path related to it
    Maneuver_id (int): relates the drone to a maneuver allowing one drone to have different paths depending on the maneuver it is in, a null value means the path is for the drone on its own with no maneuver relation 
  """
  __tablename__ = 'path_drone_maneuvers'

  drone_id   = Column(Integer, ForeignKey('drone_info.id'), primary_key=True, nullable=False)
  path_id = Column(Integer, ForeignKey('paths.id'),   nullable=True)
  maneuver_id   = Column(Integer, ForeignKey('maneuvers.id'),     nullable=True)

class Waypoint(Base):
  """Model representing a waypoint in 3D space.

  Attributes:
    id (int): Unique identifier for the waypoint, auto-incremented by the database.
    long (float): Longitude coordinate of the waypoint.
    lat (float): Latitude coordinate of the waypoint.
    alt (float): Altitude of the waypoint in meters.
  """
  __tablename__ = 'waypoints'

  id   = Column(Integer, primary_key=True, autoincrement=True)
  long = Column(Double, nullable=True)
  lat  = Column(Double, nullable=True)
  alt  = Column(Double, nullable=True)

class Path(Base):
  """Model representing a user-defined flight path.

  Attributes:
    id (int): Unique identifier for the path, auto-incremented by the database.
    name (str): Display name of the path.
    content (str): A string representation of waypoints and their associated speeds.
    created_at (datetime): Timestamp of when the path was created.
    last_updated (datetime): Timestamp of the last update to the path.
  """
  __tablename__ = 'paths'

  id            = Column(Integer, primary_key=True, nullable=False)
  name          = Column(String, unique=True, nullable=True)
  content       = Column(PickleType, nullable=True, default=list)
  created_at    = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
  last_updated  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))