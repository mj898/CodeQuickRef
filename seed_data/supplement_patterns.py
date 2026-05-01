#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
种子补充脚本：为已有分类补充模式/标记条目，并为「其他」下新建子分类
总计 >= +50 条

用法：python seed_data/supplement_patterns.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

DB_PATH = os.path.join(os.path.expanduser('~'), '.code-quickref', 'data.db')


# ============================================================
# 正则表达式 补充（+15 条）
# ============================================================
REGEX_PATTERNS = [
    {
        "title": "正向先行断言 (?=)",
        "language": "正则表达式",
        "pattern_text": "(?=...)",
        "parsed_table": '[{"段":"(?=pattern)","含义":"正向先行断言，后面必须紧跟 pattern，但不消耗字符"}]',
        "code_block": "\\\\d+(?=px)    # 匹配后面有 px 的数字，如 '100px' 中的 '100'\\n\\\\w+(?=\\\\s)   # 匹配后面是空白的单词",
        "line_by_line": '[{"代码":"\\\\\\\\d+(?=px)","说明":"匹配数字后紧跟 px 的部分，不包含 px"}]',
        "syntax_note": "断言不消耗字符，不包含在匹配结果中。常用于提取特定上下文前的值，如价格、尺寸等",
        "runnable_example": "import re\\ntext = 'width: 100px; height: 200px'\\nprint(re.findall(r'\\\\d+(?=px)', text))  # ['100', '200']",
        "common_errors": '[{"报错":"匹配结果包含多余字符","解决办法":"确认未在断言外捕获多余内容"}]',
        "aliases": "先行断言,lookahead,正向预查",
    },
    {
        "title": "负向先行断言 (?!)",
        "language": "正则表达式",
        "pattern_text": "(?!...)",
        "parsed_table": '[{"段":"(?!pattern)","含义":"负向先行断言，后面不能紧跟 pattern"}]',
        "code_block": "\\\\d+(?!px)   # 匹配后面没有 px 的数字\\nfoo(?!bar)   # 匹配 foo 但不匹配 foobar",
        "line_by_line": '[{"代码":"\\\\\\\\d+(?!px)","说明":"匹配数字，但后面不能是 px"}]',
        "syntax_note": "与 (?=) 相反，断言后面不出现某模式。常用来排除特定后缀或前缀的情况",
        "runnable_example": "import re\\nprint(re.findall(r'\\\\d+(?!px)', '100px 200pt 50em'))  # ['10', '0', '200', '50']",
        "common_errors": '[{"报错":"排除了不该排除的内容","解决办法":"检查断言的位置和模式是否正确"}]',
        "aliases": "负向先行,否定预查,negative lookahead",
    },
    {
        "title": "正向后行断言 (?<=)",
        "language": "正则表达式",
        "pattern_text": "(?<=...)",
        "parsed_table": '[{"段":"(?<=pattern)","含义":"正向后行断言，前面必须紧跟 pattern"}]',
        "code_block": "(?<=\\\\$) \\\\d+  # 匹配前面有 $ 的数字\\n(?<=@)\\\\w+    # 匹配 @ 后面的用户名",
        "line_by_line": '[{"代码":"(?<=\\\\\\\$)\\\\\\\\d+","说明":"匹配前面有 $ 的数字"}]',
        "syntax_note": "后行断言 (?<=) 要求前面的内容匹配指定模式。部分引擎（如 JavaScript 早期版本）不支持。Python 支持但要求定长模式",
        "runnable_example": "import re\\nprint(re.findall(r'(?<=\\\\$)\\\\d+', 'price: $50, total: $120'))  # ['50', '120']",
        "common_errors": '[{"报错":"look-behind requires fixed-width pattern","解决办法":"后行断言中不能用 + * 等不定长量词，改用定长写法"}]',
        "aliases": "后行断言,后顾,lookbehind,正向向后",
    },
    {
        "title": "负向后行断言 (?<!)",
        "language": "正则表达式",
        "pattern_text": "(?<!...)",
        "parsed_table": '[{"段":"(?<!pattern)","含义":"负向后行断言，前面不能紧跟 pattern"}]',
        "code_block": "(?<![\\\\d.])\\\\d+  # 匹配前面不是数字或点号的数字\\n(?<!\\\\w)@\\\\w+   # 匹配前面不是单词字符的 @用户名",
        "line_by_line": '[{"代码":"(?<!...)\\\\d+","说明":"匹配前面不满足条件的数字"}]',
        "syntax_note": "用于排除特定前缀的场景。注意：后行断言在 Python re 模块中要求定长模式，不支持 + * {n,} 等变长量词",
        "runnable_example": "import re\\nprint(re.findall(r'(?<![\\\\d.])\\\\d+', 'abc123 3.14 v2.0'))  # ['123', '14', '0']",
        "common_errors": '[{"报错":"Variable length lookbehind not supported","解决办法":"改用定长模式或分组捕获替代"}]',
        "aliases": "负向后行,否定后顾,negative lookbehind",
    },
    {
        "title": "非捕获分组 (?:)",
        "language": "正则表达式",
        "pattern_text": "(?:...)",
        "parsed_table": '[{"段":"(?:pattern)","含义":"仅分组不捕获，不占用组编号"}]',
        "code_block": "(?:\\\\d+)\\\\s*[a-z]+  # 分组但不捕获数字\\n(?:https?|ftp):\\\\/\\\\/   # 匹配协议头但不单独捕获",
        "line_by_line": '[{"代码":"(?:...)","说明":"非捕获分组，仅用于分组逻辑"}]',
        "syntax_note": "普通括号 () 会捕获匹配内容并占用组编号，非捕获 (?:) 只用于分组逻辑（如应用量词或 | 选择），提升性能并避免编号混乱",
        "runnable_example": "import re\\nm = re.search(r'(?:\\\\d{3}-)?\\\\d{8}', 'Tel: 010-12345678')\\nprint(m.group(0))  # '010-12345678'\\nprint(m.groups())  # () ─ 无捕获组",
        "common_errors": '[{"报错":"想引用组但总是 None","解决办法":"确认是否用了 (?:) 而非 () 导致没有捕获"}]',
        "aliases": "非捕获,non-capturing group,分组不捕获",
    },
    {
        "title": "原子分组 (?>)",
        "language": "正则表达式",
        "pattern_text": "(?>...)",
        "parsed_table": '[{"段":"(?>pattern)","含义":"原子分组，分组内匹配后放弃回溯"}]',
        "code_block": "(?>\\\\d+)[a-z]   # 数字匹配后不回溯，如果后面无字母则整体失败\\n(?>.*?)end     # 原子分组中的非贪婪",
        "line_by_line": '[{"代码":"(?>...)","说明":"原子分组，禁用回溯"}]',
        "syntax_note": "原子分组内的匹配一旦完成，不会因后续匹配失败而回溯重试。可大幅提升性能，防止灾难性回溯。Python 中 (?>...) 自 3.11 起支持（import regex 模块更早支持）",
        "runnable_example": "import regex\\n# 防止灾难性回溯\\npattern = r'(?>\\\\d+)x'\\nprint(regex.findall(pattern, '123x 456y'))  # ['123x']",
        "common_errors": '[{"报错":"Python re 不支持 (?>)","解决办法":"使用 regex 模块（pip install regex），或手动优化避免回溯"}]',
        "aliases": "原子组,atomic group,禁止回溯,possessive",
    },
    {
        "title": "递归匹配 (?R)",
        "language": "正则表达式",
        "pattern_text": "(?R)",
        "parsed_table": '[{"段":"(?R)","含义":"递归整个表达式"}]',
        "code_block": "\\\\((?:[^()]|(?R))*\\\\)   # 匹配平衡的括号\\((?:(?>[^()]+)|(?R))*\\)     # 高效版本",
        "line_by_line": '[{"代码":"(?R)","说明":"递归到整个模式开头重新匹配"}]',
        "syntax_note": "递归匹配用于处理嵌套结构（如括号、HTML 标签）。(?R) 表示递归整个表达式；(?1) 表示递归到第 1 组。Python re 不支持，需用 regex 模块或 pyparsing",
        "runnable_example": "import regex\\npattern = r'\\\\((?:[^()]|(?R))*\\\\)'\\ntext = 'func(a, b(c, d), e)'\\nprint(regex.findall(pattern, text))  # ['(a, b(c, d), e)']",
        "common_errors": '[{"报错":"Python re 模块不支持递归","解决办法":"安装 regex 模块（pip install regex）"}]',
        "aliases": "递归,recursion,nested,嵌套匹配,(?R)",
    },
    {
        "title": "条件匹配 (?(1)...)",
        "language": "正则表达式",
        "pattern_text": "(?(id)yes|no)",
        "parsed_table": '[{"段":"?(id)yes|no","含义":"如果第 id 组存在则匹配 yes，否则匹配 no"}]',
        "code_block": "(a)?(?(1)b|c)   # 如果有 a 则匹配 b，否则匹配 c\\n(\\\\d+)?(?(1)-\\\\d+|N/A)  # 数字存在则匹配 -数字，否则 N/A",
        "line_by_line": '[{"代码":"?(1)yes","说明":"条件：组 1 存在时匹配 yes"},{"代码":"|no","说明":"否则匹配 no"}]',
        "syntax_note": "条件匹配根据之前的分组是否参与匹配来决定后续分支。常用于可选前缀/后缀场景。Python re 不支持，regex 模块支持",
        "runnable_example": "import regex\\npattern = r'(a)?(?(1)b|c)'\\nprint(regex.match(pattern, 'ab'))   # match 'ab'\\nprint(regex.match(pattern, 'c'))    # match 'c'",
        "common_errors": '[{"报错":"Python re 不支持条件匹配","解决办法":"改用 regex 模块或改写为多步匹配"}]',
        "aliases": "条件,conditional,分支,?(1)",
    },
    {
        "title": "命名分组 (?P<name>)",
        "language": "正则表达式",
        "pattern_text": "(?P<name>...)",
        "parsed_table": '[{"段":"(?P<name>...)","含义":"命名捕获组，用名称代替数字编号引用"}]',
        "code_block": "(?P<year>\\\\d{4})-(?P<month>\\\\d{2})-(?P<day>\\\\d{2})  # 命名分组匹配日期",
        "line_by_line": '[{"代码":"(?P<year>\\\\\\\d{4})","说明":"year 组：匹配 4 位数字"}]',
        "syntax_note": "命名分组可以同时用名称和数字编号引用。Python 语法为 (?P<name>...)，其他语言风格不同：JavaScript (?<name>...)、.NET (?<name>...)",
        "runnable_example": "import re\\nm = re.search(r'(?P<year>\\\\d{4})-(?P<month>\\\\d{2})', '2024-03-15')\\nprint(m.group('year'))   # '2024'\\nprint(m.group(1))        # '2024'",
        "common_errors": '[{"报错":"不同引擎命名分组语法不同","解决办法":"Python 用 (?P<name>)，PCRE/JS 用 (?<name>)"}]',
        "aliases": "命名捕获,named group,命名组,(?P<name>)",
    },
    {
        "title": "反向引用 \\1 和 \\k<name>",
        "language": "正则表达式",
        "pattern_text": "\\\\1 \\\\k<name>",
        "parsed_table": '[{"段":"\\\1","含义":"引用第 1 个捕获组匹配的内容"},{"段":"\\\k<name>","含义":"引用命名捕获组匹配的内容"}]',
        "code_block": "([ab])\\\\1        # 匹配 aa 或 bb（重复同一字符）\\n(?P<word>\\\\w+)\\\\s+\\\\k<word>  # 匹配重复单词如 'hello hello'",
        "line_by_line": '[{"代码":"(.)\\\\1","说明":"匹配连续相同的两个字符"}]',
        "syntax_note": "反向引用匹配与之前捕获组相同的内容，而非相同的模式。\\\\1-\\\\9 是数字反向引用；\\\\k<name> 或 (?P=name) 是命名反向引用",
        "runnable_example": "import re\\nprint(re.findall(r'([ab])\\\\1', 'aa bb ab'))     # ['a', 'b']\\nprint(re.findall(r'\\\\b(\\\\w+)\\\\s+\\\\1\\\\b', 'hello hello world'))  # ['hello']",
        "common_errors": '[{"报错":"\\\\1 被解析为八进制转义","解决办法":"Python 中用 raw string r\\\"...\\\" 避免歧义"}]',
        "aliases": "反向引用,backreference,后向引用,\\k<name>",
    },
    {
        "title": "Unicode 属性 \\p{N}",
        "language": "正则表达式",
        "pattern_text": "\\\\p{}",
        "parsed_table": '[{"段":"\\\p{N}","含义":"匹配任意 Unicode 数字字符"},{"段":"\\\p{L}","含义":"匹配任意字母"},{"段":"\\\p{Sc}","含义":"匹配货币符号"}]',
        "code_block": "\\\\p{N}+        # 匹配任意语言中的数字\\n\\\\p{Han}        # 匹配汉字\\n\\\\p{Lu}         # 匹配大写字母",
        "line_by_line": '[{"代码":"\\\\p{N}","说明":"Unicode 数字类别"},{"代码":"\\\\p{Han}","说明":"CJK 统一表意文字"}]',
        "syntax_note": "\\\\p{} 按 Unicode 属性匹配字符，支持大类（L/N/P/S/Z/C）和具体属性（Han/Arabic/Greek）。Python re 不支持，regex 模块或 PyPI regex 支持",
        "runnable_example": "import regex\\nprint(regex.findall(r'\\\\p{Han}+', 'Hello 世界 123'))  # ['世界']\\nprint(regex.findall(r'\\\\p{N}+', '123 ٤٥٦ 三'))  # ['123', '٤٥٦']",
        "common_errors": '[{"报错":"bad character property \\p{}","解决办法":"Python re 不支持 \\p{}，改用 regex 模块或 \\uXXXX 范围"}]',
        "aliases": "Unicode属性,unicode property,脚本,Script,\\p{}",
    },
    {
        "title": "惰性匹配 *? +? ??",
        "language": "正则表达式",
        "pattern_text": "*? +? ?? {n,m}?",
        "parsed_table": '[{"段":"*?","含义":"零次或多次（非贪婪，尽可能少）"},{"段":"+?","含义":"一次或多次（非贪婪）"},{"段":"??","含义":"零次或一次（优先不匹配）"}]',
        "code_block": "<.+?>         # 非贪婪匹配 HTML 标签\\n\\\\w+?          # 非贪婪单词（一次就停）\\na.*?b          # a 开头 b 结尾的最短匹配",
        "line_by_line": '[{"代码":"*?","说明":"非贪婪零次或多次"},{"代码":"+?","说明":"非贪婪一次或多次"}]',
        "syntax_note": "默认量词是贪婪的（尽可能多匹配）。在量词后加 ? 变为惰性/非贪婪（尽可能少匹配）。常用于 HTML 解析、日志提取等场景",
        "runnable_example": "import re\\ntext = '<div>hello</div><p>world</p>'\\nprint(re.findall(r'<.+?>', text))   # ['<div>', '</div>', '<p>', '</p>']\\nprint(re.findall(r'<.+>', text))    # ['<div>hello</div><p>world</p>']",
        "common_errors": '[{"报错":"非贪婪还是匹配太多","解决办法":"检查是否忘了加 ?，或改用更精确的字符组如 [^>]+"}]',
        "aliases": "非贪婪,惰性,lazy,non-greedy,reluctant",
    },
    {
        "title": "占有量词 *+ ++",
        "language": "正则表达式",
        "pattern_text": "*+ ++ ?+",
        "parsed_table": '[{"段":"*+","含义":"占有零次或多次，不回溯"},{"段":"++","含义":"占有一次或多次，不回溯"}]',
        "code_block": "\\\\w++ [a-z]   # 单词字符占有匹配后不回溯\\n\\\\d++x         # 数字占有匹配，如果后面没有 x 立即失败不回溯",
        "line_by_line": '[{"代码":"*+","说明":"占有量词，匹配后不放弃字符"}]',
        "syntax_note": "占有量词在匹配完成后不再释放字符给后续模式回溯尝试。效果类似 (?>...) 原子分组。可防止灾难性回溯，提高性能。Python re 不支持，regex 模块支持",
        "runnable_example": "import regex\\ntext = '123x 456'\\n# 占有量词版本\\nprint(regex.findall(r'\\\\d++x', text))  # ['123x']\\n# 普通量词可能灾难性回溯\\nprint(regex.findall(r'\\\\d+x', text))   # ['123x']",
        "common_errors": '[{"报错":"不支持占有量词","解决办法":"改用原子分组 (?>...) 达到相同效果"}]',
        "aliases": "占有量词,possessive,不回溯,atomic",
    },
    {
        "title": "行内模式 (?im)",
        "language": "正则表达式",
        "pattern_text": "(?im) (?s) (?x)",
        "parsed_table": '[{"段":"(?i)","含义":"启用忽略大小写"},{"段":"(?m)","含义":"启用多行模式"},{"段":"(?s)","含义":"启用 DOTALL"},{"段":"(?x)","含义":"启用宽松模式（忽略空白和注释）"}]',
        "code_block": "(?i)hello          # 不区分大小写的 hello\\n(?m)^\\\\w+           # 多行模式下每行开头\\n(?x)                # 宽松模式，可加注释\\n  \\\\d{3}  -  \\\\d{4}  # 匹配电话号码",
        "line_by_line": '[{"代码":"(?im)","说明":"行内模式开关"},{"代码":"(?-i)","说明":"关闭忽略大小写"}]',
        "syntax_note": "行内模式修饰符可在表达式中间开关。格式为 (?imsx) 启用，(?-imsx) 禁用。影响修饰符之后的部分。可局部控制不同区域的匹配行为",
        "runnable_example": "import re\\nprint(re.findall(r'(?i)hello', 'Hello HELLO hello'))  # ['Hello', 'HELLO', 'hello']\\nprint(re.findall(r'(?m)^\\\\d+', '123\\\\n456\\\\n789'))  # ['123', '456', '789']",
        "common_errors": '[{"报错":"(?i) 放在末尾不生效","解决办法":"(?i) 只影响其后的模式，放在开头或需要的位置前"}]',
        "aliases": "内联修饰符,inline flag,模式修饰符,(?i)(?m)",
    },
    {
        "title": "平衡组 (?<name>-dep)",
        "language": "正则表达式",
        "pattern_text": "(?<name>-dep)",
        "parsed_table": '[{"段":"(?<name>)","含义":"入栈：将当前内容压入 name 堆栈"},{"段":"(<-name>)","含义":"出栈：弹出堆栈顶部元素"}]',
        "code_block": "(?<open>\\\\)  # 遇到 ( 入栈 open\\n(?<-open>\\\\))  # 遇到 ) 出栈 open",
        "line_by_line": '[{"代码":"(?<open>)","说明":"压栈操作"},{"代码":"(?<-open>)","说明":"弹栈操作"}]',
        "syntax_note": "平衡组是 .NET 正则引擎的独特特性，用于匹配成对嵌套结构（如括号、引号）。Python 原生 re 不支持，regex 模块也不直接支持平衡组语法，需用递归 (?R) 替代",
        "runnable_example": "# .NET 示例（C#）\\n# string pattern = @\\(\\\"(?:\\\"\\\"|[^\\\"])*\\\"|(?<open>\\()|(?<-open>\\)|(?:[^()]|(?<error>)))+\\\";\\n# Python 替代用递归\\nimport regex\\npattern = r'\\\\((?:[^()]|(?R))*\\\\)'\\nprint(regex.findall(pattern, 'f(a, b(c), d)'))  # ['(a, b(c), d)']",
        "common_errors": '[{"报错":"Python 不支持平衡组","解决办法":"用递归匹配 (?R) 或 pyparsing 库替代"}]',
        "aliases": "平衡组,balanced group,堆栈,stack,.NET regex",
    },
]

