"""
SQLite 数据库建表脚本
支持：categories / commands / code_snippets / pattern_items + FTS5 全文搜索
"""

SCHEMA_SQL = """
-- ======================================
-- 1. 分类表（树形结构）
-- ======================================
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id   INTEGER DEFAULT NULL,
    name        TEXT    NOT NULL,
    item_type   TEXT    NOT NULL DEFAULT 'command',  -- command / code / pattern
    sort_order  INTEGER DEFAULT 0,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ======================================
-- 2. 命令行条目表
-- ======================================
CREATE TABLE IF NOT EXISTS commands (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id     INTEGER NOT NULL,
    cmd_name        TEXT    NOT NULL,          -- 命令全称
    name_cn         TEXT    NOT NULL,          -- 中文名
    function_desc   TEXT    NOT NULL,          -- 核心作用
    syntax          TEXT    NOT NULL DEFAULT '', -- 完整语法
    params_json     TEXT    DEFAULT '[]',      -- 参数详解 JSON
    example_basic   TEXT    NOT NULL DEFAULT '',-- 基础用法
    example_adv     TEXT    DEFAULT '',         -- 进阶用法
    os_type         TEXT    DEFAULT '通用',     -- 操作系统差异
    aliases         TEXT    DEFAULT '',         -- 别名/关键词
    tips            TEXT    DEFAULT '',         -- 避坑提示
    favorite        INTEGER DEFAULT 0,         -- 收藏 0/1
    tags            TEXT    DEFAULT '',         -- 自定义标签
    use_count       INTEGER DEFAULT 0,         -- 使用次数
    created_at      TEXT    DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ======================================
-- 3. 代码片段表
-- ======================================
CREATE TABLE IF NOT EXISTS code_snippets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id     INTEGER NOT NULL,
    title           TEXT    NOT NULL,          -- 功能名称
    language        TEXT    NOT NULL,          -- 语言
    version         TEXT    DEFAULT '',         -- 适用版本
    code_block      TEXT    NOT NULL,          -- 完整代码块
    line_by_line    TEXT    DEFAULT '[]',      -- 逐行解析 JSON
    syntax_note     TEXT    DEFAULT '',         -- 语法规则/注意事项
    runnable_example TEXT   DEFAULT '',         -- 完整可运行示例
    common_errors   TEXT    DEFAULT '[]',      -- 常见报错 JSON
    aliases         TEXT    DEFAULT '',         -- 别名/关键词
    favorite        INTEGER DEFAULT 0,         -- 收藏
    tags            TEXT    DEFAULT '',         -- 自定义标签
    use_count       INTEGER DEFAULT 0,
    created_at      TEXT    DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ======================================
-- 4. 模式/标记语言表
-- ======================================
CREATE TABLE IF NOT EXISTS pattern_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id     INTEGER NOT NULL,
    title           TEXT    NOT NULL,
    language        TEXT    NOT NULL,          -- 如 regex / markdown / json / yaml
    version         TEXT    DEFAULT '',
    pattern_text    TEXT    NOT NULL DEFAULT '',-- 模式原文
    parsed_table    TEXT    DEFAULT '[]',      -- 逐段解析表格 JSON
    code_block      TEXT    NOT NULL,          -- 完整代码块
    line_by_line    TEXT    DEFAULT '[]',
    syntax_note     TEXT    DEFAULT '',
    runnable_example TEXT   DEFAULT '',
    common_errors   TEXT    DEFAULT '[]',
    aliases         TEXT    DEFAULT '',
    favorite        INTEGER DEFAULT 0,
    tags            TEXT    DEFAULT '',
    use_count       INTEGER DEFAULT 0,
    created_at      TEXT    DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ======================================
-- 5. FTS5 全文搜索虚拟表
-- ======================================
CREATE VIRTUAL TABLE IF NOT EXISTS commands_fts USING fts5(
    cmd_name, name_cn, function_desc, aliases, tips, tags,
    content='commands',
    content_rowid='id',
    tokenize='unicode61'
);

CREATE VIRTUAL TABLE IF NOT EXISTS snippets_fts USING fts5(
    title, language, code_block, line_by_line, syntax_note, aliases, tags,
    content='code_snippets',
    content_rowid='id',
    tokenize='unicode61'
);

CREATE VIRTUAL TABLE IF NOT EXISTS patterns_fts USING fts5(
    title, language, pattern_text, code_block, line_by_line, aliases, tags,
    content='pattern_items',
    content_rowid='id',
    tokenize='unicode61'
);

-- ======================================
-- 6. 触发器：保持 FTS 同步
-- ======================================
-- commands FTS 触发器
CREATE TRIGGER IF NOT EXISTS commands_ai AFTER INSERT ON commands BEGIN
    INSERT INTO commands_fts(rowid, cmd_name, name_cn, function_desc, aliases, tips, tags)
    VALUES (new.id, new.cmd_name, new.name_cn, new.function_desc, new.aliases, new.tips, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS commands_ad AFTER DELETE ON commands BEGIN
    INSERT INTO commands_fts(commands_fts, rowid, cmd_name, name_cn, function_desc, aliases, tips, tags)
    VALUES ('delete', old.id, old.cmd_name, old.name_cn, old.function_desc, old.aliases, old.tips, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS commands_au AFTER UPDATE ON commands BEGIN
    INSERT INTO commands_fts(commands_fts, rowid, cmd_name, name_cn, function_desc, aliases, tips, tags)
    VALUES ('delete', old.id, old.cmd_name, old.name_cn, old.function_desc, old.aliases, old.tips, old.tags);
    INSERT INTO commands_fts(rowid, cmd_name, name_cn, function_desc, aliases, tips, tags)
    VALUES (new.id, new.cmd_name, new.name_cn, new.function_desc, new.aliases, new.tips, new.tags);
END;

-- snippets FTS 触发器
CREATE TRIGGER IF NOT EXISTS snippets_ai AFTER INSERT ON code_snippets BEGIN
    INSERT INTO snippets_fts(rowid, title, language, code_block, line_by_line, syntax_note, aliases, tags)
    VALUES (new.id, new.title, new.language, new.code_block, new.line_by_line, new.syntax_note, new.aliases, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS snippets_ad AFTER DELETE ON code_snippets BEGIN
    INSERT INTO snippets_fts(snippets_fts, rowid, title, language, code_block, line_by_line, syntax_note, aliases, tags)
    VALUES ('delete', old.id, old.title, old.language, old.code_block, old.line_by_line, old.syntax_note, old.aliases, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS snippets_au AFTER UPDATE ON code_snippets BEGIN
    INSERT INTO snippets_fts(snippets_fts, rowid, title, language, code_block, line_by_line, syntax_note, aliases, tags)
    VALUES ('delete', old.id, old.title, old.language, old.code_block, old.line_by_line, old.syntax_note, old.aliases, old.tags);
    INSERT INTO snippets_fts(rowid, title, language, code_block, line_by_line, syntax_note, aliases, tags)
    VALUES (new.id, new.title, new.language, new.code_block, new.line_by_line, new.syntax_note, new.aliases, new.tags);
END;

-- pattern_items FTS 触发器
CREATE TRIGGER IF NOT EXISTS patterns_ai AFTER INSERT ON pattern_items BEGIN
    INSERT INTO patterns_fts(rowid, title, language, pattern_text, code_block, line_by_line, aliases, tags)
    VALUES (new.id, new.title, new.language, new.pattern_text, new.code_block, new.line_by_line, new.aliases, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS patterns_ad AFTER DELETE ON pattern_items BEGIN
    INSERT INTO patterns_fts(patterns_fts, rowid, title, language, pattern_text, code_block, line_by_line, aliases, tags)
    VALUES ('delete', old.id, old.title, old.language, old.pattern_text, old.code_block, old.line_by_line, old.aliases, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS patterns_au AFTER UPDATE ON pattern_items BEGIN
    INSERT INTO patterns_fts(patterns_fts, rowid, title, language, pattern_text, code_block, line_by_line, aliases, tags)
    VALUES ('delete', old.id, old.title, old.language, old.pattern_text, old.code_block, old.line_by_line, old.aliases, old.tags);
    INSERT INTO patterns_fts(rowid, title, language, pattern_text, code_block, line_by_line, aliases, tags)
    VALUES (new.id, new.title, new.language, new.pattern_text, new.code_block, new.line_by_line, new.aliases, new.tags);
END;

-- ======================================
-- 7. 索引
-- ======================================
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_commands_category ON commands(category_id);
CREATE INDEX IF NOT EXISTS idx_commands_favorite ON commands(favorite);
CREATE INDEX IF NOT EXISTS idx_snippets_category ON code_snippets(category_id);
CREATE INDEX IF NOT EXISTS idx_snippets_favorite ON code_snippets(favorite);
CREATE INDEX IF NOT EXISTS idx_patterns_category ON pattern_items(category_id);
CREATE INDEX IF NOT EXISTS idx_patterns_favorite ON pattern_items(favorite);
"""

