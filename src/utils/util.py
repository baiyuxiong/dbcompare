import re


def normalize_sql_definition(definition):
    """标准化SQL定义，统一大小写和格式"""
    # 将定义转换为大写
    definition = definition.upper()
    # 标准化空格
    definition = ' '.join(definition.split())
    return definition

def smart_split_sql_definitions(content):
    """
    智能分割SQL定义，正确处理包含逗号的字符串字面量
    例如："name VARCHAR(255) DEFAULT 'Smith, John', age INT" 
    会被正确分割为：["name VARCHAR(255) DEFAULT 'Smith, John'", "age INT"]
    """
    definitions = []
    current_def = ""
    in_string = False
    string_char = None
    paren_count = 0
    i = 0
    
    while i < len(content):
        char = content[i]
        
        # 处理字符串字面量
        if char in ("'", '"') and not in_string:
            in_string = True
            string_char = char
            current_def += char
        elif char == string_char and in_string:
            # 检查是否是转义的引号
            if i > 0 and content[i-1] == '\\':
                current_def += char
            else:
                in_string = False
                string_char = None
                current_def += char
        elif char == '(' and not in_string:
            paren_count += 1
            current_def += char
        elif char == ')' and not in_string:
            paren_count -= 1
            current_def += char
        elif char == ',' and not in_string and paren_count == 0:
            # 这是一个真正的分隔符
            if current_def.strip():
                definitions.append(current_def.strip())
            current_def = ""
        else:
            current_def += char
        
        i += 1
    
    # 添加最后一个定义
    if current_def.strip():
        definitions.append(current_def.strip())
    
    return definitions

def safe_replace_data_types(sql_text, type_mappings):
    """
    安全的数据类型替换，使用词边界匹配防止错误替换
    例如：不会将 POINT 中的 INT 错误替换为 INTEGER
    
    Args:
        sql_text: 要处理的SQL文本
        type_mappings: 类型映射字典 {'原类型': '目标类型'}
    
    Returns:
        处理后的SQL文本
    """
    result = sql_text
    
    for old_type, new_type in type_mappings.items():
        # 使用词边界匹配，确保只匹配完整的单词
        # \b 表示词边界，(?=\s|\(|$) 表示后面跟着空格、左括号或结尾
        pattern = r'\b' + re.escape(old_type.upper()) + r'(?=\s|\(|$|\)|,)'
        result = re.sub(pattern, new_type, result, flags=re.IGNORECASE)
    
    return result

def get_mysql_to_postgresql_mappings():
    """获取MySQL到PostgreSQL的数据类型映射"""
    return {
        'TINYINT': 'SMALLINT',
        'INT': 'INTEGER', 
        'BIGINT': 'BIGINT',
        'DATETIME': 'TIMESTAMP',
        'AUTO_INCREMENT': '',
        'MEDIUMTEXT': 'TEXT',
        'LONGTEXT': 'TEXT',
        'TINYTEXT': 'TEXT'
    }

def get_mysql_to_oracle_mappings():
    """获取MySQL到Oracle的数据类型映射"""
    return {
        'TINYINT': 'NUMBER(3)',
        'INT': 'NUMBER(10)', 
        'BIGINT': 'NUMBER(19)',
        'DATETIME': 'DATE',
        'TEXT': 'CLOB',
        'LONGTEXT': 'CLOB',
        'AUTO_INCREMENT': ''
    }

def get_mysql_to_sqlserver_mappings():
    """获取MySQL到SQL Server的数据类型映射"""
    return {
        'TINYINT': 'TINYINT',
        'INT': 'INT',
        'BIGINT': 'BIGINT', 
        'DATETIME': 'DATETIME2',
        'TEXT': 'NVARCHAR(MAX)',
        'LONGTEXT': 'NVARCHAR(MAX)',
        'AUTO_INCREMENT': 'IDENTITY(1,1)'
    }