# ============================================================
# Markdown 补充（+8 条）
# ============================================================
MARKDOWN_PATTERNS = [
    {
        "title": "脚注",
        "language": "Markdown",
        "pattern_text": "[^1] [^1]: ...",
        "parsed_table": '[{"段":"[^1]","含义":"脚注引用标记"},{"段":"[^1]: 内容","含义":"脚注定义（通常在文档末尾）"}]',
        "code_block": "这是一段文字[^1]，需要补充说明。\\n\\n[^1]: 这里是脚注的详细内容，可以跨行写。",
        "line_by_line": '[{"代码":"[^1]","说明":"引用编号为 1 的脚注"},{"代码":"[^1]: 内容","说明":"在底部定义脚注内容"}]',
        "syntax_note": "脚注引用 [^n] 和脚注定义 [^n]: 配对使用。数字可任意但不重复。定义可放在文档末尾任意位置。部分渲染器（如 GitHub）不支持脚注",
        "runnable_example": "Markdown 是一种轻量级标记语言[^md]。\\n\\n[^md]: 由 John Gruber 于 2004 年创建。",
        "common_errors": '[{"报错":"脚注不显示","解决办法":"确认渲染器是否支持脚注（Pandoc、GitLab 支持，GitHub 不支持）"}]',
        "aliases": "脚注,footnote,注释,引用",
    },
    {
        "title": "上标和下标",
        "language": "Markdown",
        "pattern_text": "^ ~",
        "parsed_table": '[{"段":"^上标^","含义":"上标文字（Pandoc 扩展）"},{"段":"~下标~","含义":"下标文字（Pandoc 扩展）"}]',
        "code_block": "水的化学式 H~2~O\\n面积单位 m^2^\\n引用编号 [^1]",
        "line_by_line": '[{"代码":"H~2~O","说明":"下标 2"},{"代码":"m^2^","说明":"上标 2"}]',
        "syntax_note": "上标 ^...^ 和下标 ~...~ 是 Pandoc/Markdown Extra 扩展，标准 Markdown 不支持。替代方案：HTML 标签 <sup> 和 <sub>",
        "runnable_example": "爱因斯坦的质能方程 E=mc^2^ 用 Markdown 表示为 E=mc^2^\\n\\n或者用 HTML：E=mc<sup>2</sup>",
        "common_errors": '[{"报错":"^ 和 ~ 显示为普通字符","解决办法":"改用 HTML <sup> 和 <sub> 标签"}]',
        "aliases": "上标,下标,superscript,subscript,^ ~",
    },
    {
        "title": "数学公式 $",
        "language": "Markdown",
        "pattern_text": "$ ... $ 和 $$ ... $$",
        "parsed_table": '[{"段":"$公式$","含义":"行内数学公式"},{"段":"$$公式$$","含义":"独立显示的数学公式（块级）"}]',
        "code_block": "行内公式：$E = mc^2$\\n\\n块级公式：\\n$$\\n\\\\int_a^b f(x)\\\\,dx\\n$$",
        "line_by_line": '[{"代码":"$公式$","说明":"行内 LaTeX 公式"},{"代码":"$$公式$$","说明":"块级 LaTeX 公式（居中显示）"}]',
        "syntax_note": "数学公式用 $...$（行内）或 $$...$$（块级）包裹，支持 LaTeX 语法。需要渲染器支持（如 MathJax、KaTeX）。GitHub 支持 $$ 块级数学",
        "runnable_example": "欧拉公式：$e^{i\\\\pi} + 1 = 0$\\n\\n$$\\n\\\\sum_{n=1}^{\\\\infty} \\\\frac{1}{n^2} = \\\\frac{\\\\pi^2}{6}\\n$$",
        "common_errors": '[{"报错":"公式渲染为纯文本","解决办法":"确保页面引入了 MathJax 或 KaTeX 库"}]',
        "aliases": "数学公式,LaTeX,MathJax,KaTeX,公式",
    },
    {
        "title": "Mermaid 流程图",
        "language": "Markdown",
        "pattern_text": "```mermaid ... ```",
        "parsed_table": '[{"段":"```mermaid","含义":"Mermaid 图表代码块起始"},{"段":"graph TD","含义":"流向图（Top-Down）"},{"段":"-->","含义":"箭头连接"}]',
        "code_block": "```mermaid\\ngraph TD\\n    A[开始] --> B{判断}\\n    B -->|是| C[处理]\\n    B -->|否| D[结束]\\n```",
        "line_by_line": '[{"代码":"```mermaid","说明":"Mermaid 代码块开始"},{"代码":"graph TD","说明":"自上而下的流向图"},{"代码":"A[文本]","说明":"带标签的节点"}]',
        "syntax_note": "Mermaid 支持流程图 (graph)、时序图 (sequenceDiagram)、类图 (classDiagram)、饼图 (pie) 等。需要在渲染器中启用 Mermaid 支持",
        "runnable_example": "```mermaid\\nsequenceDiagram\\n    Alice->>John: 你好 John\\n    John-->>Alice: 你好 Alice\\n    Alice->>John: 你怎么样？\\n    John-->>Alice: 我很好！\\n```",
        "common_errors": '[{"报错":"图表显示空白","解决办法":"确认渲染器支持 Mermaid，或检查语法错误"}]',
        "aliases": "流程图,时序图,mermaid,chart,图表",
    },
    {
        "title": "定义列表",
        "language": "Markdown",
        "pattern_text": "术语\\n: 定义",
        "parsed_table": '[{"段":"术语","含义":"被定义的词汇/术语"},{"段":": 定义","含义":"术语的解释说明"}]',
        "code_block": "HTML\\n: 超文本标记语言（HyperText Markup Language）\\n\\nCSS\\n: 层叠样式表（Cascading Style Sheets）\\n: 用于控制网页布局和外观",
        "line_by_line": '[{"代码":"术语","说明":"第一行：术语名称"},{"代码":": 定义","说明":"缩进的定义内容，可多个"}]',
        "syntax_note": "定义列表是 Markdown Extra / Pandoc 扩展，标准 Markdown 不支持。格式：术语独占一行，: 定义 缩进写在下一行，一个术语可有多个定义",
        "runnable_example": "Python\\n: 一种解释型、面向对象的高级编程语言\\n: 以简洁和可读性著称\\n\\nPEP\\n: Python Enhancement Proposal\\n: Python 增强建议书",
        "common_errors": '[{"报错":"定义列表显示为普通文本","解决办法":"确认渲染器支持定义列表扩展，或改用 HTML <dl> 标签"}]',
        "aliases": "定义列表,definition list,dl,术语",
    },
    {
        "title": "标记高亮 == ==",
        "language": "Markdown",
        "pattern_text": "==...==",
        "parsed_table": '[{"段":"==文字==","含义":"高亮标记（mark/highlight）"}]',
        "code_block": "这是 ==需要重点注意== 的内容\\n请 ==务必== 在部署前检查",
        "line_by_line": '[{"代码":"==文字==","说明":"高亮/标记文本"}]',
        "syntax_note": "==高亮== 是 Markdown 扩展（源自 CriticMarkup，后被 Pandoc/GFM 部分支持）。实际标准 Markdown 不支持。替代方案：用 <mark> 标签",
        "runnable_example": "请 ==务必== 在提交前运行测试！\\n\\n如果无法使用 ==，可用 HTML：<mark>务必</mark>",
        "common_errors": '[{"报错":"== 显示为普通文本","解决办法":"改用 HTML <mark>标签</mark> 实现高亮"}]',
        "aliases": "高亮,highlight,标记,mark,==,批评标记",
    },
    {
        "title": "自定义容器",
        "language": "Markdown",
        "pattern_text": "::: ... :::",
        "parsed_table": '[{"段":"::: type","含义":"自定义容器开始"},{"段":":::","含义":"自定义容器结束"}]',
        "code_block": "::: tip\\n这是一个提示信息\\n:::\\n\\n::: warning\\n警告：请注意！\\n:::\\n\\n::: danger\\n危险操作！\\n:::",
        "line_by_line": '[{"代码":"::: tip","说明":"提示类型容器"},{"代码":"::: warning","说明":"警告类型容器"},{"代码":"::: danger","说明":"危险类型容器"}]',
        "syntax_note": "自定义容器在 VuePress / Vitepress 等文档框架中广泛使用。支持 tip/warning/danger/details 等类型。不是标准 Markdown，需框架支持",
        "runnable_example": "::: tip 温馨提示\\n使用 `pip install` 安装依赖\\n:::\\n\\n::: warning\\n请确保 Python 版本 >= 3.8\\n:::",
        "common_errors": '[{"报错":"容器不渲染","解决办法":"确认使用 Markdown 框架是否支持自定义容器（VuePress、MkDocs Material 等支持）"}]',
        "aliases": "自定义容器,custom container,admonition,提示框,VuePress",
    },
    {
        "title": "锚点和目录生成",
        "language": "Markdown",
        "pattern_text": "[TOC] 和 {#id}",
        "parsed_table": '[{"段":"[TOC]","含义":"自动生成目录（Table of Contents）"},{"段":"{#自定义id}","含义":"为标题指定自定义锚点 ID"}]',
        "code_block": "[TOC]\\n\\n## 简介 {#intro}\\n\\n## 安装指南 {#install}\\n\\n## API 参考 {#api}",
        "line_by_line": '[{"代码":"[TOC]","说明":"插入目录"},{"代码":"{#intro}","说明":"自定义锚点 ID"}]',
        "syntax_note": "[TOC] 是部分平台的扩展（GitLab、Typora、VuePress）。默认 Markdown 中每个标题自动生成锚点（基于标题文本），可用 {#自定义ID} 覆盖锚点名",
        "runnable_example": "[TOC]\\n\\n# 项目文档\\n\\n## 快速开始 {#quickstart}\\n\\n## 配置说明 {#config}\\n\\n## 常见问题 {#faq}\\n\\n点击[配置说明](#config)跳转到配置章节。",
        "common_errors": '[{"报错":"[TOC] 显示为纯文本","解决办法":"确认平台是否支持 [TOC]，不支持时手动创建目录"}]',
        "aliases": "目录,TOC,锚点,anchor,标题链接,{#id}",
    },
]

