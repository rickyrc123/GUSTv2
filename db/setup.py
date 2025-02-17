#Once the database is setup, this will create all the tables defined in models
import os
from sqlalchemy import create_engine, inspect
from .models import *

def build():
    engine = create_engine(os.getenv("DATABASE_URL"))
    inspector = inspect(engine)

    if 'drone_info' not in inspector.get_table_names():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

build()
