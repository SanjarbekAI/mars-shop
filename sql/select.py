import sqlite3

conn = sqlite3.connect('./sql/shop.db')
cursor = conn.cursor()


async def get_all_products():
    query = "SELECT * FROM products WHERE status = 'active'"
    products = cursor.execute(query).fetchall()
    return products


async def get_user_all_products(chat_id: int):
    query = f"SELECT * FROM products WHERE status = 'active' AND chat_id = {chat_id}"
    products = cursor.execute(query).fetchall()
    return products


async def get_user(chat_id: int):
    query = f"SELECT * FROM users WHERE chat_id={chat_id}"
    user = cursor.execute(query).fetchone()
    return user