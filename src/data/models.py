import sqlite3
import os
import sys
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
    created_at: datetime
    updated_at: datetime

@dataclass
class History:
    id: Optional[int]
    side: str  # 'left' or 'right'
    type: str  # 'file' or 'connection'
    value: str  # file path or connection name
    display: str  # display text
    last_used: datetime

@dataclass
class AppConfig:
    id: Optional[int]
    key: str  # 配置键
    value: str  # 配置值
    created_at: datetime
    updated_at: datetime

class ConnectionManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = self._get_db_path()
        else:
            self.db_path = db_path
        self._init_db()
    
    def _get_db_path(self):
        """获取数据库文件路径，在打包环境中使用用户目录"""
        if getattr(sys, 'frozen', False):
            # 打包环境，使用用户目录
            import platform
            if platform.system() == "Darwin":  # macOS
                # 使用 ~/Library/Application Support/DBCompare/
                app_support = os.path.expanduser("~/Library/Application Support/DBCompare")
                if not os.path.exists(app_support):
                    os.makedirs(app_support, exist_ok=True)
                return os.path.join(app_support, "connections.db")
            elif platform.system() == "Windows":
                # 使用 %APPDATA%/DBCompare/
                app_data = os.path.join(os.environ.get('APPDATA', ''), 'DBCompare')
                if not os.path.exists(app_data):
                    os.makedirs(app_data, exist_ok=True)
                return os.path.join(app_data, "connections.db")
            else:  # Linux
                # 使用 ~/.config/DBCompare/
                config_dir = os.path.expanduser("~/.config/DBCompare")
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir, exist_ok=True)
                return os.path.join(config_dir, "connections.db")
        else:
            # 开发环境，使用当前目录
            return "connections.db"

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    config TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    def add_connection(self, connection: Connection) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO connections (name, type, config, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                connection.name,
                connection.type,
                json.dumps(connection.config),
                connection.created_at.isoformat(),
                connection.updated_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def update_connection(self, connection: Connection):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE connections
                SET name = ?, type = ?, config = ?, updated_at = ?
                WHERE id = ?
            """, (
                connection.name,
                connection.type,
                json.dumps(connection.config),
                connection.updated_at.isoformat(),
                connection.id
            ))
            conn.commit()

    def delete_connection(self, connection_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 删除连接
            cursor.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
            # 删除相关的历史记录
            cursor.execute("DELETE FROM history WHERE type = 'connection' AND value = ?", (str(connection_id),))
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
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(row[5])
                )
            return None

    def get_all_connections(self) -> list[Connection]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM connections ORDER BY updated_at DESC")
            return [
                Connection(
                    id=row[0],
                    name=row[1],
                    type=row[2],
                    config=json.loads(row[3]),
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(row[5])
                )
                for row in cursor.fetchall()
            ]

    def add_history(self, history: History) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 如果当前连接在之前的历史记录中已存在，则删除旧记录
            # 保证历史记录中，同样的连接只有一个
            cursor.execute("""
                DELETE FROM history 
                WHERE side = ? AND type = ? AND value = ?
            """, (history.side, history.type, history.value))
            
            # 添加新的历史记录
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

    def get_config(self, key: str, default: str = None) -> str:
        """获取配置值"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM app_config WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def set_config(self, key: str, value: str):
        print(f"set_config: {key} = {value}")
        """设置配置值"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            # 检查配置是否存在
            cursor.execute("SELECT id FROM app_config WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if row:
                # 更新现有配置
                cursor.execute("""
                    UPDATE app_config
                    SET value = ?, updated_at = ?
                    WHERE key = ?
                """, (value, now, key))
            else:
                # 创建新配置
                cursor.execute("""
                    INSERT INTO app_config (key, value, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (key, value, now, now))
            
            conn.commit()

    def update_history_display_format(self):
        """更新历史记录的显示格式，添加数据库名称"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 获取所有连接类型的历史记录
            cursor.execute("SELECT h.id, h.value, c.config FROM history h JOIN connections c ON h.value = c.id WHERE h.type = 'connection'")
            rows = cursor.fetchall()
            
            for row in rows:
                history_id, connection_id, config_json = row
                try:
                    config = json.loads(config_json)
                    # 获取连接信息
                    conn_obj = self.get_connection(connection_id)
                    if conn_obj and conn_obj.type == "mysql":
                        database_name = config.get('database', '')
                        if database_name:
                            new_display = f"{conn_obj.name} ({config['host']}:{config['port']}/{database_name})"
                        else:
                            new_display = f"{conn_obj.name} ({config['host']}:{config['port']})"
                        
                        # 更新显示文本
                        cursor.execute("UPDATE history SET display = ? WHERE id = ?", (new_display, history_id))
                except Exception:
                    # 如果解析失败，跳过这条记录
                    continue
            
            conn.commit() 