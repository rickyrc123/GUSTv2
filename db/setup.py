#Once the database is setup, this will create all the tables defined in models

from sqlalchemy import create_engine
from models import *

engine = create_engine('postgresql+psycopg2://GUSTv2:password@localhost/GUSTv2')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
