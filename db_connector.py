import mysql.connector
from typing import Dict, Any
from util import normalize_sql_definition

class DBConnector:
    def __init__(self):
        self.connection = None
        
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
            raise Exception(f"连接数据库失败: {str(e)}")
            
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
                    # {'Field': 'team_id', 'Type': 'char(32)', 'Collation': 'utf8mb4_0900_ai_ci', 'Null': 'NO', 'Key': '', 'Default': '', 'Extra': '', 'Privileges': 'select,insert,update,references', 'Comment': '组织ID'}
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
        
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None 