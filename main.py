import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from sql_parser import SQLParser
from sql_generator import SQLGenerator

class SQLCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MySQL表结构比较工具")
        self.root.geometry("1200x800")
        
        # 初始化变量
        self.sync_scroll = tk.BooleanVar(value=True)
        self.left_tables = {}
        self.right_tables = {}
        
        # 初始化SQL解析器
        self.sql_parser = SQLParser()
        self.sql_generator = SQLGenerator()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主内容区
        self.create_main_content()

        self.toggle_sync_scroll()
        
    def create_menu(self):
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=5, pady=5)
        
        compare_btn = ttk.Button(menu_frame, text="开始比较", command=self.start_compare)
        compare_btn.pack(side=tk.LEFT, padx=5)
        
        generate_btn = ttk.Button(menu_frame, text="生成同步SQL", command=self.generate_sync_sql)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加同步滚动开关
        sync_check = ttk.Checkbutton(
            menu_frame, 
            text="同步滚动", 
            variable=self.sync_scroll,
            command=self.toggle_sync_scroll
        )
        sync_check.pack(side=tk.LEFT, padx=5)
        
    def create_main_content(self):
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板
        left_frame = ttk.LabelFrame(content_frame, text="左侧SQL文件")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.left_file_btn = ttk.Button(left_frame, text="选择SQL文件", command=lambda: self.select_file("left"))
        self.left_file_btn.pack(pady=5)
        
        # 创建左侧表格
        self.left_tree = ttk.Treeview(left_frame, columns=("index", "field", "definition"), show="headings")
        self.left_tree.heading("index", text="序号")
        self.left_tree.heading("field", text="字段名")
        self.left_tree.heading("definition", text="定义")
        self.left_tree.column("index", width=50)
        self.left_tree.column("field", width=150)
        self.left_tree.column("definition", width=400)
        self.left_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 右侧面板
        right_frame = ttk.LabelFrame(content_frame, text="右侧SQL文件")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.right_file_btn = ttk.Button(right_frame, text="选择SQL文件", command=lambda: self.select_file("right"))
        self.right_file_btn.pack(pady=5)
        
        # 创建右侧表格
        self.right_tree = ttk.Treeview(right_frame, columns=("index", "field", "definition"), show="headings")
        self.right_tree.heading("index", text="序号")
        self.right_tree.heading("field", text="字段名")
        self.right_tree.heading("definition", text="定义")
        self.right_tree.column("index", width=50)
        self.right_tree.column("field", width=150)
        self.right_tree.column("definition", width=400)
        self.right_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 配置标签样式
        for tree in (self.left_tree, self.right_tree):
            tree.tag_configure("table_header", font=('DejaVu Sans Mono', 10, 'bold'), background='#666666', foreground='white')
            tree.tag_configure("header", font=('DejaVu Sans Mono', 10, 'bold'), background='#CCCCCC', foreground='black')
            tree.tag_configure("different", foreground="#ff0000", font=('DejaVu Sans Mono', 10, 'bold'))
            tree.tag_configure("missing", foreground="#0000ff", font=('DejaVu Sans Mono', 10, 'bold'))
            
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
            # 首先触发<Button-1>事件,然后Tkinter才会更新selection()的状态，前面用source_tree.selection()，这里要延时等更新后处理
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

    def select_file(self, side):
        file_path = filedialog.askopenfilename(
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if file_path:
            if side == "left":
                self.left_file_path = file_path
                self.left_file_btn.config(text=f"已选择: {file_path.split('/')[-1]}")
            else:
                self.right_file_path = file_path
                self.right_file_btn.config(text=f"已选择: {file_path.split('/')[-1]}")
                
    def start_compare(self):
        if not hasattr(self, 'left_file_path') or not hasattr(self, 'right_file_path'):
            messagebox.showerror("错误", "请先选择两个SQL文件")
            return
            
        def compare_thread():
            try:
                # 解析SQL文件
                self.left_tables = self.sql_parser.parse_file(self.left_file_path)
                self.right_tables = self.sql_parser.parse_file(self.right_file_path)
                
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
                    
                    if table_name in differences.get('modified_tables', {}):
                        changes = differences['modified_tables'][table_name]
                        if 'columns' in changes:
                            cols_changes = changes['columns']
                            if col_name in cols_changes.get('removed_columns', []):
                                left_tags.append("different")
                            if col_name in cols_changes.get('added_columns', []):
                                right_tags.append("different")
                            if col_name in cols_changes.get('modified_columns', []):
                                left_tags.append("different")
                                right_tags.append("different")
                    
                    if not left_def and right_def:
                        left_tags.append("missing")
                    if not right_def and left_def:
                        right_tags.append("missing")
                    
                    # 插入行
                    self.left_tree.insert("", "end", values=(col_index, col_name, left_def or "[缺失]"), tags=tuple(left_tags))
                    self.right_tree.insert("", "end", values=(col_index, col_name, right_def or "[缺失]"), tags=tuple(right_tags))
                
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
                    
                    if table_name in differences.get('modified_tables', {}):
                        changes = differences['modified_tables'][table_name]
                        if 'indexes' in changes:
                            idx_changes = changes['indexes']
                            if idx_name in idx_changes.get('removed_indexes', []):
                                left_tags.append("different")
                            if idx_name in idx_changes.get('added_indexes', []):
                                right_tags.append("different")
                            if idx_name in idx_changes.get('modified_indexes', []):
                                left_tags.append("different")
                                right_tags.append("different")
                    
                    if not left_idx_def and right_idx_def:
                        left_tags.append("missing")
                    if not right_idx_def and left_idx_def:
                        right_tags.append("missing")
                    
                    # 插入行
                    self.left_tree.insert("", "end", values=(idx_index, idx_name, left_idx_def or "[缺失]"), tags=tuple(left_tags))
                    self.right_tree.insert("", "end", values=(idx_index, idx_name, right_idx_def or "[缺失]"), tags=tuple(right_tags))
            
            # 添加空行
            self.left_tree.insert("", "end", values=("", "", ""))
            self.right_tree.insert("", "end", values=("", "", ""))
        
        # 配置标签样式
        for tree in (self.left_tree, self.right_tree):
            tree.tag_configure("table_header", font=('DejaVu Sans Mono', 10, 'bold'), background='#666666', foreground='white')
            tree.tag_configure("header", font=('DejaVu Sans Mono', 10, 'bold'), background='#CCCCCC', foreground='black')
            tree.tag_configure("different", foreground="#ff0000", font=('DejaVu Sans Mono', 10, 'bold'))
            tree.tag_configure("missing", foreground="#0000ff", font=('DejaVu Sans Mono', 10, 'bold'))
        
    def generate_sync_sql(self):
        if not self.left_tables or not self.right_tables:
            messagebox.showerror("错误", "请先执行比较操作")
            return
            
        try:
            sync_sql = self.sql_generator.generate_sync_sql(self.left_tables, self.right_tables)
            
            # 创建新窗口显示SQL
            sql_window = tk.Toplevel(self.root)
            sql_window.title("同步SQL")
            sql_window.geometry("800x600")
            
            sql_text = scrolledtext.ScrolledText(sql_window, wrap=tk.WORD)
            sql_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            sql_text.insert(tk.END, sync_sql)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成同步SQL时出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLCompareApp(root)
    root.mainloop() 