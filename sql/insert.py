import sqlite3

conn = sqlite3.connect('./sql/shop.db')
cursor = conn.cursor()


async def insert_product(data: dict):
    name = data['name']
    price = data['price']
    photo = data['photo']
    chat_id = data['chat_id']
    status = data['status']
    info = data['info']

    query = "INSERT INTO products (name, price, photo, chat_id, status, info) VALUES (?,?,?,?,?,?)"
    values = (name, price, photo, chat_id, status, info)

    cursor.execute(query, values)
    conn.commit()
    return True


async def insert_user(data: dict):
    full_name = data['full_name']
    login = data['login']
    password = data['password']
    phone_number = data['phone_number']
    chat_id = data['chat_id']

    query = "INSERT INTO users (full_name, login, password, chat_id, phone_number) VALUES (?,?,?,?,?)"
    values = (full_name, login, password, chat_id, phone_number)

    cursor.execute(query, values)
    conn.commit()
    return True
