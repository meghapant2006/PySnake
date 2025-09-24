# 🚀 PySnake Database Setup & Login Instructions

## 🎮 **Quick Start - Authentication System**

Your Snake game now includes a complete user authentication system with database storage!

### **How to Play:**

1. **Launch the Game**: Run `python snake_game.py` or double-click `run_game.bat`

2. **First Time Players - Sign Up:**
   - Click "Sign Up" button
   - Enter a username (3+ characters)
   - Enter a valid email address
   - Create a password (6+ characters)
   - Confirm your password
   - Click "Sign Up" to create your account

3. **Returning Players - Login:**
   - Enter your username
   - Enter your password
   - Click "Login" or press ENTER

4. **Play & Compete:**
   - Your scores are automatically saved
   - Press 'L' during gameplay to view the leaderboard
   - Beat your personal best and compete with others!

## 🗄️ **Database System**

### **Automatic Database Setup:**
- **No MySQL Required**: The game automatically uses SQLite if MySQL isn't available
- **Auto-Creation**: Database and tables are created automatically on first run
- **Secure**: Passwords are hashed using bcrypt encryption
- **Persistent**: All your progress is saved between sessions

### **What Gets Stored:**
- ✅ User accounts (username, email, encrypted password)
- ✅ All game scores with timestamps
- ✅ Personal statistics (games played, average score, etc.)
- ✅ Global leaderboard rankings

## 🎯 **Game Features with Database:**

### **Personal Progress Tracking:**
- View your highest score in real-time during gameplay
- See "NEW RECORD!" when you beat your best score
- Track total games played and average performance
- Monitor your improvement over time

### **Global Competition:**
- Press 'L' to view the global leaderboard anytime
- See top 10 players worldwide
- Your rank is highlighted in the leaderboard
- Compare scores, snake lengths, and achievement dates

### **Enhanced Game Over Screen:**
- Final score and snake length
- Game duration tracking
- Personal best achievement notifications
- Quick access to leaderboard

## 🔧 **Database Configuration (Optional)**

The game works perfectly with the automatic SQLite database, but you can optionally use MySQL:

### **MySQL Setup (Advanced Users):**
1. Install MySQL Server
2. Create a database named `snake_game`
3. Copy `config_example.py` to `config.py`
4. Update the MySQL password in the config file
5. Restart the game

### **Files Created:**
- `snake_game.db` - SQLite database file (created automatically)
- User data and scores are stored here

## 🎮 **Controls:**

### **Authentication Screen:**
- **TAB**: Switch between input fields
- **ENTER**: Submit form (Login/Sign Up)
- **ESC**: Exit game
- **Mouse**: Click on fields and buttons

### **In-Game:**
- **WASD/Arrow Keys**: Control snake movement
- **SPACE**: Pause/unpause game
- **L**: Toggle leaderboard view
- **ESC**: Exit to desktop

## 🏆 **Leaderboard Features:**

- **Real-time Rankings**: Updated after each game
- **Multiple Stats**: Score, snake length, and date achieved
- **Personal Highlighting**: Your entries are highlighted in green
- **Top 10 Display**: See the best players globally
- **Date Tracking**: When each high score was achieved

## 🔒 **Security Features:**

- **Password Hashing**: bcrypt encryption for all passwords
- **Input Validation**: Email format and password strength checking
- **SQL Injection Protection**: Parameterized queries prevent attacks
- **User Isolation**: Each user only sees their own data

## 🐛 **Troubleshooting:**

### **"Database connection failed":**
- This is normal! The game automatically uses SQLite instead
- Your data is still saved and secure

### **"Username already exists":**
- Try a different username
- Or login with your existing account

### **Game won't start:**
- Make sure all packages are installed: `pip install -r requirements.txt`
- Check that Python 3.7+ is installed

### **Forgot your password:**
- Currently no password reset feature
- Create a new account with a different username

## 📊 **Statistics Tracked:**

- **Games Played**: Total number of completed games
- **Best Score**: Your highest score ever achieved
- **Longest Snake**: Maximum snake length reached
- **Average Score**: Mean score across all games
- **Average Duration**: How long your games typically last
- **Recent Performance**: Latest scores and improvements

## 🎯 **Tips for High Scores:**

1. **Plan Your Path**: Think ahead to avoid trapping yourself
2. **Use the Walls**: Use screen edges to guide your movement
3. **Stay Calm**: Don't panic when the snake gets long
4. **Practice**: Your average improves with more games played
5. **Check Leaderboard**: Learn from top players' achievements

---

**Enjoy your new competitive Snake game with full user accounts and leaderboards!** 🐍🏆

The authentication system ensures fair play and lets you build your gaming legacy over time!