@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Downloading Python installer...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

    echo Running Python installer...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo Python installation completed.
)

:: Ensure pip is installed
echo Checking pip installation...
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Install required libraries
echo Installing required libraries...
pip install -r reqs.txt

echo All done! You can now use the scripts.
pause
