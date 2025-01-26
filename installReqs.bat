@echo off
:: Detect OS and architecture
set "DOWNLOAD_URL="
if defined ProgramFiles(x86) (
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
) else (
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8.exe"
)

:: ARM detection
wmic os get osarchitecture | find "ARM" >nul
if %ERRORLEVEL% EQU 0 (
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-arm64.exe"
)

if not defined DOWNLOAD_URL (
    echo Unsupported OS or detection failure. Please visit https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri %DOWNLOAD_URL% -OutFile python-installer.exe"
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to download Python installer.
        pause
        exit /b
    )
    echo Installing Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install Python.
        pause
        exit /b
    )
    del python-installer.exe
)

:: Check pip installation
python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
)

:: Install tkinter
pip install tk

echo Python, pip, and tkinter are ready.
pause