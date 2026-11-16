import sqlite3

DATABASE = "recipes.db"
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

connection.commit()
connection.close()
print("Database initialized with recipes and users tables.")
