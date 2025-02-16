#Once the database is setup, this will create all the tables defined in models
import os
from sqlalchemy import create_engine
from models import *

def build():
    engine = create_engine(os.getenv("DATABASE_URL"))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

build()
