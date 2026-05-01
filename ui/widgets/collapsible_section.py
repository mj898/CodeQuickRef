"""
CollapsibleSection — 可折叠/展开的详情区块
带标题栏、展开/折叠箭头、内容区域
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer


class CollapsibleSection(QWidget):
    """可折叠区块组件"""
    def __init__(self, title="", content_widget=None, expanded=True, parent=None):
        super().__init__(parent)
        self._expanded = expanded
        self._animation_duration = 150

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # 标题栏
        self._toggle_btn = QLabel()
        self._toggle_btn.setText(f"{'▼' if expanded else '▶'} {title}")
        self._toggle_btn.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #e0e0e0;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel:hover {
                background-color: #3a3a3a;
            }
        """)
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.mousePressEvent = lambda e: self.toggle()
        self._layout.addWidget(self._toggle_btn)

        # 内容区域
        self._content = content_widget or QWidget()
        self._content.setStyleSheet("""
            QWidget { background-color: #1e1e1e; }
        """)
        self._content.setVisible(expanded)
        self._layout.addWidget(self._content)

    def toggle(self):
        self._expanded = not self._expanded
        self._content.setVisible(self._expanded)
        arrow = '▼' if self._expanded else '▶'
        title = self._toggle_btn.text().split(' ', 1)
        if len(title) > 1:
            self._toggle_btn.setText(f"{arrow} {title[1]}")
        else:
            self._toggle_btn.setText(f"{arrow} ")

    def set_expanded(self, expanded):
        if expanded != self._expanded:
            self.toggle()

    @property
    def content_widget(self):
        return self._content
