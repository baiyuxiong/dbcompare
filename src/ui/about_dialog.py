"""
关于对话框
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QApplication, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

from src.i18n.i18n_manager import get_i18n_manager, tr


class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.i18n_manager = get_i18n_manager()
        
        self.setWindowTitle(tr("about"))
        self.setModal(True)
        self.setGeometry(300, 200, 550, 500)
        self.setFixedSize(550, 500)  # 增加对话框大小
        self.center_on_screen()
        
        # 应用Windows 11风格样式
        self.apply_windows11_style()
        
        self.setup_ui()
    
    def center_on_screen(self):
        """将对话框居中显示在屏幕上"""
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            screen_geometry = screen.availableGeometry()
            dialog_geometry = self.geometry()
            x = (screen_geometry.width() - dialog_geometry.width()) // 2
            y = (screen_geometry.height() - dialog_geometry.height()) // 2
            self.move(x, y)
    
    def apply_windows11_style(self):
        """应用Windows 11风格样式"""
        style_sheet = """
        QDialog {
            background-color: #fafafa;
            color: #202020;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f8f8);
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px 16px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: #202020;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f8ff, stop:1 #e6f3ff);
            border: 1px solid #0078d4;
            color: #0078d4;
        }
        
        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #106ebe);
            border: 1px solid #0078d4;
            color: white;
            font-weight: 600;
        }
        
        QPushButton#primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #106ebe, stop:1 #005a9e);
            border: 1px solid #106ebe;
        }
        
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        
        QLabel#title {
            font-size: 18px;
            font-weight: bold;
            color: #0078d4;
        }
        
        QLabel#subtitle {
            font-size: 14px;
            font-weight: 600;
            color: #333;
        }
        
        QLabel#link {
            color: #0078d4;
            text-decoration: underline;
        }
        
        QLabel#link:hover {
            color: #106ebe;
        }
        
        QTextEdit {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
            background: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
            color: #202020;
            read-only: true;
        }
        
        QFrame#separator {
            background-color: #e0e0e0;
            border: none;
        }
        """
        
        self.setStyleSheet(style_sheet)
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 应用标题
        title_label = QLabel(tr("about_title"))
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 版本信息
        version_label = QLabel(tr("about_version"))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(version_label)
        
        
        # 公司信息
        company_label = QLabel(tr("about_company"))
        company_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        company_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(company_label)
        
        # 网站链接
        website_label = QLabel(tr("about_website"))
        website_label.setObjectName("link")
        website_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        website_label.setCursor(Qt.CursorShape.PointingHandCursor)
        website_label.mousePressEvent = lambda event: self.open_website()
        layout.addWidget(website_label)
        
        # 邮箱链接
        email_label = QLabel(tr("about_email"))
        email_label.setObjectName("link")
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        email_label.setCursor(Qt.CursorShape.PointingHandCursor)
        email_label.mousePressEvent = lambda event: self.open_email()
        layout.addWidget(email_label)
        
        # 分隔线
        separator3 = QFrame()
        separator3.setObjectName("separator")
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFixedHeight(1)
        layout.addWidget(separator3)
        
        # 版权信息
        copyright_label = QLabel(tr("about_copyright"))
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(copyright_label)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton(tr("about_close"))
        close_btn.setObjectName("primary")
        close_btn.clicked.connect(self.accept)
        close_btn.setFixedWidth(80)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def open_website(self):
        """打开网站"""
        QDesktopServices.openUrl(QUrl("https://lifang.biz"))
    
    def open_email(self):
        """打开邮箱"""
        QDesktopServices.openUrl(QUrl("mailto:i@lifang.biz")) 