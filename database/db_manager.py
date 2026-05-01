"""
DBManager — 数据库 CRUD 统一管理
支持 commands / code_snippets / pattern_items 三类条目的增删改查 + FTS5 全文搜索
"""
import json
import sqlite3
import os
from pathlib import Path
from .schema import SCHEMA_SQL, CATEGORY_SEED

DB_PATH = os.path.join(str(Path.home()), '.code-quickref', 'data.db')


class DBManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._conn = None

    # ── 连接管理 ──────────────────────────────────────────

    @property
    def conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA cache_size=-8000")   # 8MB cache
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── 初始化 ────────────────────────────────────────────

    def init_db(self):
        """创建表结构和初始分类"""
        for stmt in SCHEMA_SQL.split(';'):
            stmt = stmt.strip()
            if stmt:
                try:
                    self.conn.execute(stmt)
                except sqlite3.OperationalError as e:
                    print(f"[DB] Schema warning: {e}")
        self.conn.commit()
        self._seed_categories()

    def _seed_categories(self):
        """填充默认分类树"""
        cur = self.conn.execute("SELECT COUNT(*) FROM categories")
        if cur.fetchone()[0] > 0:
            return
        # 先建一级
        name_id_map = {}
        for parent_name, name, item_type, sort_order in CATEGORY_SEED:
            if parent_name is None:
                self.conn.execute(
                    "INSERT INTO categories (parent_id, name, item_type, sort_order) VALUES (?,?,?,?)",
                    (None, name, item_type, sort_order)
                )
                name_id_map[name] = self.conn.execute(
                    "SELECT last_insert_rowid()"
                ).fetchone()[0]
        # 再建二级
        for parent_name, name, item_type, sort_order in CATEGORY_SEED:
            if parent_name is not None and parent_name in name_id_map:
                self.conn.execute(
                    "INSERT INTO categories (parent_id, name, item_type, sort_order) VALUES (?,?,?,?)",
                    (name_id_map[parent_name], name, item_type, sort_order)
                )
        self.conn.commit()

    # ── 分类操作 ──────────────────────────────────────────

    def get_categories(self, parent_id=None):
        """获取分类列表，支持懒加载"""
        if parent_id is None:
            rows = self.conn.execute(
                "SELECT * FROM categories WHERE parent_id IS NULL ORDER BY sort_order"
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM categories WHERE parent_id=? ORDER BY sort_order",
                (parent_id,)
            ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d['child_count'] = self._get_child_count(r['id'])
            # 有子分类的节点用递归汇总，叶子节点用 direct count
            if d['child_count'] > 0:
                d['item_count'] = self._get_recursive_item_count(r['id'])
            else:
                d['item_count'] = self._get_item_count(r['id'], r['item_type'])
            result.append(d)
        return result

    def get_all_categories_map(self):
        """返回 {id: name} 和 {name: id} 映射"""
        rows = self.conn.execute("SELECT id, name FROM categories").fetchall()
        id_name = {r['id']: r['name'] for r in rows}
        name_id = {r['name']: r['id'] for r in rows}
        return id_name, name_id

    def _get_child_count(self, cat_id):
        return self.conn.execute(
            "SELECT COUNT(*) FROM categories WHERE parent_id=?", (cat_id,)
        ).fetchone()[0]

    def _get_item_count(self, cat_id, item_type):
        """获取分类下的条目数量（不含子分类）"""
        table = self._table_for_type(item_type)
        if not table:
            return 0
        row = self.conn.execute(
            f"SELECT COUNT(*) FROM {table} WHERE category_id=?", (cat_id,)
        ).fetchone()
        return row[0] if row else 0

    def _get_recursive_item_count(self, cat_id):
        """递归汇总分类及其所有子分类的条目总数"""
        # 先统计自己的条目（查所有三个表）
        total = 0
        for table in ['commands', 'code_snippets', 'pattern_items']:
            row = self.conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE category_id=?", (cat_id,)
            ).fetchone()
            total += row[0] if row else 0
        # 递归子分类
        children = self.conn.execute(
            "SELECT id FROM categories WHERE parent_id=?", (cat_id,)
        ).fetchall()
        for child in children:
            total += self._get_recursive_item_count(child['id'])
        return total

    def get_item_count_for_category(self, cat_id, item_type):
        table = self._table_for_type(item_type)
        if not table:
            return 0
        row = self.conn.execute(
            f"SELECT COUNT(*) FROM {table} WHERE category_id=?", (cat_id,)
        ).fetchone()
        return row[0] if row else 0

    def get_category_path(self, cat_id):
        """获取从根到当前分类的路径名列表"""
        path = []
        current = cat_id
        id_map, _ = self.get_all_categories_map()
        while current is not None:
            row = self.conn.execute("SELECT id, parent_id, name FROM categories WHERE id=?", (current,)).fetchone()
            if not row:
                break
            path.append(row['name'])
            current = row['parent_id']
        return list(reversed(path))

    def add_category(self, name, parent_id, item_type='command', sort_order=0):
        self.conn.execute(
            "INSERT INTO categories (parent_id, name, item_type, sort_order) VALUES (?,?,?,?)",
            (parent_id, name, item_type, sort_order)
        )
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def rename_category(self, cat_id, new_name):
        self.conn.execute("UPDATE categories SET name=? WHERE id=?", (new_name, cat_id))
        self.conn.commit()

    def delete_category(self, cat_id):
        """删除分类及其所有子分类和条目"""
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.execute("DELETE FROM categories WHERE id=?", (cat_id,))
        self.conn.commit()

    def move_category(self, cat_id, new_parent_id, new_sort_order=None):
        if new_sort_order is not None:
            self.conn.execute(
                "UPDATE categories SET parent_id=?, sort_order=? WHERE id=?",
                (new_parent_id, new_sort_order, cat_id)
            )
        else:
            self.conn.execute(
                "UPDATE categories SET parent_id=? WHERE id=?",
                (new_parent_id, cat_id)
            )
        self.conn.commit()

    # ── 条目 CRUD ────────────────────────────────────────

    # -- 命令行 --

    def add_command(self, **kw):
        sql = """INSERT INTO commands
            (category_id, cmd_name, name_cn, function_desc, syntax, params_json,
             example_basic, example_adv, os_type, aliases, tips, tags)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.conn.execute(sql, (
            kw['category_id'], kw['cmd_name'], kw['name_cn'], kw['function_desc'],
            kw.get('syntax', ''), kw.get('params_json', '[]'),
            kw.get('example_basic', ''), kw.get('example_adv', ''),
            kw.get('os_type', '通用'), kw.get('aliases', ''),
            kw.get('tips', ''), kw.get('tags', ''),
        ))
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def update_command(self, item_id, **kw):
        fields = ['cmd_name', 'name_cn', 'function_desc', 'syntax', 'params_json',
                  'example_basic', 'example_adv', 'os_type', 'aliases', 'tips', 'tags', 'favorite']
        sets = []
        vals = []
        for f in fields:
            if f in kw:
                sets.append(f"{f}=?")
                vals.append(kw[f])
        if not sets:
            return
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(item_id)
        self.conn.execute(
            f"UPDATE commands SET {', '.join(sets)} WHERE id=?", vals
        )
        self.conn.commit()

    def delete_command(self, item_id):
        self.conn.execute("DELETE FROM commands WHERE id=?", (item_id,))
        self.conn.commit()

    def get_command(self, item_id):
        row = self.conn.execute("SELECT * FROM commands WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None

    def get_commands(self, category_id, page=1, page_size=500):
        """分类分页查询"""
        offset = (page - 1) * page_size
        rows = self.conn.execute(
            "SELECT * FROM commands WHERE category_id=? ORDER BY favorite DESC, use_count DESC, id LIMIT ? OFFSET ?",
            (category_id, page_size, offset)
        ).fetchall()
        total = self.conn.execute(
            "SELECT COUNT(*) FROM commands WHERE category_id=?", (category_id,)
        ).fetchone()[0]
        return [dict(r) for r in rows], total

    # -- 代码片段 --

    def add_snippet(self, **kw):
        sql = """INSERT INTO code_snippets
            (category_id, title, language, version, code_block, line_by_line,
             syntax_note, runnable_example, common_errors, aliases, tags)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
        self.conn.execute(sql, (
            kw['category_id'], kw['title'], kw['language'], kw.get('version', ''),
            kw['code_block'], kw.get('line_by_line', '[]'),
            kw.get('syntax_note', ''), kw.get('runnable_example', ''),
            kw.get('common_errors', '[]'), kw.get('aliases', ''), kw.get('tags', ''),
        ))
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def update_snippet(self, item_id, **kw):
        fields = ['title', 'language', 'version', 'code_block', 'line_by_line',
                  'syntax_note', 'runnable_example', 'common_errors', 'aliases', 'tags', 'favorite']
        sets = []
        vals = []
        for f in fields:
            if f in kw:
                sets.append(f"{f}=?")
                vals.append(kw[f])
        if not sets:
            return
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(item_id)
        self.conn.execute(
            f"UPDATE code_snippets SET {', '.join(sets)} WHERE id=?", vals
        )
        self.conn.commit()

    def delete_snippet(self, item_id):
        self.conn.execute("DELETE FROM code_snippets WHERE id=?", (item_id,))
        self.conn.commit()

    def get_snippet(self, item_id):
        row = self.conn.execute("SELECT * FROM code_snippets WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None

    def get_snippets(self, category_id, page=1, page_size=500):
        offset = (page - 1) * page_size
        rows = self.conn.execute(
            "SELECT * FROM code_snippets WHERE category_id=? ORDER BY favorite DESC, use_count DESC, id LIMIT ? OFFSET ?",
            (category_id, page_size, offset)
        ).fetchall()
        total = self.conn.execute(
            "SELECT COUNT(*) FROM code_snippets WHERE category_id=?", (category_id,)
        ).fetchone()[0]
        return [dict(r) for r in rows], total

    # -- 模式条目 --

    def add_pattern(self, **kw):
        sql = """INSERT INTO pattern_items
            (category_id, title, language, version, pattern_text, parsed_table,
             code_block, line_by_line, syntax_note, runnable_example, common_errors, aliases, tags)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.conn.execute(sql, (
            kw['category_id'], kw['title'], kw['language'], kw.get('version', ''),
            kw.get('pattern_text', ''), kw.get('parsed_table', '[]'),
            kw['code_block'], kw.get('line_by_line', '[]'),
            kw.get('syntax_note', ''), kw.get('runnable_example', ''),
            kw.get('common_errors', '[]'), kw.get('aliases', ''), kw.get('tags', ''),
        ))
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def update_pattern(self, item_id, **kw):
        fields = ['title', 'language', 'version', 'pattern_text', 'parsed_table',
                  'code_block', 'line_by_line', 'syntax_note', 'runnable_example',
                  'common_errors', 'aliases', 'tags', 'favorite']
        sets = []
        vals = []
        for f in fields:
            if f in kw:
                sets.append(f"{f}=?")
                vals.append(kw[f])
        if not sets:
            return
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(item_id)
        self.conn.execute(
            f"UPDATE pattern_items SET {', '.join(sets)} WHERE id=?", vals
        )
        self.conn.commit()

    def delete_pattern(self, item_id):
        self.conn.execute("DELETE FROM pattern_items WHERE id=?", (item_id,))
        self.conn.commit()

    def get_pattern(self, item_id):
        row = self.conn.execute("SELECT * FROM pattern_items WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None

    def get_patterns(self, category_id, page=1, page_size=500):
        offset = (page - 1) * page_size
        rows = self.conn.execute(
            "SELECT * FROM pattern_items WHERE category_id=? ORDER BY favorite DESC, use_count DESC, id LIMIT ? OFFSET ?",
            (category_id, page_size, offset)
        ).fetchall()
        total = self.conn.execute(
            "SELECT COUNT(*) FROM pattern_items WHERE category_id=?", (category_id,)
        ).fetchone()[0]
        return [dict(r) for r in rows], total

    # ── 全文搜索 ──────────────────────────────────────────

    SEARCH_LIMIT = 30

    def search(self, keyword, page=1, page_size=500, item_type=None):
        """联合搜索三类表，返回统一格式的结果"""
        offset = (page - 1) * page_size
        results = []

        # 智能分词：按空格/中文切分
        terms = self._tokenize(keyword)
        if not terms:
            return [], 0

        fts_query = ' AND '.join(f'"{t}"' for t in terms)

        if item_type in (None, 'command'):
            rows = self.conn.execute(
                f"""SELECT c.id, c.cmd_name, c.name_cn, c.function_desc, c.aliases,
                           c.category_id, cat.name as cat_name, 'command' as item_type
                    FROM commands_fts f
                    JOIN commands c ON f.rowid = c.id
                    JOIN categories cat ON c.category_id = cat.id
                    WHERE commands_fts MATCH ?
                    ORDER BY rank
                    LIMIT ? OFFSET ?""",
                (fts_query, page_size, offset)
            ).fetchall()
            results.extend(dict(r) for r in rows)

        if item_type in (None, 'code'):
            rows = self.conn.execute(
                f"""SELECT s.id, s.title, s.language, s.syntax_note, s.aliases,
                           s.category_id, cat.name as cat_name, 'code' as item_type
                    FROM snippets_fts f
                    JOIN code_snippets s ON f.rowid = s.id
                    JOIN categories cat ON s.category_id = cat.id
                    WHERE snippets_fts MATCH ?
                    ORDER BY rank
                    LIMIT ? OFFSET ?""",
                (fts_query, page_size, offset)
            ).fetchall()
            results.extend(dict(r) for r in rows)

        if item_type in (None, 'pattern'):
            rows = self.conn.execute(
                f"""SELECT p.id, p.title, p.language, p.pattern_text, p.aliases,
                           p.category_id, cat.name as cat_name, 'pattern' as item_type
                    FROM patterns_fts f
                    JOIN pattern_items p ON f.rowid = p.id
                    JOIN categories cat ON p.category_id = cat.id
                    WHERE patterns_fts MATCH ?
                    ORDER BY rank
                    LIMIT ? OFFSET ?""",
                (fts_query, page_size, offset)
            ).fetchall()
            results.extend(dict(r) for r in rows)

        total = len(results)
        return results[:page_size], total

    def _tokenize(self, text):
        """中文+英文分词，过滤短词"""
        import re
        # 切分为中文字符序列和英文词
        tokens = []
        # 英文/数字词
        for t in re.findall(r'[a-zA-Z0-9_\-.]+', text):
            if len(t) >= 1:
                tokens.append(t)
        # 中文字符（按单字也行，但FTS5 unicode61对中文不够好）
        # 用 OR 匹配：每个中文字作为单独词
        for t in re.findall(r'[\u4e00-\u9fff]+', text):
            for ch in t:
                tokens.append(ch)
        return tokens

    def search_simple(self, keyword, page=1, page_size=500):
        """简单 LIKE 搜索（中文友好）"""
        offset = (page - 1) * page_size
        pattern = f'%{keyword}%'
        results = []

        # commands
        rows = self.conn.execute(
            """SELECT id, cmd_name, name_cn, function_desc, aliases, category_id,
                      'command' as item_type
               FROM commands
               WHERE cmd_name LIKE ? OR name_cn LIKE ? OR function_desc LIKE ? OR aliases LIKE ?
               ORDER BY favorite DESC, use_count DESC
               LIMIT ? OFFSET ?""",
            (pattern, pattern, pattern, pattern, page_size, offset)
        ).fetchall()
        results.extend(dict(r) for r in rows)

        # 统计 total（仅当前页）
        return results, len(results)

    # ── 收藏 ──────────────────────────────────────────────

    def toggle_favorite(self, item_type, item_id):
        table = self._table_for_type(item_type)
        if not table:
            return False
        row = self.conn.execute(f"SELECT favorite FROM {table} WHERE id=?", (item_id,)).fetchone()
        if not row:
            return False
        new_val = 0 if row['favorite'] else 1
        self.conn.execute(f"UPDATE {table} SET favorite=? WHERE id=?", (new_val, item_id))
        self.conn.commit()
        return bool(new_val)

    def get_favorites(self, page=1, page_size=50):
        offset = (page - 1) * page_size
        results = []
        for table, item_type in [('commands', 'command'), ('code_snippets', 'code'), ('pattern_items', 'pattern')]:
            rows = self.conn.execute(
                f"""SELECT id, '{item_type}' as item_type FROM {table} WHERE favorite=1
                    ORDER BY updated_at DESC LIMIT ? OFFSET ?""",
                (page_size, offset)
            ).fetchall()
            for r in rows:
                d = dict(r)
                d['detail'] = self.get_item(r['id'], r['item_type'])
                results.append(d)
        return results

    # ── 最近查看 ──────────────────────────────────────────

    def record_use(self, item_type, item_id):
        table = self._table_for_type(item_type)
        if table:
            self.conn.execute(
                f"UPDATE {table} SET use_count=use_count+1 WHERE id=?", (item_id,)
            )
            self.conn.commit()

    # ── 导入导出 ──────────────────────────────────────────

    def export_json(self, item_ids=None, item_type='command'):
        """导出为 JSON，支持选择条目"""
        table = self._table_for_type(item_type)
        if not table:
            return '[]'
        if item_ids:
            placeholders = ','.join('?' * len(item_ids))
            rows = self.conn.execute(
                f"SELECT * FROM {table} WHERE id IN ({placeholders})", item_ids
            ).fetchall()
        else:
            rows = self.conn.execute(f"SELECT * FROM {table}").fetchall()
        return json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2, default=str)

    def import_json(self, json_str, merge=True, item_type='command'):
        """从 JSON 导入
        merge=True: 同名条目更新，不存在则新增
        merge=False: 先清空再导入
        """
        table = self._table_for_type(item_type)
        if not table:
            return 0
        data = json.loads(json_str)
        if not isinstance(data, list):
            data = [data]

        if not merge:
            self.conn.execute(f"DELETE FROM {table}")
            self.conn.commit()

        count = 0
        for item in data:
            try:
                # 尝试查找同名条目
                if item_type == 'command':
                    existing = self.conn.execute(
                        "SELECT id FROM commands WHERE cmd_name=? AND category_id=?",
                        (item.get('cmd_name', ''), item.get('category_id', 1))
                    ).fetchone()
                    if existing and merge:
                        self.update_command(existing['id'], **item)
                    else:
                        self.add_command(**item)
                elif item_type == 'code':
                    existing = self.conn.execute(
                        "SELECT id FROM code_snippets WHERE title=? AND category_id=?",
                        (item.get('title', ''), item.get('category_id', 1))
                    ).fetchone()
                    if existing and merge:
                        self.update_snippet(existing['id'], **item)
                    else:
                        self.add_snippet(**item)
                elif item_type == 'pattern':
                    existing = self.conn.execute(
                        "SELECT id FROM pattern_items WHERE title=? AND category_id=?",
                        (item.get('title', ''), item.get('category_id', 1))
                    ).fetchone()
                    if existing and merge:
                        self.update_pattern(existing['id'], **item)
                    else:
                        self.add_pattern(**item)
                count += 1
            except Exception as e:
                print(f"[DB] Import error: {e}")
        return count

    # ── 总统计 ──────────────────────────────────────────

    def get_total_count(self):
        c = self.conn.execute("SELECT COUNT(*) FROM commands").fetchone()[0]
        s = self.conn.execute("SELECT COUNT(*) FROM code_snippets").fetchone()[0]
        p = self.conn.execute("SELECT COUNT(*) FROM pattern_items").fetchone()[0]
        return c + s + p

    def get_type_counts(self):
        return {
            'command': self.conn.execute("SELECT COUNT(*) FROM commands").fetchone()[0],
            'code': self.conn.execute("SELECT COUNT(*) FROM code_snippets").fetchone()[0],
            'pattern': self.conn.execute("SELECT COUNT(*) FROM pattern_items").fetchone()[0],
        }

    # ── 辅助 ──────────────────────────────────────────────

    def _table_for_type(self, item_type):
        return {
            'command': 'commands',
            'code': 'code_snippets',
            'pattern': 'pattern_items',
        }.get(item_type)

    def get_item(self, item_id, item_type):
        """统一获取条目详情"""
        if item_type == 'command':
            return self.get_command(item_id)
        elif item_type == 'code':
            return self.get_snippet(item_id)
        elif item_type == 'pattern':
            return self.get_pattern(item_id)
        return None

    def delete_item(self, item_id, item_type):
        if item_type == 'command':
            self.delete_command(item_id)
        elif item_type == 'code':
            self.delete_snippet(item_id)
        elif item_type == 'pattern':
            self.delete_pattern(item_id)

    def get_cat_id_by_name(self, parent_name, child_name):
        """通过父分类名+子分类名查找分类ID"""
        _, name_id = self.get_all_categories_map()
        # 先找子分类
        if child_name in name_id:
            return name_id[child_name]
        return None