def get_mysql_to_sqlite_mappings():
    """获取MySQL到SQLite的数据类型映射"""
    return {
        'TINYINT': 'INTEGER',
        'INT': 'INTEGER',
        'BIGINT': 'INTEGER',
        'DATETIME': 'TEXT',
        'AUTO_INCREMENT': ''
    }

def get_mysql_to_db2_mappings():
    """获取MySQL到DB2的数据类型映射"""
    return {
        'TINYINT': 'SMALLINT',
        'INT': 'INTEGER',
        'BIGINT': 'BIGINT',
        'DATETIME': 'TIMESTAMP',
        'TEXT': 'CLOB',
        'AUTO_INCREMENT': ''
    }

def extract_default_value_enhanced(col_def: str) -> str:
    """
    增强的默认值提取逻辑，能够处理复杂的默认值表达式
    
    支持的默认值格式：
    - 简单字符串: DEFAULT 'value'
    - 数字: DEFAULT 0
    - 函数: DEFAULT CURRENT_TIMESTAMP
    - 表达式: DEFAULT (expression)
    - 带括号的字符串: DEFAULT ('complex, value')
    """
    if 'DEFAULT' not in col_def.upper():
        return None
    
    # 使用正则表达式匹配DEFAULT后面的内容
    import re
    
    # 匹配DEFAULT后面的内容，考虑各种情况
    patterns = [
        # 匹配带单引号的字符串
        r"DEFAULT\s+'([^']*(?:''[^']*)*)'(?=\s|$|,|\))",
        # 匹配带双引号的字符串 
        r'DEFAULT\s+"([^"]*(?:""[^"]*)*)"(?=\s|$|,|\))',
        # 匹配带括号的表达式
        r'DEFAULT\s+(\([^)]+\))(?=\s|$|,|\))',
        # 匹配函数调用
        r'DEFAULT\s+([A-Z_][A-Z0-9_]*\([^)]*\))(?=\s|$|,|\))',
        # 匹配简单的值（数字、关键字等）
        r'DEFAULT\s+([^\s,)]+)(?=\s|$|,|\))'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, col_def, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def parse_complex_column_definition(definition: str) -> dict:
    """
    解析复杂的列定义，更准确地提取各个属性
    """
    details = {
        'Type': None,
        'Null': 'YES', 
        'Default': None,
        'Comment': None,
        'Extra': None,
        'Charset': None,
        'Collation': None,
        'Attributes': set()
    }
    
    # 使用增强的默认值提取
    details['Default'] = extract_default_value_enhanced(definition)
    
    # 提取注释
    import re
    comment_match = re.search(r"COMMENT\s+'([^']*(?:''[^']*)*)'|", definition, re.IGNORECASE)
    if comment_match:
        details['Comment'] = comment_match.group(1)
    
    # 提取类型（更精确的匹配）
    type_match = re.match(r'^\s*([A-Z]+(?:\([^)]+\))?)', definition, re.IGNORECASE)
    if type_match:
        details['Type'] = type_match.group(1)
    
    # 检查NULL/NOT NULL
    if re.search(r'\bNOT\s+NULL\b', definition, re.IGNORECASE):
        details['Null'] = 'NO'
    elif re.search(r'\bNULL\b', definition, re.IGNORECASE):
        details['Null'] = 'YES'
    
    # 检查AUTO_INCREMENT
    if re.search(r'\bAUTO_INCREMENT\b', definition, re.IGNORECASE):
        details['Extra'] = 'auto_increment'
    
    # 检查其他属性
    for attr in ['UNSIGNED', 'ZEROFILL', 'BINARY']:
        if re.search(r'\b' + attr + r'\b', definition, re.IGNORECASE):
            details['Attributes'].add(attr.lower())
    
    # 转换属性集合
    if details['Attributes']:
        details['Attributes'] = ' '.join(sorted(details['Attributes']))
    else:
        details['Attributes'] = None
    
    return details