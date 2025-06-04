from sql_parser import SQLParser

class SQLGenerator:
    def __init__(self):
        self.parser = SQLParser()
        
    def generate_sync_sql(self, left_tables, right_tables):
        """生成同步SQL语句"""
        sql_statements = []
        
        # 获取表结构差异
        differences = self.parser.compare_tables(left_tables, right_tables)
        
        # 处理新增的表
        for table_name in differences['added_tables']:
            sql_statements.append(right_tables[table_name]['raw_sql'])
            
        # 处理删除的表
        for table_name in differences['removed_tables']:
            sql_statements.append(f"DROP TABLE IF EXISTS `{table_name}`;")
            
        # 处理修改的表
        for table_name, changes in differences['modified_tables'].items():
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
                    sql_statements.append(
                        f"ALTER TABLE `{table_name}` MODIFY COLUMN `{col_name}` {col_changes['right']};"
                    )
                
        return "\n".join(sql_statements) 