from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKey, Integer, Sequence, String, TIMESTAMP, text
from sqlalchemy.orm import relationship, mapped_column
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
  locations  = relationship(
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

  id           = Column(Integer, primary_key=True, autoincrement=True)
  drone_id     = Column(Integer, ForeignKey('drone_info.id', ondelete='CASCADE'))
  current_long = Column(Double,   nullable=True)
  current_lat  = Column(Double,   nullable=True)
  current_alt  = Column(Double,   nullable=True)
  current_yaw  = Column(Double,   nullable=True)


class Swarm(Base):
  """Model representing a drone swarm.

  Attributes:
    id (int): Unique identifier for the swarm, auto-incremented by the database.
    name (str): Display name of the swarm, must be unique.
    created_at (datetime): Timestamp of when the swarm was created.
    updated_at (datetime): Timestamp of the last update to the swarm's information.
  """
  __tablename__ = 'swarms'

  id         = Column(Integer,  primary_key=True, autoincrement=True)
  name       = Column(String,   unique=True, nullable=False)
  created_at = Column(DateTime, nullable=False, server_default='now()')
  updated_at = Column(DateTime, nullable=False, server_default='now()')

class Program_Drone_Swarm(Base):
  """Table that relates programs to drones depending on their swarm

  Attributes:
    drone_id (int): Only non nullable key, relates the specific drone that is running the program
    program_id (int): nullable, if this value is null this means that the drone does not have any
                      specific program related to it
    swarm_id (int): relates the drone to a swarm allowing one drone to have different programs
                    depending on the swarm it is in, a null value means the program is for the
                    drone on its own with no swarm relation 
  """
  __tablename__ = 'program_drone_swarms'

  drone_id   = Column(Integer, ForeignKey('drone_info.id'), primary_key=True, nullable=False)
  program_id = Column(Integer, ForeignKey('programs.id'),   nullable=True)
  swarm_id   = Column(Integer, ForeignKey('swarms.id'),     nullable=True)

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

class Program(Base):
  """Model representing a user-defined flight program.

  Attributes:
    id (int): Unique identifier for the program, auto-incremented by the database.
    name (str): Display name of the program.
    content (str): A string representation of waypoints and their associated speeds.
    created_at (datetime): Timestamp of when the program was created.
    last_updated (datetime): Timestamp of the last update to the program.
  """
  __tablename__ = 'programs'

  id            = Column(Integer, primary_key=True, nullable=False)
  name          = Column(String, nullable=False)
  content       = Column(String, nullable=False)
  created_at    = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
  last_updated  = Column(TIMESTAMP(timezone=True), server_default=text('now()'))