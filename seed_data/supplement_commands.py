#!/usr/bin/env python3
"""
补充种子数据脚本：向数据库插入大量命令行命令数据（至少200条）
数据库路径 ~/.code-quickref/data.db
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from database.db_manager import DBManager

db = DBManager()


def get_cat_id(parent_name, child_name):
    return db.get_cat_id_by_name(parent_name, child_name)


# ============================================================
# Git 补充（+14条）
# ============================================================
def seed_git_supplement(db):
    cat_id = get_cat_id('命令行工具', 'Git')
    if not cat_id:
        print('[ERR] 未找到 Git 分类')
        return 0

    commands = [
        {
            'cmd_name': 'git fetch',
            'name_cn': '获取远程更新',
            'function_desc': '从远程仓库下载所有分支的提交、文件和引用，但不自动合并到当前工作分支。安全地查看远程变更后再决定如何合并。',
            'syntax': 'git fetch [远程仓库名] [分支名]',
            'params_json': '[{"参数":"远程仓库名","说明":"远程仓库名称（默认 origin）","必填":"可选"},{"参数":"分支名","说明":"指定要获取的分支","必填":"可选"}]',
            'example_basic': 'git fetch origin',
            'example_adv': 'git fetch --prune origin && git log --oneline origin/main..main',
            'os_type': '通用', 'aliases': '获取,远程拉取,fetch',
            'tips': 'git fetch 只下载数据到本地仓库，不影响工作区。配合 git merge 或 git rebase 使用。--prune 可删除本地已不存在的远程分支引用。'
        },
        {
            'cmd_name': 'git rebase',
            'name_cn': '变基操作',
            'function_desc': '将当前分支的提交移动到另一个分支的最新提交之上，或合并/修改多个提交记录。能使历史更线性整洁。',
            'syntax': 'git rebase <目标分支>',
            'params_json': '[{"参数":"目标分支","说明":"要变基到的目标分支","必填":"是"},{"参数":"-i","说明":"交互式变基，可编辑/合并/重排提交","必填":"可选"}]',
            'example_basic': 'git rebase main',
            'example_adv': 'git rebase -i HEAD~3',
            'os_type': '通用', 'aliases': '变基,rebase,衍合',
            'tips': '不要对已推送到远程仓库的公共分支执行 rebase。交互式模式 (git rebase -i) 可以合并、修改提交信息或调整顺序。'
        },
        {
            'cmd_name': 'git cherry-pick',
            'name_cn': '挑选提交',
            'function_desc': '将其他分支的一个或多个特定提交复制到当前分支，相当于选择性合并。非常适合将 Bug 修复补丁迁移到多个发行分支。',
            'syntax': 'git cherry-pick <提交哈希>',
            'params_json': '[{"参数":"提交哈希","说明":"要挑选的提交哈希值","必填":"是"},{"参数":"-n","说明":"不自动创建提交，只应用到工作区","必填":"可选"}]',
            'example_basic': 'git cherry-pick abc1234',
            'example_adv': 'git cherry-pick abc1234..def5678',
            'os_type': '通用', 'aliases': '挑选,cherry-pick,精选提交',
            'tips': 'cherry-pick 多个提交时按顺序应用。如果遇到冲突，解决后执行 git cherry-pick --continue 继续。'
        },
        {
            'cmd_name': 'git revert',
            'name_cn': '撤销提交',
            'function_desc': '创建一个新的提交来撤销指定的提交变更。与 git reset 不同，revert 不会修改历史，适合已推送到远程仓库的提交。',
            'syntax': 'git revert <提交哈希>',
            'params_json': '[{"参数":"提交哈希","说明":"要撤销的提交哈希值","必填":"是"},{"参数":"-n","说明":"不自动创建提交","必填":"可选"}]',
            'example_basic': 'git revert abc1234',
            'example_adv': 'git revert HEAD~3..HEAD --no-edit',
            'os_type': '通用', 'aliases': '撤销,反向提交,revert',
            'tips': 'revert 是安全的撤销方式，因为它不改变历史记录。多个撤销可以用 --no-edit 跳过编辑提交信息。'
        },
        {
            'cmd_name': 'git tag',
            'name_cn': '管理标签',
            'function_desc': '给特定提交创建有意义的标签（如版本号），便于后续快速引用。分轻量标签和附注标签两种。',
            'syntax': 'git tag [-a] <标签名> [-m "信息"] [提交哈希]',
            'params_json': '[{"参数":"-a","说明":"创建附注标签（含作者、日期、信息）","必填":"可选"},{"参数":"标签名","说明":"标签名称（如 v1.0.0）","必填":"是"},{"参数":"提交哈希","说明":"指定提交打标签，不填则 HEAD","必填":"可选"}]',
            'example_basic': 'git tag v1.0.0',
            'example_adv': 'git tag -a v2.0.0 -m "Release version 2.0.0" abc1234',
            'os_type': '通用', 'aliases': '标签,版本号,tag',
            'tips': '用 git tag -l 列出所有标签。推送标签到远程用 git push origin --tags。附注标签包含完整元数据，推荐用于版本发布。'
        },
        {
            'cmd_name': 'git config',
            'name_cn': '配置管理',
            'function_desc': '查看和设置 Git 的配置项，包括用户信息、别名、编辑器等。配置分系统级、全局级和仓库级三级。',
            'syntax': 'git config [--global] <键> <值>',
            'params_json': '[{"参数":"--global","说明":"修改全局配置（~/.gitconfig）","必填":"可选"},{"参数":"--list","说明":"列出所有配置项","必填":"可选"},{"参数":"键","说明":"配置项名称（如 user.name）","必填":"是"},{"参数":"值","说明":"配置项值","必填":"是"}]',
            'example_basic': 'git config --global user.name "Your Name"',
            'example_adv': 'git config --global alias.co checkout',
            'os_type': '通用', 'aliases': '配置,alias,config',
            'tips': '三级配置优先级：仓库级 > 全局级 > 系统级。git config --list 查看当前所有生效配置。alias 可以大幅提升日常操作效率。'
        },
        {
            'cmd_name': 'git rm',
            'name_cn': '删除文件',
            'function_desc': '从 Git 仓库和工作区同时删除文件。与手动删除文件后再 git add 的效果相同，但更直接。',
            'syntax': 'git rm <文件路径>',
            'params_json': '[{"参数":"文件路径","说明":"要删除的文件路径","必填":"是"},{"参数":"--cached","说明":"仅从暂存区删除，保留工作区文件","必填":"可选"},{"参数":"-r","说明":"递归删除目录","必填":"可选"}]',
            'example_basic': 'git rm old-file.txt',
            'example_adv': 'git rm --cached secret.env',
            'os_type': '通用', 'aliases': '删除,移除,rm',
            'tips': '--cached 只从跟踪列表中移除文件但保留硬盘文件，适合不想再跟踪但需保留的配置文件。'
        },
        {
            'cmd_name': 'git mv',
            'name_cn': '移动/重命名文件',
            'function_desc': '移动或重命名 Git 仓库中的文件，同时自动更新暂存区。比手动 mv 后再 git add 更简洁。',
            'syntax': 'git mv <源路径> <目标路径>',
            'params_json': '[{"参数":"源路径","说明":"原文件或目录路径","必填":"是"},{"参数":"目标路径","说明":"新文件或目录路径","必填":"是"}]',
            'example_basic': 'git mv old.py new.py',
            'example_adv': 'git mv src/utils/ src/helpers/',
            'os_type': '通用', 'aliases': '移动,重命名,mv',
            'tips': 'git mv 本质上等同于 mv + git rm + git add 的组合操作。Git 能自动检测文件重命名（基于内容相似度）。'
        },
        {
            'cmd_name': 'git show',
            'name_cn': '显示提交详情',
            'function_desc': '显示指定提交的详细信息，包括变更内容、提交信息、作者和时间戳等。默认显示最新提交。',
            'syntax': 'git show [提交哈希]',
            'params_json': '[{"参数":"提交哈希","说明":"要查看的提交哈希（默认 HEAD）","必填":"可选"},{"参数":"--stat","说明":"仅显示文件变更统计","必填":"可选"}]',
            'example_basic': 'git show',
            'example_adv': 'git show --stat abc1234',
            'os_type': '通用', 'aliases': '查看,显示,show',
            'tips': 'git show 也可以查看标签、树对象或 blob 对象的内容。加上 --name-only 只显示变更的文件名列表。'
        },
        {
            'cmd_name': 'git blame',
            'name_cn': '文件追溯',
            'function_desc': '逐行显示文件的每一行是谁在什么时间修改的。用于代码溯源和查找 Bug 引入者。',
            'syntax': 'git blame <文件路径>',
            'params_json': '[{"参数":"文件路径","说明":"要追溯的文件路径","必填":"是"},{"参数":"-L","说明":"指定行范围，如 -L 10,20","必填":"可选"}]',
            'example_basic': 'git blame index.js',
            'example_adv': 'git blame -L 10,30 main.py',
            'os_type': '通用', 'aliases': '追溯,blame,问责',
            'tips': 'git blame 不带有责备意味，更多用于理解代码演变过程。配合 -w 参数可忽略空白变更。用 git log -p 查看历史更详细。'
        },
        {
            'cmd_name': 'git bisect',
            'name_cn': '二分查找',
            'function_desc': '通过二分查找法在提交历史中快速定位引入 Bug 的提交。标记好（good）和坏（bad）的提交，Git 自动二分定位。',
            'syntax': 'git bisect start <坏提交> <好提交>',
            'params_json': '[{"参数":"坏提交","说明":"已知有问题的提交（默认 HEAD）","必填":"可选"},{"参数":"好提交","说明":"已知正常的提交","必填":"是"}]',
            'example_basic': 'git bisect start HEAD v1.0.0',
            'example_adv': 'git bisect run npm test',
            'os_type': '通用', 'aliases': '二分查找,bisect,调试',
            'tips': 'git bisect run 可配合自动化测试脚本全自动运行。结束后执行 git bisect reset 恢复仓库到正常状态。'
        },
        {
            'cmd_name': 'git reflog',
            'name_cn': '引用日志',
            'function_desc': '显示 HEAD 和其他引用的历史移动记录。是 Git 的"后悔药"，可以找回丢失的提交（如 rebase 或 reset 后的提交）。',
            'syntax': 'git reflog [分支名]',
            'params_json': '[{"参数":"分支名","说明":"查看指定分支的 reflog（默认 HEAD）","必填":"可选"}]',
            'example_basic': 'git reflog',
            'example_adv': 'git reflog --date=iso',
            'os_type': '通用', 'aliases': '引用日志,reflog,恢复',
            'tips': 'reflog 只记录本地操作，不会同步到远程仓库。默认保留 90 天内的记录（可通过 gc.reflogExpire 配置）。'
        },
        {
            'cmd_name': 'git submodule',
            'name_cn': '子模块管理',
            'function_desc': '在一个 Git 仓库中嵌入另一个 Git 仓库作为子目录，并跟踪其特定版本。用于管理依赖项目。',
            'syntax': 'git submodule add <仓库地址> [本地路径]',
            'params_json': '[{"参数":"add","说明":"添加新的子模块","必填":"是"},{"参数":"update","说明":"更新所有子模块到记录的提交","必填":"可选"},{"参数":"--init","说明":"初始化子模块配置文件","必填":"可选"}]',
            'example_basic': 'git submodule add https://github.com/user/lib.git lib',
            'example_adv': 'git clone --recurse-submodules https://github.com/user/project.git',
            'os_type': '通用', 'aliases': '子模块,submodule,依赖',
            'tips': '克隆含子模块的仓库需加 --recurse-submodules。子模块更新后需要提交父仓库才能记录新版本。'
        },
        {
            'cmd_name': 'git reset',
            'name_cn': '重置当前分支',
            'function_desc': '将当前 HEAD 移动到指定提交，并根据 --hard/--soft/--mixed 参数决定是否重置暂存区和工作区。',
            'syntax': 'git reset [--soft|--mixed|--hard] [提交哈希]',
            'params_json': '[{"参数":"--soft","说明":"仅移动 HEAD，保留暂存区和工作区","必填":"可选"},{"参数":"--mixed","说明":"移动 HEAD 并重置暂存区，保留工作区（默认）","必填":"可选"},{"参数":"--hard","说明":"移动 HEAD 并重置暂存区和工作区（危险！）","必填":"可选"}]',
            'example_basic': 'git reset HEAD~1',
            'example_adv': 'git reset --hard origin/main',
            'os_type': '通用', 'aliases': '重置,reset,--hard,--soft',
            'tips': '--hard 会丢弃工作区的所有未提交更改，操作前务必确认。--soft 适合合并多个提交（commit --amend 的替代方案）。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Git: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Git: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# Linux 终端补充（+25条）
# ============================================================
def seed_linux_supplement(db):
    cat_id = get_cat_id('命令行工具', 'Linux终端')
    if not cat_id:
        print('[ERR] 未找到 Linux终端 分类')
        return 0

    commands = [
        {
            'cmd_name': 'scp',
            'name_cn': '安全复制',
            'function_desc': '基于 SSH 协议在本地和远程主机之间安全复制文件和目录。支持递归复制目录。',
            'syntax': 'scp [选项] <源路径> <目标路径>',
            'params_json': '[{"参数":"-r","说明":"递归复制整个目录","必填":"可选"},{"参数":"-P","说明":"指定 SSH 端口","必填":"可选"},{"参数":"源路径","说明":"源文件或目录路径","必填":"是"},{"参数":"目标路径","说明":"目标文件或目录路径","必填":"是"}]',
            'example_basic': 'scp file.txt user@host:/home/user/',
            'example_adv': 'scp -r -P 2222 ./backup/ user@host:/remote/backup/',
            'os_type': 'Linux/macOS', 'aliases': '安全复制,scp,远程复制',
            'tips': 'scp 已被 rsync 在大文件传输中逐渐取代。传输大文件建议用 rsync -P 支持断点续传。'
        },
        {
            'cmd_name': 'rsync',
            'name_cn': '远程同步',
            'function_desc': '高效的文件同步和复制工具，只传输文件差异部分，支持本地和远程同步，断点续传。',
            'syntax': 'rsync [选项] <源路径> <目标路径>',
            'params_json': '[{"参数":"-a","说明":"归档模式，保留权限/时间戳等","必填":"可选"},{"参数":"-v","说明":"详细输出","必填":"可选"},{"参数":"-z","说明":"传输时压缩","必填":"可选"},{"参数":"--delete","说明":"删除目标端多余文件","必填":"可选"}]',
            'example_basic': 'rsync -av source/ destination/',
            'example_adv': 'rsync -avz --delete --progress /local/dir/ user@host:/remote/dir/',
            'os_type': 'Linux/macOS', 'aliases': '同步,rsync,远程同步',
            'tips': '源路径末尾的斜杠有区别：带斜杠表示复制目录内容，不带斜杠表示复制目录本身。--progress 显示传输进度。'
        },
        {
            'cmd_name': 'crontab',
            'name_cn': '定时任务',
            'function_desc': '管理用户的定时任务（cron 作业），按指定的时间周期自动执行命令或脚本。',
            'syntax': 'crontab [-e|-l|-r]',
            'params_json': '[{"参数":"-e","说明":"编辑当前用户的 crontab 文件","必填":"可选"},{"参数":"-l","说明":"列出当前用户的定时任务","必填":"可选"},{"参数":"-r","说明":"删除当前用户的 crontab","必填":"可选"}]',
            'example_basic': 'crontab -e',
            'example_adv': '0 2 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1',
            'os_type': 'Linux/macOS', 'aliases': '定时任务,计划任务,crontab,cron',
            'tips': 'cron 格式：分 时 日 月 周。用 crontab -e 编辑，每条任务一行。日志重定向到文件方便排查问题。'
        },
        {
            'cmd_name': 'systemctl',
            'name_cn': '系统服务管理',
            'function_desc': '管理 systemd 系统和服务管理器，控制服务的启动、停止、重启，查看状态等。',
            'syntax': 'systemctl <子命令> [服务名]',
            'params_json': '[{"参数":"start","说明":"启动服务","必填":"可选"},{"参数":"stop","说明":"停止服务","必填":"可选"},{"参数":"restart","说明":"重启服务","必填":"可选"},{"参数":"status","说明":"查看服务状态","必填":"可选"},{"参数":"enable","说明":"设置开机自启","必填":"可选"},{"参数":"disable","说明":"取消开机自启","必填":"可选"}]',
            'example_basic': 'systemctl status nginx',
            'example_adv': 'systemctl daemon-reload && systemctl restart nginx',
            'os_type': 'Linux', 'aliases': '服务管理,systemctl,systemd',
            'tips': '修改服务配置文件后需执行 systemctl daemon-reload 重新加载。journalctl -u 服务名 可查看对应服务的日志。'
        },
        {
            'cmd_name': 'journalctl',
            'name_cn': '查看日志',
            'function_desc': '查询和查看 systemd 的日志（journal）记录，支持按服务、时间、优先级等过滤。',
            'syntax': 'journalctl [选项]',
            'params_json': '[{"参数":"-u","说明":"指定服务名过滤","必填":"可选"},{"参数":"-f","说明":"实时跟踪最新日志","必填":"可选"},{"参数":"--since","说明":"按起始时间过滤","必填":"可选"},{"参数":"-n","说明":"显示最近 N 行","必填":"可选"}]',
            'example_basic': 'journalctl -u nginx',
            'example_adv': 'journalctl -u nginx --since "1 hour ago" --until "now" -n 50',
            'os_type': 'Linux', 'aliases': '日志,journalctl,查看日志',
            'tips': 'journalctl -xe 显示详细信息并解释错误原因。日志保存在 /var/log/journal/ 目录中。'
        },
        {
            'cmd_name': 'awk',
            'name_cn': '文本分析工具',
            'function_desc': '强大的文本处理和分析编程语言，擅长按列处理结构化文本数据，支持模式匹配、格式化输出等。',
            'syntax': 'awk [选项] \'<模式>{动作}\' <文件>',
            'params_json': '[{"参数":"-F","说明":"指定输入字段分隔符","必填":"可选"},{"参数":"模式","说明":"匹配条件（如 /pattern/）","必填":"可选"},{"参数":"动作","说明":"匹配后执行的操作","必填":"是"}]',
            'example_basic': 'awk \'{print $1, $3}\' file.txt',
            'example_adv': 'awk -F: \'$3 >= 1000 {print $1, $6}\' /etc/passwd',
            'os_type': 'Linux/macOS', 'aliases': 'awk,文本处理,列提取',
            'tips': 'awk 默认以空白字符分隔列。$0 表示整行，$1 是第一列，NF 是列数，NR 是行号。'
        },
        {
            'cmd_name': 'sed',
            'name_cn': '流编辑器',
            'function_desc': '非交互式流编辑器，对文本进行替换、删除、插入等操作，常用于批量文件处理。',
            'syntax': 'sed [选项] \'<操作>\' <文件>',
            'params_json': '[{"参数":"-i","说明":"直接修改文件（备份可选）","必填":"可选"},{"参数":"-n","说明":"关闭默认输出","必填":"可选"},{"参数":"s","说明":"替换操作 s/旧/新/标志","必填":"可选"},{"参数":"d","说明":"删除匹配行","必填":"可选"}]',
            'example_basic': 'sed \'s/foo/bar/g\' file.txt',
            'example_adv': 'sed -i.bak \'/^#/d; /^$/d\' config.conf',
            'os_type': 'Linux/macOS', 'aliases': '流编辑,sed,文本替换',
            'tips': 'sed -i 直接修改文件，建议加备份后缀如 -i.bak。用 -n 和 p 配合只打印匹配行。'
        },
        {
            'cmd_name': 'sort',
            'name_cn': '排序',
            'function_desc': '对文本文件的行进行排序，支持按数字、字典序、月份、逆序等多种排序方式。',
            'syntax': 'sort [选项] <文件>',
            'params_json': '[{"参数":"-n","说明":"按数字大小排序","必填":"可选"},{"参数":"-r","说明":"逆序排序","必填":"可选"},{"参数":"-k","说明":"指定排序列","必填":"可选"},{"参数":"-u","说明":"去重后排序（同 uniq）","必填":"可选"}]',
            'example_basic': 'sort file.txt',
            'example_adv': 'sort -t: -k3 -n /etc/passwd',
            'os_type': 'Linux/macOS', 'aliases': '排序,sort,整理',
            'tips': 'sort -u 等同于 sort | uniq。默认按字典序排序，数字排序需加 -n 参数。'
        },
        {
            'cmd_name': 'uniq',
            'name_cn': '去重',
            'function_desc': '报告或忽略文件中的重复行。输入需先排序才能正确去重，通常与 sort 配合使用。',
            'syntax': 'uniq [选项] <文件>',
            'params_json': '[{"参数":"-c","说明":"显示每行出现次数","必填":"可选"},{"参数":"-d","说明":"仅显示重复的行","必填":"可选"},{"参数":"-u","说明":"仅显示不重复的行","必填":"可选"}]',
            'example_basic': 'sort file.txt | uniq',
            'example_adv': 'sort file.txt | uniq -c | sort -rn',
            'os_type': 'Linux/macOS', 'aliases': '去重,uniq,唯一',
            'tips': 'uniq 只去除连续重复行，所以必须先 sort。sort file.txt | uniq -c | sort -rn 可统计频率并排序。'
        },
        {
            'cmd_name': 'wc',
            'name_cn': '统计计数',
            'function_desc': '统计文件的行数、单词数和字符数。常用于代码行数统计或日志分析。',
            'syntax': 'wc [选项] <文件>',
            'params_json': '[{"参数":"-l","说明":"只统计行数","必填":"可选"},{"参数":"-w","说明":"只统计单词数","必填":"可选"},{"参数":"-c","说明":"只统计字节数","必填":"可选"}]',
            'example_basic': 'wc file.txt',
            'example_adv': 'wc -l *.py | tail -1',
            'os_type': 'Linux/macOS', 'aliases': '统计,wc,计数',
            'tips': 'wc -l 统计行数最常用。wc -l $(find . -name "*.py") 统计所有 Python 文件行数。'
        },
        {
            'cmd_name': 'head',
            'name_cn': '查看文件头部',
            'function_desc': '显示文件的开头部分，默认显示前 10 行。常用于快速查看日志或配置文件。',
            'syntax': 'head [选项] <文件>',
            'params_json': '[{"参数":"-n","说明":"指定行数","必填":"可选","默认":"10"},{"参数":"-c","说明":"指定字节数","必填":"可选"}]',
            'example_basic': 'head file.txt',
            'example_adv': 'head -n 20 /var/log/syslog',
            'os_type': 'Linux/macOS', 'aliases': '头部,head,查看开头',
            'tips': 'head -n -5 可以显示除最后 5 行之外的所有行。head -c 100 显示前 100 个字节。'
        },
        {
            'cmd_name': 'tail',
            'name_cn': '查看文件尾部',
            'function_desc': '显示文件的末尾部分，默认显示后 10 行。-f 模式可实时跟踪文件追加内容，非常适合查看日志。',
            'syntax': 'tail [选项] <文件>',
            'params_json': '[{"参数":"-n","说明":"指定行数（默认 10）","必填":"可选"},{"参数":"-f","说明":"实时跟踪文件新增内容","必填":"可选"},{"参数":"-F","说明":"跟踪文件（支持轮转）","必填":"可选"}]',
            'example_basic': 'tail -n 20 file.txt',
            'example_adv': 'tail -f /var/log/nginx/access.log',
            'os_type': 'Linux/macOS', 'aliases': '尾部,tail,实时查看',
            'tips': 'tail -F 比 -f 更强大，可以处理日志轮转（文件被重命名后自动追踪新文件）。'
        },
        {
            'cmd_name': 'less',
            'name_cn': '分页查看',
            'function_desc': '交互式文件阅读器，支持前后翻页、搜索、跳转等。比 more 功能更强大，不会一次性加载整个文件。',
            'syntax': 'less <文件>',
            'params_json': '[{"参数":"文件","说明":"要查看的文件名","必填":"是"},{"参数":"-N","说明":"显示行号","必填":"可选"},{"参数":"+F","说明":"启动后进入跟踪模式（类似 tail -f）","必填":"可选"}]',
            'example_basic': 'less file.txt',
            'example_adv': 'less -N +F /var/log/syslog',
            'os_type': 'Linux/macOS', 'aliases': '分页,less,查看器',
            'tips': '在 less 中：/ 搜索，n 下一个匹配，q 退出，g 跳到开头，G 跳到末尾。less 不会读入整个文件，适合大文件。'
        },
        {
            'cmd_name': 'more',
            'name_cn': '分页显示',
            'function_desc': '基本的文件分页查看器，一次显示一屏内容，按空格翻页。功能比 less 简单，但在最小环境中常用。',
            'syntax': 'more <文件>',
            'params_json': '[{"参数":"文件","说明":"要查看的文件名","必填":"是"},{"参数":"-N","说明":"显示行号","必填":"可选"}]',
            'example_basic': 'more file.txt',
            'example_adv': 'ps aux | more',
            'os_type': 'Linux/macOS', 'aliases': '分页,more,查看',
            'tips': 'more 只能向前翻页（用空格），不能后退。less 是更现代的选择，但 more 在脚本管道中可能更稳定。'
        },
        {
            'cmd_name': 'nl',
            'name_cn': '添加行号',
            'function_desc': '给文本文件的每一行添加行号，支持多种编号格式（如逻辑行、物理行）。',
            'syntax': 'nl [选项] <文件>',
            'params_json': '[{"参数":"-b","说明":"编号方式：a=所有行，t=仅非空行（默认）","必填":"可选"},{"参数":"-n","说明":"编号格式：ln=左对齐，rn=右对齐，rz=右对齐补零","必填":"可选"},{"参数":"-w","说明":"行号宽度","必填":"可选"}]',
            'example_basic': 'nl file.txt',
            'example_adv': 'nl -b a -n rz -w 3 file.txt',
            'os_type': 'Linux/macOS', 'aliases': '行号,nl,编号',
            'tips': 'cat -n 也可以添加行号但更简单。nl 支持更多编号选项，适合格式化输出。'
        },
        {
            'cmd_name': 'tee',
            'name_cn': '双向重定向',
            'function_desc': '从标准输入读取数据并同时写入文件和标准输出。类似 T 型管道，数据分流。',
            'syntax': '<命令> | tee [选项] <文件>',
            'params_json': '[{"参数":"-a","说明":"追加到文件而非覆盖","必填":"可选"},{"参数":"文件","说明":"要写入的文件路径","必填":"是"}]',
            'example_basic': 'echo "hello" | tee output.txt',
            'example_adv': 'make | tee build.log | grep -i error',
            'os_type': 'Linux/macOS', 'aliases': '分流,tee,双向输出',
            'tips': 'tee 常用于边查看输出边保存日志。tee file1 file2 可同时写入多个文件。'
        },
        {
            'cmd_name': 'xargs',
            'name_cn': '参数传递',
            'function_desc': '从标准输入读取数据并将每行作为参数传递给指定命令。解决命令参数过多或管道传递参数的问题。',
            'syntax': '<命令> | xargs [选项] <目标命令>',
            'params_json': '[{"参数":"-n","说明":"每行参数个数","必填":"可选"},{"参数":"-I","说明":"替换字符串（如 -I {}）","必填":"可选"},{"参数":"-P","说明":"并行执行数","必填":"可选"}]',
            'example_basic': 'find . -name "*.py" | xargs wc -l',
            'example_adv': 'find . -name "*.log" | xargs -I {} cp {} /backup/',
            'os_type': 'Linux/macOS', 'aliases': '参数传递,xargs,批量执行',
            'tips': 'xargs -P 0 使用所有 CPU 核心并行执行。文件名含空格时用 -0 和 find -print0 配合。'
        },
        {
            'cmd_name': 'ln',
            'name_cn': '创建链接',
            'function_desc': '创建文件的硬链接或符号链接（软链接）。符号类似 Windows 的快捷方式，硬链接是文件的另一个目录条目。',
            'syntax': 'ln [选项] <目标文件> <链接名>',
            'params_json': '[{"参数":"-s","说明":"创建符号链接（软链接）","必填":"可选"},{"参数":"-f","说明":"强制覆盖已存在的链接","必填":"可选"},{"参数":"-n","说明":"如果目标是目录则覆盖","必填":"可选"}]',
            'example_basic': 'ln -s /usr/local/bin/python3 python',
            'example_adv': 'ln -sfn /data/releases/v2.0 /data/current',
            'os_type': 'Linux/macOS', 'aliases': '链接,ln,符号链接,软链接',
            'tips': '软链接可跨文件系统，指向文件或目录；硬链接不可跨文件系统，只能指向文件。删除原文件后软链接失效。'
        },
        {
            'cmd_name': 'watch',
            'name_cn': '定时执行',
            'function_desc': '周期性执行指定命令并全屏显示输出结果，默认每 2 秒刷新一次。非常适合监控系统状态变化。',
            'syntax': 'watch [选项] <命令>',
            'params_json': '[{"参数":"-n","说明":"刷新间隔（秒，默认 2）","必填":"可选"},{"参数":"-d","说明":"高亮显示变化的内容","必填":"可选"},{"参数":"-x","说明":"传递给命令的附加参数","必填":"可选"}]',
            'example_basic': 'watch -n 1 date',
            'example_adv': 'watch -d -n 0.5 "ps aux --sort=-%mem | head -10"',
            'os_type': 'Linux/macOS', 'aliases': '监视,watch,定时刷新',
            'tips': 'watch -d 高亮每次刷新的变化内容。命令用引号包裹可避免 shell 重定向问题。'
        },
        {
            'cmd_name': 'nohup',
            'name_cn': '忽略挂起信号',
            'function_desc': '在后台运行命令，使其在终端关闭或用户退出后继续运行。输出默认重定向到 nohup.out。',
            'syntax': 'nohup <命令> [参数] &',
            'params_json': '[{"参数":"命令","说明":"要运行的命令","必填":"是"},{"参数":"&","说明":"放入后台执行","必填":"可选"}]',
            'example_basic': 'nohup python script.py &',
            'example_adv': 'nohup ./long-running-job.sh > output.log 2>&1 &',
            'os_type': 'Linux/macOS', 'aliases': '后台运行,nohup,不挂断',
            'tips': 'nohup 不自动后台运行，需手动加 &。输出重定向可覆盖默认的 nohup.out。配合 disown 更彻底。'
        },
        {
            'cmd_name': 'screen',
            'name_cn': '终端复用器（传统）',
            'function_desc': '终端复用器，允许在单个 SSH 会话中创建多个虚拟终端窗口，会话可分离和重新附加。',
            'syntax': 'screen [选项] [命令]',
            'params_json': '[{"参数":"-S","说明":"指定会话名称","必填":"可选"},{"参数":"-ls","说明":"列出所有会话","必填":"可选"},{"参数":"-r","说明":"重新附加到会话","必填":"可选"},{"参数":"-d","说明":"分离当前会话","必填":"可选"}]',
            'example_basic': 'screen -S mysession',
            'example_adv': 'screen -dmS build bash -c "make; exec bash"',
            'os_type': 'Linux/macOS', 'aliases': '终端复用,screen,虚拟终端',
            'tips': 'screen 快捷键：Ctrl+A D 分离，Ctrl+A C 新建窗口，Ctrl+A N/P 切换窗口，Ctrl+A K 关闭窗口。'
        },
        {
            'cmd_name': 'tmux',
            'name_cn': '终端复用器（现代）',
            'function_desc': '功能更强大的终端复用器，支持分屏、会话管理、窗口分组等。比 screen 有更好的配置和扩展性。',
            'syntax': 'tmux [子命令] [选项]',
            'params_json': '[{"参数":"new","说明":"创建新会话","必填":"可选"},{"参数":"-s","说明":"指定会话名称","必填":"可选"},{"参数":"attach","说明":"附加到已有会话","必填":"可选"},{"参数":"ls","说明":"列出所有会话","必填":"可选"}]',
            'example_basic': 'tmux new -s mysession',
            'example_adv': 'tmux new-session -d -s dev "vim main.py"',
            'os_type': 'Linux/macOS', 'aliases': '终端复用,tmux,分屏',
            'tips': 'tmux 前缀键默认 Ctrl+B。常用：% 垂直分屏，" 水平分屏，d 分离，c 新建窗口，, 重命名窗口。'
        },
        {
            'cmd_name': 'uptime',
            'name_cn': '系统运行时间',
            'function_desc': '显示系统已运行时间、当前时间、登录用户数和系统平均负载。快速了解系统状态。',
            'syntax': 'uptime [选项]',
            'params_json': '[{"参数":"-s","说明":"显示系统启动时间","必填":"可选"},{"参数":"-p","说明":"以友好格式显示运行时间","必填":"可选"}]',
            'example_basic': 'uptime',
            'example_adv': 'uptime -p',
            'os_type': 'Linux/macOS', 'aliases': '运行时间,uptime,负载',
            'tips': '平均负载三个数字分别代表 1/5/15 分钟平均。负载值除以 CPU 核心数得到合理利用率。'
        },
        {
            'cmd_name': 'whoami',
            'name_cn': '显示当前用户',
            'function_desc': '打印当前登录用户的用户名。等同于 id -un。常用于脚本中判断执行用户。',
            'syntax': 'whoami',
            'params_json': '[]',
            'example_basic': 'whoami',
            'example_adv': 'if [ "$(whoami)" != "root" ]; then echo "请用 root 运行"; exit 1; fi',
            'os_type': 'Linux/macOS', 'aliases': '当前用户,whoami,用户',
            'tips': 'whoami 不考虑 sudo 提升，用 sudo whoami 仍显示 root。id 命令提供更详细的信息。'
        },
        {
            'cmd_name': 'id',
            'name_cn': '用户身份信息',
            'function_desc': '显示用户和用户组的详细信息，包括 UID、GID 和所属组列表。',
            'syntax': 'id [选项] [用户名]',
            'params_json': '[{"参数":"-u","说明":"仅显示 UID","必填":"可选"},{"参数":"-g","说明":"仅显示主组 GID","必填":"可选"},{"参数":"-G","说明":"显示所有组 GID","必填":"可选"},{"参数":"-n","说明":"显示名称而非数字 ID","必填":"可选"}]',
            'example_basic': 'id',
            'example_adv': 'id -un www-data',
            'os_type': 'Linux/macOS', 'aliases': '用户信息,id,UID',
            'tips': 'id -un 等价于 whoami。id www-data 查看指定用户的完整信息。用于调试权限问题。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Linux: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Linux: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# Linux 用户管理补充（+10条）
# ============================================================
def seed_linux_user_supplement(db):
    cat_id = get_cat_id('命令行工具', 'Linux终端')
    if not cat_id:
        return 0

    commands = [
        {
            'cmd_name': 'useradd',
            'name_cn': '创建用户',
            'function_desc': '在系统中创建新用户账户，并可以同时设置主目录、Shell 和所属组。',
            'syntax': 'useradd [选项] <用户名>',
            'params_json': '[{"参数":"-m","说明":"创建用户主目录","必填":"可选"},{"参数":"-s","说明":"指定登录 Shell","必填":"可选"},{"参数":"-G","说明":"指定附加组","必填":"可选"},{"参数":"-g","说明":"指定主组","必填":"可选"}]',
            'example_basic': 'useradd -m -s /bin/bash newuser',
            'example_adv': 'useradd -m -s /bin/bash -G sudo,docker -c "John Doe" johndoe',
            'os_type': 'Linux', 'aliases': '创建用户,useradd,新增用户',
            'tips': '创建用户后需用 passwd 设置密码。useradd 和 adduser 不同，adduser 是更友好的交互式工具。'
        },
        {
            'cmd_name': 'usermod',
            'name_cn': '修改用户',
            'function_desc': '修改已存在用户的属性，如用户名、主目录、Shell、所属组等。',
            'syntax': 'usermod [选项] <用户名>',
            'params_json': '[{"参数":"-aG","说明":"追加用户到附加组（常用）","必填":"可选"},{"参数":"-l","说明":"修改用户名","必填":"可选"},{"参数":"-d","说明":"修改主目录","必填":"可选"},{"参数":"-s","说明":"修改登录 Shell","必填":"可选"}]',
            'example_basic': 'usermod -aG sudo username',
            'example_adv': 'usermod -l newname -d /home/newname -m oldname',
            'os_type': 'Linux', 'aliases': '修改用户,usermod,用户管理',
            'tips': '用 -aG 追加组而不是 -G，否则会移除用户当前所属的其他组。修改用户名后需同步修改主目录。'
        },
        {
            'cmd_name': 'passwd',
            'name_cn': '修改密码',
            'function_desc': '设置或修改用户密码。普通用户只能改自己的密码，root 可改任何用户密码。',
            'syntax': 'passwd [用户名]',
            'params_json': '[{"参数":"-l","说明":"锁定用户密码（禁用登录）","必填":"可选"},{"参数":"-u","说明":"解锁用户密码","必填":"可选"},{"参数":"-d","说明":"删除密码（空密码登录）","必填":"可选"}]',
            'example_basic': 'passwd',
            'example_adv': 'echo "newpass" | passwd --stdin username',
            'os_type': 'Linux', 'aliases': '密码,passwd,修改密码',
            'tips': 'passwd --stdin 在脚本中可用（部分发行版不支持）。passwd -S 查看密码状态信息。'
        },
        {
            'cmd_name': 'chown',
            'name_cn': '修改文件所有者',
            'function_desc': '更改文件或目录的所有者和/或所属组。需要 root 权限才能更改所有者。',
            'syntax': 'chown [选项] <用户>[:组] <路径>',
            'params_json': '[{"参数":"-R","说明":"递归修改目录内所有文件","必填":"可选"},{"参数":"用户","说明":"新所有者用户名或 UID","必填":"是"},{"参数":":组","说明":"新所属组（可选）","必填":"可选"}]',
            'example_basic': 'chown user:group file.txt',
            'example_adv': 'chown -R www-data:www-data /var/www/html',
            'os_type': 'Linux', 'aliases': '更改所有者,chown,权限',
            'tips': '只改所属组可以省略用户名如 :group。chown user: 会将组改为用户的默认组。'
        },
        {
            'cmd_name': 'chgrp',
            'name_cn': '修改文件所属组',
            'function_desc': '更改文件或目录的所属组。用户必须是目标组的成员或 root。',
            'syntax': 'chgrp [选项] <组名> <路径>',
            'params_json': '[{"参数":"-R","说明":"递归修改目录内所有文件","必填":"可选"},{"参数":"组名","说明":"新所属组名称","必填":"是"}]',
            'example_basic': 'chgrp staff file.txt',
            'example_adv': 'chgrp -R www-data /var/www/html',
            'os_type': 'Linux', 'aliases': '更改组,chgrp,组权限',
            'tips': 'chgrp 是 chown 的子集操作，chown :group file 效果相同。需要相应权限才能更改。'
        },
        {
            'cmd_name': 'mount',
            'name_cn': '挂载文件系统',
            'function_desc': '将设备（如硬盘分区、USB、ISO）挂载到目录树上的某个挂载点，使其内容可访问。',
            'syntax': 'mount [选项] <设备> <挂载点>',
            'params_json': '[{"参数":"-t","说明":"指定文件系统类型（如 ext4, ntfs）","必填":"可选"},{"参数":"-o","说明":"挂载选项（如 ro,rw,noexec）","必填":"可选"},{"参数":"-a","说明":"挂载 /etc/fstab 中的所有设备","必填":"可选"}]',
            'example_basic': 'mount /dev/sdb1 /mnt/usb',
            'example_adv': 'mount -t ntfs-3g -o uid=1000,gid=1000,umask=022 /dev/sdb1 /mnt/data',
            'os_type': 'Linux', 'aliases': '挂载,mount,文件系统',
            'tips': 'mount 无参数显示当前所有挂载。umount 卸载前确保没有进程在使用该挂载点。'
        },
        {
            'cmd_name': 'umount',
            'name_cn': '卸载文件系统',
            'function_desc': '卸载已挂载的文件系统，使其从目录树中移除。',
            'syntax': 'umount <挂载点或设备>',
            'params_json': '[{"参数":"-l","说明":"延迟卸载（设备忙时使用）","必填":"可选"},{"参数":"-f","说明":"强制卸载（可能损坏数据）","必填":"可选"}]',
            'example_basic': 'umount /mnt/usb',
            'example_adv': 'umount -l /mnt/data',
            'os_type': 'Linux', 'aliases': '卸载,umount,umount',
            'tips': '出现 "target is busy" 时用 lsof 或 fuser 查找占用进程。umount -l 延迟卸载可解决。'
        },
        {
            'cmd_name': 'fdisk',
            'name_cn': '磁盘分区管理',
            'function_desc': '交互式磁盘分区工具，用于创建、删除、修改磁盘分区表。支持 MBR 和 GPT 分区表。',
            'syntax': 'fdisk [选项] <磁盘设备>',
            'params_json': '[{"参数":"-l","说明":"列出所有磁盘和分区信息","必填":"可选"},{"参数":"磁盘设备","说明":"如 /dev/sda","必填":"是"}]',
            'example_basic': 'fdisk -l',
            'example_adv': 'echo -e "n\\np\\n1\\n\\n+10G\\nw" | fdisk /dev/sdb',
            'os_type': 'Linux', 'aliases': '分区,fdisk,磁盘管理',
            'tips': '注意区分磁盘设备（/dev/sda）和分区（/dev/sda1）。parted 更适合超过 2TB 的磁盘。'
        },
        {
            'cmd_name': 'parted',
            'name_cn': '高级分区工具',
            'function_desc': 'GNU 分区编辑器，支持 GPT 分区表和超过 2TB 的大磁盘。比 fdisk 功能更强大。',
            'syntax': 'parted [选项] <磁盘设备> [命令]',
            'params_json': '[{"参数":"-l","说明":"列出所有设备的分区信息","必填":"可选"},{"参数":"mklabel","说明":"创建新分区表（gpt/msdos）","必填":"可选"},{"参数":"mkpart","说明":"创建新分区","必填":"可选"}]',
            'example_basic': 'parted /dev/sdb mklabel gpt',
            'example_adv': 'parted /dev/sdb mkpart primary ext4 1MiB 100%',
            'os_type': 'Linux', 'aliases': '分区,parted,gpt分区',
            'tips': 'parted 的操作会立即生效，没有确认提示。用 print 命令查看当前分区表。'
        },
        {
            'cmd_name': 'mkfs',
            'name_cn': '创建文件系统',
            'function_desc': '在磁盘分区上创建文件系统（格式化）。不同版本如 mkfs.ext4, mkfs.xfs, mkfs.ntfs 等。',
            'syntax': 'mkfs [.文件系统类型] <分区>',
            'params_json': '[{"参数":"-t","说明":"指定文件系统类型","必填":"可选"},{"参数":"-L","说明":"设置卷标","必填":"可选"},{"参数":"分区","说明":"要格式化的分区设备","必填":"是"}]',
            'example_basic': 'mkfs.ext4 /dev/sdb1',
            'example_adv': 'mkfs.ext4 -L mydata -m 0 /dev/sdb1',
            'os_type': 'Linux', 'aliases': '格式化,mkfs,文件系统',
            'tips': 'mkfs 会破坏分区上的所有数据，操作前务必确认。mkfs.ext4 -m 0 将保留块设为 0，增加可用空间。'
        },
        {
            'cmd_name': 'dd',
            'name_cn': '数据复制/转换',
            'function_desc': '低级别的数据复制工具，按块从源复制到目标。常用于制作启动盘、磁盘克隆和数据恢复。',
            'syntax': 'dd if=<源> of=<目标> [选项]',
            'params_json': '[{"参数":"if","说明":"输入文件（源）","必填":"是"},{"参数":"of","说明":"输出文件（目标）","必填":"是"},{"参数":"bs","说明":"块大小","必填":"可选"},{"参数":"status=progress","说明":"显示进度（新版 dd）","必填":"可选"}]',
            'example_basic': 'dd if=/dev/sda of=/dev/sdb bs=4M status=progress',
            'example_adv': 'dd if=/dev/zero of=/dev/sdb bs=1M count=100 status=progress',
            'os_type': 'Linux', 'aliases': '复制,dd,磁盘克隆',
            'tips': 'dd 是危险工具，弄反 if 和 of 会销毁数据。建议用 status=progress 参数查看复制进度。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Linux-user: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Linux-user: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# Linux 硬件/驱动补充（+5条）
# ============================================================
def seed_linux_hw_supplement(db):
    cat_id = get_cat_id('命令行工具', 'Linux终端')
    if not cat_id:
        return 0

    commands = [
        {
            'cmd_name': 'lspci',
            'name_cn': '列出 PCI 设备',
            'function_desc': '显示系统中所有 PCI 总线设备的信息，包括显卡、网卡、声卡等。',
            'syntax': 'lspci [选项]',
            'params_json': '[{"参数":"-v","说明":"详细输出","必填":"可选"},{"参数":"-vv","说明":"更详细输出","必填":"可选"},{"参数":"-k","说明":"显示驱动模块","必填":"可选"}]',
            'example_basic': 'lspci',
            'example_adv': 'lspci -vvk | grep -A 20 "VGA"',
            'os_type': 'Linux', 'aliases': 'PCI设备,lspci,硬件列表',
            'tips': 'lspci -k 显示每个设备使用的内核驱动。lspci -nn 显示厂商和设备 ID。'
        },
        {
            'cmd_name': 'lsusb',
            'name_cn': '列出 USB 设备',
            'function_desc': '显示系统中所有 USB 总线设备的信息，包括键盘、鼠标、U 盘等外设。',
            'syntax': 'lsusb [选项]',
            'params_json': '[{"参数":"-v","说明":"详细输出","必填":"可选"},{"参数":"-t","说明":"以树状结构显示","必填":"可选"}]',
            'example_basic': 'lsusb',
            'example_adv': 'lsusb -t',
            'os_type': 'Linux', 'aliases': 'USB设备,lsusb,外设列表',
            'tips': 'lsusb -v 显示详细描述符信息。插入 U 盘后执行 lsusb 可确认设备是否被识别。'
        },
        {
            'cmd_name': 'lshw',
            'name_cn': '硬件配置',
            'function_desc': '显示系统完整的硬件配置信息，包括 CPU、内存、磁盘、网络等详细规格。',
            'syntax': 'lshw [选项]',
            'params_json': '[{"参数":"-short","说明":"简洁输出","必填":"可选"},{"参数":"-class","说明":"按类别过滤（如 cpu, memory, disk）","必填":"可选"},{"参数":"-json","说明":"JSON 格式输出","必填":"可选"}]',
            'example_basic': 'lshw -short',
            'example_adv': 'lshw -class memory -json | python3 -m json.tool',
            'os_type': 'Linux', 'aliases': '硬件信息,lshw,硬件配置',
            'tips': 'lshw 需要 root 权限才能获取完整信息。lshw -short 给出简洁的硬件列表。'
        },
        {
            'cmd_name': 'modprobe',
            'name_cn': '内核模块管理',
            'function_desc': '添加、移除和管理 Linux 内核模块。自动处理模块依赖关系。',
            'syntax': 'modprobe [选项] <模块名>',
            'params_json': '[{"参数":"-r","说明":"移除模块","必填":"可选"},{"参数":"--show-depends","说明":"显示模块依赖关系","必填":"可选"},{"参数":"-l","说明":"列出可用模块（旧）","必填":"可选"}]',
            'example_basic': 'modprobe vfio-pci',
            'example_adv': 'modprobe -r nvidia_drm nvidia_modeset nvidia',
            'os_type': 'Linux', 'aliases': '内核模块,modprobe,驱动',
            'tips': '模块配置文件在 /etc/modprobe.d/。lsmod 列出已加载模块，modinfo 查看模块信息。'
        },
        {
            'cmd_name': 'lsmod',
            'name_cn': '列出已加载模块',
            'function_desc': '显示当前已加载到内核中的所有模块及其使用计数和依赖关系。',
            'syntax': 'lsmod',
            'params_json': '[]',
            'example_basic': 'lsmod',
            'example_adv': 'lsmod | grep -i nvidia',
            'os_type': 'Linux', 'aliases': '已加载模块,lsmod,内核模块',
            'tips': '第一列是模块名，第二列是大小，第三列是被多少其他模块使用。rmmod 可卸载不需要的模块。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Linux-hw: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Linux-hw: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# CMD Windows 补充（+25条）
# ============================================================
def seed_cmd_supplement(db):
    cat_id = get_cat_id('命令行工具', 'CMD (Windows)')
    if not cat_id:
        print('[ERR] 未找到 CMD (Windows) 分类')
        return 0

    commands = [
        {
            'cmd_name': 'assoc',
            'name_cn': '显示/修改文件关联',
            'function_desc': '显示或修改文件扩展名与程序之间的关联。可设置 .txt 文件默认用记事本打开等。',
            'syntax': 'assoc [.扩展名=文件类型]',
            'params_json': '[{"参数":".扩展名","说明":"文件扩展名（如 .txt）","必填":"可选"},{"参数":"文件类型","说明":"关联的文件类型标识符","必填":"可选"}]',
            'example_basic': 'assoc .txt',
            'example_adv': 'assoc .log=txtfile',
            'os_type': 'Windows', 'aliases': '文件关联,assoc,关联',
            'tips': '用 ftype 查看/设置文件类型对应的打开程序。assoc 单独运行列出所有关联。'
        },
        {
            'cmd_name': 'ftype',
            'name_cn': '显示/修改文件类型',
            'function_desc': '显示或修改文件类型关联的打开命令，与 assoc 配合使用。',
            'syntax': 'ftype [文件类型=打开命令]',
            'params_json': '[{"参数":"文件类型","说明":"文件类型标识符","必填":"可选"},{"参数":"打开命令","说明":"如 notepad.exe %1","必填":"可选"}]',
            'example_basic': 'ftype txtfile',
            'example_adv': 'ftype txtfile=C:\\Windows\\notepad.exe %1',
            'os_type': 'Windows', 'aliases': '文件类型,ftype,打开方式',
            'tips': '%1 代表双击的文件路径，%* 代表所有参数。修改后无需重启立即生效。'
        },
        {
            'cmd_name': 'attrib',
            'name_cn': '查看/修改文件属性',
            'function_desc': '显示或修改文件的属性（只读、隐藏、系统、归档）。',
            'syntax': 'attrib [+R|-R] [+H|-H] [+S|-S] [+A|-A] <文件>',
            'params_json': '[{"参数":"+R/-R","说明":"设置/取消只读属性","必填":"可选"},{"参数":"+H/-H","说明":"设置/取消隐藏属性","必填":"可选"},{"参数":"+S/-S","说明":"设置/取消系统属性","必填":"可选"},{"参数":"+A/-A","说明":"设置/取消归档属性","必填":"可选"}]',
            'example_basic': 'attrib +h secret.txt',
            'example_adv': 'attrib -h -s /s /d D:\\*.*',
            'os_type': 'Windows', 'aliases': '文件属性,attrib,隐藏文件',
            'tips': '/s 处理子目录，/d 处理目录本身。要显示隐藏文件需在资源管理器中开启"显示隐藏文件"。'
        },
        {
            'cmd_name': 'cacls',
            'name_cn': '文件权限管理',
            'function_desc': '显示或修改文件/目录的访问控制列表（ACL）。在较新 Windows 中推荐使用 icacls。',
            'syntax': 'cacls <文件> [/T] [/E] [/G 用户:权限] [/R 用户]',
            'params_json': '[{"参数":"/T","说明":"递归处理子目录","必填":"可选"},{"参数":"/E","说明":"编辑现有 ACL 而非替换","必填":"可选"},{"参数":"/G","说明":"授予权限","必填":"可选"},{"参数":"/R","说明":"撤销权限","必填":"可选"}]',
            'example_basic': 'cacls file.txt',
            'example_adv': 'cacls C:\\Project /E /T /G Users:C',
            'os_type': 'Windows', 'aliases': '权限,cacls,ACL',
            'tips': 'Windows 10+ 推荐使用 icacls 替代 cacls。权限：F=完全控制，C=修改，R=只读。'
        },
        {
            'cmd_name': 'icacls',
            'name_cn': '高级文件权限',
            'function_desc': '显示和修改文件/目录的 DACL，是 cacls 的现代替代品，支持更精细的权限控制。',
            'syntax': 'icacls <文件> [/grant 用户:权限] [/remove 用户]',
            'params_json': '[{"参数":"/grant","说明":"授予权限","必填":"可选"},{"参数":"/remove","说明":"移除权限","必填":"可选"},{"参数":"/inheritance","说明":"设置继承策略","必填":"可选"},{"参数":"/T","说明":"递归处理","必填":"可选"}]',
            'example_basic': 'icacls C:\\Folder',
            'example_adv': 'icacls C:\\Folder /grant "Users":(OI)(CI)F /T',
            'os_type': 'Windows', 'aliases': '权限,icacls,ACL,安全',
            'tips': '权限标识：F=完全控制，M=修改，RX=读取和执行，R=只读。OI=对象继承，CI=容器继承。'
        },
        {
            'cmd_name': 'chkdsk',
            'name_cn': '磁盘检查',
            'function_desc': '检查磁盘文件系统完整性和元数据，并修复逻辑错误。也可扫描坏道。',
            'syntax': 'chkdsk [驱动器:] [/F] [/R]',
            'params_json': '[{"参数":"/F","说明":"修复磁盘错误","必填":"可选"},{"参数":"/R","说明":"修复坏扇区并恢复信息","必填":"可选"},{"参数":"/X","说明":"强制卸载卷","必填":"可选"}]',
            'example_basic': 'chkdsk C:',
            'example_adv': 'chkdsk D: /F /R',
            'os_type': 'Windows', 'aliases': '磁盘检查,chkdsk,磁盘修复',
            'tips': '使用 /F 或 /R 时需要锁定磁盘，系统盘会提示下次重启时检查。chkdsk 仅修复文件系统，坏道需用第三方工具。'
        },
        {
            'cmd_name': 'diskpart',
            'name_cn': '磁盘分区工具',
            'function_desc': '交互式磁盘分区管理工具，支持创建、删除、格式化分区，转换磁盘类型（MBR/GPT）。',
            'syntax': 'diskpart',
            'params_json': '[{"参数":"list disk","说明":"列出所有磁盘","必填":"是"},{"参数":"select disk","说明":"选择磁盘","必填":"是"},{"参数":"list partition","说明":"列出分区","必填":"可选"},{"参数":"clean","说明":"清除分区表","必填":"可选"}]',
            'example_basic': 'diskpart',
            'example_adv': 'echo select disk 1 | diskpart',
            'os_type': 'Windows', 'aliases': '分区,diskpart,磁盘管理',
            'tips': 'diskpart 操作危险，clean 会清除所有分区数据。可用 list disk -> select disk X -> clean 命令快速清空磁盘。'
        },
        {
            'cmd_name': 'sfc',
            'name_cn': '系统文件检查',
            'function_desc': '扫描并修复 Windows 系统文件的完整性。检测被篡改或损坏的系统文件并从缓存中替换。',
            'syntax': 'sfc /scannow',
            'params_json': '[{"参数":"/scannow","说明":"立即扫描所有受保护系统文件","必填":"是"},{"参数":"/verifyonly","说明":"仅检查不修复","必填":"可选"},{"参数":"/scanfile","说明":"扫描指定文件","必填":"可选"}]',
            'example_basic': 'sfc /scannow',
            'example_adv': 'sfc /scanfile=C:\\Windows\\System32\\kernel32.dll',
            'os_type': 'Windows', 'aliases': '系统文件,sfc,文件检查',
            'tips': 'sfc /scannow 需以管理员身份运行。如果修复失败，可先运行 DISM /RestoreHealth 修复系统映像源。'
        },
        {
            'cmd_name': 'dism',
            'name_cn': '部署映像管理',
            'function_desc': '用于维护和修复 Windows 映像（WIM）和系统文件。比 sfc 更底层，可修复系统映像源。',
            'syntax': 'dism /Online /Cleanup-Image /[操作]',
            'params_json': '[{"参数":"/RestoreHealth","说明":"扫描并修复系统映像","必填":"可选"},{"参数":"/CheckHealth","说明":"检查系统映像是否损坏","必填":"可选"},{"参数":"/ScanHealth","说明":"扫描系统映像损坏","必填":"可选"}]',
            'example_basic': 'dism /Online /Cleanup-Image /CheckHealth',
            'example_adv': 'dism /Online /Cleanup-Image /RestoreHealth /Source:C:\\RepairSource\\install.wim',
            'os_type': 'Windows', 'aliases': '映像,dism,系统修复',
            'tips': '推荐修复顺序：dism /RestoreHealth -> sfc /scannow。使用 /RestoreHealth 可能需要 Windows 安装源。'
        },
        {
            'cmd_name': 'bcdedit',
            'name_cn': '启动配置管理',
            'function_desc': '管理 Windows 启动配置数据（BCD），控制多系统启动、启动项、超时等。',
            'syntax': 'bcdedit [/enum] [/set 项 值]',
            'params_json': '[{"参数":"/enum","说明":"枚举当前启动项","必填":"可选"},{"参数":"/set","说明":"设置启动配置值","必填":"可选"},{"参数":"/timeout","说明":"设置启动菜单超时（秒）","必填":"可选"}]',
            'example_basic': 'bcdedit /enum',
            'example_adv': 'bcdedit /timeout 30',
            'os_type': 'Windows', 'aliases': '启动配置,bcdedit,Boot',
            'tips': 'bcdedit 修改启动配置影响重大，建议修改前备份（bcdedit /export C:\\bcd_backup）。'
        },
        {
            'cmd_name': 'shutdown',
            'name_cn': '关机/重启',
            'function_desc': '安全地关闭或重新启动计算机，支持延迟、注释和远程关机。',
            'syntax': 'shutdown [/s | /r | /l | /h] [/t 秒] [/c "注释"]',
            'params_json': '[{"参数":"/s","说明":"关机","必填":"可选"},{"参数":"/r","说明":"重启","必填":"可选"},{"参数":"/h","说明":"休眠","必填":"可选"},{"参数":"/t","说明":"延迟时间（秒）","必填":"可选"},{"参数":"/a","说明":"中止关机","必填":"可选"}]',
            'example_basic': 'shutdown /r /t 0',
            'example_adv': 'shutdown /s /t 60 /c "系统将在1分钟后维护"',
            'os_type': 'Windows', 'aliases': '关机,shutdown,重启',
            'tips': 'shutdown /a 可取消正在进行的关机。shutdown /g 重启后自动重启注册的应用。'
        },
        {
            'cmd_name': 'taskkill',
            'name_cn': '结束进程',
            'function_desc': '通过进程 ID 或映像名称终止正在运行的进程。支持远程和条件过滤。',
            'syntax': 'taskkill [/PID 进程ID | /IM 映像名] [/F] [/T]',
            'params_json': '[{"参数":"/PID","说明":"按进程 ID 终止","必填":"可选"},{"参数":"/IM","说明":"按映像名称终止（如 notepad.exe）","必填":"可选"},{"参数":"/F","说明":"强制终止进程","必填":"可选"},{"参数":"/T","说明":"终止子进程","必填":"可选"}]',
            'example_basic': 'taskkill /IM notepad.exe /F',
            'example_adv': 'taskkill /PID 1234 /F /T',
            'os_type': 'Windows', 'aliases': '结束进程,taskkill,杀进程',
            'tips': '强制终止（/F）可能丢失未保存数据。可用 tasklist 查找进程 ID。远程终止用 /S 系统名。'
        },
        {
            'cmd_name': 'schtasks',
            'name_cn': '计划任务',
            'function_desc': '创建、查询、修改和删除计划任务。比图形界面更灵活可控。',
            'syntax': 'schtasks /Create | /Query | /Delete | /Change [参数]',
            'params_json': '[{"参数":"/Create","说明":"创建新任务","必填":"可选"},{"参数":"/Query","说明":"查询任务","必填":"可选"},{"参数":"/SC","说明":"计划频率（ONCE, DAILY, WEEKLY等）","必填":"可选"},{"参数":"/TN","说明":"任务名称","必填":"可选"},{"参数":"/TR","说明":"任务运行的程序","必填":"可选"}]',
            'example_basic': 'schtasks /Query /FO LIST',
            'example_adv': 'schtasks /Create /SC DAILY /TN "Backup" /TR "backup.bat" /ST 02:00',
            'os_type': 'Windows', 'aliases': '计划任务,schtasks,定时任务',
            'tips': '/FO LIST 以列表格式显示，/FO CSV 以 CSV 格式显示。用 /Delete /F 强制删除任务。'
        },
        {
            'cmd_name': 'reg',
            'name_cn': '注册表操作',
            'function_desc': '在命令行中查询、添加、修改和删除注册表项和值。脚本操作注册表的标准方式。',
            'syntax': 'reg [Query | Add | Delete | Copy] [参数]',
            'params_json': '[{"参数":"Query","说明":"查询注册表项","必填":"可选"},{"参数":"Add","说明":"添加注册表项/值","必填":"可选"},{"参数":"Delete","说明":"删除注册表项/值","必填":"可选"},{"参数":"/v","说明":"指定值名称","必填":"可选"},{"参数":"/ve","说明":"指定默认值","必填":"可选"}]',
            'example_basic': 'reg Query HKLM\\Software /ve',
            'example_adv': 'reg Add HKCU\\Environment /v MY_VAR /t REG_SZ /d "value" /f',
            'os_type': 'Windows', 'aliases': '注册表,reg,注册表命令',
            'tips': '注册表根键：HKLM=本地机器，HKCU=当前用户，HKCR=类根，HKU=所有用户。'
        },
        {
            'cmd_name': 'regedit',
            'name_cn': '注册表编辑器',
            'function_desc': '启动图形化注册表编辑器。支持导入/导出 .reg 注册表文件。',
            'syntax': 'regedit [/E 导出文件] [/I 导入文件]',
            'params_json': '[{"参数":"/E","说明":"导出注册表到文件","必填":"可选"},{"参数":"/I","说明":"导入 .reg 文件","必填":"可选"},{"参数":"/S","说明":"静默模式（不提示）","必填":"可选"}]',
            'example_basic': 'regedit',
            'example_adv': 'regedit /S settings.reg',
            'os_type': 'Windows', 'aliases': '注册表编辑,regedit,注册表',
            'tips': 'regedit /E backup.reg HKEY_CURRENT_USER\\Software 备份部分注册表。导入 .reg 文件前建议备份。'
        },
        {
            'cmd_name': 'mstsc',
            'name_cn': '远程桌面连接',
            'function_desc': '启动 Windows 远程桌面连接（RDP）客户端，连接到远程 Windows 桌面。',
            'syntax': 'mstsc [/v:服务器] [/f] [/admin]',
            'params_json': '[{"参数":"/v","说明":"指定远程服务器地址","必填":"可选"},{"参数":"/f","说明":"全屏模式","必填":"可选"},{"参数":"/admin","说明":"连接到管理会话","必填":"可选"},{"参数":"/edit","说明":"编辑 RDP 文件","必填":"可选"}]',
            'example_basic': 'mstsc /v:192.168.1.100',
            'example_adv': 'mstsc /v:192.168.1.100 /f /admin',
            'os_type': 'Windows', 'aliases': '远程桌面,mstsc,RDP',
            'tips': 'RDP 连接信息可保存为 .rdp 文件，用 mstsc file.rdp 打开。端口默认 3389。'
        },
        {
            'cmd_name': 'msinfo32',
            'name_cn': '系统信息',
            'function_desc': '打开系统信息工具，显示硬件、系统组件和软件环境的详细信息。',
            'syntax': 'msinfo32 [/report 文件] [/computer 计算机名]',
            'params_json': '[{"参数":"/report","说明":"导出系统信息到文件","必填":"可选"},{"参数":"/computer","说明":"查看远程计算机信息","必填":"可选"}]',
            'example_basic': 'msinfo32',
            'example_adv': 'msinfo32 /report C:\\sysinfo.txt',
            'os_type': 'Windows', 'aliases': '系统信息,msinfo32,硬件信息',
            'tips': 'msinfo32 /nfo C:\\sysinfo.nfo 导出为 NFO 格式。命令行也可用 systeminfo 获取文本信息。'
        },
        {
            'cmd_name': 'dxdiag',
            'name_cn': 'DirectX 诊断',
            'function_desc': '打开 DirectX 诊断工具，显示 DirectX 版本、显卡/声卡信息和驱动详情。',
            'syntax': 'dxdiag [/x 输出文件 | /t 输出文件]',
            'params_json': '[{"参数":"/x","说明":"将诊断信息导出为 XML","必填":"可选"},{"参数":"/t","说明":"将诊断信息导出为文本文件","必填":"可选"},{"参数":"/64bit","说明":"64位版本","必填":"可选"}]',
            'example_basic': 'dxdiag',
            'example_adv': 'dxdiag /t C:\\dxdiag.txt',
            'os_type': 'Windows', 'aliases': 'DirectX,dxdiag,显卡诊断',
            'tips': 'dxdiag 可用于检查 DirectX 版本、显卡型号和驱动是否正常工作。'
        },
        {
            'cmd_name': 'color',
            'name_cn': '设置控制台颜色',
            'function_desc': '设置 CMD 控制台的前景色和背景色。颜色值由两个十六进制数字指定（背景+前景）。',
            'syntax': 'color [背景][前景]',
            'params_json': '[{"参数":"背景","说明":"背景色十六进制值（0-F）","必填":"可选"},{"参数":"前景","说明":"前景色十六进制值（0-F）","必填":"可选"}]',
            'example_basic': 'color 0A',
            'example_adv': 'color 17',
            'os_type': 'Windows', 'aliases': '颜色,color,控制台颜色',
            'tips': '颜色代码：0=黑,1=蓝,2=绿,3=青,4=红,5=紫,6=黄,7=白,8=灰,9=亮蓝,A=亮绿,B=亮青,C=亮红,D=亮紫,E=亮黄,F=亮白。'
        },
        {
            'cmd_name': 'prompt',
            'name_cn': '修改命令提示符',
            'function_desc': '修改 CMD 提示符的显示格式，支持特殊字符如 $P（路径）、$G（>）等。',
            'syntax': 'prompt [文本及代码]',
            'params_json': '[{"参数":"$P","说明":"当前路径","必填":"可选"},{"参数":"$G","说明":"> 符号","必填":"可选"},{"参数":"$D","说明":"当前日期","必填":"可选"},{"参数":"$T","说明":"当前时间","必填":"可选"}]',
            'example_basic': 'prompt $P$G',
            'example_adv': 'prompt [$T] $P$G',
            'os_type': 'Windows', 'aliases': '提示符,prompt,CMD提示',
            'tips': '特殊代码：$P=路径, $G=>, $L=<, $D=日期, $T=时间, $_=换行, $$=$。输入 prompt 恢复默认。'
        },
        {
            'cmd_name': 'title',
            'name_cn': '设置窗口标题',
            'function_desc': '设置当前 CMD 控制台窗口的标题文本。',
            'syntax': 'title <新标题>',
            'params_json': '[{"参数":"新标题","说明":"窗口标题文本","必填":"是"}]',
            'example_basic': 'title My Script',
            'example_adv': 'title Backup in Progress - %DATE% %TIME%',
            'os_type': 'Windows', 'aliases': '标题,title,窗口标题',
            'tips': '常用在批处理脚本开头标记当前脚本功能，便于多窗口时区分。'
        },
        {
            'cmd_name': 'path',
            'name_cn': '设置/显示路径',
            'function_desc': '显示或设置可执行文件的搜索路径。影响命令搜索范围。',
            'syntax': 'path [目录1;目录2;...]',
            'params_json': '[{"参数":"目录","说明":"要添加的搜索路径，分号分隔","必填":"可选"}]',
            'example_basic': 'path',
            'example_adv': 'path %PATH%;C:\\MyTools\\bin',
            'os_type': 'Windows', 'aliases': '路径,path,环境变量',
            'tips': 'path 不加参数显示当前路径。使用 %PATH% 在原有基础上追加。set PATH=... 是另一种方式。'
        },
        {
            'cmd_name': 'ver',
            'name_cn': '系统版本',
            'function_desc': '显示当前 Windows 操作系统的版本号。',
            'syntax': 'ver',
            'params_json': '[]',
            'example_basic': 'ver',
            'example_adv': 'ver | findstr /i "10" && echo 这是 Windows 10/11',
            'os_type': 'Windows', 'aliases': '版本,ver,系统版本',
            'tips': 'ver 只显示简要版本号。systeminfo 显示更详细的系统版本信息。'
        },
        {
            'cmd_name': 'vol',
            'name_cn': '显示磁盘卷标',
            'function_desc': '显示指定驱动器的卷标和序列号。',
            'syntax': 'vol [驱动器:]',
            'params_json': '[{"参数":"驱动器:","说明":"驱动器盘符（默认当前）","必填":"可选"}]',
            'example_basic': 'vol C:',
            'example_adv': 'vol D:',
            'os_type': 'Windows', 'aliases': '卷标,vol,磁盘卷',
            'tips': '用 label 命令可修改卷标。卷序列号在格式化时生成。'
        },
        {
            'cmd_name': 'label',
            'name_cn': '修改磁盘卷标',
            'function_desc': '创建、修改或删除磁盘的卷标（名称）。',
            'syntax': 'label [驱动器:] [新卷标]',
            'params_json': '[{"参数":"驱动器:","说明":"驱动器盘符","必填":"可选"},{"参数":"新卷标","说明":"新卷标名称","必填":"可选"}]',
            'example_basic': 'label D: BACKUP',
            'example_adv': 'label E:',
            'os_type': 'Windows', 'aliases': '卷标,label,磁盘名称',
            'tips': '卷标不能包含：* ? / \\ | , ; : + = [ ] < > "。不指定新卷标会提示输入。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] CMD: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] CMD: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# CMD Windows 补充2（+8条 - 目录/脚本相关）
# ============================================================
def seed_cmd2_supplement(db):
    cat_id = get_cat_id('命令行工具', 'CMD (Windows)')
    if not cat_id:
        return 0

    commands = [
        {
            'cmd_name': 'subst',
            'name_cn': '虚拟驱动器',
            'function_desc': '将文件夹路径映射为一个虚拟驱动器盘符。退出登录后失效。',
            'syntax': 'subst [盘符: 路径]',
            'params_json': '[{"参数":"盘符:","说明":"要使用的虚拟驱动器盘符","必填":"是"},{"参数":"路径","说明":"要映射的文件夹路径","必填":"是"},{"参数":"/D","说明":"删除虚拟驱动器","必填":"可选"}]',
            'example_basic': 'subst X: D:\\Projects',
            'example_adv': 'subst X: D:\\Projects /D',
            'os_type': 'Windows', 'aliases': '虚拟驱动器,subst,映射',
            'tips': 'subst 不加参数显示所有虚拟驱动器。重启后消失，可在启动脚本中设置。'
        },
        {
            'cmd_name': 'pushd',
            'name_cn': '压入目录栈',
            'function_desc': '将当前目录保存到目录栈并切换到指定目录，配合 popd 使用实现目录切换记忆。',
            'syntax': 'pushd <目录路径>',
            'params_json': '[{"参数":"目录路径","说明":"要进入并压入栈的目录","必填":"是"}]',
            'example_basic': 'pushd D:\\Projects',
            'example_adv': 'pushd \\\\server\\share && dir && popd',
            'os_type': 'Windows', 'aliases': '目录栈,pushd,切换目录',
            'tips': 'pushd 可以在网络路径映射盘符。popd 恢复原目录并从栈中移除。'
        },
        {
            'cmd_name': 'popd',
            'name_cn': '弹出目录栈',
            'function_desc': '切换到目录栈中最近保存的目录，并从栈中移除该目录。',
            'syntax': 'popd',
            'params_json': '[]',
            'example_basic': 'popd',
            'example_adv': 'pushd C:\\Windows && dir *.exe && popd',
            'os_type': 'Windows', 'aliases': '目录栈,popd,返回目录',
            'tips': 'popd 自动删除 pushd 创建的临时盘符（网络路径）。可多次嵌套使用。'
        },
        {
            'cmd_name': 'start',
            'name_cn': '启动程序',
            'function_desc': '在新窗口中启动指定的程序或命令。默认打开新 CMD 窗口。',
            'syntax': 'start [/MIN] [/MAX] [/B] <程序> [参数]',
            'params_json': '[{"参数":"/MIN","说明":"最小化启动窗口","必填":"可选"},{"参数":"/MAX","说明":"最大化启动窗口","必填":"可选"},{"参数":"/B","说明":"不在新窗口中启动（同进程）","必填":"可选"},{"参数":"/WAIT","说明":"等待程序退出","必填":"可选"}]',
            'example_basic': 'start notepad.exe',
            'example_adv': 'start /MIN /WAIT "Backup" backup.bat',
            'os_type': 'Windows', 'aliases': '启动,start,执行',
            'tips': 'start "" "path with spaces" 必须用两个引号。用 start . 打开当前目录的资源管理器。'
        },
        {
            'cmd_name': 'timeout',
            'name_cn': '延迟等待',
            'function_desc': '暂停命令执行指定的秒数，或等待按键。常用于批处理脚本节奏控制。',
            'syntax': 'timeout /T <秒数> [/NOBREAK]',
            'params_json': '[{"参数":"/T","说明":"等待的秒数（1-99999）","必填":"是"},{"参数":"/NOBREAK","说明":"忽略按键直接等待到超时","必填":"可选"}]',
            'example_basic': 'timeout /T 5',
            'example_adv': 'timeout /T 10 /NOBREAK >nul',
            'os_type': 'Windows', 'aliases': '延迟,timeout,等待',
            'tips': '>nul 隐藏等待剩余时间倒计时输出。按 Ctrl+C 可中断等待。'
        },
        {
            'cmd_name': 'choice',
            'name_cn': '选择交互',
            'function_desc': '在批处理脚本中暂停并提示用户选择，根据按键设置 ERRORLEVEL。',
            'syntax': 'choice /C <选项> /M "<提示>"',
            'params_json': '[{"参数":"/C","说明":"指定可选按键","必填":"是"},{"参数":"/M","说明":"显示提示信息","必填":"可选"},{"参数":"/N","说明":"不显示选项列表","必填":"可选"},{"参数":"/T","说明":"超时秒数和默认选项","必填":"可选"}]',
            'example_basic': 'choice /C YN /M "确认删除?"',
            'example_adv': 'choice /C ABC /T 10 /D A /M "请选择A/B/C"',
            'os_type': 'Windows', 'aliases': '选择,choice,交互',
            'tips': '通过 %ERRORLEVEL% 获取选择结果，第一选项返回 1。超时用 /D 指定默认选项。'
        },
        {
            'cmd_name': 'find',
            'name_cn': '查找文本',
            'function_desc': '在文件中搜索指定字符串，输出包含该字符串的行。CMD 中类似 Linux grep 的基础命令。',
            'syntax': 'find [/I] [/N] [/V] "字符串" <文件>',
            'params_json': '[{"参数":"/I","说明":"忽略大小写","必填":"可选"},{"参数":"/N","说明":"显示行号","必填":"可选"},{"参数":"/V","说明":"显示不包含字符串的行","必填":"可选"},{"参数":"/C","说明":"只显示匹配行数","必填":"可选"}]',
            'example_basic': 'find "ERROR" log.txt',
            'example_adv': 'find /I /N "error" *.log',
            'os_type': 'Windows', 'aliases': '查找,find,搜索文本',
            'tips': 'findstr 是 find 的增强版，支持正则表达式。字符串必须用双引号括起来。'
        },
        {
            'cmd_name': 'findstr',
            'name_cn': '高级文本查找',
            'function_desc': '在文件中搜索文本模式，支持正则表达式，是 find 的增强版。',
            'syntax': 'findstr [/I] [/R] [/C:字符串] <文件>',
            'params_json': '[{"参数":"/I","说明":"忽略大小写","必填":"可选"},{"参数":"/R","说明":"字符串被视为正则表达式","必填":"可选"},{"参数":"/C:","说明":"字面匹配（含空格）","必填":"可选"},{"参数":"/S","说明":"递归搜索子目录","必填":"可选"}]',
            'example_basic': 'findstr "error" *.txt',
            'example_adv': 'findstr /I /R "^[0-9].*\\.exe" *.txt',
            'os_type': 'Windows', 'aliases': '查找,findstr,正则搜索',
            'tips': 'findstr 支持有限的正则表达式。用 /C:"精确字符串" 匹配含空格的精确短语。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] CMD2: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] CMD2: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# Docker 补充（+18条）
# ============================================================
def seed_docker_supplement(db):
    cat_id = get_cat_id('命令行工具', 'Docker')
    if not cat_id:
        print('[ERR] 未找到 Docker 分类')
        return 0

    commands = [
        {
            'cmd_name': 'docker ps',
            'name_cn': '列出容器',
            'function_desc': '列出正在运行的容器。加上 -a 参数列出所有容器（包括已停止的）。',
            'syntax': 'docker ps [-a] [--format]',
            'params_json': '[{"参数":"-a","说明":"列出所有容器（包括已停止的）","必填":"可选"},{"参数":"-q","说明":"仅显示容器 ID","必填":"可选"},{"参数":"--format","说明":"自定义输出格式","必填":"可选"}]',
            'example_basic': 'docker ps',
            'example_adv': 'docker ps -a --format "table {{.Names}}\\t{{.Status}}\\t{{.Image}}"',
            'os_type': '通用', 'aliases': '容器列表,docker ps,容器',
            'tips': 'docker ps -q 只输出容器 ID，常用于脚本中配合其他命令。--filter 可按条件过滤。'
        },
        {
            'cmd_name': 'docker container prune',
            'name_cn': '清理停止的容器',
            'function_desc': '删除所有已停止的容器，释放磁盘空间和资源。',
            'syntax': 'docker container prune [-f]',
            'params_json': '[{"参数":"-f","说明":"强制删除，不提示确认","必填":"可选"},{"参数":"--filter","说明":"按条件过滤要清理的容器","必填":"可选"}]',
            'example_basic': 'docker container prune',
            'example_adv': 'docker container prune -f --filter "until=24h"',
            'os_type': '通用', 'aliases': '容器清理,prune,清理',
            'tips': 'docker system prune 会清理所有未使用的 Docker 对象（容器、镜像、网络、卷）。'
        },
        {
            'cmd_name': 'docker image prune',
            'name_cn': '清理未使用的镜像',
            'function_desc': '删除未被任何容器使用的镜像（悬空镜像和未被引用的镜像）。',
            'syntax': 'docker image prune [-a] [-f]',
            'params_json': '[{"参数":"-a","说明":"删除所有未使用的镜像（不只看悬空）","必填":"可选"},{"参数":"-f","说明":"强制删除","必填":"可选"}]',
            'example_basic': 'docker image prune',
            'example_adv': 'docker image prune -a -f --filter "until=24h"',
            'os_type': '通用', 'aliases': '镜像清理,prune,镜像',
            'tips': 'docker image prune -a 会删除所有未被容器引用的镜像，包括所有中间层。'
        },
        {
            'cmd_name': 'docker system df',
            'name_cn': '查看磁盘使用',
            'function_desc': '显示 Docker 占用的磁盘空间，包括镜像、容器、卷和构建缓存的大小。',
            'syntax': 'docker system df [-v]',
            'params_json': '[{"参数":"-v","说明":"显示详细信息（按镜像/容器列出）","必填":"可选"}]',
            'example_basic': 'docker system df',
            'example_adv': 'docker system df -v',
            'os_type': '通用', 'aliases': '磁盘使用,df,空间查看',
            'tips': '定期运行 docker system df 检查 Docker 磁盘占用。用 docker system prune 清理无用空间。'
        },
        {
            'cmd_name': 'docker stats',
            'name_cn': '容器资源统计',
            'function_desc': '实时显示运行中容器的 CPU、内存、网络和磁盘 I/O 使用情况。类似 Linux top。',
            'syntax': 'docker stats [容器名]',
            'params_json': '[{"参数":"--no-stream","说明":"仅显示当前快照，不持续刷新","必填":"可选"},{"参数":"--format","说明":"自定义输出格式","必填":"可选"}]',
            'example_basic': 'docker stats',
            'example_adv': 'docker stats --no-stream --format "table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}"',
            'os_type': '通用', 'aliases': '资源统计,docker stats,监控',
            'tips': 'docker stats --no-stream 输出当前快照后退出。常用于脚本采集容器指标。'
        },
        {
            'cmd_name': 'docker top',
            'name_cn': '查看容器进程',
            'function_desc': '显示指定容器内正在运行的进程列表，类似宿主机上的 ps 命令。',
            'syntax': 'docker top <容器名> [ps选项]',
            'params_json': '[{"参数":"容器名","说明":"容器名称或 ID","必填":"是"},{"参数":"ps选项","说明":"传递给 ps 命令的选项","必填":"可选"}]',
            'example_basic': 'docker top mycontainer',
            'example_adv': 'docker top mycontainer aux',
            'os_type': '通用', 'aliases': '进程查看,docker top,容器进程',
            'tips': 'docker top 在宿主机上运行，显示的是宿主机命名空间中的进程 ID。'
        },
        {
            'cmd_name': 'docker port',
            'name_cn': '查看端口映射',
            'function_desc': '列出指定容器的端口映射关系，或查询特定端口的映射地址。',
            'syntax': 'docker port <容器名> [容器端口]',
            'params_json': '[{"参数":"容器名","说明":"容器名称或 ID","必填":"是"},{"参数":"容器端口","说明":"查看特定端口的映射","必填":"可选"}]',
            'example_basic': 'docker port mycontainer',
            'example_adv': 'docker port mycontainer 80',
            'os_type': '通用', 'aliases': '端口映射,docker port,端口',
            'tips': '显示格式为 宿主机IP:宿主机端口 -> 容器端口。docker ps 也会显示端口信息。'
        },
        {
            'cmd_name': 'docker cp',
            'name_cn': '文件复制',
            'function_desc': '在容器和宿主机之间复制文件或目录。支持双向复制。',
            'syntax': 'docker cp <来源> <目标>',
            'params_json': '[{"参数":"来源","说明":"宿主机路径 或 容器名:容器路径","必填":"是"},{"参数":"目标","说明":"目标路径（格式同上）","必填":"是"}]',
            'example_basic': 'docker cp mycontainer:/app/logs ./logs',
            'example_adv': 'docker cp ./config.json mycontainer:/app/config/',
            'os_type': '通用', 'aliases': '文件复制,docker cp,复制',
            'tips': '复制目录时末尾不带斜杠的行为与 cp 命令一致。容器路径格式：容器名:路径。'
        },
        {
            'cmd_name': 'docker diff',
            'name_cn': '检查容器文件变更',
            'function_desc': '检查容器文件系统中与镜像相比发生变化的文件和目录（A=添加，C=更改，D=删除）。',
            'syntax': 'docker diff <容器名>',
            'params_json': '[{"参数":"容器名","说明":"容器名称或 ID","必填":"是"}]',
            'example_basic': 'docker diff mycontainer',
            'example_adv': 'docker diff mycontainer | grep "^A"',
            'os_type': '通用', 'aliases': '文件变更,docker diff,diff',
            'tips': 'docker diff 对调试容器中意外修改非常有用。前缀 C 表示修改，A 表示添加，D 表示删除。'
        },
        {
            'cmd_name': 'docker commit',
            'name_cn': '从容器创建镜像',
            'function_desc': '将容器的当前状态保存为一个新镜像。常用于对容器进行修改后制作快照。',
            'syntax': 'docker commit [选项] <容器名> <镜像名:标签>',
            'params_json': '[{"参数":"-a","说明":"作者信息","必填":"可选"},{"参数":"-m","说明":"提交信息","必填":"可选"},{"参数":"--change","说明":"在提交时应用 Dockerfile 指令","必填":"可选"}]',
            'example_basic': 'docker commit mycontainer myimage:v1',
            'example_adv': 'docker commit -m "added nginx" -a "admin" mycontainer myapp:v2',
            'os_type': '通用', 'aliases': '提交镜像,docker commit,快照',
            'tips': 'docker commit 更适合临时调试，生产环境推荐使用 Dockerfile 构建镜像。'
        },
        {
            'cmd_name': 'docker save',
            'name_cn': '导出镜像为文件',
            'function_desc': '将一个或多个 Docker 镜像保存为 tar 归档文件，方便迁移或备份。',
            'syntax': 'docker save [选项] <镜像名> -o <文件.tar>',
            'params_json': '[{"参数":"-o","说明":"输出文件路径","必填":"是"},{"参数":"镜像名","说明":"要导出的镜像名称","必填":"是"}]',
            'example_basic': 'docker save myimage:latest -o myimage.tar',
            'example_adv': 'docker save myapp:latest mysql:8.0 -o backup.tar',
            'os_type': '通用', 'aliases': '导出镜像,docker save,备份',
            'tips': 'docker save 保留镜像的所有层和历史。对方用 docker load 还原。压缩：gzip myimage.tar。'
        },
        {
            'cmd_name': 'docker load',
            'name_cn': '导入镜像文件',
            'function_desc': '从 tar 归档文件加载 Docker 镜像。与 docker save 配合使用。',
            'syntax': 'docker load -i <文件.tar>',
            'params_json': '[{"参数":"-i","说明":"输入文件路径","必填":"是"}]',
            'example_basic': 'docker load -i myimage.tar',
            'example_adv': 'zcat myimage.tar.gz | docker load',
            'os_type': '通用', 'aliases': '导入镜像,docker load,加载',
            'tips': 'docker load 会保留镜像名和标签。可用 docker image ls 确认导入成功。'
        },
        {
            'cmd_name': 'docker login',
            'name_cn': '登录仓库',
            'function_desc': '登录到 Docker 镜像仓库（如 Docker Hub 或私有仓库），认证后可以进行推送/拉取操作。',
            'syntax': 'docker login [仓库地址]',
            'params_json': '[{"参数":"仓库地址","说明":"镜像仓库 URL（默认 Docker Hub）","必填":"可选"},{"参数":"-u","说明":"用户名","必填":"可选"},{"参数":"-p","说明":"密码（不安全，建议交互）","必填":"可选"}]',
            'example_basic': 'docker login',
            'example_adv': 'docker login myregistry.example.com:5000',
            'os_type': '通用', 'aliases': '登录,docker login,仓库认证',
            'tips': '密码存在 ~/.docker/config.json 中，base64 编码但不加密。推荐凭据管理工具或 docker-credential-helper。'
        },
        {
            'cmd_name': 'docker tag',
            'name_cn': '标记镜像',
            'function_desc': '为本地镜像创建一个新标签（名称/版本），常用于为推送到仓库准备镜像标记。',
            'syntax': 'docker tag <源镜像>[:标签] <目标镜像>[:标签]',
            'params_json': '[{"参数":"源镜像","说明":"现有镜像名和标签","必填":"是"},{"参数":"目标镜像","说明":"新镜像名和标签","必填":"是"}]',
            'example_basic': 'docker tag myapp:latest myapp:v1.0',
            'example_adv': 'docker tag myapp:latest myregistry.io/myapp:prod',
            'os_type': '通用', 'aliases': '标记,docker tag,镜像标签',
            'tips': 'docker tag 不复制镜像数据，只是创建一个新引用。同一个镜像可以有多个标签。'
        },
        {
            'cmd_name': 'docker push',
            'name_cn': '推送镜像到仓库',
            'function_desc': '将本地镜像上传到远程镜像仓库。推前需先 docker login 并用 docker tag 标记。',
            'syntax': 'docker push <镜像名>:<标签>',
            'params_json': '[{"参数":"镜像名:标签","说明":"要推送的镜像完整名称","必填":"是"}]',
            'example_basic': 'docker push myrepo/myapp:latest',
            'example_adv': 'docker push myregistry.io/myapp:$(git rev-parse --short HEAD)',
            'os_type': '通用', 'aliases': '推送,docker push,上传',
            'tips': '推送前务必确认镜像已正确标记。推送大镜像时可用 --all-tags 推送所有标签。'
        },
        {
            'cmd_name': 'docker search',
            'name_cn': '搜索镜像',
            'function_desc': '从 Docker Hub 搜索镜像，按名称和描述匹配。',
            'syntax': 'docker search [选项] <关键词>',
            'params_json': '[{"参数":"--filter","说明":"过滤条件（stars=N, is-official=true）","必填":"可选"},{"参数":"--limit","说明":"最大结果显示数","必填":"可选"}]',
            'example_basic': 'docker search nginx',
            'example_adv': 'docker search --filter stars=1000 --filter is-official=true nginx',
            'os_type': '通用', 'aliases': '搜索,docker search,镜像查找',
            'tips': 'docker search 只搜索 Docker Hub。私有仓库需要额外配置。--limit 限制结果数量。'
        },
        {
            'cmd_name': 'docker info',
            'name_cn': 'Docker 系统信息',
            'function_desc': '显示 Docker 系统的详细信息，包括内核、存储驱动、镜像数、容器数等。',
            'syntax': 'docker info',
            'params_json': '[{"参数":"--format","说明":"自定义输出格式","必填":"可选"}]',
            'example_basic': 'docker info',
            'example_adv': 'docker info --format "{{.ServerVersion}}"',
            'os_type': '通用', 'aliases': '系统信息,docker info,信息',
            'tips': 'docker info 对排查 Docker 安装问题非常有用，可查看存储驱动、运行状态等。'
        },
        {
            'cmd_name': 'docker history',
            'name_cn': '查看镜像历史',
            'function_desc': '显示镜像的构建历史，包括每一层的大小、创建指令和创建者。',
            'syntax': 'docker history [选项] <镜像名>',
            'params_json': '[{"参数":"--no-trunc","说明":"不截断输出","必填":"可选"},{"参数":"-H","说明":"人类可读的大小","必填":"可选"}]',
            'example_basic': 'docker history nginx:latest',
            'example_adv': 'docker history --no-trunc myimage:latest',
            'os_type': '通用', 'aliases': '镜像历史,docker history,层',
            'tips': 'docker history 可帮助理解镜像构成和优化 Dockerfile。小层总数越少越好。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Docker: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Docker: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# MySQL 补充（+25条）
# ============================================================
def seed_mysql_supplement(db):
    cat_id = get_cat_id('数据库', 'MySQL')
    if not cat_id:
        print('[ERR] 未找到 MySQL 分类')
        return 0

    commands = [
        {
            'cmd_name': 'CREATE USER',
            'name_cn': '创建用户',
            'function_desc': '创建新的 MySQL 用户账户，可指定认证方式和密码。',
            'syntax': 'CREATE USER \'用户名\'@\'主机\' IDENTIFIED BY \'密码\';',
            'params_json': '[{"参数":"用户名","说明":"新用户的名称","必填":"是"},{"参数":"主机","说明":"允许登录的主机（% 表示任意）","必填":"是"},{"参数":"密码","说明":"用户密码","必填":"是"}]',
            'example_basic': "CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'password';",
            'example_adv': "CREATE USER 'appuser'@'%' IDENTIFIED WITH mysql_native_password BY 'Str0ng!Pa$$';",
            'os_type': '通用', 'aliases': '创建用户,CREATE USER,用户',
            'tips': 'MySQL 8.0+ 默认使用 caching_sha2_password 认证。主机 % 通配所有主机。'
        },
        {
            'cmd_name': 'DROP USER',
            'name_cn': '删除用户',
            'function_desc': '删除一个或多个 MySQL 用户账户。',
            'syntax': 'DROP USER \'用户名\'@\'主机\';',
            'params_json': '[{"参数":"用户名","说明":"要删除的用户名","必填":"是"},{"参数":"主机","说明":"用户的主机","必填":"是"}]',
            'example_basic': "DROP USER 'appuser'@'localhost';",
            'example_adv': "DROP USER IF EXISTS 'tempuser'@'%';",
            'os_type': '通用', 'aliases': '删除用户,DROP USER,用户',
            'tips': 'DROP USER 自动回收用户的所有权限。IF EXISTS 避免用户不存在时报错。'
        },
        {
            'cmd_name': 'ALTER USER',
            'name_cn': '修改用户',
            'function_desc': '修改 MySQL 用户账户属性，如密码、认证插件、资源限制等。',
            'syntax': "ALTER USER '用户名'@'主机' IDENTIFIED BY '新密码';",
            'params_json': '[{"参数":"用户名","说明":"要修改的用户名","必填":"是"},{"参数":"主机","说明":"用户主机","必填":"是"},{"参数":"新密码","说明":"新密码","必填":"可选"}]',
            'example_basic': "ALTER USER 'appuser'@'localhost' IDENTIFIED BY 'newpass';",
            'example_adv': "ALTER USER 'appuser'@'%' WITH MAX_QUERIES_PER_HOUR 1000;",
            'os_type': '通用', 'aliases': '修改用户,ALTER USER,用户',
            'tips': 'ALTER USER CURRENT_USER() IDENTIFIED BY ... 可修改当前用户密码。'
        },
        {
            'cmd_name': 'SHOW DATABASES',
            'name_cn': '查看所有数据库',
            'function_desc': '列出 MySQL 服务器上的所有数据库。',
            'syntax': 'SHOW DATABASES;',
            'params_json': '[]',
            'example_basic': 'SHOW DATABASES;',
            'example_adv': 'SHOW DATABASES LIKE \'test%\';',
            'os_type': '通用', 'aliases': '数据库列表,SHOW DATABASES',
            'tips': 'information_schema、mysql、performance_schema 是系统数据库。'
        },
        {
            'cmd_name': 'SHOW TABLES',
            'name_cn': '查看所有表',
            'function_desc': '显示当前数据库中的所有表。',
            'syntax': 'SHOW TABLES;',
            'params_json': '[]',
            'example_basic': 'USE mydb; SHOW TABLES;',
            'example_adv': 'SHOW TABLES FROM information_schema LIKE \'%stat%\';',
            'os_type': '通用', 'aliases': '表列表,SHOW TABLES',
            'tips': '先 USE database 切换到数据库，或使用 SHOW TABLES FROM database。'
        },
        {
            'cmd_name': 'DESC',
            'name_cn': '查看表结构',
            'function_desc': '显示表的结构，包括字段名、类型、是否为空、默认值等。简写为 DESCRIBE。',
            'syntax': 'DESC <表名>;',
            'params_json': '[{"参数":"表名","说明":"要查看的表名","必填":"是"}]',
            'example_basic': 'DESC users;',
            'example_adv': 'DESC information_schema.TABLES;',
            'os_type': '通用', 'aliases': '表结构,DESC,DESCRIBE',
            'tips': 'SHOW CREATE TABLE tablename 可以查看完整建表语句。'
        },
        {
            'cmd_name': 'EXPLAIN',
            'name_cn': '查询执行计划',
            'function_desc': '显示 MySQL 执行 SQL 查询的执行计划，帮助分析查询性能和索引使用情况。',
            'syntax': 'EXPLAIN <SELECT 语句>;',
            'params_json': '[{"参数":"SELECT 语句","说明":"要分析的查询","必填":"是"}]',
            'example_basic': "EXPLAIN SELECT * FROM users WHERE id = 1;",
            'example_adv': "EXPLAIN FORMAT=JSON SELECT u.name, o.total FROM users u JOIN orders o ON u.id=o.user_id;",
            'os_type': '通用', 'aliases': '执行计划,EXPLAIN,查询分析',
            'tips': '关注 type 列（ALL=全表扫描，ref/eq_ref=索引查找）、rows 列（扫描行数）和 Extra 列（Using filesort 等）。'
        },
        {
            'cmd_name': 'SHOW INDEX',
            'name_cn': '查看索引',
            'function_desc': '显示表的索引信息，包括索引名、字段、是否唯一等。',
            'syntax': 'SHOW INDEX FROM <表名>;',
            'params_json': '[{"参数":"表名","说明":"表名","必填":"是"}]',
            'example_basic': 'SHOW INDEX FROM users;',
            'example_adv': "SHOW INDEX FROM users WHERE Key_name = 'PRIMARY';",
            'os_type': '通用', 'aliases': '索引,SHOW INDEX',
            'tips': 'Cardinality 列显示索引的区分度，值越大索引效率越高。'
        },
        {
            'cmd_name': 'SHOW PROCESSLIST',
            'name_cn': '查看进程列表',
            'function_desc': '显示 MySQL 服务器当前的线程/连接状态，包括执行的 SQL、时间、状态等。用于排查慢查询和锁问题。',
            'syntax': 'SHOW FULL PROCESSLIST;',
            'params_json': '[]',
            'example_basic': 'SHOW PROCESSLIST;',
            'example_adv': 'SHOW FULL PROCESSLIST;',
            'os_type': '通用', 'aliases': '进程列表,SHOW PROCESSLIST,连接',
            'tips': 'FULL 参数显示完整的 SQL 语句。Info 列可帮助识别慢查询。'
        },
        {
            'cmd_name': 'KILL',
            'name_cn': '终止连接',
            'function_desc': '终止指定的 MySQL 连接/线程。常用于终止长时间运行的慢查询。',
            'syntax': 'KILL <连接ID>;',
            'params_json': '[{"参数":"连接ID","说明":"从 SHOW PROCESSLIST 获取的线程 ID","必填":"是"}]',
            'example_basic': 'KILL 12345;',
            'example_adv': 'SELECT CONCAT(\'KILL \', id, \';\') FROM information_schema.PROCESSLIST WHERE TIME > 300;',
            'os_type': '通用', 'aliases': '终止连接,KILL,杀进程',
            'tips': '需要 PROCESS 权限。KILL CONNECTION 和 KILL QUERY 的区别：QUERY 只终止当前查询。'
        },
        {
            'cmd_name': 'LOCK TABLES',
            'name_cn': '锁定表',
            'function_desc': '显式锁定表，控制并发访问。可指定读锁（共享）或写锁（独占）。',
            'syntax': 'LOCK TABLES <表名> READ|WRITE;',
            'params_json': '[{"参数":"表名","说明":"要锁定的表名","必填":"是"},{"参数":"READ","说明":"读锁（共享锁）","必填":"可选"},{"参数":"WRITE","说明":"写锁（独占锁）","必填":"可选"}]',
            'example_basic': 'LOCK TABLES users WRITE;',
            'example_adv': 'LOCK TABLES orders READ, order_items READ;',
            'os_type': '通用', 'aliases': '锁定表,LOCK TABLES,锁表',
            'tips': '锁定后必须用 UNLOCK TABLES 释放。锁定期间不能访问未锁定的表。'
        },
        {
            'cmd_name': 'UNLOCK TABLES',
            'name_cn': '解锁表',
            'function_desc': '释放当前会话持有的所有表锁。',
            'syntax': 'UNLOCK TABLES;',
            'params_json': '[]',
            'example_basic': 'UNLOCK TABLES;',
            'example_adv': '-- 事务中用 COMMIT 或 ROLLBACK 也会释放锁',
            'os_type': '通用', 'aliases': '解锁表,UNLOCK TABLES',
            'tips': 'UNLOCK TABLES 释放当前会话所有锁，不能只释放某一张表。'
        },
        {
            'cmd_name': 'START TRANSACTION',
            'name_cn': '开始事务',
            'function_desc': '开始一个新的事务，后续的 SQL 操作在事务中执行，可统一提交或回滚。',
            'syntax': 'START TRANSACTION;',
            'params_json': '[]',
            'example_basic': 'START TRANSACTION;',
            'example_adv': 'START TRANSACTION WITH CONSISTENT SNAPSHOT;',
            'os_type': '通用', 'aliases': '事务,START TRANSACTION,BEGIN',
            'tips': 'BEGIN 和 START TRANSACTION 基本等价。WITH CONSISTENT SNAPSHOT 在 InnoDB 中启动一致性读。'
        },
        {
            'cmd_name': 'COMMIT',
            'name_cn': '提交事务',
            'function_desc': '将当前事务中的所有更改持久化到数据库，并释放事务持有的锁。',
            'syntax': 'COMMIT;',
            'params_json': '[]',
            'example_basic': 'COMMIT;',
            'example_adv': 'COMMIT AND CHAIN;',
            'os_type': '通用', 'aliases': '提交,COMMIT,事务提交',
            'tips': 'COMMIT AND CHAIN 在提交后立即开始新事务。MySQL 默认 autocommit=1，每条语句自动提交。'
        },
        {
            'cmd_name': 'ROLLBACK',
            'name_cn': '回滚事务',
            'function_desc': '撤销当前事务中的所有更改，恢复到事务开始前的状态。',
            'syntax': 'ROLLBACK [TO SAVEPOINT 名称];',
            'params_json': '[{"参数":"TO SAVEPOINT","说明":"回滚到指定保存点","必填":"可选"}]',
            'example_basic': 'ROLLBACK;',
            'example_adv': 'ROLLBACK TO SAVEPOINT before_update;',
            'os_type': '通用', 'aliases': '回滚,ROLLBACK,事务撤销',
            'tips': 'ROLLBACK 不指定保存点会回滚整个事务。在 MyISAM 引擎中 ROLLBACK 无效。'
        },
        {
            'cmd_name': 'SAVEPOINT',
            'name_cn': '设置保存点',
            'function_desc': '在事务中设置一个保存点，允许回滚到该点而不影响之前的操作。',
            'syntax': 'SAVEPOINT <保存点名>;',
            'params_json': '[{"参数":"保存点名","说明":"保存点的名称","必填":"是"}]',
            'example_basic': 'SAVEPOINT before_update;',
            'example_adv': 'SAVEPOINT after_insert;',
            'os_type': '通用', 'aliases': '保存点,SAVEPOINT',
            'tips': 'RELEASE SAVEPOINT 删除保存点但不回滚。同一事务中的保存点不能重名。'
        },
        {
            'cmd_name': 'TRUNCATE TABLE',
            'name_cn': '清空表',
            'function_desc': '删除表中的所有数据并重置自增计数器，比 DELETE 更快且不能回滚（某些情况）。',
            'syntax': 'TRUNCATE TABLE <表名>;',
            'params_json': '[{"参数":"表名","说明":"要清空的表名","必填":"是"}]',
            'example_basic': 'TRUNCATE TABLE temp_logs;',
            'example_adv': 'TRUNCATE TABLE temp_logs; -- 重置 AUTO_INCREMENT',
            'os_type': '通用', 'aliases': '清空表,TRUNCATE TABLE,清空',
            'tips': 'TRUNCATE 是 DDL 操作，不能回滚（在事务中可能可回滚）。不触发 DELETE 触发器。'
        },
        {
            'cmd_name': 'REPLACE INTO',
            'name_cn': '替换插入',
            'function_desc': '如果插入数据的主键或唯一索引冲突，则先删除旧行再插入新行。否则正常插入。',
            'syntax': 'REPLACE INTO <表名> (列...) VALUES (值...);',
            'params_json': '[{"参数":"表名","说明":"目标表","必填":"是"},{"参数":"列","说明":"要插入的列","必填":"是"},{"参数":"值","说明":"对应的值","必填":"是"}]',
            'example_basic': "REPLACE INTO users (id, name) VALUES (1, 'Alice');",
            'example_adv': "REPLACE INTO users SET id=1, name='Alice', email='alice@test.com';",
            'os_type': '通用', 'aliases': '替换,REPLACE INTO',
            'tips': 'REPLACE 本质是 DELETE + INSERT，会影响自增计数器。INSERT ... ON DUPLICATE KEY UPDATE 是更好的替代。'
        },
        {
            'cmd_name': 'INSERT IGNORE',
            'name_cn': '忽略插入',
            'function_desc': '插入数据时忽略错误（如主键冲突），冲突的行不插入也不报错。',
            'syntax': 'INSERT IGNORE INTO <表名> (列...) VALUES (值...);',
            'params_json': '[{"参数":"表名","说明":"目标表","必填":"是"}]',
            'example_basic': "INSERT IGNORE INTO users (id, name) VALUES (1, 'Alice');",
            'example_adv': "INSERT IGNORE INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob');",
            'os_type': '通用', 'aliases': '忽略插入,INSERT IGNORE',
            'tips': 'INSERT IGNORE 会忽略所有警告和错误。Row count 显示实际插入的行数（不包括忽略的）。'
        },
        {
            'cmd_name': 'INSERT ... ON DUPLICATE KEY UPDATE',
            'name_cn': '插入或更新',
            'function_desc': '如果插入的行导致唯一键冲突，则执行 UPDATE 更新冲突行；否则正常 INSERT。俗称 UPSERT。',
            'syntax': "INSERT INTO <表名> (列...) VALUES (值...) ON DUPLICATE KEY UPDATE 列=值;",
            'params_json': '[{"参数":"表名","说明":"目标表","必填":"是"},{"参数":"列","说明":"要更新的列和值","必填":"是"}]',
            'example_basic': "INSERT INTO users (id, name) VALUES (1, 'Alice') ON DUPLICATE KEY UPDATE name='Alice';",
            'example_adv': "INSERT INTO stats (id, cnt) VALUES (1, 1) ON DUPLICATE KEY UPDATE cnt=cnt+1;",
            'os_type': '通用', 'aliases': '插入更新,UPSERT,ON DUPLICATE KEY',
            'tips': 'VALUES(col) 在 ON DUPLICATE KEY 中引用新值。ROW_COUNT() 可判断执行了 INSERT（1行）还是 UPDATE（2行）。'
        },
        {
            'cmd_name': 'CREATE VIEW',
            'name_cn': '创建视图',
            'function_desc': '创建一个虚拟表（视图），基于 SELECT 查询结果。视图不存储数据，是对查询的封装。',
            'syntax': 'CREATE VIEW <视图名> AS <SELECT 语句>;',
            'params_json': '[{"参数":"视图名","说明":"视图名称","必填":"是"},{"参数":"SELECT 语句","说明":"视图的查询定义","必填":"是"}]',
            'example_basic': "CREATE VIEW active_users AS SELECT * FROM users WHERE status=1;",
            'example_adv': "CREATE VIEW user_orders AS SELECT u.name, o.total FROM users u JOIN orders o ON u.id=o.user_id;",
            'os_type': '通用', 'aliases': '视图,CREATE VIEW',
            'tips': '视图可简化复杂查询、实现安全控制（只暴露部分列）。简单视图可更新，复杂视图只读。'
        },
        {
            'cmd_name': 'DROP VIEW',
            'name_cn': '删除视图',
            'function_desc': '删除一个或多个已存在的视图。',
            'syntax': 'DROP VIEW [IF EXISTS] <视图名>;',
            'params_json': '[{"参数":"IF EXISTS","说明":"视图不存在时不报错","必填":"可选"},{"参数":"视图名","说明":"要删除的视图名","必填":"是"}]',
            'example_basic': "DROP VIEW active_users;",
            'example_adv': "DROP VIEW IF EXISTS user_orders, user_stats;",
            'os_type': '通用', 'aliases': '删除视图,DROP VIEW',
            'tips': 'DROP VIEW 不影响基表数据。可一次删除多个视图，用逗号分隔。'
        },
        {
            'cmd_name': 'SHOW CREATE TABLE',
            'name_cn': '查看建表语句',
            'function_desc': '显示创建指定表的完整 CREATE TABLE 语句，包括所有列定义、索引和约束。',
            'syntax': 'SHOW CREATE TABLE <表名>;',
            'params_json': '[{"参数":"表名","说明":"表名","必填":"是"}]',
            'example_basic': 'SHOW CREATE TABLE users;',
            'example_adv': 'SHOW CREATE TABLE mysql.user\\G',
            'os_type': '通用', 'aliases': '建表语句,SHOW CREATE TABLE',
            'tips': '这是备份表结构的最佳方式。\\G 用垂直格式输出，列多时更易读。'
        },
        {
            'cmd_name': 'SHOW WARNINGS',
            'name_cn': '查看警告信息',
            'function_desc': '显示最近执行的语句产生的警告信息。',
            'syntax': 'SHOW WARNINGS;',
            'params_json': '[]',
            'example_basic': 'SHOW WARNINGS;',
            'example_adv': 'SHOW COUNT(*) WARNINGS;',
            'os_type': '通用', 'aliases': '警告,SHOW WARNINGS',
            'tips': '执行完语句后立即执行 SHOW WARNINGS 查看详情。SHOW ERRORS 只显示错误，不显示警告。'
        },
        {
            'cmd_name': 'GRANT',
            'name_cn': '授予权限',
            'function_desc': '授予用户对数据库对象的特定权限。',
            'syntax': "GRANT <权限> ON <数据库>.<表> TO '用户'@'主机';",
            'params_json': '[{"参数":"权限","说明":"如 ALL PRIVILEGES, SELECT, INSERT","必填":"是"},{"参数":"数据库.表","说明":"权限作用范围（*.* 表示所有）","必填":"是"},{"参数":"用户","说明":"目标用户","必填":"是"}]',
            'example_basic': "GRANT SELECT, INSERT ON mydb.* TO 'appuser'@'localhost';",
            'example_adv': "GRANT ALL PRIVILEGES ON mydb.* TO 'appuser'@'%' WITH GRANT OPTION;",
            'os_type': '通用', 'aliases': '授权,GRANT,权限授予',
            'tips': 'WITH GRANT OPTION 允许用户将自己的权限转授给其他用户。授权后通常要 FLUSH PRIVILEGES。'
        },
        {
            'cmd_name': 'FLUSH PRIVILEGES',
            'name_cn': '刷新权限',
            'function_desc': '重新加载权限表，使 GRANT、REVOKE、CREATE USER 等操作立即生效。',
            'syntax': 'FLUSH PRIVILEGES;',
            'params_json': '[]',
            'example_basic': 'FLUSH PRIVILEGES;',
            'example_adv': '-- 在使用 GRANT 后通常不需要，因为会自动生效',
            'os_type': '通用', 'aliases': '刷新权限,FLUSH PRIVILEGES',
            'tips': '直接使用 GRANT/REVOKE 后权限会自动加载。FLUSH PRIVILEGES 主要在用 INSERT/UPDATE/DELETE 直接操作 mysql.user 表后需要。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] MySQL: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] MySQL: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# Redis 补充（+30条）
# ============================================================
def seed_redis_supplement(db):
    cat_id = get_cat_id('数据库', 'Redis命令')
    if not cat_id:
        print('[ERR] 未找到 Redis命令 分类')
        return 0

    commands = [
        {
            'cmd_name': 'SET',
            'name_cn': '设置键值',
            'function_desc': '设置指定 key 的值为指定 string 类型 value。如果 key 已存在则覆盖。',
            'syntax': 'SET key value [NX|XX] [EX seconds|PX milliseconds]',
            'params_json': '[{"参数":"NX","说明":"仅在 key 不存在时设置","必填":"可选"},{"参数":"XX","说明":"仅在 key 已存在时设置","必填":"可选"},{"参数":"EX","说明":"过期时间（秒）","必填":"可选"},{"参数":"PX","说明":"过期时间（毫秒）","必填":"可选"}]',
            'example_basic': 'SET name "Alice"',
            'example_adv': 'SET session:123 "data" EX 3600 NX',
            'os_type': '通用', 'aliases': '设置,SET,赋值',
            'tips': 'SET 自带 NX/XX 选项可替代 SETNX/SETXX。EX 和 PX 同时指定时取精度更高的 PX。'
        },
        {
            'cmd_name': 'GET',
            'name_cn': '获取键值',
            'function_desc': '获取指定 key 的 string 值。如果 key 不存在返回 nil。',
            'syntax': 'GET key',
            'params_json': '[{"参数":"key","说明":"要获取的键名","必填":"是"}]',
            'example_basic': 'GET name',
            'example_adv': 'GET session:123',
            'os_type': '通用', 'aliases': '获取,GET,取值',
            'tips': 'MGET 可一次获取多个 key。类型错误时返回错误（非 string 类型请用相应类型命令）。'
        },
        {
            'cmd_name': 'APPEND',
            'name_cn': '追加字符串',
            'function_desc': '如果 key 已存在且是字符串，将 value 追加到原值末尾；否则创建新 key。',
            'syntax': 'APPEND key value',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"value","说明":"要追加的字符串","必填":"是"}]',
            'example_basic': 'APPEND name " World"',
            'example_adv': '-- 从 "Hello" 变为 "Hello World"',
            'os_type': '通用', 'aliases': '追加,APPEND,拼接',
            'tips': '返回追加后字符串的总长度。适合构建字符串或日志累积。'
        },
        {
            'cmd_name': 'STRLEN',
            'name_cn': '获取字符串长度',
            'function_desc': '获取指定 key 的字符串值的长度。key 不存在返回 0。',
            'syntax': 'STRLEN key',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"}]',
            'example_basic': 'STRLEN name',
            'example_adv': '-- 返回值是字符数（字节数，取决于编码）',
            'os_type': '通用', 'aliases': '字符串长度,STRLEN,长度',
            'tips': '对于中文等多字节字符，返回的是字节数而非字符数。'
        },
        {
            'cmd_name': 'INCR',
            'name_cn': '自增 1',
            'function_desc': '将 key 中存储的数字加 1。如果 key 不存在，先初始化为 0 再执行 INCR。',
            'syntax': 'INCR key',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"}]',
            'example_basic': 'INCR counter',
            'example_adv': '-- 配合 GET 实现原子计数',
            'os_type': '通用', 'aliases': '自增,INCR,计数',
            'tips': 'INCR 是原子操作，适合计数器、限流等场景。值范围限定在 64 位有符号整数内。'
        },
        {
            'cmd_name': 'DECR',
            'name_cn': '自减 1',
            'function_desc': '将 key 中存储的数字减 1。如果 key 不存在，先初始化为 0 再执行 DECR。',
            'syntax': 'DECR key',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"}]',
            'example_basic': 'DECR counter',
            'example_adv': '-- 与 INCR 配合实现库存管理',
            'os_type': '通用', 'aliases': '自减,DECR,递减',
            'tips': 'DECR 也是原子操作。值不能低于 64 位有符号整数最小值。'
        },
        {
            'cmd_name': 'INCRBY',
            'name_cn': '按步长自增',
            'function_desc': '将 key 中存储的数字增加指定的步长值。步长可以是负数（等效 DECRBY）。',
            'syntax': 'INCRBY key increment',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"increment","说明":"增加量（可负）","必填":"是"}]',
            'example_basic': 'INCRBY score 10',
            'example_adv': 'INCRBY score -5  -- 等同于 DECRBY',
            'os_type': '通用', 'aliases': '按步长自增,INCRBY',
            'tips': 'INCRBYFLOAT 支持浮点数。原子操作，适合排行榜分数更新。'
        },
        {
            'cmd_name': 'GETSET',
            'name_cn': '设置并返回旧值',
            'function_desc': '原子性地设置 key 的新值并返回原来的旧值。',
            'syntax': 'GETSET key value',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"value","说明":"新值","必填":"是"}]',
            'example_basic': 'GETSET counter "100"',
            'example_adv': '-- 适用于计数器重置场景，先获取旧值再设新值',
            'os_type': '通用', 'aliases': '设置并获取旧值,GETSET',
            'tips': 'key 不存在时返回 nil（新设值）。常用于原子性的计数器重置或状态切换。'
        },
        {
            'cmd_name': 'MSET',
            'name_cn': '批量设置',
            'function_desc': '原子性地同时设置多个 key-value 对。比多个 SET 命令网络开销更小。',
            'syntax': 'MSET key1 value1 key2 value2 ...',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"value","说明":"对应的值","必填":"是"}]',
            'example_basic': 'MSET name "Alice" age "30" city "NYC"',
            'example_adv': '-- 对应 MGET 批量获取',
            'os_type': '通用', 'aliases': '批量设置,MSET',
            'tips': 'MSET 是原子的，所有 key 一起设置或全部不设置。MSETNX 仅在所有 key 都不存在时才设置。'
        },
        {
            'cmd_name': 'MGET',
            'name_cn': '批量获取',
            'function_desc': '一次获取多个 key 的值。返回与 key 顺序对应的值列表，不存在的 key 返回 nil。',
            'syntax': 'MGET key1 key2 ...',
            'params_json': '[{"参数":"key","说明":"要获取的键名列表","必填":"是"}]',
            'example_basic': 'MGET name age city',
            'example_adv': '-- 减少网络往返，比多次 GET 更高效',
            'os_type': '通用', 'aliases': '批量获取,MGET',
            'tips': 'MGET 不是原子操作（Redis 6+ 可带原子选项）。适合缓存批量回填场景。'
        },
        {
            'cmd_name': 'SETEX',
            'name_cn': '设置并设置过期',
            'function_desc': '设置 key 的值为指定 string 并同时设置过期时间（秒）。原子操作，相当于 SET + EXPIRE。',
            'syntax': 'SETEX key seconds value',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"seconds","说明":"过期秒数","必填":"是"},{"参数":"value","说明":"值","必填":"是"}]',
            'example_basic': 'SETEX session:token 3600 "abc123"',
            'example_adv': '-- 相比 SET + EXPIRE 分开执行更安全（原子性）',
            'os_type': '通用', 'aliases': '设置过期,SETEX',
            'tips': 'SET 命令也支持 EX/PX 选项，已逐渐取代 SETEX。SETEX 是原子的。'
        },
        {
            'cmd_name': 'SETNX',
            'name_cn': '不存在时设置',
            'function_desc': '仅在 key 不存在时设置值。常用于分布式锁等场景。',
            'syntax': 'SETNX key value',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"},{"参数":"value","说明":"值","必填":"是"}]',
            'example_basic': 'SETNX lock:resource "1"',
            'example_adv': '-- 返回值 1 表示设置成功，0 表示 key 已存在',
            'os_type': '通用', 'aliases': '不存在设置,SETNX,锁',
            'tips': 'Redis 2.6.12+ 的 SET 命令支持 NX 选项，功能相同。SET key value NX EX 10 实现带过期的锁。'
        },
        {
            'cmd_name': 'TTL',
            'name_cn': '查看剩余过期时间',
            'function_desc': '返回 key 的剩余过期时间（秒）。-1 表示永不过期，-2 表示 key 不存在。',
            'syntax': 'TTL key',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"}]',
            'example_basic': 'TTL session:token',
            'example_adv': '-- 检查缓存是否即将过期',
            'os_type': '通用', 'aliases': '过期时间,TTL,剩余时间',
            'tips': 'PTTL 返回毫秒级精度。当 TTL 为 -1 时，可用 EXPIRE 设置过期时间。'
        },
        {
            'cmd_name': 'EXISTS',
            'name_cn': '检查键是否存在',
            'function_desc': '检查一个或多个 key 是否存在。返回存在的 key 数量。',
            'syntax': 'EXISTS key [key ...]',
            'params_json': '[{"参数":"key","说明":"要检查的键名","必填":"是"}]',
            'example_basic': 'EXISTS name',
            'example_adv': 'EXISTS name age city  -- 返回存在的数量',
            'os_type': '通用', 'aliases': '存在检查,EXISTS',
            'tips': '从 Redis 3.0.3 起支持多个 key。比 GET 更高效，因为不传输值。'
        },
        {
            'cmd_name': 'DEL',
            'name_cn': '删除键',
            'function_desc': '删除一个或多个 key。不存在的 key 被忽略。',
            'syntax': 'DEL key [key ...]',
            'params_json': '[{"参数":"key","说明":"要删除的键名","必填":"是"}]',
            'example_basic': 'DEL name',
            'example_adv': 'DEL name age city',
            'os_type': '通用', 'aliases': '删除,DEL,移除',
            'tips': 'DEL 返回被删除 key 的数量。删除大集合时可能阻塞 Redis，推荐用 UNLINK（异步删除）。'
        },
        {
            'cmd_name': 'TYPE',
            'name_cn': '查看值类型',
            'function_desc': '返回 key 中存储的值的类型：string, list, set, zset, hash, stream 等。',
            'syntax': 'TYPE key',
            'params_json': '[{"参数":"key","说明":"键名","必填":"是"}]',
            'example_basic': 'TYPE name',
            'example_adv': '-- 在调试时确认 key 的类型',
            'os_type': '通用', 'aliases': '类型,TYPE,值类型',
            'tips': 'key 不存在时返回 none。每个操作都应操作对应类型，否则报错。'
        },
        {
            'cmd_name': 'RENAME',
            'name_cn': '重命名键',
            'function_desc': '将 key 重命名为 newkey。如果 newkey 已存在则覆盖。',
            'syntax': 'RENAME key newkey',
            'params_json': '[{"参数":"key","说明":"原键名","必填":"是"},{"参数":"newkey","说明":"新键名","必填":"是"}]',
            'example_basic': 'RENAME old_name new_name',
            'example_adv': '-- 注意：如果 newkey 存在会被覆盖',
            'os_type': '通用', 'aliases': '重命名,RENAME',
            'tips': 'RENAMENX 在 newkey 不存在时才重命名。RENAME 是原子操作，大 key 可能阻塞。'
        },
        {
            'cmd_name': 'RPUSH',
            'name_cn': '列表右推入',
            'function_desc': '将一个或多个值插入到列表的尾部（右侧）。如果 key 不存在则创建空列表再插入。',
            'syntax': 'RPUSH key value [value ...]',
            'params_json': '[{"参数":"key","说明":"列表键名","必填":"是"},{"参数":"value","说明":"要插入的值","必填":"是"}]',
            'example_basic': 'RPUSH tasks "task1"',
            'example_adv': 'RPUSH tasks "task1" "task2" "task3"',
            'os_type': '通用', 'aliases': '列表推入,RPUSH,右推',
            'tips': 'LPUSH 插入到头部（左侧）。结合 LPOP/RPOP 实现队列或栈。'
        },
        {
            'cmd_name': 'LPOP',
            'name_cn': '列表左弹出',
            'function_desc': '移除并返回列表的第一个元素（左侧）。key 不存在或列表为空返回 nil。',
            'syntax': 'LPOP key [count]',
            'params_json': '[{"参数":"key","说明":"列表键名","必填":"是"},{"参数":"count","说明":"弹出元素数（3.2+）","必填":"可选"}]',
            'example_basic': 'LPOP tasks',
            'example_adv': 'LPOP tasks 10  -- 一次弹出10个',
            'os_type': '通用', 'aliases': '弹出,LPOP,左弹出',
            'tips': 'RPOP 从右侧弹出。BLPOP/BRPOP 是阻塞版本，适合消息队列。'
        },
        {
            'cmd_name': 'LLEN',
            'name_cn': '列表长度',
            'function_desc': '返回列表的长度。key 不存在时返回 0。',
            'syntax': 'LLEN key',
            'params_json': '[{"参数":"key","说明":"列表键名","必填":"是"}]',
            'example_basic': 'LLEN tasks',
            'example_adv': '-- 查看队列积压情况',
            'os_type': '通用', 'aliases': '列表长度,LLEN,队列长度',
            'tips': '时间复杂度 O(1)，内部维护了列表长度计数器。'
        },
        {
            'cmd_name': 'LINDEX',
            'name_cn': '按索引获取列表元素',
            'function_desc': '返回列表中指定索引的元素。索引从 0 开始，负数表示从尾部开始。',
            'syntax': 'LINDEX key index',
            'params_json': '[{"参数":"key","说明":"列表键名","必填":"是"},{"参数":"index","说明":"索引（可负）","必填":"是"}]',
            'example_basic': 'LINDEX tasks 0',
            'example_adv': 'LINDEX tasks -1  -- 最后一个元素',
            'os_type': '通用', 'aliases': '索引获取,LINDEX',
            'tips': '时间复杂度 O(N)，N 为索引到端点的距离。大量索引操作建议用 LRANGE。'
        },
        {
            'cmd_name': 'LRANGE',
            'name_cn': '获取列表范围',
            'function_desc': '返回列表中指定范围内的元素。start 和 stop 索引从 0 开始，-1 表示最后一个元素。',
            'syntax': 'LRANGE key start stop',
            'params_json': '[{"参数":"key","说明":"列表键名","必填":"是"},{"参数":"start","说明":"起始索引","必填":"是"},{"参数":"stop","说明":"结束索引","必填":"是"}]',
            'example_basic': 'LRANGE tasks 0 -1',
            'example_adv': 'LRANGE tasks 0 9  -- 前10个',
            'os_type': '通用', 'aliases': '范围获取,LRANGE,列表范围',
            'tips': 'LRANGE key 0 -1 获取整个列表。大列表上使用需注意性能。'
        },
        {
            'cmd_name': 'SADD',
            'name_cn': '集合添加元素',
            'function_desc': '向集合中添加一个或多个成员。重复成员会被忽略。',
            'syntax': 'SADD key member [member ...]',
            'params_json': '[{"参数":"key","说明":"集合键名","必填":"是"},{"参数":"member","说明":"要添加的成员","必填":"是"}]',
            'example_basic': 'SADD users "alice"',
            'example_adv': 'SADD tags "redis" "database" "nosql"',
            'os_type': '通用', 'aliases': '集合添加,SADD',
            'tips': '集合无序且唯一。SMEMBERS 获取所有成员。'
        },
        {
            'cmd_name': 'SMEMBERS',
            'name_cn': '获取所有集合成员',
            'function_desc': '返回集合中的所有成员。无序输出。',
            'syntax': 'SMEMBERS key',
            'params_json': '[{"参数":"key","说明":"集合键名","必填":"是"}]',
            'example_basic': 'SMEMBERS users',
            'example_adv': '-- 注意：大集合会返回大量数据',
            'os_type': '通用', 'aliases': '集合成员,SMEMBERS',
            'tips': '大集合慎用 SMEMBERS（会阻塞）。SSCAN 提供游标式迭代。'
        },
        {
            'cmd_name': 'SINTER',
            'name_cn': '集合交集',
            'function_desc': '返回所有给定集合的交集（共同的成员）。',
            'syntax': 'SINTER key [key ...]',
            'params_json': '[{"参数":"key","说明":"多个集合键名","必填":"是"}]',
            'example_basic': 'SINTER set1 set2',
            'example_adv': '-- 适用于找共同关注、共同好友等',
            'os_type': '通用', 'aliases': '交集,SINTER',
            'tips': 'SINTERSTORE 将结果保存到新集合。SUNION 并集，SDIFF 差集。'
        },
        {
            'cmd_name': 'SUNION',
            'name_cn': '集合并集',
            'function_desc': '返回所有给定集合的并集（所有不重复的成员）。',
            'syntax': 'SUNION key [key ...]',
            'params_json': '[{"参数":"key","说明":"多个集合键名","必填":"是"}]',
            'example_basic': 'SUNION set1 set2',
            'example_adv': 'SUNIONSTORE dest set1 set2',
            'os_type': '通用', 'aliases': '并集,SUNION',
            'tips': 'SUNIONSTORE 可将结果保存到新集合。结果中不含重复元素。'
        },
        {
            'cmd_name': 'ZADD',
            'name_cn': '有序集合添加',
            'function_desc': '向有序集合中添加一个或多个成员，每个成员关联一个分数。',
            'syntax': 'ZADD key [NX|XX] [CH] [INCR] score member [score member ...]',
            'params_json': '[{"参数":"NX","说明":"仅添加新元素","必填":"可选"},{"参数":"XX","说明":"仅更新已有元素","必填":"可选"},{"参数":"CH","说明":"返回变更数而非新增数","必填":"可选"},{"参数":"INCR","说明":"将分数增加指定值","必填":"可选"}]',
            'example_basic': 'ZADD leaderboard 100 "player1"',
            'example_adv': 'ZADD leaderboard 100 "player1" 200 "player2" 150 "player3"',
            'os_type': '通用', 'aliases': '有序集合,ZADD,排行榜',
            'tips': '分数相同时按字典序排列。ZINCRBY 可递增某个成员的分数。'
        },
        {
            'cmd_name': 'ZRANGE',
            'name_cn': '有序集合范围查询',
            'function_desc': '按索引范围返回有序集合中的成员，默认按分数升序排列。支持 WITHSCORES。',
            'syntax': 'ZRANGE key start stop [WITHSCORES]',
            'params_json': '[{"参数":"start","说明":"起始索引（0开始）","必填":"是"},{"参数":"stop","说明":"结束索引（-1为全部）","必填":"是"},{"参数":"WITHSCORES","说明":"同时返回分数","必填":"可选"}]',
            'example_basic': 'ZRANGE leaderboard 0 2 WITHSCORES',
            'example_adv': 'ZRANGE leaderboard 0 -1  -- 全部',
            'os_type': '通用', 'aliases': '范围查询,ZRANGE,排序',
            'tips': 'ZREVRANGE 降序排列。ZRANGEBYSCORE 按分数范围查。'
        },
        {
            'cmd_name': 'ZREVRANGE',
            'name_cn': '有序集合降序范围',
            'function_desc': '按索引范围返回有序集合中的成员，按分数降序排列（从高到低）。',
            'syntax': 'ZREVRANGE key start stop [WITHSCORES]',
            'params_json': '[{"参数":"start","说明":"起始索引","必填":"是"},{"参数":"stop","说明":"结束索引","必填":"是"}]',
            'example_basic': 'ZREVRANGE leaderboard 0 2 WITHSCORES',
            'example_adv': '-- 获取排行榜前三名',
            'os_type': '通用', 'aliases': '降序范围,ZREVRANGE,排行榜',
            'tips': 'ZREVRANGE key 0 0 获得最高分成员。ZREVRANK 获取成员的降序排名。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] Redis: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] Redis: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# PowerShell 补充（+25条）
# ============================================================
def seed_powershell_supplement(db):
    cat_id = get_cat_id('命令行工具', 'PowerShell')
    if not cat_id:
        print('[ERR] 未找到 PowerShell 分类')
        return 0

    commands = [
        {
            'cmd_name': 'Get-Command',
            'name_cn': '获取命令信息',
            'function_desc': '获取所有 PowerShell 命令的信息，包括 cmdlet、函数、别名、外部程序等。',
            'syntax': 'Get-Command [-Name <名称>] [-CommandType <类型>]',
            'params_json': '[{"参数":"-Name","说明":"命令名称或通配符","必填":"可选"},{"参数":"-CommandType","说明":"命令类型（Cmdlet, Function, Alias等）","必填":"可选"}]',
            'example_basic': 'Get-Command',
            'example_adv': 'Get-Command -CommandType Cmdlet | Where-Object { $_.Name -like "*Service*" }',
            'os_type': 'Windows', 'aliases': '命令,Get-Command,gcm',
            'tips': 'Get-Command 是 PowerShell 自发现的核心 cmdlet。别名 gcm。Get-Command -Name *process* 模糊搜索。'
        },
        {
            'cmd_name': 'Get-Member',
            'name_cn': '获取对象成员',
            'function_desc': '获取对象的属性和方法信息。了解任何对象的结构和可用成员。',
            'syntax': '<对象> | Get-Member [-MemberType <类型>]',
            'params_json': '[{"参数":"-MemberType","说明":"成员类型（Property, Method, Event等）","必填":"可选"},{"参数":"-Name","说明":"按名称筛选","必填":"可选"}]',
            'example_basic': 'Get-Process | Get-Member',
            'example_adv': 'Get-Process | Get-Member -MemberType Property -Name "*ID*"',
            'os_type': 'Windows', 'aliases': '成员,Get-Member,gm',
            'tips': '别名 gm。管道对象到 Get-Member 查看其类型和可用成员，是 PowerShell 调试利器。'
        },
        {
            'cmd_name': 'Select-Object',
            'name_cn': '选择对象属性',
            'function_desc': '选择对象的指定属性、前 N 个对象或跳过前 N 个。类似 SQL 的 SELECT。',
            'syntax': '<对象> | Select-Object [-Property <属性>] [-First <数量>] [-Last <数量>]',
            'params_json': '[{"参数":"-Property","说明":"要选择的属性名","必填":"可选"},{"参数":"-First","说明":"选择前 N 个对象","必填":"可选"},{"参数":"-Last","说明":"选择后 N 个对象","必填":"可选"},{"参数":"-Unique","说明":"去重","必填":"可选"}]',
            'example_basic': 'Get-Process | Select-Object Name, CPU, WorkingSet',
            'example_adv': 'Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, CPU',
            'os_type': 'Windows', 'aliases': '选择,Select-Object,select',
            'tips': '别名 select。Select-Object -ExpandProperty 提取单个属性的值数组。'
        },
        {
            'cmd_name': 'Sort-Object',
            'name_cn': '排序对象',
            'function_desc': '按一个或多个属性对对象进行排序，支持升序和降序。',
            'syntax': '<对象> | Sort-Object [-Property <属性>] [-Descending] [-Unique]',
            'params_json': '[{"参数":"-Property","说明":"排序的属性","必填":"可选"},{"参数":"-Descending","说明":"降序排序","必填":"可选"},{"参数":"-Unique","说明":"去重","必填":"可选"}]',
            'example_basic': 'Get-Process | Sort-Object CPU -Descending',
            'example_adv': 'Get-Service | Sort-Object Status, DisplayName',
            'os_type': 'Windows', 'aliases': '排序,Sort-Object,sort',
            'tips': '别名 sort。多属性排序用逗号分隔，第一个属性为主排序键。'
        },
        {
            'cmd_name': 'Group-Object',
            'name_cn': '分组对象',
            'function_desc': '按指定属性对对象进行分组，类似 SQL 的 GROUP BY。',
            'syntax': '<对象> | Group-Object [-Property <属性>] [-NoElement]',
            'params_json': '[{"参数":"-Property","说明":"分组依据的属性","必填":"是"},{"参数":"-NoElement","说明":"不显示组内成员","必填":"可选"}]',
            'example_basic': 'Get-Service | Group-Object Status',
            'example_adv': 'Get-Process | Group-Object ProcessName | Sort-Object Count -Descending | Select -First 5',
            'os_type': 'Windows', 'aliases': '分组,Group-Object,group',
            'tips': '别名 group。结果包含 Count, Name, Group 属性，Group 包含组内对象。'
        },
        {
            'cmd_name': 'Measure-Object',
            'name_cn': '统计对象',
            'function_desc': '计算对象的统计信息，如计数、总和、平均值、最大最小值。',
            'syntax': '<对象> | Measure-Object [-Property <属性>] [-Sum] [-Average] [-Maximum] [-Minimum]',
            'params_json': '[{"参数":"-Property","说明":"要统计的属性","必填":"可选"},{"参数":"-Sum","说明":"计算总和","必填":"可选"},{"参数":"-Average","说明":"计算平均值","必填":"可选"},{"参数":"-Maximum","说明":"计算最大值","必填":"可选"},{"参数":"-Minimum","说明":"计算最小值","必填":"可选"}]',
            'example_basic': 'Get-Process | Measure-Object',
            'example_adv': 'Get-Process | Measure-Object WorkingSet -Sum -Average -Maximum -Minimum',
            'os_type': 'Windows', 'aliases': '统计,Measure-Object,measure',
            'tips': '别名 measure。默认只计数。统计数值属性时需指定 -Property。'
        },
        {
            'cmd_name': 'Compare-Object',
            'name_cn': '比较对象',
            'function_desc': '比较两个对象集合，找出差异。显示哪些对象只存在于引用集合，哪些在差异集合。',
            'syntax': 'Compare-Object <引用集合> <差异集合> [-Property <属性>]',
            'params_json': '[{"参数":"-ReferenceObject","说明":"引用集合","必填":"是"},{"参数":"-DifferenceObject","说明":"差异集合","必填":"是"},{"参数":"-Property","说明":"比较的属性","必填":"可选"},{"参数":"-IncludeEqual","说明":"包含相同的对象","必填":"可选"}]',
            'example_basic': 'Compare-Object (Get-ChildItem dir1) (Get-ChildItem dir2)',
            'example_adv': 'Compare-Object (Get-Process) (Get-Process -ComputerName remote) -Property Name, CPU',
            'os_type': 'Windows', 'aliases': '比较,Compare-Object,diff,compare',
            'tips': '结果中 <= 表示仅在引用集合，=> 表示仅在差异集合。别名 diff 和 compare。'
        },
        {
            'cmd_name': 'Out-File',
            'name_cn': '输出到文件',
            'function_desc': '将输出发送到文件，可指定编码、宽度等。类似 > 重定向但更强大。',
            'syntax': '<对象> | Out-File [-FilePath] <路径> [-Encoding <编码>] [-Append]',
            'params_json': '[{"参数":"-FilePath","说明":"文件路径","必填":"是"},{"参数":"-Encoding","说明":"编码（UTF8, ASCII, Unicode等）","必填":"可选"},{"参数":"-Append","说明":"追加到文件末尾","必填":"可选"},{"参数":"-NoClobber","说明":"不覆盖已有文件","必填":"可选"}]',
            'example_basic': 'Get-Process | Out-File processes.txt',
            'example_adv': 'Get-Process | Out-File -FilePath report.csv -Encoding UTF8',
            'os_type': 'Windows', 'aliases': '输出文件,Out-File,重定向',
            'tips': 'Out-File -Append 追加内容。Set-Content 直接写入文本（不格式化对象）。'
        },
        {
            'cmd_name': 'Export-Csv',
            'name_cn': '导出 CSV',
            'function_desc': '将对象导出为逗号分隔值（CSV）文件，可用于 Excel 或其他程序。',
            'syntax': '<对象> | Export-Csv [-Path] <路径> [-NoTypeInformation] [-Encoding <编码>]',
            'params_json': '[{"参数":"-Path","说明":"CSV 文件路径","必填":"是"},{"参数":"-NoTypeInformation","说明":"不输出类型信息头","必填":"可选"},{"参数":"-Delimiter","说明":"分隔符（默认逗号）","必填":"可选"}]',
            'example_basic': 'Get-Process | Export-Csv processes.csv -NoTypeInformation',
            'example_adv': 'Get-Service | Export-Csv services.csv -Delimiter ";" -Encoding UTF8',
            'os_type': 'Windows', 'aliases': '导出CSV,Export-Csv,export',
            'tips': 'ConvertTo-Csv 输出字符串而非文件。导入时用 Import-Csv。'
        },
        {
            'cmd_name': 'Import-Csv',
            'name_cn': '导入 CSV',
            'function_desc': '从 CSV 文件创建表格对象，每列作为属性。',
            'syntax': 'Import-Csv [-Path] <路径> [-Delimiter <分隔符>] [-Encoding <编码>]',
            'params_json': '[{"参数":"-Path","说明":"CSV 文件路径","必填":"是"},{"参数":"-Delimiter","说明":"分隔符","必填":"可选"}]',
            'example_basic': 'Import-Csv users.csv',
            'example_adv': 'Import-Csv data.csv -Delimiter ";" | Where-Object { $_.Age -gt 18 }',
            'os_type': 'Windows', 'aliases': '导入CSV,Import-Csv,import',
            'tips': 'Import-Csv 返回自定义对象（PSCustomObject），可按列名直接访问属性。'
        },
        {
            'cmd_name': 'ConvertTo-Json',
            'name_cn': '转换为 JSON',
            'function_desc': '将 PowerShell 对象转换为 JSON 格式字符串。',
            'syntax': '<对象> | ConvertTo-Json [-Depth <深度>] [-Compress]',
            'params_json': '[{"参数":"-Depth","说明":"嵌套深度（默认 2）","必填":"可选"},{"参数":"-Compress","说明":"压缩输出（去掉空白）","必填":"可选"}]',
            'example_basic': 'Get-Process -Id 1 | ConvertTo-Json',
            'example_adv': 'Get-Service | Select-Object Name, Status | ConvertTo-Json -Depth 1 | Out-File services.json',
            'os_type': 'Windows', 'aliases': '转JSON,ConvertTo-Json',
            'tips': '默认深度 2，复杂对象需增加 -Depth。Compress 生成一行紧凑 JSON。'
        },
        {
            'cmd_name': 'ConvertFrom-Json',
            'name_cn': '从 JSON 转换',
            'function_desc': '将 JSON 格式字符串转换为 PowerShell 对象。',
            'syntax': '<JSON字符串> | ConvertFrom-Json',
            'params_json': '[]',
            'example_basic': '\'{"name":"Alice","age":30}\' | ConvertFrom-Json',
            'example_adv': 'Get-Content config.json | ConvertFrom-Json',
            'os_type': 'Windows', 'aliases': '解析JSON,ConvertFrom-Json',
            'tips': '常与 Get-Content 配合读取 JSON 配置文件。结果直接以点号访问属性。'
        },
        {
            'cmd_name': 'Invoke-Command',
            'name_cn': '远程执行命令',
            'function_desc': '在本地或远程计算机上执行命令。是 PowerShell 远程管理核心。',
            'syntax': 'Invoke-Command -ComputerName <计算机名> -ScriptBlock { <命令> }',
            'params_json': '[{"参数":"-ComputerName","说明":"远程计算机名或IP","必填":"可选"},{"参数":"-ScriptBlock","说明":"要执行的脚本块","必填":"是"},{"参数":"-Credential","说明":"凭据","必填":"可选"},{"参数":"-Session","说明":"在指定 PSSession 中运行","必填":"可选"}]',
            'example_basic': 'Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Service }',
            'example_adv': 'Invoke-Command -ComputerName Server01,Server02 -ScriptBlock { Get-Process | Select Name, CPU } -Credential $cred',
            'os_type': 'Windows', 'aliases': '远程执行,Invoke-Command,icm',
            'tips': '别名 icm。需要 WinRM 开启并配置。多台计算机和 -ErrorAction SilentlyContinue 配合批量管理。'
        },
        {
            'cmd_name': 'Enter-PSSession',
            'name_cn': '进入远程会话',
            'function_desc': '启动与远程计算机的交互式 PowerShell 会话。输入的命令在远程计算机上执行。',
            'syntax': 'Enter-PSSession -ComputerName <计算机名>',
            'params_json': '[{"参数":"-ComputerName","说明":"远程计算机名","必填":"是"},{"参数":"-Credential","说明":"凭据","必填":"可选"},{"参数":"-Session","说明":"使用现有 PSSession","必填":"可选"}]',
            'example_basic': 'Enter-PSSession Server01',
            'example_adv': 'Enter-PSSession -ComputerName 192.168.1.100 -Credential (Get-Credential)',
            'os_type': 'Windows', 'aliases': '远程会话,Enter-PSSession,etsn',
            'tips': '提示符变为 [计算机名] PS> 表示在远程会话中。Exit-PSSession 退出远程会话。'
        },
        {
            'cmd_name': 'New-Object',
            'name_cn': '创建对象',
            'function_desc': '创建 .NET 或 COM 对象的新实例。可灵活创建 PowerShell 中未预定义的对象。',
            'syntax': 'New-Object [-TypeName] <类型名> [-ArgumentList <参数>]',
            'params_json': '[{"参数":"-TypeName","说明":"类型名称（如 System.Collections.ArrayList）","必填":"是"},{"参数":"-ArgumentList","说明":"构造函数参数","必填":"可选"},{"参数":"-ComObject","说明":"创建 COM 对象","必填":"可选"}]',
            'example_basic': 'New-Object -TypeName PSObject -Property @{Name="Alice"; Age=30}',
            'example_adv': '$list = New-Object -TypeName System.Collections.ArrayList; $list.Add("item")',
            'os_type': 'Windows', 'aliases': '创建对象,New-Object,new',
            'tips': '[PSCustomObject]@{...} 是 PS3.0+ 更简洁的方式。New-Object -ComObject 操作 COM 组件。'
        },
        {
            'cmd_name': 'Get-Service',
            'name_cn': '获取服务',
            'function_desc': '获取本地或远程计算机上的 Windows 服务信息。',
            'syntax': 'Get-Service [-Name <名称>] [-DisplayName <显示名>] [-ComputerName <计算机>]',
            'params_json': '[{"参数":"-Name","说明":"服务名称（支持通配符）","必填":"可选"},{"参数":"-DisplayName","说明":"显示名称","必填":"可选"},{"参数":"-ComputerName","说明":"远程计算机","必填":"可选"}]',
            'example_basic': 'Get-Service',
            'example_adv': 'Get-Service -Name *sql* | Where-Object Status -eq Running',
            'os_type': 'Windows', 'aliases': '服务,Get-Service,gsv',
            'tips': '别名 gsv。结合 Start-Service, Stop-Service, Restart-Service 管理服务。'
        },
        {
            'cmd_name': 'Start-Service',
            'name_cn': '启动服务',
            'function_desc': '启动一个或多个 Windows 服务。',
            'syntax': 'Start-Service [-Name] <服务名>',
            'params_json': '[{"参数":"-Name","说明":"服务名称","必填":"是"},{"参数":"-DisplayName","说明":"显示名称","必填":"可选"},{"参数":"-InputObject","说明":"从管道传入服务对象","必填":"可选"}]',
            'example_basic': 'Start-Service -Name Spooler',
            'example_adv': 'Get-Service -Name *sql* -ComputerName Server01 | Start-Service',
            'os_type': 'Windows', 'aliases': '启动服务,Start-Service,sasv',
            'tips': '需要管理员权限。可用 Get-Service 过滤后管道给 Start-Service。'
        },
        {
            'cmd_name': 'Get-Process',
            'name_cn': '获取进程',
            'function_desc': '获取本地或远程计算机上运行的进程信息。',
            'syntax': 'Get-Process [-Name <进程名>] [-Id <PID>] [-ComputerName <计算机>]',
            'params_json': '[{"参数":"-Name","说明":"进程名（支持通配符）","必填":"可选"},{"参数":"-Id","说明":"进程ID","必填":"可选"},{"参数":"-ComputerName","说明":"远程计算机","必填":"可选"}]',
            'example_basic': 'Get-Process',
            'example_adv': 'Get-Process -Name *chrome* | Sort-Object WorkingSet64 -Descending | Select Name, WorkingSet64',
            'os_type': 'Windows', 'aliases': '进程,Get-Process,ps,gps',
            'tips': '别名 ps 或 gps。查看 CPU、内存使用情况做性能分析。'
        },
        {
            'cmd_name': 'Stop-Process',
            'name_cn': '终止进程',
            'function_desc': '终止一个或多个正在运行的进程。',
            'syntax': 'Stop-Process [-Name] <进程名> | [-Id] <PID> [-Force]',
            'params_json': '[{"参数":"-Name","说明":"进程名","必填":"可选"},{"参数":"-Id","说明":"进程ID","必填":"可选"},{"参数":"-Force","说明":"强制终止","必填":"可选"}]',
            'example_basic': 'Stop-Process -Name notepad',
            'example_adv': 'Get-Process -Name *chrome* | Where-Object WorkingSet64 -gt 500MB | Stop-Process -Force',
            'os_type': 'Windows', 'aliases': '终止进程,Stop-Process,kill,spps',
            'tips': '别名 kill。强制终止（-Force）可能导致未保存数据丢失。'
        },
        {
            'cmd_name': 'Test-Connection',
            'name_cn': '网络连通测试',
            'function_desc': '发送 ICMP 回显请求（ping）到一台或多台计算机，返回结果对象。比传统 ping 更强大。',
            'syntax': 'Test-Connection [-ComputerName] <目标> [-Count <次数>] [-Quiet]',
            'params_json': '[{"参数":"-ComputerName","说明":"目标计算机名或IP","必填":"是"},{"参数":"-Count","说明":"发送次数","必填":"可选"},{"参数":"-Quiet","说明":"只返回布尔结果","必填":"可选"},{"参数":"-BufferSize","说明":"缓冲大小","必填":"可选"}]',
            'example_basic': 'Test-Connection google.com',
            'example_adv': 'Test-Connection -ComputerName Server01,Server02 -Count 2 -Quiet',
            'os_type': 'Windows', 'aliases': 'Ping,Test-Connection,网络测试',
            'tips': '-Quiet 返回 True/False 适合脚本条件判断。Test-NetConnection 是更全面的网络诊断工具。'
        },
        {
            'cmd_name': 'Test-Path',
            'name_cn': '测试路径',
            'function_desc': '测试路径是否存在，判断是文件还是目录。',
            'syntax': 'Test-Path [-Path] <路径> [-PathType <容器|叶子>]',
            'params_json': '[{"参数":"-Path","说明":"要测试的路径","必填":"是"},{"参数":"-PathType","说明":"Container（目录）或 Leaf（文件）","必填":"可选"}]',
            'example_basic': 'Test-Path C:\\Windows\\notepad.exe',
            'example_adv': 'if (Test-Path $profile) { notepad $profile } else { New-Item -Path $profile -Type File -Force }',
            'os_type': 'Windows', 'aliases': '测试路径,Test-Path,路径检查',
            'tips': '返回布尔值。可用 -IsValid 检查路径格式是否正确（不检查存在性）。'
        },
        {
            'cmd_name': 'New-Item',
            'name_cn': '创建新项',
            'function_desc': '创建文件、目录、注册表项等新项。是 PowerShell 中创建文件/目录的标准方式。',
            'syntax': 'New-Item [-Path] <路径> [-ItemType <类型>] [-Force]',
            'params_json': '[{"参数":"-Path","说明":"新项路径","必填":"是"},{"参数":"-ItemType","说明":"类型（File, Directory, SymbolicLink等）","必填":"可选"},{"参数":"-Force","说明":"强制创建（覆盖）","必填":"可选"}]',
            'example_basic': 'New-Item -Path C:\\Temp -ItemType Directory',
            'example_adv': 'New-Item -Path C:\\Temp\\config.json -ItemType File -Force',
            'os_type': 'Windows', 'aliases': '创建,New-Item,ni,md',
            'tips': '别名 ni（文件）和 md（目录）。创建符号链接：New-Item -ItemType SymbolicLink -Path link -Target target。'
        },
        {
            'cmd_name': 'Remove-Item',
            'name_cn': '删除项',
            'function_desc': '删除文件、目录、注册表项等。支持递归删除。',
            'syntax': 'Remove-Item [-Path] <路径> [-Recurse] [-Force]',
            'params_json': '[{"参数":"-Path","说明":"要删除的路径","必填":"是"},{"参数":"-Recurse","说明":"递归删除子项","必填":"可选"},{"参数":"-Force","说明":"强制删除（隐藏/只读）","必填":"可选"}]',
            'example_basic': 'Remove-Item C:\\Temp\\test.txt',
            'example_adv': 'Remove-Item C:\\Temp -Recurse -Force',
            'os_type': 'Windows', 'aliases': '删除,Remove-Item,rm,del,ri',
            'tips': '别名 rm, del, ri。删除目录需 -Recurse。使用 -WhatIf 预览删除操作。'
        },
        {
            'cmd_name': 'Get-Content',
            'name_cn': '读取文件内容',
            'function_desc': '获取文件内容，以行为单位返回字符串数组。支持读取大文件的开头/结尾。',
            'syntax': 'Get-Content [-Path] <文件路径> [-Tail <行数>] [-Encoding <编码>]',
            'params_json': '[{"参数":"-Path","说明":"文件路径","必填":"是"},{"参数":"-Tail","说明":"读取末尾 N 行（类似 tail）","必填":"可选"},{"参数":"-Encoding","说明":"编码","必填":"可选"},{"参数":"-Wait","说明":"等待追加内容（类似 tail -f）","必填":"可选"}]',
            'example_basic': 'Get-Content C:\\Temp\\log.txt',
            'example_adv': 'Get-Content C:\\Temp\\log.txt -Tail 100 -Wait',
            'os_type': 'Windows', 'aliases': '读取文件,Get-Content,gc,cat,type',
            'tips': '别名 gc, cat, type。大文件建议用 -Tail 或 -ReadCount 提高性能。'
        },
        {
            'cmd_name': 'Get-ChildItem',
            'name_cn': '获取子项',
            'function_desc': '获取指定位置中的文件和目录。类似 CMD 的 dir 或 Linux 的 ls。',
            'syntax': 'Get-ChildItem [[-Path] <路径>] [-Recurse] [-Filter <过滤器>] [-File] [-Directory]',
            'params_json': '[{"参数":"-Path","说明":"路径","必填":"可选"},{"参数":"-Recurse","说明":"递归子目录","必填":"可选"},{"参数":"-Filter","说明":"通配符过滤器","必填":"可选"},{"参数":"-File","说明":"仅文件","必填":"可选"},{"参数":"-Directory","说明":"仅目录","必填":"可选"}]',
            'example_basic': 'Get-ChildItem C:\\Windows',
            'example_adv': 'Get-ChildItem -Path C:\\Projects -Recurse -Filter "*.py" | Select FullName, Length',
            'os_type': 'Windows', 'aliases': '列表,Get-ChildItem,ls,dir,gci',
            'tips': '别名 ls, dir, gci。-Filter 比 Where-Object 过滤高效得多。'
        },
        {
            'cmd_name': 'Set-Location',
            'name_cn': '切换目录',
            'function_desc': '将当前工作目录切换到指定路径。类似 CMD 的 cd 命令。',
            'syntax': 'Set-Location [[-Path] <路径>] | [[-StackName] <栈名>]',
            'params_json': '[{"参数":"-Path","说明":"目标路径","必填":"是"},{"参数":"-PassThru","说明":"返回新路径对象","必填":"可选"}]',
            'example_basic': 'Set-Location C:\\Windows',
            'example_adv': 'Set-Location -Path C:\\Projects\\MyApp -PassThru',
            'os_type': 'Windows', 'aliases': '切换目录,Set-Location,cd,sl',
            'tips': '别名 cd, sl。Set-Location - 切换到上一个目录。Push-Location 和 Pop-Location 管理目录栈。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] PowerShell: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] PowerShell: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# SQLite 补充（+15条）
# ============================================================
def seed_sqlite_supplement(db):
    cat_id = get_cat_id('数据库', 'SQLite')
    if not cat_id:
        print('[ERR] 未找到 SQLite 分类')
        return 0

    commands = [
        {
            'cmd_name': '.backup',
            'name_cn': '备份数据库',
            'function_desc': '创建当前数据库的备份文件。在备份时确保数据库一致性。',
            'syntax': '.backup [备份文件名]',
            'params_json': '[{"参数":"备份文件名","说明":"备份文件路径（默认 main.db.backup）","必填":"可选"}]',
            'example_basic': '.backup',
            'example_adv': '.backup /tmp/mydb_backup.db',
            'os_type': '通用', 'aliases': '备份,.backup,导出',
            'tips': '.backup 在备份期间会锁定数据库，确保一致性。恢复用 .restore 命令。'
        },
        {
            'cmd_name': '.databases',
            'name_cn': '列出数据库',
            'function_desc': '列出当前连接中所有已打开的数据库，包括主数据库和附加的数据库。',
            'syntax': '.databases',
            'params_json': '[]',
            'example_basic': '.databases',
            'example_adv': '-- seq, name, file 三列信息',
            'os_type': '通用', 'aliases': '数据库列表,.databases',
            'tips': '默认有 main 和 temp 数据库。ATTACH DATABASE 可附加更多。'
        },
        {
            'cmd_name': '.dump',
            'name_cn': '导出数据库',
            'function_desc': '将数据库导出为 SQL 文本（包含完整建表和插入语句），可用于备份或迁移。',
            'syntax': '.dump [表名]',
            'params_json': '[{"参数":"表名","说明":"仅导出指定表（可选）","必填":"可选"}]',
            'example_basic': '.dump',
            'example_adv': '.dump users > users_backup.sql',
            'os_type': '通用', 'aliases': '导出,.dump,SQL导出',
            'tips': '.dump 的输出可直接通过管道导入另一个 sqlite3 进程。.output 可重定向到文件。'
        },
        {
            'cmd_name': '.echo',
            'name_cn': '回显开关',
            'function_desc': '打开或关闭命令回显。打开时显示执行的 SQL 命令。',
            'syntax': '.echo on|off',
            'params_json': '[{"参数":"on","说明":"开启回显","必填":"是"},{"参数":"off","说明":"关闭回显","必填":"是"}]',
            'example_basic': '.echo on',
            'example_adv': '.echo on  -- 调试 SQL 脚本时有用',
            'os_type': '通用', 'aliases': '回显,.echo,调试',
            'tips': '在运行 SQL 脚本文件时特别有用 (.read script.sql)。'
        },
        {
            'cmd_name': '.headers',
            'name_cn': '显示列头',
            'function_desc': '在查询结果中显示或隐藏列标题。',
            'syntax': '.headers on|off',
            'params_json': '[{"参数":"on","说明":"显示列头","必填":"是"},{"参数":"off","说明":"隐藏列头","必填":"是"}]',
            'example_basic': '.headers on',
            'example_adv': '.headers on  -- 查询结果更易读',
            'os_type': '通用', 'aliases': '列头,.headers,标题',
            'tips': '通常与 .mode column 配合使用，获得表格样式的输出。'
        },
        {
            'cmd_name': '.help',
            'name_cn': '帮助信息',
            'function_desc': '显示所有点命令的帮助信息。',
            'syntax': '.help [命令]',
            'params_json': '[{"参数":"命令","说明":"查看指定命令的帮助（可选）","必填":"可选"}]',
            'example_basic': '.help',
            'example_adv': '.help .mode',
            'os_type': '通用', 'aliases': '帮助,.help',
            'tips': '.help .mode 查看 .mode 命令的详细说明。'
        },
        {
            'cmd_name': '.import',
            'name_cn': '导入数据',
            'function_desc': '从 CSV 或其他分隔符文件中导入数据到指定表。',
            'syntax': '.import <文件> <表名>',
            'params_json': '[{"参数":"文件","说明":"要导入的数据文件","必填":"是"},{"参数":"表名","说明":"目标表名","必填":"是"}]',
            'example_basic': '.import data.csv users',
            'example_adv': '.separator "," \\n.import data.csv users',
            'os_type': '通用', 'aliases': '导入,.import,CSV导入',
            'tips': '导入前先设置 .separator 匹配文件格式。表不存在时会自动创建（类型全是 TEXT）。'
        },
        {
            'cmd_name': '.indexes',
            'name_cn': '列出索引',
            'function_desc': '显示当前数据库中所有索引，或指定表的索引。',
            'syntax': '.indexes [表名]',
            'params_json': '[{"参数":"表名","说明":"列出指定表的索引（可选）","必填":"可选"}]',
            'example_basic': '.indexes',
            'example_adv': '.indexes users',
            'os_type': '通用', 'aliases': '索引,.indexes',
            'tips': 'SQLite 会自动为主键和 UNIQUE 约束创建索引。'
        },
        {
            'cmd_name': '.mode',
            'name_cn': '设置输出模式',
            'function_desc': '设置查询结果的输出格式，支持 column, csv, json, markdown, table 等多种模式。',
            'syntax': '.mode <模式>',
            'params_json': '[{"参数":"模式","说明":"column|csv|json|markdown|table|list|html|insert|line|tabs|quote","必填":"是"}]',
            'example_basic': '.mode column',
            'example_adv': '.mode markdown  -- 生成 Markdown 表格格式',
            'os_type': '通用', 'aliases': '输出模式,.mode,格式',
            'tips': '.mode column 配合 .headers on 显示表格。.mode json 输出 JSON 格式。'
        },
        {
            'cmd_name': '.nullvalue',
            'name_cn': 'NULL 显示值',
            'function_desc': '设置 NULL 值在输出中显示的字符串。默认是空字符串。',
            'syntax': '.nullvalue <字符串>',
            'params_json': '[{"参数":"字符串","说明":"用于表示 NULL 的文本","必填":"是"}]',
            'example_basic': '.nullvalue NULL',
            'example_adv': '.nullvalue "<null>"',
            'os_type': '通用', 'aliases': 'NULL值,.nullvalue',
            'tips': '设置后 NULL 值不会与空字符串混淆。'
        },
        {
            'cmd_name': '.open',
            'name_cn': '打开数据库',
            'function_desc': '关闭当前数据库并打开新的数据库文件。',
            'syntax': '.open <数据库文件>',
            'params_json': '[{"参数":"数据库文件","说明":"要打开的 .db 文件路径","必填":"是"}]',
            'example_basic': '.open mydb.db',
            'example_adv': '.open :memory:  -- 创建内存数据库',
            'os_type': '通用', 'aliases': '打开,.open,切换数据库',
            'tips': '.open :memory: 创建临时内存数据库。:memory: 数据库在连接关闭后消失。'
        },
        {
            'cmd_name': '.output',
            'name_cn': '输出重定向',
            'function_desc': '将查询结果写入文件而不是输出到控制台。',
            'syntax': '.output <文件名>',
            'params_json': '[{"参数":"文件名","说明":"输出文件路径","必填":"是"}]',
            'example_basic': '.output result.txt',
            'example_adv': '.output stdout  -- 恢复输出到控制台',
            'os_type': '通用', 'aliases': '输出重定向,.output',
            'tips': '.output stdout 恢复控制台输出。常用模式：.output file.csv 配合 .mode csv 导出 CSV。'
        },
        {
            'cmd_name': '.schema',
            'name_cn': '查看表结构',
            'function_desc': '显示数据库的 CREATE 语句，包括所有表和视图。',
            'syntax': '.schema [表名]',
            'params_json': '[{"参数":"表名","说明":"仅显示指定表的结构（可选）","必填":"可选"}]',
            'example_basic': '.schema',
            'example_adv': '.schema users',
            'os_type': '通用', 'aliases': '结构,.schema,schema',
            'tips': '.schema 显示完整的 CREATE TABLE/VIEW/INDEX 语句。'
        },
        {
            'cmd_name': '.tables',
            'name_cn': '列出表',
            'function_desc': '列出当前数据库中所有表和视图。',
            'syntax': '.tables [模式]',
            'params_json': '[{"参数":"模式","说明":"通配符过滤（可选）","必填":"可选"}]',
            'example_basic': '.tables',
            'example_adv': '.tables users*',
            'os_type': '通用', 'aliases': '表列表,.tables',
            'tips': '.tables 效果等同于 SELECT name FROM sqlite_master WHERE type=\'table\';'
        },
        {
            'cmd_name': '.timer',
            'name_cn': '计时开关',
            'function_desc': '控制 SQL 语句执行时间的显示。打开后每个查询显示 CPU 时间和实际时间。',
            'syntax': '.timer on|off',
            'params_json': '[{"参数":"on","说明":"开启计时","必填":"是"},{"参数":"off","说明":"关闭计时","必填":"是"}]',
            'example_basic': '.timer on',
            'example_adv': '.timer on  -- 分析查询性能',
            'os_type': '通用', 'aliases': '计时,.timer,性能',
            'tips': '单位是秒（CPU time），显示 real time（实际耗时）和 user time（CPU 耗时）。'
        },
    ]

    count = 0
    for cmd in commands:
        try:
            db.add_command(category_id=cat_id, **cmd)
            count += 1
            print(f'  [OK] SQLite: {cmd["cmd_name"]}')
        except Exception as e:
            print(f'  [ERR] SQLite: {cmd["cmd_name"]} - {e}')
    return count


# ============================================================
# 主函数
# ============================================================
def main():
    print('开始补充命令行种子数据...')
    print()

    total = 0

    print('--- Git 补充 ---')
    total += seed_git_supplement(db)
    print()

    print('--- Linux 终端补充 ---')
    total += seed_linux_supplement(db)
    total += seed_linux_user_supplement(db)
    total += seed_linux_hw_supplement(db)
    print()

    print('--- CMD Windows 补充 ---')
    total += seed_cmd_supplement(db)
    total += seed_cmd2_supplement(db)
    print()

    print('--- Docker 补充 ---')
    total += seed_docker_supplement(db)
    print()

    print('--- MySQL 补充 ---')
    total += seed_mysql_supplement(db)
    print()

    print('--- Redis 补充 ---')
    total += seed_redis_supplement(db)
    print()

    print('--- PowerShell 补充 ---')
    total += seed_powershell_supplement(db)
    print()

    print('--- SQLite 补充 ---')
    total += seed_sqlite_supplement(db)
    print()

    # 获取总命令数
    from database.db_manager import DBManager
    db2 = DBManager()
    total_cmds = db2.conn.execute("SELECT COUNT(*) FROM commands").fetchone()[0]

    print(f'[OK] 本次补充完成！共插入 {total} 条命令')
    print(f'[OK] 数据库中当前总命令数：{total_cmds}')


if __name__ == '__main__':
    main()
