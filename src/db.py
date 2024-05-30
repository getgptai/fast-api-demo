from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL
DATABASE_URL = "sqlite:///./test.db"

# Create an engine to manage connections to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session local object to interact with the database
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()