"""
连接管理对话框 - PyQt6版本
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTreeWidget, QTreeWidgetItem, QGroupBox,
    QGridLayout, QMessageBox, QComboBox, QCheckBox,
    QWidget, QTextEdit, QSplitter, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from data.models import Connection, ConnectionManager
from datetime import datetime


class ConnectionDialog(QDialog):
    """连接管理对话框"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.selected_connection = None
        
        self.setWindowTitle("连接管理")
        self.setGeometry(200, 200, 900, 350)
        self.setModal(True)
        
        self.setup_ui()
        self.load_connections()
        
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
        self.connection_tree.setStyleSheet("QTreeWidget::item { padding: 2px; }")
        self.connection_tree.itemClicked.connect(self.on_connection_selected)
        list_layout.addWidget(self.connection_tree)
        
        # 列表操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        add_btn = QPushButton("新建")
        add_btn.clicked.connect(self.add_connection)
        btn_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("删除")
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
        basic_layout.addWidget(QLabel("连接名称:"), 0, 0)
        self.name_edit = QLineEdit()
        basic_layout.addWidget(self.name_edit, 0, 1)
        
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
        mysql_layout.addWidget(QLabel("主机地址:"), 0, 0)
        self.host_edit = QLineEdit()
        self.host_edit.setText("localhost")
        self.host_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.host_edit, 0, 1)
        
        # 端口
        mysql_layout.addWidget(QLabel("端口:"), 1, 0)
        self.port_edit = QLineEdit()
        self.port_edit.setText("3306")
        self.port_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.port_edit, 1, 1)
        
        # 用户名
        mysql_layout.addWidget(QLabel("用户名:"), 2, 0)
        self.username_edit = QLineEdit()
        self.username_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.username_edit, 2, 1)
        
        # 密码
        mysql_layout.addWidget(QLabel("密码:"), 3, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.password_edit, 3, 1)
        
        # 数据库名
        mysql_layout.addWidget(QLabel("数据库名:"), 4, 0)
        self.database_edit = QLineEdit()
        self.database_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mysql_layout.addWidget(self.database_edit, 4, 1)
        
        # 设置列拉伸
        # mysql_layout.setColumnStretch(1, 1)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        test_btn = QPushButton("测试连接")
        test_btn.clicked.connect(self.test_connection)
        btn_layout.addWidget(test_btn)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_connection)
        btn_layout.addWidget(save_btn)
        
        details_layout.addLayout(btn_layout)
        
        # 添加弹性空间，让元素靠上排列
        details_layout.addStretch()
        

        
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
                
    def load_connection_details(self, connection):
        """加载连接详情"""
        if connection.type == "mysql":
            config = connection.config
            
            self.name_edit.setText(connection.name)
            self.host_edit.setText(config.get('host', ''))
            self.port_edit.setText(str(config.get('port', '')))
            self.username_edit.setText(config.get('username', ''))
            self.password_edit.setText(config.get('password', ''))
            self.database_edit.setText(config.get('database', ''))
            
    def add_connection(self):
        """添加连接"""
        # 清空表单
        self.name_edit.clear()
        self.host_edit.setText("localhost")
        self.port_edit.setText("3306")
        self.username_edit.clear()
        self.password_edit.clear()
        self.database_edit.clear()
        
        # 清空选择
        self.connection_tree.clearSelection()
        self.selected_connection = None
        
    def save_connection(self):
        """保存连接"""
        name = self.name_edit.text().strip()
        host = self.host_edit.text().strip()
        port = int(self.port_edit.text().strip() or "3306")
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        database = self.database_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "警告", "请输入连接名称")
            return
            
        if not host:
            QMessageBox.warning(self, "警告", "请输入主机地址")
            return
            
        if not username:
            QMessageBox.warning(self, "警告", "请输入用户名")
            return
            
        # 构建配置
        config = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'database': database
        }
        
        # 创建或更新连接
        if self.selected_connection:
            # 更新现有连接
            connection = Connection(
                id=self.selected_connection.id,
                name=name,
                type="mysql",
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
                type="mysql",
                config=config,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.connection_manager.add_connection(connection)
            
        # 重新加载连接列表
        self.load_connections()
        
    def delete_connection(self):
        """删除连接"""
        current_item = self.connection_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要删除的连接")
            return
            
        conn_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        if not conn_id:
            return
            
        # 确认删除
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            "确定要删除这个连接吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.connection_manager.delete_connection(conn_id)
            self.load_connections()
            self.add_connection()  # 清空表单
            
    def test_connection(self):
        """测试连接"""
        try:
            config = {
                "host": self.host_edit.text().strip(),
                "port": int(self.port_edit.text().strip() or "3306"),
                "user": self.username_edit.text().strip(),
                "password": self.password_edit.text(),
                "database": self.database_edit.text().strip()
            }
            
            # 尝试建立连接
            import mysql.connector
            conn = mysql.connector.connect(**config)
            conn.close()
            
            QMessageBox.information(self, "成功", "MySQL数据库连接测试成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"MySQL数据库连接测试失败：{str(e)}")


class SelectConnectionDialog(QDialog):
    """选择连接对话框"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.selected_connection = None
        
        self.setWindowTitle("选择连接")
        self.setGeometry(200, 200, 700, 500)
        self.setModal(True)
        
        self.setup_ui()
        self.load_connections()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("请选择数据库连接")
        layout.addWidget(title_label)
        
        # 连接列表
        self.connection_tree = QTreeWidget()
        self.connection_tree.setHeaderLabels(["名称", "类型", "主机", "数据库名"])
        self.connection_tree.setColumnWidth(0, 200)
        self.connection_tree.setColumnWidth(1, 100)
        self.connection_tree.setColumnWidth(2, 150)
        self.connection_tree.setColumnWidth(3, 120)
        self.connection_tree.setStyleSheet("QTreeWidget::item { padding: 2px; }")
        self.connection_tree.itemDoubleClicked.connect(self.on_connection_double_clicked)
        layout.addWidget(self.connection_tree)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        select_btn = QPushButton("选择")
        select_btn.clicked.connect(self.accept)
        btn_layout.addWidget(select_btn)
        
        cancel_btn = QPushButton("取消")
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