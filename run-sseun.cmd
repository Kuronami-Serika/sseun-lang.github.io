@echo off
setlocal

py -3 --version >nul 2>&1
if not errorlevel 1 (
    py -3 -X utf8 "%~dp0sseun.py" %*
) else (
    python -X utf8 "%~dp0sseun.py" %*
)

set "sseun_exit_code=%errorlevel%"
echo(
pause
exit /b %sseun_exit_code%
