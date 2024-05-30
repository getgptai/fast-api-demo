from pydantic import BaseModel

class ApiKey(BaseModel):
    """
    Represents an API key for authentication.

    Attributes:
    - api_key (str): The API key string.
    """
    api_key: str