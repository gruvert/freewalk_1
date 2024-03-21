from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form
from pydantic import BaseModel
import sqlite3
#З'єднання з базою даних та створення "курсора"
#Курсор - те, що дозволяє "рухатись" по базі даних
connection = sqlite3.connect('Restaurants.db')
cursor = connection.cursor()

#Cтворення таблиці з параметрами
#Ім'я, адрес, пароль, кількість місць, короткий опис
#Таблиця створюється автоматично при запуску файла
#Для відображення бази даних існує DB Browser (SQLite)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Restaurants (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
adress TEXT NOT NULL,
password TEXT NOT NULL,
count_places INTEGER NOT NULL,
short_topic TEXT NOT NULL
)
''')

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

#Функція дозволяє додати нового юзера \_(0_0)_/
def add_user(name, short_topic, adress, count_places, email, password):
    cursor.execute('INSERT INTO Restaurants (name, adress, password, count_places, free_places, short_topic) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, short_topic, adress, count_places, email, password,))
    connection.commit()

# Приклад виклику функції:

#Видалення юзера за іменем
def dell_user(user_name):
    cursor.execute('DELETE FROM Restaurants WHERE name =?', (user_name,))
    # cursor.commit()

#Отримання користувачів у вигляді списку зі словників
#де елементи словника - параметри юзера
def get_info(a):
    cursor.execute('SELECT * FROM Restaurants')
    users = cursor.fetchall()
    if a:
        for user in users:
            if user[0] == a:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'short_description': user[2],
                    'adress': user[3],
                    'count_places': user[4],
                    'email' : user[5],
                    "password": user[6]}
        return user_dict
    else:
        users_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'short_description': user[2],
                'adress': user[3],
                'count_places': user[4],
                'email' : user[5],
                "password": user[6]}
            users_list.append(user_dict)
        return users_list

#Оновлення даних в самій базі. Якщо ви хочете змінити лише один параметр, то вписуєте старі параметри та
#новий, він зміниться, старі залишаться.
def update_info(name, adress, password, coun_places, free_places, short_topic, id):
    cursor.execute('UPDATE Restaurants SET name = ?, adress = ?, password = ?, count_places =?, free_places =? short_topic = ? WHERE id = ?',
                   (name, adress, password, coun_places, free_places, short_topic, id))
    cursor.commit()
    
class User(BaseModel):
    name: str
    short_description: str
    address: str
    count_places: int
    email: str
    password: str



@app.post("/register/", response_class=HTMLResponse)
async def register(request: Request, name: str = Form(...), short_description: str = Form(...), address: str = Form(...), count_places: int = Form(...), email: str = Form(...), password: str = Form(...)):
    add_user(name, short_description, address, count_places, email, password)
    print(get_info(0))
    return 
    # print(get_info(0))
    # print(name, short_description, address, count_places, email, password)
    # Ваш код для обробки форми тут

# async def register(request: Request, resto_data: str):
#     resto_data = resto_data.split('&')
#     resto_keys = ['name', 'short_description', 'address', 'count_places', 'email', 'password']
#     resto_data_dict = {}
#     for section in resto_data:
#         for category in resto_keys:
#             resto_data_dict[category] = section
#         break
#     if any(resto_data.email == user['email'] for user in get_info("a")):
#         raise HTTPException(status_code=400, detail="This email is already registered")
#     add_user(resto_data.name, resto_data.short_description, resto_data.address,
#                      resto_data.count_places, resto_data.email, resto_data.password)
#     return templates.TemplateResponse(request=request, name = "registration.html", context={"request": request, "message": "Restaurant registered successfully", "restaurant": resto_data})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    for index, resto in enumerate(get_info(0)): # resto is a dict
        if resto['email'] == email:
            if resto['password'] == password:
                restaurant = get_info(index+1)
                print(restaurant)
                return 
            raise HTTPException(status_code=401, detail="Invalid password")
        raise HTTPException(status_code=401, detail="Invalid email")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# add_user("Назва ресторану", "Адреса рсторану", "Секретний_пароль", 50, 20, "Коротка_тема")
