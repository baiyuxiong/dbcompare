import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from models import Connection, ConnectionManager
from datetime import datetime
import mysql.connector

class ConnectionDialog(tk.Toplevel):
    def __init__(self, parent, connection_manager: ConnectionManager, on_connection_selected: Optional[Callable[[Connection], None]] = None):
        super().__init__(parent)
        self.title("连接管理")
        self.connection_manager = connection_manager
        self.on_connection_selected = on_connection_selected
        self.selected_connection: Optional[Connection] = None
        
        self._init_ui()
        self._load_connections()

    def _init_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 连接列表
        list_frame = ttk.LabelFrame(main_frame, text="连接列表", padding="5")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.connection_list = ttk.Treeview(list_frame, columns=("name", "database"), show="headings")
        self.connection_list.heading("name", text="名称")
        self.connection_list.heading("database", text="数据库名称")
        self.connection_list.pack(fill=tk.BOTH, expand=True)
        self.connection_list.bind("<<TreeviewSelect>>", self._on_select_connection)
        self.connection_list.bind("<Double-1>", self._on_double_click)

        # 按钮框架
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="新建", command=self._on_new).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="删除", command=self._on_delete).pack(side=tk.LEFT, padx=2)

        # 连接详情框架
        detail_frame = ttk.LabelFrame(main_frame, text="连接详情", padding="5")
        detail_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 基本信息
        ttk.Label(detail_frame, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(detail_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        # MySQL配置框架
        self.mysql_frame = ttk.LabelFrame(detail_frame, text="MySQL配置", padding="5")
        self.mysql_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)

        ttk.Label(self.mysql_frame, text="主机:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.host_entry = ttk.Entry(self.mysql_frame)
        self.host_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(self.mysql_frame, text="端口:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.port_entry = ttk.Entry(self.mysql_frame)
        self.port_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        ttk.Label(self.mysql_frame, text="用户名:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.username_entry = ttk.Entry(self.mysql_frame)
        self.username_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)

        ttk.Label(self.mysql_frame, text="密码:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.password_entry = ttk.Entry(self.mysql_frame, show="*")
        self.password_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)

        ttk.Label(self.mysql_frame, text="数据库:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.database_entry = ttk.Entry(self.mysql_frame)
        self.database_entry.grid(row=4, column=1, sticky=tk.EW, pady=2)

        # 按钮框架
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="测试连接", command=self._test_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存", command=self._on_save).pack(side=tk.LEFT, padx=5)

    def _load_connections(self):
        # 清空列表
        for item in self.connection_list.get_children():
            self.connection_list.delete(item)
        
        # 加载连接
        connections = self.connection_manager.get_all_connections()
        for conn in connections:
            database_name = ""
            if conn.type == "mysql" and "database" in conn.config:
                database_name = conn.config["database"]
            self.connection_list.insert("", "end", values=(conn.name, database_name), tags=(str(conn.id),))

    def _on_select_connection(self, event):
        selection = self.connection_list.selection()
        if not selection:
            return
        
        item = selection[0]
        conn_id = int(self.connection_list.item(item)["tags"][0])
        self.selected_connection = self.connection_manager.get_connection(conn_id)
        self._update_ui()

    def _on_new(self):
        self.selected_connection = None
        self._clear_ui()

    def _on_delete(self):
        if not self.selected_connection:
            return
        
        # 创建模态确认对话框
        confirm_dialog = tk.Toplevel(self)
        confirm_dialog.title("确认")
        confirm_dialog.transient(self)  # 设置为主窗口的临时窗口
        confirm_dialog.grab_set()  # 设置为模态
        
        # 居中显示
        confirm_dialog.geometry("+%d+%d" % (
            self.winfo_rootx() + 50,
            self.winfo_rooty() + 50))
        
        # 添加确认信息
        ttk.Label(confirm_dialog, text="确定要删除这个连接吗？").pack(padx=20, pady=10)
        
        # 添加按钮
        btn_frame = ttk.Frame(confirm_dialog)
        btn_frame.pack(pady=10)
        
        def on_confirm():
            self.connection_manager.delete_connection(self.selected_connection.id)
            self._load_connections()
            self.selected_connection = None
            self._clear_ui()
            # 通知主窗口刷新历史记录
            if hasattr(self.master, '_update_history_lists'):
                self.master._update_history_lists()
            confirm_dialog.destroy()
            
        def on_cancel():
            confirm_dialog.destroy()
            
        ttk.Button(btn_frame, text="确定", command=on_confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 等待对话框关闭
        self.wait_window(confirm_dialog)

    def _update_ui(self):
        if not self.selected_connection:
            return
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_connection.name)
        
        config = self.selected_connection.config
        if self.selected_connection.type == "mysql":
            self.host_entry.delete(0, tk.END)
            self.host_entry.insert(0, config.get("host", ""))
            
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, str(config.get("port", "")))
            
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, config.get("username", ""))
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, config.get("password", ""))
            
            self.database_entry.delete(0, tk.END)
            self.database_entry.insert(0, config.get("database", ""))

    def _clear_ui(self):
        self.name_entry.delete(0, tk.END)
        self.host_entry.delete(0, tk.END)
        self.port_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.database_entry.delete(0, tk.END)

    def _on_save(self):
        name = self.name_entry.get().strip()
        if not name:
            tk.messagebox.showerror("错误", "请输入连接名称")
            return
        
        # 默认使用直连MySQL
        conn_type = "mysql"
        config = {
            "host": self.host_entry.get().strip(),
            "port": int(self.port_entry.get().strip() or "3306"),
            "username": self.username_entry.get().strip(),
            "password": self.password_entry.get(),
            "database": self.database_entry.get().strip()
        }
        
        now = datetime.now()
        if self.selected_connection:
            self.selected_connection.name = name
            self.selected_connection.type = conn_type
            self.selected_connection.config = config
            self.selected_connection.last_used = now
            self.connection_manager.update_connection(self.selected_connection)
        else:
            connection = Connection(
                id=None,
                name=name,
                type=conn_type,
                config=config,
                last_used=now,
                created_at=now
            )
            self.connection_manager.add_connection(connection)
        
        self._load_connections()

    def _on_double_click(self, event):
        self._on_select()

    def _on_select(self):
        if not self.selected_connection:
            return
            
        if self.on_connection_selected:
            self.on_connection_selected(self.selected_connection)
        self.destroy()

    def _test_connection(self):
        """测试数据库连接"""
        self._test_mysql_connection()

    def _test_mysql_connection(self):
        """测试MySQL连接"""
        try:
            config = {
                "host": self.host_entry.get().strip(),
                "port": int(self.port_entry.get().strip() or "3306"),
                "user": self.username_entry.get().strip(),
                "password": self.password_entry.get(),
                "database": self.database_entry.get().strip()
            }
            
            # 尝试建立连接
            conn = mysql.connector.connect(**config)
            conn.close()
            
            messagebox.showinfo("成功", "MySQL数据库连接测试成功！", parent=self)
        except Exception as e:
            messagebox.showerror("错误", f"MySQL数据库连接测试失败：{str(e)}", parent=self)

class SelectConnectionDialog(tk.Toplevel):
    def __init__(self, parent, connection_manager: ConnectionManager, on_connection_selected: Optional[Callable[[Connection], None]] = None):
        super().__init__(parent)
        self.title("选择连接")
        self.connection_manager = connection_manager
        self.on_connection_selected = on_connection_selected
        self.selected_connection: Optional[Connection] = None
        
        self._init_ui()
        self._load_connections()

    def _init_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 连接列表
        list_frame = ttk.LabelFrame(main_frame, text="连接列表", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.connection_list = ttk.Treeview(list_frame, columns=("name", "database"), show="headings")
        self.connection_list.heading("name", text="名称")
        self.connection_list.heading("database", text="数据库名称")
        self.connection_list.pack(fill=tk.BOTH, expand=True)
        self.connection_list.bind("<<TreeviewSelect>>", self._on_select_connection)
        self.connection_list.bind("<Double-1>", self._on_double_click)

        # 按钮框架
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="选择", command=self._on_select).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.LEFT, padx=2)

    def _load_connections(self):
        # 清空列表
        for item in self.connection_list.get_children():
            self.connection_list.delete(item)
        
        # 加载连接
        connections = self.connection_manager.get_all_connections()
        for conn in connections:
            database_name = ""
            if conn.type == "mysql" and "database" in conn.config:
                database_name = conn.config["database"]
            self.connection_list.insert("", "end", values=(conn.name, database_name), tags=(str(conn.id),))

    def _on_select_connection(self, event):
        selection = self.connection_list.selection()
        if not selection:
            return
        
        item = selection[0]
        conn_id = int(self.connection_list.item(item)["tags"][0])
        self.selected_connection = self.connection_manager.get_connection(conn_id)

    def _on_double_click(self, event):
        self._on_select()

    def _on_select(self):
        if not self.selected_connection:
            return
            
        if self.on_connection_selected:
            self.on_connection_selected(self.selected_connection)
        self.destroy() 