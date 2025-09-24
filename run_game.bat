@echo off
echo ================================================
echo  PySnake - Attractive Snake Game with Database
echo ================================================
echo.
echo Features:
echo  - User Registration and Login
echo  - High Score Tracking
echo  - Personal Statistics
echo  - Global Leaderboard
echo.
echo Starting game...
echo.
cd /d "%~dp0"
.\.venv\Scripts\python.exe snake_game.py
echo.
echo Game ended. Press any key to close...
pause > nul