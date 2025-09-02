# DBCompare - 数据库表结构比较工具

一个功能强大的数据库表结构比较工具，支持多种数据库类型，提供直观的图形界面和强大的比较功能。

## ✨ 特性

- **多数据库支持**: 支持MySQL、PostgreSQL、Oracle、SQL Server、SQLite、MongoDB、IBM Db2等7种主流数据库
- **智能比较**: 自动检测表结构差异，包括列、索引、约束等
- **SQL生成**: 自动生成同步SQL语句，支持多种数据库语法
- **文件支持**: 支持SQL DDL文件比较
- **历史记录**: 保存连接历史，方便重复使用
- **搜索功能**: 强大的搜索和导航功能
- **现代化UI**: 基于PyQt6的现代化图形界面
- **国际化**: 支持中英文界面

## 🗄️ 支持的数据库类型

### 1. MySQL
- 连接管理
- 表结构获取
- SQL生成
- 语法解析

### 2. PostgreSQL
- 连接管理
- 表结构获取
- SQL生成（支持MySQL语法转换）
- 语法解析

### 3. Oracle
- 连接管理（支持SID和服务名）
- 表结构获取
- SQL生成（支持MySQL语法转换）
- 语法解析

### 4. SQL Server
- 连接管理（支持ODBC驱动）
- 表结构获取
- SQL生成（支持MySQL语法转换）
- 语法解析

### 5. SQLite
- 文件连接管理
- 表结构获取
- SQL生成（支持MySQL语法转换）
- 语法解析

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python src/main.py
```

## 📋 系统要求

- Python 3.8+
- PyQt6
- 相应数据库驱动（可选，根据需要安装）

### 数据库驱动

```bash
# MySQL
pip install mysql-connector-python

# PostgreSQL
pip install psycopg2-binary

# Oracle
pip install cx_Oracle

# SQL Server
pip install pyodbc

# MongoDB
pip install pymongo

# IBM Db2
pip install ibm_db

# SQLite (内置，无需安装)
```

## 🎯 主要功能

### 数据库连接管理
- 支持多种数据库类型
- 连接测试功能
- 连接历史记录
- 安全的密码存储

### 表结构比较
- 自动检测表差异
- 列定义比较
- 索引比较
- 约束比较
- 支持忽略大小写

### SQL生成
- 自动生成同步SQL
- 支持多种数据库语法
- 智能语法转换
- 差异高亮显示

### 搜索和导航
- 实时搜索
- 结果高亮
- 导航快捷键
- 支持正则表达式

## 🏗️ 架构设计

项目采用工厂模式和策略模式设计，具有良好的扩展性：

```
src/
├── core/           # 核心功能模块
│   ├── db_connector.py    # 数据库连接器
│   ├── sql_parser.py      # SQL解析器
│   └── sql_generator.py   # SQL生成器
├── ui/             # 用户界面
├── data/           # 数据模型
├── i18n/           # 国际化
└── utils/          # 工具函数
```

### 扩展性设计

要添加新的数据库类型支持，只需：

1. 继承相应的基类
2. 实现具体的连接、解析、生成逻辑
3. 在工厂类中注册新类型

## 📖 使用说明

### 1. 连接数据库
- 点击"连接管理"按钮
- 选择数据库类型
- 填写连接信息
- 测试连接并保存

### 2. 比较表结构
- 左侧选择数据源（数据库或文件）
- 右侧选择数据源（数据库或文件）
- 点击"开始比较"
- 查看差异结果

### 3. 生成同步SQL
- 完成比较后，点击"生成同步SQL"
- 选择目标数据库
- 查看生成的SQL语句
- 复制到剪贴板

## 🔧 配置说明

### 数据库连接配置

#### MySQL
```json
{
  "host": "localhost",
  "port": 3306,
  "username": "user",
  "password": "password",
  "database": "dbname"
}
```

#### PostgreSQL
```json
{
  "host": "localhost",
  "port": 5432,
  "username": "user",
  "password": "password",
  "database": "dbname"
}
```

#### Oracle
```json
{
  "host": "localhost",
  "port": 1521,
  "username": "user",
  "password": "password",
  "service_name": "orcl"
}
```

#### SQL Server
```json
{
  "host": "localhost",
  "port": 1433,
  "username": "user",
  "password": "password",
  "database": "dbname",
  "driver": "ODBC Driver 17 for SQL Server"
}
```

#### SQLite
```json
{
  "file": "/path/to/database.db"
}
```

#### MongoDB
```json
{
  "host": "localhost",
  "port": 27017,
  "username": "user",
  "password": "password",
  "database": "dbname",
  "auth_source": "admin"
}
```

#### IBM Db2
```json
{
  "host": "localhost",
  "port": 50000,
  "username": "user",
  "password": "password",
  "database": "dbname"
}
```

## 🐛 故障排除

### 常见问题

1. **连接失败**
   - 检查网络连接
   - 验证连接参数
   - 确认数据库服务运行状态

2. **驱动未安装**
   - 安装相应的数据库驱动
   - 检查Python环境

3. **权限问题**
   - 确认数据库用户权限
   - 检查防火墙设置

### 日志和调试

应用会在控制台输出详细的调试信息，包括：
- 连接状态
- SQL执行结果
- 错误详情

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发环境设置

1. 克隆项目
2. 安装依赖
3. 运行测试
4. 提交代码

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**DBCompare** - 让数据库表结构比较变得简单高效！ 