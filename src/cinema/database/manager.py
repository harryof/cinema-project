"""Работа с базой sqlite."""
import os
import sqlite3

from config import DB_PATH
from src.cinema.exceptions import DatabaseError


class DatabaseManager:
    """Открывает базу и сам её закрывает, работает через with."""

    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = None

    def __enter__(self):
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row  # чтоб доставать колонки по имени
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()  # если упали, ничего не сохраняем
            self.conn.close()
        return False

    def init_db(self):
        """Создаёт таблицы из schema.sql."""
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def execute(self, sql, params=()):
        """Запрос в базу."""
        if self.conn is None:
            raise DatabaseError("база не открыта, используй with")
        return self.conn.execute(sql, params)

    def fetch_all(self, sql, params=()):
        """Запрос, вернёт список строк."""
        return self.execute(sql, params).fetchall()

    def fetch_one(self, sql, params=()):
        """Запрос, вернёт одну строку."""
        return self.execute(sql, params).fetchone()
