from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import Rest_DB

app = FastAPI()

class User(BaseModel):
    name: str
    short_description: str
    adress: str
    count_places: int
    email: str
    password: str

@app.post("/register/")
async def register(resto_data: User):
    if any(resto_data.email == user['email'] for user in Rest_DB.get_info("a")):
        raise HTTPException(status_code=400, detail="This email is already registered")
    Rest_DB.add_user(resto_data.name, resto_data.short_description, resto_data.adress,
resto_data.count_places, resto_data.email, resto_data.password)
    return {"message": "Restaurant registered successfully", "restaurant": resto_data}

@app.post("/login/")
async def login(resto_data: User):
    for index, resto in enumerate(Rest_DB.get_info("a")): # resto is a dict
        if resto['email'] == resto_data.email:
            if resto['password'] == resto_data.password:
                restaurant = Rest_DB.get_info(index)
                return {"message": "Successful login", "restaurant": restaurant}
            raise HTTPException(status_code=401, detail="Invalid password")
        raise HTTPException(status_code=401, detail="Invalid email")
    return {"message": "Successful login", "restaurant": restaurant}
