from sqlalchemy import Column, Integer, String
from src.db import Base

class APIKey(Base):
    """
    A class representing the APIKey table in the database.

    Attributes:
    - id (int): Primary key for the APIKey table.
    - api_key (str): Unique API key associated with the entry.
    """

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_key = Column(String, unique=True, index=True)