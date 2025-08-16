"""
国际化管理器
负责语言切换和文本翻译
"""

import json
import os
import locale
import platform
import sys
from typing import Dict, Any, Optional
from pathlib import Path


class I18nManager:
    """国际化管理器"""
    
    def __init__(self, connection_manager=None):
        self.current_language = "zh_CN"  # 默认中文
        self.translations: Dict[str, Dict[str, str]] = {}
        self.connection_manager = connection_manager
        self.load_translations()
        self.load_language_setting()
        
        # 如果是首次启动（没有保存的语言设置），则检测系统语言
        if not self._has_saved_language_setting():
            self._detect_system_language()
    
    def load_translations(self):
        """加载翻译文件"""
        # 获取语言文件路径
        i18n_dir = self._get_i18n_directory()
        
        # 加载中文翻译
        zh_file = i18n_dir / "zh_CN.json"
        if zh_file.exists():
            try:
                with open(zh_file, 'r', encoding='utf-8') as f:
                    self.translations["zh_CN"] = json.load(f)
                print(f"✓ 加载中文翻译文件: {zh_file}")
            except Exception as e:
                print(f"✗ 加载中文翻译文件失败: {e}")
        else:
            print(f"✗ 中文翻译文件不存在: {zh_file}")
        
        # 加载英文翻译
        en_file = i18n_dir / "en_US.json"
        if en_file.exists():
            try:
                with open(en_file, 'r', encoding='utf-8') as f:
                    self.translations["en_US"] = json.load(f)
                print(f"✓ 加载英文翻译文件: {en_file}")
            except Exception as e:
                print(f"✗ 加载英文翻译文件失败: {e}")
        else:
            print(f"✗ 英文翻译文件不存在: {en_file}")
        
        # 如果没有加载到任何翻译文件，使用内置的默认翻译
        if not self.translations:
            print("⚠ 未找到翻译文件，使用内置默认翻译")
            self._load_default_translations()
    
    def _get_i18n_directory(self) -> Path:
        """获取国际化文件目录"""
        # 检查是否在PyInstaller打包环境中
        if getattr(sys, 'frozen', False):
            # 打包环境 - 尝试多个可能的路径
            base_path = Path(sys._MEIPASS)
            
            # 路径1: 直接在根目录下的i18n文件夹
            i18n_path = base_path / "i18n"
            if i18n_path.exists():
                return i18n_path
            
            # 路径2: 在src/i18n目录下
            src_i18n_path = base_path / "src" / "i18n"
            if src_i18n_path.exists():
                return src_i18n_path
            
            # 路径3: 在当前目录下查找
            current_dir = Path.cwd()
            current_i18n_path = current_dir / "i18n"
            if current_i18n_path.exists():
                return current_i18n_path
            
            # 路径4: 在可执行文件所在目录下查找
            exe_dir = Path(sys.executable).parent
            exe_i18n_path = exe_dir / "i18n"
            if exe_i18n_path.exists():
                return exe_i18n_path
            
            # 如果都找不到，返回默认路径
            print(f"⚠ 在打包环境中未找到i18n目录，使用默认路径: {base_path / 'i18n'}")
            return base_path / "i18n"
        else:
            # 开发环境 - 使用相对路径
            current_dir = Path(__file__).parent
            return current_dir
    
    def _load_default_translations(self):
        """加载内置的默认翻译"""
        # 中文翻译
        self.translations["zh_CN"] = {
            "app_title": "MySQL表结构比较工具",
            "connection_management": "连接管理",
            "start_compare": "开始比较",
            "generate_sync_sql": "生成同步SQL",
            "sync_scroll": "同步滚动",
            "hide_same_rows": "隐藏相同行",
            "show_missing_only": "仅显示缺失",
            "ignore_case": "忽略大小写",
            "left_data_source": "左侧数据源",
            "right_data_source": "右侧数据源",
            "connect": "连接",
            "file": "文件",
            "history": "历史记录:",
            "select_sql_file": "选择SQL文件",
            "sql_files": "SQL files (*.sql)",
            "all_files": "All files (*.*)",
            "warning": "警告",
            "error": "错误",
            "info": "提示",
            "please_select_two_data_sources": "请先选择两个数据源",
            "please_load_left_table_structure": "请先加载左侧表结构数据",
            "please_load_right_table_structure": "请先加载右侧表结构数据",
            "please_load_left_and_right_table_structure": "请先加载左侧和右侧的表结构数据",
            "file_load_failed": "加载文件失败",
            "get_table_structure_failed": "获取表结构失败",
            "generate_sync_sql_error": "生成同步SQL时出错",
            "agent_connection_not_supported": "暂不支持Agent类型的连接",
            "table": "表",
            "table_name": "表名:",
            "field_count": "字段数:",
            "index_count": "索引数:",
            "field": "字段",
            "index": "索引",
            "missing": "[缺失]",
            "sequence_number": "序号",
            "field_name": "字段名",
            "field_definition": "字段定义",
            "select_target_database": "选择目标库",
            "select_target_database_desc": "选择要将哪个数据库作为目标，另一个数据库的结构将同步到目标数据库中",
            "sync_direction": "同步方向",
            "target_right_database": "以 {right_name} 为目标库（将左侧结构同步到右侧）",
            "target_left_database": "以 {left_name} 为目标库（将右侧结构同步到左侧）",
            "confirm": "确定",
            "cancel": "取消",
            "close": "关闭",
            "copy_sql": "复制SQL",
            "sql_copied_to_clipboard": "SQL已复制到剪贴板",
            "sync_sql_title_right": "同步SQL - 将 {left_name} 同步到 {right_name}",
            "sync_sql_title_left": "同步SQL - 将 {right_name} 同步到 {left_name}",
            "generated_sync_sql_prompt": "生成的同步SQL语句如下，请仔细检查后执行：",
            "connection_name": "连接名称",
            "connection_type": "连接类型",
            "host": "主机",
            "port": "端口",
            "username": "用户名",
            "password": "密码",
            "database": "数据库",
            "url": "URL",
            "add_connection": "添加连接",
            "edit_connection": "编辑连接",
            "delete_connection": "删除连接",
            "test_connection": "测试连接",
            "connection_test_success": "连接测试成功",
            "connection_test_failed": "连接测试失败",
            "please_fill_required_fields": "请填写必填字段",
            "connection_name_required": "连接名称不能为空",
            "host_required": "主机地址不能为空",
            "port_required": "端口不能为空",
            "username_required": "用户名不能为空",
            "database_required": "数据库名不能为空",
            "url_required": "URL不能为空",
            "mysql": "MySQL",
            "agent": "Agent",
            "language_settings": "语言设置",
            "language": "语言",
            "chinese": "中文",
            "english": "English",
            "settings": "设置",
            "apply": "应用",
            "language_setting_tip": "选择您希望使用的语言",
            "language_setting_saved": "语言设置已保存,请重启应用以应用新语言",
            "search": "搜索",
            "search_placeholder": "输入搜索内容...",
            "clear": "清除",
            "no_search_results": "未找到匹配的搜索结果",
            "search_result_info": "搜索结果：第 {current} 项，共 {total} 项"
        }
        
        # 英文翻译
        self.translations["en_US"] = {
            "app_title": "MySQL Table Structure Comparison Tool",
            "connection_management": "Connection Management",
            "start_compare": "Start Compare",
            "generate_sync_sql": "Generate Sync SQL",
            "sync_scroll": "Sync Scroll",
            "hide_same_rows": "Hide Same Rows",
            "show_missing_only": "Show Missing Only",
            "ignore_case": "Ignore Case",
            "left_data_source": "Left Data Source",
            "right_data_source": "Right Data Source",
            "connect": "Connect",
            "file": "File",
            "history": "History:",
            "select_sql_file": "Select SQL File",
            "sql_files": "SQL files (*.sql)",
            "all_files": "All files (*.*)",
            "warning": "Warning",
            "error": "Error",
            "info": "Info",
            "please_select_two_data_sources": "Please select two data sources first",
            "please_load_left_table_structure": "Please load left table structure data first",
            "please_load_right_table_structure": "Please load right table structure data first",
            "please_load_left_and_right_table_structure": "Please load left and right table structure data first",
            "file_load_failed": "Failed to load file",
            "get_table_structure_failed": "Failed to get table structure",
            "generate_sync_sql_error": "Error occurred while generating sync SQL",
            "agent_connection_not_supported": "Agent connection type is not supported yet",
            "table": "Table",
            "table_name": "Table Name:",
            "field_count": "Field Count:",
            "index_count": "Index Count:",
            "field": "Field",
            "index": "Index",
            "missing": "[Missing]",
            "sequence_number": "No.",
            "field_name": "Field Name",
            "field_definition": "Field Definition",
            "select_target_database": "Select Target Database",
            "select_target_database_desc": "Select which database to use as target, the structure of the other database will be synchronized to the target database",
            "sync_direction": "Sync Direction",
            "target_right_database": "Use {right_name} as target (sync left structure to right)",
            "target_left_database": "Use {left_name} as target (sync right structure to left)",
            "confirm": "OK",
            "cancel": "Cancel",
            "close": "Close",
            "copy_sql": "Copy SQL",
            "sql_copied_to_clipboard": "SQL copied to clipboard",
            "sync_sql_title_right": "Sync SQL - Sync {left_name} to {right_name}",
            "sync_sql_title_left": "Sync SQL - Sync {right_name} to {left_name}",
            "generated_sync_sql_prompt": "Generated sync SQL statements are shown below, please review carefully before execution:",
            "connection_name": "Connection Name",
            "connection_type": "Connection Type",
            "host": "Host",
            "port": "Port",
            "username": "Username",
            "password": "Password",
            "database": "Database",
            "url": "URL",
            "add_connection": "Add Connection",
            "edit_connection": "Edit Connection",
            "delete_connection": "Delete Connection",
            "test_connection": "Test Connection",
            "connection_test_success": "Connection test successful",
            "connection_test_failed": "Connection test failed",
            "please_fill_required_fields": "Please fill in required fields",
            "connection_name_required": "Connection name cannot be empty",
            "host_required": "Host address cannot be empty",
            "port_required": "Port cannot be empty",
            "username_required": "Username cannot be empty",
            "database_required": "Database name cannot be empty",
            "url_required": "URL cannot be empty",
            "mysql": "MySQL",
            "agent": "Agent",
            "language_settings": "Language Settings",
            "language": "Language",
            "chinese": "中文",
            "english": "English",
            "settings": "Settings",
            "apply": "Apply",
            "language_setting_tip": "Select your preferred language",
            "language_setting_saved": "Language settings saved, please restart the application to apply the new language",
            "search": "Search",
            "search_placeholder": "Enter search content...",
            "clear": "Clear",
            "no_search_results": "No matching search results found",
            "search_result_info": "Search result: {current} of {total}"
        }
    
    def load_language_setting(self):
        """加载语言设置"""
        if self.connection_manager:
            try:
                saved_language = self.connection_manager.get_config('language', 'zh_CN')
                if saved_language in self.translations:
                    self.current_language = saved_language
            except Exception as e:
                print(f"加载语言设置失败: {e}")
    
    def save_language_setting(self):
        """保存语言设置"""
        if self.connection_manager:
            try:
                self.connection_manager.set_config('language', self.current_language)
            except Exception as e:
                print(f"保存语言设置失败: {e}")
    
    def set_language(self, language: str):
        """设置当前语言"""
        if language in self.translations:
            self.current_language = language
            self.save_language_setting()
    
    def get_language(self) -> str:
        """获取当前语言"""
        return self.current_language
    
    def get_available_languages(self) -> list:
        """获取可用的语言列表"""
        return list(self.translations.keys())
    
    def tr(self, key: str, default: str = None) -> str:
        """翻译文本"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, default or key)
        return default or key
    
    def _has_saved_language_setting(self) -> bool:
        """检查是否有保存的语言设置"""
        if self.connection_manager:
            try:
                saved_language = self.connection_manager.get_config('language', None)
                return saved_language is not None
            except Exception:
                return False
        return False
    
    def _detect_system_language(self):
        """检测系统语言"""
        try:
            system_lang = self._get_system_language()
            if system_lang and system_lang in self.translations:
                self.current_language = system_lang
                self.save_language_setting()
                print(f"检测到系统语言: {system_lang}")
        except Exception as e:
            print(f"系统语言检测失败: {e}")
    
    def _get_system_language(self) -> Optional[str]:
        """获取系统语言"""
        system = platform.system().lower()
        
        if system == "windows":
            return self._get_windows_language()
        elif system == "darwin":  # macOS
            return self._get_macos_language()
        elif system == "linux":
            return self._get_linux_language()
        else:
            return self._get_fallback_language()
    
    def _get_windows_language(self) -> Optional[str]:
        """获取Windows系统语言"""
        try:
            # 方法1: 使用locale模块
            lang, _ = locale.getdefaultlocale()
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法2: 使用环境变量
            lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法3: 使用Windows API (需要ctypes)
            try:
                import ctypes
                windll = ctypes.windll.kernel32
                lang_id = windll.GetUserDefaultUILanguage()
                # 将语言ID转换为语言代码
                if lang_id == 0x804:  # 简体中文
                    return "zh_CN"
                elif lang_id == 0x409:  # 英语(美国)
                    return "en_US"
            except ImportError:
                pass
                
        except Exception as e:
            print(f"Windows语言检测失败: {e}")
        
        return None
    
    def _get_macos_language(self) -> Optional[str]:
        """获取macOS系统语言"""
        try:
            # 方法1: 使用locale模块
            lang, _ = locale.getdefaultlocale()
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法2: 使用环境变量
            lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法3: 读取系统偏好设置
            try:
                import subprocess
                result = subprocess.run(['defaults', 'read', 'NSGlobalDomain', 'AppleLanguages'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    # 解析输出，获取第一个语言代码
                    output = result.stdout.strip()
                    # 简单的解析，实际可能需要更复杂的处理
                    if 'zh' in output.lower():
                        return "zh_CN"
                    elif 'en' in output.lower():
                        return "en_US"
            except Exception:
                pass
                
        except Exception as e:
            print(f"macOS语言检测失败: {e}")
        
        return None
    
    def _get_linux_language(self) -> Optional[str]:
        """获取Linux系统语言"""
        try:
            # 方法1: 使用locale模块
            lang, _ = locale.getdefaultlocale()
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法2: 使用环境变量
            lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
            if lang:
                return self._normalize_language_code(lang)
            
            # 方法3: 读取locale配置文件
            try:
                locale_file = "/etc/default/locale"
                if os.path.exists(locale_file):
                    with open(locale_file, 'r') as f:
                        for line in f:
                            if line.startswith('LANG='):
                                lang = line.split('=')[1].strip().strip('"')
                                return self._normalize_language_code(lang)
            except Exception:
                pass
                
        except Exception as e:
            print(f"Linux语言检测失败: {e}")
        
        return None
    
    def _get_fallback_language(self) -> Optional[str]:
        """获取备用语言检测方法"""
        try:
            # 使用locale模块的通用方法
            lang, _ = locale.getdefaultlocale()
            if lang:
                return self._normalize_language_code(lang)
            
            # 使用环境变量
            lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
            if lang:
                return self._normalize_language_code(lang)
                
        except Exception as e:
            print(f"备用语言检测失败: {e}")
        
        return None
    
    def _normalize_language_code(self, lang_code: str) -> Optional[str]:
        """标准化语言代码"""
        if not lang_code:
            return None
        
        # 转换为小写并移除编码部分
        lang = lang_code.lower().split('.')[0].split('_')[0]
        
        # 映射到支持的语言
        if lang in ['zh', 'zh-cn', 'zh_cn', 'chinese']:
            return "zh_CN"
        elif lang in ['en', 'en-us', 'en_us', 'english']:
            return "en_US"
        
        return None
    
    def get_language_name(self, language_code: str) -> str:
        """获取语言名称"""
        language_names = {
            "zh_CN": "中文",
            "en_US": "English"
        }
        return language_names.get(language_code, language_code)


# 全局实例
_i18n_manager = None


def get_i18n_manager(connection_manager=None) -> I18nManager:
    """获取全局国际化管理器实例"""
    global _i18n_manager
    if _i18n_manager is None:
        _i18n_manager = I18nManager(connection_manager)
    elif connection_manager is not None:
        # 如果提供了新的connection_manager，更新现有实例
        _i18n_manager.connection_manager = connection_manager
        _i18n_manager.load_language_setting()
    return _i18n_manager


def tr(key: str, default: str = None) -> str:
    """翻译文本的便捷函数"""
    return get_i18n_manager().tr(key, default)
