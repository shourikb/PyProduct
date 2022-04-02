# for type annotations
from select import select
from typing import List 

from fastapi import FastAPI

# using our db.py file
import db


app = FastAPI()
# run server with: uvicorn main:app --reload

# / root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Database Functions 

# Event handlers for database startup/shutdown
@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()



# /user/ endpoint functions

# get request for list of all users from database
# possibly should change to a username or indexed based system to get users
@app.get("/users/", response_model=List[db.User])
async def get_users():
    query = db.users.select()
    return await db.database.fetch_all(query)

# adds a new user to the database
@app.post("/users/", response_model=db.User)
async def create_user(user: db.UserIn):
    query = db.users.insert().values(username=user.username, password=user.password, email=user.email, full_name=user.full_name, disabled=user.disabled)
    last_record_id = await db.database.execute(query)
    return {**user.dict(), "id": last_record_id}



# Authentication?
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

# def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    
#     selected_user = db.get_user_from_cred(credentials.username, credentials.password)
#     if selected_user is None:
#         return
#     correct_username = secrets.compare_digest(credentials.username, selected_user[1])
#     correct_password = secrets.compare_digest(credentials.password, selected_user[2])
#     if not (correct_username and correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username
    
# @app.get("/users/login")
# def read_current_user(username: str = Depends(get_current_username)):
#     return {"username": username, "isAuthenticated": True, "detail": "Is Authenticated"}