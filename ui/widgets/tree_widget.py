"""
TreeWidget — 分类树导航（左侧面板）
支持懒加载、右键菜单、收藏夹和最近查看
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMenu,
    QPushButton, QLabel, QHBoxLayout, QInputDialog, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QFont


class CategoryTreeWidget(QWidget):
    """分类树导航 + 快捷入口"""
    category_selected = Signal(int, str)    # (category_id, item_type)
    item_selected = Signal(object, str)     # (item_data, item_type) 直接从搜索/收藏/最近中选择条目
    search_requested = Signal(str)          # 关键词

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self._favorites = []
        self._recent = []
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumWidth(220)
        self.setMaximumWidth(350)
        self.setStyleSheet("""
            QWidget#treePanel {
                background-color: #1a1a1a;
                border-right: 1px solid #333;
            }
            QTreeWidget {
                background-color: #1a1a1a;
                color: #ccc;
                border: none;
                font-size: 13px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 4px 8px;
                border-radius: 3px;
            }
            QTreeWidget::item:selected {
                background-color: #2d5a8a;
                color: #fff;
            }
            QTreeWidget::item:hover {
                background-color: #2a2a2a;
            }
            QPushButton#sectionBtn {
                background-color: #222;
                color: #999;
                border: none;
                text-align: left;
                padding: 6px 10px;
                font-size: 12px;
                font-weight: bold;
                border-bottom: 1px solid #333;
            }
            QPushButton#sectionBtn:hover {
                background-color: #2a2a2a;
                color: #ddd;
            }
            QLabel#sectionLabel {
                color: #999;
                font-size: 11px;
                padding: 4px 10px;
                font-weight: bold;
                text-transform: uppercase;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 快捷入口
        self._btn_recent = QPushButton("📋 最近查看")
        self._btn_recent.setObjectName("sectionBtn")
        self._btn_recent.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self._btn_recent)

        self._btn_favs = QPushButton("⭐ 收藏夹")
        self._btn_favs.setObjectName("sectionBtn")
        self._btn_favs.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self._btn_favs)

        # 分类树标签
        label = QLabel("📂 分类导航")
        label.setObjectName("sectionLabel")
        layout.addWidget(label)

        # 分类树
        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setAnimated(True)
        self._tree.setIndentation(16)
        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemExpanded.connect(self._on_item_expanded)
        self._tree.customContextMenuRequested.connect(self._show_context_menu)
        self._tree.setStyleSheet("""
            QTreeWidget { padding-top: 4px; }
        """)
        layout.addWidget(self._tree)

        # 状态
        self._status_label = QLabel("加载中...")
        self._status_label.setStyleSheet("color: #666; font-size: 11px; padding: 4px 10px;")
        layout.addWidget(self._status_label)

    # ── 加载数据 ──────────────────────────────────────────

    def refresh_tree(self):
        """刷新整个分类树"""
        self._tree.clear()
        roots = self.db.get_categories(parent_id=None)
        for root in roots:
            item = QTreeWidgetItem(self._tree)
            count = root.get('item_count', 0)
            child_count = root.get('child_count', 0)
            text = f"{root['name']}  ({count})"
            item.setText(0, text)
            item.setData(0, Qt.UserRole, root)

            # 如果有子分类，添加占位节点使之可展开
            if child_count > 0:
                placeholder = QTreeWidgetItem(item)
                placeholder.setText(0, "加载中...")
                placeholder.setFlags(Qt.NoItemFlags)

        self._tree.expandAll()
        self._update_status()

    def _load_children(self, parent_item):
        """懒加载子分类"""
        data = parent_item.data(0, Qt.UserRole)
        if not data:
            return

        # 移除占位符
        parent_item.takeChildren()

        children = self.db.get_categories(parent_id=data['id'])
        for child in children:
            item = QTreeWidgetItem(parent_item)
            count = child.get('item_count', 0)
            child_count = child.get('child_count', 0)
            text = f"{child['name']}  ({count})"
            item.setText(0, text)
            item.setData(0, Qt.UserRole, child)

            # 三级子分类
            if child_count > 0:
                placeholder = QTreeWidgetItem(item)
                placeholder.setText(0, "加载中...")
                placeholder.setFlags(Qt.NoItemFlags)

    def _on_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if not data or data.get('id') is None:
            return
        # 叶节点（无子分类）才触发条目加载
        child_count = data.get('child_count', 0)
        if child_count == 0:
            self.category_selected.emit(data['id'], data['item_type'])

    def _on_item_expanded(self, item):
        data = item.data(0, Qt.UserRole)
        if data and data.get('child_count', 0) > 0:
            # 检查是否还是占位符
            if item.childCount() == 1 and item.child(0).text(0) == "加载中...":
                self._load_children(item)

    def _show_context_menu(self, pos):
        item = self._tree.itemAt(pos)
        if not item:
            return
        data = item.data(0, Qt.UserRole)
        if not data:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #2a2a2a; color: #ccc; border: 1px solid #444; }
            QMenu::item:selected { background-color: #2d5a8a; }
        """)

        add_action = menu.addAction("➕ 新增子分类")
        rename_action = menu.addAction("✏️ 重命名")
        delete_action = menu.addAction("🗑️ 删除分类")
        menu.addSeparator()
        refresh_action = menu.addAction("🔄 刷新计数")

        action = menu.exec(self._tree.mapToGlobal(pos))

        if action == add_action:
            self._add_category(data)
        elif action == rename_action:
            self._rename_category(item, data)
        elif action == delete_action:
            self._delete_category(item, data)
        elif action == refresh_action:
            self.refresh_tree()

    def _add_category(self, parent_data):
        name, ok = QInputDialog.getText(self, "新增子分类", "分类名称:")
        if not ok or not name.strip():
            return
        item_type = parent_data.get('item_type', 'command')
        self.db.add_category(name.strip(), parent_data['id'], item_type)
        self.refresh_tree()

    def _rename_category(self, item, data):
        name, ok = QInputDialog.getText(self, "重命名", "新名称:", text=data['name'])
        if not ok or not name.strip():
            return
        self.db.rename_category(data['id'], name.strip())
        self.refresh_tree()

    def _delete_category(self, item, data):
        reply = QMessageBox.question(
            self, "确认删除",
            f"删除「{data['name']}」及其所有子分类和条目？不可撤销。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_category(data['id'])
            self.refresh_tree()

    def _update_status(self):
        total = self.db.get_total_count()
        counts = self.db.get_type_counts()
        self._status_label.setText(
            f"共 {total} 条  |  💻{counts.get('command',0)} 🧩{counts.get('code',0)} 📐{counts.get('pattern',0)}"
        )

    # ── 外部接口 ──────────────────────────────────────────

    def refresh_count(self):
        self._update_status()
