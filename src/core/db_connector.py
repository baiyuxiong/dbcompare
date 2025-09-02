import mysql.connector
import psycopg2
from typing import Dict, Any, Optional, List, Set
from utils.util import normalize_sql_definition

class BaseDBConnector:
    """数据库连接器基类"""
    
    def __init__(self):
        self.connection = None
        
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到数据库，子类必须实现"""
        raise NotImplementedError
        
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构，子类必须实现"""
        raise NotImplementedError
        
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

class MySQLConnector(BaseDBConnector):
    """MySQL数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到MySQL数据库"""
        try:
            self.connection = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
        except Exception as e:
            raise Exception(f"连接MySQL数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor(dictionary=True)
        tables = {}
        
        try:
            # 获取所有表名
            cursor.execute("SHOW TABLES")
            table_names = [row[f'Tables_in_{self.connection.database}'] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取表结构
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table_sql = cursor.fetchone()['Create Table']
                
                # 获取列信息
                cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
                columns = {}
                for col in cursor.fetchall():
                    col_name = col['Field']
                    col_type = col['Type']
                    col_null = 'NULL' if col['Null'] == 'YES' else 'NOT NULL'
                    col_default = f"DEFAULT {col['Default']}" if col['Default'] is not None else ''
                    col_extra = col['Extra']
                    col_comment = f"COMMENT '{col['Comment']}'" if col['Comment'] else ''
                    
                    # 组合列定义 
                    col_def = f"{col_type} {col_null} {col_default} {col_extra} {col_comment}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": col['Type'],
                            "Collation": col['Collation'],
                            "Null": col['Null'],
                            "Key": col['Key'],
                            "Default": col['Default'],
                            "Extra": col['Extra'],
                            "Comment": col['Comment'],
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"SHOW INDEX FROM `{table_name}`")
                indexes = {}
                for idx in cursor.fetchall():
                    idx_name = idx['Key_name']
                    if idx_name == 'PRIMARY':
                        idx_type = 'PRIMARY KEY'
                    elif idx['Non_unique'] == 0:
                        idx_type = 'UNIQUE KEY'
                    else:
                        idx_type = 'KEY'
                        
                    if idx_name not in indexes:
                        indexes[idx_name] = {
                            'type': idx_type,
                            'columns': idx['Column_name']
                        }
                    else:
                        # 如果索引包含多个列，将它们组合起来
                        indexes[idx_name]['columns'] += f", {idx['Column_name']}"
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables

class PostgreSQLConnector(BaseDBConnector):
    """PostgreSQL数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到PostgreSQL数据库"""
        try:
            self.connection = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
        except Exception as e:
            raise Exception(f"连接PostgreSQL数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # 获取所有表名（排除系统表）
            cursor.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                ORDER BY tablename
            """)
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取表结构
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default, 
                           character_maximum_length, numeric_precision, numeric_scale,
                           udt_name, col_description((table_schema||'.'||table_name)::regclass, ordinal_position) as comment
                    FROM information_schema.columns 
                    WHERE table_name = %s AND table_schema = 'public'
                    ORDER BY ordinal_position
                """, (table_name,))
                
                columns = {}
                for col in cursor.fetchall():
                    col_name = col[0]
                    col_type = col[1]
                    is_nullable = col[2]
                    col_default = col[3]
                    char_max_length = col[4]
                    numeric_precision = col[5]
                    numeric_scale = col[6]
                    udt_name = col[7]
                    comment = col[8]
                    
                    # 构建完整的类型定义
                    full_type = self._build_postgresql_type(col_type, char_max_length, numeric_precision, numeric_scale)
                    
                    # 构建列定义
                    col_null = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                    col_default_str = f"DEFAULT {col_default}" if col_default else ''
                    col_comment = f"COMMENT '{comment}'" if comment else ''
                    
                    col_def = f"{full_type} {col_null} {col_default_str} {col_comment}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": full_type,
                            "Null": is_nullable,
                            "Default": col_default,
                            "Comment": comment,
                            "UDT": udt_name,
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"""
                    SELECT 
                        i.relname as index_name,
                        a.attname as column_name,
                        ix.indisunique as is_unique,
                        ix.indisprimary as is_primary
                    FROM pg_class t, pg_class i, pg_index ix, pg_attribute a
                    WHERE t.oid = ix.indrelid 
                        AND i.oid = ix.indexrelid 
                        AND a.attrelid = t.oid 
                        AND a.attnum = ANY(ix.indkey)
                        AND t.relkind = 'r'
                        AND t.relname = %s
                    ORDER BY i.relname, a.attnum
                """, (table_name,))
                
                indexes = {}
                for idx in cursor.fetchall():
                    idx_name = idx[0]
                    col_name = idx[1]
                    is_unique = idx[2]
                    is_primary = idx[3]
                    
                    if is_primary:
                        idx_type = 'PRIMARY KEY'
                    elif is_unique:
                        idx_type = 'UNIQUE KEY'
                    else:
                        idx_type = 'KEY'
                        
                    if idx_name not in indexes:
                        indexes[idx_name] = {
                            'type': idx_type,
                            'columns': col_name
                        }
                    else:
                        # 如果索引包含多个列，将它们组合起来
                        indexes[idx_name]['columns'] += f", {col_name}"
                
                # 生成CREATE TABLE语句（简化版）
                create_table_sql = self._generate_create_table_sql(table_name, columns, indexes)
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables
    
    def _build_postgresql_type(self, base_type: str, char_max_length: Optional[int], 
                              numeric_precision: Optional[int], numeric_scale: Optional[int]) -> str:
        """构建PostgreSQL类型定义"""
        if base_type in ('character varying', 'varchar'):
            if char_max_length:
                return f"VARCHAR({char_max_length})"
            return "VARCHAR"
        elif base_type in ('character', 'char'):
            if char_max_length:
                return f"CHAR({char_max_length})"
            return "CHAR"
        elif base_type in ('numeric', 'decimal'):
            if numeric_precision and numeric_scale:
                return f"DECIMAL({numeric_precision},{numeric_scale})"
            elif numeric_precision:
                return f"DECIMAL({numeric_precision})"
            return "DECIMAL"
        elif base_type == 'timestamp without time zone':
            return "TIMESTAMP"
        elif base_type == 'timestamp with time zone':
            return "TIMESTAMPTZ"
        elif base_type == 'time without time zone':
            return "TIME"
        elif base_type == 'time with time zone':
            return "TIMETZ"
        else:
            return base_type.upper()
    
    def _generate_create_table_sql(self, table_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句"""
        sql_parts = [f"CREATE TABLE {table_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class OracleConnector(BaseDBConnector):
    """Oracle数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到Oracle数据库"""
        try:
            import cx_Oracle
            # 构建连接字符串
            if 'service_name' in config:
                dsn = cx_Oracle.makedsn(
                    config['host'], 
                    config['port'], 
                    service_name=config['service_name']
                )
            else:
                dsn = cx_Oracle.makedsn(
                    config['host'], 
                    config['port'], 
                    sid=config.get('sid', '')
                )
            
            self.connection = cx_Oracle.connect(
                user=config['user'],
                password=config['password'],
                dsn=dsn
            )
        except ImportError:
            raise Exception("Oracle驱动未安装，请先安装cx_Oracle: pip install cx_Oracle")
        except Exception as e:
            raise Exception(f"连接Oracle数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # 获取当前用户的表
            cursor.execute("""
                SELECT table_name 
                FROM user_tables 
                ORDER BY table_name
            """)
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取列信息
                cursor.execute(f"""
                    SELECT column_name, data_type, data_length, data_precision, data_scale,
                           nullable, data_default, comments
                    FROM user_col_comments uc
                    LEFT JOIN user_tab_columns utc ON uc.table_name = utc.table_name 
                        AND uc.column_name = utc.column_name
                    WHERE uc.table_name = :table_name
                    ORDER BY utc.column_id
                """, table_name=table_name)
                
                columns = {}
                for col in cursor.fetchall():
                    col_name = col[0]
                    col_type = col[1]
                    data_length = col[2]
                    data_precision = col[3]
                    data_scale = col[4]
                    nullable = col[5]
                    data_default = col[6]
                    comments = col[7]
                    
                    # 构建类型定义
                    full_type = self._build_oracle_type(col_type, data_length, data_precision, data_scale)
                    
                    # 构建列定义
                    col_null = 'NULL' if nullable == 'Y' else 'NOT NULL'
                    col_default = f"DEFAULT {data_default}" if data_default else ''
                    col_comment = f"COMMENT '{comments}'" if comments else ''
                    
                    col_def = f"{full_type} {col_null} {col_default} {col_comment}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": full_type,
                            "Null": nullable,
                            "Default": data_default,
                            "Comment": comments,
                            "Length": data_length,
                            "Precision": data_precision,
                            "Scale": data_scale,
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"""
                    SELECT index_name, uniqueness, column_name
                    FROM user_ind_columns uic
                    JOIN user_indexes ui ON uic.index_name = ui.index_name
                    WHERE uic.table_name = :table_name
                    ORDER BY uic.index_name, uic.column_position
                """, table_name=table_name)
                
                indexes = {}
                for idx in cursor.fetchall():
                    idx_name = idx[0]
                    uniqueness = idx[1]
                    col_name = idx[2]
                    
                    if idx_name == 'SYS_C':
                        continue  # 跳过系统生成的索引
                    
                    if 'UNIQUE' in uniqueness:
                        idx_type = 'UNIQUE KEY'
                    else:
                        idx_type = 'KEY'
                        
                    if idx_name not in indexes:
                        indexes[idx_name] = {
                            'type': idx_type,
                            'columns': col_name
                        }
                    else:
                        indexes[idx_name]['columns'] += f", {col_name}"
                
                # 生成CREATE TABLE语句
                create_table_sql = self._generate_create_table_sql(table_name, columns, indexes)
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables
    
    def _build_oracle_type(self, base_type: str, data_length: Optional[int], 
                          data_precision: Optional[int], data_scale: Optional[int]) -> str:
        """构建Oracle类型定义"""
        if base_type in ('VARCHAR2', 'VARCHAR'):
            if data_length:
                return f"VARCHAR2({data_length})"
            return "VARCHAR2"
        elif base_type in ('CHAR', 'NCHAR'):
            if data_length:
                return f"{base_type}({data_length})"
            return base_type
        elif base_type in ('NUMBER', 'NUMERIC'):
            if data_precision and data_scale:
                return f"NUMBER({data_precision},{data_scale})"
            elif data_precision:
                return f"NUMBER({data_precision})"
            return "NUMBER"
        elif base_type in ('DATE', 'TIMESTAMP'):
            return base_type
        else:
            return base_type
    
    def _generate_create_table_sql(self, table_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句"""
        sql_parts = [f"CREATE TABLE {table_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class SQLServerConnector(BaseDBConnector):
    """SQL Server数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到SQL Server数据库"""
        try:
            import pyodbc
            # 构建连接字符串
            if 'driver' in config:
                conn_str = f"DRIVER={{{config['driver']}}};SERVER={config['host']};PORT={config['port']};DATABASE={config['database']};UID={config['user']};PWD={config['password']}"
            else:
                conn_str = f"SERVER={config['host']};PORT={config['port']};DATABASE={config['database']};UID={config['user']};PWD={config['password']}"
            
            self.connection = pyodbc.connect(conn_str)
        except ImportError:
            raise Exception("SQL Server驱动未安装，请先安装pyodbc: pip install pyodbc")
        except Exception as e:
            raise Exception(f"连接SQL Server数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # 获取所有表名
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取列信息
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
                           NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE, 
                           COLUMN_DEFAULT, COLUMNPROPERTY(object_id(TABLE_SCHEMA + '.' + TABLE_NAME), COLUMN_NAME, 'IsIdentity') as IS_IDENTITY
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """, table_name)
                
                columns = {}
                for col in cursor.fetchall():
                    col_name = col[0]
                    col_type = col[1]
                    char_max_length = col[2]
                    numeric_precision = col[3]
                    numeric_scale = col[4]
                    is_nullable = col[5]
                    col_default = col[6]
                    is_identity = col[7]
                    
                    # 构建类型定义
                    full_type = self._build_sqlserver_type(col_type, char_max_length, numeric_precision, numeric_scale)
                    
                    # 构建列定义
                    col_null = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                    col_default = f"DEFAULT {col_default}" if col_default else ''
                    identity = 'IDENTITY(1,1)' if is_identity else ''
                    
                    col_def = f"{full_type} {col_null} {col_default} {identity}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": full_type,
                            "Null": is_nullable,
                            "Default": col_default,
                            "Identity": is_identity,
                            "Length": char_max_length,
                            "Precision": numeric_precision,
                            "Scale": numeric_scale,
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"""
                    SELECT i.name as index_name, i.is_unique, i.is_primary_key, c.name as column_name
                    FROM sys.indexes i
                    JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                    JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                    WHERE i.object_id = OBJECT_ID(?)
                    ORDER BY i.name, ic.key_ordinal
                """, table_name)
                
                indexes = {}
                for idx in cursor.fetchall():
                    idx_name = idx[0]
                    is_unique = idx[1]
                    is_primary = idx[2]
                    col_name = idx[3]
                    
                    if is_primary:
                        idx_type = 'PRIMARY KEY'
                    elif is_unique:
                        idx_type = 'UNIQUE KEY'
                    else:
                        idx_type = 'KEY'
                        
                    if idx_name not in indexes:
                        indexes[idx_name] = {
                            'type': idx_type,
                            'columns': col_name
                        }
                    else:
                        indexes[idx_name]['columns'] += f", {col_name}"
                
                # 生成CREATE TABLE语句
                create_table_sql = self._generate_create_table_sql(table_name, columns, indexes)
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables
    
    def _build_sqlserver_type(self, base_type: str, char_max_length: Optional[int], 
                             numeric_precision: Optional[int], numeric_scale: Optional[int]) -> str:
        """构建SQL Server类型定义"""
        if base_type in ('varchar', 'nvarchar'):
            if char_max_length == -1:
                return f"{base_type.upper()}(MAX)"
            elif char_max_length:
                return f"{base_type.upper()}({char_max_length})"
            return base_type.upper()
        elif base_type in ('char', 'nchar'):
            if char_max_length:
                return f"{base_type.upper()}({char_max_length})"
            return base_type.upper()
        elif base_type in ('decimal', 'numeric'):
            if numeric_precision and numeric_scale:
                return f"{base_type.upper()}({numeric_precision},{numeric_scale})"
            elif numeric_precision:
                return f"{base_type.upper()}({numeric_precision})"
            return base_type.upper()
        elif base_type in ('int', 'bigint', 'smallint', 'tinyint'):
            return base_type.upper()
        elif base_type in ('datetime', 'datetime2', 'date', 'time'):
            return base_type.upper()
        else:
            return base_type.upper()
    
    def _generate_create_table_sql(self, table_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句"""
        sql_parts = [f"CREATE TABLE {table_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class SQLiteConnector(BaseDBConnector):
    """SQLite数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到SQLite数据库"""
        try:
            import sqlite3
            db_path = config.get('database', config.get('file', ':memory:'))
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
        except ImportError:
            raise Exception("SQLite驱动未安装，请先安装sqlite3: pip install sqlite3")
        except Exception as e:
            raise Exception(f"连接SQLite数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取表结构
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = {}
                
                for col in cursor.fetchall():
                    col_name = col[1]
                    col_type = col[2]
                    not_null = col[3]
                    col_default = col[4]
                    primary_key = col[5]
                    
                    # 构建列定义
                    col_null = 'NOT NULL' if not_null else 'NULL'
                    col_default_str = f"DEFAULT {col_default}" if col_default else ''
                    primary_key_str = 'PRIMARY KEY' if primary_key else ''
                    
                    col_def = f"{col_type} {col_null} {col_default_str} {primary_key_str}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": col_type,
                            "Null": 'NO' if not_null else 'YES',
                            "Default": col_default,
                            "PrimaryKey": primary_key,
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = {}
                
                for idx in cursor.fetchall():
                    idx_name = idx[1]
                    is_unique = idx[2]
                    
                    # 获取索引列
                    cursor.execute(f"PRAGMA index_info({idx_name})")
                    idx_columns = []
                    for col_info in cursor.fetchall():
                        col_pos = col_info[2]
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        table_cols = cursor.fetchall()
                        if col_pos < len(table_cols):
                            idx_columns.append(table_cols[col_pos][1])
                    
                    if idx_columns:
                        if is_unique:
                            idx_type = 'UNIQUE KEY'
                        else:
                            idx_type = 'KEY'
                        
                        indexes[idx_name] = {
                            'type': idx_type,
                            'columns': ', '.join(idx_columns)
                        }
                
                # 生成CREATE TABLE语句
                create_table_sql = self._generate_create_table_sql(table_name, columns, indexes)
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables
    
    def _generate_create_table_sql(self, table_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句"""
        sql_parts = [f"CREATE TABLE {table_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class MongoDBConnector(BaseDBConnector):
    """MongoDB数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到MongoDB数据库"""
        try:
            from pymongo import MongoClient
            
            # 构建连接字符串
            if 'username' in config and 'password' in config:
                if 'auth_source' in config:
                    uri = f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?authSource={config['auth_source']}"
                else:
                    uri = f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            else:
                uri = f"mongodb://{config['host']}:{config['port']}/{config['database']}"
            
            self.connection = MongoClient(uri)
            self.database = self.connection[config['database']]
            
        except ImportError:
            raise Exception("MongoDB驱动未安装，请先安装pymongo: pip install pymongo")
        except Exception as e:
            raise Exception(f"连接MongoDB数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有集合的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        collections = {}
        
        try:
            # 获取所有集合名
            collection_names = self.database.list_collection_names()
            
            for collection_name in collection_names:
                # 获取集合的文档结构
                collection = self.database[collection_name]
                
                # 分析集合结构（基于样本文档）
                sample_docs = list(collection.find().limit(100))
                columns = self._analyze_mongodb_structure(sample_docs)
                
                # 获取索引信息
                indexes = self._get_mongodb_indexes(collection)
                
                # 生成CREATE TABLE语句（模拟）
                create_table_sql = self._generate_create_table_sql(collection_name, columns, indexes)
                
                collections[collection_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        except Exception as e:
            raise Exception(f"获取MongoDB集合结构失败: {str(e)}")
            
        return collections
    
    def _analyze_mongodb_structure(self, sample_docs: List[Dict]) -> Dict:
        """分析MongoDB文档结构"""
        columns = {}
        
        if not sample_docs:
            return columns
        
        # 分析所有文档的字段
        all_fields = set()
        for doc in sample_docs:
            all_fields.update(self._extract_fields(doc))
        
        # 为每个字段确定类型
        for field in all_fields:
            field_type = self._determine_field_type(sample_docs, field)
            columns[field] = {
                'raw': field_type,
                'normalized': normalize_sql_definition(field_type),
                'details': {
                    "Type": field_type,
                    "Null": "YES",  # MongoDB字段可以为空
                    "Default": None,
                    "Comment": f"MongoDB字段: {field}",
                }
            }
        
        return columns
    
    def _extract_fields(self, doc: Dict, prefix: str = "") -> Set[str]:
        """递归提取文档中的所有字段"""
        fields = set()
        
        for key, value in doc.items():
            field_name = f"{prefix}.{key}" if prefix else key
            fields.add(field_name)
            
            # 递归处理嵌套文档
            if isinstance(value, dict):
                fields.update(self._extract_fields(value, field_name))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # 处理数组中的第一个文档作为样本
                fields.update(self._extract_fields(value[0], field_name))
        
        return fields
    
    def _determine_field_type(self, sample_docs: List[Dict], field: str) -> str:
        """确定字段类型"""
        types = set()
        
        for doc in sample_docs:
            value = self._get_nested_value(doc, field)
            if value is not None:
                types.add(type(value).__name__)
        
        # 根据类型确定SQL类型
        if 'ObjectId' in types:
            return 'VARCHAR(24)'
        elif 'datetime' in types:
            return 'DATETIME'
        elif 'int' in types:
            return 'BIGINT'
        elif 'float' in types:
            return 'DOUBLE'
        elif 'bool' in types:
            return 'BOOLEAN'
        elif 'list' in types:
            return 'TEXT'
        elif 'dict' in types:
            return 'TEXT'
        else:
            return 'TEXT'
    
    def _get_nested_value(self, doc: Dict, field: str):
        """获取嵌套字段的值"""
        keys = field.split('.')
        value = doc
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def _get_mongodb_indexes(self, collection) -> Dict:
        """获取MongoDB索引信息"""
        indexes = {}
        
        try:
            # 获取集合的索引信息
            index_list = collection.list_indexes()
            
            for index in index_list:
                index_name = index['name']
                index_keys = index['key']
                
                # 确定索引类型
                if index_name == '_id_':
                    index_type = 'PRIMARY KEY'
                elif index.get('unique', False):
                    index_type = 'UNIQUE KEY'
                else:
                    index_type = 'KEY'
                
                # 构建列名列表
                columns = []
                for key, direction in index_keys:
                    columns.append(key)
                
                indexes[index_name] = {
                    'type': index_type,
                    'columns': ', '.join(columns)
                }
                
        except Exception as e:
            print(f"获取索引信息失败: {e}")
        
        return indexes
    
    def _generate_create_table_sql(self, collection_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句（模拟）"""
        sql_parts = [f"CREATE TABLE {collection_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class Db2Connector(BaseDBConnector):
    """IBM Db2数据库连接器"""
    
    def connect(self, config: Dict[str, Any]) -> None:
        """连接到IBM Db2数据库"""
        try:
            import ibm_db
            import ibm_db_dbi
            
            # 构建连接字符串
            if 'username' in config and 'password' in config:
                conn_str = f"DATABASE={config['database']};HOSTNAME={config['host']};PORT={config['port']};PROTOCOL=TCPIP;UID={config['username']};PWD={config['password']}"
            else:
                conn_str = f"DATABASE={config['database']};HOSTNAME={config['host']};PORT={config['port']};PROTOCOL=TCPIP"
            
            # 建立连接
            ibm_conn = ibm_db.connect(conn_str, "", "")
            if ibm_conn:
                self.connection = ibm_db_dbi.Connection(ibm_conn)
            else:
                raise Exception("无法建立Db2连接")
                
        except ImportError:
            raise Exception("IBM Db2驱动未安装，请先安装ibm_db: pip install ibm_db")
        except Exception as e:
            raise Exception(f"连接IBM Db2数据库失败: {str(e)}")
            
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connection:
            raise Exception("未连接到数据库")
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # 获取所有表名
            cursor.execute("""
                SELECT TABNAME 
                FROM SYSCAT.TABLES 
                WHERE TABSCHEMA = CURRENT SCHEMA 
                AND TYPE = 'T'
                ORDER BY TABNAME
            """)
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # 获取列信息
                cursor.execute(f"""
                    SELECT COLNAME, TYPENAME, LENGTH, SCALE, NULLS, DEFAULT, REMARKS
                    FROM SYSCAT.COLUMNS 
                    WHERE TABNAME = ? AND TABSCHEMA = CURRENT SCHEMA
                    ORDER BY COLNO
                """, (table_name,))
                
                columns = {}
                for col in cursor.fetchall():
                    col_name = col[0]
                    col_type = col[1]
                    length = col[2]
                    scale = col[3]
                    nulls = col[4]
                    default_val = col[5]
                    remarks = col[6]
                    
                    # 构建类型定义
                    full_type = self._build_db2_type(col_type, length, scale)
                    
                    # 构建列定义
                    col_null = 'NULL' if nulls == 'Y' else 'NOT NULL'
                    col_default = f"DEFAULT {default_val}" if default_val else ''
                    col_comment = f"COMMENT '{remarks}'" if remarks else ''
                    
                    col_def = f"{full_type} {col_null} {col_default} {col_comment}".strip()
                    columns[col_name] = {
                        'raw': col_def,
                        'normalized': normalize_sql_definition(col_def),
                        'details': {
                            "Type": full_type,
                            "Null": nulls,
                            "Default": default_val,
                            "Comment": remarks,
                            "Length": length,
                            "Scale": scale,
                        }
                    }
                
                # 获取索引信息
                cursor.execute(f"""
                    SELECT IXNAME, UNIQUERULE, COLNAMES
                    FROM SYSCAT.INDEXES 
                    WHERE TABNAME = ? AND TABSCHEMA = CURRENT SCHEMA
                    ORDER BY IXNAME
                """, (table_name,))
                
                indexes = {}
                for idx in cursor.fetchall():
                    idx_name = idx[0]
                    unique_rule = idx[1]
                    col_names = idx[2]
                    
                    # 确定索引类型
                    if unique_rule == 'P':
                        idx_type = 'PRIMARY KEY'
                    elif unique_rule == 'U':
                        idx_type = 'UNIQUE KEY'
                    else:
                        idx_type = 'KEY'
                        
                    indexes[idx_name] = {
                        'type': idx_type,
                        'columns': col_names
                    }
                
                # 生成CREATE TABLE语句
                create_table_sql = self._generate_create_table_sql(table_name, columns, indexes)
                
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': create_table_sql
                }
                
        finally:
            cursor.close()
            
        return tables
    
    def _build_db2_type(self, base_type: str, length: Optional[int], scale: Optional[int]) -> str:
        """构建Db2类型定义"""
        if base_type in ('VARCHAR', 'CHAR'):
            if length:
                return f"{base_type}({length})"
            return base_type
        elif base_type in ('DECIMAL', 'NUMERIC'):
            if scale:
                return f"{base_type}({length},{scale})"
            elif length:
                return f"{base_type}({length})"
            return base_type
        elif base_type in ('INTEGER', 'BIGINT', 'SMALLINT'):
            return base_type
        elif base_type in ('TIMESTAMP', 'DATE', 'TIME'):
            return base_type
        elif base_type == 'BLOB':
            if length:
                return f"BLOB({length})"
            return "BLOB"
        elif base_type == 'CLOB':
            if length:
                return f"CLOB({length})"
            return "CLOB"
        else:
            return base_type
    
    def _generate_create_table_sql(self, table_name: str, columns: Dict, indexes: Dict) -> str:
        """生成CREATE TABLE语句"""
        sql_parts = [f"CREATE TABLE {table_name} ("]
        
        # 添加列定义
        col_defs = []
        for col_name, col_info in columns.items():
            col_defs.append(f"    {col_name} {col_info['raw']}")
        
        # 添加主键约束
        for idx_name, idx_info in indexes.items():
            if idx_info['type'] == 'PRIMARY KEY':
                col_defs.append(f"    PRIMARY KEY ({idx_info['columns']})")
                break
        
        sql_parts.append(",\n".join(col_defs))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)

class DBConnector:
    """数据库连接器工厂类"""
    
    def __init__(self):
        self.connector = None
        self.connection_type = None
        
    def connect(self, config: Dict[str, Any], db_type: str = "mysql") -> None:
        """连接到指定类型的数据库"""
        # 关闭现有连接
        if self.connector:
            self.connector.close()
            
        # 根据类型创建相应的连接器
        if db_type.lower() == "mysql":
            self.connector = MySQLConnector()
        elif db_type.lower() == "postgresql":
            self.connector = PostgreSQLConnector()
        elif db_type.lower() == "oracle":
            self.connector = OracleConnector()
        elif db_type.lower() == "sqlserver":
            self.connector = SQLServerConnector()
        elif db_type.lower() == "sqlite":
            self.connector = SQLiteConnector()
        elif db_type.lower() == "mongodb":
            self.connector = MongoDBConnector()
        elif db_type.lower() == "db2":
            self.connector = Db2Connector()
        else:
            raise Exception(f"不支持的数据库类型: {db_type}")
            
        self.connection_type = db_type.lower()
        self.connector.connect(config)
        
    def get_table_structure(self) -> Dict[str, Dict[str, Any]]:
        """获取所有表的结构"""
        if not self.connector:
            raise Exception("未连接到数据库")
        return self.connector.get_table_structure()
        
    def close(self):
        """关闭数据库连接"""
        if self.connector:
            self.connector.close()
            self.connector = None
            self.connection_type = None
            
    def get_connection_type(self) -> Optional[str]:
        """获取当前连接类型"""
        return self.connection_type 