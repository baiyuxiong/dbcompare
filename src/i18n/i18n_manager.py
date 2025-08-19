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
        self.connection_manager = connection_manager
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_language = "zh_CN"  # 默认中文
        
        # 加载翻译文件
        self.load_translations()
        
        # 初始化语言设置
        self._init_language_setting()
    
    def load_translations(self):
        """加载翻译文件"""
        i18n_dir = self._get_i18n_directory()
        
        # 加载所有可用的语言文件
        for lang_file in i18n_dir.glob("*.json"):
            lang_code = lang_file.stem  # 获取文件名（不含扩展名）
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
                print(f"✓ 加载翻译文件: {lang_file}")
            except Exception as e:
                print(f"✗ 加载翻译文件失败 {lang_file}: {e}")
    
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
    
    def _init_language_setting(self):
        """初始化语言设置"""
        # 首先尝试从配置中加载保存的语言设置
        saved_language = self._load_saved_language()
        print("I18nManager: _init_language_setting: saved_language",saved_language)
        
        if saved_language and saved_language in self.translations:
            # 如果有保存的语言设置且该语言可用，使用保存的设置
            self.current_language = saved_language
            print(f"使用保存的语言设置: {saved_language}")
        else:
            # 否则检测系统语言
            system_language = self._detect_system_language()
            if system_language in self.translations:
                self.current_language = system_language
                print(f"检测到系统语言: {system_language}")
            else:
                # 如果系统语言不支持，默认使用英文
                self.current_language = "en_US"
                print("系统语言不支持，使用默认英文")
            
            # 保存检测到的语言设置
            self._save_language_setting(self.current_language)
    
    def _load_saved_language(self) -> Optional[str]:
        """从配置中加载保存的语言设置"""
        if self.connection_manager:
            try:
                return self.connection_manager.get_config('language', None)
            except Exception as e:
                print(f"加载保存的语言设置失败: {e}")
        return None
    
    def _save_language_setting(self, language: str):
        """保存语言设置到配置"""
        if self.connection_manager:
            try:
                self.connection_manager.set_config('language', language)
            except Exception as e:
                print(f"保存语言设置失败: {e}")
        else:
            print("connection_manager is None")
    
    def _detect_system_language(self) -> str:
        """检测系统语言，简化逻辑：只返回中文或英文"""
        try:
            # 获取系统语言
            system_lang = self._get_system_language_code()
            
            # 判断是否为中文
            if system_lang and self._is_chinese_language(system_lang):
                return "zh_CN"
            else:
                return "en_US"
                
        except Exception as e:
            print(f"系统语言检测失败: {e}")
            return "en_US"  # 默认英文
    
    def _get_system_language_code(self) -> Optional[str]:
        """获取系统语言代码"""
        try:
            # 方法1: 使用locale模块
            lang, _ = locale.getdefaultlocale()
            if lang:
                return lang
            
            # 方法2: 使用环境变量
            lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
            if lang:
                return lang
            
            # 方法3: 平台特定的检测
            system = platform.system().lower()
            if system == "windows":
                return self._get_windows_language()
            elif system == "darwin":  # macOS
                return self._get_macos_language()
            elif system == "linux":
                return self._get_linux_language()
                
        except Exception as e:
            print(f"获取系统语言代码失败: {e}")
        
        return None
    
    def _is_chinese_language(self, lang_code: str) -> bool:
        """判断是否为中文语言"""
        if not lang_code:
            return False
        
        # 转换为小写并移除编码部分
        lang = lang_code.lower().split('.')[0].split('_')[0]
        
        # 中文语言代码列表
        chinese_codes = ['zh', 'zh-cn', 'zh_cn', 'zh-tw', 'zh_tw', 'zh-hk', 'zh_hk', 'chinese']
        
        return lang in chinese_codes
    
    def _get_windows_language(self) -> Optional[str]:
        """获取Windows系统语言"""
        try:
            import ctypes
            windll = ctypes.windll.kernel32
            lang_id = windll.GetUserDefaultUILanguage()
            
            # 将语言ID转换为语言代码
            if lang_id == 0x804:  # 简体中文
                return "zh_CN"
            elif lang_id == 0x404:  # 繁体中文
                return "zh_TW"
            elif lang_id == 0x409:  # 英语(美国)
                return "en_US"
        except ImportError:
            pass
        
        return None
    
    def _get_macos_language(self) -> Optional[str]:
        """获取macOS系统语言"""
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', 'NSGlobalDomain', 'AppleLanguages'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                if 'zh' in output.lower():
                    return "zh_CN"
                elif 'en' in output.lower():
                    return "en_US"
        except Exception:
            pass
        
        return None
    
    def _get_linux_language(self) -> Optional[str]:
        """获取Linux系统语言"""
        try:
            # 读取locale配置文件
            locale_file = "/etc/default/locale"
            if os.path.exists(locale_file):
                with open(locale_file, 'r') as f:
                    for line in f:
                        if line.startswith('LANG='):
                            lang = line.split('=')[1].strip().strip('"')
                            return lang
        except Exception:
            pass
        
        return None
    
    def set_language(self, language: str):
        """设置当前语言"""
        if language in self.translations:
            self.current_language = language
            self._save_language_setting(language)
            print(f"语言已设置为: {language}")
        else:
            print(f"不支持的语言: {language}")
    
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
    else:
        # 如果传入了新的connection_manager，更新现有实例
        if connection_manager and _i18n_manager.connection_manager != connection_manager:
            _i18n_manager.connection_manager = connection_manager
    return _i18n_manager


def tr(key: str, default: str = None) -> str:
    """翻译文本的便捷函数"""
    return get_i18n_manager().tr(key, default)
