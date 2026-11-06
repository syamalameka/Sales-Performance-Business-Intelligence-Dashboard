@echo off
title Sales Analytics & BI Dashboard Runner
color 0A
cls

echo ======================================================================
echo    SALES PERFORMANCE & BUSINESS INTELLIGENCE DASHBOARD
echo ======================================================================
echo.
echo Choose an option to run:
echo.
echo  [1] Open Interactive Dashboard in Browser (Fastest - 0 Setup)
echo  [2] Run Python Analysis & SQL Database Queries (Shows printed results)
echo  [3] Open Project Folder on Desktop
echo  [4] Open Power BI File (sales_dashboard.pbix)
echo  [5] Exit
echo.
echo ======================================================================
set /p choice="Enter your choice (1-5) and press Enter: "

if "%choice%"=="1" goto OPENDASH
if "%choice%"=="2" goto RUNPY
if "%choice%"=="3" goto OPENDIR
if "%choice%"=="4" goto OPENPBI
if "%choice%"=="5" goto EXIT
goto INVALID

:OPENDASH
echo.
echo Opening interactive dashboard in your browser...
start "" "%~dp0dashboard\interactive_dashboard.html"
echo Done! Check your browser window.
pause
goto MENU

:RUNPY
echo.
echo Running Python script and executing SQL queries...
echo.
python "%~dp0run_analysis.py"
echo.
pause
goto MENU

:OPENDIR
start "" "%~dp0"
goto MENU

:OPENPBI
start "" "%~dp0dashboard\sales_dashboard.pbix"
goto MENU

:INVALID
echo Invalid choice, please try again.
pause
goto MENU

:MENU
cls
goto :EOF
