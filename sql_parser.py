import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from sqlparse.tokens import Keyword, DML, Whitespace

class SQLParser:
    def __init__(self):
        pass
        
    def normalize_sql_definition(self, definition):
        """标准化SQL定义，统一大小写和格式"""
        # 将定义转换为大写
        definition = definition.upper()
        # 标准化空格
        definition = ' '.join(definition.split())
        return definition
        
    def parse_file(self, file_path):
        """解析SQL文件，返回表结构字典"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 解析SQL语句
        statements = sqlparse.parse(content)
        tables = {}
        
        for statement in statements:
            # 只处理CREATE TABLE语句
            if not statement.get_type().upper() == 'CREATE':
                continue
                
            # 获取表名和列定义
            table_name = None
            columns = {}
            indexes = {}
            
            # 遍历语句的token
            for item in statement.tokens:
                if isinstance(item, Identifier):
                    # 获取表名
                    if not table_name:
                        table_name = item.get_name().strip('`')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 分割每个定义
                    defs = [d.strip() for d in content.split(',')]
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理索引定义
                        if definition.upper().startswith(('PRIMARY KEY', 'KEY', 'UNIQUE KEY', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析索引类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    index_columns = parts[2].strip('()')
                                else:
                                    index_type = parts[0].upper()
                                    if len(parts) > 2:
                                        index_name = parts[1].strip('`')
                                        index_columns = parts[2].strip('()')
                                        
                                if index_type and index_columns:
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('`')
                            col_type = parts[1].strip()
                            # 存储原始定义和标准化后的定义
                            columns[col_name] = {
                                'raw': col_type,
                                'normalized': self.normalize_sql_definition(col_type)
                            }
                            
            if table_name:
                tables[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'raw_sql': str(statement)
                }
                
        return tables
        
    def compare_tables(self, left_tables, right_tables):
        """比较两个表结构的差异"""
        differences = {
            'added_tables': [],
            'removed_tables': [],
            'modified_tables': {}
        }
        
        # 检查新增和删除的表
        left_table_names = set(left_tables.keys())
        right_table_names = set(right_tables.keys())
        
        differences['added_tables'] = list(right_table_names - left_table_names)
        differences['removed_tables'] = list(left_table_names - right_table_names)
        
        # 检查修改的表
        common_tables = left_table_names & right_table_names
        for table_name in common_tables:
            left_cols = left_tables[table_name]['columns']
            right_cols = right_tables[table_name]['columns']
            left_indexes = left_tables[table_name]['indexes']
            right_indexes = right_tables[table_name]['indexes']
            
            table_diffs = {}
            
            # 比较列定义
            if left_cols != right_cols:
                table_diffs['columns'] = {
                    'added_columns': {col: defn['raw'] for col, defn in right_cols.items() if col not in left_cols},
                    'removed_columns': {col: defn['raw'] for col, defn in left_cols.items() if col not in right_cols},
                    'modified_columns': {
                        col: {'left': left_cols[col]['raw'], 'right': right_cols[col]['raw']}
                        for col in set(left_cols.keys()) & set(right_cols.keys())
                        if left_cols[col]['normalized'] != right_cols[col]['normalized']
                    }
                }
            
            # 比较索引定义
            if left_indexes != right_indexes:
                table_diffs['indexes'] = {
                    'added_indexes': {idx: defn for idx, defn in right_indexes.items() if idx not in left_indexes},
                    'removed_indexes': {idx: defn for idx, defn in left_indexes.items() if idx not in right_indexes},
                    'modified_indexes': {
                        idx: {'left': left_indexes[idx], 'right': right_indexes[idx]}
                        for idx in set(left_indexes.keys()) & set(right_indexes.keys())
                        if left_indexes[idx] != right_indexes[idx]
                    }
                }
            
            if table_diffs:
                differences['modified_tables'][table_name] = table_diffs
                
        return differences 