# Database Configuration for PySnake
# Copy this file to config.py and modify the settings for your database

# MySQL Database Settings
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'database': 'snake_game'
}

# Alternative: If you don't have MySQL installed, the game will automatically
# use SQLite as a fallback database (snake_game.db file will be created)

# Database Features:
# - User registration and authentication
# - Password hashing with bcrypt
# - High score tracking per user
# - Global leaderboard
# - User statistics (games played, average score, etc.)

# Setup Instructions:
# 1. Install MySQL Server (optional - SQLite fallback available)
# 2. Create a database named 'snake_game' (automatic if using root user)
# 3. Update the password in DATABASE_CONFIG above
# 4. Run the game - tables will be created automatically

# Note: The game will work without MySQL by automatically creating
# a local SQLite database file for testing purposes.