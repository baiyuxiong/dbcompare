"""
简化的图标管理模块
统一处理应用程序图标设置
"""

import os
import sys
import platform
from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow


class IconManager:
    """简化的图标管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_frozen = getattr(sys, 'frozen', False)
        self.base_path = self._get_base_path()
    
    def _get_base_path(self):
        """获取图标文件的基础路径"""
        if self.is_frozen:
            # 打包后的应用程序
            if self.system == "darwin":
                return Path(sys.executable).parent.parent.parent / "Resources"
            else:
                return Path(sys.executable).parent
        else:
            # 开发环境
            return Path(__file__).parent.parent.parent
    
    def get_icon_path(self):
        """获取图标文件路径"""
        # 根据操作系统选择图标文件
        if self.system == "windows":
            icon_names = ['icon.ico', 'icon.png']
        elif self.system == "darwin":
            icon_names = ['icon.icns', 'icon.png']
        else:
            icon_names = ['icon.png', 'icon.ico']
        
        # 查找图标文件
        search_paths = [
            self.base_path,
            Path.cwd(),
        ]
        
        for search_path in search_paths:
            for icon_name in icon_names:
                icon_path = search_path / icon_name
                if icon_path.exists():
                    return str(icon_path)
        
        return None
    
    def setup_icon(self, app, window):
        """统一设置应用和窗口图标"""
        icon_path = self.get_icon_path()
        
        if icon_path:
            try:
                icon = QIcon(icon_path)
                if not icon.isNull():
                    app.setWindowIcon(icon)
                    window.setWindowIcon(icon)
                    
                    # 设置应用信息
                    app.setApplicationName("DBCompare")
                    app.setOrganizationName("DBCompare")
                    
                    # macOS特定设置
                    if self.system == "darwin" and hasattr(window, 'setUnifiedTitleAndToolBarOnMac'):
                        window.setUnifiedTitleAndToolBarOnMac(True)
                    
                    print(f"✓ 图标设置成功: {icon_path}")
                    return True
            except Exception as e:
                print(f"⚠ 图标设置失败: {e}")
        
        # 使用默认图标
        default_icon = app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon)
        app.setWindowIcon(default_icon)
        window.setWindowIcon(default_icon)
        print("⚠ 使用默认系统图标")
        return False


# 全局图标管理器实例
_icon_manager = None

def get_icon_manager():
    """获取全局图标管理器实例"""
    global _icon_manager
    if _icon_manager is None:
        _icon_manager = IconManager()
    return _icon_manager

def setup_application_icon(app):
    """设置应用程序图标（向后兼容）"""
    return True

def setup_window_icon(window):
    """设置窗口图标（向后兼容）"""
    app = QApplication.instance()
    if app:
        icon_manager = get_icon_manager()
        return icon_manager.setup_icon(app, window)
    return False