# ============================================================
# JSON 补充（+6 条）
# ============================================================
JSON_PATTERNS = [
    {
        "title": "JSON Schema 基础",
        "language": "JSON语法",
        "pattern_text": "{\\\"$schema\\\": ...}",
        "parsed_table": '[{"段":"$schema","含义":"Schema 规范版本 URL"},{"段":"$id","含义":"Schema 的唯一标识"},{"段":"type","含义":"数据类型约束"},{"段":"properties","含义":"对象属性的定义"}]',
        "code_block": '{\\n  "$schema": "http://json-schema.org/draft-07/schema#",\\n  "$id": "https://example.com/person.schema.json",\\n  "title": "Person",\\n  "type": "object",\\n  "properties": {\\n    "name": {\\n      "type": "string",\\n      "description": "姓名"\\n    },\\n    "age": {\\n      "type": "integer",\\n      "minimum": 0,\\n      "maximum": 150\\n    }\\n  },\\n  "required": ["name"]\\n}',
        "line_by_line": '[{"代码":"\\\"$schema\\\"","说明":"Schema 规范版本"},{"代码":"\\\"type\\\": \\\"object\\\"","说明":"顶层数据类型"},{"代码":"\\\"properties\\\"","说明":"定义各字段的约束"},{"代码":"\\\"required\\\"","说明":"必填字段列表"}]',
        "syntax_note": "JSON Schema 用于描述 JSON 数据的结构和约束。支持类型校验、范围限制、枚举、正则模式等。常用于 API 文档和自动化校验",
        "runnable_example": '{ "type": "string", "minLength": 1, "maxLength": 100, "pattern": "^[a-zA-Z]+$" }',
        "common_errors": '[{"报错":"schema 版本不兼容","解决办法":"确认使用的 draft 版本（draft-04/06/07/2019-09）并指定 $schema"}]',
        "aliases": "JSON Schema,数据校验,数据模型,schema validation",
    },
    {
        "title": "JSON Lines (.jsonl)",
        "language": "JSON语法",
        "pattern_text": "每一行是一个 JSON 对象",
        "parsed_table": '[{"段":"每行一个 JSON","含义":"每行都是一个独立的 JSON 对象"},{"段":".jsonl 后缀","含义":"文件扩展名，也可用 .ndjson"}]',
        "code_block": '{"name": "张三", "age": 28, "city": "北京"}\\n{"name": "李四", "age": 32, "city": "上海"}\\n{"name": "王五", "age": 25, "city": "广州"}',
        "line_by_line": '[{"代码":"行1: {...}","说明":"第一条记录"},{"代码":"行2: {...}","说明":"第二条记录"}]',
        "syntax_note": "JSON Lines 格式每行一个独立 JSON 对象，用换行分隔。相比标准 JSON 数组：可逐行流式处理，内存友好，支持追加。常用于日志和大数据集",
        "runnable_example": "# Python 读取 .jsonl\nimport json\nwith open('data.jsonl') as f:\n    for line in f:\n        obj = json.loads(line)\n        print(obj['name'])",
        "common_errors": '[{"报错":"文件末尾多余空行","解决办法":"处理时 strip() 或跳过空行"}]',
        "aliases": "JSONL,NDJSON,json lines,流式JSON,换行分隔JSON",
    },
    {
        "title": "JSONPath 查询",
        "language": "JSON语法",
        "pattern_text": "$.store.book[0].title",
        "parsed_table": '[{"段":"$","含义":"根对象"},{"段":".key","含义":"属性访问"},{"段":"[n]","含义":"数组索引"},{"段":"[*]","含义":"数组通配符"},{"段":"..","含义":"深度递归搜索"}]',
        "code_block": '$.store.book[*].title        # 所有书的标题\\n$.store.book[0].title        # 第一本书的标题\\n$..author                     # 所有 author 属性的值\\n$.store.book[?(@.price<10)]  # 价格小于 10 的书',
        "line_by_line": '[{"代码":"$.store.book[0]","说明":"根 → store → book → 第1本"},{"代码":"$..author","说明":"递归查找所有 author"},{"代码":"[?(@.price<10)]","说明":"筛选条件表达式"}]',
        "syntax_note": "JSONPath 类似 XPath 但用于 JSON。Python 中常用 jsonpath-ng 或 jsonpath-rw 库。语法有多个变体（Stefan Goessner 版 vs JSONPath-Plus 版）",
        "runnable_example": 'from jsonpath_ng import parse\nimport json\ndata = json.loads(\'{"store": {"book": [{"title": "A", "price": 8}, {"title": "B", "price": 12}]}}\')\nexpr = parse(\'$.store.book[?(@.price<10)].title\')\nprint([m.value for m in expr.find(data)])  # [\'A\']',
        "common_errors": '[{"报错":"JSONPath 表达式不工作","解决办法":"不同库语法有差异，jsonpath-ng 用 [?()] 而不是 [?()] 或 $.."}]',
        "aliases": "JSONPath,查询语言,query,json查询,XPath for JSON",
    },
    {
        "title": "JSONP (JSON with Padding)",
        "language": "JSON语法",
        "pattern_text": "callback({...})",
        "parsed_table": '[{"段":"callback(...)","含义":"函数调用包裹 JSON 数据"},{"段":".js 文件","含义":"JSONP 响应通常为 .js 或 .jsonp"}]',
        "code_block": 'callback({\\n  "name": "张三",\\n  "age": 28\\n})\\n\\n# 或指定函数名\\nhandleResponse({\\n  "status": "ok",\\n  "data": []\\n})',
        "line_by_line": '[{"代码":"callback({...})","说明":"回调函数名 + 括号包裹的 JSON 数据"}]',
        "syntax_note": "JSONP 利用 <script> 标签跨域请求的特性绕过同源策略。服务端返回：`callback(JSON数据)`。仅支持 GET 请求。已被 CORS 替代，现代项目很少使用",
        "runnable_example": "<!-- HTML 中使用 JSONP -->\\n<script>\\nfunction handleData(data) {\\n    console.log(data.name);\\n}\\n</script>\\n<script src=\\\"https://api.example.com/user?callback=handleData\\\"></script>",
        "common_errors": '[{"报错":"JSONP 不是标准 JSON","解决办法":"JSONP 是 JS 代码而非纯 JSON，不能直接用 JSON.parse()"}]',
        "aliases": "JSONP,跨域,带填充的JSON,padding,callback,跨域请求",
    },
    {
        "title": "JSON 与 BSON 区别",
        "language": "JSON语法",
        "pattern_text": "BSON 二进制 JSON",
        "parsed_table": '[{"段":"JSON","含义":"文本格式，人类可读"},{"段":"BSON","含义":"二进制格式，机器高效"},{"段":"BSON 类型更丰富","含义":"支持 Date、Binary、ObjectId 等"}]',
        "code_block": "# JSON (文本)\\n{\\n  \\\"_id\\\": \\\"507f1f77bcf86cd799439011\\\",\\n  \\\"createdAt\\\": \\\"2024-01-15T10:30:00Z\\\"\\n}\\n\\n# BSON (二进制，内部表示)\\n# \\x16\\x00\\x00\\x00\\x02_id\\x00\\x24...\\n# _id 为 ObjectId 类型\\n# createdAt 为 Date 类型",
        "line_by_line": '[{"代码":"JSON 文本","说明":"纯文本，约 100 字节"},{"代码":"BSON 二进制","说明":"二进制，约 120 字节（含类型信息）"}]',
        "syntax_note": "BSON 是 MongoDB 的数据存储格式。BSON 比 JSON 略大（因为存储了类型信息），但解析更快。BSON 支持更多数据类型：Date、BinData、ObjectId、Decimal128",
        "runnable_example": "# MongoDB 使用 BSON 存储\\nfrom bson import json_util\\nimport json\\ndata = {'_id': '507f1f77bcf86cd799439011', 'count': 42}\\n# 互相转换\\njson_str = json_util.dumps(data)\\nbson_bytes = json_util.loads(json_str)\\nprint(type(bson_bytes))",
        "common_errors": '[{"报错":"BSON 时间戳不是字符串","解决办法":"用 json_util.dumps() 序列化 BSON 类型，不要手动转字符串"}]',
        "aliases": "BSON,二进制JSON,MongoDB,序列化格式差异",
    },
    {
        "title": "JSON 序列化选项",
        "language": "JSON语法",
        "pattern_text": "json.dumps(obj, indent=2, ensure_ascii=False)",
        "parsed_table": '[{"段":"indent","含义":"缩进空格数，美化输出"},{"段":"ensure_ascii=False","含义":"保留非 ASCII 字符（如中文）"},{"段":"sort_keys","含义":"按键名排序"},{"段":"default","含义":"自定义序列化函数"}]',
        "code_block": 'import json\\n\\ndata = {"name": "张三", "age": 28, "scores": [95, 87]}\\n\\n# 美化输出\\nprint(json.dumps(data, indent=2, ensure_ascii=False))\\n\\n# 排序键名\\nprint(json.dumps(data, sort_keys=True))\\n\\n# 排除 None\\nprint(json.dumps(data, default=lambda o: None))',
        "line_by_line": '[{"代码":"indent=2","说明":"2 空格缩进格式化"},{"代码":"ensure_ascii=False","说明":"保留中文/Unicode"},{"代码":"sort_keys=True","说明":"按键字母排序"}]',
        "syntax_note": "json.dumps() 常用选项：indent（美化）、ensure_ascii（保留中文）、sort_keys（排序）、separators（压缩输出）、default（处理特殊类型）。json.dump() 写文件",
        "runnable_example": 'import json\\n\\ndata = {"name": "Alice", "age": 30}\\n\\n# 压缩输出（最小）\\ncompact = json.dumps(data, separators=(",", ":"))\\nprint(compact)  # {"name":"Alice","age":30}\\n\\n# 写入文件\\nwith open("data.json", "w", encoding="utf-8") as f:\\n    json.dump(data, f, indent=2, ensure_ascii=False)',
        "common_errors": '[{"报错":"Object of type X is not JSON serializable","解决办法":"提供 default 函数或实现对象的 __json__ 方法"}]',
        "aliases": "序列化,serialization,json.dumps,美化,格式化,pretty print",
    },
]

