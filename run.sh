#!/bin/bash
# CodeQuickRef 启动脚本 (Linux/WSL)
# 用法: ./run.sh [--seed|--pack]

cd "$(dirname "$0")"

if [ "$1" == "--seed" ]; then
    echo "正在导入种子数据..."
    python3 seed_data/seed_commands.py
    python3 seed_data/seed_snippets.py
    python3 seed_data/seed_patterns.py
    echo "种子数据导入完成！"
    exit 0
fi

if [ "$1" == "--pack" ]; then
    echo "正在打包..."
    pyinstaller CodeQuickRef.spec
    echo "打包完成！"
    exit 0
fi

echo "正在启动 CodeQuickRef..."
python3 main.py
