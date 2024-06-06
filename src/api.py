import uvicorn
from fastapi import FastAPI, HTTPException, Header, Depends
import uuid
from sqlalchemy.orm import Session
from typing import Annotated
from src import tables
from src.tables import APIKey
from src.db import session_local, engine

# Initialize FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Create all database tables on startup.
    """
    tables.Base.metadata.create_all(bind=engine)

async def get_db():
    """
    Dependency that provides a SQLAlchemy session and ensures it is closed after request.
    """
    db_session = session_local()
    try:
        yield db_session
    finally:
        db_session.close()

async def verify_api_key(
    session: Annotated[Session, Depends(get_db)], api_key: str = Header(None)
):
    """
    Dependency to verify API key provided in the request headers.
    """
    is_valid = session.query(APIKey).filter_by(api_key=api_key).first() is not None
    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/generate-api-key", response_model=dict)
async def generate_api_key(session: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to generate a new API key and store it in the database.
    """
    new_api_key = str(uuid.uuid4())
    session.add(APIKey(api_key=new_api_key))
    session.commit()
    return {"api_key": new_api_key}

@app.get("/secure-data", response_model=str, dependencies=[Depends(verify_api_key)])
async def secure_data():
    """
    Endpoint to access secure data, requires valid API key.
    """
    return "This is a secure message!"

@app.get("/get-api-keys")
async def get_api_keys(session: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to retrieve all API keys.
    """
    return session.query(APIKey).all()

@app.get("/")
async def home():
    """
    Home endpoint returning a welcome message.
    """
    return {"Message": "Welcome"}

# Run the application
if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')