"""
Linux平台图标配置
"""

import os
import subprocess
from pathlib import Path


class LinuxIconConfig:
    """Linux图标配置管理器"""
    
    def __init__(self, app_name, icon_path):
        """
        初始化Linux图标配置
        
        Args:
            app_name: 应用程序名称
            icon_path: 图标文件路径
        """
        self.app_name = app_name
        self.icon_path = Path(icon_path).resolve()
        self.desktop_file_name = f"{app_name.lower()}.desktop"
    
    def create_desktop_file(self, executable_path, desktop_dir=None):
        """
        创建桌面文件（.desktop）
        
        Args:
            executable_path: 可执行文件路径
            desktop_dir: 桌面文件目录（可选）
        """
        if desktop_dir is None:
            # 尝试多个可能的桌面文件目录
            possible_dirs = [
                os.path.expanduser("~/.local/share/applications"),
                "/usr/local/share/applications",
                "/usr/share/applications"
            ]
            
            for dir_path in possible_dirs:
                if os.path.exists(dir_path) and os.access(dir_path, os.W_OK):
                    desktop_dir = dir_path
                    break
            else:
                # 如果都不可写，使用用户目录
                desktop_dir = os.path.expanduser("~/.local/share/applications")
        
        try:
            # 确保目录存在
            os.makedirs(desktop_dir, exist_ok=True)
            
            # 创建桌面文件内容
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={self.app_name}
Comment=MySQL表结构比较工具
Exec={executable_path}
Icon={self.icon_path}
Terminal=false
Categories=Development;Database;
Keywords=database;mysql;compare;structure;
StartupWMClass={self.app_name}
"""
            
            # 写入桌面文件
            desktop_file_path = os.path.join(desktop_dir, self.desktop_file_name)
            with open(desktop_file_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)
            
            # 设置执行权限
            os.chmod(desktop_file_path, 0o755)
            
            print(f"✓ Linux桌面文件创建成功: {desktop_file_path}")
            return True
            
        except Exception as e:
            print(f"⚠ Linux桌面文件创建失败: {e}")
            return False
    
    def install_icon_to_system(self, icon_size="256"):
        """
        安装图标到系统图标目录
        
        Args:
            icon_size: 图标尺寸（如"16", "32", "48", "64", "128", "256"）
        """
        try:
            # 系统图标目录
            icon_dirs = [
                os.path.expanduser(f"~/.local/share/icons/hicolor/{icon_size}x{icon_size}/apps"),
                f"/usr/local/share/icons/hicolor/{icon_size}x{icon_size}/apps",
                f"/usr/share/icons/hicolor/{icon_size}x{icon_size}/apps"
            ]
            
            icon_installed = False
            for icon_dir in icon_dirs:
                if os.path.exists(icon_dir) or os.access(os.path.dirname(icon_dir), os.W_OK):
                    try:
                        os.makedirs(icon_dir, exist_ok=True)
                        icon_dest = os.path.join(icon_dir, f"{self.app_name.lower()}.png")
                        
                        # 复制图标文件
                        import shutil
                        shutil.copy2(self.icon_path, icon_dest)
                        
                        print(f"✓ 系统图标安装成功: {icon_dest}")
                        icon_installed = True
                        break
                        
                    except Exception as e:
                        print(f"⚠ 安装到 {icon_dir} 失败: {e}")
                        continue
            
            if not icon_installed:
                print("⚠ 无法安装系统图标，所有目录都不可写")
                return False
            
            return True
            
        except Exception as e:
            print(f"⚠ 系统图标安装失败: {e}")
            return False
    
    def update_icon_cache(self):
        """更新图标缓存"""
        try:
            # 尝试更新图标缓存
            subprocess.run(['gtk-update-icon-cache', '-f', '-t'], 
                         check=True, capture_output=True)
            print("✓ 图标缓存更新成功")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠ 图标缓存更新失败或gtk-update-icon-cache不可用")
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
            
            # 设置窗口类名（用于任务栏识别）
            window.setWindowTitle(self.app_name)
            
            print("✓ Linux任务栏图标设置成功")
            return True
            
        except Exception as e:
            print(f"⚠ Linux任务栏图标设置失败: {e}")
            return False
    
    def create_menu_entry(self, executable_path, menu_dir=None):
        """
        创建菜单项
        
        Args:
            executable_path: 可执行文件路径
            menu_dir: 菜单目录（可选）
        """
        if menu_dir is None:
            menu_dir = os.path.expanduser("~/.local/share/applications")
        
        return self.create_desktop_file(executable_path, menu_dir)
    
    def uninstall(self):
        """卸载应用程序图标"""
        try:
            # 删除桌面文件
            desktop_dirs = [
                os.path.expanduser("~/.local/share/applications"),
                "/usr/local/share/applications",
                "/usr/share/applications"
            ]
            
            for desktop_dir in desktop_dirs:
                desktop_file = os.path.join(desktop_dir, self.desktop_file_name)
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)
                    print(f"✓ 桌面文件删除成功: {desktop_file}")
            
            # 删除系统图标
            icon_sizes = ["16", "32", "48", "64", "128", "256"]
            for size in icon_sizes:
                icon_dirs = [
                    os.path.expanduser(f"~/.local/share/icons/hicolor/{size}x{size}/apps"),
                    f"/usr/local/share/icons/hicolor/{size}x{size}/apps",
                    f"/usr/share/icons/hicolor/{size}x{size}/apps"
                ]
                
                for icon_dir in icon_dirs:
                    icon_file = os.path.join(icon_dir, f"{self.app_name.lower()}.png")
                    if os.path.exists(icon_file):
                        os.remove(icon_file)
                        print(f"✓ 系统图标删除成功: {icon_file}")
            
            # 更新图标缓存
            self.update_icon_cache()
            
            print("✓ 应用程序图标卸载完成")
            return True
            
        except Exception as e:
            print(f"⚠ 应用程序图标卸载失败: {e}")
            return False


def setup_linux_icon(app_name, icon_path, window=None, executable_path=None):
    """
    便捷函数：设置Linux图标
    
    Args:
        app_name: 应用程序名称
        icon_path: 图标文件路径
        window: PyQt窗口对象（可选）
        executable_path: 可执行文件路径（可选，用于创建桌面文件）
    """
    config = LinuxIconConfig(app_name, icon_path)
    
    # 安装系统图标
    config.install_icon_to_system()
    
    # 创建桌面文件
    if executable_path:
        config.create_desktop_file(executable_path)
    
    # 如果提供了窗口对象，设置任务栏图标
    if window:
        config.set_taskbar_icon(window)
    
    return config
