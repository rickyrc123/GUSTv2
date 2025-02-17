from pydantic import BaseModel, Field
from typing import List, Tuple, Annotated

class Post(BaseModel):
  content: str
  title: str

  class Config:
    from_attributes = True

class CreatePost(Post):
  pass

class DroneInSwarm(BaseModel):
  """Read-only representation of a Drone within a Swarm.
  
  Attributes:
    id (int): Unique identifier for the drone
    name (str): Display name of the drone
    model (str): Model/type identifier of the drone
  """
  id: Annotated[int, Field(description="Unique identifier for the drone")]
  name: Annotated[str, Field(description="Display name of the drone")]
  model: Annotated[str, Field(description="Model/type identifier of the drone")]

  class Config:
    from_attributes = True

class Drone(BaseModel):
  """Base Drone model containing all common drone attributes.
  
  Attributes:
    name (str): Display name of the drone
    model (str): Model/type identifier of the drone
    current_long (float): Current longitude position
    current_lat (float): Current latitude position
    current_alt (float): Current altitude in meters
    current_yaw (float): Current yaw angle in degrees
  """
  _id: Annotated[int, Field(description="Drone id (internal use only)")]
  name: Annotated[str, Field(description="Display name of the drone")]
  model: Annotated[str, Field(description="Model/type identifier of the drone")]
  current_long: Annotated[float, Field(description="Current longitude position")]
  current_lat: Annotated[float, Field(description="Current latitude position")]
  current_alt: Annotated[float, Field(description="Current altitude in meters")]
  current_yaw: Annotated[float, Field(description="Current yaw angle in degrees")]

  class Config:
    from_attributes = True

class CreateDrone(Drone):
  """Schema for creating a new drone.
  
  Attributes:
    name (Optional[str]): Display name of the drone. If None, will be auto-generated as 'Drone{id:06}'.
    All other attributes inherited from DroneBase.
  """
  name: Annotated[str | None, Field(default=None, description="Display name of the drone. If None, will be auto-generated as 'Drone{id:06}'")]

class Swarm(BaseModel):
  """Base Swarm model representing a group of drones.
  
  Attributes:
    name (str): Display name of the swarm
    drones (List[DroneInSwarm]): List of drones currently in the swarm
  """
  name: Annotated[str, Field(description="Display name of the swarm")]
  drones: Annotated[List[DroneInSwarm], Field(default=[], description="List of drones currently in the swarm")]

  class Config:
    from_attributes = True

class CreateSwarm(Swarm):
  """Schema for creating a new swarm.
  
  Attributes:
    name (Optional[str]): Display name of the swarm. If None, must be provided.
    All other attributes inherited from SwarmBase.
  """
  name: Annotated[str | None, Field(default=None, description="Display name of the swarm. If None, must be provided.")]

class Waypoint(BaseModel):
  """Represents a single waypoint in 3D space.
  
  Attributes:
    long (float): Longitude coordinate
    lat (float): Latitude coordinate
    alt (float): Altitude in meters
  """
  long: Annotated[float, Field(description="Longitude coordinate")]
  lat: Annotated[float, Field(description="Latitude coordinate")]
  alt: Annotated[float, Field(description="Altitude in meters")]

  class Config:
    from_attributes = True

class CreateWaypoint(Waypoint):
  """Schema for creating a new waypoint.
  
  Attributes:
    All attributes inherited from Waypoint.
  """
  pass

class Program(BaseModel):
  """Represents a flight program consisting of waypoints and their associated speeds.
  
  Attributes:
    name (str): Display name of the program
    content (List[Tuple[Waypoint, float]]): List of waypoint and speed pairs. Each tuple contains:
      - Waypoint: The target position
      - float: The speed to travel to this waypoint in meters/second
  """
  name: Annotated[str, Field(description="Display name of the program")]
  content: Annotated[List[Tuple[Waypoint, float]], Field(description="List of waypoint and speed pairs. Each tuple contains a Waypoint and the speed to travel to this waypoint in meters/second")]

  class Config:
    from_attributes = True

class CreateProgram(Program):
  """Schema for creating a new program.
  
  Attributes:
    name (Optional[str]): Display name of the program. If None, must be provided.
    All other attributes inherited from Program.
  """
  name: Annotated[str | None, Field(default=None, description="Display name of the program. If None, must be provided.")]

class DroneUpdate(BaseModel):
  """Schema for updating drone properties. All fields are optional.
  
  Attributes:
    name (Optional[str]): New display name
    model (Optional[str]): New model identifier
    current_long (Optional[float]): New longitude position
    current_lat (Optional[float]): New latitude position
    current_alt (Optional[float]): New altitude in meters
    current_yaw (Optional[float]): New yaw angle in degrees
  """
  name: Annotated[str | None, Field(default=None, description="New display name")]
  model: Annotated[str | None, Field(default=None, description="New model identifier")]
  current_long: Annotated[float | None, Field(default=None, description="New longitude position")]
  current_lat: Annotated[float | None, Field(default=None, description="New latitude position")]
  current_alt: Annotated[float | None, Field(default=None, description="New altitude in meters")]
  current_yaw: Annotated[float | None, Field(default=None, description="New yaw angle in degrees")]

class WaypointUpdate(BaseModel):
  """Schema for updating waypoint properties. All fields are optional.
  
  Attributes:
    long (Optional[float]): New longitude coordinate
    lat (Optional[float]): New latitude coordinate
    alt (Optional[float]): New altitude in meters
  """
  long: Annotated[float | None, Field(default=None, description="New longitude coordinate")]
  lat: Annotated[float | None, Field(default=None, description="New latitude coordinate")]
  alt: Annotated[float | None, Field(default=None, description="New altitude in meters")]