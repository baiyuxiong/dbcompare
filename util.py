

def normalize_sql_definition(definition):
    """标准化SQL定义，统一大小写和格式"""
    # 将定义转换为大写
    definition = definition.upper()
    # 标准化空格
    definition = ' '.join(definition.split())
    return definition