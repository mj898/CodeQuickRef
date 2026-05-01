"""
AddEditDialog — 新增/编辑条目的模态对话框
支持三种类型：command / code / pattern
根据类型展示对应表单
"""
import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QScrollArea,
    QWidget, QFormLayout, QCheckBox, QGroupBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class AddEditDialog(QDialog):
    """新增/编辑条目对话框"""

    def __init__(self, db_manager, item_type='command', category_id=None, item_data=None, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.item_type = item_type
        self.category_id = category_id
        self.item_data = item_data  # 编辑模式用
        self.is_edit = item_data is not None

        self.setWindowTitle(f"{'编辑' if self.is_edit else '新增'} 条目")
        self.setMinimumSize(650, 550)
        self.setMaximumSize(900, 800)

        self._setup_style()
        self._build_ui()
        self._populate_data()

    def _setup_style(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ccc;
                font-size: 13px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #2d5a8a;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QPushButton {
                border-radius: 4px;
                padding: 8px 24px;
                font-size: 14px;
            }
            QPushButton#saveBtn {
                background-color: #2d5a8a;
                color: #fff;
                border: none;
            }
            QPushButton#saveBtn:hover {
                background-color: #3a6a9a;
            }
            QPushButton#cancelBtn {
                background-color: #3a3a3a;
                color: #ccc;
                border: 1px solid #555;
            }
            QPushButton#cancelBtn:hover {
                background-color: #4a4a4a;
            }
            QGroupBox {
                color: #ddd;
                font-size: 13px;
                font-weight: bold;
                border: 1px solid #333;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 8px;
                background-color: #1e1e1e;
            }
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # 顶部：类型和分类选择
        top = QHBoxLayout()
        top.addWidget(QLabel("条目类型:"))
        self._type_combo = QComboBox()
        self._type_combo.addItems(["命令行", "代码片段", "模式/标记"])
        self._type_combo.setCurrentIndex(
            {'command': 0, 'code': 1, 'pattern': 2}.get(self.item_type, 0)
        )
        self._type_combo.currentIndexChanged.connect(self._on_type_changed)
        top.addWidget(self._type_combo)

        top.addWidget(QLabel("  分类:"))
        self._cat_combo = QComboBox()
        self._load_categories()
        top.addWidget(self._cat_combo, 1)
        layout.addLayout(top)

        # 滚动内容区
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self._form_container = QWidget()
        self._form_layout = QVBoxLayout(self._form_container)
        self._form_layout.setSpacing(4)
        scroll.setWidget(self._form_container)
        layout.addWidget(scroll, 1)

        # 底部按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._btn_save = QPushButton("💾 保存")
        self._btn_save.setObjectName("saveBtn")
        self._btn_save.clicked.connect(self._on_save)
        self._btn_cancel = QPushButton("取消")
        self._btn_cancel.setObjectName("cancelBtn")
        self._btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self._btn_cancel)
        btn_layout.addWidget(self._btn_save)
        layout.addLayout(btn_layout)

        # 初始化表单
        self._build_form()

    def _load_categories(self):
        self._cat_combo.clear()
        self._cat_combo.addItem("请选择分类...", None)
        roots = self.db.get_categories(parent_id=None)
        for root in roots:
            children = self.db.get_categories(parent_id=root['id'])
            for child in children:
                text = f"{root['name']} / {child['name']}"
                self._cat_combo.addItem(text, child['id'])
        # 尝试选择传入的分类
        if self.category_id:
            idx = self._cat_combo.findData(self.category_id)
            if idx >= 0:
                self._cat_combo.setCurrentIndex(idx)

    def _on_type_changed(self, idx):
        # 切换类型时重建表单
        self._clear_form()
        new_type = ['command', 'code', 'pattern'][idx]
        self.item_type = new_type
        self._build_form()

    def _clear_form(self):
        while self._form_layout.count():
            item = self._form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _build_form(self):
        self._form_widgets = {}
        if self.item_type == 'command':
            self._build_command_form()
        elif self.item_type == 'code':
            self._build_code_form()
        elif self.item_type == 'pattern':
            self._build_pattern_form()

    # ── 命令行表单 ────────────────────────────────────────

    def _build_command_form(self):
        fields = [
            ("cmd_name", "命令全称", True),
            ("name_cn", "中文名", True),
            ("function_desc", "核心作用", True),
            ("syntax", "完整语法格式", False),
            ("params_json", "参数详解 (JSON数组)", False,
             '格式: [{"参数":"-a","说明":"自动暂存"}, ...]'),
            ("example_basic", "基础用法示例", False),
            ("example_adv", "进阶用法示例", False),
            ("os_type", "操作系统差异", False),
            ("aliases", "别名/关键词", False),
            ("tips", "避坑提示", False),
        ]
        self._add_fields(fields)

    # ── 代码片段表单 ──────────────────────────────────────

    def _build_code_form(self):
        fields = [
            ("title", "功能名称", True),
            ("language", "所属语言", True),
            ("version", "适用版本", False),
            ("code_block", "完整代码块", True),
            ("line_by_line", "逐行解析 (JSON)", False,
             '格式: [{"代码":"import pandas as pd","说明":"导入pandas库"}, ...]'),
            ("syntax_note", "语法规则/注意事项", False),
            ("runnable_example", "完整可运行示例", False),
            ("common_errors", "常见报错 (JSON)", False,
             '格式: [{"报错":"FileNotFoundError","解决办法":"检查路径"}, ...]'),
            ("aliases", "别名/关键词", False),
        ]
        self._add_fields(fields)

    # ── 模式/标记表单 ─────────────────────────────────────

    def _build_pattern_form(self):
        fields = [
            ("title", "功能名称", True),
            ("language", "类型", True),
            ("version", "适用版本", False),
            ("pattern_text", "模式原文", True),
            ("parsed_table", "逐段解析 (JSON)", False,
             '格式: [{"段":"\\\\d","含义":"匹配数字"}, ...]'),
            ("code_block", "完整代码块", True),
            ("line_by_line", "逐行解析 (JSON)", False),
            ("syntax_note", "语法规则", False),
            ("runnable_example", "完整示例", False),
            ("common_errors", "常见报错 (JSON)", False),
            ("aliases", "别名/关键词", False),
        ]
        self._add_fields(fields)

    # ── 统一字段渲染 ──────────────────────────────────────

    def _add_fields(self, fields):
        for field in fields:
            key = field[0]
            label = field[1]
            required = field[2]
            hint = field[3] if len(field) > 3 else None

            group = QGroupBox(f"{label}{' *' if required else ''}")
            glayout = QVBoxLayout(group)
            glayout.setContentsMargins(8, 4, 8, 4)
            glayout.setSpacing(4)

            if hint:
                hint_label = QLabel(f"💡 {hint}")
                hint_label.setStyleSheet("color: #888; font-size: 11px; padding: 0;")
                hint_label.setWordWrap(True)
                glayout.addWidget(hint_label)

            # 大文本用 QTextEdit，小文本用 QLineEdit
            if key in ('code_block', 'runnable_example', 'syntax', 'syntax_note', 'pattern_text'):
                widget = QTextEdit()
                widget.setPlaceholderText(f"请输入{label}...")
                widget.setMinimumHeight(80)
                widget.setFont(QFont("Consolas", 12))
            elif key in ('params_json', 'line_by_line', 'common_errors', 'parsed_table'):
                widget = QTextEdit()
                widget.setPlaceholderText(f"请输入{label}...")
                widget.setMinimumHeight(60)
                widget.setFont(QFont("Consolas", 11))
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(f"请输入{label}...")

            glayout.addWidget(widget)
            self._form_widgets[key] = widget
            self._form_layout.addWidget(group)

    def _populate_data(self):
        """编辑模式：填充已有数据"""
        if not self.item_data:
            return
        data = self.item_data
        for key, widget in self._form_widgets.items():
            val = data.get(key, '')
            if val is None:
                val = ''
            if isinstance(val, (list, dict)):
                val = json.dumps(val, ensure_ascii=False)
            if isinstance(widget, QTextEdit):
                widget.setPlainText(str(val))
            else:
                widget.setText(str(val))

        # 选择正确的分类
        cat_id = data.get('category_id')
        if cat_id:
            idx = self._cat_combo.findData(cat_id)
            if idx >= 0:
                self._cat_combo.setCurrentIndex(idx)

    def _on_save(self):
        """保存数据并关闭"""
        # 校验必填
        if self.item_type == 'command':
            required = ['cmd_name', 'name_cn', 'function_desc']
        elif self.item_type == 'code':
            required = ['title', 'language', 'code_block']
        else:
            required = ['title', 'language', 'pattern_text', 'code_block']

        for key in required:
            widget = self._form_widgets.get(key)
            if widget:
                val = widget.toPlainText() if isinstance(widget, QTextEdit) else widget.text()
                if not val.strip():
                    QMessageBox.warning(self, "提示", f"请填写必填字段")
                    return

        # 收集数据
        data = {}
        for key, widget in self._form_widgets.items():
            if isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            else:
                data[key] = widget.text()

        # 处理 JSON 字段
        for json_field in ('params_json', 'line_by_line', 'common_errors', 'parsed_table'):
            if json_field in data and data[json_field].strip():
                try:
                    json.loads(data[json_field])
                except (json.JSONDecodeError, Exception):
                    QMessageBox.warning(self, "格式错误", f"「{json_field}」不是有效的 JSON 格式")
                    return

        # 分类
        data['category_id'] = self._cat_combo.currentData()

        if self.is_edit:
            data['id'] = self.item_data['id']

        self._result_data = data
        self.accept()

    def get_result(self):
        """返回保存的数据"""
        return getattr(self, '_result_data', None)
