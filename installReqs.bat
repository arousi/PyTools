@echo off
:: Detect the operating system architecture
set "DOWNLOAD_URL="
set "OS_VERSION="

:: Determine OS and architecture
if defined ProgramFiles(x86) (
    :: 64-bit Windows
    echo Detected 64-bit Windows.
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
) else (
    :: 32-bit Windows
    echo Detected 32-bit Windows.
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8.exe"
)

:: Check for ARM architecture on Windows
wmic os get osarchitecture | find "ARM" >nul
if %ERRORLEVEL% EQU 0 (
    echo Detected ARM64 Windows.
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-arm64.exe"
)

:: Detect macOS (requires manual re-run in macOS terminal)
ver | find "Darwin" >nul
if %ERRORLEVEL% EQU 0 (
    echo Detected macOS.
    set "DOWNLOAD_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-macos11.pkg"
)

if not defined DOWNLOAD_URL (
    echo Operating system not supported or detection failed.
    echo Please visit https://www.python.org/downloads/ to download Python manually.
    pause
    exit /b
)

:: Download Python installer
echo Downloading Python installer from %DOWNLOAD_URL%...
curl -o python-installer.exe %DOWNLOAD_URL%

:: Install Python
echo Running Python installer...
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if %ERRORLEVEL% NEQ 0 (
    echo Python installation failed. Please install Python manually and re-run this script.
    pause
    exit /b
)

:: Ensure pip is installed and updated
echo Checking and upgrading pip...
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Install required libraries from reqs.txt
if exist reqs.txt (
    echo Installing required Python libraries...
    pip install -r reqs.txt
) else (
    echo No reqs.txt file found. Skipping library installation.
)

echo All done! You can now use the scripts.
pause
