@echo off
title MUSE Launcher
echo.
echo   M U S E  -  Launching...
echo.

set "APP_PATH=%~dp0index.html"
set "API_PORT=3000"
set "LX_PORT=9000"

:: Start Netease API server in background (if not already running)
echo   Starting Netease API (port %API_PORT%)...
netstat -ano | findstr ":%API_PORT% " | findstr "LISTENING" >nul
if errorlevel 1 (
    start "MUSE-NeteaseAPI" /MIN cmd /c "cd /d %~dp0 && npx -y NeteaseCloudMusicApi"
    echo   Waiting for API to be ready...
    timeout /t 6 /nobreak >nul
) else (
    echo   API already running on port %API_PORT%.
)

:: Start LX multi-platform API server (if not already running)
echo   Starting Multi-Platform API (port %LX_PORT%)...
netstat -ano | findstr ":%LX_PORT% " | findstr "LISTENING" >nul
if errorlevel 1 (
    start "MUSE-LX-API" /MIN cmd /c "cd /d %~dp0lx-api-server && python main.py"
    echo   Waiting for LX API to be ready...
    timeout /t 4 /nobreak >nul
) else (
    echo   LX API already running on port %LX_PORT%.
)

:: Find Edge or Chrome
set "BROWSER="
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)
if "%BROWSER%"=="" (
    if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
        set "BROWSER=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    )
)
if "%BROWSER%"=="" (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        set "BROWSER=C:\Program Files\Google\Chrome\Application\chrome.exe"
    )
)
if "%BROWSER%"=="" (
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        set "BROWSER=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
)
if "%BROWSER%"=="" (
    for /d %%d in ("%LOCALAPPDATA%\Google\Chrome\Application\*") do (
        if exist "%%d\chrome.exe" set "BROWSER=%%d\chrome.exe"
    )
)

if "%BROWSER%"=="" (
    echo [ERROR] Chrome or Edge not found.
    pause
    exit /b 1
)

echo.
echo   Browser: %BROWSER%
echo   App: %APP_PATH%
echo   API: http://localhost:%API_PORT%
echo.
echo   Launching MUSE in chromeless window...
echo.

start "" "%BROWSER%" --app="%APP_PATH%"

exit /b 0
