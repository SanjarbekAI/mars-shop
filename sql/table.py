import sqlite3


conn = sqlite3.connect('./sql/shop.db')
cursor = conn.cursor()

# query = """
# CREATE TABLE users (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# full_name TEXT NOT NULL,
# phone_number TEXT NOT NULL,
# login TEXT NOT NUll,
# password TEXT NOT NULL,
# chat_id INTEGER NOT NULL
# )
# """
query = """
CREATE TABLE products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
info TEXT NOT NULL,
photo TEXT NOT NULL,
price REAL NOT NUll,
status TEXT,
chat_id INTEGER NOT NULL
)
"""

cursor.execute(query)
conn.commit()