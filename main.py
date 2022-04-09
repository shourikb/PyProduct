# for type annotations
from typing import List 

from fastapi import FastAPI, Depends

# using our modules
from users import User, UserInDB
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



# /users/ endpoint functions

# get request for list of all users from database
# possibly should change to a username or indexed based system to get users
@app.get("/users/", response_model=List[User])
async def get_users():
    query = db.usersTable.select()
    return await db.database.fetch_all(query)

# adds a new user to the database
@app.post("/users/create", response_model=User)
async def create_user(user: UserInDB):
    query = db.usersTable.insert().values(username=user.username, hashed_password=user.hashed_password, email=user.email, full_name=user.full_name, disabled=user.disabled)
    last_record_id = await db.database.execute(query)
    return {**user.dict(), "id": last_record_id}



# OAuth2 Authentication Flow
from datetime import timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from users_oauth import *

@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}


# import secrets
# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBasic, HTTPBasicCredentials

# security = HTTPBasic()

# def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
#     correct_password = secrets.compare_digest(credentials.password, "swordfish")
#     if not (correct_username and correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username


# @app.get("/users/me")
# def read_current_user(username: str = Depends(get_current_username)):
#     return {"username": username}

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
