#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
种子脚本：插入模式/标记语言（正则表达式、Markdown、JSON、YAML）数据
用法：python seed_data/seed_patterns.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

# ── 数据库路径 ────────────────────────────────────────────
DB_PATH = os.path.join(os.path.expanduser('~'), '.code-quickref', 'data.db')

# ── 正则表达式（12 条）─────────────────────────────────────

REGEX_PATTERNS = [
    {
        "title": "匹配任意数字",
        "language": "正则表达式",
        "pattern_text": "\\d",
        "parsed_table": '[{"段":"\\\\d","含义":"匹配 0-9 任意一个数字"}]',
        "code_block": "\\d+   # 匹配一个或多个连续数字",
        "line_by_line": '[{"代码":"\\\\d","说明":"匹配单个数字字符 0-9"},{"代码":"+","说明":"量词，表示一次或多次"}]',
        "syntax_note": "\\\\d 等于 [0-9]，只匹配单个数字字符。要匹配多位数字需要用量词如 \\\\d+ 或 \\\\d{n}",
        "runnable_example": "# Python 示例\nimport re\ntext = \"My phone is 138-1234\"\nnums = re.findall(r\"\\d+\", text)\nprint(nums)  # ['138', '1234']",
        "common_errors": '[{"报错":"匹配不到任何内容","解决办法":"检查是否忘了加 + 或 * 量词"},{"报错":"转义问题","解决办法":"Python 中建议使用 raw string r\"...\""}]',
        "aliases": "数字,digit,匹配数字",
    },
    {
        "title": "匹配任意字母/数字/下划线",
        "language": "正则表达式",
        "pattern_text": "\\w",
        "parsed_table": '[{"段":"\\\\w","含义":"匹配字母、数字、下划线（等价于 [a-zA-Z0-9_]）"}]',
        "code_block": "\\w+   # 匹配一个或多个单词字符",
        "line_by_line": '[{"代码":"\\\\w","说明":"匹配单个单词字符"},{"代码":"+","说明":"一次或多次"}]',
        "syntax_note": "\\\\w 等于 [a-zA-Z0-9_]，中文等 Unicode 字符默认不匹配（部分引擎支持 re.UNICODE 标志）",
        "runnable_example": "# Python 示例\nimport re\ntext = \"hello_world 123\"\nwords = re.findall(r\"\\w+\", text)\nprint(words)  # ['hello_world', '123']",
        "common_errors": '[{"报错":"中文匹配不到","解决办法":"加 re.UNICODE 标志或改用 [\\\\u4e00-\\\\u9fa5]"}]',
        "aliases": "单词字符,word,字母数字下划线",
    },
    {
        "title": "匹配任意空白字符",
        "language": "正则表达式",
        "pattern_text": "\\s",
        "parsed_table": '[{"段":"\\\\s","含义":"匹配空格、制表符、换行符等空白字符"}]',
        "code_block": "\\s+   # 匹配一个或多个空白字符",
        "line_by_line": '[{"代码":"\\\\s","说明":"匹配单个空白字符"},{"代码":"+","说明":"一次或多次"}]',
        "syntax_note": "\\\\s 包含：空格、制表符 \\\\t、换行符 \\\\n、回车符 \\\\r、换页符 \\\\f",
        "runnable_example": "# Python 示例\nimport re\ntext = \"hello   world\\nfoo\"\nparts = re.split(r\"\\s+\", text)\nprint(parts)  # ['hello', 'world', 'foo']",
        "common_errors": '[{"报错":"分割结果包含空字符串","解决办法":"检查开头/结尾是否有空白，用 strip() 预处理"}]',
        "aliases": "空白,whitespace,空格",
    },
    {
        "title": "匹配行首 ^ 和行尾 $",
        "language": "正则表达式",
        "pattern_text": "^ 和 $",
        "parsed_table": '[{"段":"^","含义":"匹配行/字符串开头"},{"段":"$","含义":"匹配行/字符串结尾"}]',
        "code_block": "^Hello   # 匹配以 Hello 开头的行\nend$      # 匹配以 end 结尾的行",
        "line_by_line": '[{"代码":"^Hello","说明":"字符串以 Hello 开头"},{"代码":"end$","说明":"字符串以 end 结尾"}]',
        "syntax_note": "多行模式（re.MULTILINE）下 ^ 和 $ 匹配每行的开头/结尾，否则只匹配整个字符串的开头/结尾",
        "runnable_example": "# Python 示例\nimport re\ntext = \"Hello world\\nHi there\"\nprint(re.findall(r\"^\\w+\", text, re.MULTILINE))  # ['Hello', 'Hi']",
        "common_errors": '[{"报错":"只匹配到第一行","解决办法":"检查是否忘了加 re.MULTILINE 标志"}]',
        "aliases": "开头结尾,行首行尾,anchor",
    },
    {
        "title": "匹配任意字符 .",
        "language": "正则表达式",
        "pattern_text": ".",
        "parsed_table": '[{"段":".","含义":"匹配除换行符外的任意单个字符"}]',
        "code_block": "h.t   # 匹配 hat, hit, hot 等，但不匹配 ht 或 h\\nt",
        "line_by_line": '[{"代码":"h.t","说明":". 匹配任意一个非换行字符"}]',
        "syntax_note": "默认不匹配 \\\\n。re.DOTALL 标志下 . 可以匹配任意字符（含换行符）",
        "runnable_example": "# Python 示例\nimport re\nprint(re.findall(r\"h.t\", \"hat hot h\\nt\"))      # ['hat', 'hot']\nprint(re.findall(r\"h.t\", \"hat hot h\\nt\", re.DOTALL))  # ['hat', 'hot', 'h\\nt']",
        "common_errors": '[{"报错":"跨行匹配不到","解决办法":"加 re.DOTALL 标志"}]',
        "aliases": "任意字符,dottall,点号",
    },
    {
        "title": "重复次数 * + ? {n,m}",
        "language": "正则表达式",
        "pattern_text": "* + ? {n,m}",
        "parsed_table": '[{"段":"*","含义":"前一个元素出现 0 次或多次"},{"段":"+","含义":"前一个元素出现 1 次或多次"},{"段":"?","含义":"前一个元素出现 0 次或 1 次"},{"段":"{n,m}","含义":"前一个元素出现 n 到 m 次"}]',
        "code_block": "a*    # 匹配 '', 'a', 'aa', 'aaa'...\na+    # 匹配 'a', 'aa', 'aaa'...\na?    # 匹配 '', 'a'\na{2,4} # 匹配 'aa', 'aaa', 'aaaa'",
        "line_by_line": '[{"代码":"a*","说明":"零次或多次（贪婪）"},{"代码":"a+","说明":"一次或多次（贪婪）"},{"代码":"a?","说明":"零次或一次"},{"代码":"a{2,4}","说明":"2 到 4 次"}]',
        "syntax_note": "默认是贪婪模式（尽可能多匹配），加 ? 变成非贪婪：*? +? ?? {n,m}?",
        "runnable_example": "# Python 示例\nimport re\ntext = \"<div>hello</div><p>world</p>\"\n# 贪婪\nprint(re.findall(r\"<.+>\", text))   # ['<div>hello</div><p>world</p>']\n# 非贪婪\nprint(re.findall(r\"<.+?>\", text))  # ['<div>', '</div>', '<p>', '</p>']",
        "common_errors": '[{"报错":"匹配结果过长（贪婪）","解决办法":"在量词后加 ? 变为非贪婪模式"}]',
        "aliases": "量词,重复,quantifier,greedy,lazy",
    },
    {
        "title": "字符组 [abc] [^abc]",
        "language": "正则表达式",
        "pattern_text": "[abc] [^abc]",
        "parsed_table": '[{"段":"[abc]","含义":"匹配 a、b、c 中的任意一个字符"},{"段":"[^abc]","含义":"匹配除 a、b、c 之外的任意字符"}]',
        "code_block": "[aeiou]  # 匹配任意一个元音字母\n[^0-9]   # 匹配任意非数字字符",
        "line_by_line": '[{"代码":"[aeiou]","说明":"匹配 a/e/i/o/u 之一"},{"代码":"[^0-9]","说明":"匹配非数字字符"}]',
        "syntax_note": "字符组内可连写范围如 [a-z]、[0-9]、[a-zA-Z0-9_]；^ 在开头表示取反，在其他位置表示字面 ^",
        "runnable_example": "# Python 示例\nimport re\nprint(re.findall(r\"[aeiou]\", \"hello world\"))  # ['e', 'o', 'o']\nprint(re.findall(r\"[^a-z]\", \"hello 123!\"))    # [' ', '1', '2', '3', '!']",
        "common_errors": '[{"报错":"取反不生效","解决办法":"确认 ^ 是否在字符组最开头 [^...]"}]',
        "aliases": "字符类,字符集,charclass,character class",
    },
    {
        "title": "分组与捕获 ()",
        "language": "正则表达式",
        "pattern_text": "()",
        "parsed_table": '[{"段":"()","含义":"将内容分组并捕获到组中"},{"段":"(?:)","含义":"仅分组不捕获"}]',
        "code_block": "(\\w+)@(\\w+)\\.(\\w+)  # 捕获邮箱的用户名、域名、后缀",
        "line_by_line": '[{"代码":"(\\\\w+)","说明":"捕获组 1：用户名"},{"代码":"(\\\\w+)\\.","说明":"捕获组 2：域名"},{"代码":"(\\\\w+)","说明":"捕获组 3：后缀"}]',
        "syntax_note": "捕获组从 1 开始编号，可用 \\\\1 \\\\2 反向引用；(?:) 是非捕获分组",
        "runnable_example": "# Python 示例\nimport re\ntext = \"user@example.com\"\nm = re.search(r\"(\\w+)@(\\w+)\\.(\\w+)\", text)\nprint(m.groups())  # ('user', 'example', 'com')\nprint(m.group(1))  # 'user'",
        "common_errors": '[{"报错":"组编号混乱","解决办法":"分组嵌套时按左括号出现顺序编号"},{"报错":"不需要捕获时用了()","解决办法":"改用 (?:) 提升性能"}]',
        "aliases": "捕获组,capture group,反向引用,backreference",
    },
    {
        "title": "或条件 |",
        "language": "正则表达式",
        "pattern_text": "|",
        "parsed_table": '[{"段":"|","含义":"匹配左边或右边的模式，二选一"}]',
        "code_block": "cat|dog   # 匹配 'cat' 或 'dog'",
        "line_by_line": '[{"代码":"cat|dog","说明":"匹配 cat 或 dog"},{"代码":"gr(a|e)y","说明":"匹配 gray 或 grey"}]',
        "syntax_note": "| 优先级较低，常与 () 配合：gr(a|e)y 匹配 gray/grey。不分组时作用于左右整个表达式",
        "runnable_example": "# Python 示例\nimport re\ntext = \"I have a cat and a dog\"\nprint(re.findall(r\"cat|dog\", text))  # ['cat', 'dog']\nprint(re.findall(r\"gr(a|e)y\", \"gray grey grAy\"))  # ['gray', 'grey']",
        "common_errors": '[{"报错":"| 匹配了意外内容","解决办法":"检查是否需要加括号限定范围"}]',
        "aliases": "或,选择,alternation,or",
    },
    {
        "title": "转义字符 \\",
        "language": "正则表达式",
        "pattern_text": "\\",
        "parsed_table": '[{"段":"\\\\","含义":"将特殊字符转义为字面含义"}]',
        "code_block": "\\.   # 匹配字面点号（而非任意字符）\n\\*   # 匹配字面星号（而非量词）",
        "line_by_line": '[{"代码":"\\\\.","说明":"匹配字面 ."},{"代码":"\\\\*","说明":"匹配字面 *"}]',
        "syntax_note": "需要转义的常见字符：. ^ $ * + ? ( ) [ ] { } \\\\ |。Python 中建议用 raw string r\"...\" 避免双重转义",
        "runnable_example": "# Python 示例\nimport re\nprint(re.findall(r\"\\.\", \"test.txt\"))      # ['.']\nprint(re.findall(r\"\\*\\.\", \"file*.txt\"))  # ['*.']",
        "common_errors": '[{"报错":"SyntaxError: invalid escape","解决办法":"Python 字符串中用 r\"...\" 或 \\\\ 双重转义"}]',
        "aliases": "转义,escape,raw string",
    },
    {
        "title": "零宽断言 (?=) (?<=) (?!) (?<!)",
        "language": "正则表达式",
        "pattern_text": "(?=) (?<=) (?!) (?<!)",
        "parsed_table": '[{"段":"(?=...)","含义":"正向先行断言：后面紧跟着 ..."},{"段":"(?<=...)","含义":"正向后行断言：前面紧跟着 ..."},{"段":"(?!...)","含义":"负向先行断言：后面不跟着 ..."},{"段":"(?<!...)","含义":"负向后行断言：前面不跟着 ..."}]',
        "code_block": "\\d+(?=px)   # 匹配后面有 px 的数字\n(?<=\\$)\\d+  # 匹配前面有 $ 的数字",
        "line_by_line": '[{"代码":"\\\\d+(?=px)","说明":"匹配像素值（不包含 px）"},{"代码":"(?<=\\\$)\\\\d+","说明":"匹配美元金额（不包含 $）"}]',
        "syntax_note": "零宽断言不消耗字符（不包含在匹配结果中）。后行断言 (?<=) 在部分引擎中不支持变长模式",
        "runnable_example": "# Python 示例\nimport re\nprint(re.findall(r\"\\d+(?=px)\", \"width: 100px\"))   # ['100']\nprint(re.findall(r\"(?<=\\$)\\d+\", \"price: $50\"))   # ['50']\nprint(re.findall(r\"\\d+(?!px)\", \"100px 200pt\"))    # ['20', '0', '200']",
        "common_errors": '[{"报错":"re.error: look-behind requires fixed-width pattern","解决办法":"后行断言中不能用 + * 等不定长量词"}]',
        "aliases": "前瞻,后顾,lookahead,lookbehind,断言",
    },
    {
        "title": "标志位 /g /i /m",
        "language": "正则表达式",
        "pattern_text": "/g /i /m /s",
        "parsed_table": '[{"段":"g","含义":"全局匹配，返回所有结果"},{"段":"i","含义":"忽略大小写"},{"段":"m","含义":"多行模式，^$ 匹配每行开头结尾"},{"段":"s","含义":"DOTALL，. 匹配换行符"}]',
        "code_block": "/hello/gi   # 全局忽略大小写匹配 hello\nre.findall(r\"hello\", text, re.I)",
        "line_by_line": '[{"代码":"/g","说明":"全局搜索"},{"代码":"/i","说明":"忽略大小写"},{"代码":"/m","说明":"多行模式"},{"代码":"/s","说明":"点号匹配换行"}]',
        "syntax_note": "各语言标志位写法不同：Python 用 re.I / re.M / re.S / re.U；JavaScript 用 /pattern/gim；PHP 用 /pattern/gim 修饰符",
        "runnable_example": "# Python 示例\nimport re\ntext = \"Hello\\nHELLO\\nhello\"\nprint(re.findall(r\"^hello\", text, re.IGNORECASE | re.MULTILINE))  # ['Hello', 'HELLO', 'hello']",
        "common_errors": '[{"报错":"跨平台移植时标志位不工作","解决办法":"确认目标语言或引擎的修饰符语法"}]',
        "aliases": "标志,flags,修饰符,modifier",
    },
]

