from .sql_parser import SQLParser
from utils.util import extract_default_value_enhanced

class BaseSQLGenerator:
    """
    SQL生成器基类
    
    注意：DBCompare工具仅支持同类型数据库之间的比较和同步
    左右两侧必须是相同的数据库类型（如MySQL vs MySQL）
    不支持跨数据库类型的转换和迁移
    """
    
    def __init__(self, db_type):
        self.parser = SQLParser()
        self.db_type = db_type.lower()
        
    def generate_sync_sql(self, left_tables, right_tables):
        """生成同步SQL语句，子类必须实现"""
        raise NotImplementedError
        
    def validate_same_database_type(self, left_db_type, right_db_type):
        """验证左右两侧是否为相同的数据库类型"""
        if left_db_type.lower() != right_db_type.lower():
            raise ValueError(
                f"DBCompare仅支持同类型数据库比较。"
                f"左侧: {left_db_type}, 右侧: {right_db_type}。"
                f"请确保两侧使用相同的数据库类型。"
            )

class MySQLSQLGenerator(BaseSQLGenerator):
    """
    MySQL SQL生成器
    用于生成MySQL数据库之间的结构同步SQL
    """
    
    def __init__(self):
        super().__init__('mysql')
    
    def generate_sync_sql(self, left_tables, right_tables):
        """生成MySQL同步SQL语句"""
        sql_statements = []
        
        # 获取表结构差异
        differences = self.parser.compare_tables(left_tables, right_tables)
        
        # 处理新增的表
        for table_name in differences['added_tables']:
            sql_statements.append(f"-- 创建新表: {table_name}")
            sql_statements.append(right_tables[table_name]['raw_sql'])
            sql_statements.append("")
            
        # 处理删除的表
        for table_name in differences['removed_tables']:
            sql_statements.append(f"-- 删除表: {table_name}")
            sql_statements.append(f"DROP TABLE IF EXISTS `{table_name}`;")
            sql_statements.append("")
            
        # 处理修改的表
        for table_name, changes in differences['modified_tables'].items():
            sql_statements.append(f"-- 修改表: {table_name}")
            
            # 添加新列
            if 'columns' in changes and 'added_columns' in changes['columns']:
                for col_name, col_def in changes['columns']['added_columns'].items():
                    sql_statements.append(
                        f"ALTER TABLE `{table_name}` ADD COLUMN `{col_name}` {col_def};"
                    )
                
            # 删除列
            if 'columns' in changes and 'removed_columns' in changes['columns']:
                for col_name in changes['columns']['removed_columns']:
                    sql_statements.append(
                        f"ALTER TABLE `{table_name}` DROP COLUMN `{col_name}`;"
                    )
                
            # 修改列
            if 'columns' in changes and 'modified_columns' in changes['columns']:
                for col_name, col_changes in changes['columns']['modified_columns'].items():
                    # 获取右侧的列定义
                    right_def = col_changes['raw']['right']
                    sql_statements.append(
                        f"ALTER TABLE `{table_name}` MODIFY COLUMN `{col_name}` {right_def};"
                    )
            
            # 处理索引变化
            if 'indexes' in changes:
                # 添加新索引
                if 'added_indexes' in changes['indexes']:
                    for idx_name, idx_def in changes['indexes']['added_indexes'].items():
                        if idx_def['type'] == 'PRIMARY KEY':
                            sql_statements.append(
                                f"ALTER TABLE `{table_name}` ADD PRIMARY KEY ({idx_def['columns']});"
                            )
                        elif idx_def['type'] == 'UNIQUE':
                            sql_statements.append(
                                f"ALTER TABLE `{table_name}` ADD UNIQUE KEY `{idx_name}` ({idx_def['columns']});"
                            )
                        else:
                            sql_statements.append(
                                f"ALTER TABLE `{table_name}` ADD KEY `{idx_name}` ({idx_def['columns']});"
                            )
                
                # 删除索引
                if 'removed_indexes' in changes['indexes']:
                    for idx_name in changes['indexes']['removed_indexes']:
                        if idx_name == 'PRIMARY':
                            sql_statements.append(
                                f"ALTER TABLE `{table_name}` DROP PRIMARY KEY;"
                            )
                        else:
                            sql_statements.append(
                                f"ALTER TABLE `{table_name}` DROP KEY `{idx_name}`;"
                            )
            
            sql_statements.append("")
                
        return "\n".join(sql_statements)

