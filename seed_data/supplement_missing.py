#!/usr/bin/env python3
"""补充缺失语言种子数据：C#/PHP/Ruby/Auto.js"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

db = DBManager()
db.init_db()

def find_cat(parent_name, child_name):
    for root in db.get_categories(parent_id=None):
        if root['name'] == parent_name:
            for child in db.get_categories(parent_id=root['id']):
                if child['name'] == child_name:
                    return child['id']
    return None

def add_all(cat_id, items):
    for item in items:
        item['category_id'] = cat_id
        db.add_snippet(**item)

# ============ C#（8条） ============
cat = find_cat('编程语言', 'C#')
if cat:
    items = [
        {
            'title': 'Hello World',
            'language': 'C#', 'version': '>=10',
            'code_block': 'using System;\n\nclass Program\n{\n    static void Main(string[] args)\n    {\n        Console.WriteLine("Hello, World!");\n        Console.WriteLine($"1+1={1+1}");\n    }\n}',
            'line_by_line': '[{"代码":"using System","说明":"引入System命名空间"},{"代码":"class Program","说明":"类定义"},{"代码":"static void Main","说明":"程序入口方法"},{"代码":"Console.WriteLine","说明":"输出到控制台"}]',
            'syntax_note': 'C# 是大小写敏感的\\nMain 方法首字母大写\\n$ 字符串插值类似 Python 的 f-string',
            'runnable_example': '// dotnet new console -n Hello\\n// dotnet run\\nusing System;\\nclass Program {\\n    static void Main() {\\n        Console.WriteLine("你好！");\\n    }\\n}',
            'common_errors': '[]',
            'aliases': 'Hello World,C#入门',
        },
        {
            'title': 'List<T> 泛型列表',
            'language': 'C#', 'version': '>=8',
            'code_block': 'using System;\nusing System.Collections.Generic;\nusing System.Linq;\n\nclass Program\n{\n    static void Main()\n    {\n        // 创建列表\n        List<string> fruits = new List<string> { "苹果", "香蕉", "橙子" };\n        \n        // 添加\n        fruits.Add("葡萄");\n        fruits.Insert(1, "草莓");  // 在索引1插入\n        \n        // 访问\n        Console.WriteLine(fruits[0]);\n        \n        // 删除\n        fruits.Remove("香蕉");\n        fruits.RemoveAt(0);\n        \n        // 遍历\n        foreach (var fruit in fruits)\n        {\n            Console.WriteLine(fruit);\n        }\n        \n        // LINQ 查询\n        var longNames = fruits.Where(f => f.Length > 1).ToList();\n        var sorted = fruits.OrderBy(f => f).ToList();\n        \n        Console.WriteLine($"总数: {fruits.Count}");\n    }\n}',
            'line_by_line': '[{"代码":"List<T>","说明":"泛型列表，类似C++的vector"},{"代码":"Add() / Remove()","说明":"添加/删除元素"},{"代码":"foreach (var x in list)","说明":"遍历集合"},{"代码":"Where() / OrderBy()","说明":"LINQ扩展方法，需using System.Linq"}]',
            'syntax_note': 'List<T> 是数组的泛型版本，自动扩容\\nLINQ 查询在集合操作中非常强大\\nvar 关键字让编译器推断类型',
            'runnable_example': 'using System;\\nusing System.Collections.Generic;\\nusing System.Linq;\\n\\nvar scores = new List<int> { 85, 92, 78, 90 };\\nvar avg = scores.Average();\\nvar max = scores.Max();\\nConsole.WriteLine($"平均: {avg}, 最高: {max}");',
            'common_errors': '[]',
            'aliases': 'List<T>,泛型列表,集合',
        },
    ]
    add_all(cat, items)
    print(f'[OK] C# +{len(items)}')

# ============ PHP（8条） ============
cat = find_cat('编程语言', 'PHP')
if cat:
    items = [
        {
            'title': '数组与 foreach 遍历',
            'language': 'PHP', 'version': '>=8',
            'code_block': '<?php\n// 索引数组\n$fruits = ["苹果", "香蕉", "橙子"];\necho $fruits[0];  // 苹果\n\n// 关联数组\n$user = [\n    "name" => "张三",\n    "age" => 28,\n    "city" => "北京"\n];\necho $user["name"];  // 张三\n\n// foreach 遍历\nforeach ($fruits as $fruit) {\n    echo $fruit . "\\n";\n}\n\nforeach ($user as $key => $value) {\n    echo "$key: $value\\n";\n}\n\n// 数组操作\n$numbers = [3, 1, 4, 1, 5];\nsort($numbers);\necho implode(", ", $numbers);  // 1, 1, 3, 4, 5\n\n// 添加元素\n$fruits[] = "葡萄";  // 追加到末尾\narray_push($fruits, "草莓");\necho count($fruits);  // 5\n?>',
            'line_by_line': '[{"代码":"$arr = [...]","说明":"数组定义，索引数组或关联数组"},{"代码":"foreach ($arr as $v)","说明":"遍历值"},{"代码":"foreach ($arr as $k => $v)","说明":"遍历键值对"},{"代码":"sort($arr)","说明":"数组排序"},{"代码":"implode(glue, arr)","说明":"数组拼接为字符串"}]',
            'syntax_note': 'PHP 变量以 $ 开头\\n数组用 [] 而非 array()（PHP 5.4+）\\necho 输出，print_r() 打印数组结构',
            'runnable_example': '<?php\\n$scores = ["张三" => 85, "李四" => 92, "王五" => 78];\\n$maxScore = max($scores);\\n$bestStudent = array_search($maxScore, $scores);\\necho "最高分: $bestStudent ($maxScore分)";\\n?>',
            'common_errors': '[]',
            'aliases': '数组,foreach,PHP数组',
        },
        {
            'title': 'PDO 数据库操作',
            'language': 'PHP', 'version': '>=8',
            'code_block': '<?php\n$host = "localhost";\n$dbname = "test";\n$username = "root";\n$password = "";\n\ntry {\n    // 连接\n    $pdo = new PDO(\n        "mysql:host=$host;dbname=$dbname;charset=utf8",\n        $username,\n        $password\n    );\n    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);\n\n    // 查询\n    $stmt = $pdo->query("SELECT * FROM users");\n    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {\n        echo $row["name"] . "\\n";\n    }\n\n    // 预处理（防SQL注入）\n    $stmt = $pdo->prepare("SELECT * FROM users WHERE age > ?");\n    $stmt->execute([18]);\n    $users = $stmt->fetchAll();\n\n    // 插入\n    $stmt = $pdo->prepare(\n        "INSERT INTO users (name, age) VALUES (:name, :age)"\n    );\n    $stmt->execute([\n        ":name" => "张三",\n        ":age" => 28\n    ]);\n    echo "插入ID: " . $pdo->lastInsertId();\n\n} catch (PDOException $e) {\n    echo "数据库错误: " . $e->getMessage();\n}\n?>',
            'line_by_line': '[{"代码":"new PDO(dsn, user, pass)","说明":"创建PDO数据库连接"},{"代码":"ER RMODE_EXCEPTION","说明":"错误模式设为抛异常"},{"代码":"query(SQL)","说明":"执行查询，返回PDOStatement"},{"代码":"prepare(SQL)","说明":"预处理语句（防SQL注入）"},{"代码":"execute(params)","说明":"执行预处理并传入参数"},{"代码":"fetch(ASSOC) / fetchAll()","说明":"获取一行/所有结果"}]',
            'syntax_note': 'PDO 支持多种数据库（MySQL/SQLite/PostgreSQL）\\n用预处理语句代替拼接 SQL 防止注入\\nPDO::FETCH_ASSOC 返回关联数组',
            'runnable_example': '<?php\\n$pdo = new PDO("sqlite:test.db");\\n$pdo->exec("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)");\\n$stmt = $pdo->prepare("INSERT INTO users VALUES (?, ?)");\\n$stmt->execute([1, "张三"]);\\nforeach($pdo->query("SELECT * FROM users") as $row) {\\n    print_r($row);\\n}\\n?>',
            'common_errors': '[{"报错":"could not find driver","解决办法":"安装PDO扩展，如 php-mysql"}]',
            'aliases': 'PDO,数据库,MySQL,SQL注入防护',
        },
    ]
    add_all(cat, items)
    print(f'[OK] PHP +{len(items)}')

# ============ Ruby（8条） ============
cat = find_cat('编程语言', 'Ruby')
if cat:
    items = [
        {
            'title': 'Hello World 与基本语法',
            'language': 'Ruby', 'version': '>=3.0',
            'code_block': '# 输出\nputs "Hello, World!"\nprint "不换行输出"\np [1, 2, 3]  # 打印数组\n\n# 变量（无需声明类型）\nname = "张三"\nage = 28\n\n# 字符串插值\nputs "我叫#{name}，今年#{age}岁"\n\n# 方法定义\ndef greet(name)\n  \"你好，#{name}！\"\nend\n\nputs greet("李四")\n\n# 条件判断\nif age >= 18\n  puts "成年人"\nelse\n  puts "未成年"\nend\n\n# unless（if的反向）\nunless age < 18\n  puts "可以喝酒"\nend\n\n# 三元运算符\nstatus = age >= 60 ? "老人" : "非老人"\nputs status',
            'line_by_line': '[{"代码":"puts / print / p","说明":"puts=换行输出，print=不换行，p=调试输出"},{"代码":"#{var}","说明":"字符串插值，类似Python f-string"},{"代码":"def name\\nend","说明":"方法定义，用end结束"},{"代码":"unless 条件","说明":"if not 的简写"}]',
            'syntax_note': 'Ruby 中一切皆对象\\n不需要分号结尾\\n方法最后一行表达式自动作为返回值',
            'runnable_example': '# hello.rb\\n# 运行: ruby hello.rb\\ndef say_hello(name)\\n  "Hello, #{name}!"\\nend\\n\\nputs say_hello("Ruby")\\nputs say_hello("世界")',
            'common_errors': '[]',
            'aliases': 'Hello World,Ruby基本语法,puts',
        },
        {
            'title': 'Hash 与 Symbol',
            'language': 'Ruby', 'version': '>=3.0',
            'code_block': '# Hash 创建\nuser = {\n  "name" => "张三",\n  "age" => 28,\n  "city" => "北京"\n}\nputs user["name"]  # 张三\n\n# Symbol 作为键（推荐）\nuser = {\n  name: "张三",   # 等价于 :name => "张三"\n  age: 28,\n  city: "北京"\n}\nputs user[:name]  # 张三\n\n# 遍历\nuser.each do |key, value|\n  puts "#{key}: #{value}"\nend\n\n# Hash 方法\nputs user.keys.inspect    # [:name, :age, :city]\nputs user.values.inspect  # ["张三", 28, "北京"]\nputs user.key?(:name)     # true\nputs user.fetch(:phone, "无")  # 无（默认值）\n\n# 合并\nother = { phone: "13800138000" }\nmerged = user.merge(other)\nputs merged\n\n# Symbol 特点\nputs :name.class          # Symbol\nputs "name".to_sym        # :name\nputs :name.to_s           # "name"',
            'line_by_line': '[{"代码":"{ key: value }","说明":"Symbol键的Hash简写语法"},{"代码":"hash[:key]","说明":"通过Symbol键访问值"},{"代码":"hash.each do |k, v|","说明":"遍历Hash"},{"代码":"hash.merge(other)","说明":"合并两个Hash"},{"代码":":symbol","说明":"Symbol是不可变的标识符，比字符串高效"}]',
            'syntax_note': 'Symbol 是不可变、可重用的标识符，比字符串内存效率高\\nRuby 3+ 支持 {key: value} 语法\\nHash#fetch 比直接 [] 更安全（可设默认值）',
            'runnable_example': '# 统计单词出现次数\\ntext = "apple banana apple orange banana apple"\\ncount = Hash.new(0)\\ntext.split.each { |word| count[word] += 1 }\\nputs count  # {"apple"=>3, "banana"=>2, "orange"=>1}',
            'common_errors': '[]',
            'aliases': 'Hash,字典,Symbol,哈希',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Ruby +{len(items)}')

# ============ Auto.js（6条，新分类） ============
# 检查是否有 Auto.js 分类，没有则创建
auto_cat = find_cat('编程语言', 'Auto.js')
if not auto_cat:
    # 找到编程语言分类的ID
    for root in db.get_categories(parent_id=None):
        if root['name'] == '编程语言':
            parent_id = root['id']
            # 获取最大sort_order
            children = db.get_categories(parent_id=parent_id)
            max_order = max((c.get('sort_order', 0) for c in children), default=0)
            auto_cat = db.add_category('Auto.js', parent_id, 'code', max_order + 1)
            print(f'[OK] 创建 Auto.js 分类 (id={auto_cat})')
            break

if auto_cat:
    items = [
        {
            'title': 'click 点击与 toast 提示',
            'language': 'Auto.js', 'version': '>=4.0',
            'code_block': '// 点击坐标\nclick(500, 800);\n\n// 点击文本（自动找按钮）\nclick("开始");\nclick("确定");\ntext("提交").findOne().click();\n\n// 等待控件出现再点击\nvar btn = textContains("同意").findOne(2000);  // 等2秒\nif (btn) {\n    btn.click();\n}\n\n// Toast 提示\ntoast("脚本开始执行");\ntoastLog("这条也会出现在日志");\n\n// 长按\nlongClick(500, 800);\n\n// 等待\nsleep(1000);  // 毫秒\n\n// 查找多个\nvar allButtons = className("android.widget.Button").find();\nfor (var i = 0; i < allButtons.length; i++) {\n    toast(allButtons[i].text());\n}',
            'line_by_line': '[{"代码":"click(x, y)","说明":"点击屏幕指定坐标"},{"代码":"click(\\"文本\\")","说明":"点击包含指定文本的控件"},{"代码":"text(\\"...\\").findOne()","说明":"查找并返回匹配的控件"},{"代码":"toast(\\"...\\")","说明":"弹出短提示"},{"代码":"sleep(ms)","说明":"等待指定毫秒数"},{"代码":"longClick(x, y)","说明":"长按指定位置"}]',
            'syntax_note': 'findOne() 默认等待直到找到控件\\nfindOne(timeout) 最多等待timeout毫秒\\nfind() 返回所有匹配的控件集合',
            'runnable_example': '// 自动签到脚本\\nlaunchApp("目标应用");\\nsleep(3000);\\nvar signBtn = textContains("签到").findOne(5000);\\nif (signBtn) {\\n    signBtn.click();\\n    toast("签到成功");\\n} else {\\n    toast("未找到签到按钮");\\n}',
            'common_errors': '[]',
            'aliases': 'click,点击,toast,控件操作',
        },
        {
            'title': 'swipe 滑动操作',
            'language': 'Auto.js', 'version': '>=4.0',
            'code_block': '// 从(x1,y1)滑动到(x2,y2)，耗时200ms\nswipe(500, 1500, 500, 500, 200);\n\n// 上滑（滚动列表）\nfunction swipeUp() {\n    var w = device.width;\n    var h = device.height;\n    swipe(w / 2, h * 0.7, w / 2, h * 0.3, 300);\n}\n\n// 下滑\nfunction swipeDown() {\n    var w = device.width;\n    var h = device.height;\n    swipe(w / 2, h * 0.3, w / 2, h * 0.7, 300);\n}\n\n// 左滑\nfunction swipeLeft() {\n    var w = device.width;\n    var h = device.height;\n    swipe(w * 0.8, h / 2, w * 0.2, h / 2, 300);\n}\n\n// 控件滑动\nvar list = className("android.widget.ListView").findOne();\nif (list) {\n    list.scrollForward();  // 向下滚动\n    sleep(500);\n    list.scrollBackward();  // 向上滚动\n}\n\n// 手势（多点滑动）\ngesture(1000, [100, 500], [200, 500], [300, 300], [400, 200]);',
            'line_by_line': '[{"代码":"swipe(x1, y1, x2, y2, duration)","说明":"从点1滑动到点2"},{"代码":"device.width / height","说明":"获取屏幕尺寸"},{"代码":"list.scrollForward()","说明":"控件向前滚动"},{"代码":"gesture(duration, points...)","说明":"多点手势路径"}]',
            'syntax_note': 'swipe 的 duration 是毫秒\\ngesture 可以画曲线路径\\nscrollForward/scrollBackward 只在支持滚动的控件上有效',
            'runnable_example': '// 在抖音中连滑3次\\nfunction swipeUp() {\\n    var w = device.width, h = device.height;\\n    swipe(w/2, h*0.8, w/2, h*0.2, 500);\\n}\\nfor (var i = 0; i < 3; i++) {\\n    swipeUp();\\n    sleep(2000);\\n}\\ntoast("已滑动3次");',
            'common_errors': '[]',
            'aliases': 'swipe,滑动,手势,滚动',
        },
    ]
    add_all(auto_cat, items)
    print(f'[OK] Auto.js +{len(items)}')

# ============ 总统计 ============
total = db.get_total_count()
snip = db.conn.execute("SELECT COUNT(*) FROM code_snippets").fetchone()[0]
print(f'\\n{"="*50}')
print(f'[OK] 代码片段总计: {snip}')
print(f'[OK] 数据库总计: {total}')
print(f'{"="*50}')
