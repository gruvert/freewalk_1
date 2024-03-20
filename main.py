from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pydantic import BaseModel

class ChangeData(BaseModel):
    arg: int

connection = sqlite3.connect('Restaurants.db', check_same_thread=False)
cursor = connection.cursor()


app = FastAPI()
templates = Jinja2Templates(directory='templates')
@app.get('/restaurants/{id}')
def main(request:Request, id:int):
    user = get_by_id(id)
    if user is None:
        return templates.TemplateResponse(request=request, name = 'sitepage.html', context={'free_places':list(range(1, 2)), 'taken_places':list(range(2, 4))})
    free_places = user['free_places']
    count_places = user['count_places']
    return templates.TemplateResponse(request=request, name = 'sitepage.html', context={'id':id, 'free_places':list(range(1, free_places+1)), 'taken_places':list(range(free_places+1, count_places+1))})

@app.put('/change/{id}')
def change_table(request:Request, id:int, data: ChangeData):
    n = int(data.arg)
    user = get_by_id(id)
    print(n)
    user = get_by_id(id)
    if n == 1:
        update_info(user['id'],user['free_places']+1)
    else:
        update_info(user['id'], user['free_places']-1)


def get_by_id(id:int):
    users_list = get_info()
    for user in users_list:
        if user['id'] == id:
            return user
    return None
#Отримання користувачів у вигляді списку зі словників
#де елементи словника - параметри юзера
def get_info():
    cursor.execute('SELECT * FROM Restaurants')
    users = cursor.fetchall()

    users_list = []
    for user in users:
        user_dict = {
            'id': int(user[0]),
            'name': user[1],
            'adress': user[2],
            'password': user[3],
            'count_places': int(user[4]),
            'free_places': int(user[5]),
            'short_topic': user[6]}
        users_list.append(user_dict)
    print(users_list)
    return users_list

#Оновлення даних в самій базі. Якщо ви хочете змінити лише один параметр, то вписуєте старі параметри та
#новий, він зміниться, старі залишаться.
def update_info(id, free_places):
    cursor.execute('UPDATE Restaurants SET free_places = ? WHERE id = ?',
                   (free_places, id))
    
    connection.commit()
