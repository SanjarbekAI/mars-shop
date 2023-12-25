import sqlite3

conn = sqlite3.connect('shop.db')
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
