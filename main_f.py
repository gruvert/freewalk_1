from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import Rest_DB

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    name: str
    short_description: str
    address: str
    count_places: int
    email: str
    password: str

@app.post("/register/", response_class=HTMLResponse)
async def register(request: Request, resto_data: User):
    if any(resto_data.email == user['email'] for user in Rest_DB.get_info("a")):
        raise HTTPException(status_code=400, detail="This email is already registered")
    Rest_DB.add_user(resto_data.name, resto_data.short_description, resto_data.address,
                     resto_data.count_places, resto_data.email, resto_data.password)
    return templates.TemplateResponse("index.html", {"request": request, "message": "Restaurant registered successfully", "restaurant": resto_data})

@app.get("/Log in/", response_class=HTMLResponse)
async def login(request: Request, resto_data: User):
    for index, resto in enumerate(Rest_DB.get_info("a")): # resto is a dict
        if resto['email'] == resto_data.email:
            if resto['password'] == resto_data.password:
                restaurant = Rest_DB.get_info(index)
                return templates.TemplateResponse("login.html", {"request": request, "message": "Successful login", "restaurant": restaurant})
            raise HTTPException(status_code=401, detail="Invalid password")
        raise HTTPException(status_code=401, detail="Invalid email")
    return templates.TemplateResponse("log_in.html", context={"request": request, "message": "Successful login", "restaurant": restaurant})
# print(Rest_DB.get_info(0))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    


