"""
MySQL表结构比较工具 - PyQt6版本
主应用程序
"""

import sys
import os
import threading
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
    QCheckBox, QFrame, QGroupBox, QSplitter, QMessageBox,
    QFileDialog, QTextEdit, QDialog, QRadioButton, QButtonGroup,
    QGridLayout, QLineEdit, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QClipboard, QPalette, QIcon, QAction

from core.sql_parser import SQLParser
from core.sql_generator import SQLGenerator
from core.db_connector import DBConnector
from data.models import ConnectionManager, Connection, History
from ui.connection_dialog import ConnectionDialog, SelectConnectionDialog
from ui.language_dialog import LanguageDialog
from i18n.i18n_manager import get_i18n_manager, tr

class SQLCompareApp(QMainWindow):
    """MySQL表结构比较工具主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化变量
        self.sync_scroll = True
        self.hide_same = False
        self.show_missing_only = False
        self.sync_row_selection_enabled = False  # 控制行选择同步
        self.ignore_case = True  # 是否忽略大小写
        self.left_tables = {}
        self.right_tables = {}
        
        # 初始化组件
        self.sql_parser = SQLParser(ignore_case=self.ignore_case)
        self.sql_generator = SQLGenerator()
        self.db_connector = DBConnector()
        self.connection_manager = ConnectionManager()
        
        # 初始化国际化管理器
        self.i18n_manager = get_i18n_manager(self.connection_manager)
        
        self.setWindowTitle(tr("app_title"))
        self.showMaximized()
        
        # 应用Windows 11风格样式
        self.apply_windows11_style()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建界面
        self.create_ui()
        
        # 初始化历史记录
        self.connection_manager.update_history_display_format()
        self.update_history_lists()
    
    def apply_windows11_style(self):
        """应用Windows 11风格样式"""
        # Windows 11 现代化样式表
        style_sheet = """
        /* 主窗口样式 */
        QMainWindow {
            background-color: #fafafa;
            color: #202020;
        }
        
        /* 中央部件样式 */
        QWidget#centralWidget {
            background-color: #fafafa;
            border: none;
        }
        
        /* 工具栏样式 */
        QFrame#toolbar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f0f0f0);
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin: 0px;
            padding: 0px;
        }
        
        /* 按钮样式 - Windows 11风格 */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f8f8);
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px 16px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: #202020;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f8ff, stop:1 #e6f3ff);
            border: 1px solid #0078d4;
            color: #0078d4;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e6f3ff, stop:1 #d1e7ff);
            border: 1px solid #106ebe;
        }
        
        QPushButton:disabled {
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            color: #a0a0a0;
        }
        
        /* 主要操作按钮样式 */
        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #106ebe);
            border: 1px solid #0078d4;
            color: white;
            font-weight: 600;
        }
        
        QPushButton#primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #106ebe, stop:1 #005a9e);
            border: 1px solid #106ebe;
        }
        
        QPushButton#primary:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #005a9e, stop:1 #004578);
        }
        
        /* 复选框样式 */
        QCheckBox {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #d0d0d0;
            border-radius: 4px;
            background: white;
        }
        
        QCheckBox::indicator:hover {
            border: 2px solid #0078d4;
        }
        
        QCheckBox::indicator:checked {
            background: #0078d4;
            border: 2px solid #0078d4;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }
        
        /* 组合框样式 */
        QComboBox {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 6px 12px;
            background: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border: 1px solid #0078d4;
        }
        
        QComboBox:focus {
            border: 2px solid #0078d4;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzY2NjY2NiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            background: white;
            selection-background-color: #e6f3ff;
            selection-color: #202020;
            padding: 8px 0px;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            min-height: 32px;
            margin: 2px 0px;
            line-height: 32px;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            background: white;
            selection-background-color: #e6f3ff;
            selection-color: #202020;
            padding: 8px 0px;
            spacing: 4px;
        }
        
        /* 表格样式 */
        QTableWidget {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            gridline-color: #f0f0f0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
            color: #202020;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background: #e6f3ff;
            color: #202020;
        }
        
        QTableWidget::item:hover {
            background: #f8f9fa;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            border: none;
            border-bottom: 1px solid #dee2e6;
            padding: 10px 8px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
            font-weight: 600;
            color: #495057;
        }
        
        QHeaderView::section:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e9ecef, stop:1 #dee2e6);
        }
        
        /* 分组框样式 */
        QGroupBox {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #202020;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            background: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            background: white;
        }
        
        /* 分割器样式 */
        QSplitter::handle {
            background: #e0e0e0;
            border-radius: 2px;
        }
        
        QSplitter::handle:hover {
            background: #0078d4;
        }
        
        /* 标签样式 */
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        
        /* 文本编辑框样式 */
        QTextEdit {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
            background: white;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: #202020;
        }
        
        QTextEdit:focus {
            border: 2px solid #0078d4;
        }
        
        /* 对话框样式 */
        QDialog {
            background: #fafafa;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            background: #f0f0f0;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background: #f0f0f0;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background: #c0c0c0;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #a0a0a0;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        """
        
        self.setStyleSheet(style_sheet)
        
        # 设置窗口图标和属性
        # 尝试加载自定义图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # 如果自定义图标不存在，使用默认图标
            self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        # 设置字体
        app = QApplication.instance()
        if app:
            font = QFont("Segoe UI", 9)
            app.setFont(font)

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 设置菜单
        settings_menu = menubar.addMenu(tr("settings"))
        
        # 语言设置菜单项
        language_action = QAction(tr("language_settings"), self)
        language_action.triggered.connect(self.show_language_dialog)
        settings_menu.addAction(language_action)
    
    def show_language_dialog(self):
        """显示语言设置对话框"""
        dialog = LanguageDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 语言已更改，需要重启应用
            self.restart_application()
    
    def restart_application(self):
        """重启应用程序"""
        QApplication.quit()
        # 重新启动应用
        os.execv(sys.executable, ['python'] + sys.argv)

    def create_ui(self):
        """创建用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 工具栏
        self.create_toolbar(main_layout)
        
        # 主要内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setChildrenCollapsible(False)
        main_layout.addWidget(content_splitter, 1)  # 设置拉伸因子为1，让内容区域占用剩余空间
        
        # 左侧面板
        self.create_left_panel(content_splitter)
        
        # 右侧面板
        self.create_right_panel(content_splitter)
        
        # 设置分割器比例
        content_splitter.setSizes([800, 800])
        
    def create_toolbar(self, parent_layout):
        """创建工具栏"""
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbar")
        # 设置工具栏的高度，使其更紧凑
        # toolbar_frame.setMaximumHeight(50)
        # toolbar_frame.setMinimumHeight(45)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        # toolbar_layout.setSpacing(10)  # 减少间距
        # 设置边距，确保垂直居中且不超出容器
        # toolbar_layout.setContentsMargins(10, 6, 10, 6)  # 减少边距
        # 设置垂直对齐方式为居中
        toolbar_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # 左侧按钮组
        left_btn_layout = QHBoxLayout()
        left_btn_layout.setSpacing(10)
        left_btn_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # 连接管理按钮
        self.conn_btn = QPushButton(tr("connection_management"))
        self.conn_btn.setObjectName("primary")
        self.conn_btn.clicked.connect(self.show_connection_dialog)
        self.conn_btn.setFixedHeight(30)  # 进一步减小按钮高度
        left_btn_layout.addWidget(self.conn_btn)
        
        # 开始比较按钮
        self.compare_btn = QPushButton(tr("start_compare"))
        self.compare_btn.setObjectName("primary")
        self.compare_btn.clicked.connect(self.start_compare)
        self.compare_btn.setFixedHeight(30)  # 进一步减小按钮高度
        left_btn_layout.addWidget(self.compare_btn)
        
        # 生成同步SQL按钮
        self.generate_btn = QPushButton(tr("generate_sync_sql"))
        self.generate_btn.setObjectName("primary")
        self.generate_btn.clicked.connect(self.generate_sync_sql)
        self.generate_btn.setFixedHeight(30)  # 进一步减小按钮高度
        left_btn_layout.addWidget(self.generate_btn)
        
        toolbar_layout.addLayout(left_btn_layout)
        toolbar_layout.addStretch()
        
        # 右侧选项组
        right_option_layout = QHBoxLayout()
        right_option_layout.setSpacing(10)  # 减少间距
        right_option_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # 同步滚动复选框
        self.sync_scroll_check = QCheckBox(tr("sync_scroll"))
        self.sync_scroll_check.setChecked(self.sync_scroll)
        self.sync_scroll_check.toggled.connect(self.toggle_sync_scroll)
        self.sync_scroll_check.setFixedHeight(30)  # 进一步减小复选框高度
        right_option_layout.addWidget(self.sync_scroll_check)
        
        # 隐藏相同行复选框
        self.hide_same_check = QCheckBox(tr("hide_same_rows"))
        self.hide_same_check.setChecked(self.hide_same)
        self.hide_same_check.toggled.connect(self.toggle_hide_same)
        self.hide_same_check.setFixedHeight(30)  # 进一步减小复选框高度
        right_option_layout.addWidget(self.hide_same_check)
        
        # 仅显示缺失复选框
        self.show_missing_check = QCheckBox(tr("show_missing_only"))
        self.show_missing_check.setChecked(self.show_missing_only)
        self.show_missing_check.toggled.connect(self.toggle_show_missing)
        self.show_missing_check.setFixedHeight(30)  # 进一步减小复选框高度
        right_option_layout.addWidget(self.show_missing_check)
        
        # 忽略大小写复选框
        self.ignore_case_check = QCheckBox(tr("ignore_case"))
        self.ignore_case_check.setChecked(self.ignore_case)
        self.ignore_case_check.toggled.connect(self.toggle_ignore_case)
        self.ignore_case_check.setFixedHeight(30)  # 进一步减小复选框高度
        right_option_layout.addWidget(self.ignore_case_check)
        
        toolbar_layout.addLayout(right_option_layout)
        parent_layout.addWidget(toolbar_frame, 0)  # 设置拉伸因子为0，工具栏不拉伸
        
    def create_left_panel(self, parent):
        """创建左侧面板"""
        left_group = QGroupBox(tr("left_data_source"))
        parent.addWidget(left_group)
        
        left_layout = QVBoxLayout(left_group)
        left_layout.setSpacing(15)
        
        # 选择框架
        select_frame = QFrame()
        select_layout = QHBoxLayout(select_frame)
        select_layout.setSpacing(10)
        
        # 连接按钮 - 固定大小
        self.left_conn_btn = QPushButton(tr("connect"))
        self.left_conn_btn.clicked.connect(lambda: self.show_connection_dialog("left"))
        self.left_conn_btn.setFixedWidth(60)
        select_layout.addWidget(self.left_conn_btn)
        
        # 文件按钮 - 固定大小
        self.left_file_btn = QPushButton(tr("file"))
        self.left_file_btn.clicked.connect(lambda: self.select_file("left"))
        self.left_file_btn.setFixedWidth(60)
        select_layout.addWidget(self.left_file_btn)
        
        # 历史记录标签 - 固定大小
        history_label = QLabel(tr("history"))
        history_label.setFixedWidth(80)
        select_layout.addWidget(history_label)
        
        # 历史记录下拉框 - 占用剩余空间
        self.left_history_combo = QComboBox()
        self.left_history_combo.currentTextChanged.connect(
            lambda text: self.on_history_select("left", text)
        )
        select_layout.addWidget(self.left_history_combo, 1)  # 设置拉伸因子为1，占用剩余空间
        
        left_layout.addWidget(select_frame)
        
        # 表格视图
        self.left_tree = QTableWidget()
        self.left_tree.setColumnCount(3)
        self.left_tree.setHorizontalHeaderLabels([tr("sequence_number"), tr("field_name"), tr("field_definition")])
        self.left_tree.setColumnWidth(0, 60)
        self.left_tree.setColumnWidth(1, 200)
        # 设置第三列自动占用剩余空间
        self.left_tree.horizontalHeader().setStretchLastSection(True)
        self.left_tree.setAlternatingRowColors(True)
        self.left_tree.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        left_layout.addWidget(self.left_tree)
        
    def create_right_panel(self, parent):
        """创建右侧面板"""
        right_group = QGroupBox(tr("right_data_source"))
        parent.addWidget(right_group)
        
        right_layout = QVBoxLayout(right_group)
        right_layout.setSpacing(15)
        
        # 选择框架
        select_frame = QFrame()
        select_layout = QHBoxLayout(select_frame)
        select_layout.setSpacing(10)
        
        # 连接按钮 - 固定大小
        self.right_conn_btn = QPushButton(tr("connect"))
        self.right_conn_btn.clicked.connect(lambda: self.show_connection_dialog("right"))
        self.right_conn_btn.setFixedWidth(60)
        select_layout.addWidget(self.right_conn_btn)
        
        # 文件按钮 - 固定大小
        self.right_file_btn = QPushButton(tr("file"))
        self.right_file_btn.clicked.connect(lambda: self.select_file("right"))
        self.right_file_btn.setFixedWidth(60)
        select_layout.addWidget(self.right_file_btn)
        
        # 历史记录标签 - 固定大小
        history_label = QLabel(tr("history"))
        history_label.setFixedWidth(80)
        select_layout.addWidget(history_label)
        
        # 历史记录下拉框 - 占用剩余空间
        self.right_history_combo = QComboBox()
        self.right_history_combo.currentTextChanged.connect(
            lambda text: self.on_history_select("right", text)
        )
        select_layout.addWidget(self.right_history_combo, 1)  # 设置拉伸因子为1，占用剩余空间
        
        right_layout.addWidget(select_frame)
        
        # 表格视图
        self.right_tree = QTableWidget()
        self.right_tree.setColumnCount(3)
        self.right_tree.setHorizontalHeaderLabels([tr("sequence_number"), tr("field_name"), tr("field_definition")])
        self.right_tree.setColumnWidth(0, 60)
        self.right_tree.setColumnWidth(1, 200)
        # 设置第三列自动占用剩余空间
        self.right_tree.horizontalHeader().setStretchLastSection(True)
        self.right_tree.setAlternatingRowColors(True)
        self.right_tree.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        right_layout.addWidget(self.right_tree)
        
        # 连接同步滚动
        self.left_tree.verticalScrollBar().valueChanged.connect(self.sync_scroll_bars)
        self.right_tree.verticalScrollBar().valueChanged.connect(self.sync_scroll_bars)
        
        # 连接行选择同步
        self.left_tree.itemSelectionChanged.connect(self.sync_row_selection)
        self.right_tree.itemSelectionChanged.connect(self.sync_row_selection)
        
    def sync_scroll_bars(self):
        """同步滚动条"""
        if not self.sync_scroll:
            return
            
        sender = self.sender()
        if sender == self.left_tree.verticalScrollBar():
            self.right_tree.verticalScrollBar().setValue(sender.value())
        elif sender == self.right_tree.verticalScrollBar():
            self.left_tree.verticalScrollBar().setValue(sender.value())
            
    def sync_row_selection(self):
        """同步行选择"""
        if not self.sync_row_selection_enabled:
            return
            
        sender = self.sender()
        if sender == self.left_tree:
            # 左侧表格选择变化，同步到右侧
            selected_rows = self.left_tree.selectedItems()
            if selected_rows:
                row = selected_rows[0].row()
                self.sync_row_selection_enabled = False  # 防止循环触发
                self.right_tree.selectRow(row)
                self.sync_row_selection_enabled = True
        elif sender == self.right_tree:
            # 右侧表格选择变化，同步到左侧
            selected_rows = self.right_tree.selectedItems()
            if selected_rows:
                row = selected_rows[0].row()
                self.sync_row_selection_enabled = False  # 防止循环触发
                self.left_tree.selectRow(row)
                self.sync_row_selection_enabled = True
            
    def toggle_sync_scroll(self, checked):
        """切换同步滚动状态"""
        self.sync_scroll = checked
        
    def toggle_hide_same(self, checked):
        """切换隐藏相同行状态"""
        self.hide_same = checked
        self.show_differences()
        
    def toggle_show_missing(self, checked):
        """切换仅显示缺失状态"""
        self.show_missing_only = checked
        self.show_differences()
        
    def toggle_ignore_case(self, checked):
        """切换忽略大小写状态"""
        self.ignore_case = checked
        # 重新初始化SQL解析器
        self.sql_parser = SQLParser(ignore_case=self.ignore_case)
        # 如果已经有数据，重新比较
        if self.left_tables and self.right_tables:
            self.show_differences()
        
    def show_connection_dialog(self, side=None):
        """显示连接对话框"""
        if side is None or side is False:
            # 连接管理按钮 - 显示完整的连接管理窗口
            dialog = ConnectionDialog(self, self.connection_manager)
            dialog.exec()
        else:
            # 连接按钮 - 只显示连接选择窗口
            dialog = SelectConnectionDialog(self, self.connection_manager)
            if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_connection:
                self.on_connection_selected(side, dialog.selected_connection)
        
    def select_file(self, side):
        """选择SQL文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("select_sql_file"),
            "",
            tr("sql_files") + ";;" + tr("all_files")
        )
        
        if file_path:
            try:
                # 添加到历史记录
                history = History(
                    id=None,
                    side=side,
                    type="file",
                    value=file_path,
                    display=file_path,
                    last_used=datetime.now()
                )
                self.connection_manager.add_history(history)
                
                # 更新历史记录列表
                self.update_history_lists()
                
                # 设置当前选择
                if side == "left":
                    self.left_history_combo.setCurrentText(file_path)
                else:
                    self.right_history_combo.setCurrentText(file_path)
                    
                # 解析SQL文件
                if side == "left":
                    self.left_tables = self.sql_parser.parse_file(file_path)
                else:
                    self.right_tables = self.sql_parser.parse_file(file_path)
                    
                # 显示表结构
                self.show_tables(side)
                
            except Exception as e:
                QMessageBox.critical(self, tr("error"), f"{tr('file_load_failed')}: {str(e)}")
            
    def start_compare(self):
        """开始比较"""
        # 获取左右两侧的历史记录选择
        left_display = self.left_history_combo.currentText()
        right_display = self.right_history_combo.currentText()
        
        if not left_display or not right_display:
            QMessageBox.warning(self, tr("warning"), tr("please_select_two_data_sources"))
            return
            
        # 执行比较
        self.show_differences()
        
        # 启用行选择同步功能
        self.sync_row_selection_enabled = True
        
    def show_differences(self):
        """显示差异"""
        # 禁用行选择同步，避免在数据加载过程中触发
        self.sync_row_selection_enabled = False
        
        # 清空显示区域
        self.left_tree.setRowCount(0)
        self.right_tree.setRowCount(0)
        
        # 获取差异
        differences = self.sql_parser.compare_tables(self.left_tables, self.right_tables)
        
        # 获取所有表名
        all_tables = sorted(set(list(self.left_tables.keys()) + list(self.right_tables.keys())))
        
        # 准备数据
        left_data = []
        right_data = []
        
        # 为每个表创建数据
        for table_index, table_name in enumerate(all_tables, 1):
            # 获取左右表的字段
            left_columns = self.left_tables.get(table_name, {}).get('columns', {})
            right_columns = self.right_tables.get(table_name, {}).get('columns', {})
            
            # 计算字段数量
            left_count = len(left_columns)
            right_count = len(right_columns)
            
            # 检查表是否有差异
            has_table_differences = (
                table_name in differences.get('modified_tables', {}) or
                table_name in differences.get('added_tables', []) or
                table_name in differences.get('removed_tables', [])
            )
            
            # 如果启用了隐藏相同行且表没有差异，则跳过
            if self.hide_same and not has_table_differences:
                continue
                
            # 添加表头行
            left_data.append([f"{tr('table')}{table_index}", f"{tr('table_name')} {table_name}", f"{tr('field_count')} {left_count}"])
            right_data.append([f"{tr('table')}{table_index}", f"{tr('table_name')} {table_name}", f"{tr('field_count')} {right_count}"])
            
            # 添加字段信息
            all_columns = sorted(set(list(left_columns.keys()) + list(right_columns.keys())))
            
            for col_index, col_name in enumerate(all_columns, 1):
                left_def = left_columns.get(col_name, "")
                right_def = right_columns.get(col_name, "")
                
                # 确定是否有差异
                has_column_differences = False
                is_missing = False
                
                if table_name in differences.get('modified_tables', {}):
                    changes = differences['modified_tables'][table_name]
                    if 'columns' in changes:
                        cols_changes = changes['columns']
                        if (col_name in cols_changes.get('removed_columns', {}) or
                            col_name in cols_changes.get('added_columns', {}) or
                            col_name in cols_changes.get('modified_columns', {})):
                            has_column_differences = True
                
                if not left_def and right_def:
                    has_column_differences = True
                    is_missing = True
                if not right_def and left_def:
                    has_column_differences = True
                    is_missing = True
                
                # 如果启用了隐藏相同行且字段没有差异，则跳过
                if self.hide_same and not has_column_differences:
                    continue
                    
                # 如果启用了仅显示缺失且不是缺失字段，则跳过
                if self.show_missing_only and not is_missing:
                    continue
                
                # 准备数据
                left_def_display = left_def.get('raw', '') if isinstance(left_def, dict) else left_def
                right_def_display = right_def.get('raw', '') if isinstance(right_def, dict) else right_def
                
                left_row = [str(col_index), col_name, left_def_display or tr("missing")]
                right_row = [str(col_index), col_name, right_def_display or tr("missing")]
                
                left_data.append(left_row)
                right_data.append(right_row)
        
        # 填充表格
        self.fill_table(self.left_tree, left_data)
        self.fill_table(self.right_tree, right_data)
        
        # 设置差异颜色
        self.set_difference_colors(left_data, right_data, differences)
        
        # 重新启用行选择同步
        self.sync_row_selection_enabled = True
        
    def fill_table(self, table, data):
        """填充表格数据"""
        table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                table.setItem(row_index, col_index, item)
                
                # 设置表头行的样式
                if row_data[1].startswith(tr("table_name")):
                    item.setBackground(QColor(240, 240, 240))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                # 设置标题行的样式
                elif row_data[1] in [tr("field"), tr("index")]:
                    item.setBackground(QColor(220, 220, 220))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
        
    def set_difference_colors(self, left_data, right_data, differences):
        """设置差异颜色"""
        # 遍历数据，找到差异行并设置颜色
        for row_index, (left_row, right_row) in enumerate(zip(left_data, right_data)):
            # 跳过表头行
            if left_row[1].startswith("表名:"):
                continue
                
            # 检查是否是字段行
            if len(left_row) >= 3 and len(right_row) >= 3:
                col_name = left_row[1]
                left_def = left_row[2]
                right_def = right_row[2]
                
                # 检查是否有差异
                has_differences = False
                is_missing = False
                
                if left_def == tr("missing") or right_def == tr("missing"):
                    has_differences = True
                    is_missing = True
                elif left_def != right_def:
                    # 在忽略大小写模式下，需要标准化比较
                    if self.ignore_case:
                        from utils.util import normalize_sql_definition
                        left_normalized = normalize_sql_definition(left_def)
                        right_normalized = normalize_sql_definition(right_def)
                        if left_normalized != right_normalized:
                            has_differences = True
                    else:
                        has_differences = True
                
                # 设置颜色
                if has_differences:
                    color = QColor("green") if is_missing else QColor("red")
                    
                    # 设置左侧表格颜色
                    left_item = self.left_tree.item(row_index, 2)
                    if left_item:
                        left_item.setForeground(color)
                    
                    # 设置右侧表格颜色
                    right_item = self.right_tree.item(row_index, 2)
                    if right_item:
                        right_item.setForeground(color)
        
    def generate_sync_sql(self):
        """生成同步SQL"""
        # 检查是否有表数据
        if not self.left_tables and not self.right_tables:
            QMessageBox.warning(self, tr("warning"), tr("please_load_left_and_right_table_structure"))
            return
        elif not self.left_tables:
            QMessageBox.warning(self, tr("warning"), tr("please_load_left_table_structure"))
            return
        elif not self.right_tables:
            QMessageBox.warning(self, tr("warning"), tr("please_load_right_table_structure"))
            return
            
        # 创建目标库选择对话框
        dialog = TargetDatabaseDialog(self, self.connection_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            target_side = dialog.target_side
            left_name = dialog.left_name
            right_name = dialog.right_name
            
            try:
                if target_side == "right":
                    # 以右侧为目标库，将左侧结构同步到右侧
                    sync_sql = self.sql_generator.generate_sync_sql(self.left_tables, self.right_tables)
                    title = tr("sync_sql_title_right").format(left_name=left_name, right_name=right_name)
                else:
                    # 以左侧为目标库，将右侧结构同步到左侧
                    sync_sql = self.sql_generator.generate_sync_sql(self.right_tables, self.left_tables)
                    title = tr("sync_sql_title_left").format(right_name=right_name, left_name=left_name)
                
                # 显示SQL窗口
                self.show_sql_window(title, sync_sql)
                
            except Exception as e:
                QMessageBox.critical(self, tr("error"), f"{tr('generate_sync_sql_error')}:\n{str(e)}")
                
    def show_sql_window(self, title, sql_content):
        """显示SQL窗口"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setGeometry(200, 200, 900, 700)
        
        # 应用Windows 11风格样式
        dialog.setStyleSheet("""
        QDialog {
            background-color: #fafafa;
            color: #202020;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f8f8);
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px 16px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: #202020;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f8ff, stop:1 #e6f3ff);
            border: 1px solid #0078d4;
            color: #0078d4;
        }
        
        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #106ebe);
            border: 1px solid #0078d4;
            color: white;
            font-weight: 600;
        }
        
        QPushButton#primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #106ebe, stop:1 #005a9e);
            border: 1px solid #106ebe;
        }
        
        QTextEdit {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
            background: white;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: #202020;
        }
        
        QTextEdit:focus {
            border: 2px solid #0078d4;
        }
        
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 提示信息
        info_label = QLabel(tr("generated_sync_sql_prompt"))
        info_label.setStyleSheet("color: #666; font-weight: bold; margin-bottom: 10px; font-size: 14px;")
        layout.addWidget(info_label)
        
        # SQL文本区域
        text_edit = QTextEdit()
        text_edit.setPlainText(sql_content)
        text_edit.setFont(QFont("Consolas", 11))
        layout.addWidget(text_edit)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        # 复制按钮
        copy_btn = QPushButton(tr("copy_sql"))
        copy_btn.setObjectName("primary")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(sql_content))
        btn_layout.addWidget(copy_btn)
        
        btn_layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton(tr("close"))
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
        
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, tr("info"), tr("sql_copied_to_clipboard"))
        
    def update_history_lists(self):
        """更新历史记录列表"""
        # 获取历史记录
        left_history = self.connection_manager.get_history("left")
        right_history = self.connection_manager.get_history("right")
        
        # 更新左侧历史记录列表
        self.left_history_combo.clear()
        for history in left_history:
            self.left_history_combo.addItem(history.display)
            
        # 更新右侧历史记录列表
        self.right_history_combo.clear()
        for history in right_history:
            self.right_history_combo.addItem(history.display)
            
    def on_history_select(self, side, display):
        """历史记录选择回调"""
        if not display:
            return
            
        # 获取历史记录
        history_list = self.connection_manager.get_history(side)
        for history in history_list:
            if history.display == display:
                if history.type == "file":
                    # 解析SQL文件
                    if side == "left":
                        self.left_tables = self.sql_parser.parse_file(history.value)
                    else:
                        self.right_tables = self.sql_parser.parse_file(history.value)
                    
                    # 显示表结构
                    self.show_tables(side)
                elif history.type == "connection":
                    # 获取连接信息
                    conn = self.connection_manager.get_connection(history.value)
                    if conn.type == "mysql":
                        try:
                            # 连接到数据库
                            db_config = conn.config.copy()
                            db_config['user'] = db_config.pop('username')
                            self.db_connector.connect(db_config)
                            # 获取表结构
                            tables = self.db_connector.get_table_structure()
                            # 关闭连接
                            self.db_connector.close()
                            
                            # 更新表结构
                            if side == "left":
                                self.left_tables = tables
                            else:
                                self.right_tables = tables
                                
                            # 显示表结构
                            self.show_tables(side)
                        except Exception as e:
                            QMessageBox.critical(self, tr("error"), f"{tr('get_table_structure_failed')}: {str(e)}")
                    elif conn.type == "agent":
                        QMessageBox.information(self, tr("info"), tr("agent_connection_not_supported"))
                    
                # 更新最后使用时间
                self.connection_manager.update_history_last_used(history.id)
                break
                
        # 显示差异
        self.show_tables(side)
        
    def on_connection_selected(self, side, connection):
        """连接选择回调"""
        # 生成显示文本
        if connection.type == "mysql":
            config = connection.config
            database_name = config.get('database', '')
            if database_name:
                display = f"{connection.name} ({config['host']}:{config['port']}/{database_name})"
            else:
                display = f"{connection.name} ({config['host']}:{config['port']})"
        else:
            display = f"{connection.name} ({connection.config['url']})"
            
        # 添加到历史记录
        history = History(
            id=None,
            side=side,
            type="connection",
            value=connection.id,
            display=display,
            last_used=datetime.now()
        )
        self.connection_manager.add_history(history)
        
        # 更新历史记录列表
        self.update_history_lists()
        
        # 设置当前选择
        if side == "left":
            self.left_history_combo.setCurrentText(display)
        else:
            self.right_history_combo.setCurrentText(display)
            
        # 从数据库获取表结构
        if connection.type == "mysql":
            try:
                # 连接到数据库
                db_config = connection.config.copy()
                db_config['user'] = db_config.pop('username')
                self.db_connector.connect(db_config)
                # 获取表结构
                tables = self.db_connector.get_table_structure()
                # 关闭连接
                self.db_connector.close()
                
                # 更新表结构
                if side == "left":
                    self.left_tables = tables
                else:
                    self.right_tables = tables
                    
                # 显示表结构
                self.show_tables(side)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取表结构失败: {str(e)}")
        elif connection.type == "agent":
            QMessageBox.information(self, tr("info"), tr("agent_connection_not_supported"))
        
    def show_tables(self, side):
        """显示表结构"""
        # 清空显示区域
        table = self.left_tree if side == "left" else self.right_tree
        table.setRowCount(0)
        
        # 获取表数据
        tables = self.left_tables if side == "left" else self.right_tables
        
        # 获取所有表名
        all_tables = sorted(tables.keys())
        
        # 准备数据
        table_data = []
        
        # 为每个表创建数据
        for table_index, table_name in enumerate(all_tables, 1):
            # 获取表的字段
            columns = tables[table_name].get('columns', {})
            indexes = tables[table_name].get('indexes', {})
            
            # 计算字段数量和索引数量
            column_count = len(columns)
            index_count = len(indexes)
            
            # 添加表头行
            table_data.append([f"{tr('table')}{table_index}", f"{tr('table_name')} {table_name}", f"{tr('field_count')} {column_count} {tr('index_count')} {index_count}"])
            
            # 添加字段信息
            if columns:
                # 添加字段标题行
                table_data.append(["", tr("field"), ""])
                
                # 添加字段行
                for col_index, (col_name, col_def) in enumerate(sorted(columns.items()), 1):
                    col_def_display = col_def.get('raw', '') if isinstance(col_def, dict) else col_def
                    table_data.append([str(col_index), col_name, col_def_display])
            
            # 添加索引信息
            if indexes:
                # 添加索引标题行
                table_data.append(["", tr("index"), ""])
                
                # 添加索引行
                for idx_index, (idx_name, idx_def) in enumerate(sorted(indexes.items()), 1):
                    idx_type = idx_def.get('type', '')
                    idx_columns = idx_def.get('columns', '')
                    idx_def_display = f"{idx_type} ({idx_columns})"
                    table_data.append([str(idx_index), idx_name, idx_def_display])
        
        # 填充表格
        self.fill_table(table, table_data)


