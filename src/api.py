import uvicorn
from fastapi import FastAPI, HTTPException, Header, Depends
import uuid
from sqlalchemy.orm import Session
from typing import Annotated
from src import tables
from src.tables import APIKey
from src.db import session_local, engine

app = FastAPI()

def create_database():
    """
    Function to create database tables on application startup.
    """
    tables.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    create_database()

async def get_db():
    """
    Function to get a database session.
    """
    session = session_local()
    try:
        yield session
    finally:
        session.close()

async def verify_api_key(
    session: Annotated[Session, Depends(get_db)], api_key: str = Header(None)
):
    """
    Function to verify the API key provided in the request header.
    
    Args:
        session (Session): Database session.
        api_key (str): API key provided in the request header.
    
    Raises:
        HTTPException: If the API key is invalid.
    """
    verified = session.query(APIKey).filter_by(api_key=api_key).first() is not None
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/generate-api-key", response_model=dict)
async def generate_api_key(session: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to generate a new API key.
    
    Args:
        session (Session): Database session.
    
    Returns:
        dict: A dictionary containing the newly generated API key.
    """
    new_api_key = str(uuid.uuid4())
    session.add(APIKey(api_key=new_api_key))
    session.commit()
    return {"api_key": new_api_key}

@app.get("/secure-data", response_model=str, dependencies=[Depends(verify_api_key)])
async def secure_data():
    """
    Endpoint to access secure data.
    
    Returns:
        str: A secure message.
    """
    return "This is a secure message!"

@app.get("/get-api-keys")
async def get_api_keys(session: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to retrieve all API keys stored in the database.
    
    Args:
        session (Session): Database session.
    
    Returns:
        List[APIKey]: A list of all API keys stored in the database.
    """
    return session.query(APIKey).all()

@app.get("/")
async def home():
    """
    Default endpoint to welcome users.
    
    Returns:
        dict: A welcome message.
    """
    return {"Message": "Welcome"}

"""
if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')
"""