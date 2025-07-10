from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

class Base(DeclarativeBase):
    pass

# Get the path of the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the database URL for the current directory
database_url = f"sqlite:///{os.path.join(current_directory, 'Customer Database.db')}"

# Create the engine
engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)