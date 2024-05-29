from sqlalchemy import Column, Integer, String
from src.db import Base

class APIKey(Base):
    """
    A class representing the APIKey table in the database.

    Attributes:
    - id: An integer column representing the primary key of the table.
    - api_key: A string column representing the API key stored in the table.
    """

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_key = Column(String, unique=True, index=True)