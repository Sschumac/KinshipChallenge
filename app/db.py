from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

def init_session():
    Base = automap_base()
    engine = create_engine(
        'postgresql://kinship_webapp:{}@db:5432/challenge_db'.format(os.environ['PG_PWD']))
    Base.prepare(engine, reflect=True)
    return Session(engine), engine