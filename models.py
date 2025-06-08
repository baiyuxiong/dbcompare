import sqlite3
from dataclasses import dataclass
from typing import Optional
import json
from datetime import datetime

@dataclass
class Connection:
    id: Optional[int]
    name: str
    type: str  # 'mysql' or 'agent'
    config: dict
    last_used: datetime
    created_at: datetime

@dataclass
class History:
    id: Optional[int]
    side: str  # 'left' or 'right'
    type: str  # 'file' or 'connection'
    value: str  # file path or connection name
    display: str  # display text
    last_used: datetime

class ConnectionManager:
    def __init__(self, db_path: str = "connections.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    config TEXT NOT NULL,
                    last_used TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    side TEXT NOT NULL,
                    type TEXT NOT NULL,
                    value TEXT NOT NULL,
                    display TEXT NOT NULL,
                    last_used TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    def add_connection(self, connection: Connection) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO connections (name, type, config, last_used, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                connection.name,
                connection.type,
                json.dumps(connection.config),
                connection.last_used.isoformat(),
                connection.created_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def update_connection(self, connection: Connection):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE connections
                SET name = ?, type = ?, config = ?, last_used = ?
                WHERE id = ?
            """, (
                connection.name,
                connection.type,
                json.dumps(connection.config),
                connection.last_used.isoformat(),
                connection.id
            ))
            conn.commit()

    def delete_connection(self, connection_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
            conn.commit()

    def get_connection(self, connection_id: int) -> Optional[Connection]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM connections WHERE id = ?", (connection_id,))
            row = cursor.fetchone()
            if row:
                return Connection(
                    id=row[0],
                    name=row[1],
                    type=row[2],
                    config=json.loads(row[3]),
                    last_used=datetime.fromisoformat(row[4]),
                    created_at=datetime.fromisoformat(row[5])
                )
            return None

    def get_all_connections(self) -> list[Connection]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM connections ORDER BY last_used DESC")
            return [
                Connection(
                    id=row[0],
                    name=row[1],
                    type=row[2],
                    config=json.loads(row[3]),
                    last_used=datetime.fromisoformat(row[4]),
                    created_at=datetime.fromisoformat(row[5])
                )
                for row in cursor.fetchall()
            ]

    def add_history(self, history: History) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history (side, type, value, display, last_used)
                VALUES (?, ?, ?, ?, ?)
            """, (
                history.side,
                history.type,
                history.value,
                history.display,
                history.last_used.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def get_history(self, side: str, limit: int = 10) -> list[History]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM history 
                WHERE side = ? 
                ORDER BY last_used DESC 
                LIMIT ?
            """, (side, limit))
            return [
                History(
                    id=row[0],
                    side=row[1],
                    type=row[2],
                    value=row[3],
                    display=row[4],
                    last_used=datetime.fromisoformat(row[5])
                )
                for row in cursor.fetchall()
            ]

    def update_history_last_used(self, history_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE history 
                SET last_used = ? 
                WHERE id = ?
            """, (datetime.now().isoformat(), history_id))
            conn.commit() 