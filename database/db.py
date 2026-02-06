import sqlite3
from threading import Lock

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.cursor = None
        self.lock = Lock()

    def __del__(self):
        self.connection.close()

    def create_database(self, schema: dict):
        req = ""
        self.cursor = self.connection.cursor()
        for item in schema['database']['tables']:
            table_name, table_def = next(iter(item.items()))
            fields = table_def["fields"]
            cols = []
            for f in fields:
                col_name, col_def = next(iter(f.items()))
                cols.append(f'"{col_name}" {col_def}')

            req = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(cols)});'
            self.cursor.execute(req)

        self.connection.commit()


