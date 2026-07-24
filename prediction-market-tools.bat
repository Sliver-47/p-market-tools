@echo off
chcp 65001 >nul
title Prediction Market Tools - 预测市场数据工具

cd /d "%~dp0"

:menu
cls
echo ============================================================
echo   Prediction Market Tools - 预测市场数据工具
echo ============================================================
echo.
echo   1. 一键抓取热门市场（前 30 个）
echo   2. 按分类抓取
echo   3. 抓取并保存为 Markdown 文件
echo   4. 启动 Chrome Debug 模式
echo   5. 检查依赖状态
echo   6. 退出
echo.
echo ============================================================
echo.
echo ⚠️  免责声明：本工具仅供学习研究使用，请遵守目标平台服务条款
echo.
set /p choice=请选择操作 (1-6): 

if "%choice%"=="1" goto all
if "%choice%"=="2" goto category
if "%choice%"=="3" goto save
if "%choice%"=="4" goto chrome
if "%choice%"=="5" goto check
if "%choice%"=="6" goto end
goto menu

:all
cls
echo [1/1] 正在抓取热门市场...
echo.
python skills\crawl-polymarket-markets\scripts\crawl_polymarket_markets.py
echo.
pause
goto menu

:category
cls
echo 可选分类:
echo   1. all (全部)
echo   2. politics (政治)
echo   3. sports (体育)
echo   4. crypto (加密货币)
echo   5. esports (电竞)
echo   6. finance (金融)
echo   7. geopolitics (地缘政治)
echo   8. tech (科技)
echo   9. culture (文化)
echo   10. economy (经济)
echo   11. weather (天气)
echo.
set /p cat=请输入分类编号或名称: 

set CAT_NAME=%cat%
if "%cat%"=="1" set CAT_NAME=all
if "%cat%"=="2" set CAT_NAME=politics
if "%cat%"=="3" set CAT_NAME=sports
if "%cat%"=="4" set CAT_NAME=crypto
if "%cat%"=="5" set CAT_NAME=esports
if "%cat%"=="6" set CAT_NAME=finance
if "%cat%"=="7" set CAT_NAME=geopolitics
if "%cat%"=="8" set CAT_NAME=tech
if "%cat%"=="9" set CAT_NAME=culture
if "%cat%"=="10" set CAT_NAME=economy
if "%cat%"=="11" set CAT_NAME=weather

cls
echo [1/1] 正在抓取 %CAT_NAME% 分类市场...
echo.
python skills\crawl-polymarket-markets\scripts\crawl_polymarket_markets.py --category %CAT_NAME%
echo.
pause
goto menu

:save
cls
set /p count=抓取前多少个 (默认30): 
if "%count%"=="" set count=30

set filename=prediction_markets_%date:~0,4%%date:~5,2%%date:~8,2%.md
echo.
echo [1/1] 正在抓取前 %count% 个市场，保存到 %filename%...
echo.
python skills\crawl-polymarket-markets\scripts\crawl_polymarket_markets.py --top %count% --save %filename%
echo.
pause
goto menu

:chrome
cls
echo 正在启动 Chrome Debug 模式...
echo.
echo 注意: 如果 Chrome 已经在运行，请先关闭所有 Chrome 窗口
echo.

set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
)
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
)

if "%CHROME_PATH%"=="" (
    echo [错误] 未找到 Chrome 浏览器
    echo 请手动安装 Chrome 或指定路径
    pause
    goto menu
)

echo Chrome 路径: %CHROME_PATH%
echo 调试端口: 9222
echo 用户数据: %~dp0browser_profiles\chrome-debug
echo.
echo 启动后请保持 Chrome 窗口打开
echo.

if not exist "%~dp0browser_profiles" mkdir "%~dp0browser_profiles"
if not exist "%~dp0browser_profiles\chrome-debug" mkdir "%~dp0browser_profiles\chrome-debug"

start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%~dp0browser_profiles\chrome-debug"

echo Chrome 已启动
echo.
pause
goto menu

:check
cls
echo 依赖检查
echo ============================================================
echo.

echo [1/3] Python...
python --version 2>nul
if %errorlevel%==0 (
    echo     ✓ Python 已安装
) else (
    echo     ✗ Python 未安装，请先安装 Python 3.10+
)
echo.

echo [2/3] websocket-client...
python -c "import websocket; print('    ✓ websocket-client 已安装')" 2>nul
if errorlevel 1 (
    echo     ✗ websocket-client 未安装
    echo       安装命令: pip install websocket-client
)
echo.

echo [3/3] Chrome Debug 端口...
python -c "import urllib.request; urllib.request.urlopen('http://localhost:9222/json', timeout=2); print('    ✓ Chrome Debug 已连接')" 2>nul
if errorlevel 1 (
    echo     ✗ 未检测到 Chrome Debug (端口 9222)
    echo       请使用选项 4 启动 Chrome Debug
)
echo.

echo ============================================================
echo.
pause
goto menu

:end
cls
echo 再见！
timeout /t 1 >nul
exit /b 0
