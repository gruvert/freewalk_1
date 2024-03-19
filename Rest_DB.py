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
free_places INTEGER NOT NULL,
short_topic TEXT NOT NULL
)
''')

#Функція дозволяє додати нового юзера \_(0_0)_/
def add_user(name, adress, password, count_places, email, short_topic):
    cursor.execute('INSERT INTO Restaurants (name, adress, password, count_places, free_places, short_topic) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, short_topic, adress, count_places, email, password,))
    # cursor.commit()

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
                    'adress': user[2],
                    'password': user[3],
                    'count_places': user[4],
                    'free_places': user[5],
                    'short_topic': user[6]}
                return user_dict
    else:
        users_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'adress': user[2],
                'password': user[3],
                'count_places': user[4],
                'free_places': user[5],
                'short_topic': user[6]}
            users_list.append(user_dict)
        return users_list

#Оновлення даних в самій базі. Якщо ви хочете змінити лише один параметр, то вписуєте старі параметри та
#новий, він зміниться, старі залишаться.
def update_info(name, adress, password, coun_places, free_places, short_topic, id):
    cursor.execute('UPDATE Restaurants SET name = ?, adress = ?, password = ?, count_places =?, free_places =? short_topic = ? WHERE id = ?',
                   (name, adress, password, coun_places, free_places, short_topic, id))
    cursor.commit()

# add_user("Назва ресторану", "Адреса рсторану", "Секретний_пароль", 50, 20, "Коротка_тема")
