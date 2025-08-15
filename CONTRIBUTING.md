# 贡献指南

感谢您对DBCompare项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🌍 翻译改进

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/dbcompare.git
cd dbcompare
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. 运行应用

```bash
python app.py
```

## 代码规范

### Python代码风格

- 遵循PEP 8代码风格指南
- 使用4个空格缩进
- 行长度不超过120字符
- 使用有意义的变量和函数名

### 提交信息规范

使用清晰的提交信息，格式如下：

```
类型(范围): 简短描述

详细描述（可选）
```

类型包括：
- `feat`: 新功能
- `fix`: 修复Bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 分支命名

- `feature/功能名称`: 新功能开发
- `fix/问题描述`: Bug修复
- `docs/文档名称`: 文档更新
- `refactor/重构内容`: 代码重构

## 提交Pull Request

### 1. Fork项目

在GitHub上Fork本项目到您的账户。

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 3. 提交更改

```bash
git add .
git commit -m "feat: 添加新功能描述"
```

### 4. 推送分支

```bash
git push origin feature/your-feature-name
```

### 5. 创建Pull Request

在GitHub上创建Pull Request，并填写以下信息：

- **标题**: 简洁描述您的更改
- **描述**: 详细说明更改的原因和影响
- **关联Issue**: 如果修复了某个Issue，请关联它

## 报告Bug

在报告Bug时，请包含以下信息：

1. **操作系统**: Windows/macOS/Linux版本
2. **Python版本**: `python --version`
3. **DBCompare版本**: 当前使用的版本
4. **重现步骤**: 详细的重现步骤
5. **预期行为**: 您期望看到的结果
6. **实际行为**: 实际发生的情况
7. **错误信息**: 如果有错误信息，请完整提供

## 功能建议

在提出新功能建议时，请考虑：

1. **功能描述**: 详细描述您想要的功能
2. **使用场景**: 说明在什么情况下会用到这个功能
3. **实现建议**: 如果有实现思路，请提供建议
4. **优先级**: 说明这个功能对您的重要程度

## 国际化贡献

如果您想帮助改进翻译：

1. 查看 `src/i18n/` 目录下的翻译文件
2. 修改或添加翻译内容
3. 确保所有翻译键都有对应的翻译
4. 测试翻译是否正确显示

## 测试

在提交代码前，请确保：

1. 代码能够正常运行
2. 没有引入新的Bug
3. 遵循项目的代码规范
4. 更新相关文档

## 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 在GitHub上创建Issue
- 发送邮件到项目维护者

感谢您的贡献！🎉
