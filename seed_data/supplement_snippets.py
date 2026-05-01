#!/usr/bin/env python3
"""补充代码片段种子数据：Java/C/C++/Go/C#/PHP/Ruby/Auto.js + 更多 Python/JS/Rust/Shell/HTML/CSS/Vue/React"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import DBManager

db = DBManager()
db.init_db()

def find_cat(parent_name, child_name):
    """通过父分类名+子分类名查找分类ID"""
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

total_before = db.conn.execute("SELECT COUNT(*) FROM code_snippets").fetchone()[0]

# ============ Java 补充（8条到10+） ============
cat = find_cat('编程语言', 'Java')
if cat:
    items = [
        {
            'title': '文件读取（BufferedReader）',
            'language': 'Java', 'version': '>=8',
            'code_block': 'import java.io.*;\n\npublic class ReadFile {\n    public static void main(String[] args) {\n        try (BufferedReader br = new BufferedReader(\n                new FileReader("data.txt"))) {\n            String line;\n            while ((line = br.readLine()) != null) {\n                System.out.println(line);\n            }\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n    }\n}',
            'line_by_line': '[{"代码":"BufferedReader br = new BufferedReader(new FileReader(...))","说明":"创建缓冲字符输入流读取文件"},{"代码":"br.readLine()","说明":"逐行读取，读到末尾返回null"},{"代码":"try-with-resources","说明":"自动关闭资源，无需显式调用close()"}]',
            'syntax_note': 'try-with-resources 自动关闭实现了 AutoCloseable 的资源\\nFileReader 默认使用系统编码，指定编码用 InputStreamReader\\nBufferedReader 比 FileReader 单独使用效率更高',
            'runnable_example': '// data.txt 内容\\n// 第一行\\n// 第二行\\nimport java.io.*;\\npublic class Main {\\n    public static void main(String[] args) throws Exception {\\n        try (BufferedReader br = new BufferedReader(new FileReader("data.txt"))) {\\n            br.lines().forEach(System.out::println);\\n        }\\n    }\\n}',
            'common_errors': '[{"报错":"FileNotFoundException","解决办法":"检查文件路径"},{"报错":"IOException","解决办法":"文件读取IO错误，检查文件权限"}]',
            'aliases': '文件读取,BufferedReader,文件IO',
        },
        {
            'title': '正则匹配 Pattern/Matcher',
            'language': 'Java', 'version': '>=8',
            'code_block': 'import java.util.regex.*;\n\npublic class RegexDemo {\n    public static void main(String[] args) {\n        String text = "我的邮箱是 zhangsan@example.com";\n        String pattern = "([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,})";\n\n        Pattern p = Pattern.compile(pattern);\n        Matcher m = p.matcher(text);\n\n        if (m.find()) {\n            System.out.println("完整邮箱: " + m.group(0));\n            System.out.println("用户名: " + m.group(1));\n            System.out.println("域名: " + m.group(2));\n        }\n\n        // 查找全部\n        String html = "<a>link1</a><a>link2</a>";\n        Matcher matcher = Pattern.compile("<a>(.*?)</a>").matcher(html);\n        while (matcher.find()) {\n            System.out.println("链接: " + matcher.group(1));\n        }\n    }\n}',
            'line_by_line': '[{"代码":"Pattern.compile(regex)","说明":"编译正则表达式为Pattern对象"},{"代码":"p.matcher(text)","说明":"创建Matcher对象，用于匹配文本"},{"代码":"m.find()","说明":"查找下一个匹配的子序列"},{"代码":"m.group(n)","说明":"获取第n个捕获组的内容"}]',
            'syntax_note': 'Pattern.compile() 可以传第二个参数如 Pattern.CASE_INSENSITIVE\\nMatcher 的 matches() 要求完全匹配，find() 是部分匹配\\n正则中的括号 () 是捕获组，从1开始编号',
            'runnable_example': 'import java.util.regex.*;\\npublic class Main {\\n    public static void main(String[] args) {\\n        String phone = "138-1234-5678";\\n        Pattern p = Pattern.compile("(\\\\d{3})-(\\\\d{4})-(\\\\d{4})");\\n        Matcher m = p.matcher(phone);\\n        if (m.matches()) {\\n            System.out.println("区号: " + m.group(1));\\n            System.out.println("号码: " + m.group(3));\\n        }\\n    }\\n}',
            'common_errors': '[{"报错":"PatternSyntaxException","解决办法":"正则语法错误，检查转义符"}]',
            'aliases': '正则匹配,Pattern,Matcher,regex',
        },
        {
            'title': '线程创建 Thread/Runnable',
            'language': 'Java', 'version': '>=8',
            'code_block': 'public class ThreadDemo {\n    public static void main(String[] args) {\n        // 方式1：继承Thread\n        class MyThread extends Thread {\n            public void run() {\n                System.out.println("线程: " + getName() + " 运行中");\n            }\n        }\n        new MyThread().start();\n\n        // 方式2：实现Runnable（推荐）\n        Runnable task = () -> {\n            System.out.println("Runnable线程运行中");\n        };\n        new Thread(task).start();\n\n        // 方式3：Lambda + Thread\n        new Thread(() -> {\n            for (int i = 0; i < 3; i++) {\n                System.out.println("Lambda线程: " + i);\n                try { Thread.sleep(500); } catch (Exception e) {}\n            }\n        }).start();\n\n        // 等待线程结束\n        Thread t = new Thread(() -> System.out.println("工作线程"));\n        t.start();\n        t.join();  // 等待t执行完毕\n        System.out.println("主线程继续");\n    }\n}',
            'line_by_line': '[{"代码":"extends Thread","说明":"继承Thread类并重写run()方法"},{"代码":"implements Runnable","说明":"实现Runnable接口，推荐方式（更灵活）"},{"代码":"new Thread(task).start()","说明":"创建线程并启动"},{"代码":"t.join()","说明":"等待线程t执行完毕"}]',
            'syntax_note': '实现Runnable接口比继承Thread更好（Java单继承限制）\\nLambda表达式可以简化Runnable的写法\\nstart() 启动线程，run() 直接调用不会创建新线程',
            'runnable_example': 'public class Main {\\n    public static void main(String[] args) throws Exception {\\n        Runnable countdown = () -> {\\n            try {\\n                for (int i = 3; i > 0; i--) {\\n                    System.out.println(i);\\n                    Thread.sleep(1000);\\n                }\\n            } catch (InterruptedException e) {}\\n        };\\n        Thread t = new Thread(countdown);\\n        t.start();\\n        t.join();\\n        System.out.println("Go!");\\n    }\\n}',
            'common_errors': '[]',
            'aliases': '线程,Thread,Runnable,多线程',
        },
        {
            'title': 'Stream API 操作集合',
            'language': 'Java', 'version': '>=8',
            'code_block': 'import java.util.*;\nimport java.util.stream.*;\n\npublic class StreamDemo {\n    public static void main(String[] args) {\n        List<String> names = Arrays.asList("张三", "李四", "王五", "赵六");\n\n        // filter 过滤\n        List<String> filtered = names.stream()\n            .filter(name -> name.startsWith("张"))\n            .collect(Collectors.toList());\n\n        // map 转换\n        List<Integer> lengths = names.stream()\n            .map(String::length)\n            .collect(Collectors.toList());\n\n        // sorted 排序\n        List<String> sorted = names.stream()\n            .sorted()\n            .collect(Collectors.toList());\n\n        // 统计\n        long count = names.stream()\n            .filter(n -> n.length() == 2)\n            .count();\n\n        // 收集为Map\n        Map<String, Integer> map = names.stream()\n            .collect(Collectors.toMap(n -> n, String::length));\n\n        // 链式操作\n        List<String> result = names.stream()\n            .filter(n -> n.length() > 1)\n            .sorted(Comparator.comparingInt(String::length))\n            .map(String::toUpperCase)\n            .collect(Collectors.toList());\n    }\n}',
            'line_by_line': '[{"代码":".stream()","说明":"将集合转为Stream流"},{"代码":"filter(predicate)","说明":"过滤，保留符合条件的元素"},{"代码":"map(function)","说明":"转换，每个元素应用函数"},{"代码":"sorted()","说明":"排序"},{"代码":"collect(Collectors.toList())","说明":"将Stream收集为List"},{"代码":"count()","说明":"计数"}]',
            'syntax_note': 'Stream 不会修改原集合，返回新集合\\nStream 操作分中间操作（lazy）和终端操作（eager）\\n终端操作执行后Stream就消耗了，不能重复使用',
            'runnable_example': 'import java.util.*;\\nimport java.util.stream.*;\\n\\npublic class Main {\\n    public static void main(String[] args) {\\n        List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5, 6);\\n        double avg = nums.stream()\\n            .filter(n -> n % 2 == 0)\\n            .mapToInt(Integer::intValue)\\n            .average()\\n            .orElse(0);\\n        System.out.println("偶数平均: " + avg);  // 4.0\\n    }\\n}',
            'common_errors': '[{"报错":"stream has already been operated upon or closed","解决办法":"每个Stream只能用一次，需要重新创建"}]',
            'aliases': 'Stream流,函数式编程,集合操作',
        },
        {
            'title': 'Optional 避免空指针',
            'language': 'Java', 'version': '>=8',
            'code_block': 'import java.util.Optional;\n\npublic class OptionalDemo {\n    public static void main(String[] args) {\n        // 创建Optional\n        Optional<String> empty = Optional.empty();\n        Optional<String> present = Optional.of("Hello");\n        Optional<String> nullable = Optional.ofNullable(mightBeNull());\n\n        // 安全取值\n        String val = present.orElse("默认值");\n        String val2 = present.orElseGet(() -> computeDefault());\n        String val3 = present.orElseThrow(() -> new RuntimeException("值不存在"));\n\n        // 判断\n        if (present.isPresent()) {\n            System.out.println(present.get());\n        }\n\n        // ifPresent\n        present.ifPresent(v -> System.out.println("值: " + v));\n        \n        // 链式操作\n        String result = nullable\n            .map(String::toUpperCase)\n            .filter(s -> s.length() > 3)\n            .orElse("默认");\n    }\n\n    static String mightBeNull() {\n        return Math.random() > 0.5 ? "随机值" : null;\n    }\n}',
            'line_by_line': '[{"代码":"Optional.of(value)","说明":"创建包含非空值的Optional"},{"代码":"Optional.ofNullable(value)","说明":"创建可能为null的Optional"},{"代码":".orElse(default)","说明":"值为空时返回默认值"},{"代码":".orElseGet(supplier)","说明":"值为空时调用函数生成默认值（惰性）"},{"代码":".map(function)","说明":"值存在时应用转换函数"},{"代码":".ifPresent(consumer)","说明":"值存在时执行操作"}]',
            'syntax_note': 'Optional.of() 参数不能为 null，会抛 NPE\\nOptional 主要是返回值类型，不推荐作为参数或字段\\norElse 和 orElseGet 区别：orElse 无论值是否存在都会计算默认值',
            'runnable_example': 'import java.util.*;\\n\\npublic class Main {\\n    public static Optional<String> findUser(int id) {\\n        Map<Integer, String> users = Map.of(1, "张三", 2, "李四");\\n        return Optional.ofNullable(users.get(id));\\n    }\\n    \\n    public static void main(String[] args) {\\n        String name = findUser(3)\\n            .orElse("未知用户");\\n        System.out.println(name);  // 未知用户\\n    }\\n}',
            'common_errors': '[{"报错":"NoSuchElementException: No value present","解决办法":"调用get()前需检查isPresent()，用orElse替代"}]',
            'aliases': 'Optional,空指针,空值处理',
        },
        {
            'title': 'Lambda 表达式',
            'language': 'Java', 'version': '>=8',
            'code_block': 'import java.util.*;\nimport java.util.function.*;\n\npublic class LambdaDemo {\n    public static void main(String[] args) {\n        // 1. 无参，无返回值\n        Runnable r1 = () -> System.out.println("Hello");\n\n        // 2. 单参，可省略括号\n        Consumer<String> c1 = s -> System.out.println(s);\n        c1.accept("测试");\n\n        // 3. 多参，有返回值\n        Comparator<Integer> comp = (a, b) -> a - b;\n\n        // 4. 多行，需要花括号和return\n        Function<String, Integer> f1 = (s) -> {\n            int len = s.length();\n            return len * 2;\n        };\n\n        // 5. 方法引用\n        List<String> names = Arrays.asList("张三", "李四");\n        names.forEach(System.out::println);  // 方法引用\n        names.sort(String::compareTo);        // 静态方法引用\n\n        // 6. 实际应用：排序\n        List<Integer> nums = Arrays.asList(3, 1, 4, 1, 5);\n        nums.sort((a, b) -> b - a);  // 降序\n        System.out.println(nums);\n    }\n}',
            'line_by_line': '[{"代码":"() -> System.out.println(...)","说明":"Lambda基础语法：参数 -> 表达式"},{"代码":"s -> s.length()","说明":"单参数可省略括号"},{"代码":"(a, b) -> a - b","说明":"多参数必须加括号"},{"代码":"System.out::println","说明":"方法引用：类名::方法名"}]',
            'syntax_note': 'Lambda 表达式可以赋值给函数式接口（只有一个抽象方法的接口）\\n常用的函数式接口：Runnable, Consumer, Function, Predicate, Supplier\\n方法引用是Lambda的语法糖，更简洁',
            'runnable_example': 'import java.util.*;\\n\\npublic class Main {\\n    public static void main(String[] args) {\\n        List<String> words = Arrays.asList("java", "python", "rust", "c");\\n        // 按长度升序\\n        words.sort((a, b) -> a.length() - b.length());\\n        System.out.println(words);  // [c, java, rust, python]\\n    }\\n}',
            'common_errors': '[]',
            'aliases': 'Lambda,函数式接口,方法引用',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Java +{len(items)}')

# ============ C 语言补充（8条到10+） ============
cat = find_cat('编程语言', 'C语言')
if cat:
    items = [
        {
            'title': '动态内存分配 malloc/free',
            'language': 'C', 'version': 'C99+',
            'code_block': '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    // 分配可以存5个int的连续内存\n    int *arr = (int*)malloc(5 * sizeof(int));\n    if (arr == NULL) {\n        printf("内存分配失败！\\n");\n        return 1;\n    }\n\n    // 使用\n    for (int i = 0; i < 5; i++) {\n        arr[i] = i * 10;\n    }\n\n    // 打印\n    for (int i = 0; i < 5; i++) {\n        printf("arr[%d] = %d\\n", i, arr[i]);\n    }\n\n    // 释放\n    free(arr);\n    arr = NULL;  // 避免野指针\n\n    // realloc：重新分配大小\n    arr = (int*)malloc(3 * sizeof(int));\n    int *temp = (int*)realloc(arr, 5 * sizeof(int));\n    if (temp != NULL) {\n        arr = temp;\n    }\n\n    free(arr);\n    return 0;\n}',
            'line_by_line': '[{"代码":"malloc(size)","说明":"分配指定字节数的内存，返回void*指针"},{"代码":"(int*)malloc(...)","说明":"将void*强制转为int*"},{"代码":"if (arr == NULL)","说明":"检查内存分配是否成功"},{"代码":"free(arr)","说明":"释放动态分配的内存"},{"代码":"arr = NULL","说明":"释放后将指针置NULL，防止悬空指针"},{"代码":"realloc(ptr, new_size)","说明":"重新调整内存大小，可能移动数据到新位置"}]',
            'syntax_note': 'malloc 分配的内存内容未初始化（可能含垃圾值）\\ncalloc 分配并初始化为0\\n每用一次 malloc 必须对应一次 free\\nfree 后要将指针置 NULL 防止野指针',
            'runnable_example': '#include <stdio.h>\\n#include <stdlib.h>\\n\\nint main() {\\n    int n;\\n    printf("输入数组大小: ");\\n    scanf("%d", &n);\\n    \\n    int *arr = (int*)calloc(n, sizeof(int));\\n    if (!arr) return 1;\\n    \\n    for (int i = 0; i < n; i++)\\n        arr[i] = i * i;\\n    \\n    for (int i = 0; i < n; i++)\\n        printf("%d ", arr[i]);\\n    printf("\\\\n");\\n    \\n    free(arr);\\n    return 0;\\n}',
            'common_errors': '[{"报错":"Segmentation fault","解决办法":"检查是否访问了已释放的内存"},{"报错":"Memory leak","解决办法":"检查malloc和free是否成对出现"}]',
            'aliases': 'malloc,free,动态内存,内存分配',
        },
        {
            'title': '结构体定义与使用',
            'language': 'C', 'version': 'C99+',
            'code_block': '#include <stdio.h>\n#include <string.h>\n\n// 定义结构体\nstruct Student {\n    char name[50];\n    int age;\n    float score;\n};\n\n// typedef 简化类型名\ntypedef struct {\n    int x;\n    int y;\n} Point;\n\nint main() {\n    // 声明并初始化\n    struct Student s1 = {"张三", 20, 85.5};\n    printf("姓名: %s, 年龄: %d, 分数: %.1f\\n", s1.name, s1.age, s1.score);\n\n    // 逐个赋值\n    struct Student s2;\n    strcpy(s2.name, "李四");\n    s2.age = 22;\n    s2.score = 90.0;\n\n    // 结构体指针\n    struct Student *p = &s1;\n    printf("指针访问: %s\\n", p->name);  // 使用 ->\n\n    // typedef 结构体\n    Point pt = {10, 20};\n    printf("Point: (%d, %d)\\n", pt.x, pt.y);\n\n    // 结构体数组\n    struct Student class[3] = {\n        {"王五", 19, 78.0},\n        {"赵六", 21, 92.5},\n        {"钱七", 20, 88.0}\n    };\n    for (int i = 0; i < 3; i++) {\n        printf("%s: %.1f\\n", class[i].name, class[i].score);\n    }\n\n    return 0;\n}',
            'line_by_line': '[{"代码":"struct Student { ... }","说明":"定义结构体类型"},{"代码":"typedef struct { ... } Point","说明":"typedef为结构体起别名，使用时可省略struct关键字"},{"代码":"s1.name, s1.age","说明":"点运算符访问结构体成员"},{"代码":"p->name","说明":"箭头运算符通过指针访问结构体成员"}]',
            'syntax_note': '结构体变量做参数默认是值传递（整个复制），大数据用指针\\n字符串数组不能直接赋值，用 strcpy\\n匿名结构体（typedef的）不能自引用（链表等需要名字）',
            'runnable_example': '#include <stdio.h>\\n\\ntypedef struct {\\n    int hour, minute, second;\\n} Time;\\n\\nvoid print_time(Time t) {\\n    printf("%02d:%02d:%02d\\\\n", t.hour, t.minute, t.second);\\n}\\n\\nint main() {\\n    Time now = {14, 30, 0};\\n    print_time(now);  // 14:30:00\\n    return 0;\\n}',
            'common_errors': '[]',
            'aliases': '结构体,struct,typedef',
        },
        {
            'title': '文件读写 fopen/fclose',
            'language': 'C', 'version': 'C99+',
            'code_block': '#include <stdio.h>\n\nint main() {\n    // 写入文件\n    FILE *fp = fopen("output.txt", "w");\n    if (fp == NULL) {\n        printf("无法打开文件！\\n");\n        return 1;\n    }\n    fprintf(fp, "Hello, World!\\n");\n    fprintf(fp, "这是第二行\\n");\n    fclose(fp);\n\n    // 读取文件\n    fp = fopen("output.txt", "r");\n    if (fp == NULL) {\n        printf("文件不存在！\\n");\n        return 1;\n    }\n    char buffer[256];\n    while (fgets(buffer, sizeof(buffer), fp) != NULL) {\n        printf("读取: %s", buffer);\n    }\n    fclose(fp);\n\n    // 追加模式\n    fp = fopen("output.txt", "a");\n    fprintf(fp, "追加一行\\n");\n    fclose(fp);\n\n    // 二进制读写\n    int data[] = {1, 2, 3, 4, 5};\n    fp = fopen("data.bin", "wb");\n    fwrite(data, sizeof(int), 5, fp);\n    fclose(fp);\n\n    return 0;\n}',
            'line_by_line': '[{"代码":"FILE *fp = fopen(路径, 模式)","说明":"打开文件，模式：r=读 w=写 a=追加 b=二进制"},{"代码":"fprintf(fp, 格式, ...)","说明":"格式化写入文件"},{"代码":"fgets(buf, size, fp)","说明":"从文件读取一行"},{"代码":"fclose(fp)","说明":"关闭文件"},{"代码":"fwrite(data, size, count, fp)","说明":"二进制写入数据块"}]',
            'syntax_note': '始终检查 fopen 返回是否为 NULL\\nfclose 后指针悬空，不要再使用\\nr+ 读写模式不会清空文件，w+ 会清空\\n二进制模式下不会做换行符转换',
            'runnable_example': '#include <stdio.h>\\n\\nint main() {\\n    // 复制文件\\n    FILE *src = fopen("source.txt", "r");\\n    FILE *dst = fopen("dest.txt", "w");\\n    if (!src || !dst) {\\n        printf("文件打开失败\\\\n");\\n        return 1;\\n    }\\n    char c;\\n    while ((c = fgetc(src)) != EOF) {\\n        fputc(c, dst);\\n    }\\n    fclose(src);\\n    fclose(dst);\\n    printf("复制完成\\\\n");\\n    return 0;\\n}',
            'common_errors': '[{"报错":"Segmentation fault","解决办法":"检查文件指针是否为NULL"},{"报错":"Permission denied","解决办法":"检查文件是否被其他程序占用"}]',
            'aliases': '文件读写,fopen,fclose,fprintf',
        },
    ]
    add_all(cat, items)
    print(f'[OK] C +{len(items)}')

# ============ C++ 补充（10条） ============
cat = find_cat('编程语言', 'C++')
if cat:
    items = [
        {
            'title': 'cout/cin 输入输出',
            'language': 'C++', 'version': 'C++11+',
            'code_block': '#include <iostream>\n#include <string>\n\nint main() {\n    // 输出\n    std::cout << "Hello, World!" << std::endl;\n    \n    int age = 25;\n    double pi = 3.14159;\n    std::cout << "年龄: " << age << ", 圆周率: " << pi << std::endl;\n\n    // 输入\n    std::string name;\n    std::cout << "请输入姓名: ";\n    std::getline(std::cin, name);\n\n    int score;\n    std::cout << "请输入分数: ";\n    std::cin >> score;\n\n    std::cout << name << " 的分数是 " << score << std::endl;\n\n    // 格式化\n    std::cout.precision(4);\n    std::cout << "pi = " << pi << std::endl;  // 3.142\n\n    return 0;\n}',
            'line_by_line': '[{"代码":"#include <iostream>","说明":"包含输入输出流头文件"},{"代码":"std::cout << ...","说明":"标准输出流，<<是插入运算符"},{"代码":"std::cin >> var","说明":"标准输入流，>>是提取运算符"},{"代码":"std::endl","说明":"换行并刷新缓冲区"},{"代码":"std::getline(cin, str)","说明":"读取一行字符串（包含空格）"}]',
            'syntax_note': 'using namespace std; 可以省略 std:: 前缀，但大型项目不推荐\\ncin >> 遇到空格会停止，想读含空格的字符串用 getline\\nendl 和 \\\\n 的区别：endl 会强制刷新缓冲区',
            'runnable_example': '#include <iostream>\\nusing namespace std;\\n\\nint main() {\\n    int a, b;\\n    cout << "输入两个整数: ";\\n    cin >> a >> b;\\n    cout << a << " + " << b << " = " << a + b << endl;\\n    return 0;\\n}',
            'common_errors': '[]',
            'aliases': 'cout,cin,输入输出,iostream',
        },
        {
            'title': 'vector 动态数组',
            'language': 'C++', 'version': 'C++11+',
            'code_block': '#include <iostream>\n#include <vector>\n#include <algorithm>\n\nint main() {\n    // 创建vector\n    std::vector<int> nums = {3, 1, 4, 1, 5};\n    \n    // 添加元素\n    nums.push_back(9);\n    nums.push_back(2);\n    \n    // 访问\n    std::cout << "第一个: " << nums[0] << std::endl;\n    std::cout << "最后一个: " << nums.back() << std::endl;\n    \n    // 遍历方式1: 索引\n    for (size_t i = 0; i < nums.size(); i++) {\n        std::cout << nums[i] << " ";\n    }\n    std::cout << std::endl;\n    \n    // 遍历方式2: 范围for (推荐)\n    for (int n : nums) {\n        std::cout << n << " ";\n    }\n    std::cout << std::endl;\n    \n    // 算法\n    std::sort(nums.begin(), nums.end());\n    auto it = std::find(nums.begin(), nums.end(), 4);\n    if (it != nums.end()) {\n        std::cout << "找到4在位置: " << (it - nums.begin()) << std::endl;\n    }\n    \n    // 其他操作\n    std::cout << "大小: " << nums.size() << std::endl;\n    std::cout << "容量: " << nums.capacity() << std::endl;\n    nums.pop_back();  // 删除最后一个\n    nums.clear();      // 清空\n    std::cout << "是否为空: " << (nums.empty() ? "是" : "否") << std::endl;\n    \n    return 0;\n}',
            'line_by_line': '[{"代码":"#include <vector>","说明":"包含vector头文件"},{"代码":"vector<int> nums = {...}","说明":"创建并初始化int类型的vector"},{"代码":"push_back(val)","说明":"在末尾添加元素"},{"代码":"nums[i]","说明":"索引访问"},{"代码":"sort(begin, end)","说明":"排序（需#include <algorithm>）"},{"代码":"find(begin, end, val)","说明":"查找元素，返回迭代器"}]',
            'syntax_note': 'vector 自动管理内存，动态增长\\n访问越界不会报错（未定义行为），用 at() 会做边界检查\\nsize() 返回元素个数，capacity() 返回容量',
            'runnable_example': '#include <iostream>\\n#include <vector>\\nusing namespace std;\\n\\nint main() {\\n    vector<int> scores = {85, 92, 78, 90};\\n    int sum = 0;\\n    for (int s : scores) sum += s;\\n    double avg = (double)sum / scores.size();\\n    cout << "平均分: " << avg << endl;  // 86.25\\n    return 0;\\n}',
            'common_errors': '[]',
            'aliases': 'vector,动态数组,STL容器',
        },
        {
            'title': 'string 字符串操作',
            'language': 'C++', 'version': 'C++11+',
            'code_block': '#include <iostream>\n#include <string>\n\nint main() {\n    // 创建\n    std::string s1 = "Hello";\n    std::string s2("World");\n    \n    // 拼接\n    std::string s3 = s1 + " " + s2;\n    std::cout << s3 << std::endl;  // Hello World\n    \n    // 长度\n    std::cout << "长度: " << s3.length() << std::endl;\n    \n    // 访问字符\n    std::cout << "第一个: " << s3[0] << std::endl;\n    std::cout << "最后一个: " << s3.back() << std::endl;\n    \n    // 查找\n    size_t pos = s3.find("World");\n    if (pos != std::string::npos) {\n        std::cout << "World 在位置: " << pos << std::endl;\n    }\n    \n    // 子串\n    std::string sub = s3.substr(6, 5);\n    std::cout << "子串: " << sub << std::endl;  // World\n    \n    // 插入\n    s3.insert(5, " lovely");\n    std::cout << s3 << std::endl;  // Hello lovely World\n    \n    // 替换\n    s3.replace(6, 5, "beautiful");\n    std::cout << s3 << std::endl;  // Hello beautiful World\n    \n    // C风格字符串\n    const char *cstr = s3.c_str();\n    printf("C风格: %s\\n", cstr);\n    \n    return 0;\n}',
            'line_by_line': '[{"代码":"string s1 = \\"Hello\\"","说明":"创建字符串"},{"代码":"s1 + \\" \\" + s2","说明":"字符串拼接（+运算符重载）"},{"代码":"s.length() / s.size()","说明":"获取字符串长度"},{"代码":"s.find(sub)","说明":"查找子串，返回位置，找不到返回npos"},{"代码":"s.substr(pos, len)","说明":"提取子串"},{"代码":"s.c_str()","说明":"转为C风格的const char*"}]',
            'syntax_note': 'string 是类类型，不是基本类型\\nsize() 和 length() 等价\\nfind 返回 size_t 类型，判断用 != string::npos\\nc_str() 返回的指针在 string 修改后可能失效',
            'runnable_example': '#include <iostream>\\n#include <string>\\nusing namespace std;\\n\\nint main() {\\n    string email = "user@example.com";\\n    size_t at = email.find("@");\\n    if (at != string::npos) {\\n        string name = email.substr(0, at);\\n        string domain = email.substr(at + 1);\\n        cout << "用户名: " << name << endl;\\n        cout << "域名: " << domain << endl;\\n    }\\n    return 0;\\n}',
            'common_errors': '[]',
            'aliases': 'string,字符串,std::string',
        },
    ]
    add_all(cat, items)
    print(f'[OK] C++ +{len(items)}')

# ============ Go 补充（10条） ============
cat = find_cat('编程语言', 'Go')
if cat:
    items = [
        {
            'title': 'Hello World',
            'language': 'Go', 'version': '>=1.0',
            'code_block': 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
            'line_by_line': '[{"代码":"package main","说明":"每个Go文件属于一个包，main包是可执行程序"},{"代码":"import \\"fmt\\"","说明":"导入标准库fmt（格式化输入输出）"},{"代码":"func main()","说明":"程序入口函数"},{"代码":"fmt.Println(...)","说明":"打印一行到控制台"}]',
            'syntax_note': 'Go 不需要分号结尾\\n左花括号必须与函数名同行\\nmain 包必须包含 main() 函数才能生成可执行文件',
            'runnable_example': '// 编译: go build hello.go\\n// 运行: ./hello\\npackage main\\nimport "fmt"\\nfunc main() {\\n    name := "Go语言"\\n    fmt.Printf("你好, %s!\\\\n", name)\\n}',
            'common_errors': '[]',
            'aliases': 'Hello World,Go入门,main函数',
        },
        {
            'title': 'goroutine 并发',
            'language': 'Go', 'version': '>=1.0',
            'code_block': 'package main\n\nimport (\n    "fmt"\n    "time"\n)\n\nfunc worker(id int, jobs <-chan int, results chan<- int) {\n    for job := range jobs {\n        fmt.Printf("工人%d 开始任务%d\\n", id, job)\n        time.Sleep(time.Second)\n        fmt.Printf("工人%d 完成任务%d\\n", id, job)\n        results <- job * 2\n    }\n}\n\nfunc main() {\n    const numJobs = 5\n    jobs := make(chan int, numJobs)\n    results := make(chan int, numJobs)\n\n    // 启动3个worker\n    for w := 1; w <= 3; w++ {\n        go worker(w, jobs, results)\n    }\n\n    // 发送任务\n    for j := 1; j <= numJobs; j++ {\n        jobs <- j\n    }\n    close(jobs)\n\n    // 收集结果\n    for r := 1; r <= numJobs; r++ {\n        <-results\n    }\n\n    fmt.Println("所有任务完成!")\n}',
            'line_by_line': '[{"代码":"go worker(...)","说明":"go关键字启动goroutine（轻量级线程）"},{"代码":"make(chan int)","说明":"创建channel用于goroutine间通信"},{"代码":"jobs <-chan int","说明":"只读channel（接收）"},{"代码":"results chan<- int","说明":"只写channel（发送）"},{"代码":"close(jobs)","说明":"关闭channel，通知接收方不再有数据"},{"代码":"<-results","说明":"从channel接收数据（阻塞直到有数据）"}]',
            'syntax_note': 'goroutine 比线程轻量得多（栈初始2KB）\\nchannel 默认无缓冲（同步），带缓冲的 make(chan T, n)\\n不要通过共享内存通信，通过通信共享内存',
            'runnable_example': 'package main\\nimport "fmt"\\n\\nfunc main() {\\n    ch := make(chan string)\\n    \\n    go func() {\\n        ch <- "来自goroutine的消息"\\n    }()\\n    \\n    msg := <-ch\\n    fmt.Println(msg)\\n}',
            'common_errors': '[{"报错":"fatal error: all goroutines are asleep - deadlock","解决办法":"检查channel读写是否匹配，防止死锁"}]',
            'aliases': 'goroutine,channel,并发,协程',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Go +{len(items)}')

# ============ Shell 补充（8条） ============
cat = find_cat('编程语言', 'Shell脚本')
if cat:
    items = [
        {
            'title': 'case 分支语句',
            'language': 'Shell', 'version': 'Bash 4+',
            'code_block': '#!/bin/bash\n\necho "请选择操作:"\necho "1) 查看日期"\necho "2) 查看当前目录"\necho "3) 查看系统信息"\nread -p "请输入选项 [1-3]: " choice\n\ncase $choice in\n    1)\n        echo "当前日期: $(date)"\n        ;;\n    2)\n        echo "当前目录: $(pwd)"\n        ls -la\n        ;;\n    3)\n        echo "系统信息:"\n        uname -a\n        echo "CPU: $(nproc)核"\n        echo "内存: $(free -h | grep Mem | awk \'{print $2}\')"\n        ;;\n    *)\n        echo "无效选项！"\n        ;;\nesac',
            'line_by_line': '[{"代码":"case $var in","说明":"case分支开始，匹配变量值"},{"代码":"模式)","说明":"匹配模式，支持通配符"},{"代码":";;","说明":"每个分支结束标志"},{"代码":"*)","说明":"默认分支，匹配所有未匹配的情况"},{"代码":"esac","说明":"case结束（case倒写）"}]',
            'syntax_note': '每个分支必须以 ;; 结尾\\n模式支持通配符：*) 是默认 \\ncase 比多个 if-elif 更清晰',
            'runnable_example': '#!/bin/bash\\nread -p "输入文件名: " file\\ncase $file in\\n    *.txt) echo "文本文件" ;;&nbsp\\n    *.jpg|*.png) echo "图片文件" ;;&nbsp\\n    *.sh) echo "Shell脚本" ;;&nbsp\\n    *) echo "未知类型" ;;&nbsp\\nesac',
            'common_errors': '[]',
            'aliases': 'case分支,switch,条件分支',
        },
        {
            'title': 'for/while 循环',
            'language': 'Shell', 'version': 'Bash 4+',
            'code_block': '#!/bin/bash\n\n# for循环1: 遍历列表\nfor fruit in 苹果 香蕉 橙子; do\n    echo "水果: $fruit"\ndone\n\n# for循环2: 数字范围\nfor i in {1..5}; do\n    echo "数字: $i"\ndone\n\n# for循环3: C风格\nfor ((i=0; i<3; i++)); do\n    echo "C风格: $i"\ndone\n\n# for循环4: 遍历文件\nfor file in *.txt; do\n    if [ -f "$file" ]; then\n        echo "文本文件: $file"\n    fi\ndone\n\n# while循环\ncount=0\nwhile [ $count -lt 3 ]; do\n    echo "count = $count"\n    ((count++))\ndone\n\n# until循环（条件为假时执行）\nnum=0\nuntil [ $num -ge 3 ]; do\n    echo "num = $num"\n    ((num++))\ndone',
            'line_by_line': '[{"代码":"for var in list; do...done","说明":"遍历列表"},{"代码":"for ((init; cond; inc))","说明":"C风格的for循环"},{"代码":"while [ cond ]; do...done","说明":"条件为真时循环"},{"代码":"until [ cond ]; do...done","说明":"条件为假时循环"},{"代码":"((count++))","说明":"算术运算，类似C语法"},{"代码":"{1..5}","说明":"花括号展开生成1到5的序列"}]',
            'syntax_note': 'for 循环遍历文件时，最好加 [ -f ] 判断是否真找到文件\\n((...)) 是算术运算，不需要 $ 前缀\\n{1..10..2} 生成1 3 5 7 9（步长2）',
            'runnable_example': '#!/bin/bash\\n# 批量重命名.txt为.bak\\nfor file in *.txt; do\\n    if [ -f "$file" ]; then\\n        mv "$file" "${file%.txt}.bak"\\n        echo "重命名: $file -> ${file%.txt}.bak"\\n    fi\\ndone',
            'common_errors': '[]',
            'aliases': 'for循环,while循环,循环',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Shell +{len(items)}')

# ============ 更多 Python（10条） ============
cat = find_cat('编程语言', 'Python')
if cat:
    items = [
        {
            'title': 'os.walk 遍历目录树',
            'language': 'Python', 'version': '>=3.0',
            'code_block': 'import os\n\nroot_dir = "."\nfor dirpath, dirnames, filenames in os.walk(root_dir):\n    # 当前目录路径\n    print(f"目录: {dirpath}")\n    \n    # 子目录列表\n    for d in dirnames:\n        print(f"  子目录: {d}")\n    \n    # 文件列表\n    for f in filenames:\n        full_path = os.path.join(dirpath, f)\n        size = os.path.getsize(full_path)\n        print(f"  文件: {f} ({size} bytes)")\n\n# 统计文件类型\nextensions = {}\nfor dirpath, _, filenames in os.walk("."):\n    for f in filenames:\n        ext = os.path.splitext(f)[1]\n        extensions[ext] = extensions.get(ext, 0) + 1\n\nprint(f"\\n文件类型统计: {extensions}")',
            'line_by_line': '[{"代码":"os.walk(root)","说明":"生成器，遍历目录树，每次返回(dirpath, dirnames, filenames)"},{"代码":"dirpath","说明":"当前遍历到的目录路径"},{"代码":"dirnames","说明":"当前目录下的子目录名列表"},{"代码":"filenames","说明":"当前目录下的文件名列表"}]',
            'syntax_note': 'os.walk 默认深度优先遍历\\n修改 dirnames 列表（如 del dirnames[:]）可控制遍历哪些子目录\\n大量文件时性能优于递归 os.listdir',
            'runnable_example': 'import os\\n# 找到所有大于1MB的文件\\nfor dirpath, _, files in os.walk("."):\\n    for f in files:\\n        path = os.path.join(dirpath, f)\\n        size = os.path.getsize(path)\\n        if size > 1024 * 1024:\\n            print(f"{path}: {size/1024/1024:.1f}MB")',
            'common_errors': '[]',
            'aliases': 'os.walk,遍历目录,文件遍历',
        },
        {
            'title': 'collections.Counter 计数',
            'language': 'Python', 'version': '>=3.0',
            'code_block': 'from collections import Counter\n\n# 统计单词出现次数\ntext = "apple banana apple orange banana apple"\nwords = text.split()\ncount = Counter(words)\nprint(count)  # Counter({"apple": 3, "banana": 2, "orange": 1})\n\n# 最常见的N个\nprint(count.most_common(2))  # [("apple", 3), ("banana", 2)]\n\n# 统计字符\ns = "hello world"\nchar_count = Counter(s)\nprint(char_count)  # Counter({"l": 3, "o": 2, "h": 1, ...})\n\n# 加减运算\nc1 = Counter(a=3, b=1)\nc2 = Counter(a=1, b=2)\nprint(c1 + c2)  # Counter({"a": 4, "b": 3})\nprint(c1 - c2)  # Counter({"a": 2})  (不会出现负数)\n\n# 统计列表\nnumbers = [1, 1, 2, 3, 2, 1, 4, 2]\nc = Counter(numbers)\nprint(c)  # Counter({1: 3, 2: 3, 3: 1, 4: 1})',
            'line_by_line': '[{"代码":"Counter(iterable)","说明":"创建计数器，统计可迭代对象中各元素出现次数"},{"代码":".most_common(n)","说明":"返回出现次数最多的n个元素"},{"代码":"c1 + c2","说明":"合并两个计数器"},{"代码":"c1 - c2","说明":"计数器相减（结果不出现负数）"}]',
            'syntax_note': 'Counter 是 dict 的子类，继承所有字典方法\\n访问不存在的键返回0而不是KeyError\\nelements() 方法返回所有元素的迭代器（按计数重复）',
            'runnable_example': 'from collections import Counter\\n# 找出列表中的奇数及其出现次数\\nnums = [1,2,3,2,1,3,3,4,5,5,5]\\nc = Counter(nums)\\nodds = {k: v for k, v in c.items() if k % 2 == 1}\\nprint(odds)  # {1: 2, 3: 3, 5: 3}',
            'common_errors': '[]',
            'aliases': 'Counter,计数,统计,collections',
        },
        {
            'title': 'glob 文件模式匹配',
            'language': 'Python', 'version': '>=3.0',
            'code_block': 'import glob\n\n# 查找所有txt文件\nfor file in glob.glob("*.txt"):\n    print(f"文本文件: {file}")\n\n# 递归查找所有py文件\npy_files = glob.glob("**/*.py", recursive=True)\nprint(f"找到 {len(py_files)} 个Python文件")\n\n# 查找特定模式\nimages = glob.glob("images/*.{jpg,png,gif}", recursive=True)\nprint(f"图片文件: {images}")\n\n# 忽略大小写匹配\nmatches = [f for f in glob.glob("[!.]*") if not f.startswith(".")]\nprint(f"非隐藏文件: {matches}")',
            'line_by_line': '[{"代码":"glob.glob(pattern)","说明":"查找匹配pattern的文件路径，返回列表"},{"代码":"**/*.py","说明":"**匹配任意级子目录（需recursive=True）"},{"代码":"*.{jpg,png}","说明":"花括号展开，匹配多个扩展名"},{"代码":"[!.]*","说明":"匹配不以点开头的文件（排除隐藏文件）"}]',
            'syntax_note': 'glob 使用Unix shell风格的通配符\\nrecursive=True 且用 ** 才能递归子目录\\nglob 不返回隐藏文件（点开头的），除非pattern匹配',
            'runnable_example': 'import glob\\n# 递归查找所有日志文件并统计大小\\nimport os\\ntotal = 0\\nfor f in glob.glob("**/*.log", recursive=True):\\n    size = os.path.getsize(f)\\n    total += size\\n    print(f"{f}: {size} bytes")\\nprint(f"总计: {total} bytes")',
            'common_errors': '[]',
            'aliases': 'glob,文件匹配,通配符,文件查找',
        },
        {
            'title': 'subprocess 运行系统命令',
            'language': 'Python', 'version': '>=3.0',
            'code_block': 'import subprocess\n\n# 运行命令并获取输出\nresult = subprocess.run(\n    ["ls", "-la"],\n    capture_output=True,\n    text=True\n)\nprint("返回码:", result.returncode)\nprint("标准输出:", result.stdout)\nprint("标准错误:", result.stderr)\n\n# 使用shell=True（不推荐，有注入风险）\n# result = subprocess.run("ls -la", shell=True, capture_output=True, text=True)\n\n# 实时输出\nprocess = subprocess.Popen(\n    ["ping", "-c", "4", "8.8.8.8"],\n    stdout=subprocess.PIPE,\n    text=True\n)\nfor line in process.stdout:\n    print(line, end="")\nprocess.wait()\n\n# 检查命令是否存在\nimport shutil\nif shutil.which("git"):\n    print("Git已安装")\n\n# 超时控制\ntry:\n    subprocess.run(["sleep", "10"], timeout=3, capture_output=True)\nexcept subprocess.TimeoutExpired:\n    print("命令超时")',
            'line_by_line': '[{"代码":"subprocess.run(cmd)","说明":"运行命令并等待完成，返回CompletedProcess"},{"代码":"capture_output=True","说明":"捕获标准输出和错误"},{"代码":"text=True","说明":"以文本模式返回（而非bytes）"},{"代码":"Popen(cmd, stdout=PIPE)","说明":"创建子进程，可实时读取输出"},{"代码":"shutil.which(cmd)","说明":"查找可执行文件路径"},{"代码":"timeout=N","说明":"设置超时秒数"}]',
            'syntax_note': '推荐传命令列表而非字符串（避免shell注入）\\ncapture_output 代替旧的 subprocess.check_output\\n大量输出时用 Popen + stdout=PIPE 实时读取',
            'runnable_example': 'import subprocess\\n# 检查磁盘使用情况\\nresult = subprocess.run(["df", "-h"], capture_output=True, text=True)\\nfor line in result.stdout.strip().split("\\\\n"):\\n    print(line)',
            'common_errors': '[{"报错":"FileNotFoundError","解决办法":"命令不存在，用 shutil.which 先检查"},{"报错":"TimeoutExpired","解决办法":"命令超时，增加timeout值"}]',
            'aliases': 'subprocess,运行命令,系统命令,进程',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Python +{len(items)}')

# ============ 更多 JavaScript（10条） ============
cat = find_cat('编程语言', 'JavaScript')
if cat:
    items = [
        {
            'title': 'Map 和 Set 数据结构',
            'language': 'JavaScript', 'version': 'ES6+',
            'code_block': '// Map: 键值对集合（键可以是任意类型）\nconst map = new Map();\n\nmap.set("name", "张三");\nmap.set(42, "数字键");\nmap.set({id: 1}, "对象键");\n\nconsole.log(map.get("name"));  // 张三\nconsole.log(map.has(42));      // true\nconsole.log(map.size);         // 3\n\nmap.delete(42);\n// map.clear();  // 清空\n\n// 遍历\nfor (const [key, value] of map) {\n    console.log(`${key}: ${value}`);\n}\n\n// Set: 不重复的值的集合\nconst set = new Set([1, 2, 3, 3, 4, 4, 5]);\nconsole.log(set);  // Set {1, 2, 3, 4, 5}\n\nset.add(6);\nconsole.log(set.has(3));  // true\nconsole.log(set.size);    // 6\n\n// 数组去重\nconst arr = [1, 2, 2, 3, 3, 3];\nconst unique = [...new Set(arr)];\nconsole.log(unique);  // [1, 2, 3]\n\n// 交集/并集/差集\nconst a = new Set([1, 2, 3]);\nconst b = new Set([3, 4, 5]);\nconst union = new Set([...a, ...b]);      // 并集\nconst intersect = new Set([...a].filter(x => b.has(x)));  // 交集\nconst diff = new Set([...a].filter(x => !b.has(x)));      // 差集',
            'line_by_line': '[{"代码":"new Map()","说明":"创建Map，键可以是任意类型（对象、数字等）"},{"代码":"map.set(k, v) / get(k)","说明":"设置和获取键值对"},{"代码":"new Set(arr)","说明":"创建Set，自动去重"},{"代码":"[...new Set(arr)]","说明":"数组去重的简写方式"}]',
            'syntax_note': 'Map 的键是有序的（按插入顺序）\\nNaN 在 Map 中可作为键\\nSet 的 === 比较，对象引用不同即使内容相同也不算重复',
            'runnable_example': '// 统计元素出现次数\\nconst items = ["a", "b", "a", "c", "b", "a"];\\nconst countMap = new Map();\\nitems.forEach(item => {\\n    countMap.set(item, (countMap.get(item) || 0) + 1);\\n});\\nconsole.log([...countMap.entries()]);\\n// [["a", 3], ["b", 2], ["c", 1]]',
            'common_errors': '[]',
            'aliases': 'Map,Set,集合,字典',
        },
        {
            'title': 'Generator 生成器函数',
            'language': 'JavaScript', 'version': 'ES6+',
            'code_block': '// 生成器函数定义\nfunction* fibonacci() {\n    let a = 0, b = 1;\n    while (true) {\n        yield a;\n        [a, b] = [b, a + b];\n    }\n}\n\n// 使用生成器\nconst fib = fibonacci();\nconsole.log(fib.next().value);  // 0\nconsole.log(fib.next().value);  // 1\nconsole.log(fib.next().value);  // 1\nconsole.log(fib.next().value);  // 2\nconsole.log(fib.next().value);  // 3\n\n// for-of 遍历（有限生成器）\nfunction* range(start, end) {\n    for (let i = start; i <= end; i++) {\n        yield i;\n    }\n}\n\nfor (const n of range(1, 5)) {\n    console.log(n);  // 1 2 3 4 5\n}\n\n// 生成器也可以接收值\nfunction* counter() {\n    let count = 0;\n    while (true) {\n        const reset = yield ++count;\n        if (reset) count = 0;\n    }\n}\n\nconst c = counter();\nconsole.log(c.next().value);      // 1\nconsole.log(c.next().value);      // 2\nconsole.log(c.next(true).value);  // 1 (重置)',
            'line_by_line': '[{"代码":"function* fn()","说明":"定义生成器函数，*表示这是一个生成器"},{"代码":"yield value","说明":"产出一个值，暂停函数执行"},{"代码":".next()","说明":"调用下一个yield，返回{value, done}"},{"代码":".next(arg)","说明":"向生成器传入值，作为上个yield的结果"}]',
            'syntax_note': '生成器返回的是迭代器对象\\nyield* 可以委托给另一个生成器\\n生成器无限循环时不能用 for-of（会无限遍历）',
            'runnable_example': '// 分页加载数据\\nfunction* paginate(url, pageSize = 10) {\\n    let page = 1;\\n    while (true) {\\n        yield fetch(`${url}?page=${page}&size=${pageSize}`)\\n            .then(r => r.json());\\n        page++;\\n    }\\n}\\n\\nconst pages = paginate("https://api.example.com/items");\\n// const page1 = await pages.next().value;\\n// const page2 = await pages.next().value;',
            'common_errors': '[]',
            'aliases': 'Generator,生成器,yield,迭代器',
        },
    ]
    add_all(cat, items)
    print(f'[OK] JavaScript +{len(items)}')

# ============ 更多 Rust（8条） ============
cat = find_cat('编程语言', 'Rust')
if cat:
    items = [
        {
            'title': 'String vs &str',
            'language': 'Rust', 'version': '>=1.0',
            'code_block': 'fn main() {\n    // &str: 字符串切片（不可变，固定大小）\n    let s1: &str = "hello";\n    \n    // String: 堆分配的字符串（可变，可增长）\n    let mut s2: String = String::from("hello");\n    \n    // &str -> String\n    let s3: String = s1.to_string();\n    let s4: String = "world".to_owned();\n    let s5: String = "example".into();\n    \n    // String -> &str\n    let s6: &str = &s2;\n    let s7: &str = s2.as_str();\n    \n    // 拼接\n    s2.push_str(" world");  // 追加字符串\n    s2.push(\'!\');            // 追加字符\n    let s8 = s1.to_string() + " " + &s2;\n    let s9 = format!("{} {}", s1, s2);\n    \n    // 切片\n    let slice = &s2[0..5];\n    println!("切片: {}", slice);\n    \n    // 遍历\n    for c in "你好".chars() {\n        println!("{}", c);\n    }\n    \n    // 字节遍历\n    for b in s2.bytes() {\n        println!("{}", b);\n    }\n}',
            'line_by_line': '[{"代码":"&str","说明":"字符串切片，不可变，固定大小，栈上"},{"代码":"String","说明":"堆分配的字符串，可变，可增长"},{"代码":".to_string()","说明":"从&str创建String"},{"代码":"push_str() / push()","说明":"追加字符串/字符"],{"代码":"format!()","说明":"格式化创建String"}]',
            'syntax_note': '&str 是胖指针（指针+长度）\\nString 是 Vec<u8> 的包装\\n字符串索引不是O(1)，因为UTF-8变长编码\\n用 chars() 遍历字符，bytes() 遍历字节',
            'runnable_example': 'fn main() {\\n    let greeting = String::from("你好世界");\\n    println!("长度: {} 字节", greeting.len());  // 12字节\\n    println!("字符数: {} 个", greeting.chars().count());  // 4个\\n    \\n    // 检查是否包含\\n    println!("包含 好? {}", greeting.contains("好"));\\n}',
            'common_errors': '[{"报错":"cannot index into a value of type `String`","解决办法":"Rust字符串不能用索引，用 chars() 或切片"}]',
            'aliases': 'String,&str,字符串切片,所有权',
        },
        {
            'title': '切片 &[T]',
            'language': 'Rust', 'version': '>=1.0',
            'code_block': 'fn main() {\n    let arr = [1, 2, 3, 4, 5];\n    \n    // 创建切片\n    let slice: &[i32] = &arr[1..4];  // [2, 3, 4]\n    println!("{:?}", slice);\n    \n    // 切片操作\n    println!("长度: {}", slice.len());\n    println!("是否为空: {}", slice.is_empty());\n    println!("第一个: {:?}", slice.first());\n    println!("最后一个: {:?}", slice.last());\n    \n    // Vec 也可以切片\n    let v = vec![10, 20, 30, 40, 50];\n    let vs: &[i32] = &v[..3];  // [10, 20, 30]\n    \n    // 函数参数用切片\n    fn sum(nums: &[i32]) -> i32 {\n        nums.iter().sum()\n    }\n    \n    println!("和: {}", sum(&arr));     // 15\n    println!("和: {}", sum(&v));       // 150\n    println!("和: {}", sum(&arr[2..])); // 12\n    \n    // 可变切片\n    let mut data = [1, 2, 3, 4, 5];\n    let mutable_slice: &mut [i32] = &mut data[1..4];\n    mutable_slice[0] = 100;\n    println!("修改后: {:?}", data);  // [1, 100, 3, 4, 5]\n}',
            'line_by_line': '[{"代码":"&arr[start..end]","说明":"创建从start到end-1的切片"},{"代码":"&arr[..n]","说明":"从头到n-1的切片"},{"代码":"&arr[n..]","说明":"从n到末尾的切片"},{"代码":"&mut data[..]","说明":"可变切片，可修改内容"}]',
            'syntax_note': '切片是对连续元素的引用，不拥有所有权\\n切片范围使用 .. 语法，左闭右开\\n字符串切片必须切在字符边界（UTF-8），否则panic',
            'runnable_example': 'fn main() {\\n    let nums = [1, 2, 3, 4, 5, 6, 7, 8];\\n    let (left, right) = nums.split_at(4);\\n    println!("左半: {:?}", left);  // [1, 2, 3, 4]\\n    println!("右半: {:?}", right); // [5, 6, 7, 8]\\n}',
            'common_errors': '[{"报错":"index out of bounds","解决办法":"切片范围不能超出数组长度"}]',
            'aliases': '切片,slice,&[T],数组切片',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Rust +{len(items)}')

# ============ 更多 HTML（8条） ============
cat = find_cat('前端技术', 'HTML')
if cat:
    items = [
        {
            'title': '表单 form 与 input 类型',
            'language': 'HTML', 'version': 'HTML5',
            'code_block': '<form action="/submit" method="POST">\n    <!-- 文本输入 -->\n    <label>用户名: <input type="text" name="username" placeholder="输入用户名" required></label><br>\n\n    <!-- 密码 -->\n    <label>密码: <input type="password" name="password" minlength="6"></label><br>\n\n    <!-- 邮箱 -->\n    <label>邮箱: <input type="email" name="email" required></label><br>\n\n    <!-- 数字 -->\n    <label>年龄: <input type="number" name="age" min="0" max="150"></label><br>\n\n    <!-- 日期 -->\n    <label>生日: <input type="date" name="birthday"></label><br>\n\n    <!-- 单选 -->\n    <label>性别:\n        <input type="radio" name="gender" value="male" checked> 男\n        <input type="radio" name="gender" value="female"> 女\n    </label><br>\n\n    <!-- 多选 -->\n    <label>爱好:\n        <input type="checkbox" name="hobby" value="reading"> 阅读\n        <input type="checkbox" name="hobby" value="music"> 音乐\n        <input type="checkbox" name="hobby" value="sports"> 运动\n    </label><br>\n\n    <!-- 下拉选择 -->\n    <label>城市:\n        <select name="city">\n            <option value="">请选择</option>\n            <option value="beijing">北京</option>\n            <option value="shanghai">上海</option>\n            <option value="shenzhen">深圳</option>\n        </select>\n    </label><br>\n\n    <!-- 多行文本 -->\n    <label>简介: <textarea name="bio" rows="3" cols="30"></textarea></label><br>\n\n    <!-- 文件上传 -->\n    <label>头像: <input type="file" name="avatar" accept="image/*"></label><br>\n\n    <!-- 颜色选择 -->\n    <label>主题色: <input type="color" name="theme"></label><br>\n\n    <!-- 范围滑块 -->\n    <label>音量: <input type="range" name="volume" min="0" max="100" value="50"></label><br>\n\n    <!-- 隐藏字段 -->\n    <input type="hidden" name="token" value="abc123">\n\n    <!-- 提交/重置 -->\n    <button type="submit">提交</button>\n    <button type="reset">重置</button>\n</form>',
            'line_by_line': '[{"代码":"<form action=method=>","说明":"表单容器，action=提交地址，method=GET/POST"},{"代码":"<input type=text/password/email/...>","说明":"输入框，type决定输入类型和验证"},{"代码":"<label>文字 <input></label>","说明":"通过包裹关联label和input"},{"代码":"required","说明":"必填字段，浏览器会自动验证"},{"代码":"<select><option>","说明":"下拉选择框"}]',
            'syntax_note': 'POST 方法数据在请求体，GET 在URL上\\n每个输入应有 name 属性才能提交\\nrequired/minlength/pattern 等是HTML5内置验证',
            'runnable_example': '<form>\\n    <input type="text" name="username" pattern="[A-Za-z0-9]{4,16}" required>\\n    <input type="email" name="email" required>\\n    <button>注册</button>\\n</form>\\n<!-- pattern 要求4-16位字母数字 -->',
            'common_errors': '[]',
            'aliases': '表单,form,input,提交',
        },
        {
            'title': '语义标签 header/nav/main/footer',
            'language': 'HTML', 'version': 'HTML5',
            'code_block': '<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n    <title>语义化HTML</title>\n</head>\n<body>\n    <!-- 页眉 -->\n    <header>\n        <h1>我的博客</h1>\n        <p>分享技术心得</p>\n    </header>\n\n    <!-- 导航栏 -->\n    <nav>\n        <ul>\n            <li><a href="/">首页</a></li>\n            <li><a href="/articles">文章</a></li>\n            <li><a href="/about">关于</a></li>\n        </ul>\n    </nav>\n\n    <!-- 主要内容 -->\n    <main>\n        <article>\n            <header>\n                <h2>文章标题</h2>\n                <time datetime="2024-01-15">2024年1月15日</time>\n            </header>\n            <section>\n                <h3>第一节</h3>\n                <p>这里是文章内容...</p>\n            </section>\n            <section>\n                <h3>第二节</h3>\n                <p>更多内容...</p>\n            </section>\n        </article>\n\n        <aside>\n            <h3>侧边栏</h3>\n            <ul>\n                <li><a href="/tag/html">HTML标签</a></li>\n                <li><a href="/tag/css">CSS技巧</a></li>\n            </ul>\n        </aside>\n    </main>\n\n    <!-- 页脚 -->\n    <footer>\n        <p>&copy; 2024 我的博客. All rights reserved.</p>\n        <address>联系: admin@example.com</address>\n    </footer>\n</body>\n</html>',
            'line_by_line': '[{"代码":"<header>","说明":"页眉，通常放标题、logo、导航"},{"代码":"<nav>","说明":"导航栏，放主要导航链接"},{"代码":"<main>","说明":"页面主要内容，每个页面只有一个"},{"代码":"<article>","说明":"独立的内容块，如博客文章"},{"代码":"<section>","说明":"文档中的节/段"},{"代码":"<aside>","说明":"侧边栏，放相关但不核心的内容"},{"代码":"<footer>","说明":"页脚，版权/联系信息"},{"代码":"<time>","说明":"日期时间，datetime属性机器可读"}]',
            'syntax_note': '语义标签对SEO和无障碍重要\\n一个页面只有一个 <main>\\n<article> 可以嵌套 <section>，反之亦然\\n语义标签不影响默认样式，需要自己写CSS',
            'runnable_example': '<header>\\n    <h1>我的网站</h1>\\n</header>\\n<nav>\\n    <a href="/">首页</a> | <a href="/blog">博客</a>\\n</nav>\\n<main>\\n    <article>\\n        <h2>文章</h2>\\n        <p>内容...</p>\\n    </article>\\n</main>\\n<footer>\\n    <p>Copyright 2024</p>\\n</footer>',
            'common_errors': '[]',
            'aliases': '语义标签,HTML5,header,nav,main,footer,article,section,aside',
        },
    ]
    add_all(cat, items)
    print(f'[OK] HTML +{len(items)}')

# ============ 更多 CSS（8条） ============
cat = find_cat('前端技术', 'CSS')
if cat:
    items = [
        {
            'title': 'Grid 网格布局',
            'language': 'CSS', 'version': 'CSS3',
            'code_block': '.grid-container {\n    display: grid;\n    /* 定义3列，宽度1:1:1 */\n    grid-template-columns: 1fr 1fr 1fr;\n    /* 定义行高 */\n    grid-template-rows: auto;\n    /* 间距 */\n    gap: 16px;\n}\n\n/* 固定+自适应 */\n.grid-mixed {\n    display: grid;\n    grid-template-columns: 200px 1fr 200px;\n    grid-template-areas:\n        "header header header"\n        "sidebar main aside"\n        "footer footer footer";\n}\n\n.header { grid-area: header; }\n.sidebar { grid-area: sidebar; }\n.main { grid-area: main; }\n.aside { grid-area: aside; }\n.footer { grid-area: footer; }\n\n/* 自适应列数 */\n.grid-auto {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 20px;\n}\n\n/* 项目放置 */\n.item-special {\n    grid-column: span 2;  /* 跨2列 */\n    grid-row: 1 / 3;      /* 从行1到行3 */\n}',
            'line_by_line': '[{"代码":"display: grid","说明":"启用Grid布局"},{"代码":"grid-template-columns: 1fr 1fr 1fr","说明":"定义列数和宽度，fr等分剩余空间"},{"代码":"grid-template-areas","说明":"用命名区域定义布局模板"},{"代码":"gap","说明":"网格间距"},{"代码":"repeat(auto-fit, minmax(250px, 1fr))","说明":"自动适应列数，每列最小250px"},{"代码":"grid-column: span 2","说明":"项目跨2列"}]',
            'syntax_note': 'Grid 是二维布局，Flexbox 是一维\\nfr 单位份额剩余的可用空间\\nauto-fit 和 auto-fill 区别：auto-fit 空列会折叠',
            'runnable_example': '/* 响应式卡片网格 */\\n.cards {\\n    display: grid;\\n    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));\\n    gap: 20px;\\n    padding: 20px;\\n}\\n.card {\\n    background: white;\\n    border-radius: 8px;\\n    padding: 20px;\\n    box-shadow: 0 2px 8px rgba(0,0,0,0.1);\\n}',
            'common_errors': '[]',
            'aliases': 'Grid,网格布局,grid布局',
        },
        {
            'title': '@media 响应式查询',
            'language': 'CSS', 'version': 'CSS3',
            'code_block': '/* 基础样式 */\n.container {\n    display: grid;\n    grid-template-columns: 1fr 1fr 1fr;\n    gap: 20px;\n}\n\n/* 平板（≤768px） */\n@media (max-width: 768px) {\n    .container {\n        grid-template-columns: 1fr 1fr;\n    }\n    body {\n        font-size: 14px;\n    }\n}\n\n/* 手机（≤480px） */\n@media (max-width: 480px) {\n    .container {\n        grid-template-columns: 1fr;\n    }\n    .sidebar {\n        display: none;\n    }\n}\n\n/* 打印样式 */\n@media print {\n    header, footer, nav {\n        display: none;\n    }\n    body {\n        font-size: 12pt;\n    }\n}\n\n/* 暗色模式偏好 */\n@media (prefers-color-scheme: dark) {\n    body {\n        background-color: #1a1a1a;\n        color: #e0e0e0;\n    }\n}\n\n/* 横屏 */\n@media (orientation: landscape) {\n    .sidebar {\n        width: 300px;\n    }\n}',
            'line_by_line': '[{"代码":"@media (max-width: 768px)","说明":"屏幕宽度≤768px时应用"},{"代码":"@media print","说明":"打印时应用的样式"},{"代码":"@media (prefers-color-scheme: dark)","说明":"用户系统为暗色模式时"},{"代码":"@media (orientation: landscape)","说明":"横屏时"}]',
            'syntax_note': '媒体查询不增加CSS选择器的权重\\n常用断点：480px(手机), 768px(平板), 1024px(桌面)\\n可组合条件：@media (min-width: 600px) and (max-width: 1024px)',
            'runnable_example': '/* Mobile First 策略 */\\n.container {\\n    grid-template-columns: 1fr;  /* 手机默认单列 */\\n}\\n\\n@media (min-width: 600px) {\\n    .container { grid-template-columns: 1fr 1fr; }\\n}\\n\\n@media (min-width: 900px) {\\n    .container { grid-template-columns: 1fr 1fr 1fr; }\\n}',
            'common_errors': '[]',
            'aliases': '@media,响应式,媒体查询,responsive',
        },
    ]
    add_all(cat, items)
    print(f'[OK] CSS +{len(items)}')

# ============ 更多 Vue（6条） ============
cat = find_cat('前端技术', 'Vue')
if cat:
    items = [
        {
            'title': '计算属性 computed',
            'language': 'Vue', 'version': 'Vue 3',
            'code_block': '<template>\n    <div>\n        <input v-model="price" type="number" placeholder="价格">\n        <input v-model="quantity" type="number" placeholder="数量">\n        \n        <p>小计: {{ subtotal }}</p>\n        <p>折扣: {{ discount }}</p>\n        <p>总计: {{ total }}</p>\n        <p>支付方式: {{ paymentMethod }}</p>\n    </div>\n</template>\n\n<script setup>\nimport { ref, computed } from "vue";\n\nconst price = ref(0);\nconst quantity = ref(1);\nconst isVIP = ref(false);\n\n// 计算属性 - 自动缓存\nconst subtotal = computed(() => price.value * quantity.value);\n\nconst discount = computed(() => {\n    if (isVIP.value) return subtotal.value * 0.2;\n    return subtotal.value >= 100 ? subtotal.value * 0.1 : 0;\n});\n\nconst total = computed(() => subtotal.value - discount.value);\n\n// getter/setter 计算属性\nconst paymentMethod = computed({\n    get: () => total.value > 0 ? "在线支付" : "免费",\n    set: (val) => {\n        console.log("设置支付方式:", val);\n    }\n});\n</script>',
            'line_by_line': '[{"代码":"computed(() => expr)","说明":"只读计算属性，返回计算结果"},{"代码":"computed({get, set})","说明":"可读写计算属性"},{"代码":"computed 自动缓存","说明":"只有依赖变化时才重新计算"}]',
            'syntax_note': 'computed 有缓存，methods 每次调用都会执行\\n不要在 computed 中修改响应式数据（副作用）\\ncomputed 默认只读，如果需要修改加 get/set',
            'runnable_example': '<template>\\n    <div>\\n        <input v-model="firstName" placeholder="姓">\\n        <input v-model="lastName" placeholder="名">\\n        <p>全名: {{ fullName }}</p>\\n    </div>\\n</template>\\n\\n<script setup>\\nimport { ref, computed } from "vue";\\nconst firstName = ref("");\\nconst lastName = ref("");\\nconst fullName = computed(() => `${firstName.value}${lastName.value}`);\\n</script>',
            'common_errors': '[]',
            'aliases': 'computed,计算属性,响应式计算',
        },
        {
            'title': 'watch 侦听器',
            'language': 'Vue', 'version': 'Vue 3',
            'code_block': '<template>\n    <div>\n        <input v-model="searchQuery" placeholder="搜索...">\n        <p>结果数: {{ results.length }}</p>\n        <ul>\n            <li v-for="item in results" :key="item">{{ item }}</li>\n        </ul>\n    </div>\n</template>\n\n<script setup>\nimport { ref, watch } from "vue";\n\nconst searchQuery = ref("");\nconst results = ref([]);\n\n// 基础侦听\nwatch(searchQuery, (newVal, oldVal) => {\n    console.log(`搜索词从 "${oldVal}" 变为 "${newVal}"`);\n    // 模拟搜索\n    if (newVal) {\n        results.value = [`结果1: ${newVal}`, `结果2: ${newVal}`];\n    } else {\n        results.value = [];\n    }\n});\n\n// 侦听多个源\nconst x = ref(0);\nconst y = ref(0);\nwatch([x, y], ([newX, newY], [oldX, oldY]) => {\n    console.log(`位置从 (${oldX},${oldY}) 变为 (${newX},${newY})`);\n});\n\n// 深度侦听对象\nconst user = ref({ name: "张三", details: { age: 28 } });\nwatch(\n    user,\n    (newVal) => {\n        console.log("用户信息变了", newVal);\n    },\n    { deep: true, immediate: true }\n);\n// deep: 深度侦听嵌套属性\n// immediate: 立即执行一次\n</script>',
            'line_by_line': '[{"代码":"watch(source, callback)","说明":"侦听单个响应式数据变化"},{"代码":"watch([s1, s2], callback)","说明":"侦听多个数据源"},{"代码":"{ deep: true }","说明":"深度侦听嵌套对象"},{"代码":"{ immediate: true }","说明":"创建时立即执行一次回调"}]',
            'syntax_note': 'watch 是惰性的，只有数据变化才执行（除非 immediate: true）\\nwatchEffect 会自动收集依赖，立即执行\\n侦听 ref 直接传变量，侦听 reactive 要传函数 () => obj.prop',
            'runnable_example': '<script setup>\\nimport { ref, watch } from "vue";\\nconst count = ref(0);\\n\\n// 当count达到10时重置\\nwatch(count, (val) => {\\n    if (val >= 10) {\\n        console.log("达到上限，重置");\\n        count.value = 0;\\n    }\\n});\\n</script>\\n<template>\\n    <button @click="count++">点击: {{ count }}</button>\\n</template>',
            'common_errors': '[]',
            'aliases': 'watch,侦听器,观察者',
        },
    ]
    add_all(cat, items)
    print(f'[OK] Vue +{len(items)}')

# ============ 更多 React（6条） ============
cat = find_cat('前端技术', 'React')
if cat:
    items = [
        {
            'title': 'useEffect 副作用',
            'language': 'React', 'version': 'React 16.8+',
            'code_block': 'import { useState, useEffect } from "react";\n\nfunction UserProfile({ userId }) {\n    const [user, setUser] = useState(null);\n    const [loading, setLoading] = useState(true);\n\n    // 1. 组件挂载时执行一次\n    useEffect(() => {\n        console.log("组件已挂载");\n    }, []);  // 空依赖数组\n\n    // 2. 依赖变化时执行\n    useEffect(() => {\n        async function fetchUser() {\n            setLoading(true);\n            try {\n                const res = await fetch(`/api/users/${userId}`);\n                const data = await res.json();\n                setUser(data);\n            } catch (err) {\n                console.error("加载失败:", err);\n            } finally {\n                setLoading(false);\n            }\n        }\n\n        fetchUser();\n    }, [userId]);  // userId变化时重新获取\n\n    // 3. 清理函数（组件卸载或重新执行前）\n    useEffect(() => {\n        const timer = setInterval(() => {\n            console.log("定时器执行中...");\n        }, 1000);\n\n        return () => {\n            clearInterval(timer);  // 组件卸载时清理\n            console.log("定时器已清理");\n        };\n    }, []);\n\n    // 4. 每次渲染都执行\n    useEffect(() => {\n        console.log("组件更新了");\n    });  // 无依赖数组\n\n    if (loading) return <div>加载中...</div>;\n    return <div>{user?.name}</div>;\n}',
            'line_by_line': '[{"代码":"useEffect(fn, [deps])","说明":"副作用钩子，在渲染后执行"},{"代码":"[ ]","说明":"空数组：仅在挂载时执行一次"},{"代码":"[dep]","说明":"依赖变化时重新执行"},{"代码":"return () => { cleanup }","说明":"清理函数，组件卸载或重新执行前调用"},{"代码":"无依赖","说明":"每次渲染后都执行"}]',
            'syntax_note': 'useEffect 在浏览器渲染完成后执行（不阻塞渲染）\\n不要在useEffect中更新触发无限循环的状态\\n如果多个依赖变化触发了同一个useEffect，React会自动批处理',
            'runnable_example': 'function WindowWidth() {\\n    const [width, setWidth] = useState(window.innerWidth);\\n    \\n    useEffect(() => {\\n        const handleResize = () => setWidth(window.innerWidth);\\n        window.addEventListener("resize", handleResize);\\n        return () => window.removeEventListener("resize", handleResize);\\n    }, []);\\n    \\n    return <p>窗口宽度: {width}px</p>;\\n}',
            'common_errors': '[{"报错":"Maximum update depth exceeded","解决办法":"检查useEffect是否在更新中触发了自身依赖的状态"}]',
            'aliases': 'useEffect,副作用,生命周期,React Hooks',
        },
        {
            'title': 'useRef 和 useMemo',
            'language': 'React', 'version': 'React 16.8+',
            'code_block': 'import { useState, useRef, useMemo, useCallback } from "react";\n\nfunction Timer() {\n    const [count, setCount] = useState(0);\n    \n    // useRef: 保存可变值，不触发重新渲染\n    const intervalRef = useRef(null);\n    const inputRef = useRef(null);\n    const prevCountRef = useRef(0);\n\n    // 记录上一次的count\n    useEffect(() => {\n        prevCountRef.current = count;\n    }, [count]);\n\n    const startTimer = () => {\n        intervalRef.current = setInterval(() => {\n            setCount(c => c + 1);\n        }, 1000);\n    };\n\n    const stopTimer = () => {\n        clearInterval(intervalRef.current);\n    };\n\n    // 聚焦输入框\n    const focusInput = () => {\n        inputRef.current?.focus();\n    };\n\n    // useMemo: 缓存计算结果（避免重复计算）\n    const expensiveResult = useMemo(() => {\n        console.log("计算中...");\n        return Array.from({ length: 1000 }, (_, i) => i ** 2)\n            .filter(n => n < count * 1000);\n    }, [count]);  // count变化时才重新计算\n\n    return (\n        <div>\n            <input ref={inputRef} placeholder="自动聚焦" />\n            <button onClick={focusInput}>聚焦输入框</button>\n            <p>计数: {count}</p>\n            <button onClick={startTimer}>开始</button>\n            <button onClick={stopTimer}>停止</button>\n            <p>结果数: {expensiveResult.length}</p>\n        </div>\n    );\n}\n\n// useCallback: 缓存函数引用\nconst memoizedCallback = useCallback(\n    () => { doSomething(a, b); },\n    [a, b]\n);',
            'line_by_line': '[{"代码":"useRef(initialValue)","说明":"创建可变的ref对象，.current属性存储值"},{"代码":"ref={inputRef}","说明":"绑定到DOM元素的ref属性，可访问原生DOM"},{"代码":"useMemo(() => fn, [deps])","说明":"缓存计算结果，依赖不变跳过计算"},{"代码":"useCallback(fn, [deps])","说明":"缓存函数引用，避免子组件不必要的重渲染"}]',
            'syntax_note': 'useRef 修改 .current 不会触发重新渲染\\nuseMemo 和 useCallback 用于性能优化，不要滥用\\npremature optimization is the root of all evil',
            'runnable_example': 'function AutoFocusInput() {\\n    const inputRef = useRef(null);\\n    \\n    useEffect(() => {\\n        inputRef.current?.focus();  // 自动聚焦\\n    }, []);\\n    \\n    return <input ref={inputRef} />;\\n}',
            'common_errors': '[]',
            'aliases': 'useRef,useMemo,useCallback,ref,缓存',
        },
    ]
    add_all(cat, items)
    print(f'[OK] React +{len(items)}')

# ============ 总统计 ============
total_snippets = db.conn.execute("SELECT COUNT(*) FROM code_snippets").fetchone()[0]
grand_total = db.get_total_count()
print(f'\\n{"="*50}')
print(f'[OK] 代码片段总条数: {total_snippets}')
print(f'[OK] 数据库总条数: {grand_total}')
print(f'{"="*50}')
