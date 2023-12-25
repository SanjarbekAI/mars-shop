import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()


async def get_all_products():
    query = "SELECT * FROM products WHERE status = 'active'"
    products = cursor.execute(query).fetchall()
    return products