# ============================================================
# YAML 补充（+6 条）
# ============================================================
YAML_PATTERNS = [
    {
        "title": "多文档 ---/...",
        "language": "YAML",
        "pattern_text": "--- 和 ...",
        "parsed_table": '[{"段":"---","含义":"文档起始标记"},{"段":"...","含义":"文档结束标记"}]',
        "code_block": "---\\nname: 文档一\\nversion: 1\\n...\\n---\\nname: 文档二\\nversion: 2\\n...",
        "line_by_line": '[{"代码":"---","说明":"第一个文档开始"},{"代码":"...","说明":"第一个文档结束"},{"代码":"---","说明":"第二个文档开始"}]',
        "syntax_note": "YAML 文件可包含多个文档，用 --- 分隔，... 可选结束标记。解析时可通过 yaml.load_all() 依次读取所有文档。单文档文件可省略开头的 ---",
        "runnable_example": "import yaml\\nwith open('multi.yaml') as f:\\n    for doc in yaml.safe_load_all(f):\\n        print(doc)\\n\\n# multi.yaml 内容：\\n# ---\\n# kind: ConfigMap\\n# ---\\n# kind: Secret",
        "common_errors": '[{"报错":"load_all 只读取了第一个文档","解决办法":"使用 yaml.safe_load_all() 而非 yaml.safe_load()"}]',
        "aliases": "多文档,multi-document,---,文档分隔,stream",
    },
    {
        "title": "强制类型 !!str !!int",
        "language": "YAML",
        "pattern_text": "!!str !!int !!float",
        "parsed_table": '[{"段":"!!str","含义":"强制为字符串类型"},{"段":"!!int","含义":"强制为整数类型"},{"段":"!!float","含义":"强制为浮点数类型"},{"段":"!!bool","含义":"强制为布尔类型"}]',
        "code_block": "a: !!str 123        # 强制为字符串 '123'\\nb: !!int '456'      # 强制为整数 456\\nc: !!float 789      # 强制为浮点数 789.0\\nd: !!bool yes       # 强制为布尔值 true\\ne: !!str true       # 强制为字符串 'true'",
        "line_by_line": '[{"代码":"!!str 123","说明":"将数字转为字符串"},{"代码":"!!int \\\"456\\\"","说明":"将字符串转为整数"}]',
        "syntax_note": "!!type 是 YAML 的类型标签（tag），用于显式指定值的类型。常见标签：!!str、!!int、!!float、!!bool、!!null、!!timestamp、!!seq、!!map",
        "runnable_example": "config:\\n  port: !!str 8080      # 字符串 '8080' 而非数字\\n  debug: !!bool yes    # true\\n  version: !!float 1   # 1.0\\n  timeout: 30           # 自动推断为整数 30",
        "common_errors": '[{"报错":"!!int 不识别","解决办法":"确保 YAML 解析器支持类型标签（Python PyYAML 支持）"}]',
        "aliases": "强制类型,类型标签,tag,!!str,!!int,类型转换",
    },
    {
        "title": "合并键 <<: *",
        "language": "YAML",
        "pattern_text": "<<: *anchor",
        "parsed_table": '[{"段":">>","含义":"合并键声明"},{"段":"*anchor","含义":"引用锚点合并映射"}]',
        "code_block": "defaults: &defaults\\n  adapter: postgres\\n  host: localhost\\n  port: 5432\\n\\ndevelopment:\\n  <<: *defaults\\n  database: dev_db\\n  debug: true\\n\\nproduction:\\n  <<: *defaults\\n  host: prod.example.com\\n  database: prod_db\\n  debug: false",
        "line_by_line": '[{"代码":"<<: *defaults","说明":"合并 defaults 锚点的所有键值对"}]',
        "syntax_note": "<<: * 是 YAML 的 Merge Key 扩展（TypeScript/PyYAML 支持）。将锚点映射的所有键值对合并到当前映射。合并后的键可以被当前映射中的键覆盖",
        "runnable_example": "base: &base\\n  timeout: 30\\n  retries: 3\\n  log_level: info\\n\\nweb:\\n  <<: *base\\n  port: 80\\n  timeout: 60  # 覆盖 base 的 timeout\\n\\nworker:\\n  <<: *base\\n  port: 9000",
        "common_errors": '[{"报错":"<<: 不是标准 YAML 1.1","解决办法":"确认解析器支持 Merge Key 扩展（PyYAML 支持，yaml-cpp 部分支持）"}]',
        "aliases": "合并键,merge key,<<:,映射合并,继承",
    },
    {
        "title": "折叠块标量 >-",
        "language": "YAML",
        "pattern_text": ">-",
        "parsed_table": '[{"段":">","含义":"折叠换行为空格"},{"段":">-","含义":"折叠 + 去除末尾换行"},{"段":">+","含义":"折叠 + 保留末尾换行"}]',
        "code_block": "summary: >-\\n  这是一个折叠块标量\\n  所有换行都会变成空格\\n  最终不保留末尾换行\\n\\nmessage: >\\n  这个保留一个末尾换行\\n  但中间的换行被折叠\\n\\nnote: >+\\n  这个保留所有末尾换行\\n  包括最后多余的换行\\n",
        "line_by_line": '[{"代码":">-","说明":"折叠块 + 去掉末尾换行"},{"代码":">","说明":"折叠块 + 保留一个末尾换行"},{"代码":">+","说明":"折叠块 + 保留所有末尾换行"}]',
        "syntax_note": "块标量指示符 >（折叠）将内部换行替换为空格。后缀 - 去掉末尾换行，+ 保留末尾换行，默认无后缀时保留一个末尾换行。常用于长段落文本",
        "runnable_example": "description: >-\\n  这是一段关于产品的描述文字。\\n  即使在这个 YAML 中写了多行，\\n  解析后也会变成一行。\\n\\n  # 空行会被保留为一个空格",
        "common_errors": '[{"报错":"折叠后空格位置不对","解决办法":"检查缩进，块内行缩进必须一致"}]',
        "aliases": "折叠标量,folded,block scalar,>-,折叠换行",
    },
    {
        "title": "文字块标量 |+",
        "language": "YAML",
        "pattern_text": "|+",
        "parsed_table": '[{"段":"|","含义":"保留换行的文字块"},{"段":"|-","含义":"保留换行 + 去掉末尾换行"},{"段":"|+","含义":"保留换行 + 保留所有末尾换行"}]',
        "code_block": "code: |\\n  def hello():\\n      print(\\\"Hello\\\")\\n\\nscript: |-\\n  #!/bin/bash\\n  echo \\\"Hello\\\"\\n\\npoem: |+\\n  床前明月光\\n  疑是地上霜\\n\\n",
        "line_by_line": '[{"代码":"|","说明":"保留换行，末尾加一个换行"},{"代码":"|-","说明":"保留换行，去除末尾换行"},{"代码":"|+","说明":"保留换行，保留所有末尾换行"}]',
        "syntax_note": "| 字面块标量保留所有换行符。后缀含义同 >。常用于代码片段、诗歌等需要保留格式的文本。可在 | 后加数字指定缩进偏移（如 |2）",
        "runnable_example": "script: |\\n  #!/usr/bin/env python3\\n  import sys\\n  \\n  def main():\\n      print(\\\"Hello\\\")\\n  \\n  if __name__ == \\\"__main__\\\":\\n      main()\\n\\nconfig: |-\\n  [server]\\n  host = localhost\\n  port = 8080",
        "common_errors": '[{"报错":"块内容缩进不对齐","解决办法":"块内容必须缩进比键名多至少一个空格"}]',
        "aliases": "文字块,literal block,|,块标量,保留换行,heredoc",
    },
    {
        "title": "锚点别名链式引用",
        "language": "YAML",
        "pattern_text": "& * 链式",
        "parsed_table": '[{"段":"&a","含义":"定义锚点 a"},{"段":"*a","含义":"引用锚点 a"},{"段":"链式","含义":"锚点可引用其他锚点"}]',
        "code_block": "base: &base\\n  host: localhost\\n  port: 8080\\n\\nextended: &extended\\n  <<: *base\\n  debug: true\\n  version: 2\\n\\napp_one:\\n  <<: *extended\\n  name: app-1\\n\\napp_two:\\n  <<: *extended\\n  name: app-2\\n  port: 9090  # 覆盖 port",
        "line_by_line": '[{"代码":"&base","说明":"定义基础锚点"},{"代码":"&extended","说明":"扩展锚点（引用 base）"},{"代码":"*extended","说明":"链式引用最终结果"}]',
        "syntax_note": "锚点可以链式引用：一个锚点通过 <<: * 合并另一个锚点，形成继承链。注意不能形成循环引用。这种模式在 Kubernetes YAML 配置中非常常见",
        "runnable_example": "api: &api\\n  timeout: 30\\n  retries: 3\\n\\napi_v2: &api_v2\\n  <<: *api\\n  retries: 5  # 覆盖\\n  tracing: true\\n\\nuser_service:\\n  <<: *api_v2\\n  endpoint: /users\\n\\norder_service:\\n  <<: *api_v2\\n  endpoint: /orders",
        "common_errors": '[{"报错":"循环引用导致解析失败","解决办法":"检查锚点链中是否有 A->B->A 的循环"}]',
        "aliases": "链式引用,chained anchor,继承链,组合复用,锚点链",
    },
]

