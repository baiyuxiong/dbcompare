"""
连接管理对话框 - PyQt6版本
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTreeWidget, QTreeWidgetItem, QGroupBox,
    QGridLayout, QMessageBox,  QSplitter, QSizePolicy, QApplication,
    QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from data.models import Connection, ConnectionManager
from datetime import datetime
from src.i18n.i18n_manager import tr


class ConnectionDialog(QDialog):
    """连接管理对话框"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.selected_connection = None
        
        self.setWindowTitle(tr("connection_management"))
        self.setGeometry(200, 200, 900, 350)
        self.setModal(True)
        self.center_on_screen()
        
        # 应用Windows 11风格样式
        self.apply_windows11_style()
        
        self.setup_ui()
        self.load_connections()
        
        # 初始化时显示MySQL配置，隐藏PostgreSQL配置
        self.on_database_type_changed("MySQL")
    
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
        /* 对话框样式 */
        QDialog {
            background-color: #fafafa;
            color: #202020;
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
        
        /* 输入框样式 */
        QLineEdit {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px 12px;
            background: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
            min-height: 20px;
        }
        
        QLineEdit:hover {
            border: 1px solid #0078d4;
        }
        
        QLineEdit:focus {
            border: 2px solid #0078d4;
            background: #fafafa;
        }
        
        /* 树形控件样式 */
        QTreeWidget {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
            color: #202020;
            gridline-color: #f0f0f0;
        }
        
        QTreeWidget::item {
            padding: 6px;
            border: none;
        }
        
        QTreeWidget::item:selected {
            background: #e6f3ff;
            color: #202020;
        }
        
        QTreeWidget::item:hover {
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
        
        /* 标签样式 */
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        
        /* 分割器样式 */
        QSplitter::handle {
            background: #e0e0e0;
            border-radius: 2px;
        }
        
        QSplitter::handle:hover {
            background: #0078d4;
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
        """
        
        self.setStyleSheet(style_sheet)
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧：连接列表
        self.create_connection_list(splitter)
        
        # 右侧：连接详情
        self.create_connection_details(splitter)
        
        # 设置分割器比例
        splitter.setSizes([450, 450])
        
    def create_connection_list(self, parent):
        """创建连接列表"""
        list_group = QGroupBox("连接列表")
        parent.addWidget(list_group)
        
        list_layout = QVBoxLayout(list_group)
        list_layout.setSpacing(15)
        
        # 连接树形视图
        self.connection_tree = QTreeWidget()
        self.connection_tree.setHeaderLabels(["名称", "类型", "主机", "数据库名"])
        self.connection_tree.setColumnWidth(0, 100)
        self.connection_tree.setColumnWidth(1, 50)
        self.connection_tree.setColumnWidth(2, 120)
        self.connection_tree.setColumnWidth(3, 120)
        self.connection_tree.setStyleSheet("QTreeWidget::item { padding: 8px; }")
        self.connection_tree.itemClicked.connect(self.on_connection_selected)
        list_layout.addWidget(self.connection_tree)
        
        # 列表操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        add_btn = QPushButton(tr("add_connection"))
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self.add_connection)
        btn_layout.addWidget(add_btn)
        
        delete_btn = QPushButton(tr("delete_connection"))
        delete_btn.clicked.connect(self.delete_connection)
        btn_layout.addWidget(delete_btn)
        
        list_layout.addLayout(btn_layout)
        
    def create_connection_details(self, parent):
        """创建连接详情"""
        details_group = QGroupBox("连接详情")
        parent.addWidget(details_group)
        
        details_layout = QVBoxLayout(details_group)
        details_layout.setSpacing(12)
        details_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 基本信息
        basic_layout = QGridLayout()
        basic_layout.setSpacing(8)
        
        # 连接名称
        basic_layout.addWidget(QLabel(tr("connection_name") + ":"), 0, 0)
        self.name_edit = QLineEdit()
        basic_layout.addWidget(self.name_edit, 0, 1)
        
        # 数据库类型选择
        basic_layout.addWidget(QLabel(tr("database_type") + ":"), 1, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItem("MySQL", "mysql")
        self.type_combo.addItem("PostgreSQL", "postgresql")
        self.type_combo.addItem("Oracle", "oracle")
        self.type_combo.addItem("SQL Server", "sqlserver")
        self.type_combo.addItem("SQLite", "sqlite")
        self.type_combo.addItem("MongoDB", "mongodb")
        self.type_combo.addItem("IBM Db2", "db2")
        self.type_combo.currentTextChanged.connect(self.on_database_type_changed)
        basic_layout.addWidget(self.type_combo, 1, 1)
        
        details_layout.addLayout(basic_layout)
        
        # MySQL配置
        mysql_group = QGroupBox("MySQL配置")
        mysql_group.setStyleSheet("QGroupBox { padding: 8px; }")
        mysql_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(mysql_group)
        
        mysql_layout = QGridLayout(mysql_group)
        mysql_layout.setSpacing(4)
        mysql_layout.setVerticalSpacing(2)
        
        # 主机地址
        mysql_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.host_edit = QLineEdit()
        self.host_edit.setText("localhost")
        self.host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.host_edit, 0, 1)
        
        # 端口
        mysql_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.port_edit = QLineEdit()
        self.port_edit.setText("3306")
        self.port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.port_edit, 1, 1)
        
        # 用户名
        mysql_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.username_edit = QLineEdit()
        self.username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.username_edit, 2, 1)
        
        # 密码
        mysql_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.password_edit, 3, 1)
        
        # 数据库名
        mysql_layout.addWidget(QLabel(tr("database") + ":"), 4, 0)
        self.database_edit = QLineEdit()
        self.database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.database_edit, 4, 1)
        
        # 设置列拉伸
        # mysql_layout.setColumnStretch(1, 1)
        
        # PostgreSQL配置
        postgresql_group = QGroupBox("PostgreSQL配置")
        postgresql_group.setStyleSheet("QGroupBox { padding: 8px; }")
        postgresql_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(postgresql_group)
        
        postgresql_layout = QGridLayout(postgresql_group)
        postgresql_layout.setSpacing(4)
        postgresql_layout.setVerticalSpacing(2)
        
        # 主机地址
        postgresql_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.pg_host_edit = QLineEdit()
        self.pg_host_edit.setText("localhost")
        self.pg_host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        postgresql_layout.addWidget(self.pg_host_edit, 0, 1)
        
        # 端口
        postgresql_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.pg_port_edit = QLineEdit()
        self.pg_port_edit.setText("5432")
        self.pg_port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        postgresql_layout.addWidget(self.pg_port_edit, 1, 1)
        
        # 用户名
        postgresql_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.pg_username_edit = QLineEdit()
        self.pg_username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        postgresql_layout.addWidget(self.pg_username_edit, 2, 1)
        
        # 密码
        postgresql_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.pg_password_edit = QLineEdit()
        self.pg_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pg_password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        postgresql_layout.addWidget(self.pg_password_edit, 3, 1)
        
        # 数据库名
        postgresql_layout.addWidget(QLabel(tr("database") + ":"), 4, 0)
        self.pg_database_edit = QLineEdit()
        self.pg_database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        postgresql_layout.addWidget(self.pg_database_edit, 4, 1)
        
        # 设置列拉伸
        # postgresql_layout.setColumnStretch(1, 1)
        
        # Oracle配置
        oracle_group = QGroupBox("Oracle配置")
        oracle_group.setStyleSheet("QGroupBox { padding: 8px; }")
        oracle_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(oracle_group)
        
        oracle_layout = QGridLayout(oracle_group)
        oracle_layout.setSpacing(4)
        oracle_layout.setVerticalSpacing(2)
        
        # 主机地址
        oracle_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.oracle_host_edit = QLineEdit()
        self.oracle_host_edit.setText("localhost")
        self.oracle_host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        oracle_layout.addWidget(self.oracle_host_edit, 0, 1)
        
        # 端口
        oracle_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.oracle_port_edit = QLineEdit()
        self.oracle_port_edit.setText("1521")
        self.oracle_port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        oracle_layout.addWidget(self.oracle_port_edit, 1, 1)
        
        # 用户名
        oracle_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.oracle_username_edit = QLineEdit()
        self.oracle_username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        oracle_layout.addWidget(self.oracle_username_edit, 2, 1)
        
        # 密码
        oracle_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.oracle_password_edit = QLineEdit()
        self.oracle_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.oracle_password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        oracle_layout.addWidget(self.oracle_password_edit, 3, 1)
        
        # 服务名/SID
        oracle_layout.addWidget(QLabel(tr("service_name") + "/SID:"), 4, 0)
        self.oracle_service_edit = QLineEdit()
        self.oracle_service_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        oracle_layout.addWidget(self.oracle_service_edit, 4, 1)
        
        # SQL Server配置
        sqlserver_group = QGroupBox("SQL Server配置")
        sqlserver_group.setStyleSheet("QGroupBox { padding: 8px; }")
        sqlserver_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(sqlserver_group)
        
        sqlserver_layout = QGridLayout(sqlserver_group)
        sqlserver_layout.setSpacing(4)
        sqlserver_layout.setVerticalSpacing(2)
        
        # 主机地址
        sqlserver_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.sqlserver_host_edit = QLineEdit()
        self.sqlserver_host_edit.setText("localhost")
        self.sqlserver_host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_host_edit, 0, 1)
        
        # 端口
        sqlserver_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.sqlserver_port_edit = QLineEdit()
        self.sqlserver_port_edit.setText("1433")
        self.sqlserver_port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_port_edit, 1, 1)
        
        # 用户名
        sqlserver_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.sqlserver_username_edit = QLineEdit()
        self.sqlserver_username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_username_edit, 2, 1)
        
        # 密码
        sqlserver_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.sqlserver_password_edit = QLineEdit()
        self.sqlserver_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.sqlserver_password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_password_edit, 3, 1)
        
        # 数据库名
        sqlserver_layout.addWidget(QLabel(tr("database") + ":"), 4, 0)
        self.sqlserver_database_edit = QLineEdit()
        self.sqlserver_database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_database_edit, 4, 1)
        
        # 驱动
        sqlserver_layout.addWidget(QLabel(tr("driver") + ":"), 5, 0)
        self.sqlserver_driver_edit = QLineEdit()
        self.sqlserver_driver_edit.setText("ODBC Driver 17 for SQL Server")
        self.sqlserver_driver_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlserver_layout.addWidget(self.sqlserver_driver_edit, 5, 1)
        
        # SQLite配置
        sqlite_group = QGroupBox("SQLite配置")
        sqlite_group.setStyleSheet("QGroupBox { padding: 8px; }")
        sqlite_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(sqlite_group)
        
        sqlite_layout = QGridLayout(sqlite_group)
        sqlite_layout.setSpacing(4)
        sqlite_layout.setVerticalSpacing(2)
        
        # 数据库文件
        sqlite_layout.addWidget(QLabel(tr("database_file") + ":"), 0, 0)
        self.sqlite_file_edit = QLineEdit()
        self.sqlite_file_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sqlite_layout.addWidget(self.sqlite_file_edit, 0, 1)
        
        # 浏览按钮
        self.sqlite_browse_btn = QPushButton(tr("browse"))
        self.sqlite_browse_btn.clicked.connect(self.browse_sqlite_file)
        sqlite_layout.addWidget(self.sqlite_browse_btn, 0, 2)
        
        # MongoDB配置
        mongodb_group = QGroupBox("MongoDB配置")
        mongodb_group.setStyleSheet("QGroupBox { padding: 8px; }")
        mongodb_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(mongodb_group)
        
        mongodb_layout = QGridLayout(mongodb_group)
        mongodb_layout.setSpacing(4)
        mongodb_layout.setVerticalSpacing(2)
        
        # 主机地址
        mongodb_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.mongodb_host_edit = QLineEdit()
        self.mongodb_host_edit.setText("localhost")
        self.mongodb_host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_host_edit, 0, 1)
        
        # 端口
        mongodb_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.mongodb_port_edit = QLineEdit()
        self.mongodb_port_edit.setText("27017")
        self.mongodb_port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_port_edit, 1, 1)
        
        # 用户名
        mongodb_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.mongodb_username_edit = QLineEdit()
        self.mongodb_username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_username_edit, 2, 1)
        
        # 密码
        mongodb_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.mongodb_password_edit = QLineEdit()
        self.mongodb_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.mongodb_password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_password_edit, 3, 1)
        
        # 数据库名
        mongodb_layout.addWidget(QLabel(tr("database") + ":"), 4, 0)
        self.mongodb_database_edit = QLineEdit()
        self.mongodb_database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_database_edit, 4, 1)
        
        # 认证源
        mongodb_layout.addWidget(QLabel(tr("auth_source") + ":"), 5, 0)
        self.mongodb_auth_source_edit = QLineEdit()
        self.mongodb_auth_source_edit.setText("admin")
        self.mongodb_auth_source_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mongodb_layout.addWidget(self.mongodb_auth_source_edit, 5, 1)
        
        # Db2配置
        db2_group = QGroupBox("IBM Db2配置")
        db2_group.setStyleSheet("QGroupBox { padding: 8px; }")
        db2_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        details_layout.addWidget(db2_group)
        
        db2_layout = QGridLayout(db2_group)
        db2_layout.setSpacing(4)
        db2_layout.setVerticalSpacing(2)
        
        # 主机地址
        db2_layout.addWidget(QLabel(tr("host") + ":"), 0, 0)
        self.db2_host_edit = QLineEdit()
        self.db2_host_edit.setText("localhost")
        self.db2_host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        db2_layout.addWidget(self.db2_host_edit, 0, 1)
        
        # 端口
        db2_layout.addWidget(QLabel(tr("port") + ":"), 1, 0)
        self.db2_port_edit = QLineEdit()
        self.db2_port_edit.setText("50000")
        self.db2_port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        db2_layout.addWidget(self.db2_port_edit, 1, 1)
        
        # 用户名
        db2_layout.addWidget(QLabel(tr("username") + ":"), 2, 0)
        self.db2_username_edit = QLineEdit()
        self.db2_username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        db2_layout.addWidget(self.db2_username_edit, 2, 1)
        
        # 密码
        db2_layout.addWidget(QLabel(tr("password") + ":"), 3, 0)
        self.db2_password_edit = QLineEdit()
        self.db2_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.db2_password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        db2_layout.addWidget(self.db2_password_edit, 3, 1)
        
        # 数据库名
        db2_layout.addWidget(QLabel(tr("database") + ":"), 4, 0)
        self.db2_database_edit = QLineEdit()
        self.db2_database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        db2_layout.addWidget(self.db2_database_edit, 4, 1)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        test_btn = QPushButton(tr("test_connection"))
        test_btn.clicked.connect(self.test_connection)
        btn_layout.addWidget(test_btn)
        
        save_btn = QPushButton(tr("confirm"))
        save_btn.setObjectName("primary")
        save_btn.clicked.connect(self.save_connection)
        btn_layout.addWidget(save_btn)
        
        details_layout.addLayout(btn_layout)
        
        # 添加弹性空间，让元素靠上排列
        details_layout.addStretch()
    
    def browse_sqlite_file(self):
        """浏览SQLite数据库文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("select_sqlite_file"),
            "",
            tr("sqlite_files") + ";;" + tr("all_files")
        )
        if file_path:
            self.sqlite_file_edit.setText(file_path)
        
    def on_database_type_changed(self, text):
        """数据库类型改变时的处理"""
        # 隐藏所有配置组
        for child in self.findChildren(QGroupBox):
            if "配置" in child.title():
                child.setVisible(False)
        
        # 根据选择的类型显示相应的配置组
        if text == "MySQL":
            for child in self.findChildren(QGroupBox):
                if "MySQL" in child.title():
                    child.setVisible(True)
        elif text == "PostgreSQL":
            for child in self.findChildren(QGroupBox):
                if "PostgreSQL" in child.title():
                    child.setVisible(True)
        elif text == "Oracle":
            for child in self.findChildren(QGroupBox):
                if "Oracle" in child.title():
                    child.setVisible(True)
        elif text == "SQL Server":
            for child in self.findChildren(QGroupBox):
                if "SQL Server" in child.title():
                    child.setVisible(True)
        elif text == "SQLite":
            for child in self.findChildren(QGroupBox):
                if "SQLite" in child.title():
                    child.setVisible(True)
        elif text == "MongoDB":
            for child in self.findChildren(QGroupBox):
                if "MongoDB" in child.title():
                    child.setVisible(True)
        elif text == "IBM Db2":
            for child in self.findChildren(QGroupBox):
                if "IBM Db2" in child.title():
                    child.setVisible(True)
        
    def load_connections(self):
        """加载连接列表"""
        self.connection_tree.clear()
        
        connections = self.connection_manager.get_all_connections()
        for conn in connections:
            item = QTreeWidgetItem(self.connection_tree)
            item.setText(0, conn.name)
            item.setText(1, conn.type)
            
            if conn.type == "mysql":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "postgresql":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "oracle":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('service_name', ''))
            elif conn.type == "sqlserver":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "sqlite":
                config = conn.config
                item.setText(2, tr("local_file"))
                item.setText(3, config.get('file', ''))
            elif conn.type == "mongodb":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "db2":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            else:
                item.setText(2, conn.config.get('url', ''))
                item.setText(3, '')
                
            item.setData(0, Qt.ItemDataRole.UserRole, conn.id)
            
    def on_connection_selected(self, item):
        """连接选择事件"""
        conn_id = item.data(0, Qt.ItemDataRole.UserRole)
        if conn_id:
            connection = self.connection_manager.get_connection(conn_id)
            if connection:
                self.load_connection_details(connection)
                self.selected_connection = connection
                print(f"选择了连接: {connection.name} (ID: {connection.id})")  # 调试信息
        else:
            # 如果没有选择有效的连接，清空选择状态
            self.selected_connection = None
                
    def load_connection_details(self, connection):
        """加载连接详情"""
        self.name_edit.setText(connection.name)
        
        if connection.type == "mysql":
            config = connection.config
            
            # 设置类型选择
            self.type_combo.setCurrentText("MySQL")
            
            # 加载MySQL配置
            self.host_edit.setText(config.get('host', ''))
            self.port_edit.setText(str(config.get('port', '')))
            self.username_edit.setText(config.get('username', ''))
            self.password_edit.setText(config.get('password', ''))
            self.database_edit.setText(config.get('database', ''))
            
        elif connection.type == "postgresql":
            config = connection.config
            
            # 设置类型选择
            self.type_combo.setCurrentText("PostgreSQL")
            
            # 加载PostgreSQL配置
            self.pg_host_edit.setText(config.get('host', ''))
            self.pg_port_edit.setText(str(config.get('port', '')))
            self.pg_username_edit.setText(config.get('username', ''))
            self.pg_password_edit.setText(config.get('password', ''))
            self.pg_database_edit.setText(config.get('database', ''))
            
        elif connection.type == "oracle":
            config = connection.config
            
            # 设置类型选择
            self.type_combo.setCurrentText("Oracle")
            
            # 加载Oracle配置
            self.oracle_host_edit.setText(config.get('host', ''))
            self.oracle_port_edit.setText(str(config.get('port', '')))
            self.oracle_username_edit.setText(config.get('username', ''))
            self.oracle_password_edit.setText(config.get('password', ''))
            self.oracle_service_edit.setText(config.get('service_name', ''))
            
        elif connection.type == "sqlserver":
            config = connection.config
            
            # 设置类型选择
            self.type_combo.setCurrentText("SQL Server")
            
            # 加载SQL Server配置
            self.sqlserver_host_edit.setText(config.get('host', ''))
            self.sqlserver_port_edit.setText(str(config.get('port', '')))
            self.sqlserver_username_edit.setText(config.get('username', ''))
            self.sqlserver_password_edit.setText(config.get('password', ''))
            self.sqlserver_database_edit.setText(config.get('database', ''))
            self.sqlserver_driver_edit.setText(config.get('driver', ''))
            
        elif connection.type == "sqlite":
            config = connection.config
            
            # 设置类型选择
            self.type_combo.setCurrentText("SQLite")
            
            # 加载SQLite配置
            self.sqlite_file_edit.setText(config.get('file', ''))
            
        elif connection.type == "mongodb":
            config = connection.config
            self.type_combo.setCurrentText("MongoDB")
            self.mongodb_host_edit.setText(config.get('host', ''))
            self.mongodb_port_edit.setText(str(config.get('port', '')))
            self.mongodb_username_edit.setText(config.get('username', ''))
            self.mongodb_password_edit.setText(config.get('password', ''))
            self.mongodb_database_edit.setText(config.get('database', ''))
            self.mongodb_auth_source_edit.setText(config.get('auth_source', ''))

        elif connection.type == "db2":
            config = connection.config
            self.type_combo.setCurrentText("IBM Db2")
            self.db2_host_edit.setText(config.get('host', ''))
            self.db2_port_edit.setText(str(config.get('port', '')))
            self.db2_username_edit.setText(config.get('username', ''))
            self.db2_password_edit.setText(config.get('password', ''))
            self.db2_database_edit.setText(config.get('database', ''))
            
    def add_connection(self):
        """添加连接"""
        # 清空表单
        self.name_edit.clear()
        self.host_edit.setText("localhost")
        self.port_edit.setText("3306")
        self.username_edit.clear()
        self.password_edit.clear()
        self.database_edit.clear()
        
        # 清空PostgreSQL表单
        self.pg_host_edit.setText("localhost")
        self.pg_port_edit.setText("5432")
        self.pg_username_edit.clear()
        self.pg_password_edit.clear()
        self.pg_database_edit.clear()
        
        # 清空Oracle表单
        self.oracle_host_edit.setText("localhost")
        self.oracle_port_edit.setText("1521")
        self.oracle_username_edit.clear()
        self.oracle_password_edit.clear()
        self.oracle_service_edit.clear()
        
        # 清空SQL Server表单
        self.sqlserver_host_edit.setText("localhost")
        self.sqlserver_port_edit.setText("1433")
        self.sqlserver_username_edit.clear()
        self.sqlserver_password_edit.clear()
        self.sqlserver_database_edit.clear()
        self.sqlserver_driver_edit.setText("ODBC Driver 17 for SQL Server")
        
        # 清空SQLite表单
        self.sqlite_file_edit.clear()

        # 清空MongoDB表单
        self.mongodb_host_edit.setText("localhost")
        self.mongodb_port_edit.setText("27017")
        self.mongodb_username_edit.clear()
        self.mongodb_password_edit.clear()
        self.mongodb_database_edit.clear()
        self.mongodb_auth_source_edit.setText("admin")

        # 清空Db2表单
        self.db2_host_edit.setText("localhost")
        self.db2_port_edit.setText("50000")
        self.db2_username_edit.clear()
        self.db2_password_edit.clear()
        self.db2_database_edit.clear()
        
        # 设置默认类型为MySQL
        self.type_combo.setCurrentText("MySQL")
        
        # 清空选择
        self.connection_tree.clearSelection()
        self.selected_connection = None
        
        # 确保表单处于新建模式
        self.name_edit.setFocus()
        
    def save_connection(self):
        """保存连接"""
        name = self.name_edit.text().strip()
        db_type = self.type_combo.currentData()
        
        if not name:
            QMessageBox.warning(self, tr("warning"), tr("connection_name_required"))
            return
        
        # 根据数据库类型获取配置
        if db_type == "mysql":
            host = self.host_edit.text().strip()
            port = int(self.port_edit.text().strip() or "3306")
            username = self.username_edit.text().strip()
            password = self.password_edit.text()
            database = self.database_edit.text().strip()
            
            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return
                
            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return
                
            # 构建MySQL配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database
            }
            
        elif db_type == "postgresql":
            host = self.pg_host_edit.text().strip()
            port = int(self.pg_port_edit.text().strip() or "5432")
            username = self.pg_username_edit.text().strip()
            password = self.pg_password_edit.text()
            database = self.pg_database_edit.text().strip()
            
            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return
                
            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return
                
            # 构建PostgreSQL配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database
            }
            
        elif db_type == "oracle":
            host = self.oracle_host_edit.text().strip()
            port = int(self.oracle_port_edit.text().strip() or "1521")
            username = self.oracle_username_edit.text().strip()
            password = self.oracle_password_edit.text()
            service_name = self.oracle_service_edit.text().strip()
            
            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return
                
            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return
                
            if not service_name:
                QMessageBox.warning(self, tr("warning"), tr("service_name_required"))
                return
                
            # 构建Oracle配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'service_name': service_name
            }
            
        elif db_type == "sqlserver":
            host = self.sqlserver_host_edit.text().strip()
            port = int(self.sqlserver_port_edit.text().strip() or "1433")
            username = self.sqlserver_username_edit.text().strip()
            password = self.sqlserver_password_edit.text()
            database = self.sqlserver_database_edit.text().strip()
            driver = self.sqlserver_driver_edit.text().strip()
            
            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return
                
            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return
                
            if not database:
                QMessageBox.warning(self, tr("warning"), tr("database_required"))
                return
                
            # 构建SQL Server配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database,
                'driver': driver
            }
            
        elif db_type == "sqlite":
            file_path = self.sqlite_file_edit.text().strip()
            
            if not file_path:
                QMessageBox.warning(self, tr("warning"), tr("database_file_path_required"))
                return
                
            # 构建SQLite配置
            config = {
                'file': file_path
            }

        elif db_type == "mongodb":
            host = self.mongodb_host_edit.text().strip()
            port = int(self.mongodb_port_edit.text().strip() or "27017")
            username = self.mongodb_username_edit.text().strip()
            password = self.mongodb_password_edit.text()
            database = self.mongodb_database_edit.text().strip()
            auth_source = self.mongodb_auth_source_edit.text().strip()

            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return

            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return

            if not database:
                QMessageBox.warning(self, tr("warning"), tr("database_required"))
                return

            # 构建MongoDB配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database,
                'auth_source': auth_source
            }

        elif db_type == "db2":
            host = self.db2_host_edit.text().strip()
            port = int(self.db2_port_edit.text().strip() or "50000")
            username = self.db2_username_edit.text().strip()
            password = self.db2_password_edit.text()
            database = self.db2_database_edit.text().strip()

            if not host:
                QMessageBox.warning(self, tr("warning"), tr("host_required"))
                return

            if not username:
                QMessageBox.warning(self, tr("warning"), tr("username_required"))
                return

            if not database:
                QMessageBox.warning(self, tr("warning"), tr("database_required"))
                return

            # 构建Db2配置
            config = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database
            }
        
        try:
            # 调试信息
            print(f"保存连接 - selected_connection: {self.selected_connection}")
            if self.selected_connection:
                print(f"更新连接: {self.selected_connection.name} (ID: {self.selected_connection.id})")
            else:
                print("创建新连接")
                
            # 创建或更新连接
            if self.selected_connection:
                # 更新现有连接
                connection = Connection(
                    id=self.selected_connection.id,
                    name=name,
                    type=db_type,
                    config=config,
                    created_at=self.selected_connection.created_at,
                    updated_at=datetime.now()
                )
                self.connection_manager.update_connection(connection)
            else:
                # 创建新连接
                connection = Connection(
                    id=None,
                    name=name,
                    type=db_type,
                    config=config,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                new_id = self.connection_manager.add_connection(connection)
                
            # 重新加载连接列表
            self.load_connections()
            
            # 显示成功提示
            if self.selected_connection:
                QMessageBox.information(self, tr("info"), tr("connection_update_success"))
            else:
                QMessageBox.information(self, tr("info"), tr("connection_create_success"))
            
            # 如果是新建连接，清空表单
            if not self.selected_connection:
                self.add_connection()
                
        except Exception as e:
            QMessageBox.critical(self, tr("error"), f"保存连接失败: {str(e)}")
        
    def delete_connection(self):
        """删除连接"""
        current_item = self.connection_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, tr("warning"), tr("please_fill_required_fields"))
            return
            
        conn_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        if not conn_id:
            return
            
        # 确认删除
        reply = QMessageBox.question(
            self, 
            tr("confirm"), 
            tr("confirm_delete_connection"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.connection_manager.delete_connection(conn_id)
            self.load_connections()
            self.add_connection()  # 清空表单
            
    def test_connection(self):
        """测试连接"""
        db_type = self.type_combo.currentData()
        
        try:
            if db_type == "mysql":
                config = {
                    "host": self.host_edit.text().strip(),
                    "port": int(self.port_edit.text().strip() or "3306"),
                    "user": self.username_edit.text().strip(),
                    "password": self.password_edit.text(),
                    "database": self.database_edit.text().strip()
                }
                
                # 尝试建立MySQL连接
                import mysql.connector
                conn = mysql.connector.connect(**config)
                conn.close()
                
            elif db_type == "postgresql":
                config = {
                    "host": self.pg_host_edit.text().strip(),
                    "port": int(self.pg_port_edit.text().strip() or "5432"),
                    "user": self.pg_username_edit.text().strip(),
                    "password": self.pg_password_edit.text(),
                    "database": self.pg_database_edit.text().strip()
                }
                
                # 尝试建立PostgreSQL连接
                try:
                    import psycopg2
                    conn = psycopg2.connect(**config)
                    conn.close()
                except ImportError:
                    QMessageBox.warning(self, tr("warning"), tr("postgresql_driver_not_installed"))
                    return
                    
            elif db_type == "oracle":
                config = {
                    "host": self.oracle_host_edit.text().strip(),
                    "port": int(self.oracle_port_edit.text().strip() or "1521"),
                    "user": self.oracle_username_edit.text().strip(),
                    "password": self.oracle_password_edit.text(),
                    "service_name": self.oracle_service_edit.text().strip()
                }
                
                # 尝试建立Oracle连接
                try:
                    import cx_Oracle
                    dsn = cx_Oracle.makedsn(config["host"], config["port"], service_name=config["service_name"])
                    conn = cx_Oracle.connect(user=config["user"], password=config["password"], dsn=dsn)
                    conn.close()
                except ImportError:
                    QMessageBox.warning(self, tr("warning"), tr("oracle_driver_not_installed"))
                    return
                    
            elif db_type == "sqlserver":
                config = {
                    "host": self.sqlserver_host_edit.text().strip(),
                    "port": int(self.sqlserver_port_edit.text().strip() or "1433"),
                    "user": self.sqlserver_username_edit.text().strip(),
                    "password": self.sqlserver_password_edit.text(),
                    "database": self.sqlserver_database_edit.text().strip(),
                    "driver": self.sqlserver_driver_edit.text().strip()
                }
                
                # 尝试建立SQL Server连接
                try:
                    import pyodbc
                    conn_str = f"DRIVER={{{config['driver']}}};SERVER={config['host']};PORT={config['port']};DATABASE={config['database']};UID={config['user']};PWD={config['password']}"
                    conn = pyodbc.connect(conn_str)
                    conn.close()
                except ImportError:
                    QMessageBox.warning(self, tr("warning"), tr("sqlserver_driver_not_installed"))
                    return
                    
            elif db_type == "sqlite":
                file_path = self.sqlite_file_edit.text().strip()
                
                if not file_path:
                    QMessageBox.warning(self, tr("warning"), tr("database_file_path_required"))
                    return
                
                # 尝试建立SQLite连接
                try:
                    import sqlite3
                    conn = sqlite3.connect(file_path)
                    conn.close()
                except ImportError:
                    # SQLite是Python内置模块，不应该出现ImportError
                    QMessageBox.warning(self, tr("warning"), tr("sqlite_connection_error"))
                    return

            elif db_type == "mongodb":
                config = {
                    "host": self.mongodb_host_edit.text().strip(),
                    "port": int(self.mongodb_port_edit.text().strip() or "27017"),
                    "user": self.mongodb_username_edit.text().strip(),
                    "password": self.mongodb_password_edit.text(),
                    "database": self.mongodb_database_edit.text().strip(),
                    "auth_source": self.mongodb_auth_source_edit.text().strip()
                }
                try:
                    import pymongo
                    client = pymongo.MongoClient(host=config["host"], port=config["port"])
                    if config["user"] and config["password"]:
                        client.admin.authenticate(config["user"], config["password"])
                    db = client[config["database"]]
                    if config["auth_source"] and config["auth_source"] != "admin":
                        db = client[config["database"]][config["auth_source"]]
                    db.command("ping")
                    client.close()
                except ImportError:
                    QMessageBox.warning(self, tr("warning"), tr("mongodb_driver_not_installed"))
                    return
                except Exception as e:
                    QMessageBox.warning(self, tr("warning"), tr("mongodb_connection_failed").format(error=str(e)))
                    return

            elif db_type == "db2":
                config = {
                    "host": self.db2_host_edit.text().strip(),
                    "port": int(self.db2_port_edit.text().strip() or "50000"),
                    "user": self.db2_username_edit.text().strip(),
                    "password": self.db2_password_edit.text(),
                    "database": self.db2_database_edit.text().strip()
                }
                try:
                    import ibm_db
                    conn_str = f"DATABASE={config['database']};HOSTNAME={config['host']};PORT={config['port']};PROTOCOL=TCPIP;UID={config['user']};PWD={config['password']}"
                    conn = ibm_db.connect(conn_str, "", "")
                    ibm_db.close(conn)
                except ImportError:
                    QMessageBox.warning(self, tr("warning"), tr("db2_driver_not_installed"))
                    return
                except Exception as e:
                    QMessageBox.warning(self, tr("warning"), tr("db2_connection_failed").format(error=str(e)))
                    return
            
            QMessageBox.information(self, tr("info"), tr("connection_test_success"))
        except Exception as e:
            QMessageBox.critical(self, tr("error"), f"{tr('connection_test_failed')}：{str(e)}")


class SelectConnectionDialog(QDialog):
    """选择连接对话框"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.selected_connection = None
        
        self.setWindowTitle("选择连接")
        self.setGeometry(200, 200, 700, 500)
        self.setModal(True)
        self.center_on_screen()
        
        # 应用Windows 11风格样式
        self.apply_windows11_style()
        
        self.setup_ui()
        self.load_connections()
    
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
        /* 对话框样式 */
        QDialog {
            background-color: #fafafa;
            color: #202020;
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
        
        /* 树形控件样式 */
        QTreeWidget {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
            color: #202020;
            gridline-color: #f0f0f0;
        }
        
        QTreeWidget::item {
            padding: 6px;
            border: none;
        }
        
        QTreeWidget::item:selected {
            background: #e6f3ff;
            color: #202020;
        }
        
        QTreeWidget::item:hover {
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
        
        /* 标签样式 */
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
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
        """
        
        self.setStyleSheet(style_sheet)
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(tr("select_sql_file"))  # 使用现有的翻译键
        layout.addWidget(title_label)
        
        # 连接列表
        self.connection_tree = QTreeWidget()
        self.connection_tree.setHeaderLabels([tr("connection_name"), tr("connection_type"), tr("host"), tr("database")])
        self.connection_tree.setColumnWidth(0, 200)
        self.connection_tree.setColumnWidth(1, 100)
        self.connection_tree.setColumnWidth(2, 150)
        self.connection_tree.setColumnWidth(3, 120)
        self.connection_tree.setStyleSheet("QTreeWidget::item { padding: 8px; }")
        self.connection_tree.itemDoubleClicked.connect(self.on_connection_double_clicked)
        layout.addWidget(self.connection_tree)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        select_btn = QPushButton(tr("confirm"))
        select_btn.setObjectName("primary")
        select_btn.clicked.connect(self.accept)
        btn_layout.addWidget(select_btn)
        
        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
    def load_connections(self):
        """加载连接列表"""
        self.connection_tree.clear()
        
        connections = self.connection_manager.get_all_connections()
        for conn in connections:
            item = QTreeWidgetItem(self.connection_tree)
            item.setText(0, conn.name)
            item.setText(1, conn.type)
            
            if conn.type == "mysql":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "postgresql":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "oracle":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('service_name', ''))
            elif conn.type == "sqlserver":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "sqlite":
                config = conn.config
                item.setText(2, tr("local_file"))
                item.setText(3, config.get('file', ''))
            elif conn.type == "mongodb":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            elif conn.type == "db2":
                config = conn.config
                host_info = f"{config.get('host', '')}:{config.get('port', '')}"
                item.setText(2, host_info)
                item.setText(3, config.get('database', ''))
            else:
                item.setText(2, conn.config.get('url', ''))
                item.setText(3, '')
            
            item.setData(0, Qt.ItemDataRole.UserRole, conn.id)
            
    def on_connection_double_clicked(self, item):
        """连接双击事件"""
        conn_id = item.data(0, Qt.ItemDataRole.UserRole)
        if conn_id:
            self.selected_connection = self.connection_manager.get_connection(conn_id)
            self.accept()
            
    def accept(self):
        """确认选择"""
        current_item = self.connection_tree.currentItem()
        if current_item:
            conn_id = current_item.data(0, Qt.ItemDataRole.UserRole)
            if conn_id:
                self.selected_connection = self.connection_manager.get_connection(conn_id)
                
        super().accept() 