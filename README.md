# DBCompare - MySQL表结构比较工具

一个用于比较MySQL数据库表结构的图形化工具，支持文件导入和数据库连接两种方式。

![截图](screenshot.png)
## 功能特性

- 🔍 **表结构比较**: 比较两个数据源的表结构差异
- 📁 **文件支持**: 支持导入SQL文件进行分析
- 🗄️ **数据库连接**: 支持直接连接MySQL数据库
- 🔄 **同步SQL生成**: 自动生成同步表结构的SQL语句
- 📊 **可视化界面**: 直观的差异显示界面
- 🔗 **连接管理**: 保存和管理数据库连接信息
- 📜 **历史记录**: 记录使用过的数据源
- 🌍 **国际化支持**: 支持中英文界面切换

## 项目结构

```
dbcompare/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── sql_parser.py      # SQL解析器
│   │   ├── sql_generator.py   # SQL生成器
│   │   └── db_connector.py    # 数据库连接器
│   ├── ui/                # 用户界面模块
│   │   ├── connection_dialog.py # 连接管理对话框
│   │   └── language_dialog.py  # 语言设置对话框
│   ├── data/              # 数据模型和存储
│   │   └── models.py          # 数据模型定义
│   ├── i18n/              # 国际化模块
│   │   ├── i18n_manager.py    # 国际化管理器
│   │   ├── zh_CN.json         # 中文翻译文件
│   │   └── en_US.json         # 英文翻译文件
│   ├── utils/             # 工具函数
│   │   └── util.py            # 通用工具函数
│   └── main.py            # 主应用程序
├── scripts/               # 构建和部署脚本
│   ├── build/             # 构建脚本
│   │   ├── build.py           # Python构建脚本
│   │   ├── build_with_spec.py # 高级构建脚本
│   │   ├── build_macos.sh     # macOS构建脚本
│   │   ├── build_linux.sh     # Linux构建脚本
│   │   └── build_windows.bat  # Windows构建脚本
│   └── deploy/            # 部署脚本
│       └── run_mac.sh         # macOS运行脚本
├── config/                # 配置文件
│   ├── build_config.py       # 构建配置
│   └── DBCompare.spec        # PyInstaller配置文件
├── docs/                  # 文档目录
│   └── BUILD_README.md    # 构建说明文档
├── app.py                 # 应用程序入口
├── build.py               # 构建脚本入口
├── requirements.txt       # 依赖包列表
├── setup.py              # 安装配置
├── pyproject.toml        # 项目配置
├── MANIFEST.in           # 包清单文件
├── icon.png              # 应用图标
└── README.md             # 项目说明
```

## 安装和运行

### 环境要求

- Python 3.7+
- PyQt6
- MySQL Connector/Python
- sqlparse

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python app.py
```

### 开发安装

```bash
pip install -e .
```

## 使用方法

1. **启动程序**: 运行 `python app.py`
2. **选择数据源**: 
   - 点击"连接"按钮连接数据库
   - 点击"文件"按钮选择SQL文件
3. **开始比较**: 选择两个数据源后点击"开始比较"
4. **查看差异**: 程序会显示表结构的差异
5. **生成同步SQL**: 点击"生成同步SQL"获取同步语句
6. **语言设置**: 通过"设置" -> "语言设置"切换界面语言

## 开发

### 构建应用程序

```bash
# 快速构建（推荐）
python build.py

# 平台特定构建
bash scripts/build/build_macos.sh    # macOS
bash scripts/build/build_linux.sh    # Linux
scripts/build/build_windows.bat      # Windows

# 高级构建选项
python scripts/build/build_with_spec.py --help
```

### 运行构建后的应用程序

```bash
# macOS
bash scripts/deploy/run_mac.sh
```

### 开发构建

```bash
python setup.py build
```

## 国际化

项目支持中英文界面切换，详细说明请参考 [I18N_README.md](I18N_README.md)。

## 项目结构

详细的项目结构说明请参考 [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 