# ============================================================
# 批处理/BAT（+10 条）
# ============================================================
BAT_PATTERNS = [
    {
        "title": "@echo off",
        "language": "批处理/BAT",
        "pattern_text": "@echo off",
        "parsed_table": '[{"段":"@","含义":"隐藏本条命令自身的回显"},{"段":"echo off","含义":"关闭后续命令的回显"}]',
        "code_block": "@echo off\\necho 这行不会显示命令本身\\necho 只输出这行文字\\npause",
        "line_by_line": '[{"代码":"@echo off","说明":"关闭命令回显（推荐作为 BAT 第一行）"},{"代码":"echo 文本","说明":"输出文本"}]',
        "syntax_note": "@echo off 是几乎所有 .bat 文件的第一行。@ 抑制本条命令的回显；echo off 抑制后续所有命令的回显。用 echo on 可重新开启",
        "runnable_example": "@echo off\\necho Hello, World!\\necho 当前时间：%time%\\npause",
        "common_errors": '[{"报错":"命令在终端显示","解决办法":"确认 BAT 第一行是 @echo off 而不是 echo off"}]',
        "aliases": "关闭回显,echo off,隐藏命令,静默模式",
    },
    {
        "title": "set /p 用户输入",
        "language": "批处理/BAT",
        "pattern_text": "set /p var=提示",
        "parsed_table": '[{"段":"set /p","含义":"等待用户输入并存入变量"},{"段":"var=提示文字","含义":"变量名和提示信息"}]',
        "code_block": "@echo off\\nset /p name=请输入您的名字：\\necho 您好，%name%！\\npause",
        "line_by_line": '[{"代码":"set /p name=","说明":"等待输入存入 name 变量"},{"代码":"echo %name%","说明":"输出变量值"}]',
        "syntax_note": "set /p 将用户输入存入变量，变量值两侧不能有空格（影响精确比较）。如果用户直接按回车，变量保持原值或为空",
        "runnable_example": "@echo off\\nset /p choice=是否继续？(Y/N)：\\nif /i \\\"%choice%\\\"==\\\"Y\\\" echo 继续执行\\nif /i \\\"%choice%\\\"==\\\"N\\\" exit\\npause",
        "common_errors": '[{"报错":"变量比较总是失败","解决办法":"用 \\\"%var%\\\" 包裹变量再比较，避免空格问题"}]',
        "aliases": "用户输入,input,set /p,交互,命令行输入",
    },
    {
        "title": "if exist 判断",
        "language": "批处理/BAT",
        "pattern_text": "if exist ...",
        "parsed_table": '[{"段":"if exist 路径","含义":"检查文件或文件夹是否存在"},{"段":"if not exist 路径","含义":"检查是否不存在"}]',
        "code_block": "@echo off\\nif exist \\\"C:\\\\Windows\\\\notepad.exe\\\" (\\n    echo 记事本存在\\n) else (\\n    echo 记事本不存在\\n)\\n\\nif not exist \\\"output\\\" (\\n    mkdir output\\n)",
        "line_by_line": '[{"代码":"if exist 文件","说明":"文件存在则执行"},{"代码":"if not exist 文件夹","说明":"文件夹不存在则创建"}]',
        "syntax_note": "路径含空格必须用双引号。可用 ( ) 包裹多行命令块。else 必须与 ) 在同一行或用 ^ 续行",
        "runnable_example": "@echo off\\nif exist \\\"%USERPROFILE%\\\\Desktop\\\\test.txt\\\" (\\n    echo 文件存在于桌面\\n    del \\\"%USERPROFILE%\\\\Desktop\\\\test.txt\\\"\\n) else (\\n    echo 文件不存在\\n)\\npause",
        "common_errors": '[{"报错":"else 语法错误","解决办法":"else 必须与 ) 同行：\\\") else (\\\""}]',
        "aliases": "文件存在判断,if exist,条件判断,文件检查",
    },
    {
        "title": "for %%i 循环",
        "language": "批处理/BAT",
        "pattern_text": "for %%i in (...) do ...",
        "parsed_table": '[{"段":"for %%i in (集合)","含义":"遍历集合中的元素"},{"段":"%%i","含义":"循环变量（两个百分号）"}]',
        "code_block": "@echo off\\nrem 遍历文件\\nfor %%f in (*.txt) do (\\n    echo 找到文件：%%f\\n)\\n\\nrem 遍历数字范围\\nfor /l %%i in (1,1,5) do (\\n    echo 计数：%%i\\n)\\n\\nrem 遍历目录\\nfor /d %%d in (*) do (\\n    echo 目录：%%d\\n)",
        "line_by_line": '[{"代码":"for %%f in (*.txt)","说明":"遍历当前目录所有 .txt 文件"},{"代码":"for /l %%i (1,1,5)","说明":"从 1 到 5 步进 1"}]',
        "syntax_note": "批处理中循环变量必须用 %%i（两个百分号），命令行中用一个 %i。/l 表示数字范围（start,step,end）；/d 遍历目录；/r 递归遍历",
        "runnable_example": "@echo off\\nrem 批量重命名 .txt 为 .bak\\nfor %%f in (*.txt) do (\\n    ren \\\"%%f\\\" \\\"%%~nf.bak\\\"\\n)\\necho 重命名完成！\\npause",
        "common_errors": '[{"报错":"%%i 报语法错误","解决办法":"批处理文件中用 %%i，命令行中用一个 %i"}]',
        "aliases": "for循环,遍历,loop,for /l,for /d,批量处理",
    },
    {
        "title": "findstr 搜索",
        "language": "批处理/BAT",
        "pattern_text": "findstr ...",
        "parsed_table": '[{"段":"findstr 模式 文件","含义":"搜索文件中匹配的行"},{"段":"/i","含义":"忽略大小写"},{"段":"/v","含义":"显示不匹配的行"},{"段":"/n","含义":"显示行号"}]',
        "code_block": "@echo off\\nrem 基本搜索\\nfindstr \\\"error\\\" log.txt\\n\\nrem 忽略大小写\\nfindstr /i \\\"warning\\\" *.log\\n\\nrem 递归搜索\\nfindstr /s \\\"TODO\\\" *.py\\n\\nrem 显示不匹配的行\\nfindstr /v \\\"#\\\" config.ini",
        "line_by_line": '[{"代码":"findstr \\\"text\\\" file","说明":"在文件中搜索文本"},{"代码":"findstr /i \\\"text\\\" *.log","说明":"忽略大小写搜索多个文件"}]',
        "syntax_note": "findstr 是 Windows 版的 grep，支持正则表达式（有限）。/i 忽略大小写，/v 反向匹配，/n 显示行号，/s 递归子目录，/m 仅显示文件名",
        "runnable_example": "@echo off\\nrem 查找所有包含 IP 地址的行\\nfindstr /n /r \\\"[0-9][0-9]*\\\\.[0-9][0-9]*\\\\.[0-9][0-9]*\\\\.[0-9][0-9]*\\\" *.log\\npause",
        "common_errors": '[{"报错":"findstr 不支持某些正则","解决办法":"findstr 的正则有限，复杂搜索用 powershell Select-String"}]',
        "aliases": "文本搜索,findstr,字符串查找,grep for Windows",
    },
    {
        "title": "choice 和 errorlevel",
        "language": "批处理/BAT",
        "pattern_text": "choice /c YN",
        "parsed_table": '[{"段":"choice /c 选项","含义":"显示选项并等待按键"},{"段":"errorlevel","含义":"返回上一个命令的退出代码"}]',
        "code_block": "@echo off\\nchoice /c YNC /n /m \\\"请选择 (Y)是 (N)否 (C)取消：\\\"\\necho 选择的键是：%errorlevel%\\n\\nif errorlevel 3 echo 选择了取消\\nif errorlevel 2 echo 选择了否\\nif errorlevel 1 echo 选择了是\\n\\nrem 注意：errorlevel 检测从大到小排列",
        "line_by_line": '[{"代码":"choice /c YN","说明":"等待用户按 Y 或 N"},{"代码":"if errorlevel 1","说明":"如果错误码 >= 1"}]',
        "syntax_note": "choice 显示提示并等待按键。第一个键返回 errorlevel=1，第二个=2，依此类推。errorlevel 判断用 if errorlevel n（检测 >=n），必须从大到小检测",
        "runnable_example": "@echo off\\n:retry\\nchoice /c AC /n /m \\\"(A) 继续 (C) 取消：\\\"\\nif errorlevel 2 exit\\nif errorlevel 1 goto start\\n\\n:start\\necho 开始执行任务...\\npause",
        "common_errors": '[{"报错":"errorlevel 检测顺序不对","解决办法":"始终从大（高值）到小（低值）检测"}]',
        "aliases": "choice,errorlevel,退出码,按键选择,用户交互",
    },
    {
        "title": "goto 标签跳转",
        "language": "批处理/BAT",
        "pattern_text": "goto :label",
        "parsed_table": '[{"段":"goto :label","含义":"跳转到标签处执行"},{"段":":label","含义":"标签定义（冒号开头）"}]',
        "code_block": "@echo off\\necho 程序开始\\ngoto :middle\\n\\n:start\\necho 这是开始部分\\ngoto :end\\n\\n:middle\\necho 直接跳到中间\\ngoto :start\\n\\n:end\\necho 程序结束\\npause",
        "line_by_line": '[{"代码":"goto :label","说明":"跳转到指定标签"},{"代码":":label","说明":"标签定义（不区分大小写）"}]',
        "syntax_note": "标签以 : 开头。goto 跳转不区分标签名大小写。标签独占一行，也可在命令前（如 `:error echo 错误`）。避免 goto 过多导致代码难以维护",
        "runnable_example": "@echo off\\nif not exist \\\"data.txt\\\" goto :error\\ntype data.txt\\ngoto :end\\n\\n:error\\necho 错误：data.txt 不存在！\\n\\n:end\\npause",
        "common_errors": '[{"报错":"标签找不到","解决办法":"检查标签名是否一致（有无空格或拼写错误）"}]',
        "aliases": "goto,标签跳转,label,跳转,jump,分支",
    },
    {
        "title": "延迟扩展 !var!",
        "language": "批处理/BAT",
        "pattern_text": "setlocal enabledelayedexpansion",
        "parsed_table": '[{"段":"setlocal enabledelayedexpansion","含义":"启用延迟变量扩展"},{"段":"!var!","含义":"即时扩展的变量（而非 %var%）"}]',
        "code_block": "@echo off\\nsetlocal enabledelayedexpansion\\n\\nset count=0\\nfor /l %%i in (1,1,5) do (\\n    set /a count+=1\\n    rem %%count%% 在 for 中不会更新\\n    echo 使用延迟扩展：!count!\\n)\\n\\necho 最终值：%count%",
        "line_by_line": '[{"代码":"setlocal enabledelayedexpansion","说明":"启用延迟变量扩展"},{"代码":"!var!","说明":"在循环中获取变量的实时值"}]',
        "syntax_note": "批处理中 %var% 在代码块解析时一次性展开。!var! 在每次执行时展开，用于 for 循环等场景实时获取变量变化。setlocal 必须在文件开头启用",
        "runnable_example": "@echo off\\nsetlocal enabledelayedexpansion\\n\\nset total=0\\nfor /l %%i in (1,1,10) do (\\n    set /a total+=%%i\\n)\\necho 1 到 10 的和：!total!\\npause",
        "common_errors": '[{"报错":"!var! 显示为字面感叹号","解决办法":"确认已执行 setlocal enabledelayedexpansion"}]',
        "aliases": "延迟扩展,delayed expansion,!var!,setlocal,变量延迟",
    },
    {
        "title": "call 子程序和 start",
        "language": "批处理/BAT",
        "pattern_text": "call :sub start ...",
        "parsed_table": '[{"段":"call 标签","含义":"调用子程序（返回原处）"},{"段":"call 文件.bat","含义":"调用另一个批处理文件"},{"段":"start 程序","含义":"启动新窗口运行程序"}]',
        "code_block": "@echo off\\nrem 调用子程序\\ncall :sub 参数1 参数2\\necho 回到主程序\\n\\nrem 启动新窗口\\nstart notepad.exe myfile.txt\\n\\nrem 启动并等待\\nstart /wait ping 127.0.0.1 -n 5\\n\\ngoto :eof\\n\\n:sub\\necho 子程序开始\\necho 参数1：%1\\necho 参数2：%2\\necho 子程序结束\\ngoto :eof",
        "line_by_line": '[{"代码":"call :sub","说明":"调用子程序"},{"代码":"start notepad","说明":"启动程序（新窗口）"},{"代码":"goto :eof","说明":"返回/结束子程序"}]',
        "syntax_note": "call :label 跳转到标签并保存返回点，执行到 goto :eof 或文件末尾时返回。start 在新窗口中启动程序，/wait 等待程序退出",
        "runnable_example": "@echo off\\nrem 启动计算器并等待\\nstart /wait calc.exe\\necho 计算器已关闭，继续执行...\\n\\nrem 带参数调用子程序\\ncall :print \\\"Hello\\\" \\\"World\\\"\\npause\\nexit /b\\n\\n:print\\necho %1 %2\\ngoto :eof",
        "common_errors": '[{"报错":"子程序参数为空","解决办法":"call :sub 后加参数，子程序中用 %1 %2 等获取"}]',
        "aliases": "子程序,call,start,调用,子过程,subroutine",
    },
    {
        "title": "ping 延时和 type nul >",
        "language": "批处理/BAT",
        "pattern_text": "ping -n timeout && type nul > file",
        "parsed_table": '[{"段":"ping -n 秒 127.1 > nul","含义":"用 ping 实现延时"},{"段":"type nul > 文件","含义":"清空文件或创建空文件"}]',
        "code_block": "@echo off\\necho 等待 3 秒...\\nrem 用 ping 实现延时\\nping -n 4 127.0.0.1 > nul\\necho 继续执行\\n\\nrem 清空日志文件\\ntype nul > log.txt\\necho 日志已清空\\n\\nrem 创建空文件\\ntype nul > newfile.txt",
        "line_by_line": '[{"代码":"ping -n 4 127.1 >nul","说明":"延时约 3 秒（4 次 ping -1）"},{"代码":"type nul > file","说明":"创建或清空文件"}]',
        "syntax_note": "ping -n 4 127.0.0.1 > nul：Windows 中 ping 间隔约 1 秒，4 次约 3 秒延时。type nul > file 创建空文件或清空已有文件内容。也可用 copy nul file",
        "runnable_example": "@echo off\\necho 正在启动服务，请等待...\\n\\nrem 延时 5 秒\\nping -n 6 127.0.0.1 > nul\\n\\nrem 清空上一次的日志\\ntype nul > output.log\\n\\necho 服务已启动！\\necho 日志文件已重置。\\npause",
        "common_errors": '[{"报错":"ping 不支持 -n","解决办法":"Windows 系统支持，Linux 需改用 sleep 命令"}]',
        "aliases": "延时,ping delay,timeout,清空文件,type nul,创建空文件",
    },
]

