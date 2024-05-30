from pydantic import BaseModel

class ApiKey(BaseModel):
    """
    Represents an API key.

    Attributes:
    - api_key (str): The API key string.
    """
    api_key: str