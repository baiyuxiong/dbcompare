import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from sqlparse.tokens import Keyword, DML, Whitespace
from utils.util import normalize_sql_definition
class SQLParser:
    def __init__(self):
        pass
        
    def _parse_column_definition(self, definition):
        """解析MySQL列定义，返回详细信息
        
        支持的列定义格式示例：
        - INT NOT NULL AUTO_INCREMENT
        - VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT ''
        - DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0.00
        - TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        """
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息（如 AUTO_INCREMENT）
            'Charset': None,        # 字符集
            'Collation': None,      # 排序规则
            'Attributes': set(),    # 其他属性（如 UNSIGNED, ZEROFILL 等）
            'Key': None,            # 键类型
        }
        
        # 分割定义字符串
        parts = definition.split()
        if not parts:
            return details
            
        # 解析类型（包括长度/精度）
        type_parts = []
        i = 0
        while i < len(parts):
            current = parts[i].upper()
            # 如果遇到属性关键字，停止类型解析
            if current in ('UNSIGNED', 'ZEROFILL', 'NOT', 'NULL', 'DEFAULT', 'COMMENT', 
                         'CHARACTER', 'COLLATE', 'AUTO_INCREMENT', 'UNIQUE', 'PRIMARY',
                         'STORAGE', 'MEMORY', 'ON'):
                break
            type_parts.append(parts[i])
            i += 1
        details['Type'] = ' '.join(type_parts)
        
        # 解析剩余属性
        while i < len(parts):
            current = parts[i].upper()
            
            # 处理 NULL/NOT NULL
            if current == 'NOT' and i + 1 < len(parts) and parts[i + 1].upper() == 'NULL':
                details['Null'] = 'NO'
                i += 2
            elif current == 'NULL':
                details['Null'] = 'YES'
                i += 1
                
            # 处理 DEFAULT
            elif current == 'DEFAULT':
                if i + 1 < len(parts):
                    default_value = parts[i + 1]
                    # 处理带引号的默认值
                    if default_value.startswith("'") and default_value.endswith("'"):
                        default_value = default_value[1:-1]
                    # 处理特殊默认值
                    elif default_value.upper() in ('CURRENT_TIMESTAMP', 'NULL'):
                        default_value = default_value
                    details['Default'] = default_value
                i += 2
                
            # 处理 COMMENT
            elif current == 'COMMENT':
                if i + 1 < len(parts):
                    comment = parts[i + 1]
                    if comment.startswith("'") and comment.endswith("'"):
                        comment = comment[1:-1]
                    details['Comment'] = comment
                i += 2
                
            # 处理字符集
            elif current == 'CHARACTER' and i + 2 < len(parts) and parts[i + 1].upper() == 'SET':
                details['Charset'] = parts[i + 2]
                i += 3
                
            # 处理排序规则
            elif current == 'COLLATE':
                if i + 1 < len(parts):
                    details['Collation'] = parts[i + 1]
                i += 2
                
            # 处理 AUTO_INCREMENT
            elif current == 'AUTO_INCREMENT':
                details['Extra'] = 'auto_increment'
                i += 1
                
            # 处理其他属性
            elif current in ('UNSIGNED', 'ZEROFILL', 'STORAGE', 'MEMORY'):
                details['Attributes'].add(current.lower())
                i += 1
                
            # 处理 ON UPDATE CURRENT_TIMESTAMP
            elif current == 'ON' and i + 2 < len(parts):
                if ' '.join(parts[i:i+3]).upper() == 'ON UPDATE CURRENT_TIMESTAMP':
                    details['Extra'] = 'on update CURRENT_TIMESTAMP'
                    i += 3
                else:
                    i += 1
            else:
                i += 1
                
        # 将属性集合转换为字符串
        if details['Attributes']:
            details['Attributes'] = ' '.join(sorted(details['Attributes']))
        else:
            details['Attributes'] = None
            
        return details
        
    def parse_file(self, file_path):
        """解析SQL文件，返回表结构字典"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            # 文件不存在时返回空字典
            return {}
        except Exception as e:
            # 其他错误时也返回空字典
            print(f"读取文件 {file_path} 时出错: {e}")
            return {}
            
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
                            col_definition = parts[1].strip()
                            # 存储原始定义和标准化后的定义
                            columns[col_name] = {
                                'raw': col_definition,
                                'normalized': normalize_sql_definition(col_definition),
                                'details': self._parse_column_definition(col_definition)
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
        
        def normalize_value(value):
            """统一处理空值"""
            if value == '':
                return None
            return value
            
        def normalize_details(details):
            """统一处理details中的空值"""
            if not details:
                return details
            normalized = {}
            for key, value in details.items():
                if isinstance(value, dict):
                    normalized[key] = normalize_details(value)
                else:
                    normalized[key] = normalize_value(value)
            return normalized
        
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
                    'modified_columns': {}
                }
                
                # 比较共同列的details
                for col in set(left_cols.keys()) & set(right_cols.keys()):
                    left_details = normalize_details(left_cols[col]['details'])
                    right_details = normalize_details(right_cols[col]['details'])
                    
                    if left_details != right_details:
                        # 找出具体哪些属性发生了变化
                        changed_attrs = {}
                        for key in set(left_details.keys()) | set(right_details.keys()):
                            if left_details.get(key) != right_details.get(key):
                                changed_attrs[key] = {
                                    'left': left_details.get(key),
                                    'right': right_details.get(key)
                                }
                        
                        if changed_attrs:
                            table_diffs['columns']['modified_columns'][col] = {
                                'raw': {
                                    'left': left_cols[col]['raw'],
                                    'right': right_cols[col]['raw']
                                },
                                'details': changed_attrs
                            }
                            print("table_diffs",table_diffs['columns']['modified_columns'][col])
            
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