"""
MySQL表结构比较工具 - PyQt6版本
主应用程序
"""

import sys
import threading
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
    QCheckBox, QFrame, QGroupBox, QSplitter, QMessageBox,
    QFileDialog, QTextEdit, QDialog, QRadioButton, QButtonGroup,
    QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QClipboard

from core.sql_parser import SQLParser
from core.sql_generator import SQLGenerator
from core.db_connector import DBConnector
from data.models import ConnectionManager, Connection, History
from ui.connection_dialog import ConnectionDialog, SelectConnectionDialog

class SQLCompareApp(QMainWindow):
    """MySQL表结构比较工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MySQL表结构比较工具")
        self.showMaximized()
        
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
        
        # 创建界面
        self.create_ui()
        
        # 初始化历史记录
        self.connection_manager.update_history_display_format()
        self.update_history_lists()
        

    def create_ui(self):
        """创建用户界面"""
        # 创建中央部件
        central_widget = QWidget()
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
        # 设置工具栏的最大高度，减少高度
        toolbar_frame.setMaximumHeight(50)
        toolbar_frame.setMinimumHeight(40)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setSpacing(15)
        # 减少上下边距
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # 左侧按钮组
        left_btn_layout = QHBoxLayout()
        left_btn_layout.setSpacing(10)
        
        # 连接管理按钮
        self.conn_btn = QPushButton("连接管理")
        self.conn_btn.clicked.connect(self.show_connection_dialog)
        self.conn_btn.setFixedHeight(30)  # 设置按钮高度
        left_btn_layout.addWidget(self.conn_btn)
        
        # 开始比较按钮
        self.compare_btn = QPushButton("开始比较")
        self.compare_btn.clicked.connect(self.start_compare)
        self.compare_btn.setFixedHeight(30)  # 设置按钮高度
        left_btn_layout.addWidget(self.compare_btn)
        
        # 生成同步SQL按钮
        self.generate_btn = QPushButton("生成同步SQL")
        self.generate_btn.clicked.connect(self.generate_sync_sql)
        self.generate_btn.setFixedHeight(30)  # 设置按钮高度
        left_btn_layout.addWidget(self.generate_btn)
        
        toolbar_layout.addLayout(left_btn_layout)
        toolbar_layout.addStretch()
        
        # 右侧选项组
        right_option_layout = QHBoxLayout()
        right_option_layout.setSpacing(15)
        
        # 同步滚动复选框
        self.sync_scroll_check = QCheckBox("同步滚动")
        self.sync_scroll_check.setChecked(self.sync_scroll)
        self.sync_scroll_check.toggled.connect(self.toggle_sync_scroll)
        self.sync_scroll_check.setFixedHeight(30)  # 设置复选框高度
        right_option_layout.addWidget(self.sync_scroll_check)
        
        # 隐藏相同行复选框
        self.hide_same_check = QCheckBox("隐藏相同行")
        self.hide_same_check.setChecked(self.hide_same)
        self.hide_same_check.toggled.connect(self.toggle_hide_same)
        self.hide_same_check.setFixedHeight(30)  # 设置复选框高度
        right_option_layout.addWidget(self.hide_same_check)
        
        # 仅显示缺失复选框
        self.show_missing_check = QCheckBox("仅显示缺失")
        self.show_missing_check.setChecked(self.show_missing_only)
        self.show_missing_check.toggled.connect(self.toggle_show_missing)
        self.show_missing_check.setFixedHeight(30)  # 设置复选框高度
        right_option_layout.addWidget(self.show_missing_check)
        
        # 忽略大小写复选框
        self.ignore_case_check = QCheckBox("忽略大小写")
        self.ignore_case_check.setChecked(self.ignore_case)
        self.ignore_case_check.toggled.connect(self.toggle_ignore_case)
        self.ignore_case_check.setFixedHeight(30)  # 设置复选框高度
        right_option_layout.addWidget(self.ignore_case_check)
        
        toolbar_layout.addLayout(right_option_layout)
        parent_layout.addWidget(toolbar_frame, 0)  # 设置拉伸因子为0，工具栏不拉伸
        
    def create_left_panel(self, parent):
        """创建左侧面板"""
        left_group = QGroupBox("左侧数据源")
        parent.addWidget(left_group)
        
        left_layout = QVBoxLayout(left_group)
        left_layout.setSpacing(15)
        
        # 选择框架
        select_frame = QFrame()
        select_layout = QHBoxLayout(select_frame)
        select_layout.setSpacing(10)
        
        # 连接按钮 - 固定大小
        self.left_conn_btn = QPushButton("连接")
        self.left_conn_btn.clicked.connect(lambda: self.show_connection_dialog("left"))
        self.left_conn_btn.setFixedWidth(60)
        select_layout.addWidget(self.left_conn_btn)
        
        # 文件按钮 - 固定大小
        self.left_file_btn = QPushButton("文件")
        self.left_file_btn.clicked.connect(lambda: self.select_file("left"))
        self.left_file_btn.setFixedWidth(60)
        select_layout.addWidget(self.left_file_btn)
        
        # 历史记录标签 - 固定大小
        history_label = QLabel("历史记录:")
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
        self.left_tree.setHorizontalHeaderLabels(["序号", "字段名", "字段定义"])
        self.left_tree.setColumnWidth(0, 60)
        self.left_tree.setColumnWidth(1, 200)
        self.left_tree.setColumnWidth(2, 500)
        self.left_tree.setAlternatingRowColors(True)
        self.left_tree.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        left_layout.addWidget(self.left_tree)
        
    def create_right_panel(self, parent):
        """创建右侧面板"""
        right_group = QGroupBox("右侧数据源")
        parent.addWidget(right_group)
        
        right_layout = QVBoxLayout(right_group)
        right_layout.setSpacing(15)
        
        # 选择框架
        select_frame = QFrame()
        select_layout = QHBoxLayout(select_frame)
        select_layout.setSpacing(10)
        
        # 连接按钮 - 固定大小
        self.right_conn_btn = QPushButton("连接")
        self.right_conn_btn.clicked.connect(lambda: self.show_connection_dialog("right"))
        self.right_conn_btn.setFixedWidth(60)
        select_layout.addWidget(self.right_conn_btn)
        
        # 文件按钮 - 固定大小
        self.right_file_btn = QPushButton("文件")
        self.right_file_btn.clicked.connect(lambda: self.select_file("right"))
        self.right_file_btn.setFixedWidth(60)
        select_layout.addWidget(self.right_file_btn)
        
        # 历史记录标签 - 固定大小
        history_label = QLabel("历史记录:")
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
        self.right_tree.setHorizontalHeaderLabels(["序号", "字段名", "字段定义"])
        self.right_tree.setColumnWidth(0, 60)
        self.right_tree.setColumnWidth(1, 200)
        self.right_tree.setColumnWidth(2, 500)
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
            "选择SQL文件",
            "",
            "SQL files (*.sql);;All files (*.*)"
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
                QMessageBox.critical(self, "错误", f"加载文件失败: {str(e)}")
            
    def start_compare(self):
        """开始比较"""
        # 获取左右两侧的历史记录选择
        left_display = self.left_history_combo.currentText()
        right_display = self.right_history_combo.currentText()
        
        if not left_display or not right_display:
            QMessageBox.warning(self, "警告", "请先选择两个数据源")
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
            left_data.append([f"表{table_index}", f"表名: {table_name}", f"字段数: {left_count}"])
            right_data.append([f"表{table_index}", f"表名: {table_name}", f"字段数: {right_count}"])
            
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
                
                left_row = [str(col_index), col_name, left_def_display or "[缺失]"]
                right_row = [str(col_index), col_name, right_def_display or "[缺失]"]
                
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
                if row_data[1].startswith("表名:"):
                    item.setBackground(QColor(240, 240, 240))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                # 设置标题行的样式
                elif row_data[1] in ["字段", "索引"]:
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
                
                if left_def == "[缺失]" or right_def == "[缺失]":
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
            QMessageBox.warning(self, "警告", "请先加载左侧和右侧的表结构数据")
            return
        elif not self.left_tables:
            QMessageBox.warning(self, "警告", "请先加载左侧表结构数据")
            return
        elif not self.right_tables:
            QMessageBox.warning(self, "警告", "请先加载右侧表结构数据")
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
                    title = f"同步SQL - 将 {left_name} 同步到 {right_name}"
                else:
                    # 以左侧为目标库，将右侧结构同步到左侧
                    sync_sql = self.sql_generator.generate_sync_sql(self.right_tables, self.left_tables)
                    title = f"同步SQL - 将 {right_name} 同步到 {left_name}"
                
                # 显示SQL窗口
                self.show_sql_window(title, sync_sql)
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"生成同步SQL时出错:\n{str(e)}")
                
    def show_sql_window(self, title, sql_content):
        """显示SQL窗口"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setGeometry(200, 200, 900, 700)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 提示信息
        info_label = QLabel("生成的同步SQL语句如下，请仔细检查后执行：")
        info_label.setStyleSheet("color: #666; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # SQL文本区域
        text_edit = QTextEdit()
        text_edit.setPlainText(sql_content)
        text_edit.setFont(QFont("Consolas", 10))
        text_edit.setStyleSheet("background-color: #f8f9fa; border: 1px solid #ddd;")
        layout.addWidget(text_edit)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        # 复制按钮
        copy_btn = QPushButton("复制SQL")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(sql_content))
        btn_layout.addWidget(copy_btn)
        
        btn_layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
        
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "提示", "SQL已复制到剪贴板")
        
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
                            QMessageBox.critical(self, "错误", f"获取表结构失败: {str(e)}")
                    elif conn.type == "agent":
                        QMessageBox.information(self, "提示", "暂不支持Agent类型的连接")
                    
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
            QMessageBox.information(self, "提示", "暂不支持Agent类型的连接")
        
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
            table_data.append([f"表{table_index}", f"表名: {table_name}", f"字段数: {column_count} 索引数: {index_count}"])
            
            # 添加字段信息
            if columns:
                # 添加字段标题行
                table_data.append(["", "字段", ""])
                
                # 添加字段行
                for col_index, (col_name, col_def) in enumerate(sorted(columns.items()), 1):
                    col_def_display = col_def.get('raw', '') if isinstance(col_def, dict) else col_def
                    table_data.append([str(col_index), col_name, col_def_display])
            
            # 添加索引信息
            if indexes:
                # 添加索引标题行
                table_data.append(["", "索引", ""])
                
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
        self.left_name = "左侧数据库"
        self.right_name = "右侧数据库"
        
        self.setWindowTitle("选择目标库")
        self.setModal(True)
        self.setGeometry(300, 300, 500, 300)
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("请选择目标数据库")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel("选择要将哪个数据库作为目标，另一个数据库的结构将同步到目标数据库中")
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
        option_group = QGroupBox("同步方向")
        option_layout = QVBoxLayout(option_group)
        option_layout.setSpacing(15)
        
        # 单选按钮组
        self.button_group = QButtonGroup()
        
        # 第一个选项
        self.right_radio = QRadioButton(f"以 {self.right_name} 为目标库（将左侧结构同步到右侧）")
        self.right_radio.setChecked(True)
        self.button_group.addButton(self.right_radio, 1)
        option_layout.addWidget(self.right_radio)
        
        # 第二个选项
        self.left_radio = QRadioButton(f"以 {self.left_name} 为目标库（将右侧结构同步到左侧）")
        self.button_group.addButton(self.left_radio, 2)
        option_layout.addWidget(self.left_radio)
        
        layout.addWidget(option_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("取消")
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
    app.setApplicationName("MySQL表结构比较工具")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("DBCompare")
    
    # 创建主窗口
    window = SQLCompareApp()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 