# ============================================================
# 配置文件(.ini/.env) 补充（+6 条）
# ============================================================
CONFIG_PATTERNS = [
    {
        "title": "INI 节 [section]",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "[section]",
        "parsed_table": '[{"段":"[section]","含义":"定义配置节（section）"},{"段":"key=value","含义":"节内的键值对"}]',
        "code_block": "[database]\\nhost = localhost\\nport = 5432\\ndbname = myapp\\n\\n[server]\\nhost = 0.0.0.0\\nport = 8080\\ndebug = true\\n\\n[logging]\\nlevel = INFO\\nfile = app.log",
        "line_by_line": '[{"代码":"[database]","说明":"数据库配置节"},{"代码":"host = localhost","说明":"键值对"},{"代码":"[server]","说明":"服务器配置节"}]',
        "syntax_note": "INI 文件由节（section）和键值对组成。节名用 [] 包裹，独占一行。键值对用 = 或 : 分隔。Python 用 configparser 模块解析",
        "runnable_example": "# Python 读取 INI\\nimport configparser\\nconfig = configparser.ConfigParser()\\nconfig.read('config.ini')\\nprint(config['database']['host'])  # localhost",
        "common_errors": '[{"报错":"选项未找到","解决办法":"确认节名和键名大小写是否正确（默认区分大小写）"}]',
        "aliases": "INI文件,配置文件,section,节,configparser",
    },
    {
        "title": "INI 键=值和注释",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "key=value 和 ; #",
        "parsed_table": '[{"段":"key=value","含义":"INI 键值对"},{"段":"; 注释","含义":"INI 标准注释"},{"段":"# 注释","含义":"另一种注释方式（部分解析器支持）"}]',
        "code_block": "; 数据库配置\\n# 这也是注释（configparser 支持）\\n[database]\\nhost = localhost  ; 行尾注释\\nport = 5432\\n\\n; 以下为可选配置\\n# timeout = 30",
        "line_by_line": '[{"代码":"; 注释","说明":"INI 标准注释（行首）"},{"代码":"key=value","说明":"键值对"},{"代码":"; 行尾注释","说明":"值后的注释"}]',
        "syntax_note": "INI 标准注释符是 ;，# 也被部分解析器支持但非标准。注释可独占一行或在行尾（某些解析器只支持独立行注释）。值中的 ; 不是注释",
        "runnable_example": "import configparser\\nconfig = configparser.ConfigParser()\\nconfig.read_string('''\\n; 应用程序配置\\n[app]\\nname = MyApp  ; 应用名称\\nversion = 1.0\\n''')\\nprint(config['app']['name'])  # 'MyApp'",
        "common_errors": '[{"报错":"注释导致解析错误","解决办法":"检查行尾注释是否被解析器支持，或放独立行"}]',
        "aliases": "INI注释,键值对,;注释,config注释",
    },
    {
        "title": ".env 变量 FOO=bar",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "KEY=VALUE",
        "parsed_table": '[{"段":"KEY=VALUE","含义":"环境变量定义"},{"段":"# 注释","含义":".env 文件注释"}]',
        "code_block": "# 数据库配置\\nDB_HOST=localhost\\nDB_PORT=5432\\nDB_NAME=myapp\\nDB_USER=admin\\nDB_PASS=secret123\\n\\n# 应用配置\\nAPP_ENV=development\\nAPP_DEBUG=true\\nAPP_SECRET=your-secret-key",
        "line_by_line": '[{"代码":"DB_HOST=localhost","说明":"环境变量：数据库主机"},{"代码":"APP_DEBUG=true","说明":"环境变量：调试开关"}]',
        "syntax_note": ".env 文件存储环境变量，每行 KEY=value 格式。值不加引号（如果值含空格或特殊字符才加引号）。Python 用 python-dotenv 库加载",
        "runnable_example": "# Python 加载 .env\\nfrom dotenv import load_dotenv\\nimport os\\nload_dotenv()\\ndb_host = os.getenv('DB_HOST')\\nprint(db_host)  # localhost",
        "common_errors": '[{"报错":"值包含空格被截断","解决办法":"用双引号包裹含空格的值：KEY=\\\"value with spaces\\\""}]',
        "aliases": ".env,环境变量,dotenv,环境配置,env file",
    },
    {
        "title": ".env 引用 ${VAR}",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "${VAR}",
        "parsed_table": '[{"段":"${VAR}","含义":"引用其他环境变量的值"},{"段":"${VAR:-default}","含义":"带默认值的引用"}]',
        "code_block": "# 基础变量\\nAPP_HOME=/opt/myapp\\nLOG_DIR=${APP_HOME}/logs\\nDATA_DIR=${APP_HOME}/data\\n\\n# 带默认值的引用\\nPORT=${PORT:-8080}\\nHOST=${HOST:-localhost}\\n\\n# 组合变量\\nDATABASE_URL=postgres://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}",
        "line_by_line": '[{"代码":"LOG_DIR=${APP_HOME}/logs","说明":"引用 APP_HOME 变量组合路径"},{"代码":"PORT=${PORT:-8080}","说明":"如果 PORT 未定义则默认 8080"}]',
        "syntax_note": "${VAR} 语法用于在 .env 中引用其他变量。${VAR:-default} 提供默认值。Python python-dotenv 支持此扩展语法。注意：Windows 系统变量也可被引用",
        "runnable_example": "# .env 文件\\nNODE_ENV=production\\nAPI_URL=https://api.${NODE_ENV}.example.com\\n# 解析后 API_URL = https://api.production.example.com",
        "common_errors": '[{"报错":"变量未展开为原样","解决办法":"确认 dotenv 库支持变量展开（python-dotenv>=0.10.0）"}]',
        "aliases": "变量引用,${VAR},环境变量引用,变量展开,dotenv引用",
    },
    {
        "title": "TOML 简单语法",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "[table] key = \\\"value\\\"",
        "parsed_table": '[{"段":"[table]","含义":"表（类似 INI 节）"},{"段":"key = value","含义":"键值对"},{"段":"[table.subtable]","含义":"嵌套表"}]',
        "code_block": "# TOML 配置文件\\ntitle = \\\"我的应用\\\"\\nversion = \\\"1.0.0\\\"\\n\\n[database]\\nhost = \\\"localhost\\\"\\nport = 5432\\nuser = \\\"admin\\\"\\n\\n[server]\\nhost = \\\"0.0.0.0\\\"\\nport = 8080\\n\\n[database.options]\\npool_size = 10\\ntimeout = 30.0",
        "line_by_line": '[{"代码":"[database]","说明":"表定义"},{"代码":"host = \\\"localhost\\\"","说明":"字符串值"},{"代码":"port = 5432","说明":"整数值"},{"代码":"[database.options]","说明":"嵌套表"}]',
        "syntax_note": "TOML 是 Rust 社区推广的配置文件格式。支持字符串（双引号）、整数、浮点数、布尔值、日期时间。用 [table] 定义表，[table.sub] 定义嵌套表",
        "runnable_example": "# Python 读取 TOML\\nimport tomllib\\nwith open('config.toml', 'rb') as f:\\n    config = tomllib.load(f)\\nprint(config['database']['host'])  # localhost",
        "common_errors": '[{"报错":"tomllib 需要 Python 3.11+","解决办法":"旧版本用 pip install tomli 或 pip install toml"}]',
        "aliases": "TOML,配置文件,Rust配置,表结构,[table],tomllib",
    },
    {
        "title": "INI/TOML 分层和数组",
        "language": "配置文件(.ini/.env)",
        "pattern_text": "[[array]]",
        "parsed_table": '[{"段":"[[array]]","含义":"TOML 数组表"},{"段":"[section]\\nkey=value","含义":"INI 分层配置"}]',
        "code_block": "# TOML 数组表\\n[[servers]]\\nname = \\\"web01\\\"\\nip = \\\"10.0.0.1\\\"\\n\\n[[servers]]\\nname = \\\"web02\\\"\\nip = \\\"10.0.0.2\\\"\\n\\n# INI 模拟数组\\n[servers]\\nserver1 = \\\"web01\\\"\\nserver2 = \\\"web02\\\"",
        "line_by_line": '[{"代码":"[[servers]]","说明":"TOML 数组表中的一项"},{"代码":"[servers]","说明":"INI 用多个键模拟数组"}]',
        "syntax_note": "TOML 支持 [[array_table]] 作为对象数组。INI 不支持原生数组，需用键名后缀编号或其他方式模拟。TOML 还支持行内表（inline table）和数组",
        "runnable_example": "# TOML 数组表示例\\n[[products]]\\nname = \\\"Hammer\\\"\\nsku = 738594937\\n\\n[[products]]\\nname = \\\"Nail\\\"\\nsku = 284758393\\ncolor = \\\"gray\\\"\\n\\n# 解析后 products 是对象列表",
        "common_errors": '[{"报错":"数组表不能与同名的表混用","解决办法":"不能同时定义 [products] 和 [[products]]"}]',
        "aliases": "数组表,array table,TOML数组,[[],分层配置",
    },
]


