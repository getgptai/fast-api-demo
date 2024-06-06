# Import necessary components from sqlalchemy
from sqlalchemy import Column, Integer, String

# Import Base from the database setup module
from src.db import Base

class APIKey(Base):
    """
    This class represents the APIKey table in the database.
    Each instance of this class corresponds to a row in the api_keys table.
    """
    # Define the name of the table
    __tablename__ = "api_keys"

    # Define the columns of the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String, unique=True, index=True)