import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from sqlparse.tokens import Keyword, DML, Whitespace
from utils.util import normalize_sql_definition, smart_split_sql_definitions, parse_complex_column_definition

class BaseSQLParser:
    """SQL解析器基类"""
    
    def __init__(self, ignore_case=True):
        self.ignore_case = ignore_case
        
    def _normalize_name(self, name):
        """标准化名称，根据ignore_case设置决定是否转换为小写"""
        if self.ignore_case:
            return name.lower()
        return name
        
    def parse_sql(self, sql_content):
        """解析SQL字符串，返回表结构字典"""
        # 解析SQL语句
        statements = sqlparse.parse(sql_content)
        return self._parse_statements(statements)
        
    def parse_file(self, file_path):
        """解析SQL文件，返回表结构字典"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            # 文件不存在时返回空字典
            print(f"错误：文件 '{file_path}' 不存在")
            return {}
        except PermissionError:
            print(f"错误：没有权限读取文件 '{file_path}'")
            return {}
        except UnicodeDecodeError as e:
            print(f"错误：文件 '{file_path}' 编码错误：{e}")
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    content = file.read()
                print(f"使用 GBK 编码成功读取文件")
            except Exception:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                    print(f"使用 Latin-1 编码成功读取文件")
                except Exception:
                    print(f"错误：无法使用任何编码读取文件 '{file_path}'")
                    return {}
        except Exception as e:
            # 其他错误时提供更具体的错误信息
            print(f"错误：读取文件 '{file_path}' 时出错：{type(e).__name__}: {e}")
            return {}
            
        # 解析SQL语句
        try:
            statements = sqlparse.parse(content)
            return self._parse_statements(statements)
        except Exception as e:
            print(f"错误：解析SQL文件 '{file_path}' 内容时出错：{type(e).__name__}: {e}")
            return {}
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典，子类必须实现"""
        raise NotImplementedError
        
    def compare_tables(self, left_tables, right_tables):
        """比较两个表结构的差异，子类必须实现"""
        raise NotImplementedError

