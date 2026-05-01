#!/usr/bin/env python3
"""种子数据：代码片段（Python/JS/Rust/Java/C/HTML/CSS/Vue/React）"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

db = DBManager()
db.init_db()

def get_cat(parent, child):
    """根据父分类和子分类名获取 category_id"""
    cats = db.get_categories()
    id_map = {}
    # 先收集所有分类的(id, name, parent_id)
    for root in db.get_categories(parent_id=None):
        for child_cat in db.get_categories(parent_id=root['id']):
            if root['name'] == parent and child_cat['name'] == child:
                return child_cat['id']
    return None

# ==========================================================
# Python 片段（20条）
# ==========================================================
python_cat = get_cat('编程语言', 'Python')
if python_cat:
    snippets = [
        {
            'title': '读取CSV文件并打印前5行',
            'language': 'Python',
            'version': '>=3.7',
            'code_block': 'import pandas as pd\n\ndf = pd.read_csv("data.csv")\nprint(df.head())',
            'line_by_line': '[{"代码":"import pandas as pd","说明":"导入pandas数据处理库，简写为pd"},{"代码":"df = pd.read_csv(\\"data.csv\\")","说明":"读取CSV文件到DataFrame对象"},{"代码":"print(df.head())","说明":"打印前5行数据，默认显示5行"}]',
            'syntax_note': '确保已安装pandas: pip install pandas\\n文件路径可用绝对路径或相对路径\\n如果CSV文件含中文，需加 encoding="utf-8" 参数',
            'runnable_example': '# 假设 data.csv 内容：\\n# name,age,city\\n# 张三,28,北京\\n# 李四,25,上海\\nimport pandas as pd\\ndf = pd.read_csv("data.csv")\\nprint(df.head())',
            'common_errors': '[{"报错":"FileNotFoundError","解决办法":"检查路径是否正确，文件是否存在"},{"报错":"UnicodeDecodeError","解决办法":"加 encoding=\\"utf-8\\" 或 encoding=\\"gbk\\""},{"报错":"ModuleNotFoundError: pandas","解决办法":"运行 pip install pandas"}]',
            'aliases': 'csv读取,读文件,pandas,数据分析',
        },
        {
            'title': '读取JSON文件',
            'language': 'Python',
            'version': '>=3.6',
            'code_block': 'import json\n\nwith open("data.json", "r", encoding="utf-8") as f:\n    data = json.load(f)\nprint(data)',
            'line_by_line': '[{"代码":"import json","说明":"导入json标准库"},{"代码":"with open(...) as f","说明":"以只读模式打开文件，with自动关闭"},{"代码":"data = json.load(f)","说明":"将JSON文件内容解析为Python字典/列表"},{"代码":"print(data)","说明":"打印读取的数据"}]',
            'syntax_note': 'JSON文件必须使用双引号，不能用单引号\\njson.load() 从文件读取，json.loads() 从字符串读取',
            'runnable_example': '# 假设 data.json 内容：\\n# {"name": "张三", "age": 28, "city": "北京"}\\nimport json\\nwith open("data.json", "r", encoding="utf-8") as f:\\n    data = json.load(f)\\nprint(data["name"])  # 张三',
            'common_errors': '[{"报错":"json.decoder.JSONDecodeError","解决办法":"检查JSON格式是否合法，键必须用双引号"},{"报错":"FileNotFoundError","解决办法":"检查文件路径"}]',
            'aliases': 'json读取,读json,json文件',
        },
        {
            'title': '写入文本文件',
            'language': 'Python',
            'version': '>=3.6',
            'code_block': 'with open("output.txt", "w", encoding="utf-8") as f:\n    f.write("Hello, World!\\n")\n    f.write("第二行内容\\n")',
            'line_by_line': '[{"代码":"with open(...) as f","说明":"打开文件，w表示写入模式，文件不存在则创建"},{"代码":"f.write(...)","说明":"写入一行文本，\\\\n表示换行"}]',
            'syntax_note': '"w"模式会覆盖已有文件，"a"模式追加内容\\n记得写 encoding="utf-8" 支持中文\\nwith语句结束后自动关闭文件，不用手动f.close()',
            'runnable_example': 'with open("hello.txt", "w", encoding="utf-8") as f:\\n    f.write("你好，世界！\\n")\\n    f.write("这是第二行\\n")\\n# 执行后同级目录会生成 hello.txt',
            'common_errors': '[{"报错":"PermissionError","解决办法":"没有写入权限，换个目录试试"},{"报错":"FileNotFoundError","解决办法":"父目录不存在，先os.makedirs()创建"}]',
            'aliases': '写文件,文件写入,输出文件',
        },
        {
            'title': '列表推导式创建新列表',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': '# 生成1-10的平方列表\nsquares = [x**2 for x in range(1, 11)]\nprint(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]\n\n# 带条件的列表推导式\neven_squares = [x**2 for x in range(1, 11) if x % 2 == 0]\nprint(even_squares)  # [4, 16, 36, 64, 100]',
            'line_by_line': '[{"代码":"[x**2 for x in range(1, 11)]","说明":"对1-10每个数求平方，生成新列表"},{"代码":"if x % 2 == 0","说明":"条件过滤，只保留偶数"},{"代码":"x**2","说明":"x的平方运算"}]',
            'syntax_note': '列表推导式结构：[表达式 for 变量 in 可迭代对象 if 条件]\\n比传统的for循环更简洁高效\\n不要嵌套太深，超过两个for可读性会下降',
            'runnable_example': '# 传统写法 vs 推导式\\nnums = []\\nfor x in range(1, 6):\\n    nums.append(x * 2)\\n# 等效推导式\\nnums = [x * 2 for x in range(1, 6)]  # [2, 4, 6, 8, 10]',
            'common_errors': '[{"报错":"语法错误(意外缩进)","解决办法":"检查推导式中的冒号和缩进"}]',
            'aliases': '列表生成式,list comprehension,推导式',
        },
        {
            'title': 'for循环遍历字典',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'user = {"name": "张三", "age": 28, "city": "北京"}\n\n# 遍历键\nfor key in user:\n    print(key)\n\n# 遍历键值对\nfor key, value in user.items():\n    print(f"{key}: {value}")\n\n# 遍历值\nfor value in user.values():\n    print(value)',
            'line_by_line': '[{"代码":"for key in user:","说明":"默认遍历字典的键"},{"代码":"user.items()","说明":"返回键值对元组的视图"},{"代码":"user.values()","说明":"返回所有值的视图"},{"代码":"f\\"{key}: {value}\\"","说明":"f-string格式化字符串"}]',
            'syntax_note': '遍历字典时不要修改字典大小（增删键），会报错\\n.items() 返回的是视图，不是副本，但遍历是安全的\\nPython 3.7+ 字典保持插入顺序',
            'runnable_example': 'scores = {"语文": 90, "数学": 95, "英语": 88}\\ntotal = 0\\nfor subject, score in scores.items():\\n    print(f"{subject}: {score}分")\\n    total += score\\nprint(f"总分: {total}")',
            'common_errors': '[{"报错":"RuntimeError: dictionary changed size during iteration","解决办法":"不要在循环中增删字典键"}]',
            'aliases': '字典遍历,dict遍历,items方法',
        },
        {
            'title': '函数定义与默认参数',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'def greet(name, greeting="你好"):\n    """向指定用户发送问候"""\n    return f"{greeting}，{name}！"\n\nprint(greet("张三"))          # 你好，张三！\nprint(greet("John", "Hello"))  # Hello，John！',
            'line_by_line': '[{"代码":"def greet(name, greeting=\\"你好\\"):","说明":"定义函数，greeting有默认值\\"你好\\""},{"代码":"\"\"\"向指定用户发送问候\"\"\"","说明":"文档字符串，描述函数功能"},{"代码":"return f...","说明":"返回格式化的问候语"}]',
            'syntax_note': '默认参数必须放在必选参数后面\\n默认参数在函数定义时计算一次，不要用可变对象如[]作为默认值\\n用 def func(x, lst=None): 替代 def func(x, lst=[]):',
            'runnable_example': '# 默认参数陷阱示例\\ndef add_item(item, lst=None):\\n    if lst is None:\\n        lst = []\\n    lst.append(item)\\n    return lst\\n\\nprint(add_item("a"))  # ["a"]\\nprint(add_item("b"))  # ["b"] (正确)',
            'common_errors': '[{"报错":"可变默认参数共享","解决办法":"用 None + if 判断来初始化"}]',
            'aliases': '函数定义,默认参数,def,函数',
        },
        {
            'title': '异常处理 try/except',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'try:\n    num = int(input("请输入一个数字: "))\n    result = 10 / num\n    print(f"结果是: {result}")\nexcept ValueError:\n    print("错误：请输入有效的整数！")\nexcept ZeroDivisionError:\n    print("错误：除数不能为零！")\nexcept Exception as e:\n    print(f"未知错误：{e}")\nelse:\n    print("计算成功完成！")\nfinally:\n    print("程序结束。")',
            'line_by_line': '[{"代码":"try:","说明":"尝试执行可能出错的代码"},{"代码":"except ValueError:","说明":"捕获特定类型错误：值错误"},{"代码":"except Exception as e:","说明":"捕获所有其他异常，e保存错误信息"},{"代码":"else:","说明":"没有异常时执行"},{"代码":"finally:","说明":"无论是否异常都执行"}]',
            'syntax_note': '尽量捕获具体的异常类型，少用裸except:\\nelse 和 finally 是可选的\\n多个except按顺序匹配，第一个匹配的会被执行',
            'runnable_example': 'def safe_divide(a, b):\\n    try:\\n        return a / b\\n    except ZeroDivisionError:\\n        return "不能除以零"\\n\\nprint(safe_divide(10, 2))  # 5.0\\nprint(safe_divide(10, 0))  # 不能除以零',
            'common_errors': '[{"报错":"捕获范围太广","解决办法":"尽量指定具体异常类型"}]',
            'aliases': '异常处理,try except,错误处理',
        },
        {
            'title': '正则提取文本中的邮箱',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'import re\n\ntext = "请联系 support@example.com 或 admin@test.org"\npattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"\nemails = re.findall(pattern, text)\nprint(emails)  # ["support@example.com", "admin@test.org"]',
            'line_by_line': '[{"代码":"import re","说明":"导入正则模块"},{"代码":"r\\"...\\"","说明":"raw string，反斜杠不会转义"},{"代码":"[a-zA-Z0-9._%+-]+","说明":"邮箱用户名部分：字母数字和特殊字符"},{"代码":"@","说明":"匹配@符号"},{"代码":"[a-zA-Z0-9.-]+","说明":"域名部分"},{"代码":"\\\\.[a-zA-Z]{2,}","说明":"点号+顶级域名（如.com至少2个字母）"},{"代码":"re.findall(pattern, text)","说明":"找出所有匹配的字符串，返回列表"}]',
            'syntax_note': '正则前加 r 避免反斜杠转义问题\\nre.findall() 返回所有匹配\\nre.search() 返回第一个匹配对象\\nre.match() 从字符串开头匹配',
            'runnable_example': 'import re\\ntext = "我的邮箱是 zhangsan@gmail.com，备用邮箱是 lisi@163.com"\\nemails = re.findall(r"[\\w.]+@[\\w.]+\\.[a-z]+", text)\\nprint(f"找到了 {len(emails)} 个邮箱: {emails}")',
            'common_errors': '[{"报错":"re.error: bad escape","解决办法":"在正则字符串前加 r"},{"报错":"匹配不到","解决办法":"检查正则表达式是否正确"}]',
            'aliases': '正则提取,邮箱匹配,re模块',
        },
        {
            'title': '字符串格式化 f-string',
            'language': 'Python',
            'version': '>=3.6',
            'code_block': 'name = "张三"\nage = 28\nheight = 1.75\n\n# 基本用法\nprint(f"我叫{name}，今年{age}岁")\n\n# 数字格式化\nprint(f"身高: {height:.2f}米")   # 身高: 1.75米\nprint(f"比例: {age/100:.1%}")    # 比例: 28.0%\n\n# 表达式\nprint(f"明年{age+1}岁")\nprint(f"姓名: {name.upper()}")',
            'line_by_line': '[{"代码":"f\\"...{变量}...\\"","说明":"f前缀的字符串，花括号内放变量或表达式"},{"代码":"{height:.2f}","说明":".2f保留两位小数"},{"代码":"{age/100:.1%}","说明":".1%格式化为百分比"}]',
            'syntax_note': 'f-string 在 Python 3.6 引入\\n花括号内可以放任何Python表达式\\n字符串本身包含花括号需写 {{ 或 }}',
            'runnable_example': 'score = 85.5\\ntotal = 100\\nprint(f"得分: {score}/{total} = {score/total:.1%}")\\n# 输出: 得分: 85.5/100 = 85.5%',
            'common_errors': '[{"报错":"f-string: unmatched \'{\'","解决办法":"检查花括号是否成对"}]',
            'aliases': 'fstring,f-string,字符串格式化,格式化',
        },
        {
            'title': '日期时间处理',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'from datetime import datetime, timedelta\n\n# 当前时间\nnow = datetime.now()\nprint(f"当前时间: {now}")\n\n# 格式化输出\nprint(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2024-01-15 14:30:00\n\n# 字符串转日期\ndate_str = "2024-01-15"\ndate_obj = datetime.strptime(date_str, "%Y-%m-%d")\nprint(date_obj.weekday())  # 0=周一\n\n# 日期加减\ntomorrow = now + timedelta(days=1)\nlast_week = now - timedelta(weeks=1)',
            'line_by_line': '[{"代码":"from datetime import datetime, timedelta","说明":"导入日期时间模块"},{"代码":"datetime.now()","说明":"获取当前系统时间"},{"代码":"strftime(\\"%Y-%m-%d\\")","说明":"将日期格式化为字符串，%Y=年 %m=月 %d=日"},{"代码":"strptime(str, format)","说明":"将字符串解析为日期对象"},{"代码":"timedelta(days=1)","说明":"时间增量，可用于日期加减"}]',
            'syntax_note': 'strftime 是日期→字符串\\nstrptime 是字符串→日期（注意区分 p 和 f）\\n星期一是0，星期日是6\\n时区问题：datetime.now() 获取本地时间',
            'runnable_example': 'from datetime import datetime\\n# 计算距离元旦还有多少天\\nnew_year = datetime(2025, 1, 1)\\ntoday = datetime.now()\\ndelta = new_year - today\\nprint(f"距离2025年元旦还有 {delta.days} 天")',
            'common_errors': '[{"报错":"ValueError: unconverted data remains","解决办法":"检查格式字符串是否完全匹配输入字符串"}]',
            'aliases': '日期,时间,datetime,strftime',
        },
        {
            'title': '类定义与继承',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'class Animal:\n    """动物基类"""\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        raise NotImplementedError("子类必须实现此方法")\n\n\nclass Dog(Animal):\n    """狗类，继承Animal"""\n    def speak(self):\n        return f"{self.name}说: 汪汪！"\n\n\nclass Cat(Animal):\n    """猫类，继承Animal"""\n    def speak(self):\n        return f"{self.name}说: 喵喵！"\n\n\n# 使用\ndog = Dog("旺财")\ncat = Cat("咪咪")\nprint(dog.speak())  # 旺财说: 汪汪！\nprint(cat.speak())  # 咪咪说: 喵喵！',
            'line_by_line': '[{"代码":"class Animal:","说明":"定义类"},{"代码":"def __init__(self, name):","说明":"构造函数，创建对象时自动调用"},{"代码":"self.name = name","说明":"实例属性"},{"代码":"class Dog(Animal):","说明":"Dog继承Animal"},{"代码":"def speak(self):","说明":"重写父类的speak方法（多态）"}]',
            'syntax_note': '所有方法第一个参数必须是 self\\n__init__ 相当于其他语言的构造函数\\nPython支持多重继承：class A(B, C):\\n子类可以重写父类的任何方法',
            'runnable_example': 'class Student:\\n    def __init__(self, name, score):\\n        self.name = name\\n        self.score = score\\n    \\n    def grade(self):\\n        if self.score >= 90: return "A"\\n        elif self.score >= 80: return "B"\\n        else: return "C"\\n\\ns = Student("张三", 85)\\nprint(f"{s.name}: {s.grade()}")  # 张三: B',
            'common_errors': '[{"报错":"TypeError: __init__() missing 1 required positional argument","解决办法":"检查创建对象时是否传了所有必选参数"}]',
            'aliases': '类,继承,面向对象,oop,class',
        },
        {
            'title': '使用requests发送HTTP请求',
            'language': 'Python',
            'version': '>=3.6',
            'code_block': 'import requests\n\n# GET请求\nresponse = requests.get("https://api.github.com")\nprint(response.status_code)   # 200\nprint(response.json())         # 解析JSON响应\n\n# POST请求（带JSON数据）\ndata = {"name": "张三", "age": 28}\nresponse = requests.post("https://httpbin.org/post", json=data)\nprint(response.text)           # 原始响应文本\n\n# 带查询参数\nparams = {"q": "python", "page": 1}\nresponse = requests.get("https://api.github.com/search/repositories", params=params)',
            'line_by_line': '[{"代码":"import requests","说明":"导入requests第三方库"},{"代码":"requests.get(url)","说明":"发送GET请求"},{"代码":"response.status_code","说明":"HTTP状态码，200=成功"},{"代码":"response.json()","说明":"将响应解析为Python字典"},{"代码":"requests.post(url, json=data)","说明":"发送POST请求，数据自动序列化为JSON"},{"代码":"params=params","说明":"URL查询参数"}]',
            'syntax_note': 'requests需要安装: pip install requests\\nresponse.json() 可能抛出异常，如果响应不是合法JSON\\n建议用 try/except 包裹网络请求',
            'runnable_example': 'import requests\\ntry:\\n    r = requests.get("https://api.github.com", timeout=5)\\n    print(f"状态: {r.status_code}")\\n    print(f"API版本: {r.json()[\\"current_user_url\\"]}")\\nexcept requests.RequestException as e:\\n    print(f"请求失败: {e}")',
            'common_errors': '[{"报错":"requests.exceptions.ConnectionError","解决办法":"检查网络连接"},{"报错":"requests.exceptions.Timeout","解决办法":"请求超时，设置timeout参数"},{"报错":"ModuleNotFoundError","解决办法":"pip install requests"}]',
            'aliases': 'http请求,网络请求,requests,api调用',
        },
        {
            'title': '多线程 threading',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'import threading\nimport time\n\ndef work(name, seconds):\n    print(f"线程 {name} 开始工作")\n    time.sleep(seconds)\n    print(f"线程 {name} 完成工作")\n\n# 创建线程\nthreads = []\nfor i in range(3):\n    t = threading.Thread(target=work, args=(f"T{i}", i+1))\n    threads.append(t)\n    t.start()\n\n# 等待所有线程完成\nfor t in threads:\n    t.join()\n\nprint("所有线程已完成")',
            'line_by_line': '[{"代码":"import threading","说明":"导入多线程模块"},{"代码":"target=work, args=(...)","说明":"指定线程执行的函数和参数"},{"代码":"t.start()","说明":"启动线程"},{"代码":"t.join()","说明":"等待线程执行完毕"}]',
            'syntax_note': 'start() 启动线程，join() 等待线程结束\\n多线程适用于I/O密集型任务（网络请求、文件读写）\\nCPU密集型任务用 multiprocessing 模块',
            'runnable_example': 'import threading, time\\n\\ndef count_down(name, n):\\n    while n > 0:\\n        print(f"{name}: {n}")\\n        time.sleep(0.5)\\n        n -= 1\\n\\nt1 = threading.Thread(target=count_down, args=("A", 3))\\nt2 = threading.Thread(target=count_down, args=("B", 3))\\nt1.start()\\nt2.start()\\nt1.join()\\nt2.join()\\nprint("倒计时结束！")',
            'common_errors': '[{"报错":"RuntimeError: threads can only be started once","解决办法":"每个线程只能start一次，需要重复执行就新建线程"}]',
            'aliases': '多线程,threading,并发,并行',
        },
        {
            'title': 'os.path文件路径操作',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'import os\n\n# 路径拼接\npath = os.path.join("data", "images", "photo.jpg")\nprint(path)  # data/images/photo.jpg\n\n# 获取路径各部分\nprint(os.path.basename(path))  # photo.jpg\nprint(os.path.dirname(path))   # data/images\nprint(os.path.splitext(path))  # ("data/images/photo", ".jpg")\n\n# 判断路径类型\nprint(os.path.exists(path))    # 文件/文件夹是否存在\nprint(os.path.isfile(path))    # 是否是文件\nprint(os.path.isdir(path))     # 是否是目录\n\n# 获取绝对路径\nprint(os.path.abspath("."))    # 当前目录绝对路径',
            'line_by_line': '[{"代码":"os.path.join()","说明":"跨平台路径拼接，自动处理斜杠方向"},{"代码":"os.path.basename()","说明":"获取文件名部分"},{"代码":"os.path.dirname()","说明":"获取目录部分"},{"代码":"os.path.splitext()","说明":"分割文件名和扩展名，返回元组"},{"代码":"os.path.exists()","说明":"判断路径是否存在"}]',
            'syntax_note': 'os.path.join() 会自动使用正确的路径分隔符（Windows用\\\\，Linux用/）\\n推荐用 pathlib.Path 替代 os.path（Python 3.4+）\\nos.path 只是字符串操作，不会访问磁盘',
            'runnable_example': 'import os\\n# 遍历目录下所有txt文件\\nfolder = "."\\nfor f in os.listdir(folder):\\n    if f.endswith(".txt"):\\n        full_path = os.path.join(folder, f)\\n        size = os.path.getsize(full_path)\\n        print(f"{f}: {size} bytes")',
            'common_errors': '[]',
            'aliases': '路径操作,os.path,文件路径',
        },
        {
            'title': '使用argparse解析命令行参数',
            'language': 'Python',
            'version': '>=3.2',
            'code_block': 'import argparse\n\nparser = argparse.ArgumentParser(description="文件处理工具")\nparser.add_argument("input", help="输入文件路径")\nparser.add_argument("-o", "--output", help="输出文件路径", default="output.txt")\nparser.add_argument("-v", "--verbose", help="显示详细信息", action="store_true")\nparser.add_argument("--count", help="处理次数", type=int, default=1)\n\nargs = parser.parse_args()\n\nif args.verbose:\n    print(f"输入: {args.input}")\n    print(f"输出: {args.output}")\n    print(f"次数: {args.count}")\nprint(f"正在处理 {args.input}...")',
            'line_by_line': '[{"代码":"ArgumentParser(description=...)","说明":"创建参数解析器，description显示帮助信息"},{"代码":"add_argument(\\"input\\")","说明":"添加位置参数（必填）"},{"代码":"add_argument(\\"-o\\", \\"--output\\")","说明":"添加可选参数，-o是短格式，--output是长格式"},{"代码":"default=\\"output.txt\\"","说明":"设置默认值，用户不传则使用"},{"代码":"action=\\"store_true\\"","说明":"开关型参数，传了就为True"},{"代码":"type=int","说明":"指定参数类型，自动转换"}]',
            'syntax_note': '位置参数按顺序解析，可选参数用 - 或 -- 开头\\n使用 python script.py -h 查看帮助\\ntype=int 会自动做类型转换，无效时报错',
            'runnable_example': '# 运行命令：\\n# python script.py data.txt -o result.txt -v --count 3\\n\\nimport argparse\\nparser = argparse.ArgumentParser()\\nparser.add_argument("name", help="你的名字")\\nparser.add_argument("--age", type=int, help="年龄")\\nargs = parser.parse_args()\\nprint(f"你好 {args.name}!")\\nif args.age:\\n    print(f"你 {args.age} 岁了")',
            'common_errors': '[{"报错":"unrecognized arguments","解决办法":"检查参数名拼写"},{"报错":"expected one argument","解决办法":"可选参数需要传值"}]',
            'aliases': '命令行参数,argparse,参数解析',
        },
        {
            'title': 'enumerate同时获取索引和值',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'fruits = ["苹果", "香蕉", "橙子"]\n\n# 传统方式\nfor i in range(len(fruits)):\n    print(i, fruits[i])\n\n# enumerate方式（推荐）\nfor i, fruit in enumerate(fruits):\n    print(f"{i}: {fruit}")\n\n# 指定起始编号\nfor i, fruit in enumerate(fruits, start=1):\n    print(f"第{i}个: {fruit}")',
            'line_by_line': '[{"代码":"enumerate(fruits)","说明":"返回(索引, 元素)的迭代器"},{"代码":"enumerate(fruits, start=1)","说明":"从1开始编号"},{"代码":"for i, fruit in enumerate(...)","说明":"解包元组，同时获取索引和值"}]',
            'syntax_note': 'enumerate 比 range(len()) 更简洁、更Pythonic\\nstart 参数指定起始值，默认为0\\nenumerate 返回的是迭代器，惰性求值',
            'runnable_example': 'shopping = ["牛奶", "面包", "鸡蛋"]\\nprint("购物清单:")\\nfor i, item in enumerate(shopping, 1):\\n    print(f"  {i}. {item}")',
            'common_errors': '[]',
            'aliases': '枚举,索引循环,enumerate',
        },
        {
            'title': 'zip合并两个列表',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'names = ["张三", "李四", "王五"]\nscores = [90, 85, 95]\n\n# 合并两个列表\nfor name, score in zip(names, scores):\n    print(f"{name}: {score}分")\n\n# 创建字典\ndict1 = dict(zip(names, scores))\nprint(dict1)  # {"张三": 90, "李四": 85, "王五": 95}\n\n# 解压缩：把键值对拆开\nkeys, values = zip(*dict1.items())\nprint(keys)    # ("张三", "李四", "王五")\nprint(values)  # (90, 85, 95)',
            'line_by_line': '[{"代码":"zip(names, scores)","说明":"将两个列表对应位置的元素配对，返回元组迭代器"},{"代码":"dict(zip(...))","说明":"将配对的键值对转换为字典"},{"代码":"zip(*dict1.items())","说明":"*解包操作符，将字典的键值对拆分回列表"}]',
            'syntax_note': 'zip 以最短列表为准，超出的元素会被忽略\\nzip 返回迭代器，需用list()转为列表\\nzip(*...) 是解压缩操作，还原多个列表',
            'runnable_example': 'questions = ["姓名", "年龄", "城市"]\\nanswers = ["张三", 28, "北京"]\\n\\n# 生成问卷结果\\nfor q, a in zip(questions, answers):\\n    print(f"{q}: {a}")\\n\\n# 转成字典更直观\\nresult = dict(zip(questions, answers))\\nprint(result)',
            'common_errors': '[]',
            'aliases': 'zip,列表合并,配对,同时遍历',
        },
        {
            'title': 'lambda与sorted排序',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'students = [\n    {"name": "张三", "score": 85},\n    {"name": "李四", "score": 92},\n    {"name": "王五", "score": 78},\n]\n\n# 按分数升序\nsorted_by_score = sorted(students, key=lambda s: s["score"])\n\n# 按分数降序\nsorted_desc = sorted(students, key=lambda s: s["score"], reverse=True)\n\n# 按名字长度排序\nsorted_by_name = sorted(students, key=lambda s: len(s["name"]))\n\nprint("最高分:", sorted_desc[0]["name"])  # 李四',
            'line_by_line': '[{"代码":"sorted(列表, key=函数)","说明":"返回排序后的新列表，原列表不变"},{"代码":"lambda s: s[\\"score\\"]","说明":"匿名函数，接收一个学生字典，返回分数"},{"代码":"reverse=True","说明":"降序排列，默认False为升序"},{"代码":"key=lambda s: len(s[\\"name\\"])","说明":"按名字长度排序"}]',
            'syntax_note': 'sorted() 返回新列表，不修改原列表\\n列表.sort() 是原地排序，修改原列表\\nkey 参数可以是任何可调用对象（函数、lambda等）',
            'runnable_example': 'nums = [3, 1, 4, 1, 5, 9, 2, 6]\\n# 按数字的个位数排序\\nsorted_nums = sorted(nums, key=lambda x: x % 10)\\nprint(sorted_nums)  # [1, 1, 2, 3, 4, 5, 6, 9]',
            'common_errors': '[]',
            'aliases': '排序,lambda,匿名函数,sorted',
        },
        {
            'title': '生成器yield',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': 'def fibonacci(n):\n    """生成斐波那契数列的前n个数"""\n    a, b = 0, 1\n    count = 0\n    while count < n:\n        yield a\n        a, b = b, a + b\n        count += 1\n\n# 使用生成器\nfor num in fibonacci(10):\n    print(num, end=" ")  # 0 1 1 2 3 5 8 13 21 34\n\n# 转为列表\nfib_list = list(fibonacci(10))\nprint(fib_list)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]',
            'line_by_line': '[{"代码":"yield a","说明":"暂停函数，返回a的值，下次调用从这继续"},{"代码":"a, b = b, a + b","说明":"同时更新两个变量，Pythonic的交换写法"},{"代码":"while count < n","说明":"循环直到生成n个数"},{"代码":"list(fibonacci(10))","说明":"将生成器转为列表"}]',
            'syntax_note': 'yield 让函数变成生成器函数\\n生成器一次只生成一个值，内存友好\\n生成器只能遍历一次，遍历完就空了\\n适用于处理大数据集或无限序列',
            'runnable_example': 'def read_large_file(file_path):\\n    """逐行读取大文件，不一次性加载到内存"""\\n    with open(file_path, "r") as f:\\n        for line in f:\\n            yield line.strip()\\n\\n# 使用\\n# for line in read_large_file("huge_file.txt"):\\n#     print(line)',
            'common_errors': '[{"报错":"StopIteration","解决办法":"生成器耗尽后会抛出此异常，for循环自动处理"}]',
            'aliases': '生成器,yield,generator,惰性求值',
        },
        {
            'title': 'pip安装与管理包',
            'language': 'Python',
            'version': '>=3.0',
            'code_block': '# 安装包\n# pip install 包名\n# pip install requests\n\n# 安装指定版本\n# pip install requests==2.28.0\n\n# 安装大于某版本\n# pip install "requests>=2.0"\n\n# 从requirements.txt安装\n# pip install -r requirements.txt\n\n# 卸载包\n# pip uninstall requests\n\n# 列出已安装的包\n# pip list\n\n# 导出已安装的包列表\n# pip freeze > requirements.txt\n\n# 查看包信息\n# pip show requests',
            'line_by_line': '[{"代码":"pip install 包名","说明":"安装Python第三方包"},{"代码":"pip install 包名==版本","说明":"安装指定版本"},{"代码":"pip install -r requirements.txt","说明":"批量安装文件中列出的所有包"},{"代码":"pip freeze > requirements.txt","说明":"将当前环境的包列表导出到文件"},{"代码":"pip list","说明":"列出所有已安装的包"}]',
            'syntax_note': '在虚拟环境中使用 pip，避免污染全局环境\\n建议用 python -m pip install 而不是直接 pip install\\nrequirements.txt 是 Python 项目标准依赖文件',
            'runnable_example': '# 1. 创建虚拟环境\\n# python -m venv venv\\n# 2. 激活虚拟环境\\n# venv\\Scripts\\activate  # Windows\\n# source venv/bin/activate  # Linux/Mac\\n# 3. 安装依赖\\n# pip install pandas numpy requests\\n# 4. 导出依赖\\n# pip freeze > requirements.txt',
            'common_errors': '[{"报错":"pip: command not found","解决办法":"用 python -m pip 代替，或检查pip是否安装"},{"报错":"Permission denied","解决办法":"加 --user 或在虚拟环境中安装"}]',
            'aliases': 'pip,包管理,安装包,python包',
        },
    ]
    for s in snippets:
        s['category_id'] = python_cat
        db.add_snippet(**s)
    print(f"✅ Python: {len(snippets)} 条")

# ==========================================================
# JavaScript 片段（15条）
# ==========================================================
js_cat = get_cat('编程语言', 'JavaScript')
if js_cat:
    snippets = [
        {
            'title': 'console.log 打印输出',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// 基本打印\nconsole.log("Hello, World!");\n\n// 打印变量\nconst name = "张三";\nconsole.log(name);\n\n// 打印多个值\nconsole.log("姓名:", name, "年龄:", 28);\n\n// 格式化打印\nconsole.log(`你好，${name}！`);\n\n// 打印对象\nconst user = { name: "张三", age: 28 };\nconsole.log(user);\nconsole.table(user);  // 表格形式\n\n// 打印警告和错误\nconsole.warn("这是警告");\nconsole.error("这是错误");',
            'line_by_line': '[{"代码":"console.log(...)","说明":"向控制台输出信息"},{"代码":"console.table(obj)","说明":"以表格形式打印对象/数组"},{"代码":"console.warn()","说明":"打印警告信息（黄色）"},{"代码":"console.error()","说明":"打印错误信息（红色）"}]',
            'syntax_note': 'console.log 接受任意数量的参数\\n浏览器中按 F12 打开开发者工具查看控制台\\n调试时比 alert() 更方便，不会阻塞页面',
            'runnable_example': '// 在浏览器控制台或Node.js中运行\\nconst items = ["苹果", "香蕉", "橙子"];\\nconsole.log("水果列表:");\\nitems.forEach((item, i) => console.log(`${i+1}. ${item}`));\\nconsole.table(items);',
            'common_errors': '[]',
            'aliases': '打印,console,调试,控制台输出',
        },
        {
            'title': '箭头函数',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// 传统函数\nfunction add(a, b) {\n    return a + b;\n}\n\n// 箭头函数（一行，省略return）\nconst add2 = (a, b) => a + b;\n\n// 箭头函数（多行）\nconst multiply = (a, b) => {\n    const result = a * b;\n    return result;\n};\n\n// 单个参数可省略括号\nconst double = x => x * 2;\n\n// 无参数需写空括号\nconst hello = () => console.log("你好");',
            'line_by_line': '[{"代码":"(a, b) => a + b","说明":"箭头函数，参数=>返回值"},{"代码":"const add2 = (a, b) => a + b","说明":"箭头函数赋值给变量"},{"代码":"x => x * 2","说明":"单个参数可省略括号"},{"代码":"() => console.log(...)","说明":"无参数必须写空括号"}]',
            'syntax_note': '箭头函数没有自己的 this，继承外层作用域的 this\\n箭头函数不能用作构造函数（不能 new）\\n单行表达式会自动 return，不需要写 return 关键字',
            'runnable_example': 'const numbers = [1, 2, 3, 4, 5];\\n// 箭头函数让代码更简洁\\nconst doubled = numbers.map(n => n * 2);\\nconst evens = numbers.filter(n => n % 2 === 0);\\nconsole.log(doubled);  // [2, 4, 6, 8, 10]\\nconsole.log(evens);    // [2, 4]',
            'common_errors': '[{"报错":"箭头函数中的 this 不是预期的对象","解决办法":"箭头函数不绑定this，用普通函数或bind()"}]',
            'aliases': '箭头函数,arrow function,lambda,ES6',
        },
        {
            'title': '数组 map/filter/reduce',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': 'const numbers = [1, 2, 3, 4, 5];\n\n// map: 每个元素转换\nconst doubled = numbers.map(n => n * 2);\nconsole.log(doubled);  // [2, 4, 6, 8, 10]\n\n// filter: 过滤元素\nconst evens = numbers.filter(n => n % 2 === 0);\nconsole.log(evens);    // [2, 4]\n\n// reduce: 累积计算\nconst sum = numbers.reduce((acc, n) => acc + n, 0);\nconsole.log(sum);      // 15\n\n// 链式调用\nconst result = numbers\n    .filter(n => n > 2)\n    .map(n => n * 10)\n    .reduce((a, b) => a + b, 0);\nconsole.log(result);   // 30 + 40 + 50 = 120',
            'line_by_line': '[{"代码":"arr.map(fn)","说明":"遍历数组，每个元素调用fn，返回新数组"},{"代码":"arr.filter(fn)","说明":"过滤数组，保留fn返回true的元素"},{"代码":"arr.reduce(fn, init)","说明":"累积计算，acc是累积值，n是当前元素"},{"代码":"链式调用","说明":"filter→map→reduce 依次处理数据"}]',
            'syntax_note': '这些方法不会修改原数组，返回新数组\\nmap 和 filter 返回新数组，reduce 返回累积值\\nreduce 的初始值很重要，空数组时返回初始值',
            'runnable_example': 'const students = [\\n    { name: "张三", score: 85 },\\n    { name: "李四", score: 92 },\\n    { name: "王五", score: 78 },\\n];\\n// 及格学生的平均分\\nconst passing = students.filter(s => s.score >= 80);\\nconst avg = passing.reduce((sum, s) => sum + s.score, 0) / passing.length;\\nconsole.log(`及格学生平均分: ${avg}`);',
            'common_errors': '[{"报错":"Cannot read property of undefined","解决办法":"检查数组是否为空，reduce要加初始值"}]',
            'aliases': 'map,filter,reduce,数组操作,高阶函数',
        },
        {
            'title': '模板字符串',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': 'const name = "张三";\nconst age = 28;\n\n// 拼接字符串（旧方式）\nconsole.log("我叫" + name + "，今年" + age + "岁");\n\n// 模板字符串（新方式）\nconsole.log(`我叫${name}，今年${age}岁`);\n\n// 多行字符串\nconst html = `\n<div>\n    <h1>${name}</h1>\n    <p>年龄: ${age}</p>\n</div>\n`;\n\n// 表达式\nconsole.log(`明年${age + 1}岁`);\nconsole.log(`总价: ${(price * 0.8).toFixed(2)}元`);',
            'line_by_line': '[{"代码":"`字符串 ${变量}`","说明":"反引号包裹的模板字符串，${}内放表达式"},{"代码":"多行字符串","说明":"模板字符串可以直接换行，不需要\\\\n"},{"代码":"${age + 1}","说明":"花括号内可以是任意JavaScript表达式"}]',
            'syntax_note': '用反引号（`）而不是单引号（\'）\\n${} 里可以放变量、表达式、函数调用\\n支持多行，比字符串拼接更清晰',
            'runnable_example': 'const user = { name: "张三", role: "管理员" };\\nconst message = `\\n=== 用户信息 ===\\n姓名: ${user.name}\\n角色: ${user.role}\\n================\\n`;\\nconsole.log(message);',
            'common_errors': '[]',
            'aliases': '模板字符串,template literal,模板,字符串拼接',
        },
        {
            'title': '解构赋值',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// 数组解构\nconst colors = ["红", "绿", "蓝"];\nconst [first, second, third] = colors;\nconsole.log(first);   // "红"\n\n// 跳过元素\nconst [, , last] = colors;\nconsole.log(last);    // "蓝"\n\n// 对象解构\nconst user = { name: "张三", age: 28, city: "北京" };\nconst { name, age } = user;\nconsole.log(name, age);  // "张三" 28\n\n// 重命名\nconst { name: userName, city: userCity } = user;\nconsole.log(userName);  // "张三"\n\n// 默认值\nconst { phone = "未知" } = user;\nconsole.log(phone);  // "未知"',
            'line_by_line': '[{"代码":"const [a, b] = arr","说明":"从数组中解构提取元素"},{"代码":"const [, , c] = arr","说明":"用逗号跳过不需要的元素"},{"代码":"const {name, age} = obj","说明":"从对象中提取同名属性"},{"代码":"{name: newName}","说明":"将属性重命名为新变量名"},{"代码":"{prop = defaultValue}","说明":"属性不存在时使用默认值"}]',
            'syntax_note': '解构赋值不改变原数组/对象\\n可以嵌套解构复杂对象\\n常用于函数参数的解构',
            'runnable_example': '// 函数参数解构 - 非常实用\\nfunction printUser({name, age, city = "未知"}) {\\n    console.log(`${name}(${age}岁) - ${city}`);\\n}\\n\\nconst user = { name: "李四", age: 25 };\\nprintUser(user);  // 李四(25岁) - 未知\\n\\n// 交换变量值 [a, b] = [b, a]\\nlet x = 1, y = 2;\\n[x, y] = [y, x];\\nconsole.log(x, y);  // 2 1',
            'common_errors': '[{"报错":"Cannot destructure property of undefined","解决办法":"确保被解构的对象/数组不是 undefined"}]',
            'aliases': '解构赋值,destructuring,ES6',
        },
        {
            'title': 'async/await 异步',
            'language': 'JavaScript',
            'version': 'ES8+',
            'code_block': '// 模拟异步操作\nfunction delay(ms) {\n    return new Promise(resolve => setTimeout(resolve, ms));\n}\n\n// async函数\nasync function fetchData() {\n    console.log("开始获取数据...");\n    \n    // await等待Promise完成\n    await delay(2000);  // 等待2秒\n    \n    return { id: 1, name: "张三" };\n}\n\n// 使用async函数\nasync function main() {\n    const data = await fetchData();\n    console.log("获取到数据:", data);\n}\n\nmain();\nconsole.log("程序继续执行...");  // 这行先执行',
            'line_by_line': '[{"代码":"async function fn()","说明":"定义异步函数，总是返回Promise"},{"代码":"await promise","说明":"等待Promise完成，暂停执行（不阻塞主线程）"},{"代码":"await delay(2000)","说明":"等待2秒"},{"代码":"const data = await fetchData()","说明":"等待异步函数返回结果"}]',
            'syntax_note': 'await 只能在 async 函数内部使用\\nasync 函数返回的是 Promise 对象\\n用 try/catch 处理 async/await 的错误',
            'runnable_example': 'async function getUser(id) {\\n    try {\\n        const response = await fetch(`https://api.example.com/users/${id}`);\\n        if (!response.ok) throw new Error("请求失败");\\n        const data = await response.json();\\n        return data;\\n    } catch (error) {\\n        console.error("获取用户失败:", error);\\n        return null;\\n    }\\n}\\n\\nconst user = await getUser(1);\\nconsole.log(user);',
            'common_errors': '[{"报错":"await is only valid in async function","解决办法":"确保函数前面加了 async"},{"报错":"Unhandled Promise Rejection","解决办法":"用 try/catch 包裹 await"}]',
            'aliases': 'async/await,异步,Promise,ES8',
        },
        {
            'title': 'fetch API 发送请求',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// GET请求\nfetch("https://api.github.com/users/octocat")\n    .then(response => {\n        if (!response.ok) {\n            throw new Error(`HTTP错误: ${response.status}`);\n        }\n        return response.json();\n    })\n    .then(data => console.log(data))\n    .catch(error => console.error("请求失败:", error));\n\n// POST请求\nfetch("https://api.example.com/users", {\n    method: "POST",\n    headers: {\n        "Content-Type": "application/json",\n    },\n    body: JSON.stringify({\n        name: "张三",\n        age: 28\n    })\n})\n.then(res => res.json())\n.then(data => console.log("创建成功:", data));',
            'line_by_line': '[{"代码":"fetch(url)","说明":"发送GET请求，返回Promise"},{"代码":".then(res => res.json())","说明":"解析响应为JSON格式"},{"代码":"response.ok","说明":"HTTP状态码是否在200-299之间"},{"代码":"method: \\"POST\\"","说明":"指定HTTP请求方法"},{"代码":"body: JSON.stringify(data)","说明":"将JavaScript对象转为JSON字符串发送"},{"代码":".catch(error => ...)","说明":"捕获网络错误"}]',
            'syntax_note': 'fetch 是浏览器内置API，不需要安装第三方库\\nfetch 默认不带 Cookie，需加 credentials: "include"\\nfetch 只在网络错误时 reject，HTTP 4xx/5xx 不会 reject',
            'runnable_example': 'async function searchUsers(query) {\\n    try {\\n        const res = await fetch(`https://api.github.com/search/users?q=${query}`);\\n        if (!res.ok) throw new Error("搜索失败");\\n        const data = await res.json();\\n        console.log(`找到 ${data.total_count} 个用户`);\\n        data.items.forEach(user => console.log(`- ${user.login}`));\\n    } catch (err) {\\n        console.error(err.message);\\n    }\\n}\\n\\nsearchUsers("python");',
            'common_errors': '[{"报错":"TypeError: Failed to fetch","解决办法":"检查URL是否正确，是否有CORS限制"},{"报错":"SyntaxError: JSON.parse error","解决办法":"响应不是有效JSON，用res.text()代替res.json()"}]',
            'aliases': 'fetch,HTTP请求,网络请求,API调用',
        },
        {
            'title': 'DOM 选择器',
            'language': 'JavaScript',
            'version': 'ES5+',
            'code_block': '// 通过ID选择\nconst header = document.getElementById("header");\n\n// 通过CSS选择器选择第一个\nconst firstBtn = document.querySelector(".btn");\n\n// 通过CSS选择器选择所有\nconst allBtns = document.querySelectorAll(".btn");\n\n// 通过类名\nconst items = document.getElementsByClassName("item");\n\n// 通过标签名\nconst divs = document.getElementsByTagName("div");\n\n// 修改内容\nelement.textContent = "新文本";\nelement.innerHTML = "<b>加粗文本</b>";\n\n// 修改样式\nelement.style.color = "red";\nelement.classList.add("active");\nelement.classList.remove("hidden");',
            'line_by_line': '[{"代码":"document.getElementById(id)","说明":"通过ID获取单个元素"},{"代码":"document.querySelector(css)","说明":"通过CSS选择器获取第一个匹配元素"},{"代码":"document.querySelectorAll(css)","说明":"通过CSS选择器获取所有匹配元素"},{"代码":"element.textContent","说明":"获取/设置纯文本内容（安全）"},{"代码":"element.innerHTML","说明":"获取/设置HTML内容（小心XSS）"},{"代码":"element.classList.add/remove","说明":"添加/移除CSS类名"}]',
            'syntax_note': 'querySelector 比 getElementById 更灵活，但稍慢\\ntextContent 比 innerHTML 更安全（防止XSS攻击）\\nquerySelectorAll 返回的是 NodeList（不是数组），可用 forEach',
            'runnable_example': '// 给所有链接添加新窗口打开\\ndocument.querySelectorAll("a[href^=\\"http\\"]").forEach(link => {\\n    link.setAttribute("target", "_blank");\\n    link.setAttribute("rel", "noopener noreferrer");\\n});\\n\\n// 点击按钮切换暗色模式\\nconst btn = document.getElementById("darkModeBtn");\\nbtn.addEventListener("click", () => {\\n    document.body.classList.toggle("dark-mode");\\n});',
            'common_errors': '[{"报错":"Cannot read property of null","解决办法":"确保元素已存在（DOM加载完成后执行）"},{"报错":"document is not defined","解决办法":"这是浏览器API，Node.js中不可用"}]',
            'aliases': 'DOM选择,querySelector,getElementById,元素选择',
        },
        {
            'title': '事件监听 addEventListener',
            'language': 'JavaScript',
            'version': 'ES5+',
            'code_block': '// 语法: element.addEventListener(事件类型, 处理函数, 选项)\n\nconst button = document.querySelector("#myButton");\n\n// 点击事件\nbutton.addEventListener("click", function(event) {\n    console.log("按钮被点击了");\n    console.log("事件对象:", event);\n});\n\n// 箭头函数写法\nbutton.addEventListener("click", (e) => {\n    console.log(`点击位置: (${e.clientX}, ${e.clientY})`);\n});\n\n// 常用事件\n// click       - 点击\n// dblclick    - 双击\n// mouseover   - 鼠标移入\n// mouseout    - 鼠标移出\n// keydown     - 键盘按下\n// submit      - 表单提交\n// load        - 页面/图片加载完成\n// scroll      - 滚动\n\n// 移除事件监听\n// button.removeEventListener("click", handler);',
            'line_by_line': '[{"代码":"addEventListener(type, fn)","说明":"给元素添加事件监听器"},{"代码":"event.clientX/Y","说明":"鼠标相对于视口的坐标"},{"代码":"removeEventListener(type, fn)","说明":"移除事件监听（函数必须是同一个引用）"},{"代码":"事件类型","说明":"click/mouseover/keydown等"}]',
            'syntax_note': '推荐用 addEventListener 而不是 onclick 属性\\n可以给同一个元素添加多个同类型事件\\n移除监听时，回调函数必须是同一个引用（不能用匿名函数）',
            'runnable_example': '// 双击编辑文本\\nconst editable = document.querySelector("#editable");\\neditable.addEventListener("dblclick", () => {\\n    const input = document.createElement("input");\\n    input.value = editable.textContent;\\n    editable.replaceWith(input);\\n    input.focus();\\n    input.addEventListener("blur", () => {\\n        editable.textContent = input.value;\\n        input.replaceWith(editable);\\n    });\\n});',
            'common_errors': '[{"报错":"addEventListener is not a function","解决办法":"确保选择到的是单个元素，而不是NodeList"}]',
            'aliases': '事件监听,addEventListener,事件绑定',
        },
        {
            'title': 'JSON.parse/stringify',
            'language': 'JavaScript',
            'version': 'ES5+',
            'code_block': '// 对象 → JSON字符串\nconst user = { name: "张三", age: 28, isAdmin: false };\nconst jsonString = JSON.stringify(user);\nconsole.log(jsonString);\n// {"name":"张三","age":28,"isAdmin":false}\n\n// JSON字符串 → 对象\nconst parsed = JSON.parse(jsonString);\nconsole.log(parsed.name);  // "张三"\n\n// 格式化输出\nconst pretty = JSON.stringify(user, null, 2);\nconsole.log(pretty);\n// {\n//   "name": "张三",\n//   "age": 28,\n//   "isAdmin": false\n// }\n\n// 深拷贝对象\nconst clone = JSON.parse(JSON.stringify(user));',
            'line_by_line': '[{"代码":"JSON.stringify(obj)","说明":"将JavaScript对象转为JSON字符串"},{"代码":"JSON.parse(str)","说明":"将JSON字符串转回JavaScript对象"},{"代码":"JSON.stringify(obj, null, 2)","说明":"格式化输出，2个空格缩进"},{"代码":"JSON.parse(JSON.stringify(obj))","说明":"简单深拷贝（但会丢失函数、undefined）"}]',
            'syntax_note': 'JSON 只支持：对象、数组、字符串、数字、布尔值、null\\n函数、undefined、Symbol 在 stringify 时会被忽略或转为 null\\nparse 时字符串必须是严格JSON格式（键必须双引号）',
            'runnable_example': '// 保存到localStorage\\nconst settings = { theme: "dark", fontSize: 14 };\\nlocalStorage.setItem("settings", JSON.stringify(settings));\\n\\n// 读取\\nconst saved = JSON.parse(localStorage.getItem("settings"));\\nconsole.log(saved.theme);  // "dark"',
            'common_errors': '[{"报错":"Unexpected token","解决办法":"检查JSON格式是否正确（键必须双引号）"},{"报错":"Circular reference","解决办法":"对象有循环引用时无法序列化"}]',
            'aliases': 'JSON,parse,stringify,序列化',
        },
        {
            'title': 'localStorage 读写',
            'language': 'JavaScript',
            'version': 'ES5+',
            'code_block': '// 写入\nlocalStorage.setItem("username", "张三");\nlocalStorage.setItem("theme", "dark");\n\n// 读取\nconst name = localStorage.getItem("username");\nconsole.log(name);  // "张三"\n\n// 删除一项\nlocalStorage.removeItem("theme");\n\n// 清空所有\n// localStorage.clear();\n\n// 存储对象（需要序列化）\nconst user = { id: 1, name: "李四" };\nlocalStorage.setItem("user", JSON.stringify(user));\n\n// 读取对象\nconst savedUser = JSON.parse(localStorage.getItem("user"));\nconsole.log(savedUser.name);  // "李四"\n\n// 获取存储数量\nconsole.log(localStorage.length);',
            'line_by_line': '[{"代码":"localStorage.setItem(key, value)","说明":"保存数据到本地存储"},{"代码":"localStorage.getItem(key)","说明":"读取本地存储的数据"},{"代码":"localStorage.removeItem(key)","说明":"删除指定项"},{"代码":"localStorage.clear()","说明":"清空所有本地存储"}]',
            'syntax_note': 'localStorage 只能存字符串，对象需 JSON.stringify\\n数据永久保存，除非用户清除浏览器数据\\nsessionStorage 用法相同，但关闭标签页后清除\\n每个域名有5MB左右的存储限制',
            'runnable_example': '// 记住用户偏好\\nfunction savePreference(key, value) {\\n    localStorage.setItem(key, JSON.stringify(value));\\n}\\n\\nfunction loadPreference(key, defaultValue) {\\n    const saved = localStorage.getItem(key);\\n    return saved ? JSON.parse(saved) : defaultValue;\\n}\\n\\nsavePreference("fontSize", 16);\\nsavePreference("theme", "dark");\\nconsole.log(loadPreference("theme", "light"));  // "dark"',
            'common_errors': '[{"报错":"localStorage is not defined","说明":"localStorage 只在浏览器中可用，Node.js 中没有"}]',
            'aliases': 'localStorage,本地存储,缓存',
        },
        {
            'title': '定时器 setTimeout/setInterval',
            'language': 'JavaScript',
            'version': 'ES5+',
            'code_block': '// setTimeout: 延迟执行一次\nsetTimeout(() => {\n    console.log("2秒后执行");\n}, 2000);\n\n// 带参数\nsetTimeout((name) => {\n    console.log(`你好, ${name}`);\n}, 1000, "张三");\n\n// 取消定时器\nconst timer = setTimeout(() => console.log("不会执行"), 3000);\nclearTimeout(timer);\n\n// setInterval: 每隔一段时间执行\nconst interval = setInterval(() => {\n    console.log("每秒执行一次");\n}, 1000);\n\n// 停止循环\nsetTimeout(() => {\n    clearInterval(interval);\n    console.log("已停止定时器");\n}, 5000);',
            'line_by_line': '[{"代码":"setTimeout(fn, ms)","说明":"延迟ms毫秒后执行fn一次"},{"代码":"clearTimeout(id)","说明":"取消还未执行的setTimeout"},{"代码":"setInterval(fn, ms)","说明":"每隔ms毫秒重复执行fn"},{"代码":"clearInterval(id)","说明":"停止setInterval的循环"}]',
            'syntax_note': '时间单位是毫秒，1000ms = 1秒\\n定时器不一定精确，受事件循环影响\\n返回的数字ID用于取消定时器\\n组件卸载/页面离开时记得清理定时器',
            'runnable_example': '// 倒计时示例\\nlet count = 10;\\nconsole.log(`倒计时开始: ${count}`);\\nconst timer = setInterval(() => {\\n    count--;\\n    console.log(count);\\n    if (count <= 0) {\\n        clearInterval(timer);\\n        console.log("倒计时结束！");\\n    }\\n}, 1000);',
            'common_errors': '[]',
            'aliases': '定时器,setTimeout,setInterval,延时',
        },
        {
            'title': 'Promise 基本用法',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// 创建Promise\nconst myPromise = new Promise((resolve, reject) => {\n    // 异步操作\n    const success = true;\n    \n    if (success) {\n        resolve("操作成功");\n    } else {\n        reject("操作失败");\n    }\n});\n\n// 使用Promise\nmyPromise\n    .then(result => {\n        console.log("成功:", result);\n        return "下一步";\n    })\n    .then(next => {\n        console.log(next);  // 链式调用\n    })\n    .catch(error => {\n        console.error("失败:", error);\n    })\n    .finally(() => {\n        console.log("总是执行");\n    });\n\n// Promise.all: 等待所有完成\nconst p1 = Promise.resolve(3);\nconst p2 = new Promise(r => setTimeout(() => r("完成"), 1000));\nPromise.all([p1, p2]).then(results => {\n    console.log(results);  // [3, "完成"]\n});',
            'line_by_line': '[{"代码":"new Promise((resolve, reject) => {})","说明":"创建Promise，resolve=成功，reject=失败"},{"代码":".then(onFulfilled)","说明":"Promise成功时调用"},{"代码":".catch(onRejected)","说明":"Promise失败时调用"},{"代码":".finally(onFinally)","说明":"无论成功失败都会执行"},{"代码":"Promise.all([...])","说明":"等待所有Promise完成，返回数组"}]',
            'syntax_note': 'Promise 有三种状态：pending（等待）、fulfilled（成功）、rejected（失败）\\n状态一旦改变就不可逆\\n.then() 返回新Promise，支持链式调用',
            'runnable_example': 'function loadImage(url) {\\n    return new Promise((resolve, reject) => {\\n        const img = new Image();\\n        img.onload = () => resolve(img);\\n        img.onerror = () => reject(new Error(`加载失败: ${url}`));\\n        img.src = url;\\n    });\\n}\\n\\nloadImage("https://example.com/photo.jpg")\\n    .then(img => console.log(`图片已加载: ${img.width}x${img.height}`))\\n    .catch(err => console.error(err.message));',
            'common_errors': '[{"报错":"Uncaught (in promise)","解决办法":"总是用 .catch() 处理Promise的错误"}]',
            'aliases': 'Promise,异步,ES6,promise',
        },
        {
            'title': '扩展运算符 ...',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// 展开数组\nconst arr1 = [1, 2, 3];\nconst arr2 = [4, 5, 6];\nconst combined = [...arr1, ...arr2];\nconsole.log(combined);  // [1, 2, 3, 4, 5, 6]\n\n// 复制数组\nconst copy = [...arr1];\n\n// 展开对象\nconst user = { name: "张三", age: 28 };\nconst withCity = { ...user, city: "北京" };\nconsole.log(withCity);  // {name: "张三", age: 28, city: "北京"}\n\n// 覆盖属性\nconst updated = { ...user, age: 29 };\nconsole.log(updated);  // {name: "张三", age: 29}\n\n// 函数参数\nfunction sum(...numbers) {\n    return numbers.reduce((a, b) => a + b, 0);\n}\nconsole.log(sum(1, 2, 3, 4));  // 10\n\n// 剩余参数（解构）\nconst [first, ...rest] = [1, 2, 3, 4];\nconsole.log(first);  // 1\nconsole.log(rest);   // [2, 3, 4]',
            'line_by_line': '[{"代码":"[...arr]","说明":"将数组展开为元素列表"},{"代码":"{...obj}","说明":"将对象属性展开"},{"代码":"{...obj, prop: val}","说明":"合并并覆盖属性"},{"代码":"function fn(...args)","说明":"剩余参数，将多个参数收集为数组"}]',
            'syntax_note': '扩展运算符是浅拷贝（一层）\\n对象展开时，后面的属性会覆盖前面的同名属性\\n常用于 React 的不可变数据更新',
            'runnable_example': '// 合并配置对象\\nconst defaults = { theme: "light", fontSize: 14, showSidebar: true };\\nconst userPrefs = { theme: "dark", fontSize: 16 };\\n\\nconst config = { ...defaults, ...userPrefs };\\nconsole.log(config);\\n// {theme: "dark", fontSize: 16, showSidebar: true}\\n\\n// 在数组中添加元素\\nconst todos = ["写代码", "测试"];\\nconst newTodos = [...todos, "部署"];\\n// ["写代码", "测试", "部署"]',
            'common_errors': '[]',
            'aliases': '扩展运算符,spread operator,展开,ES6',
        },
        {
            'title': '模块导入导出',
            'language': 'JavaScript',
            'version': 'ES6+',
            'code_block': '// ===== math.js (导出) =====\n// 命名导出\nexport const PI = 3.14159;\nexport function add(a, b) { return a + b; }\n\n// 默认导出\nexport default class Calculator {\n    multiply(a, b) { return a * b; }\n}\n\n// ===== main.js (导入) =====\n// 导入默认导出\nimport Calculator from "./math.js";\n\n// 导入命名导出\nimport { PI, add } from "./math.js";\n\n// 重命名\nimport { add as sum } from "./math.js";\n\n// 全部导入\nimport * as MathUtils from "./math.js";\nconsole.log(MathUtils.PI);  // 3.14159\n\n// 动态导入（按需加载）\nconst module = await import("./math.js");',
            'line_by_line': '[{"代码":"export const ...","说明":"导出变量/函数/类，可以被其他模块导入"},{"代码":"export default ...","说明":"默认导出，每个模块只能有一个"},{"代码":"import { name } from \\"...\\"","说明":"导入指定的命名导出"},{"代码":"import Default from \\"...\\"","说明":"导入默认导出"},{"代码":"import * as X from \\"...\\"","说明":"导入所有导出为命名空间对象"},{"代码":"import()","说明":"动态导入，返回Promise，支持按需加载"}]',
            'syntax_note': 'ES6 模块是静态分析，import 必须在文件顶部\\n默认导出在导入时可以任意命名\\n浏览器中使用需要 type="module" 或打包工具',
            'runnable_example': '// utils.js\\nexport function formatDate(date) {\\n    return date.toISOString().split("T")[0];\\n}\\nexport const VERSION = "1.0.0";\\n\\n// app.js\\nimport { formatDate, VERSION } from "./utils.js";\\nconsole.log(`版本 ${VERSION}`);\\nconsole.log(formatDate(new Date()));  // 2024-01-15',
            'common_errors': '[{"报错":"Cannot use import statement outside a module","解决办法":"在 package.json 加 \\"type\\": \\"module\\"，或 .mjs 扩展名"},{"报错":"Failed to resolve module specifier","解决办法":"检查导入路径是否正确"}]',
            'aliases': '模块,import,export,ES6模块',
        },
    ]
    for s in snippets:
        s['category_id'] = js_cat
        db.add_snippet(**s)
    print(f"✅ JavaScript: {len(snippets)} 条")

# ==========================================================
# Rust 片段（12条）
# ==========================================================
rust_cat = get_cat('编程语言', 'Rust')
if rust_cat:
    snippets = [
        {
            'title': '变量声明与类型注解',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': 'fn main() {\n    // 不可变变量（默认）\n    let x = 5;\n    println!("x = {}", x);  // x = 5\n\n    // 可变变量\n    let mut y = 10;\n    println!("y = {}", y);\n    y = 20;  // 可以修改\n    println!("y = {}", y);\n\n    // 显式类型注解\n    let z: i32 = 100;\n    let name: &str = "张三";\n    let pi: f64 = 3.14159;\n\n    // 常量\n    const MAX_COUNT: u32 = 1000;\n    println!("MAX_COUNT = {}", MAX_COUNT);\n\n    // 变量遮蔽（shadowing）\n    let a = \"hello\";\n    let a = a.len();  // 重新绑定为数字类型\n    println!("a = {}", a);  // a = 5\n}',
            'line_by_line': '[{"代码":"let x = 5","说明":"声明不可变变量（默认不可变）"},{"代码":"let mut y = 10","说明":"mut关键字使变量可变"},{"代码":"let z: i32 = 100","说明":"显式指定类型：32位整数"},{"代码":"const MAX: u32 = 1000","说明":"常量，编译期确定，全大写命名"},{"代码":"variable shadowing","说明":"同名变量遮蔽，可以改变类型"}]',
            'syntax_note': '变量默认不可变，这是 Rust 的安全设计\\nmut 声明的变量才能修改值\\n常量用 const，变量用 let\\nshadowing 可以改变变量类型，mut 不能',
            'runnable_example': 'fn main() {\n    let price: f64 = 29.99;\n    let quantity: i32 = 3;\n    let total = price * quantity as f64;\n    println!("总价: ¥{:.2}", total);  // 总价: ¥89.97\n}',
            'common_errors': '[{"报错":"cannot assign twice to immutable variable","解决办法":"加 mut 关键字"},{"报错":"mismatched types","解决办法":"类型不匹配，需显式转换 as 关键字"}]',
            'aliases': '变量,let,mut,const,类型,变量声明',
        },
        {
            'title': 'match 模式匹配',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': 'fn main() {\n    let number = 3;\n\n    match number {\n        1 => println!("一"),\n        2 => println!("二"),\n        3 | 4 => println!("三或四"),\n        5..=10 => println!("五到十之间"),\n        _ => println!("其他数字"),  // 默认分支\n    }\n\n    // 带值的匹配\n    let value = Some(5);\n    let result = match value {\n        Some(x) if x > 10 => format!("大于10: {}", x),\n        Some(x) => format!("值: {}", x),\n        None => String::from("无值"),\n    };\n    println!("{}", result);\n\n    // if let 简洁写法（只匹配一种情况）\n    if let Some(x) = value {\n        println!("if let: x = {}", x);\n    }\n}',
            'line_by_line': '[{"代码":"match number { 模式 => 动作 }","说明":"模式匹配，类似switch但更强"},{"代码":"3 | 4 => ...","说明":"| 表示或，匹配多个值"},{"代码":"5..=10 => ...","说明":"..= 范围匹配"},{"代码":"_ => ...","说明":"通配符，匹配所有未覆盖的情况"},{"代码":"Some(x) if x > 10","说明":"匹配守卫，加额外条件"},{"代码":"if let Some(x) = value","说明":"只需匹配一种情况的简写"}]',
            'syntax_note': 'match 必须穷举所有可能性（穷尽性检查）\\n_ 通配符处理剩余情况\\nmatch 是一个表达式，可以返回值\\nif let 是 match 的语法糖',
            'runnable_example': 'fn describe_point(x: i32, y: i32) -> &\'static str {\n    match (x, y) {\n        (0, 0) => "原点",\n        (0, _) => "在Y轴上",\n        (_, 0) => "在X轴上",\n        (x, y) if x == y => "在对角线上",\n        _ => "一般位置",\n    }\n}\n\nfn main() {\n    println!("{}", describe_point(0, 5));  // 在Y轴上\n    println!("{}", describe_point(3, 3));  // 在对角线上\n}',
            'common_errors': '[{"报错":"non-exhaustive patterns","解决办法":"添加 _ => 分支覆盖所有情况"}]',
            'aliases': 'match,模式匹配,匹配,if let',
        },
        {
            'title': 'Vec 向量操作',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': 'fn main() {\n    // 创建空向量\n    let mut v: Vec<i32> = Vec::new();\n\n    // 使用宏创建\n    let mut numbers = vec![1, 2, 3, 4, 5];\n\n    // 添加元素\n    numbers.push(6);\n    numbers.push(7);\n\n    // 访问元素\n    let third = &numbers[2];       // 索引访问（可能 panic）\n    println!("第三个元素: {}", third);\n\n    // 安全访问\n    match numbers.get(10) {\n        Some(val) => println!("找到: {}", val),\n        None => println!("索引越界"),\n    }\n\n    // 遍历\n    for val in &numbers {\n        println!("{}", val);\n    }\n\n    // 遍历并修改\n    for val in &mut numbers {\n        *val *= 2;\n    }\n\n    // 常用方法\n    println!("长度: {}", numbers.len());\n    println!("是否为空: {}", numbers.is_empty());\n    numbers.pop();  // 移除最后一个\n    numbers.remove(0);  // 移除第0个\n    println!("排序后: {:?}", numbers);\n}',
            'line_by_line': '[{"代码":"Vec::new()","说明":"创建空向量"},{"代码":"vec![1, 2, 3]","说明":"用宏创建并初始化"},{"代码":"v.push(item)","说明":"在末尾添加元素"},{"代码":"&v[index]","说明":"索引访问，越界会panic"},{"代码":"v.get(index)","说明":"安全访问，返回Option"},{"代码":"for val in &v","说明":"遍历向量"}]',
            'syntax_note': 'Vec 在堆上分配内存，可动态增长\\n索引越界会导致 panic（程序崩溃）\\nget() 返回 Option 更安全\\n遍历时 &v 是借用，&mut v 是可修改借用',
            'runnable_example': 'fn main() {\n    let mut scores = vec![85, 92, 78, 90, 88];\n    \n    // 计算平均分\n    let sum: i32 = scores.iter().sum();\n    let avg = sum as f64 / scores.len() as f64;\n    println!("平均分: {:.1}", avg);  // 86.6\n    \n    // 过滤出及格的\n    let passing: Vec<&i32> = scores.iter().filter(|&&s| s >= 80).collect();\n    println!("及格人数: {}", passing.len());\n}',
            'common_errors': '[{"报错":"index out of bounds","解决办法":"用 get() 替代索引访问"},{"报错":"cannot borrow as mutable","解决办法":"确保变量用 let mut 声明"}]',
            'aliases': 'Vec,向量,动态数组,列表',
        },
        {
            'title': 'HashMap 使用',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': 'use std::collections::HashMap;\n\nfn main() {\n    let mut scores = HashMap::new();\n\n    // 插入键值对\n    scores.insert(String::from("张三"), 85);\n    scores.insert(String::from("李四"), 92);\n    scores.insert(String::from("王五"), 78);\n\n    // 访问\n    let name = String::from("张三");\n    match scores.get(&name) {\n        Some(score) => println!("{} 的分数: {}", name, score),\n        None => println!("未找到"),\n    }\n\n    // 遍历\n    for (name, score) in &scores {\n        println!("{}: {}", name, score);\n    }\n\n    // 更新（不存在才插入）\n    scores.entry(String::from("张三")).or_insert(90);\n\n    // 更新（无论是否存在）\n    scores.insert(String::from("李四"), 95);\n\n    // 删除\n    scores.remove(&String::from("王五"));\n\n    println!("数量: {}", scores.len());  // 2\n}',
            'line_by_line': '[{"代码":"HashMap::new()","说明":"创建空哈希表"},{"代码":"map.insert(key, value)","说明":"插入键值对"},{"代码":"map.get(&key)","说明":"获取值，返回Option<&V>"},{"代码":"map.entry(key).or_insert(val)","说明":"键不存在才插入"},{"代码":"map.remove(&key)","说明":"删除键值对"}]',
            'syntax_note': 'HashMap 需要 use std::collections::HashMap\\n键和值在堆上分配所有权\\nget() 返回 Option<&V>，需要 match 处理\\nentry API 可以优雅地处理更新逻辑',
            'runnable_example': 'use std::collections::HashMap;\n\nfn main() {\n    let text = "hello world hello rust world";\n    let mut word_count = HashMap::new();\n\n    for word in text.split_whitespace() {\n        let count = word_count.entry(word).or_insert(0);\n        *count += 1;\n    }\n\n    println!("{:?}", word_count);\n    // {"hello": 2, "world": 2, "rust": 1}\n}',
            'common_errors': '[{"报错":"expected ... found ...","解决办法":"HashMap需要手动导入 use std::collections::HashMap"}]',
            'aliases': 'HashMap,哈希表,字典,map',
        },
        {
            'title': '结构体定义与实现',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': '// 定义结构体\nstruct User {\n    username: String,\n    email: String,\n    sign_in_count: u64,\n    active: bool,\n}\n\n// 元组结构体\nstruct Color(i32, i32, i32);\n\n// 单元结构体（无字段）\nstruct AlwaysEqual;\n\n// 实现方法\nimpl User {\n    // 关联函数（类似静态方法）\n    fn new(username: String, email: String) -> User {\n        User {\n            username,\n            email,\n            sign_in_count: 1,\n            active: true,\n        }\n    }\n\n    // 方法（&self）\n    fn get_email(&self) -> &String {\n        &self.email\n    }\n\n    // 修改方法（&mut self）\n    fn increment_sign_in(&mut self) {\n        self.sign_in_count += 1;\n    }\n}\n\nfn main() {\n    let mut user1 = User::new(\n        String::from("张三"),\n        String::from("zhangsan@example.com"),\n    );\n    \n    println!("邮箱: {}", user1.get_email());\n    user1.increment_sign_in();\n    \n    // 结构体更新语法\n    let user2 = User {\n        username: String::from("李四"),\n        ..user1  // 剩余字段从user1复制\n    };\n}',
            'line_by_line': '[{"代码":"struct User { fields }","说明":"定义结构体类型"},{"代码":"impl User { fn ... }","说明":"为结构体实现方法"},{"代码":"fn new(...) -> User","说明":"关联函数（无self），类似构造器"},{"代码":"fn method(&self)","说明":"实例方法，&self借用不可变"},{"代码":"fn method(&mut self)","说明":"可变方法，可修改字段"},{"代码":"..user1","说明":"结构体更新语法，从另一个实例复制字段"}]',
            'syntax_note': '字段初始化简写：字段名和变量同名可省略 fieldname:\\n结构体默认不可变，所有字段都不可变\\n.. 语法必须放在最后，且会移动所有权',
            'runnable_example': 'struct Rectangle {\n    width: u32,\n    height: u32,\n}\n\nimpl Rectangle {\n    fn area(&self) -> u32 {\n        self.width * self.height\n    }\n    \n    fn can_hold(&self, other: &Rectangle) -> bool {\n        self.width > other.width && self.height > other.height\n    }\n}\n\nfn main() {\n    let rect = Rectangle { width: 30, height: 50 };\n    println!("面积: {}", rect.area());  // 1500\n}',
            'common_errors': '[{"报错":"field is private","解决办法":"结构体默认私有，需加 pub 关键字"},{"报错":"missing field","解决办法":"创建结构体时必须提供所有字段"}]',
            'aliases': '结构体,struct,impl,方法',
        },
        {
            'title': '枚举 Option/Result',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': '// Option 枚举（可能有值或空）\nfn divide(numerator: f64, denominator: f64) -> Option<f64> {\n    if denominator == 0.0 {\n        None  // 返回空\n    } else {\n        Some(numerator / denominator)  // 返回值\n    }\n}\n\n// Result 枚举（成功或错误）\nfn parse_number(s: &str) -> Result<i32, String> {\n    match s.parse::<i32>() {\n        Ok(n) => Ok(n),\n        Err(_) => Err(format!("无法解析: {}", s)),\n    }\n}\n\nfn main() {\n    // 使用 Option\n    let result = divide(10.0, 2.0);\n    match result {\n        Some(val) => println!("结果: {}", val),\n        None => println!("不能除以零"),\n    }\n\n    // 使用 Result\n    match parse_number("42") {\n        Ok(n) => println!("数字: {}", n),\n        Err(e) => println!("错误: {}", e),\n    }\n\n    // 简写：unwrap（不推荐，会 panic）\n    // let val = divide(10.0, 0.0).unwrap();  // panic!\n\n    // 安全简写\n    if let Some(val) = divide(10.0, 2.0) {\n        println!("{}", val);\n    }\n}',
            'line_by_line': '[{"代码":"Option<T>","说明":"有值Some(T)或空None"},{"代码":"Result<T, E>","说明":"成功Ok(T)或失败Err(E)"},{"代码":"Some(val) / None","说明":"Option的两种变体"},{"代码":"Ok(val) / Err(err)","说明":"Result的两种变体"},{"代码":".unwrap()","说明":"取值或panic（快速失败，不推荐）"},{"代码":"if let Some(val) = ...","说明":"只关心一种情况的简写"}]',
            'syntax_note': 'Option 和 Result 是 Rust 最常用的枚举\\n没有 null 值，用 Option 表示可空\\n? 运算符可以传播错误（见错误处理条目）\\n推荐用模式匹配，少用 unwrap',
            'runnable_example': 'fn find_first_even(numbers: &[i32]) -> Option<&i32> {\n    for n in numbers {\n        if n % 2 == 0 {\n            return Some(n);\n        }\n    }\n    None\n}\n\nfn main() {\n    let nums = [1, 3, 5, 6, 7];\n    match find_first_even(&nums) {\n        Some(n) => println!("第一个偶数: {}", n),\n        None => println!("没有偶数"),\n    }\n}',
            'common_errors': '[{"报错":"called `Option::unwrap()` on a `None` value","解决办法":"用 match 或 if let 安全处理"}]',
            'aliases': 'Option,Result,枚举,错误处理,unwrap',
        },
        {
            'title': '错误处理 ? 运算符',
            'language': 'Rust',
            'version': '>=1.0',
            'code_block': 'use std::fs::File;\nuse std::io::{self, Read};\n\n// 读取文件内容，? 自动传播错误\nfn read_username_from_file(path: &str) -> Result<String, io::Error> {\n    let mut file = File::open(path)?;  // 出错则提前return Err\n    let mut contents = String::new();\n    file.read_to_string(&mut contents)?;\n    Ok(contents)\n}\n\n// 链式调用\nfn read_username_short(path: &str) -> Result<String, io::Error> {\n    let mut contents = String::new();\n    File::open(path)?.read_to_string(&mut contents)?;\n    Ok(contents)\n}\n\nfn main() {\n    // 调用含错误传播的函数\n    match read_username_from_file("user.txt") {\n        Ok(name) => println!("用户名: {}", name.trim()),\n        Err(e) => println!("读取失败: {}", e),\n    }\n\n    // main 函数也可以返回 Result\n    // fn main() -> Result<(), Box<dyn Error>> { ... Ok(()) }\n}',
            'line_by_line': '[{"代码":"File::open(path)?","说明":"? 运算符：成功则取出值，失败则return Err"},{"代码":".read_to_string(&mut s)?","说明":"? 可以链式调用"},{"代码":"Result<String, io::Error>","说明":"返回值类型必须与 ? 传播的错误类型兼容"},{"代码":"fn main() -> Result<...>","说明":"main函数也可以返回Result"}]',
            'syntax_note': '? 运算符只能用于返回 Result 或 Option 的函数\\n? 会调用 From trait 自动转换错误类型\\n处理多种错误类型时用 Box<dyn Error> 或自定义错误',
            'runnable_example': 'use std::num::ParseIntError;\n\nfn parse_and_sum(a: &str, b: &str) -> Result<i32, ParseIntError> {\n    let na: i32 = a.parse()?;\n    let nb: i32 = b.parse()?;\n    Ok(na + nb)\n}\n\nfn main() {\n    match parse_and_sum("10", "20") {\n        Ok(sum) => println!("和: {}", sum),\n        Err(e) => println!("解析错误: {}", e),\n    }\n}',
            'common_errors': '[{"报错":"cannot use `?` operator in a function that returns `()`","解决办法":"将函数返回值改为Result或Option类型"}]',
            'aliases': '错误处理,?运算符,错误传播,Result',
        },
    ]
    for s in snippets:
        s['category_id'] = rust_cat
        db.add_snippet(**s)
    print(f"✅ Rust: {len(snippets)} 条")

# ==========================================================
# Java 片段（10条）
# ==========================================================
java_cat = get_cat('编程语言', 'Java')
if java_cat:
    snippets = [
        {
            'title': 'Hello World',
            'language': 'Java',
            'version': '>=8',
            'code_block': 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
            'line_by_line': '[{"代码":"public class Main","说明":"定义公共类，类名必须与文件名一致"},{"代码":"public static void main(String[] args)","说明":"程序入口，固定写法"},{"代码":"System.out.println(...)","说明":"打印一行文本到控制台"}]',
            'syntax_note': '文件名必须和类名相同（Main.java）\\nJava 区分大小写\\n每个语句以分号结束',
            'runnable_example': '// Main.java\n// 编译: javac Main.java\n// 运行: java Main\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("你好，世界！");\n    }\n}',
            'common_errors': '[{"报错":"找不到或无法加载主类","解决办法":"检查类名和文件名是否一致"},{"报错":"Error: Could not find or load main class","解决办法":"执行 java 时不要加 .class 扩展名"}]',
            'aliases': 'Hello World,入口,main函数',
        },
        {
            'title': 'ArrayList 使用',
            'language': 'Java',
            'version': '>=8',
            'code_block': 'import java.util.ArrayList;\n\npublic class Main {\n    public static void main(String[] args) {\n        // 创建ArrayList\n        ArrayList<String> fruits = new ArrayList<>();\n\n        // 添加元素\n        fruits.add("苹果");\n        fruits.add("香蕉");\n        fruits.add("橙子");\n\n        // 获取元素\n        String first = fruits.get(0);\n        System.out.println("第一个: " + first);\n\n        // 修改元素\n        fruits.set(1, "葡萄");\n\n        // 删除元素\n        fruits.remove(2);\n\n        // 遍历\n        for (String fruit : fruits) {\n            System.out.println(fruit);\n        }\n\n        // 方法\n        System.out.println("大小: " + fruits.size());\n        System.out.println("是否为空: " + fruits.isEmpty());\n        System.out.println("是否包含: " + fruits.contains("苹果"));\n    }\n}',
            'line_by_line': '[{"代码":"ArrayList<String> list = new ArrayList<>()","说明":"创建字符串类型的ArrayList"},{"代码":"list.add(item)","说明":"在末尾添加元素"},{"代码":"list.get(index)","说明":"获取指定索引的元素"},{"代码":"list.set(index, item)","说明":"修改指定索引的元素"},{"代码":"list.remove(index)","说明":"删除指定索引的元素"},{"代码":"for (String s : list)","说明":"增强for循环遍历"}]',
            'syntax_note': 'ArrayList 是动态数组，自动扩容\\n尖括号里是泛型类型，不能是基本类型（用 Integer）\\nArrayList 不是线程安全的\\n相比数组，ArrayList 可以动态增删',
            'runnable_example': 'import java.util.ArrayList;\n\npublic class Main {\n    public static void main(String[] args) {\n        ArrayList<Integer> scores = new ArrayList<>();\n        scores.add(85);\n        scores.add(92);\n        scores.add(78);\n        \n        int sum = 0;\n        for (int s : scores) sum += s;\n        double avg = (double) sum / scores.size();\n        System.out.println("平均分: " + avg);  // 85.0\n    }\n}',
            'common_errors': '[{"报错":"IndexOutOfBoundsException","解决办法":"检查索引是否在0到size()-1范围内"}]',
            'aliases': 'ArrayList,动态数组,列表',
        },
    ]
    for s in snippets:
        s['category_id'] = java_cat
        db.add_snippet(**s)
    print(f"✅ Java: {len(snippets)} 条")

# ==========================================================
# C 语言片段（8条）
# ==========================================================
c_cat = get_cat('编程语言', 'C语言')
if c_cat:
    snippets = [
        {
            'title': 'Hello World',
            'language': 'C',
            'version': 'C99+',
            'code_block': '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
            'line_by_line': '[{"代码":"#include <stdio.h>","说明":"引入标准输入输出库"},{"代码":"int main()","说明":"主函数，程序入口"},{"代码":"printf(...)","说明":"格式化输出函数"},{"代码":"return 0","说明":"返回0表示程序正常结束"}]',
            'syntax_note': 'C 程序从 main() 函数开始执行\\n#include 是预处理指令（不是语句，无分号）\\n每条语句以分号结束',
            'runnable_example': '// 编译: gcc main.c -o main\n// 运行: ./main\n#include <stdio.h>\nint main() {\n    printf("你好，世界！\\n");\n    return 0;\n}',
            'common_errors': '[]',
            'aliases': 'Hello World,C入门',
        },
        {
            'title': '指针基本操作',
            'language': 'C',
            'version': 'C99+',
            'code_block': '#include <stdio.h>\n\nint main() {\n    int x = 42;\n    int *p = &x;  // p 保存 x 的地址\n\n    printf("x 的值: %d\\n", x);        // 42\n    printf("x 的地址: %p\\n", &x);      // 0x...\n    printf("指针 p 的值: %p\\n", p);    // 同 x 地址\n    printf("p 指向的值: %d\\n", *p);    // 42（解引用）\n\n    // 通过指针修改值\n    *p = 100;\n    printf("修改后 x = %d\\n", x);      // 100\n\n    return 0;\n}',
            'line_by_line': '[{"代码":"int *p = &x","说明":"声明指针p，用&取x的地址初始化"},{"代码":"*p","说明":"解引用，获取指针指向的值"},{"代码":"&x","说明":"取地址运算符，获取变量的内存地址"},{"代码":"%p","说明":"printf格式说明符，打印地址"}]',
            'syntax_note': '指针保存的是内存地址\\n* 在声明时是指针类型标记，在使用时是解引用\\n指针必须初始化，否则是野指针（危险）\\nNULL 指针不指向任何有效地址',
            'runnable_example': '#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}\n\nint main() {\n    int x = 10, y = 20;\n    printf("交换前: x=%d, y=%d\\n", x, y);\n    swap(&x, &y);\n    printf("交换后: x=%d, y=%d\\n", x, y);\n    return 0;\n}',
            'common_errors': '[{"报错":"Segmentation fault","解决办法":"检查指针是否初始化，是否访问了非法地址"}]',
            'aliases': '指针,pointer,内存地址',
        },
    ]
    for s in snippets:
        s['category_id'] = c_cat
        db.add_snippet(**s)
    print(f"✅ C: {len(snippets)} 条")

# ==========================================================
# HTML 片段（10条）
# ==========================================================
html_cat = get_cat('前端技术', 'HTML')
if html_cat:
    snippets = [
        {
            'title': '基本文档结构',
            'language': 'HTML',
            'version': 'HTML5',
            'code_block': '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>页面标题</title>\n</head>\n<body>\n    <h1>欢迎来到我的页面</h1>\n    <p>这是一个段落。</p>\n</body>\n</html>',
            'line_by_line': '[{"代码":"<!DOCTYPE html>","说明":"文档类型声明，告诉浏览器这是HTML5"},{"代码":"<html lang=\\"zh-CN\\">","说明":"根元素，lang指定语言"},{"代码":"<head>","说明":"头部，放元数据（不显示在页面上）"},{"代码":"<meta charset=\\"UTF-8\\">","说明":"设置字符编码，支持中文"},{"代码":"<title>","说明":"浏览器标签页的标题"},{"代码":"<body>","说明":"主体，所有可见内容放这里"}]',
            'syntax_note': 'HTML 是标记语言，不是编程语言\\n标签通常成对出现 <tag></tag>\\n自闭合标签如 <br>、<img> 不需要结束标签\\n缩进不影响渲染，但影响可读性',
            'runnable_example': '<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n    <title>我的第一个页面</title>\n</head>\n<body>\n    <h1>你好，世界！</h1>\n    <p>这是我的第一个HTML页面。</p>\n</body>\n</html>',
            'common_errors': '[]',
            'aliases': 'HTML结构,文档结构,html骨架',
        },
        {
            'title': '常用标签：链接/图片/文本',
            'language': 'HTML',
            'version': 'HTML5',
            'code_block': '<!-- 标题标签 -->\n<h1>一级标题</h1>\n<h2>二级标题</h2>\n<h3>三级标题</h3>\n\n<!-- 段落和文本 -->\n<p>这是一个段落。</p>\n<span>行内文本</span>\n<strong>加粗</strong>\n<em>斜体</em>\n<br>  <!-- 换行 -->\n<hr>  <!-- 分割线 -->\n\n<!-- 链接 -->\n<a href="https://example.com" target="_blank">打开新窗口</a>\n<a href="#section2">锚点跳转</a>\n\n<!-- 图片 -->\n<img src="photo.jpg" alt="照片描述" width="300" height="200">\n\n<!-- div 块级容器 -->\n<div class="container">\n    <p>这是一个区块</p>\n</div>',
            'line_by_line': '[{"代码":"<h1>~<h6>","说明":"标题标签，h1最大h6最小"},{"代码":"<p>段落</p>","说明":"段落标签，自动上下留白"},{"代码":"<a href=\\"url\\">链接</a>","说明":"超链接，href指定目标地址"},{"代码":"<img src=\\"path\\" alt=\\"描述\\">","说明":"图片标签，alt属性对无障碍很重要"},{"代码":"<div>...</div>","说明":"块级容器，常用于布局"},{"代码":"<span>...</span>","说明":"行内容器，包裹小段文本"}]',
            'syntax_note': 'a 标签的 target="_blank" 在新标签页打开链接\\nimg 的 alt 属性在图片加载失败时显示，也有利于SEO\\n自闭合标签不需要 </> 结尾',
            'runnable_example': '<!-- 一个简单的卡片 -->\n<div style="border: 1px solid #ddd; padding: 16px; max-width: 300px;">\n    <img src="https://via.placeholder.com/300x200" alt="示例图片" style="width: 100%;">\n    <h2>卡片标题</h2>\n    <p>这是一段卡片描述文字。</p>\n    <a href="#">了解更多 →</a>\n</div>',
            'common_errors': '[]',
            'aliases': 'HTML标签,链接,图片,文本标签',
        },
    ]
    for s in snippets:
        s['category_id'] = html_cat
        db.add_snippet(**s)
    print(f"✅ HTML: {len(snippets)} 条")

# ==========================================================
# CSS 片段（10条）
# ==========================================================
css_cat = get_cat('前端技术', 'CSS')
if css_cat:
    snippets = [
        {
            'title': '选择器：类/ID/标签/属性',
            'language': 'CSS',
            'version': 'CSS3',
            'code_block': '/* 标签选择器 */\np {\n    color: blue;\n    font-size: 16px;\n}\n\n/* 类选择器 */\n.highlight {\n    background-color: yellow;\n}\n\n/* ID选择器 */\n#header {\n    background: #333;\n    color: white;\n}\n\n/* 属性选择器 */\n[type="text"] {\n    border: 1px solid #ccc;\n}\n\n/* 后代选择器 */\n.container p {\n    margin: 10px;\n}\n\n/* 子选择器 */\n.container > p {\n    font-weight: bold;\n}\n\n/* 组合选择器 */\nh1, h2, h3 {\n    font-family: Arial, sans-serif;\n}',
            'line_by_line': '[{"代码":".类名","说明":"类选择器，匹配所有class包含此名的元素"},{"代码":"#ID名","说明":"ID选择器，匹配唯一ID的元素"},{"代码":"标签名","说明":"标签选择器，匹配所有此标签"},{"代码":"[属性=\\"值\\"]","说明":"属性选择器，匹配有指定属性的元素"},{"代码":"祖先 后代","说明":"后代选择器（空格），选所有后代"},{"代码":"父 > 子","说明":"子选择器（>），只选直接子元素"}]',
            'syntax_note': '类选择器用 . 开头，ID选择器用 # 开头\\nID 在页面中唯一，类可以重复使用\\n多个选择器用逗号分隔表示"或"关系\\n权重：ID > 类 > 标签（100 > 10 > 1）',
            'runnable_example': '/* HTML: <button class="btn primary">提交</button> */\\n.btn {\\n    padding: 8px 16px;\\n    border: none;\\n    border-radius: 4px;\\n    cursor: pointer;\\n}\\n.btn.primary {\\n    background-color: #007bff;\\n    color: white;\\n}\\n.btn.primary:hover {\\n    background-color: #0056b3;\\n}',
            'common_errors': '[]',
            'aliases': 'CSS选择器,选择器,class,id',
        },
        {
            'title': 'Flexbox 布局',
            'language': 'CSS',
            'version': 'CSS3',
            'code_block': '.container {\n    display: flex;           /* 启用flex布局 */\n    flex-direction: row;     /* 主轴方向：row/column */\n    justify-content: center; /* 主轴对齐 */\n    align-items: center;     /* 交叉轴对齐 */\n    flex-wrap: wrap;         /* 是否换行 */\n    gap: 16px;               /* 项目间距 */\n}\n\n.item {\n    flex: 1;                 /* 等分剩余空间 */\n    min-width: 200px;        /* 最小宽度 */\n}\n\n/* 常见对齐值 */\n/* justify-content: flex-start | center | flex-end | space-between | space-around */\n/* align-items: stretch | center | flex-start | flex-end */\n/* flex-direction: row | column | row-reverse | column-reverse */',
            'line_by_line': '[{"代码":"display: flex","说明":"开启Flexbox布局"},{"代码":"flex-direction","说明":"设置主轴方向（横/竖）"},{"代码":"justify-content","说明":"主轴方向上的对齐方式"},{"代码":"align-items","说明":"交叉轴方向上的对齐方式"},{"代码":"flex-wrap: wrap","说明":"子元素超出容器宽度时换行"},{"代码":"flex: 1","说明":"子元素等分剩余空间"},{"代码":"gap","说明":"子元素之间的间距"}]',
            'syntax_note': 'Flexbox 是一维布局，适合单行/单列排列\\n容器属性控制整体排列，项目属性控制单个元素\\njustify-content 沿主轴，align-items 沿交叉轴\\n使用 gap 替代 margin 更简洁',
            'runnable_example': '/* 水平居中的导航栏 */\\n.nav {\\n    display: flex;\\n    justify-content: space-between;\\n    align-items: center;\\n    padding: 0 20px;\\n    background: #333;\\n    height: 60px;\\n}\\n.nav a {\\n    color: white;\\n    text-decoration: none;\\n    padding: 0 15px;\\n}\\n\\n/* 三栏自适应布局 */\\n.layout {\\n    display: flex;\\n    gap: 20px;\\n}\\n.sidebar { width: 200px; }\\n.main { flex: 1; }',
            'common_errors': '[]',
            'aliases': 'flex,flexbox,弹性布局,布局',
        },
    ]
    for s in snippets:
        s['category_id'] = css_cat
        db.add_snippet(**s)
    print(f"✅ CSS: {len(snippets)} 条")

# ==========================================================
# Vue 片段（8条）
# ==========================================================
vue_cat = get_cat('前端技术', 'Vue')
if vue_cat:
    snippets = [
        {
            'title': '创建 Vue 应用',
            'language': 'Vue',
            'version': 'Vue 3',
            'code_block': '// 方式1: 使用CDN\n// <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>\nconst { createApp, ref } = Vue;\n\nconst app = createApp({\n    setup() {\n        const message = ref("你好，Vue！");\n        return { message };\n    }\n});\n\napp.mount("#app");\n\n// 方式2: 使用Vite创建项目\n// npm create vue@latest\n// 文件结构：\n// src/\n//   App.vue      - 根组件\n//   main.ts      - 入口文件\n//   components/  - 组件目录',
            'line_by_line': '[{"代码":"createApp({})","说明":"创建Vue应用实例"},{"代码":"setup()","说明":"组合式API入口，在组件创建前执行"},{"代码":"ref(\\"值\\")","说明":"创建响应式数据（支持任意类型）"},{"代码":"app.mount(\\"#app\\")","说明":"将应用挂载到DOM元素上"}]',
            'syntax_note': 'Vue 3 推荐使用组合式 API（setup）\\nref 用于基本类型和对象，reactive 只用于对象\\ntemplate 中可以自动解包 ref，不用写 .value',
            'runnable_example': '<div id="app">\\n    <h1>{{ message }}</h1>\\n    <button @click="count++">点击: {{ count }}</button>\\n</div>\\n\\n<script>\\nconst { createApp, ref } = Vue;\\ncreateApp({\\n    setup() {\\n        const message = ref("欢迎使用Vue！");\\n        const count = ref(0);\\n        return { message, count };\\n    }\\n}).mount("#app");\\n</script>',
            'common_errors': '[]',
            'aliases': 'Vue创建,Vue应用,createApp',
        },
        {
            'title': '数据绑定 v-bind/v-model',
            'language': 'Vue',
            'version': 'Vue 3',
            'code_block': '<template>\n    <!-- v-bind: 单向绑定属性（简写:） -->\n    <img :src="imageUrl" :alt="description">\n    <a :href="linkUrl" :class="{ active: isActive }">链接</a>\n\n    <!-- v-model: 双向绑定表单 -->\n    <input v-model="username" placeholder="用户名">\n    <textarea v-model="bio"></textarea>\n\n    <!-- 不同表单类型 -->\n    <select v-model="selected">\n        <option value="A">选项A</option>\n        <option value="B">选项B</option>\n    </select>\n    <input type="checkbox" v-model="agree"> 同意条款\n    <input type="radio" v-model="gender" value="male"> 男\n    <input type="radio" v-model="gender" value="female"> 女\n\n    <!-- 显示绑定的数据 -->\n    <p>用户名: {{ username }}</p>\n    <p>选择: {{ selected }}</p>\n</template>\n\n<script setup>\nimport { ref } from "vue";\n\nconst imageUrl = ref("https://example.com/photo.jpg");\nconst description = ref("示例图片");\nconst isActive = ref(true);\nconst username = ref("");\nconst bio = ref("");\nconst selected = ref("A");\nconst agree = ref(false);\nconst gender = ref("male");\n</script>',
            'line_by_line': '[{"代码":":src=\\"imageUrl\\"","说明":"v-bind简写，绑定HTML属性"},{"代码":":class=\\"{ active: isActive }\\"","说明":"动态绑定class，isActive为true则添加active类"},{"代码":"v-model=\\"username\\"","说明":"双向绑定，数据改变↔界面更新"},{"代码":"{{ username }}","说明":"文本插值，显示响应式数据"}]',
            'syntax_note': 'v-bind: 简写为 :，v-on: 简写为 @\\nv-model 是 v-bind + v-on 的语法糖\\nv-model 对于不同输入类型自动处理方式不同\\n推荐用 <script setup> 写法更简洁',
            'runnable_example': '<template>\\n    <div>\\n        <input v-model="name" placeholder="输入名字">\\n        <button :disabled="!name" @click="submit">提交</button>\\n        <p v-if="submitted">你好, {{ name }}!</p>\\n    </div>\\n</template>\\n\\n<script setup>\\nimport { ref } from "vue";\\nconst name = ref("");\\nconst submitted = ref(false);\\nconst submit = () => { submitted.value = true; };\\n</script>',
            'common_errors': '[]',
            'aliases': 'v-bind,v-model,数据绑定,双向绑定',
        },
    ]
    for s in snippets:
        s['category_id'] = vue_cat
        db.add_snippet(**s)
    print(f"✅ Vue: {len(snippets)} 条")

# ==========================================================
# React 片段（8条）
# ==========================================================
react_cat = get_cat('前端技术', 'React')
if react_cat:
    snippets = [
        {
            'title': '函数组件',
            'language': 'React',
            'version': 'React 18',
            'code_block': '// 定义函数组件\nfunction Welcome(props) {\n    return <h1>你好, {props.name}!</h1>;\n}\n\n// 箭头函数写法\nconst Welcome2 = ({ name }) => {\n    return <h1>你好, {name}!</h1>;\n};\n\n// 使用组件\nfunction App() {\n    return (\n        <div>\n            <Welcome name="张三" />\n            <Welcome name="李四" />\n            <Welcome2 name="王五" />\n        </div>\n    );\n}\n\nexport default App;',
            'line_by_line': '[{"代码":"function Welcome(props)","说明":"函数组件，接收props参数"},{"代码":"return <h1>...</h1>","说明":"返回JSX（类HTML语法）"},{"代码":"{props.name}","说明":"JSX中用花括号插入JavaScript表达式"},{"代码":"<Welcome name=\\"张三\\" />","说明":"使用组件并传入props"},{"代码":"({ name })","说明":"解构props，直接使用属性名"}]',
            'syntax_note': '函数组件首字母必须大写（与HTML标签区分）\\nJSX 不是字符串也不是HTML，是JavaScript语法扩展\\n组件返回的JSX必须有单个根元素或用<></>包裹\\nprops 是只读的，不能修改',
            'runnable_example': '// App.jsx\\nfunction Greeting({ name, time }) {\\n    const hour = new Date().getHours();\\n    const greeting = hour < 12 ? "早上好" : hour < 18 ? "下午好" : "晚上好";\\n    return <h2>{greeting}, {name}！</h2>;\\n}\\n\\nexport default function App() {\\n    return <Greeting name="张三" />;\\n}',
            'common_errors': '[{"报错":"JSX 必须有一个父元素","解决办法":"用 <></> 或 <div> 包裹多个元素"}]',
            'aliases': '组件,函数组件,React组件,props',
        },
        {
            'title': 'useState Hook',
            'language': 'React',
            'version': 'React 16.8+',
            'code_block': 'import { useState } from "react";\n\nfunction Counter() {\n    // 声明状态变量\n    // count: 当前值, setCount: 更新函数\n    const [count, setCount] = useState(0);\n\n    return (\n        <div>\n            <p>计数: {count}</p>\n            <button onClick={() => setCount(count + 1)}>+1</button>\n            <button onClick={() => setCount(count - 1)}>-1</button>\n            <button onClick={() => setCount(0)}>重置</button>\n        </div>\n    );\n}\n\n// 复杂状态\nfunction UserForm() {\n    const [user, setUser] = useState({ name: "", age: 0 });\n\n    const updateName = (e) => {\n        setUser({ ...user, name: e.target.value });\n    };\n\n    return (\n        <div>\n            <input value={user.name} onChange={updateName} />\n            <p>你好, {user.name}</p>\n        </div>\n    );\n}',
            'line_by_line': '[{"代码":"useState(初始值)","说明":"声明状态变量，参数是初始值"},{"代码":"const [count, setCount] = useState(0)","说明":"解构出状态值和更新函数"},{"代码":"setCount(newValue)","说明":"更新状态，触发重新渲染"},{"代码":"setUser({...user, name: val})","说明":"更新对象状态，要展开旧值"}]',
            'syntax_note': 'useState 是 Hook，只能在函数组件顶层调用\\n状态更新是异步的，不会立即生效\\n更新对象或数组时，要创建新的引用（不可变更新）\\nsetState 传入函数可基于旧值更新：setCount(c => c + 1)',
            'runnable_example': 'import { useState } from "react";\\n\\nfunction TodoList() {\\n    const [todos, setTodos] = useState(["写代码", "测试"]);\\n    const [input, setInput] = useState("");\\n\\n    const addTodo = () => {\\n        if (input.trim()) {\\n            setTodos([...todos, input]);\\n            setInput("");\\n        }\\n    };\\n\\n    return (\\n        <div>\\n            <input value={input} onChange={e => setInput(e.target.value)} />\\n            <button onClick={addTodo}>添加</button>\\n            <ul>\\n                {todos.map((todo, i) => <li key={i}>{todo}</li>)}\\n            </ul>\\n        </div>\\n    );\\n}',
            'common_errors': '[{"报错":"Too many re-renders","解决办法":"不要在渲染中直接调用setState，要用事件处理函数"}]',
            'aliases': 'useState,Hook,状态管理,React Hooks',
        },
    ]
    for s in snippets:
        s['category_id'] = react_cat
        db.add_snippet(**s)
    print(f"✅ React: {len(snippets)} 条")

# ==========================================================
# Shell 脚本（8条）
# ==========================================================
shell_cat = get_cat('编程语言', 'Shell脚本')
if shell_cat:
    snippets = [
        {
            'title': 'Shell 变量定义与使用',
            'language': 'Shell',
            'version': 'Bash 4+',
            'code_block': '#!/bin/bash\n# 变量定义（等号两边不能有空格）\nname="张三"\nage=28\n\n# 使用变量（$变量名 或 ${变量名}）\necho "姓名: $name"\necho "年龄: ${age}"\n\n# 只读变量\nreadonly PI=3.14159\n\n# 删除变量\nunset temp\n\n# 特殊变量\necho "脚本名: $0"\necho "参数个数: $#"\necho "所有参数: $@"\necho "上一个命令退出码: $?"\necho "当前PID: $$"',
            'line_by_line': '[{"代码":"name=\\"张三\\"","说明":"定义变量，等号两边不能有空格"},{"代码":"$name 或 ${name}","说明":"引用变量的值，花括号用于明确边界"},{"代码":"readonly PI=...","说明":"只读变量，定义后不能修改"},{"代码":"$0, $#, $@","说明":"脚本名、参数个数、所有参数"},{"代码":"$?","说明":"上一条命令的退出码（0=成功）"},{"代码":"$$","说明":"当前Shell进程的PID"}]',
            'syntax_note': '变量默认是全局的，函数内用 local 声明局部变量\\n双引号引用变量会解析，单引号不会\\n反引号或 $() 用于命令替换',
            'runnable_example': '#!/bin/bash\\n# 获取当前日期并格式化输出\\nTODAY=$(date +%Y-%m-%d)\\necho "今天是: $TODAY"\\n\\n# 计算\\nA=10\\nB=20\\nSUM=$((A + B))\\necho "$A + $B = $SUM"',
            'common_errors': '[]',
            'aliases': 'Shell变量,变量,bash变量',
        },
        {
            'title': 'Shell 条件判断 if',
            'language': 'Shell',
            'version': 'Bash 4+',
            'code_block': '#!/bin/bash\n\n# if 基本语法\nif [ 条件 ]; then\n    # 条件为真时执行\nelif [ 条件 ]; then\n    # 另一个条件\nelse\n    # 都不满足时执行\nfi\n\n# 数值比较\nif [ "$age" -gt 18 ]; then\n    echo "成年人"\nfi\n# -eq 等于  -ne 不等于  -gt 大于  -lt 小于  -ge 大于等于  -le 小于等于\n\n# 字符串比较\nif [ "$name" = "张三" ]; then\n    echo "匹配"\nfi\n# = 等于  != 不等于  -z 空字符串  -n 非空\n\n# 文件判断\nif [ -f "file.txt" ]; then\n    echo "是普通文件"\nfi\nif [ -d "dir" ]; then\n    echo "是目录"\nfi\n# -e 存在  -r 可读  -w 可写  -x 可执行\n\n# 逻辑运算\nif [ "$a" -gt 0 ] && [ "$b" -lt 10 ]; then\n    echo "a>0 且 b<10"\nfi',
            'line_by_line': '[{"代码":"if [ 条件 ]; then","说明":"if 判断，条件用方括号包裹"},{"代码":"-gt, -lt","说明":"数值比较运算符（大于、小于）"},{"代码":"=, !=","说明":"字符串比较"},{"代码":"-f, -d","说明":"文件类型判断（文件、目录）"},{"代码":"&&, ||","说明":"逻辑与、逻辑或"},{"代码":"fi","说明":"if 语句结束"}]',
            'syntax_note': '方括号 [ 前后必须有空格\\n字符串比较用 =，数值比较用 -eq\\n条件判断的退出码 0 为真，非 0 为假',
            'runnable_example': '#!/bin/bash\\n# 检查文件是否存在，不存在则创建\\nFILE="config.txt"\\nif [ ! -f "$FILE" ]; then\\n    echo "文件不存在，正在创建..."\\n    touch "$FILE"\\n    echo "created at $(date)" > "$FILE"\\nelse\\n    echo "文件已存在，内容如下:"\\n    cat "$FILE"\\nfi',
            'common_errors': '[]',
            'aliases': 'if判断,条件判断,bash if',
        },
    ]
    for s in snippets:
        s['category_id'] = shell_cat
        db.add_snippet(**s)
    print(f"✅ Shell: {len(snippets)} 条")

# ==========================================================
print(f"\\n{'='*50}")
print(f"代码片段种子数据插入完成！")
print(f"总条数: {db.get_total_count()}")
print(f"{'='*50}")
