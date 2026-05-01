#!/usr/bin/env python3
"""添加 Hermes Agent 全部命令到速查工具"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

db = DBManager()
db.init_db()

# 找到或创建 "Hermes Agent" 分类
ha_cat = None
for root in db.get_categories(parent_id=None):
    if root['name'] == '命令行工具':
        for child in db.get_categories(parent_id=root['id']):
            if child['name'] == 'Hermes Agent':
                ha_cat = child['id']
                break
        if not ha_cat:
            children = db.get_categories(parent_id=root['id'])
            max_order = max((c.get('sort_order', 0) for c in children), default=0)
            ha_cat = db.add_category('Hermes Agent', root['id'], 'command', max_order + 10)
        break

if not ha_cat:
    print('[ERR] 无法找到或创建 Hermes Agent 分类')
    sys.exit(1)

print(f'[OK] Hermes Agent 分类 ID: {ha_cat}')

# 批量插入
def add(**kw):
    kw['category_id'] = ha_cat
    db.add_command(**kw)

# ── 1. 核心命令 ──
add(
    cmd_name='hermes',
    name_cn='启动 Hermes Agent 交互会话',
    function_desc='启动与 Hermes Agent 的交互式对话。默认进入 REPL 模式，可加 -z 进入一次问答模式',
    syntax='hermes [-h] [--version] [-z PROMPT] [-m MODEL] [--provider PROVIDER] [--resume SESSION] [--continue [NAME]] [--worktree] [--skills SKILLS] [--yolo] [--tui]',
    params_json='[{"参数":"-z PROMPT","说明":"一次问答模式，单条提示直接输出结果","必填":"可选"},{"参数":"-m MODEL","说明":"临时切换模型，如 anthropic/claude-sonnet-4","必填":"可选"},{"参数":"--provider PROVIDER","说明":"临时切换提供商","必填":"可选"},{"参数":"--resume SESSION / -r","说明":"通过ID恢复之前的会话","必填":"可选"},{"参数":"--continue [NAME] / -c","说明":"按名称恢复最近的会话，不传则恢复最近一个","必填":"可选"},{"参数":"--worktree / -w","说明":"在隔离的 git worktree 中运行（并行agent）","必填":"可选"},{"参数":"--skills SKILLS / -s","说明":"预加载一个或多个技能","必填":"可选"},{"参数":"--yolo","说明":"绕过所有危险命令审批提示","必填":"可选"},{"参数":"--tui","说明":"启动现代 TUI 界面替代经典 REPL","必填":"可选"},{"参数":"--accept-hooks","说明":"自动批准未见的 shell hooks","必填":"可选"}]',
    example_basic='hermes',
    example_adv='hermes -z "用Python写一个web服务器" -m claude-sonnet\nhermes --resume abc123\nhermes --worktree -s github-auth',
    os_type='通用',
    aliases='启动,聊天,对话,REPL',
    tips='首次运行会自动进入 setup 向导。按 Ctrl+C 退出当前会话，按 Ctrl+D 结束输入。',
)

add(
    cmd_name='hermes chat',
    name_cn='单次问答模式',
    function_desc='以非交互模式向 Hermes Agent 发送一条提示，直接输出纯文本结果（无横幅、无旋转动画、无工具预览）',
    syntax='hermes chat -q "你的问题"',
    params_json='[{"参数":"-q QUERY","说明":"要发送的单条提示","必填":"必填"}]',
    example_basic='hermes chat -q "用Python删除一个目录下的所有.txt文件"',
    example_adv='hermes chat -q "解释这段代码" -m claude-sonnet-4',
    os_type='通用',
    aliases='单次查询,one-shot,chat',
    tips='结果只有纯文本，适合脚本管道使用。工具、记忆、规则正常加载，审批自动绕过。',
)

# ── 2. 模型管理 ──
add(
    cmd_name='hermes model',
    name_cn='选择默认模型和提供商',
    function_desc='交互式选择默认的推理模型和提供商，用于所有会话',
    syntax='hermes model',
    params_json='[]',
    example_basic='hermes model',
    example_adv='hermes model  # 然后从列表中选择提供商和模型',
    os_type='通用',
    aliases='模型,model,切换模型,选择模型',
    tips='也可以用 hermes config set model <模型名> 直接设置。临时切换用 hermes -m。',
)

add(
    cmd_name='hermes fallback',
    name_cn='管理备用提供商',
    function_desc='管理备用提供商链，当主模型失败时自动尝试备用',
    syntax='hermes fallback [list|add|remove]',
    params_json='[{"参数":"list","说明":"显示备用提供商链","必填":"可选"},{"参数":"add","说明":"添加一个备用提供商","必填":"可选"},{"参数":"remove","说明":"从链中移除备用提供商","必填":"可选"}]',
    example_basic='hermes fallback list\nhermes fallback add',
    example_adv='hermes fallback remove  # 交互式选择要移除的备用',
    os_type='通用',
    aliases='备用,fallback,故障转移',
    tips='备用提供商在主模型失败时自动尝试。可添加多个，按顺序尝试。',
)

# ── 3. 网关管理 ──
add(
    cmd_name='hermes gateway',
    name_cn='管理消息网关',
    function_desc='管理 Hermes Agent 的消息网关（Telegram / Discord / WhatsApp 等平台接入）',
    syntax='hermes gateway {run|start|stop|restart|status|install|uninstall|setup} [--accept-hooks]',
    params_json='[{"参数":"run","说明":"前台运行网关（推荐WSL/Docker/Termux使用）","必填":"可选"},{"参数":"start","说明":"启动已安装的 systemd/launchd 后台服务","必填":"可选"},{"参数":"stop","说明":"停止网关服务","必填":"可选"},{"参数":"restart","说明":"重启网关服务","必填":"可选"},{"参数":"status","说明":"查看网关运行状态","必填":"可选"},{"参数":"install","说明":"安装网关为 systemd/launchd 后台服务","必填":"可选"},{"参数":"uninstall","说明":"卸载网关服务","必填":"可选"},{"参数":"setup","说明":"配置消息平台接入","必填":"可选"},{"参数":"--accept-hooks","说明":"自动批准未见 shell hooks","必填":"可选"}]',
    example_basic='hermes gateway status\nhermes gateway run',
    example_adv='hermes gateway install && hermes gateway start\nhermes gateway setup',
    os_type='通用',
    aliases='网关,gateway,消息平台,wechat,telegram',
    tips='WSL 下用 hermes gateway run 前台运行；服务模式用 hermes gateway install 安装为 systemd 服务。',
)

# ── 4. 设置与认证 ──
add(
    cmd_name='hermes setup',
    name_cn='运行安装向导',
    function_desc='交互式配置向导，支持完整配置或单项配置（model/tts/terminal/gateway/tools/agent）',
    syntax='hermes setup [{model|tts|terminal|gateway|tools|agent}] [--non-interactive] [--reset] [--quick]',
    params_json='[{"参数":"model","说明":"仅配置模型","必填":"可选"},{"参数":"tts","说明":"仅配置语音合成","必填":"可选"},{"参数":"terminal","说明":"仅配置终端","必填":"可选"},{"参数":"gateway","说明":"仅配置消息网关","必填":"可选"},{"参数":"tools","说明":"仅配置工具","必填":"可选"},{"参数":"agent","说明":"仅配置Agent","必填":"可选"},{"参数":"--non-interactive","说明":"非交互模式（用默认值/环境变量）","必填":"可选"},{"参数":"--reset","说明":"重置配置为默认值","必填":"可选"},{"参数":"--quick","说明":"仅提示缺失/未设置项","必填":"可选"}]',
    example_basic='hermes setup\nhermes setup model',
    example_adv='hermes setup --quick\nhermes setup --non-interactive',
    os_type='通用',
    aliases='设置,setup,安装向导,配置向导',
    tips='首次运行 hermes 会自动进入 setup。--quick 模式在有配置的基础上只问缺失项。',
)

add(
    cmd_name='hermes login',
    name_cn='登录推理提供商',
    function_desc='向推理提供商进行认证，通常通过浏览器打开OAuth页面完成',
    syntax='hermes login [provider]',
    params_json='[{"参数":"provider","说明":"提供商名称（如 openai, anthropic, openrouter）","必填":"可选"}]',
    example_basic='hermes login\nhermes login openai',
    example_adv='hermes login anthropic  # 跳转到浏览器完成OAuth',
    os_type='通用',
    aliases='登录,login,认证,授权',
    tips='不传参数会弹出提供商选择列表。认证信息保存在 .env 文件中。',
)

add(
    cmd_name='hermes logout',
    name_cn='清除提供商认证',
    function_desc='清除已存储的推理提供商认证状态',
    syntax='hermes logout [provider]',
    params_json='[{"参数":"provider","说明":"要登出的提供商名称","必填":"可选"}]',
    example_basic='hermes logout\nhermes logout openai',
    os_type='通用',
    aliases='登出,logout,清除认证',
    tips='不传参数会列出所有已认证的提供商供选择。',
)

add(
    cmd_name='hermes auth',
    name_cn='管理池化凭证',
    function_desc='管理多个提供商凭据的池化（pooled credentials），支持添加/列出/移除/重置/查看状态',
    syntax='hermes auth {add|list|remove|reset|status|logout|spotify}',
    params_json='[{"参数":"add","说明":"添加池化凭证","必填":"可选"},{"参数":"list","说明":"列出所有池化凭证","必填":"可选"},{"参数":"remove","说明":"按索引、ID或标签移除凭证","必填":"可选"},{"参数":"reset","说明":"清除某提供商的所有凭证耗尽状态","必填":"可选"},{"参数":"status","说明":"查看指定提供商的认证状态","必填":"可选"},{"参数":"logout","说明":"退出提供商并清除认证状态","必填":"可选"},{"参数":"spotify","说明":"通过PKCE认证Spotify","必填":"可选"}]',
    example_basic='hermes auth list\nhermes auth add openai',
    example_adv='hermes auth remove openai 0\nhermes auth reset openai',
    os_type='通用',
    aliases='认证,auth,凭证,api key',
    tips='池化凭证允许多个API key轮换使用。remove按索引/ID/label匹配。',
)

# ── 5. 配置管理 ──
add(
    cmd_name='hermes config',
    name_cn='查看和编辑配置',
    function_desc='查看、编辑、设置 Hermes Agent 的配置项，支持 show/edit/set/path/check/migrate',
    syntax='hermes config {show|edit|set|path|env-path|check|migrate}',
    params_json='[{"参数":"show","说明":"显示当前配置","必填":"可选"},{"参数":"edit","说明":"在编辑器中打开配置文件","必填":"可选"},{"参数":"set","说明":"设置配置项值，如 hermes config set model gpt-4","必填":"可选"},{"参数":"path","说明":"打印配置文件路径","必填":"可选"},{"参数":"env-path","说明":"打印 .env 文件路径","必填":"可选"},{"参数":"check","说明":"检查缺失/过期的配置","必填":"可选"},{"参数":"migrate","说明":"用新选项更新配置","必填":"可选"}]',
    example_basic='hermes config show\nhermes config path',
    example_adv='hermes config set model claude-sonnet-4\nhermes config check',
    os_type='通用',
    aliases='配置,config,设置,编辑配置',
    tips='配置文件路径：~/.hermes/config.yaml。环境变量在 ~/.hermes/.env。用 hermes config edit 直接用编辑器打开。',
)

# ── 6. 状态与诊断 ──
add(
    cmd_name='hermes status',
    name_cn='显示所有组件状态',
    function_desc='显示 Hermes Agent 所有组件（模型、提供商、网关、定时任务等）的运行状态概览',
    syntax='hermes status',
    params_json='[]',
    example_basic='hermes status',
    os_type='通用',
    aliases='状态,status,检查,系统状态',
    tips='快速了解所有组件是否正常运行。如果某个组件有问题，这里会明确标出。',
)

add(
    cmd_name='hermes doctor',
    name_cn='检查配置和依赖',
    function_desc='运行诊断检查，验证所有配置项、环境变量、系统依赖是否正确',
    syntax='hermes doctor',
    params_json='[]',
    example_basic='hermes doctor',
    os_type='通用',
    aliases='诊断,doctor,健康检查,依赖检查',
    tips='当遇到奇怪的问题时先运行 hermes doctor。会检查Python版本、依赖、配置文件格式等。',
)

add(
    cmd_name='hermes dump',
    name_cn='导出配置摘要',
    function_desc='导出设置摘要，用于支持/调试。生成一个包含了配置、日志摘要的信息包',
    syntax='hermes dump',
    params_json='[]',
    example_basic='hermes dump',
    os_type='通用',
    aliases='导出摘要,dump,调试信息',
    tips='在寻求帮助时运行此命令，生成的摘要包含诊断需要的信息但会脱敏。',
)

add(
    cmd_name='hermes debug share',
    name_cn='上传调试报告',
    function_desc='上传日志和系统信息用于技术支持',
    syntax='hermes debug share',
    params_json='[{"参数":"share","说明":"上传调试报告","必填":"必填"}]',
    example_basic='hermes debug share',
    os_type='通用',
    aliases='调试,debug,上报错误',
    tips='会上传日志和配置摘要到开发团队。不会上传API密钥或敏感信息。',
)

# ── 7. 备份与恢复 ──
add(
    cmd_name='hermes backup',
    name_cn='备份 Hermes 目录',
    function_desc='将整个 Hermes 主目录（~/.hermes/）打包为一个 zip 备份文件',
    syntax='hermes backup',
    params_json='[]',
    example_basic='hermes backup',
    os_type='通用',
    aliases='备份,backup,导出,打包',
    tips='备份包含配置、会话历史、记忆、技能等所有数据。备份文件保存在当前目录。',
)

add(
    cmd_name='hermes import',
    name_cn='恢复备份',
    function_desc='从备份 zip 文件中恢复 Hermes 配置和数据',
    syntax='hermes import <backup_file>',
    params_json='[{"参数":"backup_file","说明":"备份 zip 文件路径","必填":"必填"}]',
    example_basic='hermes import hermes-backup-2024-01-15.zip',
    os_type='通用',
    aliases='恢复,import,还原,导入备份',
    tips='会覆盖当前配置。建议恢复前先备份当前状态。',
)

# ── 8. 定时任务 ──
add(
    cmd_name='hermes cron',
    name_cn='管理定时任务',
    function_desc='管理定时调度的 Agent 任务，支持创建/列出/编辑/暂停/恢复/运行/删除',
    syntax='hermes cron {list|create|edit|pause|resume|run|remove|status|tick}',
    params_json='[{"参数":"list","说明":"列出定时任务","必填":"可选"},{"参数":"create / add","说明":"创建定时任务","必填":"可选"},{"参数":"edit","说明":"编辑已有任务","必填":"可选"},{"参数":"pause","说明":"暂停任务","必填":"可选"},{"参数":"resume","说明":"恢复暂停的任务","必填":"可选"},{"参数":"run","说明":"在下一个调度周期立即运行","必填":"可选"},{"参数":"remove / rm / delete","说明":"删除任务","必填":"可选"},{"参数":"status","说明":"检查调度器是否在运行","必填":"可选"},{"参数":"tick","说明":"运行到期任务后退出","必填":"可选"}]',
    example_basic='hermes cron list\nhermes cron create',
    example_adv='hermes cron edit job_abc123\nhermes cron remove job_abc123',
    os_type='通用',
    aliases='定时任务,cron,调度,定时,任务计划',
    tips='定时任务在独立的会话中运行，无法交互。确保提示词完全自包含。支持cron表达式和自然语言（如"每天上午9点"）。',
)

# ── 9. Webhook ──
add(
    cmd_name='hermes webhook',
    name_cn='管理动态Webhook',
    function_desc='管理动态 Webhook 订阅，通过事件驱动触发 Agent 运行',
    syntax='hermes webhook {create|list|remove|trigger|verify|events}',
    params_json='[{"参数":"create","说明":"创建 Webhook 订阅","必填":"可选"},{"参数":"list","说明":"列出所有 Webhook","必填":"可选"},{"参数":"remove","说明":"移除 Webhook","必填":"可选"},{"参数":"trigger","说明":"手动触发 Webhook","必填":"可选"}]',
    example_basic='hermes webhook list\nhermes webhook create',
    os_type='通用',
    aliases='webhook,钩子,事件驱动',
    tips='Webhook 让外部服务通过 HTTP 触发 Agent 运行。需先运行网关。',
)

# ── 10. Hooks ──
add(
    cmd_name='hermes hooks',
    name_cn='管理 Shell 钩子',
    function_desc='查看和管理 shell-script 钩子，可列出所有声明的钩子及运行状态',
    syntax='hermes hooks {list|run|approve|reject|reset}',
    params_json='[{"参数":"list","说明":"列出所有钩子及状态","必填":"可选"},{"参数":"run","说明":"运行指定钩子","必填":"可选"},{"参数":"approve","说明":"批准钩子","必填":"可选"},{"参数":"reject","说明":"拒绝钩子","必填":"可选"},{"参数":"reset","说明":"重置钩子审批状态","必填":"可选"}]',
    example_basic='hermes hooks list',
    os_type='通用',
    aliases='钩子,hooks,shell钩子',
    tips='钩子在 config.yaml 中声明，首次运行需要 TTY 审批或设置 hooks_auto_accept: true。',
)

# ── 11. 技能管理 ──
add(
    cmd_name='hermes skills',
    name_cn='管理技能',
    function_desc='搜索、安装、检查、更新、审计、配置和管理技能（skills）',
    syntax='hermes skills {browse|search|install|inspect|list|check|update|audit|uninstall|reset|publish|snapshot|tap|config}',
    params_json='[{"参数":"browse","说明":"浏览所有可用技能（分页）","必填":"可选"},{"参数":"search","说明":"搜索技能注册中心","必填":"可选"},{"参数":"install","说明":"安装一个技能","必填":"可选"},{"参数":"inspect","说明":"预览技能但不安装","必填":"可选"},{"参数":"list","说明":"列出已安装技能","必填":"可选"},{"参数":"check","说明":"检查已安装的技能是否有更新","必填":"可选"},{"参数":"update","说明":"更新已安装的技能","必填":"可选"},{"参数":"uninstall","说明":"卸载技能","必填":"可选"},{"参数":"config","说明":"启用/禁用单个技能","必填":"可选"}]',
    example_basic='hermes skills list\nhermes skills search git',
    example_adv='hermes skills install github-auth\nhermes skills update\nhermes skills config',
    os_type='通用',
    aliases='技能,skills,插件,扩展',
    tips='技能可以来自 skills.sh、GitHub、ClawHub 等。安装后重启会话生效。用 hermes -s skill_name 临时加载。',
)

# ── 12. 插件管理 ──
add(
    cmd_name='hermes plugins',
    name_cn='管理插件',
    function_desc='从 Git 仓库安装、更新、删除和管理插件',
    syntax='hermes plugins {install|update|remove|list|enable|disable}',
    params_json='[{"参数":"install","说明":"从 Git URL 安装插件","必填":"可选"},{"参数":"update","说明":"拉取已安装插件的最新代码","必填":"可选"},{"参数":"remove / rm / uninstall","说明":"卸载插件","必填":"可选"},{"参数":"list / ls","说明":"列出已安装插件","必填":"可选"},{"参数":"enable","说明":"启用已禁用的插件","必填":"可选"},{"参数":"disable","说明":"禁用插件（不卸载）","必填":"可选"}]',
    example_basic='hermes plugins list\nhermes plugins install owner/repo',
    example_adv='hermes plugins update\nhermes plugins disable some-plugin',
    os_type='通用',
    aliases='插件,plugins,扩展,模块',
    tips='插件与技能不同：插件可以扩展 Hermes Agent 的核心功能（如添加新工具、新平台支持）。从 Git 仓库安装。',
)

# ── 13. 会话管理 ──
add(
    cmd_name='hermes sessions',
    name_cn='管理会话历史',
    function_desc='查看、导出、删除、清理、重命名会话历史等操作',
    syntax='hermes sessions {list|export|delete|prune|stats|rename|browse}',
    params_json='[{"参数":"list","说明":"列出最近的会话","必填":"可选"},{"参数":"export","说明":"将会话导出为 JSONL 文件","必填":"可选"},{"参数":"delete","说明":"删除指定会话","必填":"可选"},{"参数":"prune","说明":"删除旧会话","必填":"可选"},{"参数":"stats","说明":"查看会话存储统计","必填":"可选"},{"参数":"rename","说明":"设置/修改会话标题","必填":"可选"},{"参数":"browse","说明":"交互式会话浏览/搜索/恢复","必填":"可选"}]',
    example_basic='hermes sessions list\nhermes sessions stats',
    example_adv='hermes sessions rename abc123 "修复bug的会话"\nhermes sessions prune --keep 30',
    os_type='通用',
    aliases='会话,sessions,历史,对话记录',
    tips='会话存储在 SQLite 数据库中。prune 可设置保留最近N天或N条的会话。browse 进入交互式选择界面。',
)

# ── 14. 日志 ──
add(
    cmd_name='hermes logs',
    name_cn='查看和过滤日志',
    function_desc='查看、跟踪、过滤 agent.log / errors.log / gateway.log，支持行数/级别/组件/时间过滤',
    syntax='hermes logs [log_name] [-n LINES] [-f] [--level LEVEL] [--session ID] [--since TIME] [--component NAME]',
    params_json='[{"参数":"log_name","说明":"日志名：agent(默认)、errors、gateway、list","必填":"可选"},{"参数":"-n LINES","说明":"显示行数（默认50）","必填":"可选"},{"参数":"-f / --follow","说明":"实时跟踪（类似 tail -f）","必填":"可选"},{"参数":"--level LEVEL","说明":"最低日志级别：DEBUG/INFO/WARNING/ERROR","必填":"可选"},{"参数":"--session ID","说明":"过滤包含此会话ID的行","必填":"可选"},{"参数":"--since TIME","说明":"显示指定时间以来的行，如 1h / 30m / 2d","必填":"可选"},{"参数":"--component NAME","说明":"按组件过滤：gateway/agent/tools/cli/cron","必填":"可选"}]',
    example_basic='hermes logs\nhermes logs -f',
    example_adv='hermes logs errors -n 100\nhermes logs --level WARNING --since 1h\nhermes logs --component gateway -f',
    os_type='通用',
    aliases='日志,logs,log,查看日志,跟踪日志',
    tips='最常用的是 hermes logs -f 实时跟踪。排查错误用 hermes logs errors。查看网关日志用 hermes logs gateway。',
)

# ── 15. MCP ──
add(
    cmd_name='hermes mcp',
    name_cn='管理 MCP 服务器',
    function_desc='管理 Model Context Protocol (MCP) 服务器连接，支持添加/移除/测试/配置，也可将 Hermes 作为 MCP 服务器运行',
    syntax='hermes mcp {serve|add|remove|list|test|configure|login}',
    params_json='[{"参数":"serve","说明":"将 Hermes 作为 MCP 服务器运行","必填":"可选"},{"参数":"add","说明":"添加 MCP 服务器（自动发现安装）","必填":"可选"},{"参数":"remove / rm","说明":"移除 MCP 服务器","必填":"可选"},{"参数":"list / ls","说明":"列出已配置的 MCP 服务器","必填":"可选"},{"参数":"test","说明":"测试 MCP 服务器连接","必填":"可选"},{"参数":"configure / config","说明":"切换工具选择","必填":"可选"},{"参数":"login","说明":"强制重新认证 OAuth MCP 服务器","必填":"可选"}]',
    example_basic='hermes mcp list\nhermes mcp add github',
    example_adv='hermes mcp serve\nhermes mcp test my-server',
    os_type='通用',
    aliases='mcp,model context protocol,工具,服务器',
    tips='MCP 服务器提供额外的工具。在 config.yaml 的 mcp.servers 中配置，或通过 hermes mcp add 添加。',
)

# ── 16. 工具管理 ──
add(
    cmd_name='hermes tools',
    name_cn='管理启用的工具',
    function_desc='启用、禁用或列出各平台（CLI/Telegram/Discord等）的工具，不传子命令进入交互式配置',
    syntax='hermes tools [{list|disable|enable}] [--summary]',
    params_json='[{"参数":"list","说明":"显示所有工具及其启用状态","必填":"可选"},{"参数":"disable","说明":"禁用工具有集或MCP工具","必填":"可选"},{"参数":"enable","说明":"启用工具有集或MCP工具","必填":"可选"},{"参数":"--summary","说明":"打印各平台已启用工具的摘要并退出","必填":"可选"}]',
    example_basic='hermes tools\nhermes tools list',
    example_adv='hermes tools --summary\nhermes tools disable web',
    os_type='通用',
    aliases='工具,tools,启用,禁用',
    tips='内置工具有 name 标识（如 web/memory）。MCP 工具用 server:tool 格式（如 github:create_issue）。',
)

# ── 17. 记忆管理 ──
add(
    cmd_name='hermes memory',
    name_cn='管理外部记忆提供商',
    function_desc='设置和管理外部记忆提供商插件（honcho/openviking/mem0/hindsight/holographic/retaindb/byterover）',
    syntax='hermes memory {setup|status|off|reset}',
    params_json='[{"参数":"setup","说明":"交互式提供商选择和配置","必填":"可选"},{"参数":"status","说明":"显示当前记忆提供商配置","必填":"可选"},{"参数":"off","说明":"禁用外部提供商（仅内置记忆）","必填":"可选"},{"参数":"reset","说明":"擦除所有内置记忆（MEMORY.md和USER.md）","必填":"可选"}]',
    example_basic='hermes memory status\nhermes memory setup',
    example_adv='hermes memory off\nhermes memory reset',
    os_type='通用',
    aliases='记忆,memory,外部记忆,mem0,honcho',
    tips='内置记忆（MEMORY.md/USER.md）始终有效。外部记忆提供商只能激活一个。reset 会清空内置记忆文件。',
)

# ── 18. 配置文件 ──
add(
    cmd_name='hermes profile',
    name_cn='管理多配置文件',
    function_desc='管理多个隔离的 Hermes 实例配置，支持列出/切换/创建/删除/别名/导出/导入',
    syntax='hermes profile {list|use|create|delete|show|alias|rename|export|import}',
    params_json='[{"参数":"list","说明":"列出所有配置文件","必填":"可选"},{"参数":"use","说明":"设置默认配置文件","必填":"可选"},{"参数":"create","说明":"创建新配置文件","必填":"可选"},{"参数":"delete","说明":"删除配置文件","必填":"可选"},{"参数":"show","说明":"显示配置文件详情","必填":"可选"},{"参数":"alias","说明":"管理包装脚本","必填":"可选"},{"参数":"rename","说明":"重命名配置文件","必填":"可选"},{"参数":"export","说明":"导出配置文件为归档","必填":"可选"},{"参数":"import","说明":"从归档导入配置文件","必填":"可选"}]',
    example_basic='hermes profile list\nhermes profile create work',
    example_adv='hermes profile use work\nhermes profile export work --output work.tar.gz',
    os_type='通用',
    aliases='配置文件,profile,多实例,隔离环境',
    tips='每个 profile 有独立的配置、记忆和会话。alias 可以生成包装脚本（如 hermes-work 命令）。',
)

# ── 19. Dashboard ──
add(
    cmd_name='hermes dashboard',
    name_cn='启动 Web UI 面板',
    function_desc='启动内置的 Web 管理仪表盘（Dashboard），通过浏览器管理 Hermes Agent',
    syntax='hermes dashboard [--port PORT] [--host HOST]',
    params_json='[{"参数":"--port PORT","说明":"端口号，默认 9119","必填":"可选"},{"参数":"--host HOST","说明":"监听地址，默认 127.0.0.1","必填":"可选"}]',
    example_basic='hermes dashboard',
    example_adv='hermes dashboard --port 8080 --host 0.0.0.0',
    os_type='通用',
    aliases='dashboard,面板,webui,管理界面',
    tips='默认地址 http://127.0.0.1:9119。如果端口被占用自动找下一个。仅本机访问需绑定 127.0.0.1。',
)

# ── 20. 版本与更新 ──
add(
    cmd_name='hermes version',
    name_cn='显示版本信息',
    function_desc='显示 Hermes Agent 的版本号和构建信息',
    syntax='hermes --version 或 hermes version',
    params_json='[]',
    example_basic='hermes --version\nhermes version',
    os_type='通用',
    aliases='版本,version,-V,--version',
    tips='检查更新前先看版本号。也可用 hermes --version。',
)

add(
    cmd_name='hermes update',
    name_cn='更新 Hermes Agent',
    function_desc='将 Hermes Agent 更新到最新版本',
    syntax='hermes update',
    params_json='[]',
    example_basic='hermes update',
    os_type='通用',
    aliases='更新,update,升级',
    tips='建议更新前运行 hermes backup 备份。更新后可能需要重新登录提供商。',
)

add(
    cmd_name='hermes uninstall',
    name_cn='卸载 Hermes Agent',
    function_desc='完全卸载 Hermes Agent，可选择是否保留数据',
    syntax='hermes uninstall',
    params_json='[]',
    example_basic='hermes uninstall',
    os_type='通用',
    aliases='卸载,uninstall,删除',
    tips='卸载前建议运行 hermes backup 备份数据。卸载会询问是否保留配置和会话文件。',
)

# ── 21. 其他命令 ──
add(
    cmd_name='hermes whatsapp',
    name_cn='设置 WhatsApp 集成',
    function_desc='设置 WhatsApp 平台集成，使 Hermes Agent 可通过 WhatsApp 交互',
    syntax='hermes whatsapp',
    params_json='[]',
    example_basic='hermes whatsapp',
    os_type='通用',
    aliases='whatsapp,WhatsApp,消息',
    tips='需要先 hermes gateway setup 配置平台。WhatsApp 需要商业 API 或非官方库。',
)

add(
    cmd_name='hermes slack',
    name_cn='Slack 集成工具',
    function_desc='Slack 集成帮助（manifest 生成、配置等）',
    syntax='hermes slack',
    params_json='[]',
    example_basic='hermes slack',
    os_type='通用',
    aliases='slack,Slack,消息',
    tips='生成 Slack App Manifest 用于在 Slack API 控制台注册应用。',
)

add(
    cmd_name='hermes pairing',
    name_cn='管理 DM 配对码',
    function_desc='管理 DM 配对码，用于用户授权绑定到 Hermes Agent',
    syntax='hermes pairing {create|list|revoke}',
    params_json='[{"参数":"create","说明":"创建配对码","必填":"可选"},{"参数":"list","说明":"列出所有配对","必填":"可选"},{"参数":"revoke","说明":"撤销配对","必填":"可选"}]',
    example_basic='hermes pairing create\nhermes pairing list',
    os_type='通用',
    aliases='配对,pairing,授权码',
    tips='配对码用于首次将用户ID绑定到 Agent。配置文件中管理已授权用户。',
)

add(
    cmd_name='hermes acp',
    name_cn='作为 ACP 服务器运行',
    function_desc='以 Agent Client Protocol (ACP) 服务器模式运行 Hermes Agent，允许其他 ACP 客户端连接',
    syntax='hermes acp [--port PORT]',
    params_json='[{"参数":"--port PORT","说明":"监听端口","必填":"可选"}]',
    example_basic='hermes acp',
    example_adv='hermes acp --port 8080',
    os_type='通用',
    aliases='acp,agent client protocol,服务器',
    tips='ACP 是 Agent 间通信协议。启用后其他 Agent 可以通过 ACP 连接使用 Hermes。',
)

add(
    cmd_name='hermes completion',
    name_cn='生成 Shell 补全脚本',
    function_desc='生成 shell 自动补全脚本（支持 bash / zsh / fish），输出到标准输出',
    syntax='hermes completion {bash|zsh|fish}',
    params_json='[{"参数":"shell类型","说明":"bash / zsh / fish","必填":"必填"}]',
    example_basic='hermes completion bash',
    example_adv='hermes completion zsh > ~/.zsh/completion/_hermes\n# 或 source <(hermes completion zsh)',
    os_type='通用',
    aliases='补全,completion,tab补全,自动补全',
    tips='将输出 source 到 shell 配置文件中即可启用 Tab 补全。如：hermes completion bash > /etc/bash_completion.d/hermes。',
)

add(
    cmd_name='hermes insights',
    name_cn='查看使用分析',
    function_desc='显示 Hermes Agent 的使用统计和分析数据',
    syntax='hermes insights',
    params_json='[]',
    example_basic='hermes insights',
    os_type='通用',
    aliases='统计,insights,分析,使用统计',
    tips='显示会话数量、token消耗、常用工具等统计数据。',
)

add(
    cmd_name='hermes claw',
    name_cn='OpenClaw 迁移工具',
    function_desc='OpenClaw 迁移工具，帮助从旧版迁移数据',
    syntax='hermes claw {migrate|status}',
    params_json='[{"参数":"migrate","说明":"执行迁移","必填":"可选"},{"参数":"status","说明":"查看迁移状态","必填":"可选"}]',
    example_basic='hermes claw status',
    os_type='通用',
    aliases='claw,迁移,OpenClaw',
    tips='用于从 OpenClaw 系统迁移到 Hermes Agent。迁移前先备份。',
)

# ── 统计 ──
total = db.conn.execute("SELECT COUNT(*) FROM commands WHERE category_id=?", (ha_cat,)).fetchone()[0]
grand = db.get_total_count()
print(f'[OK] 添加 Hermes Agent 命令: {total} 条')
print(f'[OK] 数据库总计: {grand} 条')