class TargetDatabaseDialog(QDialog):
    """目标数据库选择对话框"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.target_side = "right"
        self.left_name = tr("left_data_source")
        self.right_name = tr("right_data_source")
        
        self.setWindowTitle(tr("select_target_database"))
        self.setModal(True)
        self.setGeometry(300, 300, 500, 300)
        self.center_on_screen()
        
        # 应用Windows 11风格样式
        self.apply_windows11_style()
        
        self.setup_ui()
    
    def center_on_screen(self):
        """将对话框居中显示在屏幕上"""
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            screen_geometry = screen.availableGeometry()
            dialog_geometry = self.geometry()
            x = (screen_geometry.width() - dialog_geometry.width()) // 2
            y = (screen_geometry.height() - dialog_geometry.height()) // 2
            self.move(x, y)
    
    def apply_windows11_style(self):
        """应用Windows 11风格样式"""
        style_sheet = """
        QDialog {
            background-color: #fafafa;
            color: #202020;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f8f8);
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px 16px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: #202020;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f8ff, stop:1 #e6f3ff);
            border: 1px solid #0078d4;
            color: #0078d4;
        }
        
        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #106ebe);
            border: 1px solid #0078d4;
            color: white;
            font-weight: 600;
        }
        
        QPushButton#primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #106ebe, stop:1 #005a9e);
            border: 1px solid #106ebe;
        }
        
        QRadioButton {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
            spacing: 8px;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #d0d0d0;
            border-radius: 9px;
            background: white;
        }
        
        QRadioButton::indicator:hover {
            border: 2px solid #0078d4;
        }
        
        QRadioButton::indicator:checked {
            background: #0078d4;
            border: 2px solid #0078d4;
        }
        
        QGroupBox {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #202020;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            background: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            background: white;
        }
        
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        """
        
        self.setStyleSheet(style_sheet)
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(tr("select_target_database"))
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel(tr("select_target_database_desc"))
        desc_label.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 10px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 获取左右数据库的名称
        left_history = self.connection_manager.get_history("left")
        right_history = self.connection_manager.get_history("right")
        
        if left_history:
            self.left_name = left_history[0].display
        if right_history:
            self.right_name = right_history[0].display
        
        # 选项组
        option_group = QGroupBox(tr("sync_direction"))
        option_layout = QVBoxLayout(option_group)
        option_layout.setSpacing(15)
        
        # 单选按钮组
        self.button_group = QButtonGroup()
        
        # 第一个选项
        self.right_radio = QRadioButton(tr("target_right_database").format(right_name=self.right_name))
        self.right_radio.setChecked(True)
        self.button_group.addButton(self.right_radio, 1)
        option_layout.addWidget(self.right_radio)
        
        # 第二个选项
        self.left_radio = QRadioButton(tr("target_left_database").format(left_name=self.left_name))
        self.button_group.addButton(self.left_radio, 2)
        option_layout.addWidget(self.left_radio)
        
        layout.addWidget(option_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton(tr("confirm"))
        ok_btn.setObjectName("primary")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # 连接信号
        self.button_group.buttonClicked.connect(self.on_button_clicked)
        
    def on_button_clicked(self, button):
        """按钮点击事件"""
        if button == self.right_radio:
            self.target_side = "right"
        elif button == self.left_radio:
            self.target_side = "left"


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName(tr("app_title"))
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("DBCompare")
    
    # 设置应用图标
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # 创建主窗口
    window = SQLCompareApp()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 