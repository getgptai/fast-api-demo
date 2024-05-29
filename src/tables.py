from sqlalchemy import Column, Integer, String
from src.db import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_key = Column(String, unique=True, index=True)
