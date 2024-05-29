from pydantic import BaseModel

class ApiKey(BaseModel):
    """
    Model class for API key.

    Attributes:
    - api_key (str): The API key string.
    """
    api_key: str