class MySQLParser(BaseSQLParser):
    """MySQL SQL解析器"""
    
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
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                    # 使用智能分割方法分割每个定义（仅限MySQLParser）
                    defs = smart_split_sql_definitions(content)
                    
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
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('KEY', 'UNIQUE'):
                                    index_type = parts[0].upper()
                                    if len(parts) > 2:
                                        # 有索引名称
                                        index_name = parts[1].strip('`"[]')
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        # 没有索引名称，使用默认名称
                                        index_name = f"auto_{index_type.lower()}_{len(indexes)}"
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue  # 不完整的定义，跳过
                                elif parts[0].upper() == 'FOREIGN':
                                    index_type = 'FOREIGN KEY'
                                    if len(parts) > 2:
                                        index_name = f"fk_{len(indexes)}"
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的索引类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
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
        if self.ignore_case:
            left_table_names = {self._normalize_name(name) for name in left_tables.keys()}
            right_table_names = {self._normalize_name(name) for name in right_tables.keys()}
            # 创建名称映射
            left_name_map = {self._normalize_name(name): name for name in left_tables.keys()}
            right_name_map = {self._normalize_name(name): name for name in right_tables.keys()}
        else:
            left_table_names = set(left_tables.keys())
            right_table_names = set(right_tables.keys())
            left_name_map = {name: name for name in left_tables.keys()}
            right_name_map = {name: name for name in right_tables.keys()}
        
        differences['added_tables'] = [right_name_map[name] for name in (right_table_names - left_table_names)]
        differences['removed_tables'] = [left_name_map[name] for name in (left_table_names - right_table_names)]
        
        # 检查修改的表
        common_tables = left_table_names & right_table_names
        for normalized_table_name in common_tables:
            # 获取原始表名
            left_original_name = left_name_map[normalized_table_name]
            right_original_name = right_name_map[normalized_table_name]
            
            left_cols = left_tables[left_original_name]['columns']
            right_cols = right_tables[right_original_name]['columns']
            left_indexes = left_tables[left_original_name]['indexes']
            right_indexes = right_tables[right_original_name]['indexes']
            
            table_diffs = {}
            
            # 比较列定义
            if self.ignore_case:
                left_col_names = {self._normalize_name(col): col for col in left_cols.keys()}
                right_col_names = {self._normalize_name(col): col for col in right_cols.keys()}
                # 在忽略大小写模式下，使用标准化后的定义进行比较
                left_col_normalized = {self._normalize_name(col): {
                    'raw': defn['raw'],
                    'normalized': defn['normalized'],
                    'details': defn['details']
                } for col, defn in left_cols.items()}
                right_col_normalized = {self._normalize_name(col): {
                    'raw': defn['raw'],
                    'normalized': defn['normalized'],
                    'details': defn['details']
                } for col, defn in right_cols.items()}
            else:
                left_col_names = {col: col for col in left_cols.keys()}
                right_col_names = {col: col for col in right_cols.keys()}
                left_col_normalized = left_cols
                right_col_normalized = right_cols
            
            # 检查列名差异（即使定义相同，列名大小写不同也算差异）
            left_col_set = set(left_col_normalized.keys())
            right_col_set = set(right_col_normalized.keys())
            
            # 在忽略大小写模式下，比较标准化后的定义
            if self.ignore_case:
                # 比较标准化后的定义
                left_normalized_defs = {col: defn['normalized'] for col, defn in left_col_normalized.items()}
                right_normalized_defs = {col: defn['normalized'] for col, defn in right_col_normalized.items()}
                definitions_different = left_normalized_defs != right_normalized_defs
            else:
                # 比较原始定义
                left_raw_defs = {col: defn['raw'] for col, defn in left_col_normalized.items()}
                right_raw_defs = {col: defn['raw'] for col, defn in right_col_normalized.items()}
                definitions_different = left_raw_defs != right_raw_defs
                
            if left_col_set != right_col_set or definitions_different:
                table_diffs['columns'] = {
                    'added_columns': {right_col_names[col]: defn['raw'] for col, defn in right_col_normalized.items() if col not in left_col_normalized},
                    'removed_columns': {left_col_names[col]: defn['raw'] for col, defn in left_col_normalized.items() if col not in right_col_normalized},
                    'modified_columns': {}
                }
                
                # 比较共同列的details
                common_cols = set(left_col_normalized.keys()) & set(right_col_normalized.keys())
                for normalized_col in common_cols:
                    left_original_col = left_col_names[normalized_col]
                    right_original_col = right_col_names[normalized_col]
                    
                    # 在区分大小写模式下，如果原始定义不同，直接标记为修改
                    if not self.ignore_case:
                        left_raw = left_cols[left_original_col]['raw']
                        right_raw = right_cols[right_original_col]['raw']
                        if left_raw != right_raw:
                            table_diffs['columns']['modified_columns'][left_original_col] = {
                                'raw': {
                                    'left': left_raw,
                                    'right': right_raw
                                },
                                'details': {
                                    'Definition': {
                                        'left': left_raw,
                                        'right': right_raw
                                    }
                                }
                            }
                            continue
                    
                    # 在忽略大小写模式下，比较details
                    left_details = normalize_details(left_cols[left_original_col]['details'])
                    right_details = normalize_details(right_cols[right_original_col]['details'])
                    
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
                            # 使用左侧的列名作为标准
                            table_diffs['columns']['modified_columns'][left_original_col] = {
                                'raw': {
                                    'left': left_cols[left_original_col]['raw'],
                                    'right': right_cols[right_original_col]['raw']
                                },
                                'details': changed_attrs
                            }
                            # 列修改信息已记录
            
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
                # 使用左侧的表名作为标准
                differences['modified_tables'][left_original_name] = table_diffs
                
        return differences

