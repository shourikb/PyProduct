# for type annotations
from typing import List 

from fastapi import FastAPI

# using our db.py file
import db


app = FastAPI()

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
    query = db.users.insert().values(username=user.username, email=user.email, full_name=user.full_name, disabled=user.disabled)
    last_record_id = await db.database.execute(query)
    return {**user.dict(), "id": last_record_id}



# Authentication?
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")