# ── Markdown（10 条）──────────────────────────────────────

MARKDOWN_PATTERNS = [
    {
        "title": "标题",
        "language": "Markdown",
        "pattern_text": "# ## ### #### ##### ######",
        "parsed_table": '[{"段":"# 标题","含义":"一级标题（最大）"},{"段":"## 标题","含义":"二级标题"},{"段":"### 标题","含义":"三级标题"},{"段":"###### 标题","含义":"六级标题（最小）"}]',
        "code_block": "# 一级标题\n## 二级标题\n### 三级标题\n#### 四级标题\n##### 五级标题\n###### 六级标题",
        "line_by_line": '[{"代码":"# 标题","说明":"一级标题"},{"代码":"## 标题","说明":"二级标题"},{"代码":"### 标题","说明":"三级标题"}]',
        "syntax_note": "# 后必须跟一个空格。部分渲染器支持 Setext 风格（=== 表示一级，--- 表示二级）",
        "runnable_example": "# 这是一个一级标题\n\n## 这是一个二级标题\n\n正文内容...",
        "common_errors": '[{"报错":"标题不生效","解决办法":"检查 # 后面是否加了空格"},{"报错":"显示成普通文本","解决办法":"确认文件后缀为 .md"}]',
        "aliases": "heading,标题,markdown标题",
    },
    {
        "title": "加粗和斜体",
        "language": "Markdown",
        "pattern_text": "** *",
        "parsed_table": '[{"段":"**文本**","含义":"加粗"},{"段":"*文本*","含义":"斜体"},{"段":"***文本***","含义":"加粗+斜体"}]',
        "code_block": "**这是加粗文字**  \n*这是斜体文字*  \n***这是加粗斜体***",
        "line_by_line": '[{"代码":"**加粗**","说明":"粗体"},{"代码":"*斜体*","说明":"斜体"},{"代码":"***粗斜体***","说明":"加粗+斜体"}]',
        "syntax_note": "部分渲染器也支持 __下划线__ 表示加粗，_下划线_ 表示斜体。符号前后不能紧贴英文字母",
        "runnable_example": "这是普通文字，**这是加粗**，*这是斜体*，***这是粗斜体***。",
        "common_errors": '[{"报错":"加粗/斜体不生效","解决办法":"检查符号前后是否有空格干扰，或符号数量是否准确（2个=加粗，1个=斜体）"}]',
        "aliases": "粗体,斜体,bold,italic,强调",
    },
    {
        "title": "列表：无序和有序",
        "language": "Markdown",
        "pattern_text": "- * + 和 1. 2. 3.",
        "parsed_table": '[{"段":"- 项目","含义":"无序列表（可用 - * + 任一）"},{"段":"1. 项目","含义":"有序列表，自动编号"}]',
        "code_block": "- 苹果\n- 香蕉\n- 橙子\n\n1. 第一步\n2. 第二步\n3. 第三步",
        "line_by_line": '[{"代码":"- 项目","说明":"无序列表"},{"代码":"1. 项目","说明":"有序列表"}]',
        "syntax_note": "符号后必须有一个空格。有序列表的数字不一定连续，大多数渲染器会自动纠正。嵌套列表缩进 2-4 个空格",
        "runnable_example": "购物清单：\n- 牛奶\n- 面包\n  - 全麦面包\n- 鸡蛋\n\n步骤：\n1. 打开冰箱\n2. 放入食物\n3. 关上门",
        "common_errors": '[{"报错":"列表显示为普通文本","解决办法":"检查符号与文字之间是否有空格"},{"报错":"缩进不生效","解决办法":"子列表需要缩进 2-4 个空格"}]',
        "aliases": "无序列表,有序列表,bullet,numbered list",
    },
    {
        "title": "链接",
        "language": "Markdown",
        "pattern_text": "[text](url)",
        "parsed_table": '[{"段":"[显示文字]","含义":"链接显示的文本"},{"段":"(链接地址)","含义":"目标 URL"}]',
        "code_block": "[点击访问百度](https://www.baidu.com)\n[相对链接](./other.md)",
        "line_by_line": '[{"代码":"[文字](url)","说明":"行内链接"},{"代码":"[参考][id]","说明":"引用式链接（需在底部定义 [id]: url）"}]',
        "syntax_note": "链接文字中可以使用格式。引用式链接：`[Google][g]` 然后在文档任意位置 `[g]: https://google.com`",
        "runnable_example": "更多信息请访问 [我们的网站](https://example.com)。\n也可以写信给 [管理员](mailto:admin@example.com)。",
        "common_errors": '[{"报错":"链接无法点击","解决办法":"检查 URL 是否完整（含 https://）"},{"报错":"引用式链接不显示","解决办法":"确认引用定义在文档中只出现一次"}]',
        "aliases": "超链接,link,href",
    },
    {
        "title": "图片",
        "language": "Markdown",
        "pattern_text": "![alt](url)",
        "parsed_table": '[{"段":"!","含义":"感叹号表示图片（区别于链接）"},{"段":"[alt]","含义":"图片无法加载时显示的替代文字"},{"段":"(url)","含义":"图片路径或 URL"}]',
        "code_block": "![可爱的猫](./images/cat.jpg)\n![Logo](https://example.com/logo.png)",
        "line_by_line": '[{"代码":"![alt](url)","说明":"行内图片"},{"代码":"![alt][id]","说明":"引用式图片（需在底部定义 [id]: url）"}]',
        "syntax_note": "语法与链接的区别在于前面的 !。也支持引用式图片。可加标题：`![alt](url \"title\")`",
        "runnable_example": "![风景图片](https://picsum.photos/200/100)\n\n![本地图标](./images/icon.png \"应用图标\")",
        "common_errors": '[{"报错":"图片显示为断裂图标","解决办法":"检查路径是否正确，URL 是否可访问"},{"报错":"图片太大","解决办法":"用 HTML <img width=\"...\"> 控制尺寸"}]',
        "aliases": "图片,image,img,插图",
    },
    {
        "title": "代码块和行内代码",
        "language": "Markdown",
        "pattern_text": "``` 和 `",
        "parsed_table": '[{"段":"`代码`","含义":"行内代码"},{"段":"```\\n代码\\n```","含义":"多行代码块"},{"段":"```python","含义":"指定语言的代码块（语法高亮）"}]',
        "code_block": "使用 `print()` 函数输出内容。\n\n```python\ndef hello():\n    print(\"Hello, World!\")\n```",
        "line_by_line": '[{"代码":"`code`","说明":"行内代码"},{"代码":"```lang","说明":"围栏代码块（可指定语言）"}]',
        "syntax_note": "代码块有三种方式：缩进 4 空格（传统）、围栏 ```（推荐）、围栏 ~~~。可在开头 ``` 后加语言名启用语法高亮",
        "runnable_example": "安装依赖请运行 `pip install requests`。\n\n示例代码：\n```javascript\nconsole.log(\"Hello\");\n```",
        "common_errors": '[{"报错":"代码块不换行","解决办法":"行内代码用单反引号 `，多行用三重反引号 ```"},{"报错":"语法高亮无效","解决办法":"确认语言名称是否正确（如 python、javascript、bash）"}]',
        "aliases": "代码,code block,fence,反引号",
    },
    {
        "title": "引用",
        "language": "Markdown",
        "pattern_text": ">",
        "parsed_table": '[{"段":"> 文字","含义":"块引用（可嵌套）"},{"段":">> 文字","含义":"嵌套引用"}]',
        "code_block": "> 这是一段引用文字\n> 可以跨多行\n>\n> > 这是嵌套引用",
        "line_by_line": '[{"代码":"> 引用","说明":"一级引用"},{"代码":">> 引用","说明":"二级引用（嵌套）"}]',
        "syntax_note": "> 后加空格。引用内可包含其他 Markdown 元素（列表、代码、标题等）。空 > 表示段落分隔",
        "runnable_example": "> **注意**：引用中的内容也可以使用格式。\n>\n> - 列表项\n> - 另一项\n>\n> `代码` 也可以。",
        "common_errors": '[{"报错":"引用内的格式不渲染","解决办法":"部分渲染器对引用内的格式支持有限"},{"报错":"段落不换行","解决办法":"引用内的空行也需要加 >"}]',
        "aliases": "引用,blockquote,quote,块引用",
    },
    {
        "title": "表格",
        "language": "Markdown",
        "pattern_text": "| --- | --- |",
        "parsed_table": '[{"段":"| 标题 | 标题 |","含义":"表头行"},{"段":"| --- | --- |","含义":"分隔行（必须有）"},{"段":"| 内容 | 内容 |","含义":"数据行"}]',
        "code_block": "| 姓名 | 年龄 | 城市 |\n| ---- | ---- | ---- |\n| 张三 | 28   | 北京 |\n| 李四 | 32   | 上海 |",
        "line_by_line": '[{"代码":"| 姓名 | 年龄 |","说明":"表头"},{"代码":"| --- | --- |","说明":"分隔线"},{"代码":"| 张三 | 28 |","说明":"数据行"}]',
        "syntax_note": "分隔线中的 - 数量不限，至少一个。可用 : 对齐：`:---` 左对齐、`---:` 右对齐、`:---:` 居中",
        "runnable_example": "| 左对齐 | 居中 | 右对齐 |\n| :----- | :--: | -----: |\n| A      |  B   |      C |\n| D      |  E   |      F |",
        "common_errors": '[{"报错":"表格不渲染","解决办法":"确认分隔行（|---|）是否存在，列数是否一致"},{"报错":"列不对齐","解决办法":"虽然不要求对齐，但每行列数必须相同"}]',
        "aliases": "表格,table,对齐,alignment",
    },
    {
        "title": "分割线",
        "language": "Markdown",
        "pattern_text": "---",
        "parsed_table": '[{"段":"---","含义":"水平分割线（也支持 *** 或 ___）"}]',
        "code_block": "---\n***\n___\n\n以上三种写法效果相同",
        "line_by_line": '[{"代码":"---","说明":"三个或更多减号"},{"代码":"***","说明":"三个或更多星号"},{"代码":"___","说明":"三个或更多下划线"}]',
        "syntax_note": "一行中三个或更多连续的 - * _ 即成为分割线。前后建议空行。注意 --- 也可能被识别为 yaml front matter",
        "runnable_example": "第一章内容......\n\n---\n\n第二章内容......",
        "common_errors": '[{"报错":"-- 显示为标题","解决办法":"--- 上面一行不能是文本，需要空行分隔"},{"报错":"与 yaml front matter 冲突","解决办法":"文件最开头的 --- 会被解析为 front matter"}]',
        "aliases": "水平线,分割线,hr,horizontal rule",
    },
    {
        "title": "任务列表",
        "language": "Markdown",
        "pattern_text": "- [ ] - [x]",
        "parsed_table": '[{"段":"- [ ] 任务","含义":"未完成的任务"},{"段":"- [x] 任务","含义":"已完成的任务"}]',
        "code_block": "- [x] 已完成任务\n- [ ] 未完成任务\n- [ ] 另一项待办",
        "line_by_line": '[{"代码":"- [ ]","说明":"未勾选"},{"代码":"- [x]","说明":"已勾选"}]',
        "syntax_note": "[ ] 和 [x] 的大小写均可（[X] 也识别）。任务列表实际上是 GFM（GitHub Flavored Markdown）扩展",
        "runnable_example": "## 今日计划\n\n- [x] 写周报\n- [ ] 买菜\n- [ ] 锻炼\n- [ ] 看书",
        "common_errors": '[{"报错":"复选框不显示","解决办法":"确保渲染器支持 GFM 任务列表"},{"报错":"x 大写不识别","解决办法":"某些渲染器只识别小写 x"}]',
        "aliases": "任务列表,todo,task list,checkbox,GFM",
    },
]

