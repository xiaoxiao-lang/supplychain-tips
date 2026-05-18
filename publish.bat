@echo off
REM ========================================
REM 自动发布脚本 - 每天定时执行
REM 1. 生成新文章
REM 2. 编译Hugo
REM 3. 推送到GitHub
REM 4. Cloudflare Pages自动部署
REM ========================================

cd /d D:\myseosite

REM 设置Git路径
set PATH=%PATH%;C:\Users\peilu\AppData\Local\Git\cmd

REM 生成新文章
echo [1/4] 生成今日文章...
"C:\Users\peilu\.workbuddy\binaries\python\versions\3.14.3\python.exe" scripts\generate_article.py
if %errorlevel% neq 0 (
    echo [ERROR] 文章生成失败
    pause
    exit /b 1
)

REM 编译Hugo
echo [2/4] 编译Hugo...
"C:\Users\peilu\AppData\Local\hugo\hugo.exe" --minify
if %errorlevel% neq 0 (
    echo [ERROR] Hugo编译失败
    pause
    exit /b 1
)

REM Git提交
echo [3/4] 提交到Git...
git add .
git commit -m "自动更新: %date% %time%"
git push origin main
if %errorlevel% neq 0 (
    echo [ERROR] Git推送失败
    pause
    exit /b 1
)

echo [4/4] 完成！Cloudflare Pages正在部署中...
echo [OK] 全部完成！
