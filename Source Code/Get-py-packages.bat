@echo off & title %~n0 & color 0F
@mode 120, 30
echo. checking internet connection...
timeout 2 >nul
Ping www.google.nl -n 1 -w 1000
cls
if errorlevel 1 (
    echo. & echo. & echo.   Not connected to internet.
    echo.   Press any key to exit ... & echo.
	pause >nul && exit
) else (
    goto start
)
:start
python --version 2>NUL
if errorlevel == 1 goto errorNoPython

:PythonExist
echo.   ^> Getting "pygame" package...      Backgrounded...
pip install pygame >nul
echo.   ^> Getting "pygame-menu" package... Backgrounded...
pip install pygame-menu -U >nul
cls && echo.
echo.
echo.   Both packages ("pygame", "pygame-menu") are installed ...
echo.   Press any key to exit %~nx0... && echo.
pause >nul && exit

:errorNoPython
echo.
echo.   Python is not installed on your system.
echo.   Now opeing the download URL for python.
echo.   Press any key to recheck... && timeout 1 >nul
start "" "https://www.python.org/"
pause >nul goto start
