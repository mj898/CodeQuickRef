#!/usr/bin/env python3
"""
种子数据脚本：向 SQLite 数据库插入 ADB (Android Debug Bridge) 命令数据
用法：python3 seed_adb.py
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from database.db_manager import DBManager

db = DBManager()
db.init_db()

# ── 查找/创建 "ADB (Android)" 分类 ──
adb_cat = None
for root in db.get_categories(parent_id=None):
    if root['name'] == '命令行工具':
        for child in db.get_categories(parent_id=root['id']):
            if child['name'] == 'ADB (Android)':
                adb_cat = child['id']
                break
        if not adb_cat:
            children = db.get_categories(parent_id=root['id'])
            max_order = max((c.get('sort_order', 0) for c in children), default=0)
            adb_cat = db.add_category('ADB (Android)', root['id'], 'command', max_order + 10)
        break

if not adb_cat:
    print('[ERR] 无法找到或创建 ADB (Android) 分类')
    sys.exit(1)

print(f'[OK] ADB (Android) 分类 ID: {adb_cat}')

# ── 批量插入辅助函数 ──
def add(**kw):
    kw['category_id'] = adb_cat
    db.add_command(**kw)

# ════════════════════════════════════════════
# 第一部分：adb 顶层命令
# ════════════════════════════════════════════

add(
    cmd_name='adb devices',
    name_cn='列出连接的设备',
    function_desc='列出所有已连接（adb 协议）的 Android 设备/模拟器，显示序列号和状态（device/offline/unauthorized）',
    syntax='adb devices [-l]',
    params_json='[{"参数":"-l","说明":"显示详细设备信息（设备型号、版本等）","必填":"可选"}]',
    example_basic='adb devices',
    example_adv='adb devices -l',
    os_type='通用',
    aliases='设备列表,列出设备,devices,连接设备',
    tips='如果显示 unauthorized，需要在设备上确认 USB 调试授权。显示 offline 表示设备连接但 adb 未就绪。',
)
add(
    cmd_name='adb connect',
    name_cn='连接远程设备',
    function_desc='通过 TCP/IP 连接到远程 Android 设备（用于无线调试），默认端口 5555',
    syntax='adb connect <设备IP>:<端口>',
    params_json='[{"参数":"设备IP","说明":"Android 设备的 IP 地址","必填":"必填"},{"参数":"端口","说明":"连接端口，默认 5555","必填":"可选"}]',
    example_basic='adb connect 192.168.1.100',
    example_adv='adb connect 192.168.1.100:5555',
    os_type='通用',
    aliases='连接设备,远程连接,无线调试,connect',
    tips='无线调试前需要先用 USB 连接并执行 adb tcpip 5555。确保设备和电脑在同一局域网。',
)
add(
    cmd_name='adb disconnect',
    name_cn='断开远程设备',
    function_desc='断开与远程 Android 设备的 TCP/IP 连接。不传参数则断开所有连接',
    syntax='adb disconnect [<设备IP>:<端口>]',
    params_json='[{"参数":"设备IP:端口","说明":"要断开连接的设备地址（可选），不填则断开所有","必填":"可选"}]',
    example_basic='adb disconnect',
    example_adv='adb disconnect 192.168.1.100:5555',
    os_type='通用',
    aliases='断开连接,断开设备,disconnect',
    tips='无线调试完成后建议断开连接以释放 adb 服务资源。',
)
add(
    cmd_name='adb install',
    name_cn='安装 APK',
    function_desc='将 APK 文件安装到连接的 Android 设备上。支持多个选项控制安装行为',
    syntax='adb install [-r] [-d] [-g] [-t] [--abi ABI] <APK路径>',
    params_json='[{"参数":"-r","说明":"覆盖安装（保留数据重新安装）","必填":"可选"},{"参数":"-d","说明":"允许版本降级安装","必填":"可选"},{"参数":"-g","说明":"授予安装时请求的所有运行时权限","必填":"可选"},{"参数":"-t","说明":"允许安装测试 APK","必填":"可选"},{"参数":"--abi ABI","说明":"强制使用指定 ABI（如 arm64-v8a）","必填":"可选"},{"参数":"APK路径","说明":"要安装的 APK 文件路径","必填":"必填"}]',
    example_basic='adb install app.apk',
    example_adv='adb install -r -d -g my_app.apk',
    os_type='通用',
    aliases='安装apk,安装应用,install,安装',
    tips='使用 -r 覆盖安装可以保留用户数据。当安装失败时先检查 adb devices 是否显示 device 状态。也可以在 install 前用 adb uninstall 卸载旧版。',
)
add(
    cmd_name='adb install-multiple',
    name_cn='安装多 APK（拆分APK）',
    function_desc='安装拆分 APK（split APK / app bundle），将多个 APK 片段组合安装为同一个应用',
    syntax='adb install-multiple [-r] [-d] [-g] [-t] <APK片段1> <APK片段2> ...',
    params_json='[{"参数":"-r","说明":"覆盖安装","必填":"可选"},{"参数":"-d","说明":"允许降级","必填":"可选"},{"参数":"-g","说明":"授予运行时权限","必填":"可选"},{"参数":"-t","说明":"测试 APK","必填":"可选"},{"参数":"APK片段","说明":"base.apk + config.*.apk 等拆分文件","必填":"必填"}]',
    example_basic='adb install-multiple base.apk split_config.arm64_v8a.apk',
    example_adv='adb install-multiple -r base.apk split_config.arm64_v8a.apk split_config.zh.apk',
    os_type='通用',
    aliases='安装拆分apk,install-multiple,split apk',
    tips='从 Google Play 下载的 app bundle 或从 aab 转换的拆分 APK 需用此命令安装。建议只用 adb install 来安装普通 APK。',
)
add(
    cmd_name='adb uninstall',
    name_cn='卸载应用',
    function_desc='从 Android 设备上卸载指定包名的应用',
    syntax='adb uninstall [-k] <包名>',
    params_json='[{"参数":"-k","说明":"卸载应用但保留数据和缓存目录","必填":"可选"},{"参数":"包名","说明":"要卸载的应用包名（如 com.example.app）","必填":"必填"}]',
    example_basic='adb uninstall com.example.app',
    example_adv='adb uninstall -k com.example.app',
    os_type='通用',
    aliases='卸载应用,删除应用,uninstall,卸载',
    tips='使用 pm list packages 或 adb shell pm list packages 查找包名。加 -k 保留数据，适合需要重新安装但保留用户数据的场景。',
)
add(
    cmd_name='adb push',
    name_cn='推送文件到设备',
    function_desc='将本地文件或目录复制到 Android 设备上的指定路径',
    syntax='adb push <本地路径> <设备路径>',
    params_json='[{"参数":"本地路径","说明":"本地文件或目录的路径","必填":"必填"},{"参数":"设备路径","说明":"设备上的目标路径","必填":"必填"}]',
    example_basic='adb push file.txt /sdcard/',
    example_adv='adb push ./data/ /sdcard/backup/',
    os_type='通用',
    aliases='推送文件,上传文件,push,上传',
    tips='设备路径通常用 /sdcard/ 或 /storage/emulated/0/。推送大文件可能会耗时较长，adb pull 可查看进度。',
)
add(
    cmd_name='adb pull',
    name_cn='从设备拉取文件',
    function_desc='从 Android 设备复制文件或目录到本地电脑',
    syntax='adb pull <设备路径> [<本地路径>]',
    params_json='[{"参数":"设备路径","说明":"设备上的源文件/目录路径","必填":"必填"},{"参数":"本地路径","说明":"本地目标路径（可选，默认当前目录）","必填":"可选"}]',
    example_basic='adb pull /sdcard/screenshot.png',
    example_adv='adb pull /sdcard/DCIM/Camera/ ./photos/',
    os_type='通用',
    aliases='拉取文件,下载文件,pull,下载',
    tips='不指定本地路径则保存到当前目录。拉取大文件目录时建议指定本地路径以便管理。如果文件不存在的检查路径是否正确。',
)
add(
    cmd_name='adb shell',
    name_cn='进入设备 Shell',
    function_desc='在 Android 设备上启动一个交互式 shell，或执行单条 shell 命令',
    syntax='adb shell [<命令>]',
    params_json='[{"参数":"命令","说明":"要在设备上执行的 shell 命令（可选），不传则进入交互式 shell","必填":"可选"}]',
    example_basic='adb shell',
    example_adv='adb shell "dumpsys battery | grep level"',
    os_type='通用',
    aliases='shell,终端,命令执行,设备终端',
    tips='不传参数进入交互式 shell（类似 SSH）。传单条命令则执行后退出。Linux shell 命令大多数可用（如 ls, ps, top, cat 等）。',
)
add(
    cmd_name='adb logcat',
    name_cn='查看设备日志',
    function_desc='实时查看 Android 设备日志输出。支持缓冲区、标签、优先级等过滤条件',
    syntax='adb logcat [选项] [过滤器]',
    params_json='[{"参数":"-b <缓冲区>","说明":"查看指定缓冲区：main/system/events/crash/all","必填":"可选"},{"参数":"-c","说明":"清空日志缓冲区","必填":"可选"},{"参数":"-d","说明":"一次性输出日志后退出","必填":"可选"},{"参数":"-v <格式>","说明":"输出格式：brief/threadtime/time/long","必填":"可选"},{"参数":"-s <标签>","说明":"只显示指定 tag 的日志","必填":"可选"},{"参数":"-f <文件>","说明":"将日志写入设备上的文件","必填":"可选"},{"参数":"过滤器","说明":"格式: <tag>:<优先级>，如 ActivityManager:I *:S","必填":"可选"}]',
    example_basic='adb logcat',
    example_adv='adb logcat -b all -v threadtime -s ActivityManager:I *:S',
    os_type='通用',
    aliases='日志,查看日志,logcat,设备日志',
    tips='最常用组合：adb logcat -b all -v threadtime。过滤特定应用日志：adb logcat -s 包名:V。清空日志：adb logcat -c。',
)
add(
    cmd_name='adb reboot',
    name_cn='重启设备',
    function_desc='重启 Android 设备。支持正常重启、进入 bootloader 或 recovery 模式',
    syntax='adb reboot [bootloader|recovery|sideload|sideload-auto-reboot]',
    params_json='[{"参数":"bootloader","说明":"重启到 bootloader 模式（引导加载器）","必填":"可选"},{"参数":"recovery","说明":"重启到 recovery 模式（恢复模式）","必填":"可选"},{"参数":"sideload","说明":"重启到 sideload 模式（侧载模式）","必填":"可选"},{"参数":"sideload-auto-reboot","说明":"侧载完成后自动重启","必填":"可选"}]',
    example_basic='adb reboot',
    example_adv='adb reboot bootloader',
    os_type='通用',
    aliases='重启,reboot,重启动,重启设备',
    tips='不传参数为正常重启。进入 bootloader 后可使用 fastboot 命令。sideload 用于 OTA 更新。',
)
add(
    cmd_name='adb reboot-bootloader',
    name_cn='重启到 Bootloader',
    function_desc='重启设备直接进入 bootloader 模式（等同于 adb reboot bootloader）',
    syntax='adb reboot-bootloader',
    params_json='[]',
    example_basic='adb reboot-bootloader',
    example_adv='adb reboot-bootloader && fastboot flash recovery recovery.img',
    os_type='通用',
    aliases='bootloader,引导加载器,fastboot模式',
    tips='进入 bootloader 后设备不再响应 adb 命令，需要使用 fastboot 命令。不同品牌进入 bootloader 的按键组合不同。',
)
add(
    cmd_name='adb wait-for-device',
    name_cn='等待设备连接',
    function_desc='阻塞当前进程直到设备连接（或指定状态），常用于脚本中确保设备就绪后再执行后续命令',
    syntax='adb wait-for-device [transport]',
    params_json='[{"参数":"transport","说明":"等待指定传输状态：device/recovery/sideload/bootloader","必填":"可选"}]',
    example_basic='adb wait-for-device',
    example_adv='adb wait-for-device && adb shell "am broadcast -a android.intent.action.BOOT_COMPLETED"',
    os_type='通用',
    aliases='等待设备,wait-for-device,等待',
    tips='注意：wait-for-device 只表示 adb 服务检测到了设备，不保证系统完全启动。如需等待系统启动完成，配合 adb shell "while [ -z $(getprop sys.boot_completed) ]; do sleep 1; done" 使用。',
)
add(
    cmd_name='adb start-server',
    name_cn='启动 ADB 服务',
    function_desc='启动 adb 后台服务进程。通常 adb 会自动启动，但手动启动可以强制刷新服务',
    syntax='adb start-server',
    params_json='[]',
    example_basic='adb start-server',
    example_adv='adb kill-server && adb start-server',
    os_type='通用',
    aliases='启动服务,start-server,启动adb',
    tips='如果 adb devices 长时间无响应或报错，先执行 adb kill-server 再 adb start-server 重启服务。',
)
add(
    cmd_name='adb kill-server',
    name_cn='停止 ADB 服务',
    function_desc='终止 adb 后台服务进程。通常用于解决 adb 连接问题或释放端口',
    syntax='adb kill-server',
    params_json='[]',
    example_basic='adb kill-server',
    example_adv='adb kill-server && adb start-server && adb devices',
    os_type='通用',
    aliases='停止服务,kill-server,终止adb',
    tips='kill-server 后 adb devices 等命令会自动重新启动服务。这个命令不会影响已连接的设备会话。',
)
add(
    cmd_name='adb forward',
    name_cn='端口转发',
    function_desc='将本机端口转发到 Android 设备上的指定端口。常用于调试 WebView、Chrome DevTools 等',
    syntax='adb forward [--no-rebind] <本地端口> <设备端口>',
    params_json='[{"参数":"--no-rebind","说明":"如果端口已被转发则报错而非覆盖","必填":"可选"},{"参数":"本地端口","说明":"本机端口号，如 tcp:8080","必填":"必填"},{"参数":"设备端口","说明":"设备上的端口，如 tcp:8080 或 localabstract:chrome_devtools_remote","必填":"必填"}]',
    example_basic='adb forward tcp:8080 tcp:8080',
    example_adv='adb forward tcp:9222 localabstract:chrome_devtools_remote',
    os_type='通用',
    aliases='端口转发,forward,转发',
    tips='使用 adb forward --list 查看当前所有转发规则。常用于 Chrome 远程调试、Android WebView 调试。',
)
add(
    cmd_name='adb reverse',
    name_cn='反向端口转发',
    function_desc='将设备端口转发到本机端口（与 forward 方向相反）。让设备上的应用可以访问本机服务',
    syntax='adb reverse [--no-rebind] <设备端口> <本地端口>',
    params_json='[{"参数":"--no-rebind","说明":"端口已被占用时报错","必填":"可选"},{"参数":"设备端口","说明":"设备上的端口","必填":"必填"},{"参数":"本地端口","说明":"本机目标端口","必填":"必填"}]',
    example_basic='adb reverse tcp:8080 tcp:8080',
    example_adv='adb reverse tcp:8081 tcp:3000',
    os_type='通用',
    aliases='反向转发,reverse,反向端口转发',
    tips='reverse 让 Android 设备可以访问电脑上的服务，不需要 USB 共享网络。常用场景：设备上的浏览器访问电脑的 localhost 开发服务器。',
)
add(
    cmd_name='adb forward --list',
    name_cn='查看端口转发列表',
    function_desc='列出当前所有 adb 端口转发规则',
    syntax='adb forward --list',
    params_json='[]',
    example_basic='adb forward --list',
    example_adv='adb forward --list | grep tcp',
    os_type='通用',
    aliases='转发列表,forward-list,查看转发',
    tips='输出格式：<序列号> <本地端口> <设备端口>。',
)
add(
    cmd_name='adb tcpip',
    name_cn='开启无线调试模式',
    function_desc='重启 adbd 在指定 TCP 端口上监听，使设备可以通过网络连接（无线调试的第一步）',
    syntax='adb tcpip <端口号>',
    params_json='[{"参数":"端口号","说明":"adb 通信端口（默认 5555）","必填":"必填"}]',
    example_basic='adb tcpip 5555',
    example_adv='adb tcpip 5555 && adb connect 192.168.1.100',
    os_type='通用',
    aliases='无线调试,tcpip,无线连接',
    tips='此命令需要通过 USB 连接时执行。执行后拔掉 USB 线，用 adb connect <IP> 连接。安全考虑，调试完成后建议 adb usb 切回 USB 模式。',
)
add(
    cmd_name='adb usb',
    name_cn='切回 USB 调试模式',
    function_desc='让 adbd 切回 USB 监听模式，断开所有无线连接',
    syntax='adb usb',
    params_json='[]',
    example_basic='adb usb',
    example_adv='adb usb && adb devices',
    os_type='通用',
    aliases='usb模式,usb调试,切回usb',
    tips='从无线调试切回 USB 调试，之后需要重新通过 USB 连接设备。',
)
add(
    cmd_name='adb root',
    name_cn='以 root 权限重启 adbd',
    function_desc='以 root 权限重新启动 adbd 守护进程。获取更高权限来执行需要 root 的操作',
    syntax='adb root',
    params_json='[]',
    example_basic='adb root',
    example_adv='adb root && adb remount',
    os_type='通用',
    aliases='root权限,root,提权',
    tips='仅限已 root 的设备或模拟器。成功后 adbd 会以 root 身份重启。执行后 adb 会短暂断开再重连。',
)
add(
    cmd_name='adb unroot',
    name_cn='取消 adbd root 权限',
    function_desc='以非 root 权限重新启动 adbd 守护进程，恢复普通用户权限',
    syntax='adb unroot',
    params_json='[]',
    example_basic='adb unroot',
    example_adv='adb unroot && adb shell "id"',
    os_type='通用',
    aliases='取消root,unroot,取消提权',
    tips='执行 adb root 后的安全恢复操作。仅限已 root 的设备。',
)
add(
    cmd_name='adb remount',
    name_cn='重新挂载分区为读写',
    function_desc='将 /system 等分区重新挂载为可读写状态，便于修改系统文件',
    syntax='adb remount',
    params_json='[]',
    example_basic='adb remount',
    example_adv='adb root && adb remount && adb push modified_file /system/app/',
    os_type='通用',
    aliases='重新挂载,remount,读写分区',
    tips='需要 root 权限，必须先执行 adb root。部分设备可能需要解锁 bootloader 才能修改 system 分区。',
)
add(
    cmd_name='adb sideload',
    name_cn='侧载 OTA 更新',
    function_desc='通过 sideload 模式传输 OTA 更新包到设备进行系统更新',
    syntax='adb sideload <OTA包路径>',
    params_json='[{"参数":"OTA包路径","说明":"OTA 更新 zip 文件路径","必填":"必填"}]',
    example_basic='adb sideload ota_update.zip',
    example_adv='adb reboot sideload && adb sideload ota_update.zip',
    os_type='通用',
    aliases='侧载,ota更新,sideload,系统更新',
    tips='设备需要先重启到 sideload 模式（adb reboot sideload）。传输完成后设备会自动验证并安装更新。',
)
add(
    cmd_name='adb backup',
    name_cn='备份设备数据',
    function_desc='创建 Android 设备/模拟器的完整或部分备份到本地文件',
    syntax='adb backup [-f <文件>] [-apk|-noapk] [-shared|-noshared] [-all] [-system|-nosystem] [<包名>...]',
    params_json='[{"参数":"-f <文件>","说明":"指定备份文件名（默认 backup.ab）","必填":"可选"},{"参数":"-apk","说明":"同时备份 APK 文件","必填":"可选"},{"参数":"-noapk","说明":"不备份 APK","必填":"可选"},{"参数":"-shared","说明":"备份共享存储（SD卡）","必填":"可选"},{"参数":"-all","说明":"备份所有已安装应用","必填":"可选"},{"参数":"-system","说明":"备份系统应用（与 -all 配合）","必填":"可选"},{"参数":"<包名>","说明":"只备份指定应用的数据","必填":"可选"}]',
    example_basic='adb backup -apk -shared -all -f backup.ab',
    example_adv='adb backup -noapk -f com.whatsapp.ab com.whatsapp',
    os_type='通用',
    aliases='备份,backup,数据备份',
    tips='备份文件默认保存到当前目录。Android 7.0+ 上某些应用可能阻止备份。恢复用 adb restore。',
)
add(
    cmd_name='adb restore',
    name_cn='恢复设备备份',
    function_desc='从 adb backup 创建的备份文件恢复到设备',
    syntax='adb restore <备份文件>',
    params_json='[{"参数":"备份文件","说明":".ab 格式备份文件路径","必填":"必填"}]',
    example_basic='adb restore backup.ab',
    example_adv='adb restore com.whatsapp.ab',
    os_type='通用',
    aliases='恢复,restore,还原备份',
    tips='恢复前建议先确认备份文件的完整性。恢复时会覆盖目标应用的现有数据。设备上需要确认恢复操作。',
)
add(
    cmd_name='adb bugreport',
    name_cn='生成 Bug 报告',
    function_desc='收集设备日志、诊断信息、系统状态等打包为 zip 文件，用于调试和 Bug 上报',
    syntax='adb bugreport [<文件名>]',
    params_json='[{"参数":"文件名","说明":"输出的 zip 文件名（可选，默认自动命名）","必填":"可选"}]',
    example_basic='adb bugreport',
    example_adv='adb bugreport my_bug_report.zip',
    os_type='通用',
    aliases='bug报告,bugreport,诊断报告',
    tips='生成时间较长，包含大量信息（dmesg, logcat, dumpstate, 应用列表等）。可使用 bugreportz 生成更紧凑的格式。',
)
add(
    cmd_name='adb get-state',
    name_cn='获取设备状态',
    function_desc='获取已连接设备的当前状态：device（正常）、offline（离线）、unknown（未知）',
    syntax='adb get-state',
    params_json='[]',
    example_basic='adb get-state',
    example_adv='[ "$(adb get-state)" = "device" ] && echo "设备就绪"',
    os_type='通用',
    aliases='设备状态,get-state',
    tips='常用于脚本中判断设备是否可用。如果有多台设备需指定序列号。',
)
add(
    cmd_name='adb get-serialno',
    name_cn='获取设备序列号',
    function_desc='获取已连接 Android 设备的序列号',
    syntax='adb get-serialno',
    params_json='[]',
    example_basic='adb get-serialno',
    example_adv='SERIAL=$(adb get-serialno) && echo "设备: $SERIAL"',
    os_type='通用',
    aliases='序列号,get-serialno,设备序列号',
    tips='序列号在多设备场景下用于唯一标识目标设备。设备线刷后序列号可能变化。',
)
add(
    cmd_name='adb get-devpath',
    name_cn='获取设备路径',
    function_desc='获取已连接设备的设备路径信息',
    syntax='adb get-devpath',
    params_json='[]',
    example_basic='adb get-devpath',
    example_adv='adb -s $(adb get-serialno) get-devpath',
    os_type='通用',
    aliases='设备路径,get-devpath,devpath',
    tips='通常返回类似 usb:1-1 的 USB 路径信息，用于多设备识别。',
)
add(
    cmd_name='adb emu',
    name_cn='发送模拟器命令',
    function_desc='向 Android 模拟器发送控制命令，如模拟来电、短信、GPS 位置等',
    syntax='adb emu <命令>',
    params_json='[{"参数":"avd <名称>","说明":"启动/控制指定 AVD","必填":"可选"},{"参数":"kill","说明":"关闭模拟器","必填":"可选"},{"参数":"sms <号码> <消息>","说明":"模拟接收短信","必填":"可选"},{"参数":"gsm call <号码>","说明":"模拟来电","必填":"可选"},{"参数":"geo fix <经度> <纬度>","说明":"设置模拟 GPS 位置","必填":"可选"},{"参数":"power <状态>","说明":"模拟电源状态（ac/off）","必填":"可选"},{"参数":"network <速度>","说明":"模拟网络速度（edge/gprs/hsdpa/lte/full）","必填":"可选"}]',
    example_basic='adb emu kill',
    example_adv='adb emu sms 13800138000 "验证码：123456"',
    os_type='通用',
    aliases='模拟器,emu,emulator命令',
    tips='仅适用于 Android 模拟器，不适用于真机。模拟短信/来电用于测试应用。',
)
add(
    cmd_name='adb version',
    name_cn='显示 ADB 版本',
    function_desc='显示 adb 工具的版本号和构建信息',
    syntax='adb version',
    params_json='[]',
    example_basic='adb version',
    example_adv='adb version | grep "Version"',
    os_type='通用',
    aliases='版本,version,adb版本',
    tips='不同版本的 adb 功能可能略有差异。建议使用最新版 Android SDK Platform Tools。',
)
add(
    cmd_name='adb help',
    name_cn='显示帮助信息',
    function_desc='显示 adb 命令的完整帮助文档，列出所有可用命令和选项',
    syntax='adb help',
    params_json='[]',
    example_basic='adb help',
    example_adv='adb help | grep "shell"',
    os_type='通用',
    aliases='帮助,help,帮助文档',
    tips='adb help 的输出比 --help 更详细。遇到不熟悉的命令时先查看帮助。',
)
add(
    cmd_name='adb -s <序列号>',
    name_cn='指定设备执行命令',
    function_desc='在多设备环境下使用 -s 参数指定目标设备序列号，对其执行后续 adb 命令',
    syntax='adb -s <序列号> <adb命令>',
    params_json='[{"参数":"序列号","说明":"目标设备的序列号（由 adb devices 列出）","必填":"必填"},{"参数":"adb命令","说明":"要执行的 adb 子命令","必填":"必填"}]',
    example_basic='adb -s emulator-5554 shell',
    example_adv='adb -s 0123456789ABCDEF install app.apk',
    os_type='通用',
    aliases='指定设备,-s,多设备,serial',
    tips='有多个设备连接时，不指定 -s 会报错"more than one device"。先执行 adb devices 列出所有序列号。',
)
add(
    cmd_name='adb -d',
    name_cn='指定 USB 设备',
    function_desc='在多设备环境中，只对通过 USB 连接的设备执行命令（不包括模拟器）',
    syntax='adb -d <adb命令>',
    params_json='[{"参数":"adb命令","说明":"要执行的 adb 子命令","必填":"必填"}]',
    example_basic='adb -d install app.apk',
    example_adv='adb -d shell "dumpsys battery"',
    os_type='通用',
    aliases='usb设备,-d,指定USB',
    tips='当同时连接了真机和模拟器时，-d 强制只操作 USB 真机。如果有多台 USB 设备则需要用 -s 指定。',
)
add(
    cmd_name='adb -e',
    name_cn='指定模拟器',
    function_desc='在多设备环境中，只对模拟器执行命令（不包括 USB 真机）',
    syntax='adb -e <adb命令>',
    params_json='[{"参数":"adb命令","说明":"要执行的 adb 子命令","必填":"必填"}]',
    example_basic='adb -e shell',
    example_adv='adb -e install app.apk',
    os_type='通用',
    aliases='模拟器,-e,指定模拟器',
    tips='-d 和 -e 不能同时使用。如果只有一个模拟器，-e 可以直接定位无需序列号。',
)

# ════════════════════════════════════════════
# 第二部分：adb shell 子命令体系
# ════════════════════════════════════════════

# ── 2.1 am (Activity Manager) ──

add(
    cmd_name='adb shell am start',
    name_cn='启动 Activity',
    function_desc='启动一个 Activity（应用界面），可携带 Intent 参数',
    syntax='adb shell am start [选项] <Intent>',
    params_json='[{"参数":"-n <组件>","说明":"指定要启动的组件（包名/Activity名）","必填":"必填"},{"参数":"-a <action>","说明":"Intent Action","必填":"可选"},{"参数":"-d <data_uri>","说明":"Intent Data URI","必填":"可选"},{"参数":"-e <key> <value>","说明":"字符串类型 Extra 参数","必填":"可选"},{"参数":"--esn <key>","说明":"空字符串 Extra","必填":"可选"},{"参数":"--ez <key> <value>","说明":"布尔类型 Extra","必填":"可选"},{"参数":"--ei <key> <value>","说明":"整数类型 Extra","必填":"可选"},{"参数":"-W","说明":"等待 Activity 启动完成后返回","必填":"可选"}]',
    example_basic='adb shell am start -n com.android.settings/.Settings',
    example_adv='adb shell am start -a android.intent.action.VIEW -d "https://www.google.com"',
    os_type='通用',
    aliases='启动activity,am start,启动应用',
    tips='Activity 名可通过 dumpsys package <包名> 查看。组合 -W 可获取启动耗时。',
)
add(
    cmd_name='adb shell am startservice',
    name_cn='启动 Service',
    function_desc='启动一个 Android Service 组件',
    syntax='adb shell am startservice [选项] <Intent>',
    params_json='[{"参数":"-n <组件>","说明":"Service 组件名","必填":"必填"},{"参数":"-a <action>","说明":"Intent Action","必填":"可选"},{"参数":"-e <key> <value>","说明":"Extra 参数","必填":"可选"},{"参数":"--ei <key> <value>","说明":"整数 Extra","必填":"可选"}]',
    example_basic='adb shell am startservice -n com.example/.MyService',
    example_adv='adb shell am startservice -a com.example.ACTION_SYNC -e "key" "value"',
    os_type='通用',
    aliases='启动服务,am startservice,startservice',
    tips='Service 组件需要在 AndroidManifest.xml 中声明。使用 startservice 前先确认 Service 已导出或使用相同 UID。',
)
add(
    cmd_name='adb shell am broadcast',
    name_cn='发送广播',
    function_desc='发送一个全局广播 Intent，可携带各种类型的数据',
    syntax='adb shell am broadcast [选项] <Intent>',
    params_json='[{"参数":"-a <action>","说明":"Broadcast Action","必填":"必填"},{"参数":"-n <组件>","说明":"指定接收组件","必填":"可选"},{"参数":"--es <key> <value>","说明":"字符串 Extra","必填":"可选"},{"参数":"--ez <key> <value>","说明":"布尔 Extra","必填":"可选"},{"参数":"--ei <key> <value>","说明":"整数 Extra","必填":"可选"},{"参数":"--user <用户ID>","说明":"发送给指定用户","必填":"可选"}]',
    example_basic='adb shell am broadcast -a android.intent.action.BATTERY_LOW',
    example_adv='adb shell am broadcast -a android.intent.action.BOOT_COMPLETED',
    os_type='通用',
    aliases='发送广播,am broadcast,broadcast',
    tips='发送系统广播需要对应权限。发送自定义广播用于触发应用的 BroadcastReceiver。',
)
add(
    cmd_name='adb shell am force-stop',
    name_cn='强制停止应用',
    function_desc='强制停止指定包名的应用进程。无论应用在前台还是后台都会被终止',
    syntax='adb shell am force-stop <包名>',
    params_json='[{"参数":"包名","说明":"要强制停止的应用包名","必填":"必填"}]',
    example_basic='adb shell am force-stop com.example.app',
    example_adv='adb shell am force-stop com.android.settings',
    os_type='通用',
    aliases='强制停止,force-stop,杀死应用',
    tips='此命令不需要 root 权限。与 kill 不同，force-stop 会清除应用的所有状态，下次启动如同冷启动。',
)
add(
    cmd_name='adb shell am kill',
    name_cn='杀死后台进程',
    function_desc='杀掉指定包名的后台进程（但允许进程在前台运行）',
    syntax='adb shell am kill <包名>',
    params_json='[{"参数":"包名","说明":"要杀死的应用包名","必填":"必填"}]',
    example_basic='adb shell am kill com.example.app',
    example_adv='adb shell am kill com.android.systemui',
    os_type='通用',
    aliases='杀死进程,am kill,kill进程',
    tips='与 kill-all 一起使用清除后台进程。如果应用在前台则不会生效。',
)
add(
    cmd_name='adb shell am kill-all',
    name_cn='杀掉所有后台进程',
    function_desc='杀掉所有允许被杀死的后台应用进程',
    syntax='adb shell am kill-all',
    params_json='[]',
    example_basic='adb shell am kill-all',
    example_adv='adb shell am kill-all && echo "所有后台进程已清除"',
    os_type='通用',
    aliases='杀死全部,kill-all,清除后台',
    tips='不会影响前台应用和系统核心进程。可用于释放内存。',
)
add(
    cmd_name='adb shell am crash',
    name_cn='模拟应用崩溃',
    function_desc='让指定包名的应用强制崩溃并抛出异常，用于测试崩溃处理和上报功能',
    syntax='adb shell am crash <包名>',
    params_json='[{"参数":"包名","说明":"要模拟崩溃的应用包名","必填":"必填"}]',
    example_basic='adb shell am crash com.example.app',
    example_adv='adb shell am crash com.example.app && adb logcat -d | grep "FATAL"',
    os_type='通用',
    aliases='模拟崩溃,am crash,crash测试',
    tips='用于测试应用的崩溃报告和分析工具（如 Firebase Crashlytics）。应用会收到未处理异常的 ANR 对话框。',
)
add(
    cmd_name='adb shell am hang',
    name_cn='模拟 ANR',
    function_desc='让系统挂起，模拟应用无响应（ANR）的场景，用于测试 ANR 检测和上报',
    syntax='adb shell am hang',
    params_json='[]',
    example_basic='adb shell am hang',
    example_adv='adb shell am hang && sleep 5 && adb shell input keyevent KEYCODE_POWER',
    os_type='通用',
    aliases='模拟anr,am hang,anr测试',
    tips='执行后系统会进入挂起状态，可能需要按电源键或重启设备恢复。谨慎使用。',
)
add(
    cmd_name='adb shell am restart',
    name_cn='重启应用',
    function_desc='重启指定包名的应用（仅限已 root 设备或系统应用调试）',
    syntax='adb shell am restart <包名>',
    params_json='[{"参数":"包名","说明":"要重启的应用包名","必填":"必填"}]',
    example_basic='adb shell am restart com.example.app',
    example_adv='adb shell am restart com.android.systemui',
    os_type='通用',
    aliases='重启应用,am restart,重启',
    tips='常用于快速重启系统 UI。部分设备可能需要 root 权限。',
)
add(
    cmd_name='adb shell am monitor',
    name_cn='监控 Activity 启动',
    function_desc='监控所有 Activity 的启动事件，实时显示打开的 Activity 名称',
    syntax='adb shell am monitor [--gdb]',
    params_json='[{"参数":"--gdb","说明":"在 Activity 启动前暂停等待 GDB 连接","必填":"可选"}]',
    example_basic='adb shell am monitor',
    example_adv='adb shell am monitor | grep "com\\.example"',
    os_type='通用',
    aliases='监控activity,am monitor,activity监控',
    tips='输出格式：显示每个新启动的 Activity 的包名和 Activity 名。按 Ctrl+C 退出。',
)
add(
    cmd_name='adb shell am dumpheap',
    name_cn='导出 Heap 快照',
    function_desc='导出指定进程的 Java heap 快照（.hprof 文件），用于内存泄漏分析',
    syntax='adb shell am dumpheap [选项] <进程名|PID> <目标文件>',
    params_json='[{"参数":"进程名","说明":"要 dump 的进程名（包名）或 PID","必填":"必填"},{"参数":"目标文件","说明":"保存 hprof 文件的目标路径","必填":"必填"}]',
    example_basic='adb shell am dumpheap com.example.app /data/local/tmp/heap.hprof',
    example_adv='adb shell am dumpheap com.example.app /data/local/tmp/heap.hprof && adb pull /data/local/tmp/heap.hprof',
    os_type='通用',
    aliases='内存快照,dumpheap,heap,hprof',
    tips='需要先确认进程 PID（ps -A | grep 包名）。hprof 文件可用 Android Studio Profiler 或 MAT 分析。',
)
add(
    cmd_name='adb shell am profile',
    name_cn='性能采样分析',
    function_desc='对指定进程启动或停止性能采样分析（profiling），用于性能瓶颈分析',
    syntax='adb shell am profile <进程名> start <采样文件>\nadb shell am profile <进程名> stop',
    params_json='[{"参数":"进程名","说明":"目标进程包名","必填":"必填"},{"参数":"start <文件>","说明":"开始采样并输出到指定文件","必填":"可选"},{"参数":"stop","说明":"停止采样","必填":"可选"}]',
    example_basic='adb shell am profile com.example.app start /data/local/tmp/sample.trace',
    example_adv='adb shell am profile com.example.app start /data/local/tmp/sample.trace && sleep 10 && adb shell am profile com.example.app stop',
    os_type='通用',
    aliases='性能分析,profile,采样',
    tips='更推荐使用 systrace 或 Android Studio Profiler 做性能分析。采样文件可用 Android Studio 打开分析。',
)
add(
    cmd_name='adb shell am set-debug-app',
    name_cn='设置调试应用',
    function_desc='标记指定包名的应用为可调试，使其等待调试器连接',
    syntax='adb shell am set-debug-app [-w] [--persistent] <包名>',
    params_json='[{"参数":"-w","说明":"等待调试器连接后才启动应用","必填":"可选"},{"参数":"--persistent","说明":"持久化此设置（重启后仍然生效）","必填":"可选"},{"参数":"包名","说明":"要标记为调试的应用包名","必填":"必填"}]',
    example_basic='adb shell am set-debug-app -w com.example.app',
    example_adv='adb shell am set-debug-app --persistent com.example.app',
    os_type='通用',
    aliases='调试应用,set-debug-app,调试模式',
    tips='配合 Android Studio 使用。清除标记用 am clear-debug-app。',
)
add(
    cmd_name='adb shell am clear-debug-app',
    name_cn='清除调试应用标记',
    function_desc='清除通过 set-debug-app 设置的调试标记',
    syntax='adb shell am clear-debug-app <包名>',
    params_json='[{"参数":"包名","说明":"要清除调试标记的应用包名","必填":"必填"}]',
    example_basic='adb shell am clear-debug-app com.example.app',
    example_adv='adb shell am clear-debug-app com.example.app && echo "调试标记已清除"',
    os_type='通用',
    aliases='清除调试标记,clear-debug-app',
    tips='如果设置了 --persistent 标记，也需要用此命令清除。',
)
add(
    cmd_name='adb shell am instrument',
    name_cn='运行 Instrumentation 测试',
    function_desc='运行 Android Instrumentation 测试，用于自动化测试和覆盖率收集',
    syntax='adb shell am instrument [选项] <测试组件>',
    params_json='[{"参数":"-r","说明":"输出原始结果（便于解析）","必填":"可选"},{"参数":"-e <key> <value>","说明":"传入测试参数","必填":"可选"},{"参数":"-w","说明":"等待测试完成","必填":"可选"},{"参数":"--no-window-animation","说明":"禁用窗口动画","必填":"可选"},{"参数":"--user <用户ID>","说明":"指定测试用户","必填":"可选"}]',
    example_basic='adb shell am instrument -w com.example.test/androidx.test.runner.AndroidJUnitRunner',
    example_adv='adb shell am instrument -w -e coverage true -e coverageFile /data/local/tmp/coverage.ec com.example.test/androidx.test.runner.AndroidJUnitRunner',
    os_type='通用',
    aliases='测试,instrument,instrumentation测试',
    tips='最常用的是 AndroidJUnitRunner。使用 -e coverage true 生成覆盖率报告。',
)
add(
    cmd_name='adb shell am to-uri',
    name_cn='Intent 转 URI',
    function_desc='将给定的 Intent 转换为 URI 字符串格式',
    syntax='adb shell am to-uri <Intent>',
    params_json='[{"参数":"Intent","说明":"要转换的 Intent（与 start 格式相同）","必填":"必填"}]',
    example_basic='adb shell am to-uri -a android.intent.action.VIEW -d "https://example.com"',
    example_adv='adb shell am to-uri -n com.example/.MainActivity -e "key" "value"',
    os_type='通用',
    aliases='intent转uri,to-uri,intent转换',
    tips='输出可用于网页链接或 adb shell am start 的 Intent URI。',
)
add(
    cmd_name='adb shell am task',
    name_cn='任务管理',
    function_desc='查看和管理 Activity 任务栈信息',
    syntax='adb shell am task [子命令]',
    params_json='[{"参数":"list","说明":"列出当前所有任务栈","必填":"可选"},{"参数":"lock <taskID>","说明":"锁定指定任务","必填":"可选"},{"参数":"unlock","说明":"解锁任务","必填":"可选"}]',
    example_basic='adb shell am task list',
    example_adv='adb shell am task list | head -20',
    os_type='通用',
    aliases='任务管理,am task,任务栈',
    tips='配合 dumpsys activity activities 可以查看更详细的任务栈信息。',
)
add(
    cmd_name='adb shell am stack',
    name_cn='Activity 栈管理',
    function_desc='管理 Activity 显示栈（多窗口/分屏模式相关）',
    syntax='adb shell am stack <子命令>',
    params_json='[{"参数":"list","说明":"列出所有显示栈","必填":"可选"},{"参数":"move-task <taskID> <stackID>","说明":"将任务移动到指定栈","必填":"可选"},{"参数":"resize-stack <stackID> <左> <上> <右> <下>","说明":"调整栈尺寸","必填":"可选"},{"参数":"resize-docked-stack <左> <上> <右> <下>","说明":"调整分屏栈尺寸","必填":"可选"}]',
    example_basic='adb shell am stack list',
    example_adv='adb shell am stack resize-docked-stack 0 0 1000 2000',
    os_type='通用',
    aliases='显示栈,am stack,多窗口',
    tips='用于测试分屏和多窗口模式。不同 Android 版本支持程度不同。',
)

# ── 2.2 pm (Package Manager) ──

add(
    cmd_name='adb shell pm list packages',
    name_cn='列出已安装包',
    function_desc='列出设备上所有已安装的应用包名，支持多种过滤条件',
    syntax='adb shell pm list packages [选项] [过滤器]',
    params_json='[{"参数":"-f","说明":"显示 APK 文件路径","必填":"可选"},{"参数":"-d","说明":"只显示已禁用的应用","必填":"可选"},{"参数":"-e","说明":"只显示已启用的应用","必填":"可选"},{"参数":"-s","说明":"只显示系统应用","必填":"可选"},{"参数":"-3","说明":"只显示第三方应用","必填":"可选"},{"参数":"-i","说明":"显示安装来源","必填":"可选"},{"参数":"-u","说明":"包含卸载但保留数据的应用","必填":"可选"},{"参数":"--show-versions","说明":"显示版本号","必填":"可选"},{"参数":"<过滤器>","说明":"按关键词过滤包名（如包含"google"的包）","必填":"可选"}]',
    example_basic='adb shell pm list packages',
    example_adv='adb shell pm list packages -3 -f | grep com.example',
    os_type='通用',
    aliases='列出包,pm list,包列表,应用列表',
    tips='常用组合：pm list packages -3 只看第三方应用。pm list packages -s 只看系统应用。pipe grep 过滤关键词。',
)
add(
    cmd_name='adb shell pm list permissions',
    name_cn='列出权限',
    function_desc='列出系统定义的所有权限，支持按组和按标签过滤',
    syntax='adb shell pm list permissions [选项]',
    params_json='[{"参数":"-g","说明":"按权限组分组显示","必填":"可选"},{"参数":"-f","说明":"显示所有权限信息","必填":"可选"},{"参数":"-d","说明":"只显示危险权限","必填":"可选"},{"参数":"-u","说明":"只显示用户可见的权限","必填":"可选"}]',
    example_basic='adb shell pm list permissions -d',
    example_adv='adb shell pm list permissions -g | grep "android.permission.CAMERA"',
    os_type='通用',
    aliases='列出权限,pm list permissions,权限列表',
    tips='使用 -d 只列出危险权限（需要运行时授权的）。使用 -g 按组查看更方便。',
)
add(
    cmd_name='adb shell pm list features',
    name_cn='列出硬件功能',
    function_desc='列出设备支持的所有硬件和软件功能特性',
    syntax='adb shell pm list features',
    params_json='[]',
    example_basic='adb shell pm list features',
    example_adv='adb shell pm list features | grep "nfc"',
    os_type='通用',
    aliases='硬件功能,features,设备特性',
    tips='常用于检查设备是否支持 NFC、指纹、蓝牙 LE 等特性。',
)
add(
    cmd_name='adb shell pm list libraries',
    name_cn='列出系统库',
    function_desc='列出设备上可用的系统库（shared libraries）',
    syntax='adb shell pm list libraries',
    params_json='[]',
    example_basic='adb shell pm list libraries',
    example_adv='adb shell pm list libraries | grep "opengl"',
    os_type='通用',
    aliases='系统库,libraries,共享库',
    tips='应用可以通过 uses-library 在 Manifest 中声明需要的系统库。',
)
add(
    cmd_name='adb shell pm list users',
    name_cn='列出用户',
    function_desc='列出设备上的所有用户（多用户模式），显示用户 ID 和状态',
    syntax='adb shell pm list users',
    params_json='[]',
    example_basic='adb shell pm list users',
    example_adv='adb shell pm list users | grep "RUNNING"',
    os_type='通用',
    aliases='列出用户,pm list users,多用户',
    tips='Android 支持多用户（如访客模式、工作资料）。每个用户有独立的 ID 和应用数据。',
)
add(
    cmd_name='adb shell pm path',
    name_cn='查询 APK 路径',
    function_desc='查询指定包名的 APK 文件在设备上的安装路径',
    syntax='adb shell pm path <包名>',
    params_json='[{"参数":"包名","说明":"要查询的应用包名","必填":"必填"}]',
    example_basic='adb shell pm path com.android.chrome',
    example_adv='adb shell pm path com.example.app | cut -d: -f2',
    os_type='通用',
    aliases='apk路径,pm path,查询路径',
    tips='对于拆分 APK 会返回多条路径。路径可用于 adb pull 拉取 APK。',
)
add(
    cmd_name='adb shell pm dump',
    name_cn='Dump 包信息',
    function_desc='输出指定包名的详细信息，包括权限、Activity、Service、Provider 等组件声明',
    syntax='adb shell pm dump <包名>',
    params_json='[{"参数":"包名","说明":"要 dump 的应用包名","必填":"必填"}]',
    example_basic='adb shell pm dump com.android.settings',
    example_adv='adb shell pm dump com.example.app | grep -A 10 "Application -"',
    os_type='通用',
    aliases='包信息,dump,pm dump,应用详情',
    tips='输出内容非常丰富，建议 pipe 到 less 查看或 grep 过滤。常用于分析应用的 Manifest 配置。',
)
add(
    cmd_name='adb shell pm clear',
    name_cn='清除应用数据',
    function_desc='清除指定应用的所有用户数据（相当于在设置中"清除数据"）',
    syntax='adb shell pm clear <包名>',
    params_json='[{"参数":"包名","说明":"要清除数据的应用包名","必填":"必填"}]',
    example_basic='adb shell pm clear com.example.app',
    example_adv='adb shell pm clear com.android.settings && echo "设置数据已清除"',
    os_type='通用',
    aliases='清除数据,pm clear,clear数据',
    tips='此操作不可逆，慎用。清除后应用回到初始安装状态。重新打开后会像首次启动。',
)
add(
    cmd_name='adb shell pm enable',
    name_cn='启用应用',
    function_desc='启用已被禁用的应用或组件',
    syntax='adb shell pm enable <包名>[/组件名]',
    params_json='[{"参数":"包名/组件","说明":"要启用的包名或组件名","必填":"必填"}]',
    example_basic='adb shell pm enable com.example.app',
    example_adv='adb shell pm enable com.android.chrome/com.google.android.apps.chrome.Main',
    os_type='通用',
    aliases='启用应用,pm enable,启用',
    tips='禁用系统应用可能导致系统不稳定。启用后可能需要重启才能生效。',
)
add(
    cmd_name='adb shell pm disable',
    name_cn='禁用应用',
    function_desc='禁用指定包名的应用（用户禁用的应用不会显示在桌面）',
    syntax='adb shell pm disable <包名>[/组件名]',
    params_json='[{"参数":"包名/组件","说明":"要禁用的包名或组件","必填":"必填"}]',
    example_basic='adb shell pm disable com.example.app',
    example_adv='adb shell pm disable com.google.android.gms',
    os_type='通用',
    aliases='禁用应用,pm disable,禁用',
    tips='禁用系统应用前请确认其作用。某些系统应用被禁用后可能导致其他功能异常。用 pm enable 恢复。',
)
add(
    cmd_name='adb shell pm disable-user',
    name_cn='用户禁用应用',
    function_desc='以当前用户身份禁用应用（与普通用户通过设置禁用相同）',
    syntax='adb shell pm disable-user [--user <用户ID>] <包名>',
    params_json='[{"参数":"--user <用户ID>","说明":"指定用户（默认当前用户）","必填":"可选"},{"参数":"包名","说明":"要禁用的包名","必填":"必填"}]',
    example_basic='adb shell pm disable-user com.example.app',
    example_adv='adb shell pm disable-user --user 0 com.example.app',
    os_type='通用',
    aliases='用户禁用,pm disable-user',
    tips='与 pm disable 类似，但只能禁用而不会完全从系统中移除。多用户环境下可指定用户。',
)
add(
    cmd_name='adb shell pm grant',
    name_cn='授予运行时权限',
    function_desc='向应用授予指定的运行时权限（无需用户交互）',
    syntax='adb shell pm grant <包名> <权限名>',
    params_json='[{"参数":"包名","说明":"要授予权限的应用包名","必填":"必填"},{"参数":"权限名","说明":"要授予的完整权限名，如 android.permission.CAMERA","必填":"必填"}]',
    example_basic='adb shell pm grant com.example.app android.permission.CAMERA',
    example_adv='adb shell pm grant com.example.app android.permission.ACCESS_FINE_LOCATION',
    os_type='通用',
    aliases='授予权限,pm grant,grant,权限授予',
    tips='仅适用于运行时权限（dangerous 级别）。targetSdkVersion 较高的应用可能需要先安装再授权。',
)
add(
    cmd_name='adb shell pm revoke',
    name_cn='撤销运行时权限',
    function_desc='撤销已授予应用的运行时权限',
    syntax='adb shell pm revoke <包名> <权限名>',
    params_json='[{"参数":"包名","说明":"要撤销权限的应用包名","必填":"必填"},{"参数":"权限名","说明":"要撤销的完整权限名","必填":"必填"}]',
    example_basic='adb shell pm revoke com.example.app android.permission.CAMERA',
    example_adv='adb shell pm revoke com.example.app android.permission.ACCESS_FINE_LOCATION',
    os_type='通用',
    aliases='撤销权限,pm revoke,revoke',
    tips='撤销后应用再次请求权限时会弹出系统对话框。',
)
add(
    cmd_name='adb shell pm reset-permissions',
    name_cn='重置应用权限',
    function_desc='将指定应用的所有运行时权限重置为默认状态（撤销所有已授予的权限）',
    syntax='adb shell pm reset-permissions [-p <包名>]',
    params_json='[{"参数":"-p <包名>","说明":"要重置权限的包名（可选），不传则重置所有应用","必填":"可选"}]',
    example_basic='adb shell pm reset-permissions -p com.example.app',
    example_adv='adb shell pm reset-permissions && echo "所有应用权限已重置"',
    os_type='通用',
    aliases='重置权限,pm reset-permissions,权限重置',
    tips='不指定包名会重置所有应用的运行时权限状态。',
)
add(
    cmd_name='adb shell pm set-install-location',
    name_cn='设置安装位置',
    function_desc='设置 APK 的默认安装位置',
    syntax='adb shell pm set-install-location [0|1|2]',
    params_json='[{"参数":"0","说明":"自动选择（系统决定）","必填":"可选"},{"参数":"1","说明":"优先安装到内部存储","必填":"可选"},{"参数":"2","说明":"优先安装到外部存储（SD卡）","必填":"可选"}]',
    example_basic='adb shell pm set-install-location 2',
    example_adv='adb shell pm set-install-location 0',
    os_type='通用',
    aliases='安装位置,set-install-location',
    tips='现代 Android 版本不再推荐外部存储。此设置在部分设备上可能无效。',
)
add(
    cmd_name='adb shell pm get-install-location',
    name_cn='查看安装位置设置',
    function_desc='查看当前 APK 默认安装位置设置',
    syntax='adb shell pm get-install-location',
    params_json='[]',
    example_basic='adb shell pm get-install-location',
    example_adv='adb shell pm get-install-location | grep -o "[0-2]"',
    os_type='通用',
    aliases='查看安装位置,get-install-location',
    tips='返回值：0=自动 1=内部存储 2=外部存储。',
)
add(
    cmd_name='adb shell pm set-home-activity',
    name_cn='设置默认桌面',
    function_desc='设置默认的桌面启动器（Launcher）应用',
    syntax='adb shell pm set-home-activity <包名/Activity名>',
    params_json='[{"参数":"包名/Activity名","说明":"要设置为默认桌面的组件名","必填":"必填"}]',
    example_basic='adb shell pm set-home-activity com.example.launcher/.MainActivity',
    example_adv='adb shell pm set-home-activity com.google.android.apps.nexuslauncher/.NexusLauncherActivity',
    os_type='通用',
    aliases='设置桌面,set-home-activity,默认桌面',
    tips='设置后立即生效。如果指定的 Activity 不是合法的 Launcher，可能会无法操作桌面。',
)
add(
    cmd_name='adb shell pm trim-caches',
    name_cn='清理缓存',
    function_desc='清理所有应用的缓存文件，释放存储空间',
    syntax='adb shell pm trim-caches <目标大小MB>',
    params_json='[{"参数":"目标大小MB","说明":"欲达到的缓存大小目标值（MB）","必填":"必填"}]',
    example_basic='adb shell pm trim-caches 10',
    example_adv='adb shell pm trim-caches 500',
    os_type='通用',
    aliases='清理缓存,trim-caches,缓存清理',
    tips='告诉系统将缓存降到指定大小以下。设为较大值则不清理。设为 0 可尽可能多地清理缓存。',
)

# ── 2.3 dumpsys ──

add(
    cmd_name='adb shell dumpsys',
    name_cn='系统诊断信息',
    function_desc='输出 Android 系统服务的诊断信息，是 Android 调试最强大的命令之一',
    syntax='adb shell dumpsys [<服务名>] [<参数>]',
    params_json='[{"参数":"服务名","说明":"指定要 dump 的系统服务名（如 battery, meminfo, wifi），不传则输出所有服务列表","必填":"可选"},{"参数":"-l","说明":"列出所有支持的 dumpsys 服务名","必填":"可选"}]',
    example_basic='adb shell dumpsys battery',
    example_adv='adb shell dumpsys -l | grep "service"',
    os_type='通用',
    aliases='诊断,dumpsys,系统信息,服务信息',
    tips='dumpsys 的输出通常很长，建议 pipe 到 grep 或 less。先运行 dumpsys -l 查看所有可用的服务。',
)
add(
    cmd_name='adb shell dumpsys battery',
    name_cn='电池信息',
    function_desc='查看电池状态、电量、温度、电压、充电状态等详细信息',
    syntax='adb shell dumpsys battery',
    params_json='[]',
    example_basic='adb shell dumpsys battery',
    example_adv='adb shell dumpsys battery | grep -E "level|temperature|status"',
    os_type='通用',
    aliases='电池,dumpsys battery,电池信息',
    tips='可修改电池状态用于测试：dumpsys battery set level 50、dumpsys battery set status 2。用 dumpsys battery reset 恢复。',
)
add(
    cmd_name='adb shell dumpsys meminfo',
    name_cn='内存信息',
    function_desc='查看系统或指定应用的内存使用情况（PSS、Private Dirty、Heap 等）',
    syntax='adb shell dumpsys meminfo [<包名|PID>]',
    params_json='[{"参数":"包名|PID","说明":"指定进程（可选），不传则显示全局内存概览","必填":"可选"}]',
    example_basic='adb shell dumpsys meminfo',
    example_adv='adb shell dumpsys meminfo com.example.app | grep -E "PSS|Heap"',
    os_type='通用',
    aliases='内存,dumpsys meminfo,内存分析',
    tips='查看指定应用内存：dumpsys meminfo <包名>。重点关注 Total PSS 列。',
)
add(
    cmd_name='adb shell dumpsys cpuinfo',
    name_cn='CPU 信息',
    function_desc='查看系统 CPU 使用情况和各进程的 CPU 占用率',
    syntax='adb shell dumpsys cpuinfo',
    params_json='[]',
    example_basic='adb shell dumpsys cpuinfo',
    example_adv='adb shell dumpsys cpuinfo | head -20',
    os_type='通用',
    aliases='cpu,dumpsys cpuinfo,cpu使用率',
    tips='显示各进程的 CPU 占用百分比。用于定位高 CPU 占用的应用。',
)
add(
    cmd_name='adb shell dumpsys diskstats',
    name_cn='磁盘统计',
    function_desc='查看设备存储空间的使用统计和应用占用的存储空间',
    syntax='adb shell dumpsys diskstats',
    params_json='[]',
    example_basic='adb shell dumpsys diskstats',
    example_adv='adb shell dumpsys diskstats | grep "App Size"',
    os_type='通用',
    aliases='磁盘,dumpsys diskstats,存储空间',
    tips='显示每个应用的缓存、数据、APK 大小。可用于找出占用空间最大的应用。',
)
add(
    cmd_name='adb shell dumpsys wifi',
    name_cn='WiFi 信息',
    function_desc='查看 WiFi 连接状态、信号强度、IP 地址、扫描结果等详细网络信息',
    syntax='adb shell dumpsys wifi',
    params_json='[]',
    example_basic='adb shell dumpsys wifi',
    example_adv='adb shell dumpsys wifi | grep -A 20 "mNetworkInfo"',
    os_type='通用',
    aliases='wifi,dumpsys wifi,无线网络',
    tips='搜索 "mWifiInfo" 查看当前连接详情。搜索 "mScanResult" 查看附近的 WiFi 列表。',
)
add(
    cmd_name='adb shell dumpsys telephony',
    name_cn='电话/蜂窝信息',
    function_desc='查看蜂窝网络状态、信号强度、网络类型、IMEI 等电话功能信息',
    syntax='adb shell dumpsys telephony',
    params_json='[]',
    example_basic='adb shell dumpsys telephony',
    example_adv='adb shell dumpsys telephony | grep -E "mSignalStrength|NetworkType"',
    os_type='通用',
    aliases='电话,dumpsys telephony,蜂窝网络',
    tips='查看信号强度和网络类型时 grep 关键字段。部分信息需要 READ_PHONE_STATE 权限。',
)
add(
    cmd_name='adb shell dumpsys activity',
    name_cn='Activity 管理器信息',
    function_desc='查看 Activity 管理器的详细状态，包括 Activity 栈、任务、进程、广播等',
    syntax='adb shell dumpsys activity [选项]',
    params_json='[{"参数":"activities","说明":"只显示 Activity 栈信息","必填":"可选"},{"参数":"processes","说明":"只显示进程信息","必填":"可选"},{"参数":"services","说明":"只显示 Service 信息","必填":"可选"},{"参数":"broadcasts","说明":"只显示 Broadcast 信息","必填":"可选"},{"参数":"intents","说明":"只显示 Intent 信息","必填":"可选"},{"参数":"top","说明":"只显示前台 Activity","必填":"可选"}]',
    example_basic='adb shell dumpsys activity',
    example_adv='adb shell dumpsys activity top | grep ACTIVITY',
    os_type='通用',
    aliases='activity,dumpsys activity,活动管理器',
    tips='最常用的是 dumpsys activity top（查看当前前台 Activity）和 dumpsys activity activities（查看完整任务栈）。',
)
add(
    cmd_name='adb shell dumpsys package',
    name_cn='包管理器信息',
    function_desc='查看包管理器的详细状态，包括所有安装应用、权限、SharedUser 等信息',
    syntax='adb shell dumpsys package [<包名>]',
    params_json='[{"参数":"包名","说明":"指定应用包名（可选），只查看该应用的详情","必填":"可选"}]',
    example_basic='adb shell dumpsys package',
    example_adv='adb shell dumpsys package com.example.app | grep -E "versionName|firstInstallTime"',
    os_type='通用',
    aliases='包,dumpsys package,安装信息',
    tips='不指定包名会输出巨量信息。始终建议指定包名或 pipe 到 less。',
)
add(
    cmd_name='adb shell dumpsys window',
    name_cn='窗口管理器信息',
    function_desc='查看窗口管理器的状态，包括窗口层次、焦点窗口、屏幕尺寸、密度等',
    syntax='adb shell dumpsys window [选项]',
    params_json='[{"参数":"policy","说明":"显示窗口策略信息","必填":"可选"},{"参数":"windows","说明":"显示所有窗口列表","必填":"可选"},{"参数":"displays","说明":"显示显示屏信息","必填":"可选"},{"参数":"tokens","说明":"显示窗口令牌","必填":"可选"}]',
    example_basic='adb shell dumpsys window displays',
    example_adv='adb shell dumpsys window | grep -E "mCurrentFocus|mFocusedApp"',
    os_type='通用',
    aliases='窗口,dumpsys window,窗口信息',
    tips='mCurrentFocus 显示当前获得焦点的窗口（前台应用）。mFocusedApp 显示焦点应用。',
)
add(
    cmd_name='adb shell dumpsys input',
    name_cn='输入系统信息',
    function_desc='查看输入系统的状态，包括输入设备、按键映射、触摸屏信息等',
    syntax='adb shell dumpsys input',
    params_json='[]',
    example_basic='adb shell dumpsys input',
    example_adv='adb shell dumpsys input | grep -E "Device|Keyboard"',
    os_type='通用',
    aliases='输入,dumpsys input,输入设备',
    tips='查看所有输入设备列表（触摸屏、键盘、鼠标等）。调试外设输入问题非常有用。',
)
add(
    cmd_name='adb shell dumpsys power',
    name_cn='电源管理信息',
    function_desc='查看电源管理状态，包括唤醒锁（Wake Lock）、屏幕状态、电池充电状态等',
    syntax='adb shell dumpsys power',
    params_json='[]',
    example_basic='adb shell dumpsys power',
    example_adv='adb shell dumpsys power | grep -E "mWakefulness|mScreenOn|Locks"',
    os_type='通用',
    aliases='电源,dumpsys power,电源管理',
    tips='查看 mWakefulness 了解设备是否允许休眠。查看 "Wake Locks" 了解哪些应用阻止休眠。',
)
add(
    cmd_name='adb shell dumpsys alarm',
    name_cn='闹钟/定时器信息',
    function_desc='查看系统所有已注册的闹钟（Alarm），包括应用设置的定时任务',
    syntax='adb shell dumpsys alarm',
    params_json='[]',
    example_basic='adb shell dumpsys alarm',
    example_adv='adb shell dumpsys alarm | grep "com\\.example"',
    os_type='通用',
    aliases='闹钟,dumpsys alarm,定时器',
    tips='查看哪些应用设置了唤醒闹钟。列出所有 pending alarm 及其触发时间。',
)
add(
    cmd_name='adb shell dumpsys notification',
    name_cn='通知管理信息',
    function_desc='查看通知管理器的状态，包括所有活动通知和通知渠道配置',
    syntax='adb shell dumpsys notification [--noredact]',
    params_json='[{"参数":"--noredact","说明":"不脱敏显示通知内容（显示完整文本）","必填":"可选"}]',
    example_basic='adb shell dumpsys notification',
    example_adv='adb shell dumpsys notification --noredact | grep "com\\.example"',
    os_type='通用',
    aliases='通知,dumpsys notification,通知信息',
    tips='查看当前显示的所有通知及通知内容。--noredact 可显示完整通知文本。',
)
add(
    cmd_name='adb shell dumpsys connectivity',
    name_cn='网络连接信息',
    function_desc='查看网络连接管理器的状态，包括网络类型、传输能力、网络评分等',
    syntax='adb shell dumpsys connectivity',
    params_json='[]',
    example_basic='adb shell dumpsys connectivity',
    example_adv='adb shell dumpsys connectivity | grep -E "NetworkAgentInfo|Capabilities"',
    os_type='通用',
    aliases='网络,dumpsys connectivity,连接信息',
    tips='查看当前活动网络类型（WiFi/移动数据）和网络能力（是否限速等）。',
)
add(
    cmd_name='adb shell dumpsys netstats',
    name_cn='网络流量统计',
    function_desc='查看网络接口的流量统计数据（上传/下载字节数）',
    syntax='adb shell dumpsys netstats',
    params_json='[]',
    example_basic='adb shell dumpsys netstats',
    example_adv='adb shell dumpsys netstats | grep "Total"',
    os_type='通用',
    aliases='流量,dumpsys netstats,网络统计',
    tips='显示各网络接口的累计流量。可用于排查应用的网络数据使用情况。',
)
add(
    cmd_name='adb shell dumpsys media',
    name_cn='媒体服务信息',
    function_desc='查看媒体服务（MediaSession、MediaRouter 等）的状态',
    syntax='adb shell dumpsys media',
    params_json='[]',
    example_basic='adb shell dumpsys media',
    example_adv='adb shell dumpsys media | grep -E "MediaSession|PlaybackState"',
    os_type='通用',
    aliases='媒体,dumpsys media,媒体服务',
    tips='查看当前媒体播放会话的状态。可用于调试音频焦点和媒体控制。',
)
add(
    cmd_name='adb shell dumpsys audio',
    name_cn='音频服务信息',
    function_desc='查看音频系统的状态，包括音量、音频设备、音频策略等',
    syntax='adb shell dumpsys audio',
    params_json='[]',
    example_basic='adb shell dumpsys audio',
    example_adv='adb shell dumpsys audio | grep -E "volume|Device"',
    os_type='通用',
    aliases='音频,dumpsys audio,声音',
    tips='查看各音频输出流的当前音量值和设备路由信息。',
)
add(
    cmd_name='adb shell dumpsys display',
    name_cn='显示服务信息',
    function_desc='查看显示管理器的状态，包括屏幕参数、刷新率、显示亮度等',
    syntax='adb shell dumpsys display',
    params_json='[]',
    example_basic='adb shell dumpsys display',
    example_adv='adb shell dumpsys display | grep -E "mBaseDisplayInfo|refreshRate"',
    os_type='通用',
    aliases='显示,dumpsys display,屏幕信息',
    tips='查看屏幕分辨率和刷新率。查看当前亮度设置。',
)
add(
    cmd_name='adb shell dumpsys usb',
    name_cn='USB 信息',
    function_desc='查看 USB 管理器状态，包括 USB 模式和连接的 USB 设备',
    syntax='adb shell dumpsys usb',
    params_json='[]',
    example_basic='adb shell dumpsys usb',
    example_adv='adb shell dumpsys usb | grep -E "mConnected|mCurrentFunctions"',
    os_type='通用',
    aliases='usb,dumpsys usb,usb状态',
    tips='查看当前 USB 功能模式（MTP、RNDIS、充电等）。',
)
add(
    cmd_name='adb shell dumpsys bluetooth',
    name_cn='蓝牙信息',
    function_desc='查看蓝牙服务的状态，包括连接设备、蓝牙开关状态等',
    syntax='adb shell dumpsys bluetooth',
    params_json='[]',
    example_basic='adb shell dumpsys bluetooth',
    example_adv='adb shell dumpsys bluetooth | grep -E "state|connected"',
    os_type='通用',
    aliases='蓝牙,dumpsys bluetooth,蓝牙信息',
    tips='查看蓝牙开启状态和已配对/已连接设备的列表。',
)
add(
    cmd_name='adb shell dumpsys location',
    name_cn='定位服务信息',
    function_desc='查看定位服务的状态，包括定位模式、最近定位、使用的定位 Provider 等',
    syntax='adb shell dumpsys location',
    params_json='[]',
    example_basic='adb shell dumpsys location',
    example_adv='adb shell dumpsys location | grep -E "LocationProvider|mLastLocation"',
    os_type='通用',
    aliases='定位,dumpsys location,位置信息',
    tips='查看最近定位结果和使用的定位提供者（GPS/Network/Fused）。',
)
add(
    cmd_name='adb shell dumpsys sensors',
    name_cn='传感器信息',
    function_desc='查看设备所有传感器的列表和当前状态',
    syntax='adb shell dumpsys sensors',
    params_json='[]',
    example_basic='adb shell dumpsys sensors',
    example_adv='adb shell dumpsys sensors | grep -E "Accelerometer|Gyroscope"',
    os_type='通用',
    aliases='传感器,dumpsys sensors,传感器列表',
    tips='查看设备支持的所有传感器类型及其参数。',
)
add(
    cmd_name='adb shell dumpsys graphicsstats',
    name_cn='图形渲染统计',
    function_desc='查看应用的图形渲染性能统计（帧率、掉帧等）',
    syntax='adb shell dumpsys graphicsstats',
    params_json='[]',
    example_basic='adb shell dumpsys graphicsstats',
    example_adv='adb shell dumpsys graphicsstats | grep "com\\.example" -A 30',
    os_type='通用',
    aliases='图形,dumpsys graphicsstats,渲染性能',
    tips='查看各应用的帧渲染直方图。掉帧严重的应用会在统计中显示大量 >16ms 的帧。',
)
add(
    cmd_name='adb shell dumpsys procstats',
    name_cn='进程统计',
    function_desc='查看进程的内存使用统计，长时间统计各进程的内存压力情况',
    syntax='adb shell dumpsys procstats [--hours <N>]',
    params_json='[{"参数":"--hours <N>","说明":"显示最近 N 小时的统计（默认 3h）","必填":"可选"}]',
    example_basic='adb shell dumpsys procstats',
    example_adv='adb shell dumpsys procstats --hours 24 | head -50',
    os_type='通用',
    aliases='进程统计,dumpsys procstats,内存统计',
    tips='显示各进程在不同内存状态（Normal/Moderate/Low/Critical）下的运行时间。',
)
add(
    cmd_name='adb shell dumpsys batterystats',
    name_cn='电池使用统计',
    function_desc='查看详细的电池使用统计，包括各应用耗电情况、唤醒次数、网络活动等',
    syntax='adb shell dumpsys batterystats [<包名>] [--charged]',
    params_json='[{"参数":"<包名>","说明":"指定应用的耗电详情","必填":"可选"},{"参数":"--charged","说明":"上次充满电以来的统计","必填":"可选"}]',
    example_basic='adb shell dumpsys batterystats',
    example_adv='adb shell dumpsys batterystats --charged | grep "com\\.example"',
    os_type='通用',
    aliases='电池统计,batterystats,耗电分析',
    tips='配合 batterystats --charged 重置统计后使用测试。输出包含各应用的估算耗电 mAh。',
)
add(
    cmd_name='adb shell dumpsys netpolicy',
    name_cn='网络策略信息',
    function_desc='查看网络策略管理器状态，包括后台数据限制、流量节省等策略',
    syntax='adb shell dumpsys netpolicy',
    params_json='[]',
    example_basic='adb shell dumpsys netpolicy',
    example_adv='adb shell dumpsys netpolicy | grep "restrict"',
    os_type='通用',
    aliases='网络策略,dumpsys netpolicy,流量策略',
    tips='查看哪些应用被限制后台数据和流量节省模式的状态。',
)
add(
    cmd_name='adb shell dumpsys jobscheduler',
    name_cn='任务调度器信息',
    function_desc='查看 JobScheduler 调度的所有定时任务的状态',
    syntax='adb shell dumpsys jobscheduler',
    params_json='[]',
    example_basic='adb shell dumpsys jobscheduler',
    example_adv='adb shell dumpsys jobscheduler | grep "com\\.example" -A 15',
    os_type='通用',
    aliases='任务调度,dumpsys jobscheduler,job',
    tips='查看所有已调度的 Job 及其下次运行时间。用于调试后台任务未按时执行的问题。',
)
add(
    cmd_name='adb shell dumpsys wallpaper',
    name_cn='壁纸信息',
    function_desc='查看壁纸管理器的状态',
    syntax='adb shell dumpsys wallpaper',
    params_json='[]',
    example_basic='adb shell dumpsys wallpaper',
    example_adv='adb shell dumpsys wallpaper | grep -E "mWallpaperComponent|mWidth"',
    os_type='通用',
    aliases='壁纸,dumpsys wallpaper,壁纸信息',
    tips='查看当前壁纸组件和壁纸尺寸信息。',
)
add(
    cmd_name='adb shell dumpsys user',
    name_cn='用户管理信息',
    function_desc='查看用户管理器的状态，包括所有用户和用户切换信息',
    syntax='adb shell dumpsys user',
    params_json='[]',
    example_basic='adb shell dumpsys user',
    example_adv='adb shell dumpsys user | grep "UserInfo"',
    os_type='通用',
    aliases='用户,dumpsys user,用户管理',
    tips='查看设备上的所有用户（多用户模式）及其状态和类型（系统/管理员/访客）。',
)

# ── 2.4 input 命令 ──

add(
    cmd_name='adb shell input',
    name_cn='模拟输入',
    function_desc='模拟各种输入事件：按键、触摸、滑动、文本输入等',
    syntax='adb shell input <子命令> [参数]',
    params_json='[{"参数":"text <字符串>","说明":"输入指定文本","必填":"可选"},{"参数":"keyevent <键码>","说明":"发送按键事件","必填":"可选"},{"参数":"tap <x> <y>","说明":"点击指定坐标","必填":"可选"},{"参数":"swipe <x1> <y1> <x2> <y2> [时长ms]","说明":"从(x1,y1)滑动到(x2,y2)","必填":"可选"},{"参数":"press","说明":"模拟按下","必填":"可选"},{"参数":"roll <dx> <dy>","说明":"模拟轨迹球滚动","必填":"可选"}]',
    example_basic='adb shell input keyevent KEYCODE_HOME',
    example_adv='adb shell input tap 500 1000 && sleep 1 && adb shell input text "hello"',
    os_type='通用',
    aliases='模拟输入,input,触控模拟',
    tips='使用 adb shell wm size 查看屏幕分辨率以确定点击坐标。文本输入需确保焦点在文本框中。',
)
add(
    cmd_name='adb shell input keyevent',
    name_cn='发送按键事件',
    function_desc='模拟发送 Android 按键事件，如 Home、Back、音量键等',
    syntax='adb shell input keyevent <键码1> [<键码2> ...]',
    params_json='[{"参数":"键码","说明":"按键码（数字或 KEYCODE_XXX 名称），多个按键可同时发送","必填":"必填"}]',
    example_basic='adb shell input keyevent KEYCODE_HOME',
    example_adv='adb shell input keyevent KEYCODE_VOLUME_DOWN KEYCODE_VOLUME_DOWN',
    os_type='通用',
    aliases='按键,input keyevent,模拟按键',
    tips='常用键码：KEYCODE_HOME=3, KEYCODE_BACK=4, KEYCODE_VOLUME_UP=24, KEYCODE_VOLUME_DOWN=25, KEYCODE_POWER=26, KEYCODE_MENU=82, KEYCODE_ENTER=66。',
)
add(
    cmd_name='adb shell input tap',
    name_cn='模拟点击',
    function_desc='模拟在屏幕指定坐标 (x, y) 处进行一次触摸点击',
    syntax='adb shell input tap <x> <y>',
    params_json='[{"参数":"x","说明":"点击位置的 X 坐标（像素）","必填":"必填"},{"参数":"y","说明":"点击位置的 Y 坐标（像素）","必填":"必填"}]',
    example_basic='adb shell input tap 540 960',
    example_adv='adb shell input tap 100 200 && sleep 0.5 && adb shell input tap 300 400',
    os_type='通用',
    aliases='点击,input tap,模拟点击',
    tips='坐标原点在左上角。使用 "开发者选项" -> "指针位置" 可显示实时坐标。',
)
add(
    cmd_name='adb shell input swipe',
    name_cn='模拟滑动',
    function_desc='模拟从起点到终点的触摸滑动操作，可指定滑动时长',
    syntax='adb shell input swipe <x1> <y1> <x2> <y2> [时长ms]',
    params_json='[{"参数":"x1 y1","说明":"起始坐标","必填":"必填"},{"参数":"x2 y2","说明":"终点坐标","必填":"必填"},{"参数":"时长ms","说明":"滑动持续时间（毫秒），默认不设置则瞬间移动","必填":"可选"}]',
    example_basic='adb shell input swipe 500 1500 500 500',
    example_adv='adb shell input swipe 500 1500 500 500 1000',
    os_type='通用',
    aliases='滑动,input swipe,模拟滑动',
    tips='长滑动用于下拉刷新或翻页。短滑动可用于拖拽。添加时长参数可实现慢速滑动。',
)
add(
    cmd_name='adb shell input text',
    name_cn='输入文本',
    function_desc='在焦点所在的文本框中输入指定文本内容（不支持中文）',
    syntax='adb shell input text <文本>',
    params_json='[{"参数":"文本","说明":"要输入的文本（仅支持 ASCII 字符，空格用 %s 代替）","必填":"必填"}]',
    example_basic='adb shell input text "hello world"',
    example_adv='adb shell input text "test%s123%stest"',
    os_type='通用',
    aliases='文本输入,input text,输入文字',
    tips='空格需要用 %s 替代。特殊字符可能需要 URL 编码。中文输入建议使用 adb shell am broadcast 发送剪贴板内容。',
)

# ── 2.5 wm (Window Manager) ──

add(
    cmd_name='adb shell wm size',
    name_cn='查看/设置屏幕分辨率',
    function_desc='查看或修改模拟器的屏幕分辨率。修改后无需重启立即生效',
    syntax='adb shell wm size [<宽>x<高>]',
    params_json='[{"参数":"宽x高","说明":"要设置的分辨率（如 1080x1920），不传则显示当前分辨率","必填":"可选"}]',
    example_basic='adb shell wm size',
    example_adv='adb shell wm size 1080x1920 && adb shell wm density 420',
    os_type='通用',
    aliases='分辨率,wm size,屏幕尺寸',
    tips='修改分辨率可用于测试不同屏幕尺寸的适配。使用 wm size reset 恢复原始分辨率。主要用于模拟器。',
)
add(
    cmd_name='adb shell wm density',
    name_cn='查看/设置屏幕密度',
    function_desc='查看或修改屏幕密度（DPI）值，修改后立即生效',
    syntax='adb shell wm density [<DPI值>]',
    params_json='[{"参数":"DPI值","说明":"要设置的密度值（如 420），不传则显示当前 DPI","必填":"可选"}]',
    example_basic='adb shell wm density',
    example_adv='adb shell wm density 320',
    os_type='通用',
    aliases='屏幕密度,wm density,dpi',
    tips='修改 DPI 可用于测试不同密度的 UI 适配或让界面显示更多内容。使用 wm density reset 恢复。',
)
add(
    cmd_name='adb shell wm overscan',
    name_cn='设置屏幕过扫描',
    function_desc='调整屏幕显示区域的边距（裁剪/扩展显示区域），四个方向独立设置',
    syntax='adb shell wm overscan <左,上,右,下>',
    params_json='[{"参数":"左,上,右,下","说明":"四个方向的边距像素值，正数裁剪，负数扩展","必填":"必填"}]',
    example_basic='adb shell wm overscan 0,50,0,0',
    example_adv='adb shell wm overscan 100,0,100,0',
    os_type='通用',
    aliases='过扫描,wm overscan,屏幕裁剪',
    tips='常用于模拟器隐藏或模拟屏幕凹口（notch）。使用 wm overscan 0,0,0,0 恢复。',
)
add(
    cmd_name='adb shell wm scaling',
    name_cn='设置缩放模式',
    function_desc='设置应用的兼容缩放模式',
    syntax='adb shell wm scaling [off|auto]',
    params_json='[{"参数":"off","说明":"关闭自动缩放","必填":"可选"},{"参数":"auto","说明":"自动缩放","必填":"可选"}]',
    example_basic='adb shell wm scaling off',
    example_adv='adb shell wm scaling auto',
    os_type='通用',
    aliases='缩放,wm scaling,缩放模式',
    tips='用于测试应用的屏幕兼容性。',
)
add(
    cmd_name='adb shell wm dismiss-keyguard',
    name_cn='解除屏幕锁定',
    function_desc='解除设备锁屏（安全锁除外），常用于自动化测试',
    syntax='adb shell wm dismiss-keyguard',
    params_json='[]',
    example_basic='adb shell wm dismiss-keyguard',
    example_adv='adb shell wm dismiss-keyguard && adb shell input keyevent KEYCODE_HOME',
    os_type='通用',
    aliases='解锁,wm dismiss-keyguard,解除锁屏',
    tips='只能解除无安全锁的锁屏（如滑动解锁）。密码/PIN/图案锁无法通过此命令解除。',
)

# ── 2.6 settings 命令 ──

add(
    cmd_name='adb shell settings',
    name_cn='管理系统设置',
    function_desc='查看、修改 Android 系统设置。支持 global/system/secure 三种命名空间',
    syntax='adb shell settings <子命令> [参数]',
    params_json='[{"参数":"list <命名空间>","说明":"列出指定命名空间的所有设置项","必填":"可选"},{"参数":"get <命名空间> <键>","说明":"获取指定设置项的值","必填":"可选"},{"参数":"put <命名空间> <键> <值>","说明":"设置指定项的值","必填":"可选"},{"参数":"delete <命名空间> <键>","说明":"删除指定设置项","必填":"可选"},{"参数":"命名空间","说明":"global（全局）/ system（系统）/ secure（安全）","必填":"必填"}]',
    example_basic='adb shell settings get global airplane_mode_on',
    example_adv='adb shell settings put global airplane_mode_on 1',
    os_type='通用',
    aliases='设置,settings,系统设置',
    tips='修改安全设置（secure）可能需要 root 权限。修改 global 和 system 通常不需要。',
)
add(
    cmd_name='adb shell settings list',
    name_cn='列出所有设置项',
    function_desc='列出指定命名空间下的所有设置键值对，支持 grep 过滤',
    syntax='adb shell settings list <global|system|secure>',
    params_json='[{"参数":"global","说明":"列出所有全局设置","必填":"必填"},{"参数":"system","说明":"列出所有系统设置","必填":"必填"},{"参数":"secure","说明":"列出所有安全设置","必填":"必填"}]',
    example_basic='adb shell settings list system',
    example_adv='adb shell settings list secure | grep "location"',
    os_type='通用',
    aliases='列出设置,settings list,设置列表',
    tips='每个命名空间下有数百个设置项。用 grep 过滤关键词查找目标设置。',
)
add(
    cmd_name='adb shell settings get',
    name_cn='获取设置值',
    function_desc='获取指定命名空间下指定设置项的当前值',
    syntax='adb shell settings get <global|system|secure> <键名>',
    params_json='[{"参数":"命名空间","说明":"global / system / secure","必填":"必填"},{"参数":"键名","说明":"设置项的键名","必填":"必填"}]',
    example_basic='adb shell settings get global airplane_mode_on',
    example_adv='adb shell settings get secure android_id',
    os_type='通用',
    aliases='获取设置,settings get,查询设置',
    tips='常用设置：global.airplane_mode_on（飞行模式）、system.screen_brightness（屏幕亮度）、secure.android_id（设备ID）。',
)
add(
    cmd_name='adb shell settings put',
    name_cn='修改设置值',
    function_desc='修改指定命名空间下的设置项的值（立即生效）',
    syntax='adb shell settings put <global|system|secure> <键名> <值>',
    params_json='[{"参数":"命名空间","说明":"global / system / secure","必填":"必填"},{"参数":"键名","说明":"设置项的键名","必填":"必填"},{"参数":"值","说明":"要设置的值（字符串或数字）","必填":"必填"}]',
    example_basic='adb shell settings put global airplane_mode_on 1',
    example_adv='adb shell settings put system screen_brightness 200',
    os_type='通用',
    aliases='修改设置,settings put,设置值',
    tips='修改飞行模式等系统设置会立即触发广播。部分设置修改后需要重启应用才会生效。',
)
add(
    cmd_name='adb shell settings delete',
    name_cn='删除设置项',
    function_desc='删除指定设置项，使其恢复为系统默认值',
    syntax='adb shell settings delete <global|system|secure> <键名>',
    params_json='[{"参数":"命名空间","说明":"global / system / secure","必填":"必填"},{"参数":"键名","说明":"要删除的设置项键名","必填":"必填"}]',
    example_basic='adb shell settings delete global airplane_mode_on',
    example_adv='adb shell settings delete system screen_brightness',
    os_type='通用',
    aliases='删除设置,settings delete,恢复默认',
    tips='删除后系统会使用内置默认值。某些设置项删除后可能无法恢复原始行为。',
)
add(
    cmd_name='adb shell settings put global airplane_mode_on',
    name_cn='开关飞行模式',
    function_desc='通过修改系统全局设置来开启或关闭飞行模式',
    syntax='adb shell settings put global airplane_mode_on <0|1>',
    params_json='[{"参数":"1","说明":"开启飞行模式","必填":"必填"},{"参数":"0","说明":"关闭飞行模式","必填":"必填"}]',
    example_basic='adb shell settings put global airplane_mode_on 1',
    example_adv='adb shell settings put global airplane_mode_on 0',
    os_type='通用',
    aliases='飞行模式,airplane,mode',
    tips='修改后需广播 Intent 使其立即生效：am broadcast -a android.intent.action.AIRPLANE_MODE。',
)
add(
    cmd_name='adb shell settings put system screen_brightness',
    name_cn='设置屏幕亮度',
    function_desc='设置屏幕亮度值（0-255），立即生效',
    syntax='adb shell settings put system screen_brightness <0-255>',
    params_json='[{"参数":"0-255","说明":"亮度值，0 最暗，255 最亮","必填":"必填"}]',
    example_basic='adb shell settings put system screen_brightness 200',
    example_adv='adb shell settings put system screen_brightness 1',
    os_type='通用',
    aliases='屏幕亮度,brightness,亮度',
    tips='注意：自动亮度开启时此设置可能被覆盖。需先关闭自动亮度。',
)
add(
    cmd_name='adb shell settings put global wifi_on',
    name_cn='开关 WiFi',
    function_desc='通过系统设置开启或关闭 WiFi',
    syntax='adb shell settings put global wifi_on <0|1>',
    params_json='[{"参数":"1","说明":"开启WiFi","必填":"必填"},{"参数":"0","说明":"关闭WiFi","必填":"必填"}]',
    example_basic='adb shell settings put global wifi_on 1',
    example_adv='adb shell settings put global wifi_on 0',
    os_type='通用',
    aliases='wifi开关,无线网络,settings wifi',
    tips='Android 10+ 上建议使用 svc wifi enable/disable 命令替代。',
)
add(
    cmd_name='adb shell settings put global bluetooth_on',
    name_cn='开关蓝牙',
    function_desc='通过系统设置开启或关闭蓝牙',
    syntax='adb shell settings put global bluetooth_on <0|1>',
    params_json='[{"参数":"1","说明":"开启蓝牙","必填":"必填"},{"参数":"0","说明":"关闭蓝牙","必填":"必填"}]',
    example_basic='adb shell settings put global bluetooth_on 1',
    example_adv='adb shell settings put global bluetooth_on 0',
    os_type='通用',
    aliases='蓝牙开关,bluetooth,settings bluetooth',
    tips='Android 8.0+ 上建议使用 svc bluetooth enable/disable 命令替代。',
)
add(
    cmd_name='adb shell settings put secure location_providers_allowed',
    name_cn='开关定位',
    function_desc='开启或关闭特定定位提供商（gps/network/wifi 等）',
    syntax='adb shell settings put secure location_providers_allowed <+|-><提供商>',
    params_json='[{"参数":"+gps","说明":"开启 GPS 定位","必填":"必填"},{"参数":"-gps","说明":"关闭 GPS 定位","必填":"必填"},{"参数":"+network","说明":"开启网络定位","必填":"必填"},{"参数":"+wifi","说明":"开启 WiFi 扫描定位","必填":"必填"}]',
    example_basic='adb shell settings put secure location_providers_allowed +gps',
    example_adv='adb shell settings put secure location_providers_allowed -gps',
    os_type='通用',
    aliases='定位开关,location,gps',
    tips='使用 + 前缀启用，- 前缀禁用。多个提供商用逗号分隔（如 +gps,+network）。',
)

# ── 2.7 service 命令 ──

add(
    cmd_name='adb shell service',
    name_cn='系统服务管理',
    function_desc='列出、检查或调用系统服务的 API 接口',
    syntax='adb shell service <子命令>',
    params_json='[{"参数":"list","说明":"列出所有运行中的系统服务","必填":"可选"},{"参数":"check <服务名>","说明":"检查指定服务是否运行","必填":"可选"},{"参数":"call <服务名> <方法ID> [参数]","说明":"直接调用服务的 AIDL 接口","必填":"可选"}]',
    example_basic='adb shell service list',
    example_adv='adb shell service call activity 1',
    os_type='通用',
    aliases='系统服务,service,服务调用',
    tips='service call 是高级用法，需要了解服务的 AIDL 接口编号。dumpsys 通常比 service call 更方便。',
)
add(
    cmd_name='adb shell service list',
    name_cn='列出系统服务',
    function_desc='列出设备上所有注册的系统服务及其接口名称',
    syntax='adb shell service list',
    params_json='[]',
    example_basic='adb shell service list',
    example_adv='adb shell service list | grep "package"',
    os_type='通用',
    aliases='服务列表,service list,系统服务列表',
    tips='输出格式: "服务名: [接口名]"。此列表就是 dumpsys -l 可用的服务名。',
)
add(
    cmd_name='adb shell service call',
    name_cn='调用服务方法',
    function_desc='通过 AIDL 接口编号直接调用系统服务的内部方法',
    syntax='adb shell service call <服务名> <方法ID> [参数...]',
    params_json='[{"参数":"服务名","说明":"目标服务名（如 activity, package, window）","必填":"必填"},{"参数":"方法ID","说明":"AIDL 接口中的方法编号（从 1 开始）","必填":"必填"},{"参数":"参数","说明":"方法参数，格式：<类型> <值>，如 i32 123, s16 "hello"","必填":"可选"}]',
    example_basic='adb shell service call activity 1',
    example_adv='adb shell service call package 17 s16 "com.example.app" i32 0',
    os_type='通用',
    aliases='调用服务,service call,aidl调用',
    tips='此命令非常底层，需要了解服务的 AIDL 接口定义。方法 ID 可查看 AOSP 源码中的 I*Service.aidl 文件。',
)

# ── 2.8 content (Content Provider) ──

add(
    cmd_name='adb shell content',
    name_cn='Content Provider 操作',
    function_desc='查询、插入、更新、删除 Content Provider 中的数据，直接操作设备数据库',
    syntax='adb shell content <子命令> [参数]',
    params_json='[{"参数":"query <URI>","说明":"查询 Content Provider 数据","必填":"可选"},{"参数":"insert <URI>","说明":"插入新数据","必填":"可选"},{"参数":"update <URI>","说明":"更新已有数据","必填":"可选"},{"参数":"delete <URI>","说明":"删除数据","必填":"可选"},{"参数":"call <URI> <方法名>","说明":"调用 Provider 的扩展方法","必填":"可选"}]',
    example_basic='adb shell content query --uri content://settings/global',
    example_adv='adb shell content query --uri content://com.example.app.provider/data --projection _id:name --where "name=\'test\'"',
    os_type='通用',
    aliases='content provider,content,数据操作',
    tips='需要知道 Content URI 格式。常见 URI：content://settings/global、content://com.android.contacts/contacts。',
)
add(
    cmd_name='adb shell content query',
    name_cn='查询 Content Provider',
    function_desc='查询 Content Provider 中的数据，支持投影（projection）、条件（where）、排序（order）等',
    syntax='adb shell content query --uri <URI> [选项]',
    params_json='[{"参数":"--uri <URI>","说明":"Content Provider URI","必填":"必填"},{"参数":"--projection <列:列...>","说明":"指定返回的列（冒号分隔）","必填":"可选"},{"参数":"--where <条件>","说明":"过滤条件（SQL where 子句）","必填":"可选"},{"参数":"--sort <排序>","说明":"排序字段","必填":"可选"},{"参数":"--limit <N>","说明":"限制返回行数","必填":"可选"}]',
    example_basic='adb shell content query --uri content://settings/global',
    example_adv='adb shell content query --uri content://com.android.contacts/contacts --projection _id:display_name --limit 10',
    os_type='通用',
    aliases='查询数据,content query,查询provider',
    tips='--where 参数中的空格需要转义或使用引号。--projection 列名用冒号分隔。',
)
add(
    cmd_name='adb shell appops',
    name_cn='应用操作权限管理',
    function_desc='管理应用的 App Ops 操作权限，可以查看和修改更细粒度的权限控制',
    syntax='adb shell appops <子命令> [参数]',
    params_json='[{"参数":"get <包名>","说明":"获取指定应用的所有 AppOps 权限状态","必填":"可选"},{"参数":"set <包名> <操作> <模式>","说明":"设置指定操作的权限模式（allow/ignore/deny）","必填":"可选"},{"参数":"reset [<包名>]","说明":"重置 AppOps 为默认状态","必填":"可选"},{"参数":"query-op <操作>","说明":"查询执行指定操作的所有应用","必填":"可选"},{"参数":"query-package <包名>","说明":"查询指定包名的详细操作状态","必填":"可选"}]',
    example_basic='adb shell appops get com.example.app',
    example_adv='adb shell appops set com.example.app android:post_notifications allow',
    os_type='通用',
    aliases='权限管理,appops,应用操作',
    tips='AppOps 比普通权限更细粒度。常用操作：android:post_notifications（通知）、android:location（定位）。',
)

# ── 2.9 device_config ──

add(
    cmd_name='adb shell device_config',
    name_cn='设备配置管理',
    function_desc='管理 Android 设备配置（DeviceConfig），用于修改系统级标志和实验性功能',
    syntax='adb shell device_config <子命令> [参数]',
    params_json='[{"参数":"get <命名空间> <键>","说明":"获取指定配置键的值","必填":"可选"},{"参数":"put <命名空间> <键> <值>","说明":"设置指定配置键的值","必填":"可选"},{"参数":"delete <命名空间> <键>","说明":"删除指定配置","必填":"可选"},{"参数":"reset [<命名空间>]","说明":"重置配置为默认","必填":"可选"}]',
    example_basic='adb shell device_config get accessibility timeout',
    example_adv='adb shell device_config put permissions auto_revoke_unused_delay_millis 1000',
    os_type='通用',
    aliases='device_config,设备配置,系统标志',
    tips='Android 10+ 引入。用于修改系统级配置和标志（Feature Flag）。修改后可能需要重启 SystemUI。',
)

# ── 2.10 svc 命令 ──

add(
    cmd_name='adb shell svc',
    name_cn='系统服务控制',
    function_desc='控制系统基础服务的开关（WiFi、蓝牙、数据网络等）',
    syntax='adb shell svc <服务> <子命令>',
    params_json='[{"参数":"wifi enable/disable","说明":"开启/关闭 WiFi","必填":"可选"},{"参数":"bluetooth enable/disable","说明":"开启/关闭蓝牙","必填":"可选"},{"参数":"data enable/disable","说明":"开启/关闭移动数据","必填":"可选"},{"参数":"power stayon true/false/usb/ac","说明":"设置充电时保持唤醒","必填":"可选"}]',
    example_basic='adb shell svc wifi enable',
    example_adv='adb shell svc wifi disable && adb shell svc bluetooth enable',
    os_type='通用',
    aliases='服务控制,svc,开关服务',
    tips='比 settings put 更直接的开关系统服务的方式。不需要 root 权限。',
)

# ── 2.11 pm 补充：install/create-user 等 ──

add(
    cmd_name='adb shell pm install',
    name_cn='PackageManager 安装',
    function_desc='通过 PackageManager 命令安装应用（类似 adb install，支持更多选项）',
    syntax='adb shell pm install [选项] <APK路径>',
    params_json='[{"参数":"-r","说明":"覆盖安装","必填":"可选"},{"参数":"-d","说明":"允许降级","必填":"可选"},{"参数":"-t","说明":"允许安装测试APK","必填":"可选"},{"参数":"-i <安装来源>","说明":"指定安装来源","必填":"可选"},{"参数":"-g","说明":"授予运行时权限","必填":"可选"},{"参数":"--user <用户ID>","说明":"指定用户安装","必填":"可选"}]',
    example_basic='adb shell pm install /sdcard/app.apk',
    example_adv='adb shell pm install -r -t --user 0 /data/local/tmp/app.apk',
    os_type='通用',
    aliases='pm install,安装,包管理器安装',
    tips='pm install 和 adb install 功能类似，但 pm install 在设备 shell 内执行，支持更多设备本地路径选项。',
)
add(
    cmd_name='adb shell pm uninstall',
    name_cn='PackageManager 卸载',
    function_desc='通过 PackageManager 卸载应用（支持指定用户和保留数据）',
    syntax='adb shell pm uninstall [选项] <包名>',
    params_json='[{"参数":"-k","说明":"保留应用数据","必填":"可选"},{"参数":"--user <用户ID>","说明":"仅从指定用户卸载","必填":"可选"}]',
    example_basic='adb shell pm uninstall com.example.app',
    example_adv='adb shell pm uninstall -k --user 0 com.example.app',
    os_type='通用',
    aliases='pm uninstall,卸载,包管理器卸载',
    tips='在设备 shell 内执行的卸载，和 adb uninstall 效果相同但支持 --user 参数。',
)
add(
    cmd_name='adb shell pm create-user',
    name_cn='创建新用户',
    function_desc='在设备上创建新的用户配置文件（多用户模式）',
    syntax='adb shell pm create-user <用户名>',
    params_json='[{"参数":"用户名","说明":"新用户的显示名称","必填":"必填"}]',
    example_basic='adb shell pm create-user Guest',
    example_adv='adb shell pm create-user WorkProfile',
    os_type='通用',
    aliases='创建用户,pm create-user,多用户',
    tips='Android 多用户功能，可用于创建访客用户或工作资料。需要系统级权限。',
)
add(
    cmd_name='adb shell pm remove-user',
    name_cn='删除用户',
    function_desc='删除指定 ID 的用户配置文件及其所有数据',
    syntax='adb shell pm remove-user <用户ID>',
    params_json='[{"参数":"用户ID","说明":"要删除的用户 ID（通过 pm list users 查看）","必填":"必填"}]',
    example_basic='adb shell pm remove-user 10',
    example_adv='adb shell pm remove-user 10',
    os_type='通用',
    aliases='删除用户,pm remove-user',
    tips="删除用户会清除该用户的所有数据，包括应用、设置和文件。",
)

# ── 2.12 其他实用快捷命令 ──

add(
    cmd_name='adb shell screencap',
    name_cn='截取屏幕截图',
    function_desc='对设备屏幕进行截图并保存到指定路径',
    syntax='adb shell screencap <文件路径>',
    params_json='[{"参数":"文件路径","说明":"截图保存路径（如 /sdcard/screenshot.png）","必填":"必填"}]',
    example_basic='adb shell screencap /sdcard/screen.png',
    example_adv='adb shell screencap /sdcard/screen.png && adb pull /sdcard/screen.png',
    os_type='通用',
    aliases='截图,screencap,屏幕截图',
    tips='使用 adb exec-out screencap -p > screen.png 可截图到电脑本地，无需中间保存步骤。',
)
add(
    cmd_name='adb shell screenrecord',
    name_cn='屏幕录制',
    function_desc='录制设备屏幕为 MP4 视频文件',
    syntax='adb shell screenrecord [选项] <输出文件>',
    params_json='[{"参数":"--size <宽x高>","说明":"视频分辨率（默认 720p）","必填":"可选"},{"参数":"--bit-rate <bps>","说明":"视频比特率（默认 4Mbps）","必填":"可选"},{"参数":"--time-limit <秒>","说明":"录制时长限制（默认 180s，最长 180s）","必填":"可选"},{"参数":"--rotate","说明":"旋转输出为横屏","必填":"可选"},{"参数":"--verbose","说明":"显示日志信息","必填":"可选"}]',
    example_basic='adb shell screenrecord /sdcard/demo.mp4',
    example_adv='adb shell screenrecord --size 1080x1920 --bit-rate 8000000 --time-limit 30 /sdcard/demo.mp4',
    os_type='通用',
    aliases='录屏,screenrecord,屏幕录制,录像',
    tips='按 Ctrl+C 停止录制。录制结束后文件自动保存在设备路径。最长 3 分钟。按 adb pull 拉取到电脑。',
)
add(
    cmd_name='adb shell monkey',
    name_cn='Monkey 压力测试',
    function_desc='运行 UI/Application Exerciser Monkey 进行随机操作的稳定性和压力测试',
    syntax='adb shell monkey [选项] <事件数>',
    params_json='[{"参数":"-p <包名>","说明":"只对指定包名进行操作","必填":"可选"},{"参数":"-v","说明":"日志详细级别（-v -v -v 最详细）","必填":"可选"},{"参数":"-s <种子>","说明":"指定随机种子（可复现相同操作序列）","必填":"可选"},{"参数":"--throttle <毫秒>","说明":"事件间延迟（毫秒）","必填":"可选"},{"参数":"--pct-touch <百分比>","说明":"触摸事件百分比","必填":"可选"},{"参数":"--kill-process-after-error","说明":"错误后杀死进程","必填":"可选"}]',
    example_basic='adb shell monkey -p com.example.app -v 500',
    example_adv='adb shell monkey -p com.example.app -s 12345 --throttle 200 --pct-touch 70 -v -v 10000',
    os_type='通用',
    aliases='monkey,压力测试,稳定性测试',
    tips='Monkey 会随机生成点击、滑动等事件。建议先用 -p 限制目标应用。常用计数：500~10000。',
)
add(
    cmd_name='adb shell pm hide',
    name_cn='隐藏应用',
    function_desc='在启动器中隐藏指定应用（不显示在桌面和应用列表）',
    syntax='adb shell pm hide <包名>',
    params_json='[{"参数":"包名","说明":"要隐藏的应用包名","必填":"必填"}]',
    example_basic='adb shell pm hide com.example.app',
    example_adv='adb shell pm hide com.android.chrome',
    os_type='通用',
    aliases='隐藏应用,pm hide,隐藏',
    tips="隐藏后应用仍在运行，但不在启动器显示。用 pm unhide 恢复显示。",
)
add(
    cmd_name='adb shell pm unhide',
    name_cn='取消隐藏应用',
    function_desc='将之前通过 pm hide 隐藏的应用恢复显示',
    syntax='adb shell pm unhide <包名>',
    params_json='[{"参数":"包名","说明":"要取消隐藏的应用包名","必填":"必填"}]',
    example_basic='adb shell pm unhide com.example.app',
    example_adv='adb shell pm unhide com.android.chrome',
    os_type='通用',
    aliases='显示应用,pm unhide,取消隐藏',
    tips='pm hide/unhide 是 Android 5.0+ 提供的功能，适用于卸载不掉的预装应用。',
)

# ════════════════════════════════════════════
# 统计与完成
# ════════════════════════════════════════════
print('[OK] ADB (Android) 命令数据已全部插入完成')
