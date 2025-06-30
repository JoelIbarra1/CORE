import sqlite3
from contextlib import contextmanager

DATABASE = "compatibility_app.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    # Aquí puedes mover toda la lógica para crear las tablas
    pass
