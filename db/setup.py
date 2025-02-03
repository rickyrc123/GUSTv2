#Once the database is setup, this will create all the tables defined in models

from sqlalchemy import create_engine
from models import *

def build():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/postgres')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

build()
