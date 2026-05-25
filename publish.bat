@echo off
chcp 65001 >nul

REM Auto publish script - Run daily
REM 1. Generate articles
REM 2. Build Hugo
REM 3. Push to GitHub
REM 4. Cloudflare Pages auto deploy

cd /d D:\myseosite

REM Setup Git path
set PATH=%PATH%;C:\Users\peilu\AppData\Local\Git\cmd

REM Step 1: Generate articles
echo [1/4] Generating articles...
"C:\Users\peilu\.workbuddy\binaries\python\versions\3.14.3\python.exe" scripts\generate_article.py
if %errorlevel% neq 0 (
    echo [ERROR] Article generation failed
    pause
    exit /b 1
)

REM Step 2: Build Hugo
echo [2/4] Building Hugo site...
"C:\Users\peilu\AppData\Local\hugo\hugo.exe" --minify
if %errorlevel% neq 0 (
    echo [ERROR] Hugo build failed
    pause
    exit /b 1
)

REM Step 3: Git commit and push
echo [3/4] Committing to Git...
git add .
git commit -m "Auto update: %date% %time%"
git push origin main
if %errorlevel% neq 0 (
    echo [ERROR] Git push failed
    pause
    exit /b 1
)

REM Done
echo [4/4] Complete! Cloudflare Pages deploying...
echo OK all done!
pause