# ── JSON 语法（8 条）─────────────────────────────────────

JSON_PATTERNS = [
    {
        "title": "对象 {}",
        "language": "JSON语法",
        "pattern_text": "{}",
        "parsed_table": '[{"段":"{ }","含义":"对象，无序的键值对集合"}]',
        "code_block": '{\n  "name": "张三",\n  "age": 28,\n  "city": "北京"\n}',
        "line_by_line": '[{"代码":"{","说明":"对象开始"},{"代码":"\"key\": value","说明":"键值对"},{"代码":"}","说明":"对象结束"}]',
        "syntax_note": "键必须用双引号包裹。值可以是字符串、数字、布尔值、null、对象或数组。键值对之间用逗号分隔",
        "runnable_example": '{"product": "笔记本电脑", "price": 5999, "inStock": true}',
        "common_errors": '[{"报错":"键没有双引号","解决办法":"JSON 要求键必须用双引号"},{"报错":"末尾多了一个逗号","解决办法":"最后一个键值对后面不能有逗号"}]',
        "aliases": "对象,object,键值对",
    },
    {
        "title": "数组 []",
        "language": "JSON语法",
        "pattern_text": "[]",
        "parsed_table": '[{"段":"[ ]","含义":"数组，有序的值列表"}]',
        "code_block": '[\n  "苹果",\n  "香蕉",\n  "橙子"\n]',
        "line_by_line": '[{"代码":"[","说明":"数组开始"},{"代码":"\"item\"","说明":"元素（可为任意类型）"},{"代码":"]","说明":"数组结束"}]',
        "syntax_note": "数组元素可以是不同类型的值：字符串、数字、对象、数组等。元素间用逗号分隔，末尾不能有多余逗号",
        "runnable_example": '["red", "green", "blue"]\n\n[1, 2, 3, 4, 5]\n\n[{"x": 1}, {"x": 2}]',
        "common_errors": '[{"报错":"解析错误：unexpected token","解决办法":"检查元素之间的逗号是否遗漏或多余"}]',
        "aliases": "数组,array,列表,list",
    },
    {
        "title": "字符串",
        "language": "JSON语法",
        "pattern_text": "\"\"",
        "parsed_table": '[{"段":"\"文本\"","含义":"字符串，必须用双引号包裹"},{"段":"\\\\转义","含义":"反斜杠转义序列"}]',
        "code_block": '"Hello, World!"\n"Line 1\\nLine 2"\n"她说：\\"你好\\""',
        "line_by_line": '[{"代码":"\"text\"","说明":"双引号字符串"},{"代码":"\\\\n","说明":"换行符转义"},{"代码":"\\\\\"","说明":"双引号转义"}]',
        "syntax_note": "JSON 字符串必须用双引号，不能用单引号。支持转义：\\\\ \" \\\\/ \\\\b \\\\f \\\\n \\\\r \\\\t \\\\uXXXX",
        "runnable_example": '{"message": "Hello", "path": "C:\\\\Users\\\\name"}',
        "common_errors": '[{"报错":"使用单引号","解决办法":"JSON 字符串必须用双引号"},{"报错":"中文乱码","解决办法":"确保 JSON 文件以 UTF-8 编码保存"}]',
        "aliases": "字符串,string,双引号",
    },
    {
        "title": "数字",
        "language": "JSON语法",
        "pattern_text": "数字",
        "parsed_table": '[{"段":"123","含义":"整数"},{"段":"3.14","含义":"浮点数"},{"段":"-42","含义":"负数"},{"段":"1.5e10","含义":"科学计数法"}]',
        "code_block": '{\n  "count": 42,\n  "price": 19.99,\n  "temperature": -5,\n  "distance": 1.5e10\n}',
        "line_by_line": '[{"代码":"42","说明":"整数"},{"代码":"19.99","说明":"浮点数"},{"代码":"-5","说明":"负数"},{"代码":"1.5e10","说明":"科学计数法"}]',
        "syntax_note": "数字无需引号。不支持八进制（如 0o77）、十六进制（0xFF）、前导零（如 0123）。NaN 和 Infinity 也不支持",
        "runnable_example": '{"age": 30, "score": 95.5, "offset": -10}',
        "common_errors": '[{"报错":"前导零报错","解决办法":"去掉数字前面的 0"},{"报错":"NaN 不被识别","解决办法":"NaN 不是合法 JSON，转为 null 或字符串"}]',
        "aliases": "数字,number,整数,浮点数",
    },
    {
        "title": "布尔值 true/false",
        "language": "JSON语法",
        "pattern_text": "true false",
        "parsed_table": '[{"段":"true","含义":"真"},{"段":"false","含义":"假"}]',
        "code_block": '{\n  "isActive": true,\n  "isAdmin": false\n}',
        "line_by_line": '[{"代码":"true","说明":"真值"},{"代码":"false","说明":"假值"}]',
        "syntax_note": "必须全部小写。True/False/FALSE/TRUE 都不是合法的 JSON 布尔值。不能用引号包裹（否则变成字符串）",
        "runnable_example": '{"enabled": true, "visible": false, "locked": true}',
        "common_errors": '[{"报错":"True 大写报错","解决办法":"JSON 布尔值必须小写 true/false"},{"报错":"\"true\" 是字符串","解决办法":"布尔值不加引号"}]',
        "aliases": "布尔值,boolean,bool,真假",
    },
    {
        "title": "null",
        "language": "JSON语法",
        "pattern_text": "null",
        "parsed_table": '[{"段":"null","含义":"空值，表示无数据"}]',
        "code_block": '{\n  "name": "张三",\n  "middleName": null,\n  "spouse": null\n}',
        "line_by_line": '[{"代码":"null","说明":"空值，无数据"}]',
        "syntax_note": "必须小写。null 与 undefined/None/nil 不同，JSON 中没有这些概念。使用 null 表示有键但值为空",
        "runnable_example": '{"title": "文章", "author": null, "published": true}',
        "common_errors": '[{"报错":"undefined 不是合法 JSON","解决办法":"用 null 代替 undefined"},{"报错":"None 报错","解决办法":"Python 的 None 在 json.dumps() 中自动转为 null"}]',
        "aliases": "空值,null,空,null值",
    },
    {
        "title": "嵌套结构",
        "language": "JSON语法",
        "pattern_text": "嵌套",
        "parsed_table": '[{"段":"对象套数组","含义":"值为数组的对象"},{"段":"数组套对象","含义":"数组中每个元素是一个对象"},{"段":"多层嵌套","含义":"任意深度"}]',
        "code_block": '{\n  "users": [\n    {\n      "name": "张三",\n      "hobbies": ["读书", "跑步"]\n    },\n    {\n      "name": "李四",\n      "hobbies": ["游泳"]\n    }\n  ]\n}',
        "line_by_line": '[{"代码":"\"users\": [...]","说明":"对象 → 数组"},{"代码":"{\"name\":...}","说明":"数组 → 对象"},{"代码":"\"hobbies\": [...]","说明":"对象 → 数组（更深一层）"}]',
        "syntax_note": "JSON 支持任意深度的嵌套。实际使用中注意深度不要过大以免解析性能问题。常见模式：数组包含对象，对象包含数组",
        "runnable_example": '{\n  "company": "ABC",\n  "departments": [\n    {\n      "name": "技术部",\n      "members": [\n        {"name": "张三", "role": "后端"},\n        {"name": "李四", "role": "前端"}\n      ]\n    }\n  ]\n}',
        "common_errors": '[{"报错":"括号不匹配","解决办法":"逐层检查括号是否成对"},{"报错":"层次太多难于调试","解决办法":"使用 JSON 格式化工具检查"}]',
        "aliases": "嵌套,nested,层级,递归",
    },
    {
        "title": "常见错误：尾逗号、单引号、注释",
        "language": "JSON语法",
        "pattern_text": "错误",
        "parsed_table": '[{"段":"尾逗号","含义":"最后一个元素后不能有逗号"},{"段":"单引号","含义":"必须用双引号"},{"段":"注释","含义":"JSON 不支持注释"}]',
        "code_block": '// ❌ 错误示例\n{\n  "name": "张三",   // 不支持注释\n  "age": 28,         // 尾逗号 ❌\n  \'city\': "北京",    // 单引号 ❌\n}                    // 尾逗号 ❌',
        "line_by_line": '[{"代码":"尾逗号","说明":"最后一项后面的逗号导致解析失败"},{"代码":"单引号","说明":"键和字符串必须双引号"},{"代码":"注释","说明":"JSON 不支持 // 或 /* */"}]',
        "syntax_note": "JSON5（JSON 的扩展）支持这些特性，但标准 JSON 不支持。使用 JSON5 解析器或在构建时预处理",
        "runnable_example": '# 正确 JSON\n{\n  "name": "张三",\n  "age": 28,\n  "city": "北京"\n}',
        "common_errors": '[{"报错":"尾逗号引发解析错误","解决办法":"移除最后一个键值对后的逗号"},{"报错":"单引号引发错误","解决办法":"将单引号替换为双引号"},{"报错":"注释引发错误","解决办法":"移除所有注释，或在构建前用工具去除"}]',
        "aliases": "常见错误,尾逗号,单引号,注释,trailing comma,JSON5",
    },
]

