# PyQt6迁移说明

## 概述

由于tkinter在中文显示和跨平台兼容性方面存在一些问题，我们决定将整个项目从tkinter迁移到PyQt6。PyQt6提供了更好的中文支持、更现代的UI组件和更稳定的跨平台表现。

## 迁移原因

### tkinter的问题
1. **中文显示问题** - 在不同系统下中文显示异常
2. **字体管理困难** - 字体检测和配置复杂
3. **样式限制** - 样式定制能力有限
4. **跨平台兼容性** - 在不同操作系统下表现不一致

### PyQt6的优势
1. **优秀的中文支持** - 原生支持Unicode和中文显示
2. **现代化的UI** - 提供丰富的UI组件和样式系统
3. **强大的样式系统** - 支持CSS样式的样式表
4. **跨平台一致性** - 在不同操作系统下表现一致
5. **更好的性能** - 更快的渲染速度和响应性

## 项目结构变化

### 新增文件
```
app_pyqt.py                    # PyQt6版本启动文件
src/main_pyqt.py              # PyQt6版本主应用
src/ui/connection_dialog_pyqt.py # PyQt6版本连接对话框（待实现）
```

### 保留文件
```
src/core/                     # 核心业务逻辑（保持不变）
src/data/                     # 数据模型（保持不变）
src/utils/                    # 工具函数（保持不变）
```

### 废弃文件
```
src/main.py                   # tkinter版本主应用（已废弃）
src/ui/connection_dialog.py   # tkinter版本连接对话框（已废弃）
src/ui/styles.py              # tkinter样式管理器（已废弃）
src/ui/font_manager.py        # tkinter字体管理器（已废弃）
```

## 技术栈对比

| 特性 | tkinter | PyQt6 |
|------|---------|-------|
| 中文支持 | 有限 | 优秀 |
| 样式系统 | 基础 | 强大（CSS样式表） |
| 组件丰富度 | 基础 | 丰富 |
| 跨平台一致性 | 一般 | 优秀 |
| 性能 | 一般 | 优秀 |
| 学习曲线 | 简单 | 中等 |
| 文档支持 | 有限 | 丰富 |

## 主要改进

### 1. 界面设计
- **现代化外观** - 采用扁平化设计风格
- **响应式布局** - 支持窗口大小调整
- **统一主题** - 一致的视觉风格

### 2. 用户体验
- **更好的交互** - 流畅的动画和反馈
- **直观的操作** - 清晰的按钮和图标
- **智能提示** - 上下文相关的帮助信息

### 3. 功能增强
- **拖拽支持** - 支持文件拖拽操作
- **快捷键** - 完整的键盘快捷键支持
- **多语言** - 支持国际化

### 4. 技术特性
- **线程安全** - 更好的多线程支持
- **内存管理** - 更高效的内存使用
- **错误处理** - 更完善的异常处理

## 使用方法

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行PyQt6版本
```bash
python app_pyqt.py
```

### 运行tkinter版本（已废弃）
```bash
python app.py
```

## 开发计划

### 第一阶段：基础框架 ✅
- [x] 创建PyQt6主窗口
- [x] 实现基本布局
- [x] 设置样式系统

### 第二阶段：核心功能 🔄
- [ ] 实现连接管理对话框
- [ ] 实现文件选择功能
- [ ] 实现表结构显示
- [ ] 实现比较功能

### 第三阶段：高级功能 📋
- [ ] 实现SQL生成功能
- [ ] 实现历史记录管理
- [ ] 实现设置对话框
- [ ] 实现帮助系统

### 第四阶段：优化完善 📋
- [ ] 性能优化
- [ ] 用户体验优化
- [ ] 错误处理完善
- [ ] 文档完善

## 样式系统

PyQt6使用CSS样式表来定义界面样式，提供了强大的样式定制能力：

```css
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}
```

## 注意事项

1. **依赖管理** - 确保安装了PyQt6相关依赖
2. **版本兼容** - 使用PyQt6 6.4.0或更高版本
3. **系统要求** - 支持Windows 10+、macOS 10.14+、Ubuntu 18.04+
4. **开发环境** - 建议使用支持PyQt6的IDE（如PyCharm、VS Code）

## 迁移指南

如果你需要将现有的tkinter代码迁移到PyQt6，可以参考以下映射关系：

| tkinter组件 | PyQt6组件 | 说明 |
|------------|----------|------|
| tk.Tk() | QApplication | 应用程序实例 |
| tk.Toplevel | QMainWindow/QDialog | 窗口和对话框 |
| tk.Frame | QWidget/QFrame | 容器组件 |
| tk.Button | QPushButton | 按钮 |
| tk.Label | QLabel | 标签 |
| tk.Entry | QLineEdit | 输入框 |
| tk.Text | QTextEdit | 文本编辑器 |
| tk.Treeview | QTreeWidget | 树形视图 |
| tk.Menu | QMenuBar/QMenu | 菜单 |
| ttk.Style | QStyleSheet | 样式系统 |

## 总结

PyQt6迁移将为项目带来显著的改进：

- **更好的用户体验** - 现代化界面和流畅交互
- **更强的稳定性** - 优秀的跨平台兼容性
- **更丰富的功能** - 强大的组件和样式系统
- **更好的维护性** - 清晰的代码结构和丰富的文档

这个迁移将确保项目在未来的发展中具有更好的可扩展性和用户体验。 