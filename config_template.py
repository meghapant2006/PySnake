# PySnake MySQL Configuration
# Rename this file to 'config.py' and update the password

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # ⚠️ PUT YOUR MYSQL PASSWORD HERE ⚠️
    'database': 'snake_game'
}

# Instructions:
# 1. Install MySQL Server or XAMPP
# 2. Set a password for the root user during installation
# 3. Replace the empty password above with your actual MySQL password
# 4. Save this file as 'config.py' (remove '_template' from the name)
# 5. Run the game - it will automatically use MySQL instead of SQLite

# Example:
# DATABASE_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'mypassword123',  # Your actual password
#     'database': 'snake_game'
# }

# For XAMPP users:
# - Default user is 'root' with no password (leave password as '')
# - Make sure MySQL service is started in XAMPP Control Panel