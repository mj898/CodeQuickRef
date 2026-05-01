"""
DetailWidget — 条目详情面板（右侧）
支持三类条目：command / code / pattern
以折叠布局展示所有字段
"""
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QTextEdit, QApplication, QMessageBox, QMenu,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QTextOption

from .collapsible_section import CollapsibleSection


class ClickableLabel(QLabel):
    """可点击标签，hover 显示提示"""
    def __init__(self, text="", tooltip=""):
        super().__init__(text)
        if tooltip:
            self.setToolTip(tooltip)
        self.setCursor(Qt.WhatsThisCursor)


class DetailWidget(QWidget):
    """条目详情展示面板"""
    favorite_toggled = Signal(str, int)  # (item_type, item_id)
    deleted = Signal(str, int)
    edit_requested = Signal(object)      # 条目数据 dict

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_item = None
        self._current_type = None
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QWidget#detailPanel {
                background-color: #1e1e1e;
                border-left: 1px solid #333;
            }
            QLabel#itemTitle {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                padding: 4px 0;
            }
            QLabel#itemSubtitle {
                font-size: 13px;
                color: #888;
            }
            QLabel#sectionContent {
                color: #d4d4d4;
                font-size: 13px;
                padding: 8px 12px;
                background-color: #252525;
                border-radius: 4px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QPushButton#actionBtn {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 13px;
                min-width: 36px;
            }
            QPushButton#actionBtn:hover {
                background-color: #4a4a4a;
            }
            QPushButton#actionBtn:pressed {
                background-color: #555;
            }
            QPushButton#favBtn {
                background-color: #3a3a3a;
                color: #f0c040;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 15px;
                min-width: 36px;
            }
            QPushButton#favBtn:hover {
                background-color: #4a4a4a;
            }
            QPushButton#deleteBtn {
                background-color: #5c2a2a;
                color: #ff6b6b;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 13px;
            }
            QPushButton#deleteBtn:hover {
                background-color: #7a3a3a;
            }
            QLabel#emptyHint {
                color: #666;
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 空状态
        self._empty_label = QLabel("← 左侧选择一个条目查看详情\n\n💡 提示：按 Ctrl+F 快速搜索")
        self._empty_label.setObjectName("emptyHint")
        self._empty_label.setAlignment(Qt.AlignCenter)
        self._empty_label.setStyleSheet("color: #666; font-size: 16px; padding: 80px;")
        layout.addWidget(self._empty_label)

        # 主要详情区域（默认隐藏）
        self._detail_scroll = QScrollArea()
        self._detail_scroll.setWidgetResizable(True)
        self._detail_scroll.setFrameShape(QFrame.NoFrame)
        self._detail_scroll.setStyleSheet("QScrollArea { background-color: #1e1e1e; border: none; }")
        self._detail_scroll.setVisible(False)

        self._detail_container = QWidget()
        self._detail_container.setObjectName("detailPanel")
        self._detail_layout = QVBoxLayout(self._detail_container)
        self._detail_layout.setContentsMargins(16, 12, 16, 12)
        self._detail_layout.setSpacing(8)
        self._detail_scroll.setWidget(self._detail_container)

        # 顶部操作栏
        self._build_action_bar()

        # 标题区
        self._title_label = QLabel()
        self._title_label.setObjectName("itemTitle")
        self._title_label.setWordWrap(True)
        self._detail_layout.addWidget(self._title_label)

        self._subtitle_label = QLabel()
        self._subtitle_label.setObjectName("itemSubtitle")
        self._detail_layout.addWidget(self._subtitle_label)

        self._func_label = QLabel()
        self._func_label.setWordWrap(True)
        self._func_label.setStyleSheet("color: #b0b0b0; font-size: 14px; padding: 4px 0 12px 0;")
        self._detail_layout.addWidget(self._func_label)

        # 折叠区块容器
        self._sections_layout = QVBoxLayout()
        self._sections_layout.setSpacing(6)
        self._detail_layout.addLayout(self._sections_layout)
        self._detail_layout.addStretch()

        layout.addWidget(self._detail_scroll)

    def _build_action_bar(self):
        bar = QWidget()
        bar.setStyleSheet("background-color: #252525; border-bottom: 1px solid #333;")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(16, 8, 16, 8)
        bar_layout.setSpacing(6)

        self._btn_add = QPushButton("➕ 新增")
        self._btn_add.setObjectName("actionBtn")

        self._btn_edit = QPushButton("✏️ 编辑")
        self._btn_edit.setObjectName("actionBtn")

        self._btn_delete = QPushButton("🗑️ 删除")
        self._btn_delete.setObjectName("deleteBtn")

        self._btn_copy = QPushButton("📋 复制")
        self._btn_copy.setObjectName("actionBtn")

        self._btn_fav = QPushButton("☆ 收藏")
        self._btn_fav.setObjectName("favBtn")

        self._btn_more = QPushButton("···")
        self._btn_more.setObjectName("actionBtn")

        bar_layout.addWidget(self._btn_add)
        bar_layout.addWidget(self._btn_edit)
        bar_layout.addWidget(self._btn_delete)
        bar_layout.addStretch()
        bar_layout.addWidget(self._btn_copy)
        bar_layout.addWidget(self._btn_fav)
        bar_layout.addWidget(self._btn_more)

        self._detail_layout.addWidget(bar)

    # ── 显示条目 ──────────────────────────────────────────

    def show_item(self, item_data, item_type):
        """显示条目详情"""
        self._current_item = item_data
        self._current_type = item_type

        self._empty_label.setVisible(False)
        self._detail_scroll.setVisible(True)

        # 清除旧的折叠区块
        self._clear_sections()

        if item_type == 'command':
            self._show_command(item_data)
        elif item_type == 'code':
            self._show_code(item_data)
        elif item_type == 'pattern':
            self._show_pattern(item_data)

        # 更新收藏按钮状态
        fav = item_data.get('favorite', 0)
        self._btn_fav.setText("★ 已收藏" if fav else "☆ 收藏")
        self._btn_fav.setStyleSheet(
            "background-color: #4a3a1a; color: #f0c040; border: none; border-radius: 4px; padding: 6px 14px; font-size: 13px;"
            if fav else
            "background-color: #3a3a3a; color: #f0c040; border: none; border-radius: 4px; padding: 6px 14px; font-size: 13px;"
        )

        # 连接按钮
        self._connect_actions(item_data, item_type)

    def _show_command(self, item):
        self._title_label.setText(f"{item.get('cmd_name', '')}  —  {item.get('name_cn', '')}")
        self._subtitle_label.setText(f"命令行  |  {item.get('os_type', '通用')}  |  别名: {item.get('aliases', '')}")
        self._func_label.setText(f"📌 {item.get('function_desc', '')}")

        # 折叠区块
        sections = [
            ("完整语法", self._make_code_block(item.get('syntax', '')), True),
            ("基础用法示例", self._make_code_block(item.get('example_basic', '')), True),
            ("参数详解", self._make_json_table(item.get('params_json', '[]'), '参数', '说明'), False),
            ("进阶示例", self._make_code_block(item.get('example_adv', '')), False),
            ("避坑提示", self._make_text_block(item.get('tips', '')), False),
            ("元数据", self._make_meta_block(item), False),
        ]
        for title, widget, expanded in sections:
            section = CollapsibleSection(title, widget, expanded)
            self._sections_layout.addWidget(section)

    def _show_code(self, item):
        self._title_label.setText(item.get('title', ''))
        lang = item.get('language', '')
        ver = item.get('version', '')
        self._subtitle_label.setText(f"代码片段  |  {lang}  |  版本: {ver if ver else '通用'}  |  别名: {item.get('aliases', '')}")
        self._func_label.setText(f"📌 {item.get('syntax_note', '')}")

        sections = [
            ("完整代码", self._make_code_block(item.get('code_block', '')), True),
            ("逐行解析", self._make_json_table(item.get('line_by_line', '[]'), '代码/关键字', '说明'), False),
            ("语法规则/注意事项", self._make_text_block(item.get('syntax_note', '')), False),
            ("完整可运行示例", self._make_code_block(item.get('runnable_example', '')), False),
            ("常见报错与解决", self._make_json_table(item.get('common_errors', '[]'), '报错', '解决办法'), False),
            ("元数据", self._make_meta_block(item), False),
        ]
        for title, widget, expanded in sections:
            section = CollapsibleSection(title, widget, expanded)
            self._sections_layout.addWidget(section)

    def _show_pattern(self, item):
        self._title_label.setText(item.get('title', ''))
        lang = item.get('language', '')
        self._subtitle_label.setText(f"模式/标记  |  {lang}  |  别名: {item.get('aliases', '')}")
        self._func_label.setText(f"📌 {item.get('syntax_note', '')}")

        sections = [
            ("模式原文", self._make_code_block(item.get('pattern_text', '')), True),
            ("逐段解析", self._make_json_table(item.get('parsed_table', '[]'), '段/元素', '含义'), True),
            ("完整代码", self._make_code_block(item.get('code_block', '')), True),
            ("逐行解析", self._make_json_table(item.get('line_by_line', '[]'), '代码/关键字', '说明'), False),
            ("语法规则", self._make_text_block(item.get('syntax_note', '')), False),
            ("完整示例", self._make_code_block(item.get('runnable_example', '')), False),
            ("常见报错", self._make_json_table(item.get('common_errors', '[]'), '报错', '解决办法'), False),
            ("元数据", self._make_meta_block(item), False),
        ]
        for title, widget, expanded in sections:
            section = CollapsibleSection(title, widget, expanded)
            self._sections_layout.addWidget(section)

    # ── 辅助渲染 ──────────────────────────────────────────

    def _make_code_block(self, text):
        if not text or text == '[]':
            return QLabel("（无内容）")
        label = QLabel(text)
        label.setObjectName("sectionContent")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setWordWrap(True)
        font = QFont("Consolas", 12)
        font.setStyleHint(QFont.Monospace)
        label.setFont(font)
        return label

    def _make_text_block(self, text):
        if not text:
            return QLabel("（无内容）")
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("color: #d4d4d4; font-size: 13px; padding: 8px 12px;")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        return label

    def _make_json_table(self, json_str, col1, col2):
        """把 JSON 数组渲染为文本表格"""
        if not json_str or json_str == '[]' or json_str == '{}':
            return QLabel("（无内容）")
        try:
            data = json.loads(json_str) if isinstance(json_str, str) else json_str
            if not data:
                return QLabel("（无内容）")
            lines = [f"{'─'*40}"]
            for item in data:
                if isinstance(item, dict):
                    a = str(item.get(col1, list(item.keys())[0] if item.keys() else ''))
                    b = str(item.get(col2, list(item.values())[0] if item.values() else ''))
                    lines.append(f"  {a}")
                    lines.append(f"  → {b}")
                    lines.append(f"{'─'*40}")
                elif isinstance(item, str):
                    lines.append(f"  {item}")
            text = '\n'.join(lines)
            return self._make_code_block(text)
        except (json.JSONDecodeError, Exception):
            return self._make_code_block(json_str)

    def _make_meta_block(self, item):
        lines = []
        lines.append(f"ID: {item.get('id', '—')}")
        lines.append(f"使用次数: {item.get('use_count', 0)}")
        if 'os_type' in item:
            lines.append(f"操作系统: {item.get('os_type', '通用')}")
        if 'version' in item:
            lines.append(f"适用版本: {item.get('version', '通用')}")
        if 'tags' in item and item.get('tags'):
            lines.append(f"标签: {item.get('tags', '')}")
        if 'created_at' in item:
            lines.append(f"创建时间: {item.get('created_at', '—')}")
        if 'updated_at' in item:
            lines.append(f"更新时间: {item.get('updated_at', '—')}")
        return self._make_text_block('\n'.join(lines))

    def _connect_actions(self, item_data, item_type):
        # 安全断开之前的连接（PySide6 兼容写法）
        try: self._btn_fav.clicked.disconnect()
        except (TypeError, RuntimeError): pass
        try: self._btn_delete.clicked.disconnect()
        except (TypeError, RuntimeError): pass
        try: self._btn_copy.clicked.disconnect()
        except (TypeError, RuntimeError): pass
        try: self._btn_edit.clicked.disconnect()
        except (TypeError, RuntimeError): pass

        self._btn_fav.clicked.connect(lambda: self._on_fav(item_data['id'], item_type))
        self._btn_delete.clicked.connect(lambda: self._on_delete(item_data['id'], item_type))
        self._btn_copy.clicked.connect(lambda: self._on_copy(item_data, item_type))
        self._btn_edit.clicked.connect(lambda: self.edit_requested.emit(item_data))

    def _on_fav(self, item_id, item_type):
        self.favorite_toggled.emit(item_type, item_id)

    def _on_delete(self, item_id, item_type):
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定永久删除此条目吗？不可撤销。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.deleted.emit(item_type, item_id)

    def _on_copy(self, item_data, item_type):
        if item_type == 'command':
            text = item_data.get('example_basic', '') or item_data.get('syntax', '')
        else:
            text = item_data.get('code_block', '')
        if text:
            QApplication.clipboard().setText(text)
            self._show_toast("✅ 已复制到剪贴板")
        else:
            self._show_toast("⚠️ 没有可复制的内容")

    def _show_toast(self, msg):
        """简单的底部提示"""
        from PySide6.QtWidgets import QLabel
        self._toast = QLabel(msg, self)
        self._toast.setStyleSheet("""
            background-color: #333;
            color: #fff;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 13px;
        """)
        self._toast.adjustSize()
        x = (self.width() - self._toast.width()) // 2
        y = self.height() - self._toast.height() - 40
        self._toast.move(x, y)
        self._toast.show()
        self._toast.raise_()
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, self._toast.deleteLater)

    def _clear_sections(self):
        while self._sections_layout.count():
            item = self._sections_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def clear(self):
        self._current_item = None
        self._current_type = None
        self._empty_label.setVisible(True)
        self._detail_scroll.setVisible(False)
        self._clear_sections()

    @property
    def current_item(self):
        return self._current_item

    @property
    def current_type(self):
        return self._current_type