# 初始分类种子数据
CATEGORY_SEED = [
    # 一级分类
    (None, '命令行工具', 'command', 1),
    (None, '编程语言', 'code', 2),
    (None, '数据库', 'command', 3),
    (None, '前端技术', 'code', 4),
    (None, '模式/标记', 'pattern', 5),
    (None, '其他', 'code', 6),

    # 命令行工具 -> 二级
    ('命令行工具', 'Git', 'command', 10),
    ('命令行工具', 'Linux终端', 'command', 11),
    ('命令行工具', 'CMD (Windows)', 'command', 12),
    ('命令行工具', 'PowerShell', 'command', 13),
    ('命令行工具', 'Docker', 'command', 14),

    # 编程语言 -> 二级
    ('编程语言', 'Python', 'code', 20),
    ('编程语言', 'JavaScript', 'code', 21),
    ('编程语言', 'Shell脚本', 'code', 22),
    ('编程语言', 'Rust', 'code', 23),
    ('编程语言', 'Java', 'code', 24),
    ('编程语言', 'C语言', 'code', 25),
    ('编程语言', 'C++', 'code', 26),
    ('编程语言', 'Go', 'code', 27),
    ('编程语言', 'C#', 'code', 28),
    ('编程语言', 'PHP', 'code', 29),
    ('编程语言', 'Ruby', 'code', 30),

    # 数据库 -> 二级
    ('数据库', 'MySQL', 'command', 40),
    ('数据库', 'SQLite', 'command', 41),
    ('数据库', 'Redis命令', 'command', 42),

    # 前端技术 -> 二级
    ('前端技术', 'HTML', 'code', 50),
    ('前端技术', 'CSS', 'code', 51),
    ('前端技术', 'Vue', 'code', 52),
    ('前端技术', 'React', 'code', 53),

    # 模式/标记 -> 二级
    ('模式/标记', '正则表达式', 'pattern', 60),
    ('模式/标记', 'Markdown', 'pattern', 61),
    ('模式/标记', 'JSON语法', 'pattern', 62),
    ('模式/标记', 'YAML', 'pattern', 63),
]
