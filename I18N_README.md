# 国际化功能使用说明

## 概述

本项目已成功集成了中英双语支持，用户可以通过菜单栏的"设置" -> "语言设置"来切换界面语言。

## 功能特性

### 1. 支持的语言
- **中文 (zh_CN)** - 默认语言
- **英文 (en_US)** - 英文界面

### 2. 语言切换
- 通过菜单栏 "设置" -> "语言设置" 打开语言设置对话框
- 选择目标语言后点击"应用"
- 应用会自动重启以应用新语言设置
- 重启过程支持Windows、macOS、Linux系统

### 3. 系统语言自动检测
- 首次启动时自动检测系统语言
- 支持Windows、macOS、Linux系统
- 如果不是中文系统，默认显示英文界面
- 检测到的语言设置会保存到数据库中

### 4. 已国际化的界面元素
- 主窗口标题和菜单
- 工具栏按钮和选项
- 左右数据源面板
- 连接管理对话框
- 目标数据库选择对话框
- SQL显示窗口
- 所有提示信息和错误消息

## 技术实现

### 1. 文件结构
```
src/
├── i18n/
│   ├── __init__.py
│   ├── i18n_manager.py      # 国际化管理器
│   ├── zh_CN.json          # 中文翻译文件
│   └── en_US.json          # 英文翻译文件
├── data/
│   └── models.py           # 数据模型（包含配置表）
├── ui/
│   ├── language_dialog.py   # 语言设置对话框
│   └── connection_dialog.py # 连接管理对话框（已国际化）
└── main.py                  # 主程序（已国际化）
```

### 2. 核心组件

#### I18nManager 类
- 负责加载和管理翻译文件
- 提供语言切换功能
- 支持格式化字符串翻译
- 使用SQLite数据库持久化语言设置

#### tr() 函数
- 便捷的翻译函数
- 自动获取当前语言的翻译文本
- 支持默认值回退

#### LanguageDialog 类
- 语言设置对话框
- 提供语言选择界面
- 处理语言切换逻辑
- 自动重启应用以应用新语言

### 3. 数据库配置功能

#### 配置表结构
```sql
CREATE TABLE app_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

#### 配置管理方法
```python
from data.models import ConnectionManager

# 创建连接管理器
connection_manager = ConnectionManager()

# 设置配置
connection_manager.set_config('language', 'en_US')
connection_manager.set_config('theme', 'dark')

# 获取配置
language = connection_manager.get_config('language', 'zh_CN')  # 第二个参数是默认值
theme = connection_manager.get_config('theme', 'light')
```

### 4. 使用方法

#### 在代码中使用翻译
```python
from i18n.i18n_manager import tr

# 简单翻译
button_text = tr("start_compare")

# 格式化字符串翻译
title = tr("sync_sql_title_right").format(
    left_name="数据库A", 
    right_name="数据库B"
)
```

#### 添加新的翻译文本
1. 在 `src/i18n/zh_CN.json` 中添加中文翻译
2. 在 `src/i18n/en_US.json` 中添加英文翻译
3. 在代码中使用 `tr("key")` 获取翻译

#### 添加新的语言支持
1. 创建新的翻译文件，如 `fr_FR.json`
2. 在 `I18nManager` 的 `get_language_name()` 方法中添加语言名称映射
3. 在 `LanguageDialog` 中添加语言选项

## 测试

### 运行测试脚本
```bash
python test_i18n.py
```

### 运行应用程序
```bash
python run_app.py
```

## 注意事项

1. **持久化存储**: 语言设置自动保存到SQLite数据库中，重启后保持设置
2. **系统语言检测**: 首次启动时自动检测系统语言，支持Windows、macOS、Linux
3. **自动重启**: 语言切换后应用会自动重启以应用新设置
4. **翻译完整性**: 确保所有翻译键在两种语言文件中都存在
5. **格式化字符串**: 使用 `.format()` 方法处理包含变量的翻译文本
6. **默认语言**: 默认使用中文，可以通过修改 `I18nManager` 的初始化来更改
7. **数据库配置**: 配置存储在 `app_config` 表中，支持多种配置项

## 扩展建议

1. **更多语言支持**: 添加法语、德语等其他语言
2. **动态语言切换**: 实现无需重启的语言切换功能
3. **配置管理界面**: 添加统一的配置管理界面
4. **配置导入导出**: 支持配置的备份和恢复功能
5. **主题支持**: 添加深色/浅色主题切换功能
