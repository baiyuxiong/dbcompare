"""
国际化管理器
负责语言切换和文本翻译
"""

import json
import os
import locale
import platform
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
        # 获取当前文件所在目录
        current_dir = Path(__file__).parent
        
        # 加载中文翻译
        zh_file = current_dir / "zh_CN.json"
        if zh_file.exists():
            with open(zh_file, 'r', encoding='utf-8') as f:
                self.translations["zh_CN"] = json.load(f)
        
        # 加载英文翻译
        en_file = current_dir / "en_US.json"
        if en_file.exists():
            with open(en_file, 'r', encoding='utf-8') as f:
                self.translations["en_US"] = json.load(f)
    
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