# ============================================================
# 分类查找/创建辅助函数
# ============================================================
def get_category_id(db, name):
    """通过分类名称查询 id"""
    _, name_id = db.get_all_categories_map()
    return name_id.get(name)


def get_or_create_category(db, name, parent_name, item_type='pattern', sort_order=0):
    """获取分类 ID，不存在则创建"""
    cid = get_category_id(db, name)
    if cid is not None:
        print(f"  [OK] 已存在: {name} (id={cid})")
        return cid

    parent_id = get_category_id(db, parent_name) if parent_name else None
    if parent_name and parent_id is None:
        print(f"  [ERR] 父分类 '{parent_name}' 不存在，无法创建 '{name}'")
        return None

    cid = db.add_category(name=name, parent_id=parent_id, item_type=item_type, sort_order=sort_order)
    print(f"  [OK] 新建分类: {name} (id={cid}, parent={parent_name})")
    return cid


def insert_patterns(db, cat_id, patterns, category_label):
    """批量插入模式条目"""
    if cat_id is None:
        print(f"  [ERR] 分类 '{category_label}' 不存在，跳过")
        return 0
    count = 0
    for p in patterns:
        try:
            db.add_pattern(
                category_id=cat_id,
                title=p["title"],
                language=p["language"],
                pattern_text=p.get("pattern_text", ""),
                parsed_table=p.get("parsed_table", "[]"),
                code_block=p["code_block"],
                line_by_line=p.get("line_by_line", "[]"),
                syntax_note=p.get("syntax_note", ""),
                runnable_example=p.get("runnable_example", ""),
                common_errors=p.get("common_errors", "[]"),
                aliases=p.get("aliases", ""),
            )
            count += 1
            print(f"  [OK] {p['title']}")
        except Exception as e:
            print(f"  [ERR] {p['title']}: {e}")
    print(f"  共插入 {count} 条\n")
    return count


