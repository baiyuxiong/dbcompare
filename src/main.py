import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from .core.sql_parser import SQLParser
from .core.sql_generator import SQLGenerator
from .ui.connection_dialog import ConnectionDialog, SelectConnectionDialog
from .ui.styles import StyleManager
from .data.models import ConnectionManager, Connection, History
from datetime import datetime
from .core.db_connector import DBConnector

class SQLCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MySQL表结构比较工具")
        self.root.geometry("1200x800")
        
        # 配置主题和样式
        self.colors, self.fonts = StyleManager.setup_styles()
        
        # 初始化变量
        self.sync_scroll = tk.BooleanVar(value=True)
        self.hide_same = tk.BooleanVar(value=False)
        self.show_missing_only = tk.BooleanVar(value=False)
        self.left_tables = {}
        self.right_tables = {}
        
        # 初始化组件
        self.sql_parser = SQLParser()
        self.sql_generator = SQLGenerator()
        self.db_connector = DBConnector()
        self.connection_manager = ConnectionManager()
        
        # 创建界面
        self.create_menu()
        self.connection_manager.update_history_display_format()
        self.create_main_content()
        self.toggle_sync_scroll()
    
        # 设置根窗口背景色
        self.root.configure(bg=self.colors['light'])
        
    def create_menu(self):
        """创建菜单栏"""
        # 创建主菜单框架，使用卡片样式
        menu_frame = ttk.Frame(self.root, style='Card.TFrame')
        menu_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 创建工具栏容器
        toolbar_frame = ttk.Frame(menu_frame)
        toolbar_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # 左侧按钮组
        left_btn_frame = ttk.Frame(toolbar_frame)
        left_btn_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # 添加连接管理按钮
        conn_btn = ttk.Button(left_btn_frame, 
                             text="连接管理", 
                             style='Primary.TButton',
                             command=self._show_connection_dialog)
        conn_btn.pack(side=tk.LEFT, padx=5)
        
        compare_btn = ttk.Button(left_btn_frame, 
                                text="开始比较", 
                                style='Success.TButton',
                                command=self.start_compare)
        compare_btn.pack(side=tk.LEFT, padx=5)
        
        generate_btn = ttk.Button(left_btn_frame, 
                                 text="生成同步SQL", 
                                 style='Warning.TButton',
                                 command=self.generate_sync_sql)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧选项组
        right_option_frame = ttk.Frame(toolbar_frame)
        right_option_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加同步滚动开关
        sync_check = ttk.Checkbutton(
            right_option_frame, 
            text="同步滚动", 
            variable=self.sync_scroll,
            command=self.toggle_sync_scroll
        )
        sync_check.pack(side=tk.LEFT, padx=10)
        
        # 添加隐藏相同行开关
        hide_same_check = ttk.Checkbutton(
            right_option_frame,
            text="隐藏相同行",
            variable=self.hide_same,
            command=self.show_differences
        )
        hide_same_check.pack(side=tk.LEFT, padx=10)
        
        # 添加仅显示缺失开关
        show_missing_check = ttk.Checkbutton(
            right_option_frame,
            text="仅显示缺失",
            variable=self.show_missing_only,
            command=self.show_differences
        )
        show_missing_check.pack(side=tk.LEFT, padx=10)
        
    def create_main_content(self):
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧面板
        left_frame = ttk.LabelFrame(content_frame, text="左侧数据源", style='Title.TLabelframe')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 左侧选择框架
        left_select_frame = ttk.Frame(left_frame)
        left_select_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # 左侧工具栏
        left_toolbar = ttk.Frame(left_select_frame)
        left_toolbar.pack(side=tk.LEFT, fill=tk.X)
        
        # 左侧连接按钮
        self.left_conn_btn = ttk.Button(left_toolbar, text="连接", 
                                      style='Primary.TButton',
                                      command=lambda: self._show_connection_dialog("left"))
        self.left_conn_btn.pack(side=tk.LEFT, padx=5)
        
        # 左侧文件按钮
        self.left_file_btn = ttk.Button(left_toolbar, text="文件", 
                                      style='Success.TButton',
                                      command=lambda: self.select_file("left"))
        self.left_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 左侧历史记录下拉框
        history_label = ttk.Label(left_select_frame, text="历史记录:", font=self.fonts['small'])
        history_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.left_history_combo = ttk.Combobox(left_select_frame, state="readonly", width=45)
        self.left_history_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.left_history_combo.bind("<<ComboboxSelected>>", lambda e: self._on_history_select("left"))
        
        # 右侧面板
        right_frame = ttk.LabelFrame(content_frame, text="右侧数据源", style='Title.TLabelframe')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 右侧选择框架
        right_select_frame = ttk.Frame(right_frame)
        right_select_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # 右侧工具栏
        right_toolbar = ttk.Frame(right_select_frame)
        right_toolbar.pack(side=tk.LEFT, fill=tk.X)
        
        # 右侧连接按钮
        self.right_conn_btn = ttk.Button(right_toolbar, text="连接", 
                                       style='Primary.TButton',
                                       command=lambda: self._show_connection_dialog("right"))
        self.right_conn_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧文件按钮
        self.right_file_btn = ttk.Button(right_toolbar, text="文件", 
                                       style='Success.TButton',
                                       command=lambda: self.select_file("right"))
        self.right_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧历史记录下拉框
        history_label = ttk.Label(right_select_frame, text="历史记录:", font=self.fonts['small'])
        history_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.right_history_combo = ttk.Combobox(right_select_frame, state="readonly", width=45)
        self.right_history_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.right_history_combo.bind("<<ComboboxSelected>>", lambda e: self._on_history_select("right"))
        
        # 初始化历史记录列表
        self._update_history_lists()
        
        # 创建左侧表格
        self.left_tree = ttk.Treeview(left_frame, columns=("index", "field", "definition"), show="headings")
        self.left_tree.heading("index", text="序号")
        self.left_tree.heading("field", text="字段名")
        self.left_tree.heading("definition", text="字段定义")
        self.left_tree.column("index", width=60)
        self.left_tree.column("field", width=180)
        self.left_tree.column("definition", width=400)
        self.left_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建右侧表格
        self.right_tree = ttk.Treeview(right_frame, columns=("index", "field", "definition"), show="headings")
        self.right_tree.heading("index", text="序号")
        self.right_tree.heading("field", text="字段名")
        self.right_tree.heading("definition", text="字段定义")
        self.right_tree.column("index", width=60)
        self.right_tree.column("field", width=180)
        self.right_tree.column("definition", width=400)
        self.right_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 配置标签样式
        for tree in (self.left_tree, self.right_tree):
            StyleManager.configure_tree_tags(tree, self.colors)
            
        # 同步选择功能
        def on_tree_click(event, source_tree, target_tree):
            def sync_selection():
                # 获取当前选中的项
                selected_items = source_tree.selection()
                if not selected_items:
                    return
                    
                # 获取所有项
                source_items = source_tree.get_children()
                target_items = target_tree.get_children()
                
                # 获取选中项在列表中的索引
                try:
                    index = source_items.index(selected_items[0])
                    if index < len(target_items):
                        # 立即清除之前的选择并选择新项
                        target_tree.selection_remove(*target_tree.selection())
                        target_tree.selection_add(target_items[index])
                        target_tree.see(target_items[index])
                        # 强制更新显示
                        target_tree.update_idletasks()
                except ValueError:
                    pass
            
            # 使用after方法延迟执行同步操作
            source_tree.after(100, sync_selection)
        
        # 绑定点击事件
        self.left_tree.bind("<Button-1>", lambda e: on_tree_click(e, self.left_tree, self.right_tree))
        self.right_tree.bind("<Button-1>", lambda e: on_tree_click(e, self.right_tree, self.left_tree))
        
        # 绑定键盘事件
        self.left_tree.bind("<Up>", lambda e: on_tree_click(e, self.left_tree, self.right_tree))
        self.left_tree.bind("<Down>", lambda e: on_tree_click(e, self.left_tree, self.right_tree))
        self.right_tree.bind("<Up>", lambda e: on_tree_click(e, self.right_tree, self.left_tree))
        self.right_tree.bind("<Down>", lambda e: on_tree_click(e, self.right_tree, self.left_tree))
        
    def toggle_sync_scroll(self):
        """切换同步滚动状态"""
        if self.sync_scroll.get():
            # 启用同步滚动
            self.left_tree.bind("<Button-4>", self.on_mousewheel)
            self.left_tree.bind("<Button-5>", self.on_mousewheel)
            self.right_tree.bind("<Button-4>", self.on_mousewheel)
            self.right_tree.bind("<Button-5>", self.on_mousewheel)
            self.root.bind_all("<Button-4>", self.on_mousewheel)
            self.root.bind_all("<Button-5>", self.on_mousewheel)
        else:
            # 禁用同步滚动
            self.left_tree.unbind("<Button-4>")
            self.left_tree.unbind("<Button-5>")
            self.right_tree.unbind("<Button-4>")
            self.right_tree.unbind("<Button-5>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
            
    def on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        if not self.sync_scroll.get():
            return
            
        # 获取当前滚动的文本框
        current_text = event.widget
        if current_text == self.root:
            # 如果事件来自根窗口，找到当前焦点所在的文本框
            focused = self.root.focus_get()
            if focused in (self.left_tree, self.right_tree):
                current_text = focused
            else:
                return
                
        other_text = self.right_tree if current_text == self.left_tree else self.left_tree
        
        # 使用after方法延迟100ms后执行滚动
        def delayed_scroll():
            # 获取当前滚动位置
            current_pos = current_text.yview()[0]  # 只使用第一个值
            other_text.yview_moveto(current_pos)
            
        self.root.after(100, delayed_scroll)

    def select_file(self, side: str):
        file_path = filedialog.askopenfilename(
            title="选择SQL文件",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if file_path:
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
            self._update_history_lists()
            
            # 设置当前选择
            if side == "left":
                self.left_history_combo.set(file_path)
            else:
                self.right_history_combo.set(file_path)
                
            # 解析SQL文件
            if side == "left":
                self.left_tables = self.sql_parser.parse_file(file_path)
            else:
                self.right_tables = self.sql_parser.parse_file(file_path)
                
            # 显示表结构
            self.show_tables(side)

    def start_compare(self):
        # 获取左右两侧的历史记录选择
        left_display = self.left_history_combo.get()
        right_display = self.right_history_combo.get()
        
        if not left_display or not right_display:
            messagebox.showerror("错误", "请先选择两个数据源")
            return
            
        def compare_thread():
            try:
                # 获取左侧历史记录
                left_history = None
                for history in self.connection_manager.get_history("left"):
                    if history.display == left_display:
                        left_history = history
                        break
                        
                # 获取右侧历史记录
                right_history = None
                for history in self.connection_manager.get_history("right"):
                    if history.display == right_display:
                        right_history = history
                        break
                
                if not left_history or not right_history:
                    messagebox.showerror("错误", "无法找到选中的数据源")
                    return
                
                # 处理左侧数据源
                if left_history.type == "file":
                    self.left_tables = self.sql_parser.parse_file(left_history.value)
                elif left_history.type == "connection":
                    conn = self.connection_manager.get_connection(left_history.value)
                    if conn.type == "agent":
                        messagebox.showerror("错误", "暂不支持Agent类型的连接")
                        return
                
                # 处理右侧数据源
                if right_history.type == "file":
                    self.right_tables = self.sql_parser.parse_file(right_history.value)
                elif right_history.type == "connection":
                    conn = self.connection_manager.get_connection(right_history.value)
                    if conn.type == "agent":
                        messagebox.showerror("错误", "暂不支持Agent类型的连接")
                        return
                
                # 比较并显示差异
                self.show_differences()
            except Exception as e:
                messagebox.showerror("错误", f"比较过程中出错: {str(e)}")
                
        # 使用线程执行比较操作
        threading.Thread(target=compare_thread, daemon=True).start()
        
    def show_differences(self):
        # 清空显示区域
        self.left_tree.delete(*self.left_tree.get_children())
        self.right_tree.delete(*self.right_tree.get_children())
        
        # 获取差异
        differences = self.sql_parser.compare_tables(self.left_tables, self.right_tables)
        
        # 获取所有表名
        all_tables = sorted(set(list(self.left_tables.keys()) + list(self.right_tables.keys())))
        
        # 为每个表创建数据
        for table_index, table_name in enumerate(all_tables, 1):
            # 获取左右表的字段
            left_columns = self.left_tables.get(table_name, {}).get('columns', {})
            right_columns = self.right_tables.get(table_name, {}).get('columns', {})
            
            # 计算字段数量
            left_count = len(left_columns)
            right_count = len(right_columns)

            # 计算索引数量
            left_indexes = self.left_tables.get(table_name, {}).get('indexes', {})
            right_indexes = self.right_tables.get(table_name, {}).get('indexes', {})

            left_index_count = len(left_indexes)
            right_index_count = len(right_indexes)
            
            # 检查表是否有差异
            has_table_differences = (
                table_name in differences.get('modified_tables', {}) or
                table_name in differences.get('added_tables', []) or
                table_name in differences.get('removed_tables', [])
            )
            
            # 如果启用了隐藏相同行且表没有差异，则跳过
            if self.hide_same.get() and not has_table_differences:
                continue
            
            # 添加表头
            self.left_tree.insert("", "end", values=(f"表{table_index}", f"表名: {table_name}", f"字段数: {left_count} 索引数: {left_index_count}"), tags=("table_header",))
            self.right_tree.insert("", "end", values=(f"表{table_index}", f"表名: {table_name}", f"字段数: {right_count} 索引数: {right_index_count}"), tags=("table_header",))
            
            # 获取所有字段名
            all_columns = sorted(set(list(left_columns.keys()) + list(right_columns.keys())))

            if all_columns:
                # 添加字段标题行
                self.left_tree.insert("", "end", values=("", "字段", ""), tags=("header",))
                self.right_tree.insert("", "end", values=("", "字段", ""), tags=("header",))
            
                # 添加字段行
                for col_index, col_name in enumerate(all_columns, 1):
                    left_def = left_columns.get(col_name, "")
                    right_def = right_columns.get(col_name, "")
                    
                    # 确定标签
                    left_tags = []
                    right_tags = []
                    
                    has_column_differences = False
                    is_missing = False
                    if table_name in differences.get('modified_tables', {}):
                        changes = differences['modified_tables'][table_name]
                        if 'columns' in changes:
                            cols_changes = changes['columns']
                            if col_name in cols_changes.get('removed_columns', {}):
                                left_tags.append("different")
                                has_column_differences = True
                            if col_name in cols_changes.get('added_columns', {}):
                                right_tags.append("different")
                                has_column_differences = True
                            if col_name in cols_changes.get('modified_columns', {}):
                                left_tags.append("different")
                                right_tags.append("different")
                                has_column_differences = True
                    
                    if not left_def and right_def:
                        left_tags.append("missing")
                        has_column_differences = True
                        is_missing = True
                    if not right_def and left_def:
                        right_tags.append("missing")
                        has_column_differences = True
                        is_missing = True
                    
                    # 如果启用了隐藏相同行且字段没有差异，则跳过
                    if self.hide_same.get() and not has_column_differences:
                        continue
                        
                    # 如果启用了仅显示缺失且不是缺失字段，则跳过
                    if self.show_missing_only.get() and not is_missing:
                        continue
                    
                    # 插入行，使用raw值
                    left_def_display = left_def.get('raw', '') if isinstance(left_def, dict) else left_def
                    right_def_display = right_def.get('raw', '') if isinstance(right_def, dict) else right_def
                    
                    self.left_tree.insert("", "end", values=(col_index, col_name, left_def_display or "[缺失]"), tags=tuple(left_tags))
                    self.right_tree.insert("", "end", values=(col_index, col_name, right_def_display or "[缺失]"), tags=tuple(right_tags))
                
            # 添加索引信息
            all_indexes = sorted(set(list(left_indexes.keys()) + list(right_indexes.keys())))
            if all_indexes:
                # 添加索引标题行
                self.left_tree.insert("", "end", values=("", "索引", ""), tags=("header",))
                self.right_tree.insert("", "end", values=("", "索引", ""), tags=("header",))
                
                # 添加索引行
                for idx_index, idx_name in enumerate(all_indexes, 1):
                    left_idx = left_indexes.get(idx_name, {})
                    right_idx = right_indexes.get(idx_name, {})
                    
                    # 格式化索引定义
                    left_idx_def = f"{left_idx.get('type', '')} ({left_idx.get('columns', '')})" if left_idx else ""
                    right_idx_def = f"{right_idx.get('type', '')} ({right_idx.get('columns', '')})" if right_idx else ""
                    
                    # 确定标签
                    left_tags = []
                    right_tags = []
                    has_index_differences = False
                    is_missing = False
                    
                    if table_name in differences.get('modified_tables', {}):
                        changes = differences['modified_tables'][table_name]
                        if 'indexes' in changes:
                            idx_changes = changes['indexes']
                            if idx_name in idx_changes.get('removed_indexes', []):
                                left_tags.append("different")
                                has_index_differences = True
                            if idx_name in idx_changes.get('added_indexes', []):
                                right_tags.append("different")
                                has_index_differences = True
                            if idx_name in idx_changes.get('modified_indexes', []):
                                left_tags.append("different")
                                right_tags.append("different")
                                has_index_differences = True
                    
                    if not left_idx_def and right_idx_def:
                        left_tags.append("missing")
                        has_index_differences = True
                        is_missing = True
                    if not right_idx_def and left_idx_def:
                        right_tags.append("missing")
                        has_index_differences = True
                        is_missing = True
                    
                    # 如果启用了隐藏相同行且索引没有差异，则跳过
                    if self.hide_same.get() and not has_index_differences:
                        continue
                        
                    # 如果启用了仅显示缺失且不是缺失索引，则跳过
                    if self.show_missing_only.get() and not is_missing:
                        continue
                    
                    # 插入行
                    self.left_tree.insert("", "end", values=(idx_index, idx_name, left_idx_def or "[缺失]"), tags=tuple(left_tags))
                    self.right_tree.insert("", "end", values=(idx_index, idx_name, right_idx_def or "[缺失]"), tags=tuple(right_tags))
            
            # 添加空行
            self.left_tree.insert("", "end", values=("", "", ""))
            self.right_tree.insert("", "end", values=("", "", ""))
        
        # 配置标签样式
        for tree in (self.left_tree, self.right_tree):
            StyleManager.configure_tree_tags(tree, self.colors)
        
    def generate_sync_sql(self):
        if not self.left_tables or not self.right_tables:
            messagebox.showerror("错误", "请先执行比较操作")
            return
            
        # 创建目标库选择对话框
        target_dialog = tk.Toplevel(self.root)
        target_dialog.title("🎯 选择目标库")
        target_dialog.geometry("500x300")
        target_dialog.transient(self.root)
        target_dialog.grab_set()
        target_dialog.configure(bg=self.colors['light'])
        
        # 居中显示
        target_dialog.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 100,
            self.root.winfo_rooty() + 100))
        
        # 获取左右数据库的名称
        left_name = "左侧数据库"
        right_name = "右侧数据库"
        
        # 尝试从历史记录中获取数据库名称
        left_history = self.connection_manager.get_history("left")
        right_history = self.connection_manager.get_history("right")
        
        if left_history:
            left_name = left_history[0].display
        if right_history:
            right_name = right_history[0].display
            
        # 创建选择框架
        main_frame = ttk.Frame(target_dialog, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="请选择目标数据库", 
                               font=self.fonts['title'],
                               foreground=self.colors['dark'])
        title_label.pack(pady=(0, 25))
        
        target_var = tk.StringVar(value="right")
        
        # 选项框架
        option_frame = ttk.LabelFrame(main_frame, text="同步方向", padding="15")
        option_frame.pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(option_frame, 
                       text=f"以 {right_name} 为目标库（将左侧结构同步到右侧）", 
                       variable=target_var, 
                       value="right",
                       font=self.fonts['body']).pack(anchor=tk.W, pady=8)
        
        ttk.Radiobutton(option_frame, 
                       text=f"以 {left_name} 为目标库（将右侧结构同步到左侧）", 
                       variable=target_var, 
                       value="left",
                       font=self.fonts['body']).pack(anchor=tk.W, pady=8)
        
        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=25)
        
        def on_confirm():
            target_side = target_var.get()
            target_dialog.destroy()
            
            try:
                if target_side == "right":
                    # 以右侧为目标库，将左侧结构同步到右侧
                    sync_sql = self.sql_generator.generate_sync_sql(self.left_tables, self.right_tables)
                    title = f"同步SQL - 将 {left_name} 同步到 {right_name}"
                else:
                    # 以左侧为目标库，将右侧结构同步到左侧
                    sync_sql = self.sql_generator.generate_sync_sql(self.right_tables, self.left_tables)
                    title = f"同步SQL - 将 {right_name} 同步到 {left_name}"
                
                # 创建新窗口显示SQL
                sql_window = tk.Toplevel(self.root)
                sql_window.title(title)
                sql_window.geometry("900x700")
                sql_window.configure(bg=self.colors['light'])
                
                # 创建SQL显示框架
                sql_frame = ttk.Frame(sql_window, padding="15")
                sql_frame.pack(fill=tk.BOTH, expand=True)
                
                # SQL标题
                sql_title = ttk.Label(sql_frame, text="生成的同步SQL语句", 
                                     font=self.fonts['subtitle'],
                                     foreground=self.colors['dark'])
                sql_title.pack(pady=(0, 10))
                
                # SQL文本区域
                sql_text = scrolledtext.ScrolledText(sql_window, 
                                                   wrap=tk.WORD,
                                                   font=self.fonts['code'],
                                                   background=self.colors['white'],
                                                   foreground=self.colors['dark'],
                                                   insertbackground=self.colors['dark'])
                sql_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
                sql_text.insert(tk.END, sync_sql)
                
            except Exception as e:
                messagebox.showerror("错误", f"生成同步SQL时出错: {str(e)}")
        
        def on_cancel():
            target_dialog.destroy()
        
        ttk.Button(btn_frame, text="确定", 
                  style='Success.TButton',
                  command=on_confirm).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", 
                  style='Warning.TButton',
                  command=on_cancel).pack(side=tk.LEFT, padx=10)
        
        # 等待对话框关闭
        self.root.wait_window(target_dialog)

    def _show_connection_dialog(self, side: str = None):
        if side is None:
            dialog = ConnectionDialog(self.root, self.connection_manager)
            dialog.grab_set()
        else:
            dialog = SelectConnectionDialog(self.root, self.connection_manager, lambda conn: self._on_connection_selected(side, conn))
            dialog.grab_set()
        
    def _on_connection_selected(self, side: str, connection: Connection):
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
        self._update_history_lists()
        
        # 设置当前选择
        if side == "left":
            self.left_history_combo.set(display)
        else:
            self.right_history_combo.set(display)
            
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
                messagebox.showerror("错误", f"获取表结构失败: {str(e)}")
        elif connection.type == "agent":
            messagebox.showinfo("提示", "暂不支持Agent类型的连接")
        
    def _update_history_lists(self):
        # 获取历史记录
        left_history = self.connection_manager.get_history("left")
        right_history = self.connection_manager.get_history("right")
        
        # 更新左侧历史记录列表
        self.left_history_combo["values"] = [h.display for h in left_history]
            
        # 更新右侧历史记录列表
        self.right_history_combo["values"] = [h.display for h in right_history]

    def _on_history_select(self, side: str):
        combo = self.left_history_combo if side == "left" else self.right_history_combo
        display = combo.get()
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
                            messagebox.showerror("错误", f"获取表结构失败: {str(e)}")
                    elif conn.type == "agent":
                        messagebox.showinfo("提示", "暂不支持Agent类型的连接")
                    
                # 更新最后使用时间
                self.connection_manager.update_history_last_used(history.id)
                break
                
        # 显示差异
        self.show_tables(side)

    def show_tables(self, side: str):
        """显示表结构"""
        # 清空显示区域
        tree = self.left_tree if side == "left" else self.right_tree
        tree.delete(*tree.get_children())
        
        # 获取表数据
        tables = self.left_tables if side == "left" else self.right_tables
        
        # 获取所有表名
        all_tables = sorted(tables.keys())
        
        # 为每个表创建数据
        for table_index, table_name in enumerate(all_tables, 1):
            # 获取表的字段
            columns = tables[table_name].get('columns', {})
            indexes = tables[table_name].get('indexes', {})
            
            # 计算字段数量和索引数量
            column_count = len(columns)
            index_count = len(indexes)
            
            # 添加表头
            tree.insert("", "end", values=(f"表{table_index}", f"表名: {table_name}", f"字段数: {column_count} 索引数: {index_count}"), tags=("table_header",))
            
            # 添加字段信息
            if columns:
                # 添加字段标题行
                tree.insert("", "end", values=("", "字段", ""), tags=("header",))
                
                # 添加字段行
                for col_index, (col_name, col_def) in enumerate(sorted(columns.items()), 1):
                    col_def_display = col_def.get('raw', '') if isinstance(col_def, dict) else col_def
                    tree.insert("", "end", values=(col_index, col_name, col_def_display))
            
            # 添加索引信息
            if indexes:
                # 添加索引标题行
                tree.insert("", "end", values=("", "索引", ""), tags=("header",))
                
                # 添加索引行
                for idx_index, (idx_name, idx_def) in enumerate(sorted(indexes.items()), 1):
                    idx_type = idx_def.get('type', '')
                    idx_columns = idx_def.get('columns', '')
                    idx_def_display = f"{idx_type} ({idx_columns})"
                    tree.insert("", "end", values=(idx_index, idx_name, idx_def_display))
            
            # 添加空行
            tree.insert("", "end", values=("", "", ""))
