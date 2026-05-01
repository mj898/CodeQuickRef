# CodeQuickRef

> 离线、轻量、零基础友好的多语言代码速查桌面工具

基于 PySide6 构建的纯本地代码参考助手，无需联网即可快速检索编程语法、命令行、代码片段与正则模式。面向新手和日常开发场景，帮你快速找到想要的代码写法。

---

## 功能特点

- **📂 分类树导航** — 按语言/工具/类别展开，懒加载高性能，右键快捷管理
- **🔍 全局模糊搜索** — 支持中英文关键词和别名匹配，秒级定位
- **📖 折叠式详情面板** — 每条记录包含语法、示例、参数说明、避坑提醒
- **⭐ 收藏夹 & 最近查看** — 高频条目一键收藏，历史记录自动追踪
- **✏️ 新增/编辑/删除** — 可在界面直接维护条目，实时更新数据库
- **📦 导入/导出 JSON** — 数据备份与迁移，方便分享条目集合
- **⌨️ 快捷键** — `Ctrl+F` 搜索、`Ctrl+N` 新增、`Ctrl+S` 保存

## 覆盖内容

| 类别 | 条数 | 覆盖范围 |
|------|------|---------|
| 命令行工具 | 117+ | Git、Linux 终端、CMD、PowerShell、Docker、MySQL、SQLite、Redis、ADB |
| 代码片段 | 56+ | Python、JavaScript、Rust、Java、C、Shell |
| 前端技术 | — | HTML、CSS、Vue、React |
| 模式/标记 | 36+ | 正则表达式、Markdown、JSON、YAML |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/mj898/CodeQuickRef.git
cd CodeQuickRef

# 安装依赖
pip install PySide6>=6.5.0

# 运行
python main.py
```

### 一键启动

Windows 下双击 `run.bat` 或 Linux/Mac 下执行:

```bash
chmod +x run.sh
./run.sh
```

## 打包为独立 exe

```bash
pip install pyinstaller
pyinstaller CodeQuickRef.spec
```

生成的可执行文件在 `dist/CodeQuickRef/` 目录。

## 技术栈

- **Python 3.11+**
- **PySide6 (Qt for Python)** — 跨平台 GUI 框架
- **SQLite** — 本地嵌入式数据库
- **PyInstaller** — 应用打包

## 许可证

[MIT](LICENSE)
