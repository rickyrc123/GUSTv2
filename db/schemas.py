from db.models import DroneModels
from pydantic import BaseModel

class PostBase(BaseModel):
  content: str
  title: str

  class Config:
    from_attributes = True

class CreatePost(PostBase):
  class Config:
    from_attributes = True

class DroneBase(BaseModel):
  longitude: float
  latitude: float
  altitude: float
  direction: float
  model: str

  class Config:
    from_attributes = True

class CreatePosition(DroneBase):
  drone_id: int
  timestamp: str

  class Config:
    form_attributes = True

class CreateDrone(DroneBase):
  class Config:
    from_attributes = True

class ProgramBase(BaseModel):
  content: str
  title: str

  class Config:
    from_attributes = True

class CreateProgram(ProgramBase):
  class Config:
    from_attributes = True