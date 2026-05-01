#!/usr/bin/env python3
"""
CodeQuickRef — 个人多语言代码速查工具（新手版）
入口文件
"""
import sys, os

# 确保项目目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow


def main():
    # 高 DPI 适配
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough  # type: ignore
    )

    app = QApplication(sys.argv)
    app.setApplicationName("CodeQuickRef")
    app.setOrganizationName("CodeQuickRef")

    # 默认字体
    font = QFont("Microsoft YaHei", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    # 延迟导入以解决循环依赖
    from PySide6.QtCore import Qt
    main()