# ── YAML（6 条）─────────────────────────────────────────

YAML_PATTERNS = [
    {
        "title": "键值对 key: value",
        "language": "YAML",
        "pattern_text": "key: value",
        "parsed_table": '[{"段":"key: value","含义":"键值对，冒号后必须有空格"}]',
        "code_block": "name: 张三\nage: 28\ncity: 北京\nisStudent: false",
        "line_by_line": '[{"代码":"name: 张三","说明":"字符串值"},{"代码":"age: 28","说明":"数字值"},{"代码":"isStudent: false","说明":"布尔值"}]',
        "syntax_note": "冒号后必须有一个空格。键默认为字符串，无需引号。值可以是字符串、数字、布尔值、null、列表、字典",
        "runnable_example": "server:\n  host: localhost\n  port: 8080\n  debug: true",
        "common_errors": '[{"报错":"解析错误：mapping values are not allowed here","解决办法":"检查冒号后是否有空格"}]',
        "aliases": "键值对,mapping,key-value",
    },
    {
        "title": "嵌套缩进",
        "language": "YAML",
        "pattern_text": "缩进",
        "parsed_table": '[{"段":"空格缩进","含义":"用空格表示层级（不使用制表符）"}]',
        "code_block": "person:\n  name: 张三\n  address:\n    city: 北京\n    street: 长安街",
        "line_by_line": '[{"代码":"person:","说明":"一级键"},{"代码":"  name:","说明":"二级（2 空格缩进）"},{"代码":"    address:","说明":"三级（4 空格缩进）"}]',
        "syntax_note": "YAML 用空格缩进表示层级，禁止使用 Tab。同层必须保持相同缩进量。通常用 2 空格",
        "runnable_example": "database:\n  host: localhost\n  port: 5432\n  credentials:\n    user: admin\n    password: secret",
        "common_errors": '[{"报错":"found a tab character where an indentation space is expected","解决办法":"将 Tab 替换为空格"},{"报错":"缩进不一致","解决办法":"确保同层级缩进空格数相同"}]',
        "aliases": "缩进,indentation,层级,嵌套",
    },
    {
        "title": "列表 -",
        "language": "YAML",
        "pattern_text": "- item",
        "parsed_table": '[{"段":"- 项目","含义":"列表项，减号后必须有空格"}]',
        "code_block": "fruits:\n  - 苹果\n  - 香蕉\n  - 橙子\n\ncolors:\n  - red\n  - green\n  - blue",
        "line_by_line": '[{"代码":"- 苹果","说明":"列表项"},{"代码":"- red","说明":"另一列表项"}]',
        "syntax_note": "- 后必须有一个空格。列表项可以嵌套：`- key: value` 或 `- - item`（内嵌列表）。缩进对齐即可",
        "runnable_example": "todo:\n  - 买牛奶\n  - 写代码\n  - 锻炼身体\n\nconfig:\n  - name: app\n    port: 3000\n  - name: api\n    port: 4000",
        "common_errors": '[{"报错":"列表项不识别","解决办法":"检查 - 后是否有空格"},{"报错":"列表项层级错乱","解决办法":"确保缩进对齐"}]',
        "aliases": "列表,list,array,序列",
    },
    {
        "title": "多行字符串 | >",
        "language": "YAML",
        "pattern_text": "| >",
        "parsed_table": '[{"段":"|","含义":"保留换行的多行字符串"},{"段":">","含义":"折叠换行为空格的多行字符串"}]',
        "code_block": "description: |\n  第一行\n  第二行\n  第三行\n\nsummary: >\n  这是一段很长的文字\n  会被折叠成一行\n  在最终输出中",
        "line_by_line": '[{"代码":"|","说明":"保留换行"},{"代码":">","说明":"折叠换行（变空格）"}]',
        "syntax_note": "| 保留原文中的换行符；> 将换行符替换为空格（段落折叠）。可在 | 后加数字（如 |2）指定缩进量",
        "runnable_example": "poem: |\n  床前明月光\n  疑是地上霜\n  举头望明月\n  低头思故乡\n\nnote: >\n  这是一条备注\n  即使写了多行\n  也会变成一句话",
        "common_errors": '[{"报错":"多行字符串缩进问题","解决办法":"多行内容必须缩进在键的下一层"}]',
        "aliases": "多行字符串,literal,folded,multiline,block scalar",
    },
    {
        "title": "锚点与引用 & *",
        "language": "YAML",
        "pattern_text": "& *",
        "parsed_table": '[{"段":"&alias","含义":"定义锚点"},{"段":"*alias","含义":"引用锚点（复制内容）"},{"段":"<<: *alias","含义":"合并锚点（merge key 扩展）"}]',
        "code_block": "defaults: &defaults\n  adapter: postgres\n  host: localhost\n\ndevelopment:\n  <<: *defaults\n  database: dev_db\n\nproduction:\n  <<: *defaults\n  host: prod.example.com\n  database: prod_db",
        "line_by_line": '[{"代码":"&defaults","说明":"定义锚点名为 defaults"},{"代码":"*defaults","说明":"引用锚点内容"},{"代码":"<<: *defaults","说明":"合并锚点内容到当前映射"}]',
        "syntax_note": "锚点用 & 定义，用 * 引用。<<: 是 YAML 的 merge key 扩展（非标准 JSON 兼容部分），用于合并映射",
        "runnable_example": "shared: &shared\n  timeout: 30\n  retries: 3\n\nservice_a:\n  <<: *shared\n  url: /api/a\n\nservice_b:\n  <<: *shared\n  url: /api/b\n  timeout: 60  # 可覆盖",
        "common_errors": '[{"报错":"anchor not found","解决办法":"检查 & 定义是否在 * 引用之前"},{"报错":"循环引用","解决办法":"避免锚点互相引用形成循环"}]',
        "aliases": "锚点,引用,anchor,alias,merge,复用",
    },
    {
        "title": "注释 #",
        "language": "YAML",
        "pattern_text": "#",
        "parsed_table": '[{"段":"# 注释","含义":"行内注释，从 # 开始到行尾"}]',
        "code_block": "# 这是一个注释\nport: 8080  # 服务端口号\nhost: localhost  # 主机地址",
        "line_by_line": '[{"代码":"# 注释","说明":"整行注释"},{"代码":"  # 行尾注释","说明":"行尾注释"}]',
        "syntax_note": "# 可以在行首或行中使用。不支持块注释（多行连续 #）。注释不能出现在 YAML 值中间",
        "runnable_example": "# 项目配置\n# 作者：张三\n\nserver:\n  host: localhost  # 开发环境\n  port: 3000\n\n# 以下为数据库配置\ndatabase:\n  url: sqlite:///app.db",
        "common_errors": '[{"报错":"注释位置导致解析错误","解决办法":"注释不能出现在值中间，如 key: va#lue 不合法"}]',
        "aliases": "注释,comment,#,行注释",
    },
]

