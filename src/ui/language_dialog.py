"""
语言设置对话框
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.i18n.i18n_manager import get_i18n_manager, tr


class LanguageDialog(QDialog):
    """语言设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.i18n_manager = get_i18n_manager()
        self.original_language = self.i18n_manager.get_language()
        print("LanguageDialog: original_language",self.original_language)
        
        self.setWindowTitle(tr("language_settings"))
        self.setModal(True)
        self.setGeometry(300, 200, 400, 150)
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
        
        QComboBox {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 6px 12px;
            background: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border: 1px solid #0078d4;
        }
        
        QComboBox:focus {
            border: 2px solid #0078d4;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzY2NjY2NiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            background: white;
            selection-background-color: #e6f3ff;
            selection-color: #202020;
            padding: 8px 0px;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            min-height: 32px;
            margin: 2px 0px;
            line-height: 32px;
        }
        
        QLabel {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            color: #202020;
        }
        """
        
        self.setStyleSheet(style_sheet)
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(tr("language_settings"))
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        # 提示信息
        tip_label = QLabel(tr("language_setting_tip"))
        tip_label.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 10px;")
        tip_label.setWordWrap(True)
        layout.addWidget(tip_label)
        
        # 语言选择
        language_layout = QHBoxLayout()
        language_layout.setSpacing(10)
        
        language_label = QLabel(tr("language"))
        language_layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem(tr("chinese"), "zh_CN")
        self.language_combo.addItem(tr("english"), "en_US")
        
        # 设置当前语言
        current_language = self.i18n_manager.get_language()
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_language:
                self.language_combo.setCurrentIndex(i)
                break
        
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        
        layout.addLayout(language_layout)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        apply_btn = QPushButton(tr("apply"))
        apply_btn.setObjectName("primary")
        apply_btn.clicked.connect(self.apply_language)
        btn_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def apply_language(self):
        """应用语言设置"""
        selected_language = self.language_combo.currentData()
        
        if selected_language != self.original_language:
            # 设置新语言
            self.i18n_manager.set_language(selected_language)
            
            # 显示成功提示
            QMessageBox.information(
                self,
                tr("info"),
                tr("language_setting_saved")
            )
            
            # 关闭对话框
            self.accept()
        else:
            self.accept()
    
    # 移除 restart_application 方法
