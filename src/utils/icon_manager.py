"""
图标管理模块
处理应用程序图标设置，包括窗口图标和任务栏图标
"""

import os
import platform
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

# 导入平台特定的图标配置
try:
    from config.windows_icon_config import setup_windows_icon
except ImportError:
    setup_windows_icon = None

try:
    from config.macos_icon_config import setup_macos_icon
except ImportError:
    setup_macos_icon = None

try:
    from config.linux_icon_config import setup_linux_icon
except ImportError:
    setup_linux_icon = None


class IconManager:
    """图标管理器"""
    
    def __init__(self, project_root=None):
        """
        初始化图标管理器
        
        Args:
            project_root: 项目根目录路径，如果为None则自动检测
        """
        if project_root is None:
            # 自动检测项目根目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.project_root = project_root
        self.system = platform.system().lower()
    
    def get_icon_paths(self):
        """获取图标文件路径列表，按优先级排序"""
        icon_paths = []
        
        # 根据操作系统选择最优的图标格式
        if self.system == "windows":
            # Windows优先使用ICO格式
            icon_paths.extend([
                os.path.join(self.project_root, 'icon.ico'),
                os.path.join(self.project_root, 'icon.png'),
                os.path.join(self.project_root, 'icon.svg'),
            ])
        elif self.system == "darwin":
            # macOS优先使用PNG格式
            icon_paths.extend([
                os.path.join(self.project_root, 'icon.png'),
                os.path.join(self.project_root, 'icon.ico'),
                os.path.join(self.project_root, 'icon.svg'),
            ])
        else:
            # Linux和其他系统
            icon_paths.extend([
                os.path.join(self.project_root, 'icon.png'),
                os.path.join(self.project_root, 'icon.svg'),
                os.path.join(self.project_root, 'icon.ico'),
            ])
        
        return icon_paths
    
    def load_icon(self):
        """加载图标"""
        icon_paths = self.get_icon_paths()
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    icon = QIcon(icon_path)
                    if not icon.isNull():
                        print(f"✓ 成功加载图标: {icon_path}")
                        return icon
                except Exception as e:
                    print(f"⚠ 加载图标失败 {icon_path}: {e}")
                    continue
        
        # 如果所有自定义图标都加载失败，返回None
        print("⚠ 无法加载自定义图标")
        return None
    
    def set_application_icon(self, app):
        """
        为应用程序设置图标
        
        Args:
            app: QApplication实例
        """
        icon = self.load_icon()
        if icon:
            app.setWindowIcon(icon)
        else:
            # 使用默认系统图标
            default_icon = app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon)
            app.setWindowIcon(default_icon)
            print("⚠ 使用默认系统应用图标")
    
    def set_window_icon(self, window):
        """
        为窗口设置图标
        
        Args:
            window: QMainWindow实例
        """
        icon = self.load_icon()
        if icon:
            window.setWindowIcon(icon)
        else:
            # 使用默认系统图标
            default_icon = window.style().standardIcon(window.style().StandardPixmap.SP_ComputerIcon)
            window.setWindowIcon(default_icon)
            print("⚠ 使用默认系统窗口图标")
    
    def setup_taskbar_icon(self, window):
        """
        设置任务栏图标（平台特定）
        
        Args:
            window: QMainWindow实例
        """
        # 获取当前窗口图标
        current_icon = window.windowIcon()
        if current_icon.isNull():
            return
        
        # 使用平台特定的图标设置
        if self.system == "windows" and setup_windows_icon:
            self._setup_windows_taskbar_icon_advanced(window)
        elif self.system == "darwin" and setup_macos_icon:
            self._setup_macos_dock_icon_advanced(window)
        elif self.system == "linux" and setup_linux_icon:
            self._setup_linux_taskbar_icon_advanced(window)
        else:
            # 使用基本设置
            if self.system == "windows":
                self._setup_windows_taskbar_icon(window, current_icon)
            elif self.system == "darwin":
                self._setup_macos_dock_icon(window, current_icon)
            else:
                self._setup_linux_taskbar_icon(window, current_icon)
    
    def _setup_windows_taskbar_icon(self, window, icon):
        """设置Windows任务栏图标"""
        try:
            # 在Windows上，设置窗口图标通常会自动应用到任务栏
            # 但我们可以尝试一些额外的设置来确保图标正确显示
            window.setWindowIcon(icon)
            
            # 设置窗口属性以确保图标在任务栏中正确显示
            window.setWindowFlags(window.windowFlags() | 0x00000001)  # Qt.WindowStaysOnTopHint
            
            print("✓ Windows任务栏图标已设置")
        except Exception as e:
            print(f"⚠ 设置Windows任务栏图标失败: {e}")
    
    def _setup_macos_dock_icon(self, window, icon):
        """设置macOS Dock图标"""
        try:
            # 在macOS上，设置窗口图标通常会自动应用到Dock
            window.setWindowIcon(icon)
            
            # 可以尝试设置一些macOS特定的属性
            if hasattr(window, 'setUnifiedTitleAndToolBarOnMac'):
                window.setUnifiedTitleAndToolBarOnMac(True)
            
            print("✓ macOS Dock图标已设置")
        except Exception as e:
            print(f"⚠ 设置macOS Dock图标失败: {e}")
    
    def _setup_linux_taskbar_icon(self, window, icon):
        """设置Linux任务栏图标"""
        try:
            # 在Linux上，设置窗口图标通常会自动应用到任务栏
            window.setWindowIcon(icon)
            
            # 可以尝试设置一些Linux特定的属性
            # 例如设置窗口类名等
            
            print("✓ Linux任务栏图标已设置")
        except Exception as e:
            print(f"⚠ 设置Linux任务栏图标失败: {e}")
    
    def _setup_windows_taskbar_icon_advanced(self, window):
        """使用高级Windows图标设置"""
        try:
            # 获取应用程序名称
            app_name = "DBCompare"
            icon_paths = self.get_icon_paths()
            if icon_paths:
                # 使用平台特定的设置
                setup_windows_icon(app_name, str(icon_paths[0]), window)
            else:
                print("⚠ 无法加载图标文件，使用基本设置")
                self._setup_windows_taskbar_icon(window, window.windowIcon())
        except Exception as e:
            print(f"⚠ 高级Windows图标设置失败: {e}")
            # 回退到基本设置
            self._setup_windows_taskbar_icon(window, window.windowIcon())
    
    def _setup_macos_dock_icon_advanced(self, window):
        """使用高级macOS图标设置"""
        try:
            # 获取应用程序名称
            app_name = "DBCompare"
            icon_paths = self.get_icon_paths()
            if icon_paths:
                # 使用平台特定的设置
                setup_macos_icon(app_name, str(icon_paths[0]), window)
            else:
                print("⚠ 无法加载图标文件，使用基本设置")
                self._setup_macos_dock_icon(window, window.windowIcon())
        except Exception as e:
            print(f"⚠ 高级macOS图标设置失败: {e}")
            # 回退到基本设置
            self._setup_macos_dock_icon(window, window.windowIcon())
    
    def _setup_linux_taskbar_icon_advanced(self, window):
        """使用高级Linux图标设置"""
        try:
            # 获取应用程序名称
            app_name = "DBCompare"
            icon_paths = self.get_icon_paths()
            if icon_paths:
                # 使用平台特定的设置
                setup_linux_icon(app_name, str(icon_paths[0]), window)
            else:
                print("⚠ 无法加载图标文件，使用基本设置")
                self._setup_linux_taskbar_icon(window, window.windowIcon())
        except Exception as e:
            print(f"⚠ 高级Linux图标设置失败: {e}")
            # 回退到基本设置
            self._setup_linux_taskbar_icon(window, window.windowIcon())


def setup_application_icon(app):
    """
    便捷函数：为应用程序设置图标
    
    Args:
        app: QApplication实例
    """
    icon_manager = IconManager()
    icon_manager.set_application_icon(app)


def setup_window_icon(window):
    """
    便捷函数：为窗口设置图标
    
    Args:
        window: QMainWindow实例
    """
    icon_manager = IconManager()
    icon_manager.set_window_icon(window)
    icon_manager.setup_taskbar_icon(window)
