@echo off
REM CodeQuickRef 启动脚本 (Windows)
REM 支持两种模式：
REM   1. 双击 run.bat —— GUI 模式
REM   2. run.bat --seed —— 仅重新导入种子数据
REM   3. run.bat --pack —— 打包 EXE

chcp 65001 >nul
echo ========================================
echo   CodeQuickRef — 代码速查工具
echo ========================================
echo.

IF "%1"=="--seed" (
    echo 正在导入种子数据...
    python seed_data/seed_commands.py
    python seed_data/seed_snippets.py
    python seed_data/seed_patterns.py
    echo 种子数据导入完成！
    pause
    exit /b
)

IF "%1"=="--pack" (
    echo 正在打包 EXE...
    pyinstaller CodeQuickRef.spec
    echo 打包完成！exe 在 dist\CodeQuickRef\
    pause
    exit /b
)

echo 正在启动应用程序...
python main.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo 启动失败，可能是依赖未安装。
    echo 请先运行: pip install PySide6
    pause
)
