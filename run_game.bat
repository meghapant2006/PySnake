@echo off
echo ================================================
echo  PySnake - Classic Snake Game
echo ================================================
echo.
echo Features:
echo  - Classic Snake Gameplay
echo  - High Score Tracking
echo  - Modern Graphics and Sound
echo.
echo Starting game...
echo.
cd /d "%~dp0"
.\.venv\Scripts\python.exe snake_game.py
echo.
echo Game ended. Press any key to close...
pause > nul