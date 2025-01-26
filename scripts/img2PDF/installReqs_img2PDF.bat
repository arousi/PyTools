@echo off
echo Installing requirements for Image to PDF Converter...
pip install -r scripts\img2PDF\reqs.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements. Check your Python and pip setup.
    exit /b 1
)
echo Requirements installed successfully!
exit /b 0