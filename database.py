import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db_connection():
    connection= sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_db_connection()
    
    connection.execute("""
                       CREATE TABLE IF NOT EXISTS users (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           email TEXT NOT NULL UNIQUE,
                           password_hash TEXT NOT NULL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
    """)
    
    connection.commit()
    connection.close()