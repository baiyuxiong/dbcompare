"""
Windows平台图标配置
"""

import os
import winreg
from pathlib import Path


class WindowsIconConfig:
    """Windows图标配置管理器"""
    
    def __init__(self, app_name, icon_path):
        """
        初始化Windows图标配置
        
        Args:
            app_name: 应用程序名称
            icon_path: 图标文件路径
        """
        self.app_name = app_name
        self.icon_path = Path(icon_path).resolve()
        self.registry_key = f"Software\\Classes\\{app_name}"
    
    def register_app_icon(self):
        """注册应用程序图标到Windows注册表"""
        try:
            # 创建注册表项
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_key) as key:
                # 设置默认图标
                winreg.SetValueEx(key, "DefaultIcon", 0, winreg.REG_SZ, str(self.icon_path))
                
                # 设置应用程序信息
                winreg.SetValueEx(key, "FriendlyAppName", 0, winreg.REG_SZ, self.app_name)
                
            print(f"✓ Windows图标注册成功: {self.registry_key}")
            return True
            
        except Exception as e:
            print(f"⚠ Windows图标注册失败: {e}")
            return False
    
    def unregister_app_icon(self):
        """从Windows注册表注销应用程序图标"""
        try:
            # 删除注册表项
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.registry_key)
            print(f"✓ Windows图标注销成功: {self.registry_key}")
            return True
            
        except Exception as e:
            print(f"⚠ Windows图标注销失败: {e}")
            return False
    
    def create_shortcut_with_icon(self, shortcut_path, target_path, description=""):
        """
        创建带图标的快捷方式
        
        Args:
            shortcut_path: 快捷方式文件路径
            target_path: 目标文件路径
            description: 描述信息
        """
        try:
            import win32com.client
            
            # 创建Shell对象
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # 创建快捷方式
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.IconLocation = str(self.icon_path)
            shortcut.Description = description
            shortcut.save()
            
            print(f"✓ 快捷方式创建成功: {shortcut_path}")
            return True
            
        except ImportError:
            print("⚠ 需要安装 pywin32 库来创建快捷方式")
            return False
        except Exception as e:
            print(f"⚠ 创建快捷方式失败: {e}")
            return False
    
    def set_taskbar_icon(self, window):
        """
        设置任务栏图标
        
        Args:
            window: PyQt窗口对象
        """
        try:
            # 设置窗口图标
            from PyQt6.QtGui import QIcon
            icon = QIcon(str(self.icon_path))
            window.setWindowIcon(icon)
            
            # 设置窗口属性以确保图标在任务栏中正确显示
            from PyQt6.QtCore import Qt
            window.setWindowFlags(window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            
            print("✓ Windows任务栏图标设置成功")
            return True
            
        except Exception as e:
            print(f"⚠ Windows任务栏图标设置失败: {e}")
            return False


def setup_windows_icon(app_name, icon_path, window=None):
    """
    便捷函数：设置Windows图标
    
    Args:
        app_name: 应用程序名称
        icon_path: 图标文件路径
        window: PyQt窗口对象（可选）
    """
    config = WindowsIconConfig(app_name, icon_path)
    
    # 注册图标
    config.register_app_icon()
    
    # 如果提供了窗口对象，设置任务栏图标
    if window:
        config.set_taskbar_icon(window)
    
    return config
