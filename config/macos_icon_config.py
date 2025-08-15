"""
macOS平台图标配置
"""

import os
import subprocess
from pathlib import Path


class MacOSIconConfig:
    """macOS图标配置管理器"""
    
    def __init__(self, app_name, icon_path):
        """
        初始化macOS图标配置
        
        Args:
            app_name: 应用程序名称
            icon_path: 图标文件路径
        """
        self.app_name = app_name
        self.icon_path = Path(icon_path).resolve()
        self.app_bundle_path = f"/Applications/{app_name}.app"
    
    def create_app_bundle(self, executable_path, bundle_path=None):
        """
        创建应用程序包（.app）
        
        Args:
            executable_path: 可执行文件路径
            bundle_path: 应用程序包路径（可选）
        """
        if bundle_path is None:
            bundle_path = self.app_bundle_path
        
        try:
            # 创建应用程序包结构
            bundle_path = Path(bundle_path)
            contents_path = bundle_path / "Contents"
            macos_path = contents_path / "MacOS"
            resources_path = contents_path / "Resources"
            
            # 创建目录结构
            macos_path.mkdir(parents=True, exist_ok=True)
            resources_path.mkdir(parents=True, exist_ok=True)
            
            # 复制可执行文件
            import shutil
            shutil.copy2(executable_path, macos_path / f"{self.app_name}")
            
            # 复制图标文件
            icon_dest = resources_path / "icon.icns"
            if self.icon_path.suffix.lower() == '.icns':
                shutil.copy2(self.icon_path, icon_dest)
            else:
                # 转换图标格式为.icns
                self._convert_to_icns(self.icon_path, icon_dest)
            
            # 创建Info.plist文件
            self._create_info_plist(contents_path)
            
            print(f"✓ macOS应用程序包创建成功: {bundle_path}")
            return True
            
        except Exception as e:
            print(f"⚠ macOS应用程序包创建失败: {e}")
            return False
    
    def _convert_to_icns(self, source_path, dest_path):
        """
        转换图标为.icns格式
        
        Args:
            source_path: 源图标文件路径
            dest_path: 目标.icns文件路径
        """
        try:
            # 使用sips命令转换图标
            cmd = [
                'sips', '-s', 'format', 'icns', 
                str(source_path), '--out', str(dest_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ 图标转换成功: {dest_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠ 图标转换失败: {e}")
            # 如果转换失败，直接复制原文件
            import shutil
            shutil.copy2(source_path, dest_path)
    
    def _create_info_plist(self, contents_path):
        """
        创建Info.plist文件
        
        Args:
            contents_path: Contents目录路径
        """
        info_plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{self.app_name}</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.dbcompare.{self.app_name.lower()}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
        
        info_plist_path = contents_path / "Info.plist"
        with open(info_plist_path, 'w', encoding='utf-8') as f:
            f.write(info_plist_content)
        
        print(f"✓ Info.plist创建成功: {info_plist_path}")
    
    def set_dock_icon(self, window):
        """
        设置Dock图标
        
        Args:
            window: PyQt窗口对象
        """
        try:
            # 设置窗口图标
            from PyQt6.QtGui import QIcon
            icon = QIcon(str(self.icon_path))
            window.setWindowIcon(icon)
            
            # 设置macOS特定属性
            if hasattr(window, 'setUnifiedTitleAndToolBarOnMac'):
                window.setUnifiedTitleAndToolBarOnMac(True)
            
            print("✓ macOS Dock图标设置成功")
            return True
            
        except Exception as e:
            print(f"⚠ macOS Dock图标设置失败: {e}")
            return False
    
    def install_to_applications(self, source_path):
        """
        安装到Applications文件夹
        
        Args:
            source_path: 源应用程序包路径
        """
        try:
            import shutil
            
            # 复制到Applications文件夹
            dest_path = Path(self.app_bundle_path)
            if dest_path.exists():
                shutil.rmtree(dest_path)
            
            shutil.copytree(source_path, dest_path)
            
            # 设置权限
            subprocess.run(['chmod', '+x', str(dest_path / "Contents" / "MacOS" / self.app_name)], check=True)
            
            print(f"✓ 应用程序安装成功: {dest_path}")
            return True
            
        except Exception as e:
            print(f"⚠ 应用程序安装失败: {e}")
            return False


def setup_macos_icon(app_name, icon_path, window=None):
    """
    便捷函数：设置macOS图标
    
    Args:
        app_name: 应用程序名称
        icon_path: 图标文件路径
        window: PyQt窗口对象（可选）
    """
    config = MacOSIconConfig(app_name, icon_path)
    
    # 如果提供了窗口对象，设置Dock图标
    if window:
        config.set_dock_icon(window)
    
    return config