def main():
    print("=" * 55)
    print("模式/标记种子数据补充脚本")
    print("=" * 55)

    # 初始化 DB
    db = DBManager(DB_PATH)
    db.init_db()
    print(f"[DB] 数据库就绪: {DB_PATH}\n")

    # ---- 创建新分类 ----
    print("── 创建新分类（其他 -> 批处理/BAT、配置文件） ──")
    bat_cat_id = get_or_create_category(
        db, "批处理/BAT", "其他", item_type="pattern", sort_order=70
    )
    config_cat_id = get_or_create_category(
        db, "配置文件(.ini/.env)", "其他", item_type="pattern", sort_order=71
    )

    # 获取已有分类 ID
    regex_cat_id = get_category_id(db, "正则表达式")
    md_cat_id = get_category_id(db, "Markdown")
    json_cat_id = get_category_id(db, "JSON语法")
    yaml_cat_id = get_category_id(db, "YAML")

    total = 0

    # ---- 正则表达式（+15） ----
    print("\n── 正则表达式 补充（15 条）──")
    total += insert_patterns(db, regex_cat_id, REGEX_PATTERNS, "正则表达式")

    # ---- Markdown（+8） ----
    print("── Markdown 补充（8 条）──")
    total += insert_patterns(db, md_cat_id, MARKDOWN_PATTERNS, "Markdown")

    # ---- JSON（+6） ----
    print("── JSON 补充（6 条）──")
    total += insert_patterns(db, json_cat_id, JSON_PATTERNS, "JSON语法")

    # ---- YAML（+6） ----
    print("── YAML 补充（6 条）──")
    total += insert_patterns(db, yaml_cat_id, YAML_PATTERNS, "YAML")

    # ---- 批处理/BAT（+10） ----
    print("── 批处理/BAT（10 条）──")
    total += insert_patterns(db, bat_cat_id, BAT_PATTERNS, "批处理/BAT")

    # ---- 配置文件(.ini/.env)（+6） ----
    print("── 配置文件(.ini/.env)（6 条）──")
    total += insert_patterns(db, config_cat_id, CONFIG_PATTERNS, "配置文件(.ini/.env)")

    # ---- 统计 ----
    print("=" * 55)
    print(f"[OK] 全部完成！共补充 {total} 条模式条目")
    print("=" * 55)


if __name__ == "__main__":
    main()
