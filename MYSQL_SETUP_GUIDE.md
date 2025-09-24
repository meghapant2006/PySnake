# 🗄️ MySQL Setup Guide for PySnake

## 📋 **Prerequisites**

1. **Install MySQL Server**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Or use XAMPP (includes MySQL): https://www.apachefriends.org/
   - Or install via package manager:
     - Windows: `winget install Oracle.MySQL`
     - macOS: `brew install mysql`

2. **Install MySQL Workbench (Optional GUI)**
   - Download from: https://dev.mysql.com/downloads/workbench/

## 🚀 **Step-by-Step MySQL Setup**

### **Step 1: Install and Start MySQL**

**For XAMPP Users:**
1. Download and install XAMPP
2. Open XAMPP Control Panel
3. Start "MySQL" service
4. Click "Admin" button next to MySQL (opens phpMyAdmin)

**For Direct MySQL Installation:**
1. Install MySQL Server
2. During installation, set a root password (remember this!)
3. Start MySQL service

### **Step 2: Create Database Configuration**

Create a file named `config.py` in your PySnake folder:

```python
# Database Configuration for PySnake
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password_here',  # Replace with your actual password
    'database': 'snake_game'
}
```

### **Step 3: Update Database Manager**

The game will automatically detect your MySQL configuration and use it instead of SQLite.

## 🔍 **Viewing User Data in MySQL**

### **Method 1: Using MySQL Command Line**

1. **Open Command Prompt/Terminal**
2. **Connect to MySQL:**
   ```bash
   mysql -u root -p
   ```
3. **Enter your MySQL password**
4. **Select the database:**
   ```sql
   USE snake_game;
   ```
5. **View all tables:**
   ```sql
   SHOW TABLES;
   ```
6. **View users table:**
   ```sql
   SELECT * FROM users;
   ```
7. **View high scores:**
   ```sql
   SELECT * FROM high_scores;
   ```
8. **View detailed user data with scores:**
   ```sql
   SELECT u.username, u.email, u.created_at, u.last_login,
          COUNT(h.id) as games_played,
          MAX(h.score) as best_score,
          AVG(h.score) as avg_score
   FROM users u
   LEFT JOIN high_scores h ON u.id = h.user_id
   GROUP BY u.id;
   ```

### **Method 2: Using phpMyAdmin (XAMPP)**

1. **Start XAMPP**
2. **Open phpMyAdmin** (usually http://localhost/phpmyadmin)
3. **Select 'snake_game' database** from the left sidebar
4. **Click on tables to view data:**
   - `users` - User accounts and login info
   - `high_scores` - All game scores and statistics

### **Method 3: Using MySQL Workbench**

1. **Open MySQL Workbench**
2. **Create new connection:**
   - Host: localhost
   - Port: 3306
   - Username: root
   - Password: your_mysql_password
3. **Connect and navigate to snake_game database**
4. **Run queries to view data**

## 📊 **Useful SQL Queries for Data Analysis**

### **View All Users:**
```sql
SELECT id, username, email, created_at, last_login 
FROM users 
ORDER BY created_at DESC;
```

### **Top 10 High Scores:**
```sql
SELECT u.username, h.score, h.snake_length, h.achieved_at
FROM high_scores h
JOIN users u ON h.user_id = u.id
ORDER BY h.score DESC
LIMIT 10;
```

### **User Statistics:**
```sql
SELECT u.username,
       COUNT(h.id) as total_games,
       MAX(h.score) as best_score,
       MIN(h.score) as worst_score,
       AVG(h.score) as average_score,
       MAX(h.snake_length) as longest_snake,
       AVG(h.game_duration) as avg_game_time
FROM users u
LEFT JOIN high_scores h ON u.id = h.user_id
GROUP BY u.id, u.username
ORDER BY best_score DESC;
```

### **Recent Activity:**
```sql
SELECT u.username, h.score, h.snake_length, h.achieved_at
FROM high_scores h
JOIN users u ON h.user_id = u.id
ORDER BY h.achieved_at DESC
LIMIT 20;
```

### **Find Specific User's Data:**
```sql
SELECT u.username, u.email, u.created_at,
       COUNT(h.id) as games_played,
       MAX(h.score) as best_score
FROM users u
LEFT JOIN high_scores h ON u.id = h.user_id
WHERE u.username = 'your_username_here'
GROUP BY u.id;
```

## 🛠️ **Database Management Commands**

### **Backup Database:**
```bash
mysqldump -u root -p snake_game > snake_game_backup.sql
```

### **Restore Database:**
```bash
mysql -u root -p snake_game < snake_game_backup.sql
```

### **Reset All Data (Careful!):**
```sql
DELETE FROM high_scores;
DELETE FROM users;
```

### **Delete Specific User:**
```sql
-- This will also delete all their scores due to foreign key constraint
DELETE FROM users WHERE username = 'username_to_delete';
```

## 🔧 **Troubleshooting**

### **"Access denied for user 'root'"**
- Check your MySQL password in config.py
- Make sure MySQL service is running
- Try connecting with MySQL command line first

### **"Database 'snake_game' doesn't exist"**
- The game will create it automatically on first run
- Or create manually: `CREATE DATABASE snake_game;`

### **"Table doesn't exist"**
- Tables are created automatically when the game starts
- Make sure you're connected to the right database

### **Connection timeout**
- Check if MySQL service is running
- Verify host and port settings (default: localhost:3306)

## 📈 **Monitoring Game Activity**

### **Create a View for Easy Data Access:**
```sql
CREATE VIEW user_summary AS
SELECT u.id, u.username, u.email,
       COUNT(h.id) as total_games,
       MAX(h.score) as best_score,
       AVG(h.score) as avg_score,
       MAX(h.achieved_at) as last_played
FROM users u
LEFT JOIN high_scores h ON u.id = h.user_id
GROUP BY u.id;

-- Then use: SELECT * FROM user_summary;
```

### **Real-time Monitoring:**
```sql
-- Show games played in the last hour
SELECT u.username, h.score, h.achieved_at
FROM high_scores h
JOIN users u ON h.user_id = u.id
WHERE h.achieved_at > NOW() - INTERVAL 1 HOUR
ORDER BY h.achieved_at DESC;
```

## 🔒 **Security Best Practices**

1. **Change default root password**
2. **Create dedicated MySQL user for the game:**
   ```sql
   CREATE USER 'snakegame'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON snake_game.* TO 'snakegame'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. **Update config.py with new user:**
   ```python
   DATABASE_CONFIG = {
       'host': 'localhost',
       'user': 'snakegame',
       'password': 'secure_password',
       'database': 'snake_game'
   }
   ```

---

**After following this guide, you'll have full MySQL integration and can easily view all user data and game statistics!** 🎮📊