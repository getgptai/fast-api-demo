import uvicorn
from fastapi import FastAPI, HTTPException, Header, Depends
import uuid
from sqlalchemy.orm import Session
from typing import Annotated
from src import tables
from src.tables import APIKey
from src.db import session_local, engine

# Create FastAPI instance
app = FastAPI()

# Event handler for startup to initialize the database
@app.on_event("startup")
async def startup_event():
    tables.Base.metadata.create_all(bind=engine)

# Dependency to provide a database session
async def get_db():
    session = session_local()
    try:
        yield session
    finally:
        session.close()

# Dependency to verify API key
async def verify_api_key(
    session: Annotated[Session, Depends(get_db)], api_key: str = Header(None)
):
    if not session.query(APIKey).filter_by(api_key=api_key).first():
        raise HTTPException(status_code=403, detail="Invalid API key")

# Endpoint to generate a new API key
@app.post("/generate-api-key", response_model=dict)
async def generate_api_key(session: Annotated[Session, Depends(get_db)]):
    new_api_key = str(uuid.uuid4())
    session.add(APIKey(api_key=new_api_key))
    session.commit()
    return {"api_key": new_api_key}

# Endpoint to access secure data, requires API key verification
@app.get("/secure-data", response_model=str, dependencies=[Depends(verify_api_key)])
async def secure_data():
    return "This is a secure message!"

# Endpoint to retrieve all API keys
@app.get("/get-api-keys")
async def get_api_keys(session: Annotated[Session, Depends(get_db)]):
    return session.query(APIKey).all()

# Home endpoint
@app.get("/")
async def home():
    return {"Message": "Welcome"}

# Main function to run the app
if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')