class PostgreSQLParser(BaseSQLParser):
    """PostgreSQL SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析PostgreSQL列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'UDT': None,            # 用户定义类型
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT'):
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
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('"')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('"')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class OracleParser(BaseSQLParser):
    """Oracle SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析Oracle列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'Length': None,         # 长度
            'Precision': None,      # 精度
            'Scale': None,          # 小数位数
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT'):
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
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('"')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('"')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class SQLServerParser(BaseSQLParser):
    """SQL Server SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析SQL Server列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'Identity': None,       # 自增属性
            'Length': None,         # 长度
            'Precision': None,      # 精度
            'Scale': None,          # 小数位数
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT', 'IDENTITY'):
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
                
            # 处理 IDENTITY
            elif current == 'IDENTITY':
                details['Identity'] = True
                i += 1
                
            # 处理 COMMENT
            elif current == 'COMMENT':
                if i + 1 < len(parts):
                    comment = parts[i + 1]
                    if comment.startswith("'") and comment.endswith("'"):
                        comment = comment[1:-1]
                    details['Comment'] = comment
                i += 2
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('[]')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('[]')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class SQLiteParser(BaseSQLParser):
    """SQLite SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析SQLite列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'PrimaryKey': False,    # 主键
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT', 'PRIMARY', 'KEY'):
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
                
            # 处理 PRIMARY KEY
            elif current == 'PRIMARY' and i + 1 < len(parts) and parts[i + 1].upper() == 'KEY':
                details['PrimaryKey'] = True
                i += 2
                
            # 处理 COMMENT
            elif current == 'COMMENT':
                if i + 1 < len(parts):
                    comment = parts[i + 1]
                    if comment.startswith("'") and comment.endswith("'"):
                        comment = comment[1:-1]
                    details['Comment'] = comment
                i += 2
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('"')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('"')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class MongoDBSQLParser(BaseSQLParser):
    """MongoDB SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析MongoDB列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'MongoDBType': None,    # MongoDB原始类型
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT'):
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
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('"')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('"')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class Db2SQLParser(BaseSQLParser):
    """IBM Db2 SQL解析器"""
    
    def _parse_column_definition(self, definition):
        """解析Db2列定义，返回详细信息"""
        details = {
            'Type': None,           # 数据类型
            'Null': 'YES',          # YES/NO
            'Default': None,        # 默认值
            'Comment': None,        # 注释
            'Extra': None,          # 额外信息
            'Length': None,         # 长度
            'Precision': None,      # 精度
            'Scale': None,          # 小数位数
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
            if current in ('NOT', 'NULL', 'DEFAULT', 'COMMENT'):
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
            else:
                i += 1
                
        return details
        
    def _parse_statements(self, statements):
        """解析SQL语句列表，返回表结构字典"""
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
                        table_name = item.get_name().strip('"')
                        continue
                        
                # 处理括号内的列定义和索引
                if isinstance(item, Parenthesis):
                    # 获取括号内的内容
                    content = item.value.strip('()')
                    # 使用智能分割方法分割每个定义
                    defs = smart_split_sql_definitions(content)
                    
                    for definition in defs:
                        if not definition:
                            continue
                            
                        # 处理约束定义
                        if definition.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')):
                            index_type = None
                            index_name = None
                            index_columns = None
                            
                            # 解析约束类型和名称
                            parts = definition.split(None, 2)
                            if len(parts) >= 2:
                                if parts[0].upper() == 'PRIMARY':
                                    index_type = 'PRIMARY KEY'
                                    index_name = 'PRIMARY'
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    else:
                                        continue  # 没有列定义，跳过
                                elif parts[0].upper() in ('UNIQUE', 'FOREIGN'):
                                    if parts[0].upper() == 'FOREIGN':
                                        index_type = 'FOREIGN KEY'
                                        index_name = f"fk_{len(indexes)}"
                                    else:
                                        index_type = parts[0].upper()
                                        index_name = f"unique_{len(indexes)}"
                                    if len(parts) > 2:
                                        index_columns = parts[2].strip('()')
                                    elif len(parts) == 2:
                                        index_columns = parts[1].strip('()')
                                    else:
                                        continue
                                else:
                                    continue  # 未知的约束类型
                                        
                                # 确保索引名称和列都不为空
                                if index_name and index_columns and index_name.strip() and index_columns.strip():
                                    indexes[index_name] = {
                                        'type': index_type,
                                        'columns': index_columns
                                    }
                            continue
                            
                        # 处理列定义
                        parts = definition.split(None, 1)
                        if len(parts) >= 2:
                            col_name = parts[0].strip('"')
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
        """比较两个表结构的差异（与MySQL相同）"""
        # 使用与MySQL相同的比较逻辑
        mysql_parser = MySQLParser(ignore_case=self.ignore_case)
        return mysql_parser.compare_tables(left_tables, right_tables)

class SQLParser:
    """SQL解析器工厂类"""
    
    def __init__(self, ignore_case=True, db_type="mysql"):
        self.db_type = db_type.lower()
        self.parsers = {
            'mysql': MySQLParser(ignore_case),
            'postgresql': PostgreSQLParser(ignore_case),
            'oracle': OracleParser(ignore_case),
            'sqlserver': SQLServerParser(ignore_case),
            'sqlite': SQLiteParser(ignore_case),
            'mongodb': MongoDBSQLParser(ignore_case),
            'db2': Db2SQLParser(ignore_case)
        }
        
        if self.db_type not in self.parsers:
            self.db_type = "mysql"  # 默认使用MySQL解析器
            
        self.parser = self.parsers[self.db_type]
        
    def parse_sql(self, sql_content):
        """解析SQL字符串，返回表结构字典"""
        return self.parser.parse_sql(sql_content)
        
    def parse_file(self, file_path):
        """解析SQL文件，返回表结构字典"""
        return self.parser.parse_file(file_path)
        
    def compare_tables(self, left_tables, right_tables):
        """比较两个表结构的差异"""
        return self.parser.compare_tables(left_tables, right_tables)
        
    def set_db_type(self, db_type):
        """设置数据库类型"""
        if db_type.lower() in self.parsers:
            self.db_type = db_type.lower()
            self.parser = self.parsers[self.db_type] 