@echo off
chcp 65001 >nul
echo ========================================
echo    DBCompare Windows 打包脚本
echo ========================================

echo 正在检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请确保已安装 Python 并添加到 PATH
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 安装依赖包失败
    pause
    exit /b 1
)

echo.
echo 正在安装 PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 错误: 安装 PyInstaller 失败
    pause
    exit /b 1
)

echo.
echo 正在清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
for %%f in (*.spec) do del %%f

echo.
echo 开始构建 Windows 应用程序...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=DBCompare ^
    --icon=icon.ico ^
    --add-data=connections.db;. ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=sqlite3 ^
    --hidden-import=mysql.connector ^
    --hidden-import=sqlparse ^
    --hidden-import=threading ^
    --hidden-import=datetime ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ 构建失败！
    pause
    exit /b 1
)

echo.
echo ✅ 构建完成！
echo 可执行文件位置: dist\DBCompare.exe
echo.
echo 运行方式:
echo 1. 双击 dist\DBCompare.exe
echo 2. 或在命令行中运行: dist\DBCompare.exe
echo.
pause 