"""
MainWindow — 主窗口
整合分类树、搜索栏、详情面板、状态栏
"""
import sys, os, json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QStatusBar, QApplication, QMessageBox, QFileDialog, QMenu,
    QComboBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer, QSize
from PySide6.QtGui import QFont, QAction, QKeySequence, QIcon, QCursor

from database.db_manager import DBManager
from ui.widgets.tree_widget import CategoryTreeWidget
from ui.widgets.detail_widget import DetailWidget
from ui.dialogs.add_edit_dialog import AddEditDialog


class MainWindow(QMainWindow):
    """代码速查工具主窗口"""

    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.db.init_db()

        self._setup_window()
        self._build_menu_bar()
        self._build_ui()
        self._connect_signals()
        self._setup_shortcuts()

        # 延迟加载数据
        QTimer.singleShot(100, self._load_initial_data)

    def _setup_window(self):
        self.setWindowTitle("CodeQuickRef — 代码速查工具")
        self.setMinimumSize(1100, 700)
        self.resize(1400, 850)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                color: #d4d4d4;
            }
            QLineEdit#searchInput {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 14px;
            }
            QLineEdit#searchInput:focus {
                border-color: #2d5a8a;
            }
            QPushButton#searchBtn {
                background-color: #2d5a8a;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton#searchBtn:hover {
                background-color: #3a6a9a;
            }
            QPushButton#toolBtn {
                background-color: #2a2a2a;
                color: #ccc;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton#toolBtn:hover {
                background-color: #3a3a3a;
            }
            QListWidget {
                background-color: #1a1a1a;
                color: #ccc;
                border: none;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #2a2a2a;
            }
            QListWidget::item:selected {
                background-color: #2d5a8a;
                color: #fff;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QStatusBar {
                background-color: #1a1a1a;
                color: #888;
                border-top: 1px solid #333;
                font-size: 12px;
            }
            QMenuBar {
                background-color: #1a1a1a;
                color: #ccc;
                border-bottom: 1px solid #333;
            }
            QMenuBar::item:selected {
                background-color: #2d5a8a;
            }
            QMenu {
                background-color: #2a2a2a;
                color: #ccc;
                border: 1px solid #444;
            }
            QMenu::item:selected {
                background-color: #2d5a8a;
            }
        """)

    def _build_menu_bar(self):
        menubar = self.menuBar()

        # 文件
        file_menu = menubar.addMenu("📁 文件")
        self._act_import = QAction("📥 导入 JSON...", self)
        self._act_export_all = QAction("📤 导出全部为 JSON...", self)
        self._act_exit = QAction("退出", self)
        self._act_exit.setShortcut("Ctrl+Q")
        self._act_exit.triggered.connect(self.close)
        file_menu.addAction(self._act_import)
        file_menu.addAction(self._act_export_all)
        file_menu.addSeparator()
        file_menu.addAction(self._act_exit)

        # 工具
        tools_menu = menubar.addMenu("🔧 工具")
        self._act_stats = QAction("📊 数据统计", self)
        self._act_check = QAction("✅ 数据完整性检查", self)
        tools_menu.addAction(self._act_stats)
        tools_menu.addAction(self._act_check)

        # 视图
        view_menu = menubar.addMenu("👁️ 视图")
        self._act_refresh = QAction("🔄 刷新", self)
        self._act_refresh.setShortcut("F5")
        view_menu.addAction(self._act_refresh)

        # 帮助
        help_menu = menubar.addMenu("❓ 帮助")
        self._act_about = QAction("关于", self)
        help_menu.addAction(self._act_about)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self._main_layout = QVBoxLayout(central)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # ── 顶部搜索栏 ──
        self._build_search_bar()

        # ── 主体：左(分类树) + 右(详情) ──
        splitter = QSplitter(Qt.Horizontal)

        self._tree_widget = CategoryTreeWidget(self.db)
        splitter.addWidget(self._tree_widget)

        self._detail_widget = DetailWidget()
        splitter.addWidget(self._detail_widget)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([280, 800])
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: #333; }")

        self._main_layout.addWidget(splitter, 1)

        # ── 状态栏 ──
        self._status_bar = QStatusBar()
        self._total_label = QLabel("正在加载...")
        self._selected_label = QLabel("未选中条目")
        self._status_bar.addWidget(self._total_label)
        self._status_bar.addPermanentWidget(self._selected_label)
        self.setStatusBar(self._status_bar)
        self._total_label.setStyleSheet("color: #888; padding-left: 8px;")
        self._selected_label.setStyleSheet("color: #888; padding-right: 8px;")

        # ── 搜索结果面板（初始隐藏） ──
        self._search_panel = QFrame()
        self._search_panel.setFrameShape(QFrame.StyledPanel)
        self._search_panel.setStyleSheet("QFrame { background-color: #1a1a1a; border-top: 1px solid #333; }")
        self._search_panel.setVisible(False)

        search_panel_layout = QVBoxLayout(self._search_panel)
        search_panel_layout.setContentsMargins(8, 4, 8, 4)

        search_header = QHBoxLayout()
        self._search_result_label = QLabel("搜索结果")
        self._search_result_label.setStyleSheet("color: #999; font-size: 12px; font-weight: bold;")
        self._btn_close_search = QPushButton("✕")
        self._btn_close_search.setObjectName("toolBtn")
        self._btn_close_search.setFixedSize(28, 28)
        self._btn_close_search.clicked.connect(lambda: self._search_panel.setVisible(False))
        search_header.addWidget(self._search_result_label)
        search_header.addStretch()
        search_header.addWidget(self._btn_close_search)
        search_panel_layout.addLayout(search_header)

        self._search_list = QListWidget()
        self._search_list.setMaximumHeight(300)
        self._search_list.itemClicked.connect(self._on_search_item_clicked)
        search_panel_layout.addWidget(self._search_list)

        self._main_layout.addWidget(self._search_panel)

    def _build_search_bar(self):
        search_bar = QWidget()
        search_bar.setStyleSheet("background-color: #252525; border-bottom: 1px solid #333;")
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(8)

        logo = QLabel("📖 CodeQuickRef")
        logo.setStyleSheet("color: #f0c040; font-size: 16px; font-weight: bold; padding: 0 8px;")
        search_layout.addWidget(logo)

        self._search_input = QLineEdit()
        self._search_input.setObjectName("searchInput")
        self._search_input.setPlaceholderText("输入关键词搜索（支持中/英文、别名）...")
        self._search_input.returnPressed.connect(self._on_search)
        search_layout.addWidget(self._search_input, 1)

        btn_search = QPushButton("🔍 搜索")
        btn_search.setObjectName("searchBtn")
        btn_search.clicked.connect(self._on_search)
        search_layout.addWidget(btn_search)

        # 过滤+备份按钮
        self._btn_filter = QPushButton("🔽 筛选")
        self._btn_filter.setObjectName("toolBtn")
        search_layout.addWidget(self._btn_filter)

        self._btn_export = QPushButton("📤 备份")
        self._btn_export.setObjectName("toolBtn")
        search_layout.addWidget(self._btn_export)

        self._btn_import = QPushButton("📥 导入")
        self._btn_import.setObjectName("toolBtn")
        search_layout.addWidget(self._btn_import)

        self._main_layout.addWidget(search_bar)

    def _connect_signals(self):
        # 树形导航 -> 加载条目列表
        self._tree_widget.category_selected.connect(self._on_category_selected)

        # 详情操作
        self._detail_widget.favorite_toggled.connect(self._on_favorite_toggle)
        self._detail_widget.deleted.connect(self._on_item_deleted)
        self._detail_widget.edit_requested.connect(self._on_edit_requested)

        # 新增按钮
        self._detail_widget._btn_add.clicked.connect(self._on_add_clicked)

        # 菜单
        self._act_export_all.triggered.connect(self._on_export_all)
        self._act_import.triggered.connect(self._on_import)
        self._act_refresh.triggered.connect(self._on_refresh)
        self._act_stats.triggered.connect(self._on_stats)

        # 工具栏按钮
        self._btn_export.clicked.connect(self._on_export_all)
        self._btn_import.clicked.connect(self._on_import)
        self._btn_filter.clicked.connect(self._on_filter)

        # 树形：收藏夹/最近查看
        self._tree_widget._btn_favs.clicked.connect(self._show_favorites)
        self._tree_widget._btn_recent.clicked.connect(self._show_recent)

    def _setup_shortcuts(self):
        # Ctrl+F: 搜索框聚焦
        QAction("搜索", self, shortcut=QKeySequence("Ctrl+F"),
                triggered=lambda: self._search_input.setFocus()).setShortcutContext(Qt.ApplicationShortcut)
        # Ctrl+N: 新增
        QAction("新增", self, shortcut=QKeySequence("Ctrl+N"),
                triggered=self._on_add_clicked).setShortcutContext(Qt.ApplicationShortcut)

    def _load_initial_data(self):
        self._tree_widget.refresh_tree()
        self._update_total()

    # ── 分类选择 ──────────────────────────────────────────

    def _on_category_selected(self, cat_id, item_type):
        """选择分类后，展示该分类下的条目列表"""
        self._current_cat_id = cat_id
        self._current_item_type = item_type

        # 清空详情
        self._detail_widget.clear()

        # 从数据库加载条目列表
        if item_type == 'command':
            items, total = self.db.get_commands(cat_id)
        elif item_type == 'code':
            items, total = self.db.get_snippets(cat_id)
        else:
            items, total = self.db.get_patterns(cat_id)

        # 如果有且仅有一条，自动显示
        if len(items) == 1:
            self._show_item_detail(items[0], item_type)
        elif len(items) > 1:
            # 显示列表选择器
            self._show_item_list(items, item_type)
        else:
            self._selected_label.setText(f"空分类 (0 条)")

    def _show_item_list(self, items, item_type):
        """在搜索面板中显示条目列表供选择"""
        self._search_panel.setVisible(True)
        self._search_list.clear()
        self._search_result_label.setText(f"📋 {self._get_cat_path()}  —  {len(items)} 条")

        for item in items:
            if item_type == 'command':
                text = f"{item.get('cmd_name', '')}  —  {item.get('name_cn', '')}"
            else:
                text = f"{item.get('title', '')}  ({item.get('language', '')})"
            list_item = QListWidgetItem(text)
            list_item.setData(Qt.UserRole, item)
            list_item.setData(Qt.UserRole + 1, item_type)
            self._search_list.addItem(list_item)

    def _get_cat_path(self):
        """获取当前分类路径"""
        if hasattr(self, '_current_cat_id'):
            return ' / '.join(self.db.get_category_path(self._current_cat_id))
        return ""

    def _on_search_item_clicked(self, item):
        """从搜索结果或分类列表中选择条目"""
        data = item.data(Qt.UserRole)
        item_type = item.data(Qt.UserRole + 1) or 'command'
        if data:
            self._show_item_detail(data, item_type)

    # ── 显示详情 ──────────────────────────────────────────

    def _show_item_detail(self, item_data, item_type):
        self._detail_widget.show_item(item_data, item_type)
        # 记录使用
        self.db.record_use(item_type, item_data['id'])
        self._selected_label.setText(f"已选中: {item_data.get('cmd_name') or item_data.get('title', '—')}")
        self._update_total()

        # 从分类列表中移除（下次通过 category_selected 重新加载）
        self._search_panel.setVisible(False)

    # ── 搜索 ──────────────────────────────────────────────

    def _on_search(self):
        keyword = self._search_input.text().strip()
        if not keyword:
            return

        self._search_panel.setVisible(True)
        self._search_list.clear()

        # 用 LIKE 搜索（中文友好）
        results, total = self.db.search_simple(keyword)
        if not results:
            # 试试 FTS
            results, total = self.db.search(keyword)
            # 如果 FTS 也没结果，用简单搜索
            if not results:
                pass  # 已空

        self._search_result_label.setText(f"🔍 搜索「{keyword}」— 找到 {len(results)} 条")

        for item in results:
            if item.get('item_type') == 'command':
                text = f"💻 {item.get('cmd_name', '')} — {item.get('name_cn', '')}"
            elif item.get('item_type') == 'code':
                text = f"🧩 {item.get('title', '')} ({item.get('language', '')})"
            else:
                text = f"📐 {item.get('title', '')}"
            list_item = QListWidgetItem(text)

            # 获取完整条目数据
            full = self.db.get_item(item['id'], item['item_type'])
            list_item.setData(Qt.UserRole, full)
            list_item.setData(Qt.UserRole + 1, item['item_type'])
            self._search_list.addItem(list_item)

    # ── 收藏 ──────────────────────────────────────────────

    def _on_favorite_toggle(self, item_type, item_id):
        new_state = self.db.toggle_favorite(item_type, item_id)
        # 刷新详情
        item = self.db.get_item(item_id, item_type)
        if item:
            self._detail_widget.show_item(item, item_type)

    def _show_favorites(self):
        favs = self.db.get_favorites()
        self._search_panel.setVisible(True)
        self._search_list.clear()
        self._search_result_label.setText(f"⭐ 收藏夹  —  {len(favs)} 条")

        for f in favs:
            detail = f.get('detail', {})
            if detail:
                if f['item_type'] == 'command':
                    text = f"💻 {detail.get('cmd_name', '')} — {detail.get('name_cn', '')}"
                else:
                    text = f"🧩 {detail.get('title', '')}"
                list_item = QListWidgetItem(text)
                list_item.setData(Qt.UserRole, detail)
                list_item.setData(Qt.UserRole + 1, f['item_type'])
                self._search_list.addItem(list_item)

    def _show_recent(self):
        # 从会话中加载最近查看（按 use_count 排序取前20）
        results = []
        for table, item_type in [('commands', 'command'), ('code_snippets', 'code'), ('pattern_items', 'pattern')]:
            rows = self.db.conn.execute(
                f"SELECT * FROM {table} ORDER BY use_count DESC, updated_at DESC LIMIT 20"
            ).fetchall()
            results.extend((dict(r), item_type) for r in rows)
        results.sort(key=lambda x: x[0].get('use_count', 0), reverse=True)
        results = results[:20]

        self._search_panel.setVisible(True)
        self._search_list.clear()
        self._search_result_label.setText(f"📋 最近查看  —  前 {len(results)} 条")

        for item, item_type in results:
            if item_type == 'command':
                text = f"💻 {item.get('cmd_name', '')} — {item.get('name_cn', '')}  [{item.get('use_count', 0)}次]"
            else:
                text = f"🧩 {item.get('title', '')}  [{item.get('use_count', 0)}次]"
            list_item = QListWidgetItem(text)
            list_item.setData(Qt.UserRole, item)
            list_item.setData(Qt.UserRole + 1, item_type)
            self._search_list.addItem(list_item)

    # ── 新增/编辑/删除 ────────────────────────────────────

    def _on_add_clicked(self):
        cat_id = getattr(self, '_current_cat_id', None)
        item_type = getattr(self, '_current_item_type', 'command')
        dlg = AddEditDialog(self.db, item_type, cat_id, parent=self)
        if dlg.exec():
            data = dlg.get_result()
            if data:
                if dlg.item_type == 'command':
                    self.db.add_command(**data)
                elif dlg.item_type == 'code':
                    self.db.add_snippet(**data)
                elif dlg.item_type == 'pattern':
                    self.db.add_pattern(**data)
                self._tree_widget.refresh_tree()
                self._update_total()
                if cat_id:
                    self._on_category_selected(cat_id, dlg.item_type)

    def _on_edit_requested(self, item_data):
        item_type = self._detail_widget.current_type
        dlg = AddEditDialog(self.db, item_type, item_data=item_data, parent=self)
        if dlg.exec():
            data = dlg.get_result()
            if data:
                item_id = data.pop('id')
                if item_type == 'command':
                    self.db.update_command(item_id, **data)
                elif item_type == 'code':
                    self.db.update_snippet(item_id, **data)
                elif item_type == 'pattern':
                    self.db.update_pattern(item_id, **data)
                # 刷新
                updated = self.db.get_item(item_id, item_type)
                if updated:
                    self._detail_widget.show_item(updated, item_type)
                self._tree_widget.refresh_tree()

    def _on_item_deleted(self, item_type, item_id):
        self.db.delete_item(item_id, item_type)
        self._detail_widget.clear()
        self._tree_widget.refresh_tree()
        self._update_total()
        if hasattr(self, '_current_cat_id'):
            self._on_category_selected(self._current_cat_id, item_type)

    # ── 导入/导出 ─────────────────────────────────────────

    def _on_export_all(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出数据", "code_quickref_backup.json", "JSON Files (*.json)"
        )
        if not file_path:
            return
        all_data = {
            'commands': json.loads(self.db.export_json(item_type='command')),
            'snippets': json.loads(self.db.export_json(item_type='code')),
            'patterns': json.loads(self.db.export_json(item_type='pattern')),
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)
        QMessageBox.information(self, "导出成功", f"已导出到:\n{file_path}")

    def _on_import(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入数据", "", "JSON Files (*.json)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = 0
            if 'commands' in data:
                count += self.db.import_json(json.dumps(data['commands']), merge=True, item_type='command')
            if 'snippets' in data:
                count += self.db.import_json(json.dumps(data['snippets']), merge=True, item_type='code')
            if 'patterns' in data:
                count += self.db.import_json(json.dumps(data['patterns']), merge=True, item_type='pattern')
            self._tree_widget.refresh_tree()
            self._update_total()
            QMessageBox.information(self, "导入成功", f"成功导入/更新 {count} 条数据")
        except Exception as e:
            QMessageBox.warning(self, "导入失败", f"错误: {str(e)}")

    def _on_refresh(self):
        self._tree_widget.refresh_tree()
        self._update_total()

    def _on_filter(self):
        # 简单的按类型过滤
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #2a2a2a; color: #ccc; border: 1px solid #444; }")
        all_action = menu.addAction("全部")
        cmd_action = menu.addAction("命令行")
        code_action = menu.addAction("代码片段")
        pattern_action = menu.addAction("模式/标记")

        action = menu.exec(QCursor.pos())
        if action:
            keyword = self._search_input.text().strip()
            if not keyword:
                return
            self._on_search()

    def _on_stats(self):
        counts = self.db.get_type_counts()
        total = sum(counts.values())
        QMessageBox.information(self, "📊 数据统计",
            f"总条目数: {total}\n\n"
            f"💻 命令行: {counts.get('command', 0)} 条\n"
            f"🧩 代码片段: {counts.get('code', 0)} 条\n"
            f"📐 模式/标记: {counts.get('pattern', 0)} 条\n\n"
            f"数据库位置: {self.db.db_path}"
        )

    # ── 辅助 ──────────────────────────────────────────────

    def _update_total(self):
        total = self.db.get_total_count()
        self._total_label.setText(f"共 {total} 条 | SQLite 已加载")