class PostgreSQLSQLGenerator(BaseSQLGenerator):
    """
    PostgreSQL SQL生成器
    用于生成PostgreSQL数据库之间的结构同步SQL
    """
    
    def __init__(self):
        super().__init__('postgresql')
    
    def generate_sync_sql(self, left_tables, right_tables):
        """生成PostgreSQL同步SQL语句"""
        sql_statements = []
        
        # 获取表结构差异
        differences = self.parser.compare_tables(left_tables, right_tables)
        
        # 处理新增的表
        for table_name in differences['added_tables']:
            sql_statements.append(f"-- 创建新表: {table_name}")
            sql_statements.append(right_tables[table_name]['raw_sql'])
            sql_statements.append("")
            
        # 处理删除的表
        for table_name in differences['removed_tables']:
            sql_statements.append(f"-- 删除表: {table_name}")
            sql_statements.append(f"DROP TABLE IF EXISTS {table_name};")
            sql_statements.append("")
            
        # 处理修改的表
        for table_name, changes in differences['modified_tables'].items():
            sql_statements.append(f"-- 修改表: {table_name}")
            
            # 添加新列
            if 'columns' in changes and 'added_columns' in changes['columns']:
                for col_name, col_def in changes['columns']['added_columns'].items():
                    sql_statements.append(
                        f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def};"
                    )
                
            # 删除列
            if 'columns' in changes and 'removed_columns' in changes['columns']:
                for col_name in changes['columns']['removed_columns']:
                    sql_statements.append(
                        f"ALTER TABLE {table_name} DROP COLUMN {col_name};"
                    )
                
            # 修改列（PostgreSQL需要分步骤修改）
            if 'columns' in changes and 'modified_columns' in changes['columns']:
                for col_name, col_changes in changes['columns']['modified_columns'].items():
                    right_def = col_changes['raw']['right']
                    
                    # 提取类型信息
                    type_part = self._extract_column_type(right_def)
                    if type_part:
                        sql_statements.append(
                            f"ALTER TABLE {table_name} ALTER COLUMN {col_name} TYPE {type_part};"
                        )
                    
                    # 处理NULL约束
                    if 'NOT NULL' in right_def.upper():
                        sql_statements.append(
                            f"ALTER TABLE {table_name} ALTER COLUMN {col_name} SET NOT NULL;"
                        )
                    elif 'NULL' in right_def.upper():
                        sql_statements.append(
                            f"ALTER TABLE {table_name} ALTER COLUMN {col_name} DROP NOT NULL;"
                        )
                    
                    # 处理默认值
                    default_value = extract_default_value_enhanced(right_def)
                    if default_value:
                        sql_statements.append(
                            f"ALTER TABLE {table_name} ALTER COLUMN {col_name} SET DEFAULT {default_value};"
                        )
            
            sql_statements.append("")
                
        return "\n".join(sql_statements)
    
    def _extract_column_type(self, col_def: str) -> str:
        """从列定义中提取类型部分"""
        parts = col_def.split()
        if parts:
            return parts[0]
        return None

class SQLiteSQLGenerator(BaseSQLGenerator):
    """
    SQLite SQL生成器
    用于生成SQLite数据库之间的结构同步SQL
    注意：SQLite限制较多，不支持DROP COLUMN和MODIFY COLUMN
    """
    
    def __init__(self):
        super().__init__('sqlite')
    
    def generate_sync_sql(self, left_tables, right_tables):
        """生成SQLite同步SQL语句"""
        sql_statements = []
        
        # 获取表结构差异
        differences = self.parser.compare_tables(left_tables, right_tables)
        
        # 处理新增的表
        for table_name in differences['added_tables']:
            sql_statements.append(f"-- 创建新表: {table_name}")
            sql_statements.append(right_tables[table_name]['raw_sql'])
            sql_statements.append("")
            
        # 处理删除的表
        for table_name in differences['removed_tables']:
            sql_statements.append(f"-- 删除表: {table_name}")
            sql_statements.append(f"DROP TABLE IF EXISTS {table_name};")
            sql_statements.append("")
            
        # 处理修改的表
        for table_name, changes in differences['modified_tables'].items():
            sql_statements.append(f"-- 修改表: {table_name}")
            
            # 添加新列（SQLite支持）
            if 'columns' in changes and 'added_columns' in changes['columns']:
                for col_name, col_def in changes['columns']['added_columns'].items():
                    sql_statements.append(
                        f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def};"
                    )
                
            # 删除列（SQLite不支持，需要重建表）
            if 'columns' in changes and 'removed_columns' in changes['columns']:
                sql_statements.append(f"-- SQLite不支持DROP COLUMN，需要手动重建表: {table_name}")
                for col_name in changes['columns']['removed_columns']:
                    sql_statements.append(f"-- 需要删除的列: {col_name}")
                
            # 修改列（SQLite不支持，需要重建表）
            if 'columns' in changes and 'modified_columns' in changes['columns']:
                sql_statements.append(f"-- SQLite不支持MODIFY COLUMN，需要手动重建表: {table_name}")
                for col_name in changes['columns']['modified_columns']:
                    sql_statements.append(f"-- 需要修改的列: {col_name}")
            
            sql_statements.append("")
                
        return "\n".join(sql_statements)

class SQLGenerator:
    """
    SQL生成器工厂类
    根据数据库类型返回相应的生成器
    注意：仅支持同类型数据库之间的比较和同步
    """
    
    def __init__(self):
        self.generators = {
            'mysql': MySQLSQLGenerator(),
            'postgresql': PostgreSQLSQLGenerator(),
            'sqlite': SQLiteSQLGenerator(),
            # 可以根据需要添加其他数据库生成器
        }
        
    def generate_sync_sql(self, left_tables, right_tables, db_type="mysql"):
        """
        生成同步SQL语句
        
        Args:
            left_tables: 左侧数据库表结构
            right_tables: 右侧数据库表结构  
            db_type: 数据库类型（左右两侧必须相同）
            
        Returns:
            生成的同步SQL语句
            
        Raises:
            ValueError: 当数据库类型不受支持时
        """
        db_type = db_type.lower()
        
        if db_type not in self.generators:
            supported_types = ', '.join(self.generators.keys())
            raise ValueError(
                f"不支持的数据库类型: {db_type}\n"
                f"支持的类型: {supported_types}"
            )
            
        generator = self.generators[db_type]
        return generator.generate_sync_sql(left_tables, right_tables)