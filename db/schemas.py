from pydantic import BaseModel, Field
from typing import List, Tuple, Annotated

class Post(BaseModel):
  content: str
  title: str

  class Config:
    from_attributes = True

class CreatePost(Post):
  pass

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
  _id: int | None
  name: Annotated[str | None, Field(default=None, description="Display name of the drone. If None, will be auto-generated as 'Drone{id:06}'")]

class Waypoint(BaseModel):
  """Represents a single waypoint in 3D space.
  
  Attributes:
    long (float): Longitude coordinate
    lat (float): Latitude coordinate
    alt (float): Altitude in meters
  """
  _id: Annotated[int, Field(description="Drone id (internal use only)")]
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
  _id: int | None

class Path(BaseModel):
  """Represents a flight path consisting of waypoints and their associated speeds.
  
  Attributes:
    name (str): Display name of the path
    content (List[Tuple[Waypoint, float]]): List of waypoint and speed pairs. Each tuple contains:
      - Waypoint: The target position
      - float: The speed to travel to this waypoint in meters/second
  """
  _id: Annotated[int, Field(description="Drone id (internal use only)")]
  name: Annotated[str, Field(description="Display name of the path")]
  content: Annotated[List[Waypoint] | None, Field(description="List of waypoint and speed pairs. Each tuple contains a Waypoint and the speed to travel to this waypoint in meters/second")]

  class Config:
    from_attributes = True

class CreatePath(Path):
  """Schema for creating a new path.
  
  Attributes:
    name (Optional[str]): Display name of the path. If None, will be auto-generated as 'Path{id:06}'.
    All other attributes inherited from Path.
  """
  _id: int | None
  name: Annotated[str | None, Field(default=None, description="Display name of the path. If None, will be auto-generated as 'Path{id:06}'")]

class Maneuver(BaseModel):
  """Base Maneuver model representing a group of drones.
  
  Attributes:
    name (str): Display name of the maneuver
    drones (List[(Drone, path)]): List of drones currently in the maneuver paired with their respective path
  """
  _id: Annotated[int, Field(description="Maneuver id (internal use only)")]
  name: Annotated[str, Field(description="Display name of the maneuver")]
  drones: Annotated[List[Tuple[Drone, Path]], Field(default=[], description="List of drones currently in the maneuver by name")]

  class Config:
    from_attributes = True

class CreateManeuver(Maneuver):
  """Schema for creating a new maneuver.
  
  Attributes:
    name (Optional[str]): Display name of the maneuver. If None, will be auto-generated as 'Maneuver{id:06}'.
    All other attributes inherited from ManeuverBase.
  """
  _id: int | None
  name: Annotated[str | None, Field(default=None, description="Display name of the maneuver. If None, will be auto-generated as 'Maneuver{id:06}'")]