#!/usr/bin/env python3
"""
种子数据脚本：向 SQLite 数据库插入大量命令行命令数据
用法：python3 seed_commands.py

数据库路径：~/.code-quickref/data.db
分类结构参见 schema.py 中的 CATEGORY_SEED
"""

import sys
import os

# 添加项目根目录到 path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from database.db_manager import DBManager


def get_yes_no(prompt, default='y'):
    """简单确认"""
    choices = 'Y/n' if default == 'y' else 'y/N'
    resp = input(f'{prompt} [{choices}] ').strip().lower()
    if not resp:
        return default == 'y'
    return resp in ('y', 'yes')


def seed_git(db):
    """插入 Git 命令数据"""
    cat_id = db.get_cat_id_by_name('命令行工具', 'Git')
    if not cat_id:
        print('[错误] 未找到 Git 分类，请先初始化数据库')
        return

    commands = [
        {
            'cmd_name': 'git init',
            'name_cn': '创建新仓库',
            'function_desc': '在当前目录初始化一个新的 Git 仓库，生成 .git 隐藏文件夹。这是使用 Git 管理项目的第一步。',
            'syntax': 'git init [目录名]',
            'params_json': '[{"参数":"目录名","说明":"指定仓库目录（可选），不填则在当前目录创建","必填":"可选"}]',
            'example_basic': 'git init',
            'example_adv': 'git init my-project && cd my-project',
            'os_type': '通用',
            'aliases': '初始化,仓库创建,git初始化',
            'tips': 'git init 后要先用 git add 添加文件，然后 git commit 才能创建第一个版本。不要在一个已有 .git 的仓库里再执行 git init。',
        },
        {
            'cmd_name': 'git clone',
            'name_cn': '克隆远程仓库',
            'function_desc': '将远程仓库完整复制到本地，包括所有历史提交记录和分支信息。',
            'syntax': 'git clone <仓库地址> [本地目录名]',
            'params_json': '[{"参数":"仓库地址","说明":"远程仓库 URL（HTTPS 或 SSH）","必填":"是"},{"参数":"本地目录名","说明":"克隆到本地的目录名称（可选）","必填":"可选"}]',
            'example_basic': 'git clone https://github.com/user/repo.git',
            'example_adv': 'git clone --depth=1 https://github.com/user/repo.git --branch main',
            'os_type': '通用',
            'aliases': '克隆,下载仓库,clone',
            'tips': '--depth=1 可以只克隆最新版本（浅克隆），适合大型仓库以节省时间和空间。SSH 方式需要先配置 SSH Key。',
        },
        {
            'cmd_name': 'git add',
            'name_cn': '添加文件到暂存区',
            'function_desc': '将工作区的文件更改添加到暂存区（Staging Area），准备下一次提交。',
            'syntax': 'git add <文件路径>',
            'params_json': '[{"参数":"文件路径","说明":"要添加的文件或目录路径，可用 . 代表所有更改","必填":"是"}]',
            'example_basic': 'git add index.html',
            'example_adv': 'git add -A && git status',
            'os_type': '通用',
            'aliases': '暂存,添加,stage',
            'tips': 'git add . 添加当前目录所有更改；git add -A 添加整个工作区的更改（包括删除）。建议用 git status 先检查再 add。',
        },
        {
            'cmd_name': 'git commit',
            'name_cn': '提交暂存区更改',
            'function_desc': '将暂存区的内容提交为一个新版本，生成唯一的 commit hash。每次提交都应是一个完整的、有意义的变更。',
            'syntax': 'git commit -m "提交信息"',
            'params_json': '[{"参数":"-m","说明":"提交信息，简要描述本次更改内容","必填":"是"},{"参数":"--amend","说明":"修改上一次提交（替代上次提交）","必填":"可选"}]',
            'example_basic': 'git commit -m "修复登录页面样式问题"',
            'example_adv': 'git commit -m "feat: 新增用户注册功能" -m "实现了邮箱验证和密码加密"',
            'os_type': '通用',
            'aliases': '提交,版本,commit',
            'tips': '提交信息建议遵循约定式提交规范：feat/fix/docs/refactor 等前缀。不要提交未完成的工作。',
        },
        {
            'cmd_name': 'git push',
            'name_cn': '推送到远程仓库',
            'function_desc': '将本地分支的提交推送到远程仓库，同步本地代码到服务器。',
            'syntax': 'git push [远程仓库名] [分支名]',
            'params_json': '[{"参数":"远程仓库名","说明":"远程仓库名称，默认为 origin","必填":"可选"},{"参数":"分支名","说明":"要推送的分支，默认为当前分支","必填":"可选"}]',
            'example_basic': 'git push origin main',
            'example_adv': 'git push --force-with-lease origin feature-branch',
            'os_type': '通用',
            'aliases': '推送,上传,push',
            'tips': '推送前先 git pull 拉取最新代码避免冲突。尽量避免使用 --force，如确需使用推荐 --force-with-lease（更安全）。',
        },
        {
            'cmd_name': 'git pull',
            'name_cn': '拉取远程更新并合并',
            'function_desc': '从远程仓库获取最新更改并自动合并到当前分支，相当于 git fetch + git merge。',
            'syntax': 'git pull [远程仓库名] [分支名]',
            'params_json': '[{"参数":"远程仓库名","说明":"远程仓库名称，默认为 origin","必填":"可选"},{"参数":"分支名","说明":"要拉取的分支，默认为当前分支","必填":"可选"}]',
            'example_basic': 'git pull origin main',
            'example_adv': 'git pull --rebase origin main',
            'os_type': '通用',
            'aliases': '拉取,更新,pull',
            'tips': '推荐使用 git pull --rebase 保持提交历史线性整洁。如果有未提交的更改，先 git stash 暂存再 pull。',
        },
        {
            'cmd_name': 'git status',
            'name_cn': '查看工作区状态',
            'function_desc': '显示工作区和暂存区的状态：哪些文件被修改、已暂存、未跟踪等。是最常用的 Git 检查命令。',
            'syntax': 'git status',
            'params_json': '[{"参数":"-s","说明":"简洁模式（short），每行显示一个文件状态","必填":"可选"},{"参数":"-b","说明":"同时显示分支信息","必填":"可选"}]',
            'example_basic': 'git status',
            'example_adv': 'git status -sb',
            'os_type': '通用',
            'aliases': '状态,检查,status',
            'tips': '每次 commit 前都应该 git status 确认更改范围。红色 = 未暂存，绿色 = 已暂存。',
        },
        {
            'cmd_name': 'git log',
            'name_cn': '查看提交历史',
            'function_desc': '显示仓库的提交历史记录，包含 commit hash、作者、日期和提交信息。',
            'syntax': 'git log [选项]',
            'params_json': '[{"参数":"--oneline","说明":"单行简洁显示每个提交","必填":"可选"},{"参数":"--graph","说明":"以图形化方式显示分支历史","必填":"可选"},{"参数":"--author","说明":"按作者筛选提交","必填":"可选"}]',
            'example_basic': 'git log --oneline --graph',
            'example_adv': 'git log --oneline --graph --all --decorate',
            'os_type': '通用',
            'aliases': '日志,历史,log',
            'tips': 'git log --oneline --graph --all 可以清晰看到所有分支的分叉历史。按 q 退出查看。',
        },
        {
            'cmd_name': 'git branch',
            'name_cn': '管理分支',
            'function_desc': '列出、创建或删除分支。分支是 Git 的核心功能，让开发者可以并行开发不同功能。',
            'syntax': 'git branch [分支名]',
            'params_json': '[{"参数":"分支名","说明":"创建新分支（可选，不填则列出所有分支）","必填":"可选"},{"参数":"-d","说明":"删除已合并的分支","必填":"可选"},{"参数":"-D","说明":"强制删除分支（即使未合并）","必填":"可选"}]',
            'example_basic': 'git branch feature-login',
            'example_adv': 'git branch -d old-feature && git branch -a',
            'os_type': '通用',
            'aliases': '分支,branch',
            'tips': '当前分支前有 * 标记。git branch -a 查看所有分支（包括远程）。删除分支前确认没有未合并的更改。',
        },
        {
            'cmd_name': 'git checkout',
            'name_cn': '切换分支/恢复文件',
            'function_desc': '切换到指定分支，或恢复工作区的文件到最近一次提交的状态。',
            'syntax': 'git checkout <分支名/文件名>',
            'params_json': '[{"参数":"分支名","说明":"要切换到的目标分支","必填":"是"},{"参数":"-b","说明":"创建并切换到新分支","必填":"可选"}]',
            'example_basic': 'git checkout main',
            'example_adv': 'git checkout -b feature/new-dashboard',
            'os_type': '通用',
            'aliases': '切换,恢复,checkout',
            'tips': 'git checkout -b 新分支名 = 创建并切换。新版 Git 推荐使用 git switch 和 git restore 替代 checkout。',
        },
        {
            'cmd_name': 'git merge',
            'name_cn': '合并分支',
            'function_desc': '将指定分支的更改合并到当前分支。是整合不同分支开发成果的主要方式。',
            'syntax': 'git merge <分支名>',
            'params_json': '[{"参数":"分支名","说明":"要合并进来的源分支","必填":"是"},{"参数":"--no-ff","说明":"禁用快进合并，保留分支历史","必填":"可选"}]',
            'example_basic': 'git merge feature-login',
            'example_adv': 'git merge --no-ff feature-login -m "merge: 合并登录功能"',
            'os_type': '通用',
            'aliases': '合并,merge',
            'tips': '合并前确保当前分支是目标分支（如 main）。遇到冲突时，手动解决后 git add + git commit 完成合并。',
        },
        {
            'cmd_name': 'git diff',
            'name_cn': '查看差异',
            'function_desc': '显示工作区、暂存区或提交之间的文件内容差异。用于审查代码更改。',
            'syntax': 'git diff [文件路径]',
            'params_json': '[{"参数":"文件路径","说明":"指定文件查看该文件的差异","必填":"可选"},{"参数":"--cached","说明":"查看已暂存与上次提交的差异","必填":"可选"},{"参数":"HEAD","说明":"查看工作区与最新提交的差异","必填":"可选"}]',
            'example_basic': 'git diff',
            'example_adv': 'git diff --cached | less',
            'os_type': '通用',
            'aliases': '差异,diff,对比',
            'tips': '不加参数默认显示未暂存的更改。git diff --cached 显示已暂存但未提交的更改。',
        },
        {
            'cmd_name': 'git stash',
            'name_cn': '暂存工作区',
            'function_desc': '将当前工作区的临时更改保存到堆栈中，恢复工作区到干净状态，以便切换分支或做其他操作。',
            'syntax': 'git stash [选项]',
            'params_json': '[{"参数":"save","说明":"保存暂存并添加描述信息","必填":"可选"},{"参数":"pop","说明":"恢复最近一次暂存并删除该记录","必填":"可选"},{"参数":"list","说明":"列出所有暂存记录","必填":"可选"}]',
            'example_basic': 'git stash',
            'example_adv': 'git stash save "wip: 登录页面功能开发中" && git stash list',
            'os_type': '通用',
            'aliases': '暂存,stash,临时保存',
            'tips': 'git stash pop 恢复并删除记录；git stash apply 恢复但保留记录。git stash list 查看所有暂存。',
        },
        {
            'cmd_name': 'git reset',
            'name_cn': '撤销提交',
            'function_desc': '撤销提交或取消暂存文件。可以回退到之前的提交状态，有软、混合、硬三种模式。',
            'syntax': 'git reset [模式] <目标提交>',
            'params_json': '[{"参数":"--soft","说明":"仅撤销提交，保留更改在暂存区","必填":"可选"},{"参数":"--mixed","说明":"撤销提交并取消暂存（默认模式）","必填":"可选"},{"参数":"--hard","说明":"完全撤销，丢弃所有更改（危险）","必填":"可选"}]',
            'example_basic': 'git reset HEAD~1',
            'example_adv': 'git reset --soft HEAD~3',
            'os_type': '通用',
            'aliases': '重置,撤销,reset',
            'tips': '--hard 会彻底丢弃更改，无法恢复！推荐先用 --soft 或 --mixed。如果已经 push 到远程，用 git revert 而不是 reset。',
        },
        {
            'cmd_name': 'git remote',
            'name_cn': '管理远程仓库',
            'function_desc': '查看和管理与本地仓库关联的远程仓库地址。支持添加、删除、重命名远程仓库。',
            'syntax': 'git remote [命令] [参数]',
            'params_json': '[{"参数":"-v","说明":"列出所有远程仓库及其 URL","必填":"可选"},{"参数":"add","说明":"添加新的远程仓库","必填":"可选"},{"参数":"remove","说明":"删除远程仓库","必填":"可选"}]',
            'example_basic': 'git remote -v',
            'example_adv': 'git remote add upstream https://github.com/original/repo.git',
            'os_type': '通用',
            'aliases': '远程,remote',
            'tips': 'origin 是克隆时自动添加的远程仓库别名。upstream 常用于 Fork 的原始仓库。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 Git 命令')


def seed_linux(db):
    """插入 Linux 终端命令数据"""
    cat_id = db.get_cat_id_by_name('命令行工具', 'Linux终端')
    if not cat_id:
        print('[错误] 未找到 Linux终端 分类')
        return

    commands = [
        {
            'cmd_name': 'ls',
            'name_cn': '列出目录内容',
            'function_desc': '列出当前或指定目录下的文件和子目录，是 Linux 中最常用的命令之一。',
            'syntax': 'ls [选项] [目录路径]',
            'params_json': '[{"参数":"-l","说明":"详细列表模式（权限、大小、修改时间）","必填":"可选"},{"参数":"-a","说明":"显示所有文件（包括以 . 开头的隐藏文件）","必填":"可选"},{"参数":"-h","说明":"人类可读的文件大小格式（与 -l 配合使用）","必填":"可选"}]',
            'example_basic': 'ls -la',
            'example_adv': 'ls -lAh --sort=time /var/log',
            'os_type': 'Linux/macOS',
            'aliases': '列出,目录列表,list',
            'tips': 'll 是 ls -la 的别名（部分发行版）。ls -R 递归列出子目录所有文件。',
        },
        {
            'cmd_name': 'cd',
            'name_cn': '切换目录',
            'function_desc': '切换到指定目录，是 Linux 终端中最常用的导航命令。',
            'syntax': 'cd [目录路径]',
            'params_json': '[{"参数":"目录路径","说明":"目标目录路径（绝对或相对路径）","必填":"可选"}]',
            'example_basic': 'cd /home/user/projects',
            'example_adv': 'cd ~/projects && pwd',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '切换目录,进入目录,change directory',
            'tips': 'cd ~ 回到用户主目录；cd - 回到上一个工作目录；cd .. 返回上级目录；cd . 当前目录。',
        },
        {
            'cmd_name': 'pwd',
            'name_cn': '显示当前目录路径',
            'function_desc': '打印当前工作目录的绝对路径，用于确认当前位置。',
            'syntax': 'pwd',
            'params_json': '[]',
            'example_basic': 'pwd',
            'example_adv': 'pwd -P',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '当前目录,print working directory',
            'tips': 'pwd -P 显示物理路径（忽略符号链接）。',
        },
        {
            'cmd_name': 'mkdir',
            'name_cn': '创建目录',
            'function_desc': '创建一个或多个新目录，是组织文件系统的基本命令。',
            'syntax': 'mkdir [选项] <目录名>',
            'params_json': '[{"参数":"-p","说明":"递归创建多级目录（父目录不存在时自动创建）","必填":"可选"},{"参数":"-v","说明":"显示创建过程详情","必填":"可选"}]',
            'example_basic': 'mkdir projects',
            'example_adv': 'mkdir -p projects/2024/documents',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '创建目录,make directory',
            'tips': 'mkdir -p 是最常用的方式，可以一次性创建多级嵌套目录。目录名不要包含空格，用下划线或连字符替代。',
        },
        {
            'cmd_name': 'rm',
            'name_cn': '删除文件或目录',
            'function_desc': '删除指定的文件或目录。注意：Linux 删除操作不可逆，没有回收站！',
            'syntax': 'rm [选项] <目标路径>',
            'params_json': '[{"参数":"-r","说明":"递归删除目录及其所有内容","必填":"可选"},{"参数":"-f","说明":"强制删除，不询问确认","必填":"可选"},{"参数":"-i","说明":"删除前逐一询问确认","必填":"可选"}]',
            'example_basic': 'rm old_file.txt',
            'example_adv': 'rm -rf temp_cache/',
            'os_type': 'Linux/macOS',
            'aliases': '删除,remove',
            'tips': 'rm -rf / 是极度危险的命令，会删除整个系统！建议删除重要文件前先 ls 确认路径。日常使用建议加上 -i 参数。',
        },
        {
            'cmd_name': 'cp',
            'name_cn': '复制文件或目录',
            'function_desc': '将源文件或目录复制到目标位置，可同时保留文件属性。',
            'syntax': 'cp [选项] <源路径> <目标路径>',
            'params_json': '[{"参数":"-r","说明":"递归复制目录","必填":"可选"},{"参数":"-v","说明":"显示复制过程","必填":"可选"},{"参数":"-i","说明":"目标存在时询问是否覆盖","必填":"可选"}]',
            'example_basic': 'cp file.txt backup.txt',
            'example_adv': 'cp -rv /source/dir/ /backup/dir/',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '复制,copy',
            'tips': '复制目录时必须加 -r 参数。cp -i 可以防止意外覆盖已有文件。',
        },
        {
            'cmd_name': 'mv',
            'name_cn': '移动或重命名文件',
            'function_desc': '移动文件/目录到新位置，或者重命名文件/目录。兼具剪切和重命名功能。',
            'syntax': 'mv [选项] <源路径> <目标路径>',
            'params_json': '[{"参数":"-i","说明":"目标存在时询问是否覆盖","必填":"可选"},{"参数":"-v","说明":"显示移动过程","必填":"可选"},{"参数":"-u","说明":"仅当源文件更新时才移动","必填":"可选"}]',
            'example_basic': 'mv file.txt /tmp/',
            'example_adv': 'mv -v project_v1/ project_v2/',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '移动,重命名,move',
            'tips': '在同一目录下 mv 就是重命名。mv 跨文件系统时会先复制再删除源文件。',
        },
        {
            'cmd_name': 'cat',
            'name_cn': '查看文件内容',
            'function_desc': '将文件的全部内容输出到终端。适合查看短文本文件的内容。',
            'syntax': 'cat [选项] <文件路径>',
            'params_json': '[{"参数":"-n","说明":"显示行号","必填":"可选"},{"参数":"-b","说明":"仅对非空行编号","必填":"可选"}]',
            'example_basic': 'cat /etc/hostname',
            'example_adv': 'cat -n file1.txt file2.txt > merged.txt',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '查看,concatenate',
            'tips': '长文件推荐用 less 或 more 替代 cat。cat 也可以用来合并文件：cat a.txt b.txt > c.txt。',
        },
        {
            'cmd_name': 'chmod',
            'name_cn': '修改文件权限',
            'function_desc': '更改文件或目录的读、写、执行权限。是 Linux 安全模型的核心命令。',
            'syntax': 'chmod [选项] <权限模式> <目标路径>',
            'params_json': '[{"参数":"权限模式","说明":"如 755（数字模式）或 u+rwx（符号模式）","必填":"是"},{"参数":"-R","说明":"递归更改目录及其所有内容的权限","必填":"可选"}]',
            'example_basic': 'chmod +x script.sh',
            'example_adv': 'chmod -R 755 /var/www/',
            'os_type': 'Linux/macOS',
            'aliases': '权限,change mode',
            'tips': '权限格式：r=4(读), w=2(写), x=1(执行)。755 = rwxr-xr-x：所有者全部权限，其他用户只读+执行。644 = rw-r--r--：普通文件常用权限。',
        },
        {
            'cmd_name': 'grep',
            'name_cn': '搜索文件内容',
            'function_desc': '在文件中搜索匹配指定模式的行，支持正则表达式。是文本处理的瑞士军刀。',
            'syntax': 'grep [选项] <模式> <文件路径>',
            'params_json': '[{"参数":"-i","说明":"忽略大小写","必填":"可选"},{"参数":"-r","说明":"递归搜索目录","必填":"可选"},{"参数":"-n","说明":"显示匹配行号","必填":"可选"},{"参数":"-v","说明":"反转匹配（显示不匹配的行）","必填":"可选"}]',
            'example_basic': 'grep "error" app.log',
            'example_adv': 'grep -rin "TODO" /src/ --include="*.py"',
            'os_type': 'Linux/macOS',
            'aliases': '搜索,查找文本,grep',
            'tips': 'grep -r 递归搜索目录。grep -E 或 egrep 支持扩展正则表达式。grep -c 只统计匹配行数。',
        },
        {
            'cmd_name': 'find',
            'name_cn': '查找文件',
            'function_desc': '在目录树中根据文件名、类型、大小、修改时间等条件搜索文件或目录。',
            'syntax': 'find <起始目录> [选项] [匹配条件]',
            'params_json': '[{"参数":"-name","说明":"按文件名匹配（支持通配符）","必填":"可选"},{"参数":"-type","说明":"按类型筛选（f=文件,d=目录）","必填":"可选"},{"参数":"-size","说明":"按文件大小筛选","必填":"可选"},{"参数":"-mtime","说明":"按修改时间筛选（天）","必填":"可选"}]',
            'example_basic': 'find . -name "*.py"',
            'example_adv': 'find /var/log -name "*.log" -mtime -7 -exec rm {} \\;',
            'os_type': 'Linux/macOS',
            'aliases': '搜索文件,查找,find',
            'tips': 'find 支持 -exec 参数对每个结果执行命令（{} 代表文件名，\\; 结束）。-mtime -7 表示最近7天内修改过的文件。',
        },
        {
            'cmd_name': 'ps',
            'name_cn': '查看进程信息',
            'function_desc': '显示当前系统中运行的进程快照，包括 PID、CPU/内存使用等。',
            'syntax': 'ps [选项]',
            'params_json': '[{"参数":"aux","说明":"显示所有用户的详细信息进程（BSD风格）","必填":"可选"},{"参数":"-ef","说明":"显示完整格式的进程列表（标准风格）","必填":"可选"}]',
            'example_basic': 'ps aux',
            'example_adv': 'ps aux --sort=-%mem | head -10',
            'os_type': 'Linux/macOS',
            'aliases': '进程,process,process status',
            'tips': 'ps aux 是最常用的用法。配合 grep 过滤：ps aux | grep nginx。top/htop 更适合实时监控。',
        },
        {
            'cmd_name': 'kill',
            'name_cn': '终止进程',
            'function_desc': '向进程发送信号，通常用于终止指定 PID 的进程。',
            'syntax': 'kill [选项] <PID>',
            'params_json': '[{"参数":"-9","说明":"SIGKILL：强制立即终止（无法被捕获）","必填":"可选"},{"参数":"-15","说明":"SIGTERM：请求正常终止（默认信号）","必填":"可选"},{"参数":"-2","说明":"SIGINT：中断（类似 Ctrl+C）","必填":"可选"}]',
            'example_basic': 'kill 12345',
            'example_adv': 'kill -9 12345',
            'os_type': 'Linux/macOS',
            'aliases': '终止,结束进程,kill',
            'tips': '先尝试 kill（SIGTERM=15）让进程优雅退出。只有无法正常终止时才用 kill -9（SIGKILL）。用 ps aux 或 pgrep 先查 PID。',
        },
        {
            'cmd_name': 'top',
            'name_cn': '实时进程监控',
            'function_desc': '动态显示系统中正在运行的进程和系统资源（CPU、内存、负载）的使用情况。',
            'syntax': 'top [选项]',
            'params_json': '[{"参数":"-u","说明":"显示指定用户的进程","必填":"可选"},{"参数":"-p","说明":"监控指定 PID","必填":"可选"}]',
            'example_basic': 'top',
            'example_adv': 'top -u mysql',
            'os_type': 'Linux/macOS',
            'aliases': '监控,资源管理器,top',
            'tips': '进入 top 后按 q 退出，按 1 查看每个 CPU 核心，按 M 按内存排序，按 P 按 CPU 排序。htop 是更友好的替代品。',
        },
        {
            'cmd_name': 'df',
            'name_cn': '查看磁盘空间',
            'function_desc': '显示文件系统的磁盘空间使用情况，包括总大小、已用、可用和挂载点。',
            'syntax': 'df [选项] [挂载点]',
            'params_json': '[{"参数":"-h","说明":"人类可读的格式（GB/MB）","必填":"可选"},{"参数":"-T","说明":"显示文件系统类型","必填":"可选"}]',
            'example_basic': 'df -h',
            'example_adv': 'df -hT /home',
            'os_type': 'Linux/macOS',
            'aliases': '磁盘,空间,disk free',
            'tips': 'df -h 是最常用的方式。du 查看目录大小，df 查看分区整体使用情况。',
        },
        {
            'cmd_name': 'du',
            'name_cn': '查看目录/文件大小',
            'function_desc': '估算文件或目录在磁盘上占用的空间大小。用于排查磁盘空间不足问题。',
            'syntax': 'du [选项] <目标路径>',
            'params_json': '[{"参数":"-h","说明":"人类可读的格式","必填":"可选"},{"参数":"-s","说明":"仅显示总计（不列出子目录）","必填":"可选"},{"参数":"--max-depth=N","说明":"指定递归深度","必填":"可选"}]',
            'example_basic': 'du -sh projects/',
            'example_adv': 'du -h --max-depth=1 /home | sort -rh',
            'os_type': 'Linux/macOS',
            'aliases': '目录大小,disk usage',
            'tips': 'du -sh * 可以列出当前目录下每个文件/目录的大小。和 sort -rh 配合可以按大小排序。',
        },
        {
            'cmd_name': 'tar',
            'name_cn': '打包压缩文件',
            'function_desc': '创建或解压 tar 归档文件，常与 gzip/bzip2 配合实现文件压缩。',
            'syntax': 'tar [选项] <归档文件> [源文件]',
            'params_json': '[{"参数":"-czf","说明":"创建 gzip 压缩的归档","必填":"可选"},{"参数":"-xzf","说明":"解压 gzip 压缩的归档","必填":"可选"},{"参数":"-tvf","说明":"查看归档内容而不解压","必填":"可选"}]',
            'example_basic': 'tar -czf archive.tar.gz myfolder/',
            'example_adv': 'tar -xzf archive.tar.gz -C /tmp/extracted/',
            'os_type': 'Linux/macOS',
            'aliases': '压缩,打包,归档,tar',
            'tips': '常用组合：czf 创建 .tar.gz，xzf 解压 .tar.gz，cjf 创建 .tar.bz2。选项前的 - 可以省略（如 tar czf）。',
        },
        {
            'cmd_name': 'curl',
            'name_cn': 'HTTP 请求工具',
            'function_desc': '强大的命令行网络工具，支持 HTTP/HTTPS/FTP 等多种协议，常用于 API 调试和文件下载。',
            'syntax': 'curl [选项] <URL>',
            'params_json': '[{"参数":"-X","说明":"指定请求方法（GET/POST/PUT/DELETE）","必填":"可选"},{"参数":"-H","说明":"添加请求头","必填":"可选"},{"参数":"-d","说明":"发送 POST 数据（请求体）","必填":"可选"},{"参数":"-o","说明":"将输出保存到文件","必填":"可选"}]',
            'example_basic': 'curl https://api.example.com/users',
            'example_adv': 'curl -X POST -H "Content-Type: application/json" -d \'{"name":"test"}\' https://api.example.com/users',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '网络请求,http,curl',
            'tips': 'curl -v 查看详细请求和响应头。curl -i 查看响应头。配合 jq 可以解析 JSON 返回数据。',
        },
        {
            'cmd_name': 'wget',
            'name_cn': '文件下载工具',
            'function_desc': '从网络下载文件，支持断点续传、递归下载、后台下载等功能。',
            'syntax': 'wget [选项] <下载URL>',
            'params_json': '[{"参数":"-O","说明":"指定保存的文件名","必填":"可选"},{"参数":"-c","说明":"断点续传（继续未完成的下载）","必填":"可选"},{"参数":"-P","说明":"指定保存目录","必填":"可选"}]',
            'example_basic': 'wget https://example.com/file.zip',
            'example_adv': 'wget -c -O output.zip https://example.com/large-file.zip',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '下载,wget',
            'tips': 'wget -c 断点续传非常实用，下载大型文件中断后不需要重头开始。wget -r 可以递归下载整个网站。',
        },
        {
            'cmd_name': 'ssh',
            'name_cn': '远程连接服务器',
            'function_desc': '通过 SSH 协议安全地连接到远程服务器，进行远程管理和操作。',
            'syntax': 'ssh [选项] <用户@主机地址>',
            'params_json': '[{"参数":"-p","说明":"指定 SSH 端口（默认 22）","必填":"可选"},{"参数":"-i","说明":"指定私钥文件路径","必填":"可选"},{"参数":"-v","说明":"详细模式（用于调试连接问题）","必填":"可选"}]',
            'example_basic': 'ssh user@192.168.1.100',
            'example_adv': 'ssh -i ~/.ssh/id_rsa -p 2222 admin@example.com',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '远程连接,ssh,secure shell',
            'tips': '首次连接时会提示确认主机指纹，输入 yes 确认。配置 ~/.ssh/config 可以简化连接参数。',
        },
        {
            'cmd_name': 'scp',
            'name_cn': '远程文件传输',
            'function_desc': '通过 SSH 协议在本地和远程服务器之间安全地复制文件。',
            'syntax': 'scp [选项] <源路径> <目标路径>',
            'params_json': '[{"参数":"-r","说明":"递归复制整个目录","必填":"可选"},{"参数":"-P","说明":"指定 SSH 端口","必填":"可选"},{"参数":"-C","说明":"启用压缩传输","必填":"可选"}]',
            'example_basic': 'scp file.txt user@server:/home/user/',
            'example_adv': 'scp -r -P 2222 user@server:/remote/dir/ ./local-dir/',
            'os_type': 'Linux/macOS/Windows',
            'aliases': '远程复制,scp,文件传输',
            'tips': '从远程复制到本地：scp user@host:远程路径 本地路径。从本地到远程：scp 本地路径 user@host:远程路径。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 Linux 终端命令')


def seed_docker(db):
    """插入 Docker 命令数据"""
    cat_id = db.get_cat_id_by_name('命令行工具', 'Docker')
    if not cat_id:
        print('[错误] 未找到 Docker 分类')
        return

    commands = [
        {
            'cmd_name': 'docker run',
            'name_cn': '创建并启动容器',
            'function_desc': '从镜像创建新容器并启动。如果本地没有镜像，会自动从仓库拉取。',
            'syntax': 'docker run [选项] <镜像名> [命令]',
            'params_json': '[{"参数":"-d","说明":"后台运行（守护模式）","必填":"可选"},{"参数":"-it","说明":"交互式终端模式","必填":"可选"},{"参数":"--name","说明":"为容器指定名称","必填":"可选"},{"参数":"-p","说明":"端口映射（宿主机:容器）","必填":"可选"}]',
            'example_basic': 'docker run nginx',
            'example_adv': 'docker run -d --name my-nginx -p 8080:80 nginx:alpine',
            'os_type': '通用',
            'aliases': '运行容器,启动容器,run',
            'tips': '--rm 参数可在容器停止后自动删除。先 docker pull 拉取镜像再 run 可以避免等待。',
        },
        {
            'cmd_name': 'docker ps',
            'name_cn': '列出容器',
            'function_desc': '列出当前正在运行的 Docker 容器及其基本信息（ID、镜像、端口等）。',
            'syntax': 'docker ps [选项]',
            'params_json': '[{"参数":"-a","说明":"列出所有容器（包括已停止的）","必填":"可选"},{"参数":"-q","说明":"仅显示容器 ID","必填":"可选"}]',
            'example_basic': 'docker ps',
            'example_adv': 'docker ps -a --format "table {{.Names}}\\t{{.Status}}"',
            'os_type': '通用',
            'aliases': '容器列表,ps',
            'tips': 'docker ps -a 查看所有容器（包括已停止的）。docker ps -q 可以配合其他命令批量操作。',
        },
        {
            'cmd_name': 'docker images',
            'name_cn': '列出镜像',
            'function_desc': '列出本地所有 Docker 镜像及其标签、大小等信息。',
            'syntax': 'docker images [选项] [仓库名]',
            'params_json': '[{"参数":"-a","说明":"显示所有镜像（包括中间层）","必填":"可选"},{"参数":"-q","说明":"仅显示镜像 ID","必填":"可选"}]',
            'example_basic': 'docker images',
            'example_adv': 'docker images --format "table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}"',
            'os_type': '通用',
            'aliases': '镜像列表,镜像,images',
            'tips': '定期清理无用的镜像：docker image prune。镜像名通常格式为 仓库名:标签（如 nginx:latest）。',
        },
        {
            'cmd_name': 'docker pull',
            'name_cn': '拉取镜像',
            'function_desc': '从 Docker 镜像仓库（如 Docker Hub）下载镜像到本地。',
            'syntax': 'docker pull [选项] <镜像名[:标签]>',
            'params_json': '[{"参数":"镜像名:标签","说明":"镜像名称和版本标签（默认为 latest）","必填":"是"}]',
            'example_basic': 'docker pull ubuntu:22.04',
            'example_adv': 'docker pull registry.example.com/myapp:v1.0.0',
            'os_type': '通用',
            'aliases': '下载镜像,拉取,pull',
            'tips': '指定具体版本标签（如 :22.04）而非 :latest，确保环境可复现。国内用户可配置镜像加速器。',
        },
        {
            'cmd_name': 'docker build',
            'name_cn': '构建镜像',
            'function_desc': '根据 Dockerfile 中的指令构建 Docker 镜像。是容器化应用的核心操作。',
            'syntax': 'docker build [选项] <构建上下文路径>',
            'params_json': '[{"参数":"-t","说明":"为镜像指定名称和标签","必填":"推荐"},{"参数":"-f","说明":"指定 Dockerfile 路径（默认 ./Dockerfile）","必填":"可选"}]',
            'example_basic': 'docker build -t myapp .',
            'example_adv': 'docker build -t myapp:1.0 -f docker/Dockerfile.prod .',
            'os_type': '通用',
            'aliases': '构建镜像,打包,build',
            'tips': '. 是构建上下文路径，Docker 会将此目录发送给守护进程。使用 .dockerignore 排除不需要的文件以加快构建速度。',
        },
        {
            'cmd_name': 'docker exec',
            'name_cn': '在容器中执行命令',
            'function_desc': '在运行中的容器内部执行命令，常用于调试和进入容器 shell。',
            'syntax': 'docker exec [选项] <容器名/ID> <命令>',
            'params_json': '[{"参数":"-it","说明":"交互式终端模式","必填":"推荐"},{"参数":"-u","说明":"指定用户执行命令","必填":"可选"}]',
            'example_basic': 'docker exec my-container ls /app',
            'example_adv': 'docker exec -it my-container /bin/bash',
            'os_type': '通用',
            'aliases': '执行命令,进入容器,exec',
            'tips': '进入容器 shell 常用 docker exec -it 容器名 sh（alpine 镜像）或 bash（ubuntu/debian 镜像）。',
        },
        {
            'cmd_name': 'docker stop',
            'name_cn': '停止容器',
            'function_desc': '优雅地停止一个或多个运行中的容器（发送 SIGTERM 信号）。',
            'syntax': 'docker stop [选项] <容器名/ID>',
            'params_json': '[{"参数":"-t","说明":"等待停止的超时时间（秒），超时后强制杀死","必填":"可选"}]',
            'example_basic': 'docker stop my-container',
            'example_adv': 'docker stop -t 30 my-container',
            'os_type': '通用',
            'aliases': '停止容器,stop',
            'tips': 'docker stop 发送 SIGTERM 让进程优雅退出。如果容器不响应，可用 docker kill 强制终止。',
        },
        {
            'cmd_name': 'docker rm',
            'name_cn': '删除容器',
            'function_desc': '删除一个或多个已停止的容器。可以同时清理关联的匿名卷。',
            'syntax': 'docker rm [选项] <容器名/ID>',
            'params_json': '[{"参数":"-v","说明":"同时删除关联的匿名卷","必填":"可选"},{"参数":"-f","说明":"强制删除运行中的容器（先 stop）","必填":"可选"}]',
            'example_basic': 'docker rm my-container',
            'example_adv': 'docker rm -v $(docker ps -aq -f "status=exited")',
            'os_type': '通用',
            'aliases': '删除容器,rm',
            'tips': 'docker container prune 可以一次性删除所有已停止的容器。批量删除：docker rm $(docker ps -aq)。',
        },
        {
            'cmd_name': 'docker rmi',
            'name_cn': '删除镜像',
            'function_desc': '删除一个或多个本地 Docker 镜像。镜像会在不被任何容器使用时才能被删除。',
            'syntax': 'docker rmi [选项] <镜像名/ID>',
            'params_json': '[{"参数":"-f","说明":"强制删除镜像","必填":"可选"}]',
            'example_basic': 'docker rmi nginx:latest',
            'example_adv': 'docker rmi $(docker images -q -f "dangling=true")',
            'os_type': '通用',
            'aliases': '删除镜像,rmi',
            'tips': 'dangling=true 筛选悬空镜像（<none>:<none>）。docker image prune 可以批量清理。',
        },
        {
            'cmd_name': 'docker logs',
            'name_cn': '查看容器日志',
            'function_desc': '查看容器的标准输出/标准错误日志，用于调试和监控应用运行状态。',
            'syntax': 'docker logs [选项] <容器名/ID>',
            'params_json': '[{"参数":"-f","说明":"实时追踪日志输出（类似 tail -f）","必填":"可选"},{"参数":"--tail","说明":"仅显示最后 N 行日志","必填":"可选"},{"参数":"-t","说明":"显示时间戳","必填":"可选"}]',
            'example_basic': 'docker logs my-container',
            'example_adv': 'docker logs -f --tail 100 my-container',
            'os_type': '通用',
            'aliases': '日志,logs',
            'tips': 'docker logs -f 实时跟踪日志。--tail 限制行数。docker logs --since 5m 查看最近5分钟的日志。',
        },
        {
            'cmd_name': 'docker-compose up',
            'name_cn': '启动 Compose 项目',
            'function_desc': '根据 docker-compose.yml 配置，创建并启动所有定义的服务容器。',
            'syntax': 'docker-compose up [选项] [服务名]',
            'params_json': '[{"参数":"-d","说明":"后台运行所有服务","必填":"可选"},{"参数":"--build","说明":"启动前重新构建镜像","必填":"可选"},{"参数":"-f","说明":"指定 Compose 文件路径","必填":"可选"}]',
            'example_basic': 'docker-compose up -d',
            'example_adv': 'docker-compose up -d --build web',
            'os_type': '通用',
            'aliases': 'compose启动,编排,up',
            'tips': 'docker-compose down 停止并移除所有容器和网络。docker-compose logs -f 查看所有服务的日志。',
        },
        {
            'cmd_name': 'docker network',
            'name_cn': '管理网络',
            'function_desc': '创建、列出和管理 Docker 网络，用于容器之间的通信和隔离。',
            'syntax': 'docker network <子命令> [选项]',
            'params_json': '[{"参数":"ls","说明":"列出所有 Docker 网络","必填":"可选"},{"参数":"create","说明":"创建新网络","必填":"可选"},{"参数":"connect","说明":"将容器连接到网络","必填":"可选"}]',
            'example_basic': 'docker network ls',
            'example_adv': 'docker network create --driver bridge my-network',
            'os_type': '通用',
            'aliases': '网络,network',
            'tips': '默认有 bridge、host、none 三种网络。自定义 bridge 网络可以让容器通过服务名互相访问。',
        },
        {
            'cmd_name': 'docker volume',
            'name_cn': '管理数据卷',
            'function_desc': '创建和管理 Docker 数据卷，用于持久化容器数据并在容器间共享数据。',
            'syntax': 'docker volume <子命令> [选项]',
            'params_json': '[{"参数":"ls","说明":"列出所有数据卷","必填":"可选"},{"参数":"create","说明":"创建新数据卷","必填":"可选"},{"参数":"prune","说明":"删除未被使用的数据卷","必填":"可选"}]',
            'example_basic': 'docker volume ls',
            'example_adv': 'docker volume create --name mydata',
            'os_type': '通用',
            'aliases': '数据卷,volume,持久化',
            'tips': '数据卷比绑定挂载（bind mount）更推荐，因为 Docker 可以更好地管理。docker run -v mydata:/data 挂载卷。',
        },
        {
            'cmd_name': 'docker inspect',
            'name_cn': '查看容器/镜像详情',
            'function_desc': '以 JSON 格式显示容器、镜像、网络、数据卷等 Docker 对象的详细信息。',
            'syntax': 'docker inspect [选项] <对象名/ID>',
            'params_json': '[{"参数":"-f","说明":"通过 Go 模板过滤特定字段","必填":"可选"}]',
            'example_basic': 'docker inspect my-container',
            'example_adv': 'docker inspect -f "{{.NetworkSettings.IPAddress}}" my-container',
            'os_type': '通用',
            'aliases': '查看详情,检查,inspect',
            'tips': '适用于调试：查看容器的 IP 地址、挂载卷、环境变量等。-f 参数配合 Go 模板可以只提取需要的字段。',
        },
        {
            'cmd_name': 'docker system prune',
            'name_cn': '清理 Docker 资源',
            'function_desc': '删除所有未被使用的 Docker 资源（容器、网络、镜像、构建缓存），释放磁盘空间。',
            'syntax': 'docker system prune [选项]',
            'params_json': '[{"参数":"-a","说明":"删除所有未使用的镜像（不仅仅是悬空镜像）","必填":"可选"},{"参数":"--volumes","说明":"同时清理未使用的数据卷","必填":"可选"},{"参数":"-f","说明":"强制清理，无需确认","必填":"可选"}]',
            'example_basic': 'docker system prune',
            'example_adv': 'docker system prune -a --volumes -f',
            'os_type': '通用',
            'aliases': '清理,prune,垃圾回收',
            'tips': '定期执行 docker system prune 可以释放大量磁盘空间。加 -a 会删除未使用的镜像（包括已打标签的），谨慎使用。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 Docker 命令')


def seed_cmd_windows(db):
    """插入 Windows CMD 命令数据"""
    cat_id = db.get_cat_id_by_name('命令行工具', 'CMD (Windows)')
    if not cat_id:
        print('[错误] 未找到 CMD (Windows) 分类')
        return

    commands = [
        {
            'cmd_name': 'dir',
            'name_cn': '列出目录内容',
            'function_desc': '显示当前目录下的文件和子目录列表，是 Windows CMD 最常用的命令。',
            'syntax': 'dir [驱动器:][路径] [选项]',
            'params_json': '[{"参数":"/w","说明":"宽列表显示","必填":"可选"},{"参数":"/s","说明":"递归显示所有子目录","必填":"可选"},{"参数":"/b","说明":"简洁模式（仅显示文件名）","必填":"可选"}]',
            'example_basic': 'dir',
            'example_adv': 'dir C:\\Windows\\System32 /w /s',
            'os_type': 'Windows',
            'aliases': '列出目录,dir',
            'tips': 'dir /a 显示所有文件（包括隐藏和系统文件）。dir /p 分页显示内容。',
        },
        {
            'cmd_name': 'cd',
            'name_cn': '切换目录',
            'function_desc': '显示当前目录路径或切换到另一个目录。',
            'syntax': 'cd [/d] [驱动器:][路径]',
            'params_json': '[{"参数":"/d","说明":"同时切换驱动器（如从 C: 切换到 D:）","必填":"可选"},{"参数":"..","说明":"返回上一级目录","必填":"可选"}]',
            'example_basic': 'cd Documents',
            'example_adv': 'cd /d D:\\Projects\\myapp',
            'os_type': 'Windows',
            'aliases': '切换目录,cd,chdir',
            'tips': '仅输入 cd 可以显示当前路径。cd /d 可以在不同驱动器之间切换（如从 C: 到 D:）。',
        },
        {
            'cmd_name': 'mkdir',
            'name_cn': '创建目录',
            'function_desc': '创建新目录，如果中间目录不存在会自动创建（类似 Linux 的 mkdir -p）。',
            'syntax': 'mkdir <目录名>',
            'params_json': '[{"参数":"目录名","说明":"要创建的目录名或路径","必填":"是"}]',
            'example_basic': 'mkdir myproject',
            'example_adv': 'mkdir C:\\projects\\myapp\\src\\components',
            'os_type': 'Windows',
            'aliases': '创建目录,mkdir,md',
            'tips': '在 CMD 中 mkdir 和 md 是等价的。路径中包含空格时需要用引号括起来。',
        },
        {
            'cmd_name': 'copy',
            'name_cn': '复制文件',
            'function_desc': '将一个或多个文件复制到指定位置。',
            'syntax': 'copy <源文件> <目标路径>',
            'params_json': '[{"参数":"/y","说明":"覆盖已有文件时不询问","必填":"可选"},{"参数":"/v","说明":"验证目标文件是否正确写入","必填":"可选"}]',
            'example_basic': 'copy file.txt backup.txt',
            'example_adv': 'copy C:\\src\\*.txt D:\\backup\\ /y',
            'os_type': 'Windows',
            'aliases': '复制,copy,xcopy',
            'tips': '复制目录及其所有内容推荐用 xcopy 或 robocopy（功能更强）。copy /b 可用于合并二进制文件。',
        },
        {
            'cmd_name': 'del',
            'name_cn': '删除文件',
            'function_desc': '删除一个或多个文件。注意：Windows CMD 删除的文件不进入回收站。',
            'syntax': 'del [选项] <文件名>',
            'params_json': '[{"参数":"/f","说明":"强制删除只读文件","必填":"可选"},{"参数":"/s","说明":"从所有子目录删除匹配的文件","必填":"可选"},{"参数":"/q","说明":"静默模式（不询问确认）","必填":"可选"}]',
            'example_basic': 'del temp.txt',
            'example_adv': 'del /s /q *.log',
            'os_type': 'Windows',
            'aliases': '删除,del,erase',
            'tips': 'del 只能删除文件，删除目录用 rmdir 或 rd。删除的文件不会进入回收站，请谨慎操作。',
        },
        {
            'cmd_name': 'move',
            'name_cn': '移动或重命名文件',
            'function_desc': '移动文件/目录到新位置，或重命名文件/目录。',
            'syntax': 'move <源路径> <目标路径>',
            'params_json': '[{"参数":"/y","说明":"覆盖已有文件时不询问","必填":"可选"}]',
            'example_basic': 'move file.txt backup\\',
            'example_adv': 'move C:\\src\\old_name.txt C:\\src\\new_name.txt',
            'os_type': 'Windows',
            'aliases': '移动,重命名,move',
            'tips': '在同一目录下 move 就是重命名操作。跨驱动器移动实际上是复制+删除。',
        },
        {
            'cmd_name': 'ren',
            'name_cn': '重命名文件/目录',
            'function_desc': '重命名文件或目录，是 rename 命令的缩写形式。',
            'syntax': 'ren <旧名称> <新名称>',
            'params_json': '[{"参数":"旧名称","说明":"要重命名的文件/目录当前名称","必填":"是"},{"参数":"新名称","说明":"新的名称","必填":"是"}]',
            'example_basic': 'ren report.txt report_2024.txt',
            'example_adv': 'ren *.htm *.html',
            'os_type': 'Windows',
            'aliases': '重命名,ren,rename',
            'tips': 'ren 不支持更改路径（不能跨目录重命名）。可以用通配符批量重命名扩展名。',
        },
        {
            'cmd_name': 'type',
            'name_cn': '查看文件内容',
            'function_desc': '在 CMD 窗口中显示文本文件的内容。类似 Linux 的 cat 命令。',
            'syntax': 'type <文件名>',
            'params_json': '[{"参数":"文件名","说明":"要查看的文本文件路径","必填":"是"}]',
            'example_basic': 'type readme.txt',
            'example_adv': 'type C:\\Users\\admin\\Documents\\notes.txt | more',
            'os_type': 'Windows',
            'aliases': '查看文件,type',
            'tips': '内容太多时可用 type file.txt | more 分页查看。type file.txt | find "keyword" 搜索关键词。',
        },
        {
            'cmd_name': 'cls',
            'name_cn': '清屏',
            'function_desc': '清除 CMD 窗口中的所有内容，将光标回到窗口顶部。',
            'syntax': 'cls',
            'params_json': '[]',
            'example_basic': 'cls',
            'example_adv': 'cls',
            'os_type': 'Windows',
            'aliases': '清屏,cls,clear',
            'tips': '与 Linux 的 clear 命令功能相同。CMD 中无快捷键，只能输入 cls 或按 Ctrl+L（部分终端支持）。',
        },
        {
            'cmd_name': 'echo',
            'name_cn': '输出文本/设置变量',
            'function_desc': '在 CMD 窗口中显示消息，或设置命令回显模式（on/off）。',
            'syntax': 'echo [消息]',
            'params_json': '[{"参数":"消息","说明":"要显示的文本信息","必填":"可选"},{"参数":"on/off","说明":"开启或关闭命令回显","必填":"可选"}]',
            'example_basic': 'echo Hello World',
            'example_adv': 'echo %USERNAME% && echo %DATE% %TIME%',
            'os_type': 'Windows',
            'aliases': '输出,echo',
            'tips': 'echo off 可用于批处理文件开头隐藏命令行本身。echo. 输出空行。%变量名% 引用环境变量。',
        },
        {
            'cmd_name': 'set',
            'name_cn': '设置/查看环境变量',
            'function_desc': '显示、设置或删除 CMD 环境变量。不加参数则列出所有环境变量。',
            'syntax': 'set [变量名=值]',
            'params_json': '[{"参数":"变量名=值","说明":"设置环境变量","必填":"可选"},{"参数":"变量名","说明":"查看指定变量的值","必填":"可选"}]',
            'example_basic': 'set',
            'example_adv': 'set MY_PATH=C:\\tools\\bin && echo %MY_PATH%',
            'os_type': 'Windows',
            'aliases': '变量,环境变量,set',
            'tips': 'set 设置的变量只在当前 CMD 会话中有效。使用 setx 命令可以设置永久环境变量。',
        },
        {
            'cmd_name': 'ping',
            'name_cn': '测试网络连通性',
            'function_desc': '向目标主机发送 ICMP 回显请求，测试网络连通性和响应延迟。',
            'syntax': 'ping [选项] <目标主机>',
            'params_json': '[{"参数":"-t","说明":"持续 ping 直到手动停止（Ctrl+C）","必填":"可选"},{"参数":"-n","说明":"指定发送的回显请求次数","必填":"可选"}]',
            'example_basic': 'ping google.com',
            'example_adv': 'ping -t 192.168.1.1',
            'os_type': 'Windows',
            'aliases': '网络测试,ping',
            'tips': 'ping -t 持续测试网络稳定性。Windows 默认 4 次，Linux 默认持续。',
        },
        {
            'cmd_name': 'ipconfig',
            'name_cn': '查看网络配置',
            'function_desc': '显示本机网络接口的 IP 地址、子网掩码、默认网关等配置信息。',
            'syntax': 'ipconfig [选项]',
            'params_json': '[{"参数":"/all","说明":"显示所有网络适配器的详细信息","必填":"可选"},{"参数":"/release","说明":"释放 DHCP 分配的 IP 地址","必填":"可选"},{"参数":"/renew","说明":"重新获取 DHCP IP 地址","必填":"可选"}]',
            'example_basic': 'ipconfig',
            'example_adv': 'ipconfig /all | findstr "IPv4"',
            'os_type': 'Windows',
            'aliases': 'IP配置,网络信息,ipconfig',
            'tips': 'ipconfig /flushdns 可以清除 DNS 缓存。ipconfig /release 和 /renew 常用于排除 DHCP 问题。',
        },
        {
            'cmd_name': 'netstat',
            'name_cn': '查看网络连接状态',
            'function_desc': '显示网络连接、路由表和网络接口统计信息，用于监控网络活动。',
            'syntax': 'netstat [选项]',
            'params_json': '[{"参数":"-a","说明":"显示所有连接和监听端口","必填":"可选"},{"参数":"-n","说明":"以数字形式显示地址和端口","必填":"可选"},{"参数":"-o","说明":"显示关联的进程 PID","必填":"可选"}]',
            'example_basic': 'netstat -an',
            'example_adv': 'netstat -ano | findstr ":80"',
            'os_type': 'Windows',
            'aliases': '网络状态,端口查看,netstat',
            'tips': 'netstat -ano 查看所有连接及对应 PID。查到的 PID 可在任务管理器中定位具体程序。',
        },
        {
            'cmd_name': 'tasklist',
            'name_cn': '查看进程列表',
            'function_desc': '显示当前系统上运行的所有进程及其详细信息（PID、内存使用等）。类似任务管理器。',
            'syntax': 'tasklist [选项]',
            'params_json': '[{"参数":"/v","说明":"显示详细信息","必填":"可选"},{"参数":"/fi","说明":"按条件筛选进程（如 /fi "STATUS eq running"）","必填":"可选"},{"参数":"/m","说明":"显示加载了指定 DLL 的进程","必填":"可选"}]',
            'example_basic': 'tasklist',
            'example_adv': 'tasklist /fi "MEMUSAGE gt 100000" /v',
            'os_type': 'Windows',
            'aliases': '进程列表,tasklist',
            'tips': '配合 taskkill 使用可以终止进程：taskkill /PID 1234。/fi 可以按内存使用、状态等条件筛选。',
        },
        {
            'cmd_name': 'findstr',
            'name_cn': '搜索文件中的文本',
            'function_desc': '在文件中搜索指定的文本模式，支持正则表达式。是 Windows 版 grep。',
            'syntax': 'findstr [选项] <模式> [文件]',
            'params_json': '[{"参数":"/i","说明":"忽略大小写","必填":"可选"},{"参数":"/s","说明":"递归搜索子目录","必填":"可选"},{"参数":"/n","说明":"显示行号","必填":"可选"},{"参数":"/r","说明":"使用正则表达式搜索","必填":"可选"}]',
            'example_basic': 'findstr "error" app.log',
            'example_adv': 'findstr /i /s /n "TODO" *.py',
            'os_type': 'Windows',
            'aliases': '搜索文本,grep,findstr',
            'tips': 'findstr 是 CMD 中最接近 Linux grep 的命令，支持基本正则表达式。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 CMD 命令')


def seed_powershell(db):
    """插入 PowerShell 命令数据"""
    cat_id = db.get_cat_id_by_name('命令行工具', 'PowerShell')
    if not cat_id:
        print('[错误] 未找到 PowerShell 分类')
        return

    commands = [
        {
            'cmd_name': 'Get-ChildItem',
            'name_cn': '列出目录内容',
            'function_desc': '获取指定目录中的文件和子目录列表（类似 CMD 的 dir 和 Linux 的 ls）。',
            'syntax': 'Get-ChildItem [[-Path] <路径>] [选项]',
            'params_json': '[{"参数":"-Path","说明":"指定要查看的目录路径","必填":"可选"},{"参数":"-Recurse","说明":"递归获取所有子目录内容","必填":"可选"},{"参数":"-Filter","说明":"按文件名模式过滤","必填":"可选"}]',
            'example_basic': 'Get-ChildItem',
            'example_adv': 'Get-ChildItem -Path C:\\Projects -Recurse -Filter "*.py"',
            'os_type': 'Windows',
            'aliases': '列出目录,ls,dir,gci',
            'tips': '别名：ls、dir。gci 是简写。PowerShell 的命令是 动词-名词 格式，比 CMD 更一致。',
        },
        {
            'cmd_name': 'Set-Location',
            'name_cn': '切换目录',
            'function_desc': '切换到指定目录，是 PowerShell 中的 cd 命令。',
            'syntax': 'Set-Location [[-Path] <路径>]',
            'params_json': '[{"参数":"-Path","说明":"目标目录路径","必填":"可选"}]',
            'example_basic': 'Set-Location C:\\Projects',
            'example_adv': 'Set-Location -Path D:\\Work\\2024 -PassThru',
            'os_type': 'Windows',
            'aliases': '切换目录,cd,sl',
            'tips': '别名：cd、chdir。sl 是简写。Set-Location .. 返回上级目录。',
        },
        {
            'cmd_name': 'Get-Content',
            'name_cn': '查看文件内容',
            'function_desc': '读取并显示文本文件的内容，支持分页、尾随等高级功能。',
            'syntax': 'Get-Content [-Path] <文件路径> [选项]',
            'params_json': '[{"参数":"-Tail","说明":"显示文件末尾的 N 行","必填":"可选"},{"参数":"-TotalCount","说明":"显示文件开头的 N 行","必填":"可选"},{"参数":"-Wait","说明":"实时追踪文件新增内容（类似 tail -f）","必填":"可选"}]',
            'example_basic': 'Get-Content log.txt',
            'example_adv': 'Get-Content app.log -Tail 100 -Wait',
            'os_type': 'Windows',
            'aliases': '查看文件,cat,gc,type',
            'tips': '别名：cat、type。gc 是简写。Get-Content -Wait 实现实时日志追踪。',
        },
        {
            'cmd_name': 'Select-String',
            'name_cn': '搜索文件内容',
            'function_desc': '在文本中搜索匹配模式的行，类似 Linux 的 grep 和 CMD 的 findstr。',
            'syntax': 'Select-String [-Pattern] <模式> [-Path] <文件路径>',
            'params_json': '[{"参数":"-Pattern","说明":"要搜索的文本或正则表达式","必填":"是"},{"参数":"-Path","说明":"要搜索的文件路径","必填":"可选"},{"参数":"-CaseSensitive","说明":"区分大小写","必填":"可选"}]',
            'example_basic': 'Select-String -Pattern "error" -Path app.log',
            'example_adv': 'Get-ChildItem *.py -Recurse | Select-String "TODO"',
            'os_type': 'Windows',
            'aliases': '搜索,grep,sls',
            'tips': '别名：sls。通过管道 Get-ChildItem | Select-String 实现递归搜索。',
        },
        {
            'cmd_name': 'Where-Object',
            'name_cn': '筛选对象',
            'function_desc': '根据条件筛选管道中的对象，是 PowerShell 管道中的核心过滤命令。',
            'syntax': 'Where-Object { 条件表达式 }',
            'params_json': '[{"参数":"条件表达式","说明":"筛选条件，如 $_.Length -gt 1MB","必填":"是"}]',
            'example_basic': 'Get-Process | Where-Object { $_.CPU -gt 10 }',
            'example_adv': 'Get-ChildItem -Recurse | Where-Object { $_.Length -gt 100MB -and $_.Extension -eq ".zip" }',
            'os_type': 'Windows',
            'aliases': '筛选,where,?',
            'tips': 'Where-Object 可以简写为 ?。$_ 代表管道中当前对象。条件是 PowerShell 表达式，用 -gt/-lt/-eq 比较。',
        },
        {
            'cmd_name': 'ForEach-Object',
            'name_cn': '遍历处理对象',
            'function_desc': '对管道中的每个对象执行指定操作，是 PowerShell 批处理的核心命令。',
            'syntax': 'ForEach-Object { 操作表达式 }',
            'params_json': '[{"参数":"操作表达式","说明":"对每个对象执行的操作，$_ 代表当前对象","必填":"是"}]',
            'example_basic': '1..10 | ForEach-Object { $_ * $_ }',
            'example_adv': 'Get-ChildItem *.log | ForEach-Object { $_.Name + " → " + $_.Length + " bytes" }',
            'os_type': 'Windows',
            'aliases': '遍历,foreach,%',
            'tips': 'ForEach-Object 可以简写为 %。$_ 代表当前对象。Begin/Process/End 脚本块用于更复杂的处理。',
        },
        {
            'cmd_name': 'Get-Process',
            'name_cn': '查看进程',
            'function_desc': '获取本地计算机上运行的所有进程信息（PID、CPU、内存等），类似任务管理器。',
            'syntax': 'Get-Process [[-Name] <进程名>]',
            'params_json': '[{"参数":"-Name","说明":"按进程名筛选（支持通配符）","必填":"可选"},{"参数":"-Id","说明":"按 PID 查找进程","必填":"可选"}]',
            'example_basic': 'Get-Process',
            'example_adv': 'Get-Process -Name "chrome" | Sort-Object WorkingSet -Descending | Select-Object -First 10',
            'os_type': 'Windows',
            'aliases': '进程,ps,gps',
            'tips': '别名：ps。返回值是对象，可以管道到 Where-Object、Sort-Object 等进行后续处理。',
        },
        {
            'cmd_name': 'Stop-Process',
            'name_cn': '终止进程',
            'function_desc': '终止一个或多个正在运行的进程，可以按名称或 PID 指定。',
            'syntax': 'Stop-Process [-Id] <PID> / [-Name] <进程名>',
            'params_json': '[{"参数":"-Id","说明":"要终止的进程 PID","必填":"是"},{"参数":"-Name","说明":"按进程名终止（如 notepad）","必填":"是"},{"参数":"-Force","说明":"强制终止进程","必填":"可选"}]',
            'example_basic': 'Stop-Process -Name notepad',
            'example_adv': 'Get-Process -Name "chrome" | Where-Object { $_.WorkingSet -gt 500MB } | Stop-Process -Force',
            'os_type': 'Windows',
            'aliases': '终止进程,kill,spps',
            'tips': '别名：kill。先用 Get-Process 确认进程再终止。',
        },
        {
            'cmd_name': 'Invoke-WebRequest',
            'name_cn': '发送 HTTP 请求',
            'function_desc': '向指定 URL 发送 HTTP/HTTPS 请求并获取响应，是 PowerShell 版 curl/wget。',
            'syntax': 'Invoke-WebRequest [-Uri] <URL> [选项]',
            'params_json': '[{"参数":"-Uri","说明":"请求的目标 URL","必填":"是"},{"参数":"-Method","说明":"HTTP 方法（GET/POST/PUT/DELETE）","必填":"可选"},{"参数":"-Headers","说明":"自定义请求头","必填":"可选"},{"参数":"-Body","说明":"请求体内容","必填":"可选"}]',
            'example_basic': 'Invoke-WebRequest -Uri https://api.example.com',
            'example_adv': '$body = @{name="test";email="test@example.com"} | ConvertTo-Json; Invoke-WebRequest -Uri https://api.example.com/users -Method POST -Body $body -ContentType "application/json"',
            'os_type': 'Windows',
            'aliases': '网络请求,curl,wget,iwr',
            'tips': '别名：curl、wget（但不是真正的 curl/wget）。Invoke-RestMethod 更适合 REST API 调用（自动解析 JSON）。',
        },
        {
            'cmd_name': 'Get-Help',
            'name_cn': '查看命令帮助',
            'function_desc': '显示 PowerShell 命令的详细帮助信息，包括参数说明、示例等。是学习 PowerShell 的最佳入口。',
            'syntax': 'Get-Help <命令名> [选项]',
            'params_json': '[{"参数":"-Examples","说明":"仅显示命令示例","必填":"可选"},{"参数":"-Detailed","说明":"显示详细帮助（含参数说明）","必填":"可选"},{"参数":"-Online","说明":"在浏览器中打开在线帮助文档","必填":"可选"}]',
            'example_basic': 'Get-Help Get-Process',
            'example_adv': 'Get-Help Select-String -Examples',
            'os_type': 'Windows',
            'aliases': '帮助,man,help,gh',
            'tips': '首次使用可运行 Update-Help 下载最新帮助。Get-Command 可以列出所有可用的 PowerShell 命令。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 PowerShell 命令')


def seed_mysql(db):
    """插入 MySQL 命令数据（SQL 语句）"""
    cat_id = db.get_cat_id_by_name('数据库', 'MySQL')
    if not cat_id:
        print('[错误] 未找到 MySQL 分类')
        return

    commands = [
        {
            'cmd_name': 'CREATE DATABASE',
            'name_cn': '创建数据库',
            'function_desc': '创建一个新的数据库，用于存储表和数据的容器。',
            'syntax': 'CREATE DATABASE [IF NOT EXISTS] <数据库名> [CHARACTER SET 字符集]',
            'params_json': '[{"参数":"IF NOT EXISTS","说明":"如果数据库不存在才创建（避免重复创建报错）","必填":"可选"},{"参数":"CHARACTER SET","说明":"指定字符集（如 utf8mb4）","必填":"可选"}]',
            'example_basic': 'CREATE DATABASE mydb;',
            'example_adv': 'CREATE DATABASE IF NOT EXISTS mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;',
            'os_type': '通用',
            'aliases': '创建数据库,CREATE DATABASE',
            'tips': '推荐使用 utf8mb4 字符集（支持 emoji 等 4 字节字符）。数据库名不要包含特殊字符和空格。',
        },
        {
            'cmd_name': 'CREATE TABLE',
            'name_cn': '创建表',
            'function_desc': '在当前数据库中创建新表，定义列名、数据类型和约束。',
            'syntax': 'CREATE TABLE [IF NOT EXISTS] <表名> (列定义...) [表选项]',
            'params_json': '[{"参数":"IF NOT EXISTS","说明":"表不存在时才创建","必填":"可选"},{"参数":"列定义","说明":"列名 数据类型 [约束]，多列用逗号分隔","必填":"是"}]',
            'example_basic': 'CREATE TABLE users (id INT, name VARCHAR(100), email VARCHAR(200));',
            'example_adv': 'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(200) UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB;',
            'os_type': '通用',
            'aliases': '建表,CREATE TABLE',
            'tips': '规划好数据类型和索引再建表，后期修改代价大。InnoDB 引擎推荐用于生产环境（支持事务、外键）。',
        },
        {
            'cmd_name': 'SELECT',
            'name_cn': '查询数据',
            'function_desc': '从表中查询数据，是 SQL 中最常用的语句。可以筛选列、行、排序、分组等。',
            'syntax': 'SELECT <列名> FROM <表名> [WHERE 条件] [ORDER BY 排序] [LIMIT 数量]',
            'params_json': '[{"参数":"列名","说明":"要查询的列，* 代表所有列","必填":"是"},{"参数":"DISTINCT","说明":"去重，只返回不同值","必填":"可选"}]',
            'example_basic': 'SELECT * FROM users;',
            'example_adv': 'SELECT name, email FROM users WHERE created_at > "2024-01-01" ORDER BY created_at DESC LIMIT 10;',
            'os_type': '通用',
            'aliases': '查询,SELECT,查询语句',
            'tips': '生产环境避免用 SELECT *，明确列出需要的列以提高性能。WHERE 条件中的列有索引会快很多。',
        },
        {
            'cmd_name': 'INSERT INTO',
            'name_cn': '插入数据',
            'function_desc': '向表中插入一行或多行新数据。',
            'syntax': 'INSERT INTO <表名> (列名...) VALUES (值...)',
            'params_json': '[{"参数":"列名","说明":"要插入数据的列（可选，不填则需为所有列提供值）","必填":"可选"},{"参数":"VALUES","说明":"要插入的值，多行用逗号分隔","必填":"是"}]',
            'example_basic': 'INSERT INTO users (name, email) VALUES ("张三", "zhang@example.com");',
            'example_adv': 'INSERT INTO users (name, email) VALUES ("张三", "a@e.com"), ("李四", "b@e.com"), ("王五", "c@e.com");',
            'os_type': '通用',
            'aliases': '插入,INSERT,添加数据',
            'tips': '一次 INSERT 多行比多次单行插入快得多。注意字符串要用单引号括起来。',
        },
        {
            'cmd_name': 'UPDATE',
            'name_cn': '更新数据',
            'function_desc': '修改表中满足条件的行的指定列的值。',
            'syntax': 'UPDATE <表名> SET 列名=新值 [WHERE 条件]',
            'params_json': '[{"参数":"SET","说明":"指定要修改的列及其新值","必填":"是"},{"参数":"WHERE","说明":"筛选要更新的行（非常重要！不加会更新所有行）","必填":"推荐"}]',
            'example_basic': 'UPDATE users SET name="张三" WHERE id=1;',
            'example_adv': 'UPDATE users SET email=CONCAT(id, "@example.com"), updated_at=NOW() WHERE email IS NULL;',
            'os_type': '通用',
            'aliases': '更新,UPDATE,修改数据',
            'tips': '⚠️ 忘写 WHERE 会更新整张表！建议先 SELECT 确认条件，再改成 UPDATE。',
        },
        {
            'cmd_name': 'DELETE',
            'name_cn': '删除数据',
            'function_desc': '删除表中满足条件的行。',
            'syntax': 'DELETE FROM <表名> [WHERE 条件]',
            'params_json': '[{"参数":"WHERE","说明":"筛选要删除的行（不加会删除所有行！）","必填":"推荐"}]',
            'example_basic': 'DELETE FROM users WHERE id=1;',
            'example_adv': 'DELETE FROM users WHERE created_at < "2020-01-01" ORDER BY id LIMIT 1000;',
            'os_type': '通用',
            'aliases': '删除,DELETE,删除数据',
            'tips': '⚠️ DELETE 不加 WHERE = 清空表。TRUNCATE TABLE 比 DELETE 全表更快（但无法回滚）。',
        },
        {
            'cmd_name': 'ALTER TABLE',
            'name_cn': '修改表结构',
            'function_desc': '修改已有表的结构：添加/删除/修改列、添加索引等。',
            'syntax': 'ALTER TABLE <表名> <操作>',
            'params_json': '[{"参数":"ADD COLUMN","说明":"添加新列","必填":"可选"},{"参数":"DROP COLUMN","说明":"删除列","必填":"可选"},{"参数":"MODIFY COLUMN","说明":"修改列的数据类型","必填":"可选"},{"参数":"RENAME TO","说明":"重命名表","必填":"可选"}]',
            'example_basic': 'ALTER TABLE users ADD COLUMN phone VARCHAR(20);',
            'example_adv': 'ALTER TABLE users MODIFY COLUMN email VARCHAR(255) NOT NULL, ADD INDEX idx_email (email);',
            'os_type': '通用',
            'aliases': '改表,ALTER TABLE',
            'tips': 'ALTER TABLE 在大表上可能很慢，建议在低峰期操作。修改列类型可能导致数据截断。',
        },
        {
            'cmd_name': 'DROP TABLE',
            'name_cn': '删除表',
            'function_desc': '删除表及其所有数据，操作不可逆。',
            'syntax': 'DROP TABLE [IF EXISTS] <表名>',
            'params_json': '[{"参数":"IF EXISTS","说明":"表存在时才删除，避免报错","必填":"可选"}]',
            'example_basic': 'DROP TABLE temp_data;',
            'example_adv': 'DROP TABLE IF EXISTS backup_2023;',
            'os_type': '通用',
            'aliases': '删表,DROP TABLE',
            'tips': '⚠️ 操作不可逆！删除前务必确认表名。如有外键引用会报错，需先处理关联表。',
        },
        {
            'cmd_name': 'JOIN',
            'name_cn': '多表连接查询',
            'function_desc': '将两个或多个表按照关联条件组合查询，是关系数据库的核心功能。',
            'syntax': 'SELECT 列 FROM 表A JOIN 表B ON 关联条件',
            'params_json': '[{"参数":"INNER JOIN","说明":"返回两个表都匹配的行（交集）","必填":"可选"},{"参数":"LEFT JOIN","说明":"返回左表所有行，右表无匹配时用 NULL","必填":"可选"},{"参数":"RIGHT JOIN","说明":"返回右表所有行，左表无匹配时用 NULL","必填":"可选"}]',
            'example_basic': 'SELECT u.name, o.order_date FROM users u JOIN orders o ON u.id = o.user_id;',
            'example_adv': 'SELECT u.name, COUNT(o.id) AS order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id ORDER BY order_count DESC;',
            'os_type': '通用',
            'aliases': '连接,JOIN,多表查询',
            'tips': 'INNER JOIN 是默认的连接类型。连接时表名起别名（如 users u）可以简化查询。连接列要有索引以提高性能。',
        },
        {
            'cmd_name': 'GROUP BY',
            'name_cn': '分组聚合',
            'function_desc': '将查询结果按指定列分组，配合聚合函数（COUNT/SUM/AVG/MAX/MIN）进行统计。',
            'syntax': 'SELECT 列, 聚合函数 FROM 表名 GROUP BY 列名',
            'params_json': '[{"参数":"GROUP BY 列","说明":"按哪些列分组","必填":"是"},{"参数":"HAVING","说明":"对分组结果进行筛选（类似 WHERE，但用于聚合后）","必填":"可选"}]',
            'example_basic': 'SELECT status, COUNT(*) FROM orders GROUP BY status;',
            'example_adv': 'SELECT user_id, SUM(amount) AS total, COUNT(*) AS cnt FROM orders GROUP BY user_id HAVING total > 1000 ORDER BY total DESC;',
            'os_type': '通用',
            'aliases': '分组,GROUP BY,聚合',
            'tips': 'SELECT 中非聚合列必须出现在 GROUP BY 中。WHERE 在分组前筛选，HAVING 在分组后筛选。',
        },
        {
            'cmd_name': 'ORDER BY',
            'name_cn': '排序',
            'function_desc': '对查询结果按指定列进行升序（ASC）或降序（DESC）排序。',
            'syntax': 'ORDER BY <列名> [ASC|DESC] [, ...]',
            'params_json': '[{"参数":"ASC","说明":"升序（从小到大，默认）","必填":"可选"},{"参数":"DESC","说明":"降序（从大到小）","必填":"可选"}]',
            'example_basic': 'SELECT * FROM users ORDER BY created_at DESC;',
            'example_adv': 'SELECT * FROM products ORDER BY category ASC, price DESC;',
            'os_type': '通用',
            'aliases': '排序,ORDER BY',
            'tips': '多列排序时先按第一列排序，相同再按第二列。排序字段有索引可以大幅提升性能。',
        },
        {
            'cmd_name': 'WHERE',
            'name_cn': '条件筛选',
            'function_desc': '在 SELECT/UPDATE/DELETE 中按条件筛选行，支持多种比较运算符和逻辑组合。',
            'syntax': 'WHERE <条件表达式>',
            'params_json': '[{"参数":"比较运算符","说明":"=, <>, >, <, >=, <=","必填":"可选"},{"参数":"LIKE","说明":"模糊匹配（% 代表任意字符）","必填":"可选"},{"参数":"IN","说明":"在指定列表中","必填":"可选"},{"参数":"BETWEEN","说明":"在指定范围内","必填":"可选"}]',
            'example_basic': 'SELECT * FROM users WHERE age >= 18;',
            'example_adv': 'SELECT * FROM products WHERE price BETWEEN 10 AND 100 AND category IN ("电子", "数码") AND name LIKE "%手机%";',
            'os_type': '通用',
            'aliases': '条件,WHERE,筛选',
            'tips': 'WHERE 中善用索引列可以大幅提高查询速度。LIKE "%keyword" 以 % 开头无法使用索引。',
        },
        {
            'cmd_name': 'LIMIT',
            'name_cn': '限制结果数量',
            'function_desc': '限制查询返回的行数，常用于分页和获取前 N 条记录。',
            'syntax': 'LIMIT <数量> [OFFSET <偏移量>]',
            'params_json': '[{"参数":"数量","说明":"返回的最大行数","必填":"是"},{"参数":"OFFSET","说明":"跳过前面多少行后开始返回","必填":"可选"}]',
            'example_basic': 'SELECT * FROM users LIMIT 10;',
            'example_adv': 'SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;  -- 第3页，每页10条',
            'os_type': '通用',
            'aliases': '限制,LIMIT,分页',
            'tips': '分页常用 LIMIT 10 OFFSET 0（第1页）、LIMIT 10 OFFSET 10（第2页）。大偏移量性能会下降，可用 WHERE id > 上次最大ID 替代。',
        },
        {
            'cmd_name': 'CREATE INDEX',
            'name_cn': '创建索引',
            'function_desc': '为表的列创建索引，加速查询速度。是数据库性能优化的核心手段。',
            'syntax': 'CREATE [UNIQUE] INDEX <索引名> ON <表名> (列名...)',
            'params_json': '[{"参数":"UNIQUE","说明":"创建唯一索引（值不能重复）","必填":"可选"},{"参数":"FULLTEXT","说明":"创建全文搜索索引","必填":"可选"}]',
            'example_basic': 'CREATE INDEX idx_email ON users(email);',
            'example_adv': 'CREATE INDEX idx_user_status ON users (status, created_at DESC);',
            'os_type': '通用',
            'aliases': '索引,CREATE INDEX,优化',
            'tips': '索引加多利少：查询变快但写入变慢。复合索引的列顺序重要，最左前缀原则。不要为每列都建索引。',
        },
        {
            'cmd_name': 'GRANT',
            'name_cn': '授予权限',
            'function_desc': '授予用户对数据库对象的访问权限，是 MySQL 权限管理的核心命令。',
            'syntax': 'GRANT <权限> ON <数据库.表> TO <用户> [IDENTIFIED BY 密码]',
            'params_json': '[{"参数":"权限","说明":"ALL PRIVILEGES/SELECT/INSERT/UPDATE/DELETE 等","必填":"是"},{"参数":"数据库.表","说明":"*.* 所有库所有表，dbname.* 指定库所有表","必填":"是"}]',
            'example_basic': 'GRANT SELECT ON mydb.* TO "readonly"@"localhost";',
            'example_adv': 'GRANT ALL PRIVILEGES ON mydb.* TO "app_user"@"192.168.1.%" IDENTIFIED BY "secure_password"; FLUSH PRIVILEGES;',
            'os_type': '通用',
            'aliases': '授权,GRANT,权限管理',
            'tips': '最小权限原则：只授予必要的权限。FLUSH PRIVILEGES 使权限立即生效。REVOKE 用于撤销权限。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 MySQL 命令')


def seed_sqlite(db):
    """插入 SQLite 命令数据"""
    cat_id = db.get_cat_id_by_name('数据库', 'SQLite')
    if not cat_id:
        print('[错误] 未找到 SQLite 分类')
        return

    commands = [
        {
            'cmd_name': '.open',
            'name_cn': '打开数据库文件',
            'function_desc': '在 sqlite3 命令行中打开或创建一个 SQLite 数据库文件。',
            'syntax': '.open <数据库文件路径>',
            'params_json': '[{"参数":"数据库文件路径","说明":"要打开/创建的 .db 或 .sqlite 文件路径","必填":"是"}]',
            'example_basic': '.open mydb.db',
            'example_adv': '.open /data/databases/company.db',
            'os_type': '通用',
            'aliases': '打开数据库,open',
            'tips': '如果文件不存在，.open 会自动创建。启动 sqlite3 时直接 sqlite3 mydb.db 也是打开数据库的方式。',
        },
        {
            'cmd_name': '.tables',
            'name_cn': '列出所有表',
            'function_desc': '显示当前数据库中所有用户创建的表和视图的名称列表。',
            'syntax': '.tables [匹配模式]',
            'params_json': '[{"参数":"匹配模式","说明":"可选，用 LIKE 风格的模式筛选表名（如 %user%）","必填":"可选"}]',
            'example_basic': '.tables',
            'example_adv': '.tables %user%',
            'os_type': '通用',
            'aliases': '表列表,tables,查看表',
            'tips': '.tables 只显示表名，想看建表语句用 .schema 表名。',
        },
        {
            'cmd_name': '.schema',
            'name_cn': '查看表结构',
            'function_desc': '显示表的 CREATE TABLE 语句，查看表结构定义。',
            'syntax': '.schema [表名]',
            'params_json': '[{"参数":"表名","说明":"要查看的表（可选，不填则显示所有表）","必填":"可选"}]',
            'example_basic': '.schema users',
            'example_adv': '.schema',
            'os_type': '通用',
            'aliases': '表结构,schema,建表语句',
            'tips': '不指定表名会显示所有表的建表语句。配合 .tables 查看有哪些表后再 .schema 具体表。',
        },
        {
            'cmd_name': '.headers on',
            'name_cn': '显示列名',
            'function_desc': '在查询结果中显示列名标题行，便于理解查询结果各列含义。',
            'syntax': '.headers on|off',
            'params_json': '[{"参数":"on","说明":"开启列名显示","必填":"是"},{"参数":"off","说明":"关闭列名显示","必填":"是"}]',
            'example_basic': '.headers on',
            'example_adv': '.headers on\nSELECT * FROM users;',
            'os_type': '通用',
            'aliases': '列名,headers,标题',
            'tips': '建议写入 ~/.sqliterc 配置文件，每次启动自动开启。',
        },
        {
            'cmd_name': '.mode column',
            'name_cn': '设置输出格式',
            'function_desc': '设置查询结果的显示格式，column 模式以对齐的列格式显示，最常用。',
            'syntax': '.mode <模式名>',
            'params_json': '[{"参数":"column","说明":"列对齐模式（最常用）","必填":"推荐"},{"参数":"csv","说明":"CSV 格式（逗号分隔）","必填":"可选"},{"参数":"json","说明":"JSON 格式（需要新版本 SQLite）","必填":"可选"},{"参数":"markdown","说明":"Markdown 表格格式","必填":"可选"}]',
            'example_basic': '.mode column',
            'example_adv': '.mode column\n.headers on\nSELECT * FROM users;',
            'os_type': '通用',
            'aliases': '输出格式,mode,显示模式',
            'tips': '配合 .headers on 和 .mode column 是最佳显示组合。.mode csv 适合导出数据到 Excel。',
        },
        {
            'cmd_name': '.import',
            'name_cn': '导入数据',
            'function_desc': '从 CSV/TSV 等文本文件导入数据到指定表。',
            'syntax': '.import <文件路径> <表名>',
            'params_json': '[{"参数":"文件路径","说明":"要导入的 CSV 文件路径","必填":"是"},{"参数":"表名","说明":"目标表名","必填":"是"}]',
            'example_basic': '.import data.csv users',
            'example_adv': '.mode csv\n.import /home/user/export.csv users',
            'os_type': '通用',
            'aliases': '导入数据,import,CSV导入',
            'tips': '导入前先用 .mode csv 设置格式。如果表不存在，.import 会以第一行作为列名自动创建表。',
        },
        {
            'cmd_name': '.output',
            'name_cn': '输出到文件',
            'function_desc': '将查询结果重定向输出到文件，而不是显示在屏幕上。',
            'syntax': '.output <文件名>',
            'params_json': '[{"参数":"文件名","说明":"输出目标文件路径","必填":"是"}]',
            'example_basic': '.output result.txt',
            'example_adv': '.output /tmp/export.csv\n.mode csv\nSELECT * FROM users;\n.output stdout',
            'os_type': '通用',
            'aliases': '输出文件,output,导出',
            'tips': '.output stdout 将输出重定向回终端。可以配合 .mode csv 导出数据到文件。',
        },
        {
            'cmd_name': '.dump',
            'name_cn': '导出数据库',
            'function_desc': '将整个数据库或指定表导出为 SQL 文本格式，可用于备份或迁移。',
            'syntax': '.dump [表名]',
            'params_json': '[{"参数":"表名","说明":"要导出的表（可选，不填则导出整个数据库）","必填":"可选"}]',
            'example_basic': '.dump',
            'example_adv': '.dump users > backup_users.sql',
            'os_type': '通用',
            'aliases': '导出,备份,dump',
            'tips': '.dump 生成的 SQL 可以直接用 .read 或 sqlite3 < backup.sql 恢复。',
        },
        {
            'cmd_name': '.read',
            'name_cn': '执行 SQL 脚本文件',
            'function_desc': '从文件中读取并执行 SQL 语句，常用于批量执行脚本或恢复备份。',
            'syntax': '.read <SQL文件路径>',
            'params_json': '[{"参数":"SQL文件路径","说明":"包含 SQL 语句的脚本文件","必填":"是"}]',
            'example_basic': '.read init.sql',
            'example_adv': '.read /home/user/backup/2024-01-01_dump.sql',
            'os_type': '通用',
            'aliases': '执行脚本,read,导入SQL',
            'tips': '.read 等同于 mysql 的 source 命令。也可以用 sqlite3 db.db < script.sql 执行外部脚本。',
        },
        {
            'cmd_name': '.quit',
            'name_cn': '退出 sqlite3',
            'function_desc': '退出 sqlite3 命令行工具，回到系统终端。',
            'syntax': '.quit',
            'params_json': '[]',
            'example_basic': '.quit',
            'example_adv': '.exit',
            'os_type': '通用',
            'aliases': '退出,quit,exit',
            'tips': '.exit 和 .quit 功能相同。也可以用 Ctrl+D 退出。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 SQLite 命令')


def seed_redis(db):
    """插入 Redis 命令数据"""
    cat_id = db.get_cat_id_by_name('数据库', 'Redis命令')
    if not cat_id:
        print('[错误] 未找到 Redis命令 分类')
        return

    commands = [
        {
            'cmd_name': 'SET',
            'name_cn': '设置键值',
            'function_desc': '设置指定 key 的值为 value，如果 key 已存在则覆盖。是 Redis 最基础的写操作。',
            'syntax': 'SET <key> <value> [NX|XX] [EX <秒>]',
            'params_json': '[{"参数":"NX","说明":"仅在 key 不存在时设置（类似 SETNX）","必填":"可选"},{"参数":"XX","说明":"仅在 key 已存在时更新","必填":"可选"},{"参数":"EX","说明":"设置过期时间（秒）","必填":"可选"}]',
            'example_basic': 'SET name "张三"',
            'example_adv': 'SET session:token "abc123" EX 3600 NX',
            'os_type': '通用',
            'aliases': '设置,写数据,SET',
            'tips': 'SET key value EX 10 NX 是分布式锁的经典实现。设置过期时间可以防止 key 永久占用内存。',
        },
        {
            'cmd_name': 'GET',
            'name_cn': '获取键值',
            'function_desc': '获取指定 key 的值。如果 key 不存在返回 nil。',
            'syntax': 'GET <key>',
            'params_json': '[{"参数":"key","说明":"要查询的键名","必填":"是"}]',
            'example_basic': 'GET name',
            'example_adv': 'GET session:token',
            'os_type': '通用',
            'aliases': '获取,读数据,GET',
            'tips': 'GET 只能用于字符串类型。如果 key 存的是其他类型（如 List、Hash），需要用对应的命令获取。',
        },
        {
            'cmd_name': 'DEL',
            'name_cn': '删除键',
            'function_desc': '删除一个或多个指定的 key，无论其数据类型如何。',
            'syntax': 'DEL <key> [key ...]',
            'params_json': '[{"参数":"key","说明":"要删除的键名，可以一次指定多个","必填":"是"}]',
            'example_basic': 'DEL name',
            'example_adv': 'DEL session:token cache:user:123 temp:data',
            'os_type': '通用',
            'aliases': '删除,DEL',
            'tips': 'DEL 返回被删除 key 的数量。删除不存在的 key 返回 0。UNLINK 是 DEL 的异步版本（不阻塞）。',
        },
        {
            'cmd_name': 'EXISTS',
            'name_cn': '检查键是否存在',
            'function_desc': '检查一个或多个 key 是否存在。返回存在的 key 数量。',
            'syntax': 'EXISTS <key> [key ...]',
            'params_json': '[{"参数":"key","说明":"要检查的键名","必填":"是"}]',
            'example_basic': 'EXISTS name',
            'example_adv': 'EXISTS user:123 email:456',
            'os_type': '通用',
            'aliases': '存在检查,EXISTS',
            'tips': '返回 1 表示存在，0 表示不存在。批量检查时返回存在的 key 总数。',
        },
        {
            'cmd_name': 'EXPIRE',
            'name_cn': '设置过期时间',
            'function_desc': '为已存在的 key 设置过期时间（秒），到期后 key 会被自动删除。',
            'syntax': 'EXPIRE <key> <秒数>',
            'params_json': '[{"参数":"秒数","说明":"多少秒后过期","必填":"是"}]',
            'example_basic': 'EXPIRE session:token 3600',
            'example_adv': 'SET captcha:code "1234" EX 300',
            'os_type': '通用',
            'aliases': '过期,TTL,EXPIRE',
            'tips': 'TTL 命令可以查看 key 的剩余存活时间。SET 命令可直接在设置时用 EX 参数指定过期时间。',
        },
        {
            'cmd_name': 'KEYS',
            'name_cn': '查找键',
            'function_desc': '按模式查找所有匹配的 key 名称。⚠️ 生产环境慎用，数据量大时会阻塞 Redis。',
            'syntax': 'KEYS <模式>',
            'params_json': '[{"参数":"模式","说明":"支持通配符：* 任意字符，? 单个字符，[ab] 字符集","必填":"是"}]',
            'example_basic': 'KEYS user:*',
            'example_adv': 'KEYS cache:*:v2',
            'os_type': '通用',
            'aliases': '查找键,KEYS,搜索',
            'tips': '⚠️ 生产环境不要用 KEYS，用 SCAN 替代（游标式迭代，不阻塞）。KEYS * 会返回所有 key。',
        },
        {
            'cmd_name': 'LPUSH',
            'name_cn': '列表左侧插入',
            'function_desc': '将一个或多个值插入到列表的头部（左侧）。如果 key 不存在则创建空列表。',
            'syntax': 'LPUSH <key> <value> [value ...]',
            'params_json': '[{"参数":"value","说明":"要插入的值，可一次插入多个","必填":"是"}]',
            'example_basic': 'LPUSH queue "task1"',
            'example_adv': 'LPUSH events:log "user_login" "page_view" "click_button"',
            'os_type': '通用',
            'aliases': '左插入,列表,LPUSH',
            'tips': 'RPUSH 从右侧插入。LLEN 查看列表长度。常用作消息队列或最新消息列表。',
        },
        {
            'cmd_name': 'LRANGE',
            'name_cn': '获取列表范围',
            'function_desc': '获取列表中指定范围内的元素。用于查看列表内容或分页。',
            'syntax': 'LRANGE <key> <起始索引> <结束索引>',
            'params_json': '[{"参数":"起始索引","说明":"0 = 第一个元素，-1 = 最后一个元素","必填":"是"},{"参数":"结束索引","说明":"包含此索引的元素","必填":"是"}]',
            'example_basic': 'LRANGE queue 0 -1',
            'example_adv': 'LRANGE messages 0 9',
            'os_type': '通用',
            'aliases': '列表查询,LRANGE',
            'tips': '索引从 0 开始，负数从尾部开始：-1 最后，-2 倒数第二。LRANGE list 0 -1 查看整个列表。',
        },
        {
            'cmd_name': 'SADD',
            'name_cn': '集合添加元素',
            'function_desc': '向集合中添加一个或多个元素，重复元素会被自动忽略。',
            'syntax': 'SADD <key> <member> [member ...]',
            'params_json': '[{"参数":"member","说明":"要添加的元素","必填":"是"}]',
            'example_basic': 'SADD tags "redis"',
            'example_adv': 'SADD user:1:tags "python" "redis" "docker"',
            'os_type': '通用',
            'aliases': '集合添加,SADD',
            'tips': '集合中的元素是唯一且无序的。SREM 删除元素。SMEMBERS 查看所有元素。SCARD 查看元素数量。',
        },
        {
            'cmd_name': 'SMEMBERS',
            'name_cn': '获取集合所有元素',
            'function_desc': '返回集合中的所有成员，常用于查看标签、用户分组等数据。',
            'syntax': 'SMEMBERS <key>',
            'params_json': '[{"参数":"key","说明":"集合的键名","必填":"是"}]',
            'example_basic': 'SMEMBERS tags',
            'example_adv': 'SMEMBERS user:1:favorites',
            'os_type': '通用',
            'aliases': '集合查询,SMEMBERS',
            'tips': '集合大小较小时可用 SMEMBERS，大数据集建议用 SSCAN 迭代（避免阻塞）。',
        },
        {
            'cmd_name': 'HSET',
            'name_cn': '设置哈希字段',
            'function_desc': '为哈希类型 key 设置一个或多个字段的值。适合存储对象数据。',
            'syntax': 'HSET <key> <field> <value> [field value ...]',
            'params_json': '[{"参数":"field","说明":"字段名","必填":"是"},{"参数":"value","说明":"字段的值","必填":"是"}]',
            'example_basic': 'HSET user:1 name "张三"',
            'example_adv': 'HSET user:100 name "张三" age 28 email "zhang@example.com" city "北京"',
            'os_type': '通用',
            'aliases': '哈希设置,对象,HSET',
            'tips': 'HGET 获取单个字段，HGETALL 获取所有字段。哈希适合存储和更新对象的部分字段。',
        },
        {
            'cmd_name': 'HGETALL',
            'name_cn': '获取哈希所有字段',
            'function_desc': '返回哈希类型 key 的所有字段和值，以 field1 value1 field2 value2 ... 交替排列。',
            'syntax': 'HGETALL <key>',
            'params_json': '[{"参数":"key","说明":"哈希的键名","必填":"是"}]',
            'example_basic': 'HGETALL user:1',
            'example_adv': 'HGETALL product:10001',
            'os_type': '通用',
            'aliases': '哈希查询,对象查询,HGETALL',
            'tips': '大哈希慎用 HGETALL（会返回所有数据），推荐用 HSCAN 或只获取需要的字段（HGET/HMGET）。',
        },
        {
            'cmd_name': 'PING',
            'name_cn': '测试连接',
            'function_desc': '测试 Redis 服务器是否正常运行。服务器正常时返回 PONG。',
            'syntax': 'PING [消息]',
            'params_json': '[{"参数":"消息","说明":"可选，指定返回消息","必填":"可选"}]',
            'example_basic': 'PING',
            'example_adv': 'PING "hello"',
            'os_type': '通用',
            'aliases': '连接测试,PING,心跳',
            'tips': 'PING 主要用于客户端检查连接状态和延迟。带参数时服务器会返回该参数。',
        },
        {
            'cmd_name': 'FLUSHALL',
            'name_cn': '清空所有数据库',
            'function_desc': '删除 Redis 服务器上所有数据库中的所有 key。⚠️ 生产环境极度危险！',
            'syntax': 'FLUSHALL [ASYNC]',
            'params_json': '[{"参数":"ASYNC","说明":"异步执行，不阻塞 Redis","必填":"可选"}]',
            'example_basic': 'FLUSHALL',
            'example_adv': 'FLUSHALL ASYNC',
            'os_type': '通用',
            'aliases': '清空,FLUSHALL,重置',
            'tips': '⚠️ 会删除所有数据！FLUSHDB 只清空当前数据库。建议加 ASYNC 参数避免阻塞。',
        },
        {
            'cmd_name': 'INFO',
            'name_cn': '查看服务器信息',
            'function_desc': '返回 Redis 服务器的各种统计信息和配置，包括内存使用、连接数、命中率等。',
            'syntax': 'INFO [section]',
            'params_json': '[{"参数":"section","说明":"指定信息类别：server/clients/memory/stats/replication 等","必填":"可选"}]',
            'example_basic': 'INFO',
            'example_adv': 'INFO memory',
            'os_type': '通用',
            'aliases': '服务器信息,INFO,状态',
            'tips': 'INFO memory 查看内存使用情况；INFO stats 查看命中率；INFO keyspace 查看各数据库 key 数量。',
        },
    ]

    for cmd in commands:
        db.add_command(category_id=cat_id, **cmd)
        print(f'  ✓ {cmd["cmd_name"]} — {cmd["name_cn"]}')

    print(f'  → 共插入 {len(commands)} 条 Redis 命令')


def main():
    db_path = os.path.join(os.path.expanduser('~'), '.code-quickref', 'data.db')

    print('=' * 60)
    print('  命令行种子数据生成脚本')
    print(f'  数据库路径: {db_path}')
    print('=' * 60)

    # 自动执行，无需确认

    # 初始化 DB
    db = DBManager(db_path=db_path)
    db.init_db()
    print(f'\n[✓] 数据库初始化完成')

    total = 0

    print('\n─── Git 命令 ───')
    seed_git(db)
    total += 15

    print('\n─── Linux 终端 ───')
    seed_linux(db)
    total += 21

    print('\n─── Docker ───')
    seed_docker(db)
    total += 15

    print('\n─── CMD (Windows) ───')
    seed_cmd_windows(db)
    total += 16

    print('\n─── PowerShell ───')
    seed_powershell(db)
    total += 10

    print('\n─── MySQL ───')
    seed_mysql(db)
    total += 15

    print('\n─── SQLite ───')
    seed_sqlite(db)
    total += 10

    print('\n─── Redis ───')
    seed_redis(db)
    total += 15

    db.close()

    print('\n' + '=' * 60)
    print(f'  ✅ 完成！共插入 {total} 条命令数据')
    print('=' * 60)


if __name__ == '__main__':
    main()