# ── 主流程 ────────────────────────────────────────────────

def get_category_id(db, name):
    """通过分类名称查询 id"""
    _, name_id = db.get_all_categories_map()
    if name not in name_id:
        print(f"[WARN] 分类 '{name}' 不存在，跳过")
        return None
    return name_id[name]


def insert_patterns(db, cat_id, patterns):
    """批量插入模式条目"""
    if cat_id is None:
        return
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
            print(f"  ✓ {p['title']}")
        except Exception as e:
            print(f"  ✗ {p['title']}: {e}")
    print(f"  共插入 {count} 条\n")


def main():
    print("=" * 50)
    print("模式/标记语言 种子数据导入")
    print("=" * 50)

    # 初始化 DB（如未初始化）
    db = DBManager(DB_PATH)
    db.init_db()
    print(f"[DB] 数据库就绪: {DB_PATH}\n")

    # 获取分类 ID
    cat_map = {
        "正则表达式": get_category_id(db, "正则表达式"),
        "Markdown": get_category_id(db, "Markdown"),
        "JSON语法": get_category_id(db, "JSON语法"),
        "YAML": get_category_id(db, "YAML"),
    }

    for name, cid in cat_map.items():
        if cid is None:
            print(f"[WARN] 分类 '{name}' 未找到，请确认数据库已包含该分类\n")
        else:
            print(f"[INFO] 分类 '{name}' → id={cid}")

    # 插入数据
    print("\n── 正则表达式（12 条）──")
    insert_patterns(db, cat_map["正则表达式"], REGEX_PATTERNS)

    print("── Markdown（10 条）──")
    insert_patterns(db, cat_map["Markdown"], MARKDOWN_PATTERNS)

    print("── JSON 语法（8 条）──")
    insert_patterns(db, cat_map["JSON语法"], JSON_PATTERNS)

    print("── YAML（6 条）──")
    insert_patterns(db, cat_map["YAML"], YAML_PATTERNS)

    # 统计
    total = (len(REGEX_PATTERNS) + len(MARKDOWN_PATTERNS) +
             len(JSON_PATTERNS) + len(YAML_PATTERNS))
    print(f"\n✅ 全部完成！共插入 {total} 条模式条目")


if __name__ == "__main__":
    main()
