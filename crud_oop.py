import sqlite3
from abc import ABC, abstractmethod
from contextlib import closing


class BaseCRUD(ABC):
    def __init__(self, database_path, table_name):
        self.database_path = database_path
        self.table_name = table_name

    def get_connection(self):
        return closing(sqlite3.connect(self.database_path))

    def insert(self, **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join('?' for _ in kwargs)
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(kwargs.values()))
            connection.commit()
            return cursor.lastrowid

    def get(self, id, id_column="id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (id,))
            return cursor.fetchone()

    def update(self, id, id_column="id", **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(f"{key}=?" for key in kwargs)
            query = f"UPDATE {self.table_name} SET {columns} WHERE {id_column}=?"
            cursor.execute(query, (*kwargs.values(), id))
            connection.commit()

    def delete(self, id, id_column="id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (id,))
            connection.commit()
