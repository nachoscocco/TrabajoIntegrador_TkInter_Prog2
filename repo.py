import sqlite3
from typing import Dict, List, Optional, Tuple

class Repository:
    def __init__(self, db_name: str, table_name: str, fields: List[dict]):
        self.db_name = db_name
        self.table_name = table_name
        # Extraemos solo los nombres de los campos para las columnas
        self.field_names = [f["name"] for f in fields]
        self._init_db()

    def _init_db(self):
        # Crea la tabla si no existe con las columnas generadas dinámicamente
        columns = ", ".join([f"{name} TEXT" for name in self.field_names])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(query)

    def add(self, record: dict) -> int:
        columns = ", ".join(self.field_names)
        placeholders = ", ".join(["?"] * len(self.field_names))
        values = tuple(record.get(name, "") for name in self.field_names)
        
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query, values)
            return cursor.lastrowid

    def get(self, record_id: int) -> Optional[dict]:
        query = f"SELECT id, {', '.join(self.field_names)} FROM {self.table_name} WHERE id = ?"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query, (record_id,))
            row = cursor.fetchone()
            if row:
                return dict(zip(self.field_names, row[1:]))
            return None

    def get_all(self) -> List[Tuple[int, dict]]:
        query = f"SELECT id, {', '.join(self.field_names)} FROM {self.table_name}"
        results = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query)
            for row in cursor.fetchall():
                record_id = row[0]
                record = dict(zip(self.field_names, row[1:]))
                results.append((record_id, record))
        return results

    def update(self, record_id: int, record: dict) -> bool:
        set_clause = ", ".join([f"{name} = ?" for name in self.field_names])
        values = tuple(record.get(name, "") for name in self.field_names) + (record_id,)
        
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query, values)
            return cursor.rowcount > 0

    def delete(self, record_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query, (record_id,))
            return cursor.rowcount > 0
