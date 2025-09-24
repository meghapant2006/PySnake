import mysql.connector
import bcrypt
from datetime import datetime
from typing import Optional, List, Tuple
import logging

class DatabaseManager:
    """Handles all database operations for the Snake game"""
    
    def __init__(self, host='localhost', user='root', password='', database='snake_game'):
        # Try to load configuration from config.py file
        try:
            from config import DATABASE_CONFIG
            self.host = DATABASE_CONFIG.get('host', host)
            self.user = DATABASE_CONFIG.get('user', user)
            self.password = DATABASE_CONFIG.get('password', password)
            self.database = DATABASE_CONFIG.get('database', database)
            print(f"✅ Loaded MySQL configuration from config.py")
        except ImportError:
            # Use default values if config.py doesn't exist
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            print("ℹ️  No config.py found, using default settings (will use SQLite fallback)")
        
        self.connection = None
        self.is_sqlite = False
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.init_database()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            return True
        except mysql.connector.Error as err:
            self.logger.error(f"Database connection error: {err}")
            return False
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # First, connect without specifying database to create it if needed
            temp_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                autocommit=True
            )
            
            cursor = temp_conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL
                )
            """)
            
            # Create high_scores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    score INT NOT NULL,
                    snake_length INT NOT NULL,
                    game_duration INT NOT NULL,
                    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_score (user_id, score),
                    INDEX idx_score (score DESC)
                )
            """)
            
            cursor.close()
            temp_conn.close()
            
            # Now connect to the specific database
            self.connect()
            self.logger.info("Database initialized successfully")
            
        except mysql.connector.Error as err:
            self.logger.error(f"Database initialization error: {err}")
            # Create a fallback SQLite database if MySQL fails
            self.init_sqlite_fallback()
    
    def init_sqlite_fallback(self):
        """Initialize SQLite as fallback if MySQL is not available"""
        try:
            import sqlite3
            self.connection = sqlite3.connect('snake_game.db')
            cursor = self.connection.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL
                )
            """)
            
            # Create high_scores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    snake_length INTEGER NOT NULL,
                    game_duration INTEGER NOT NULL,
                    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            self.connection.commit()
            self.logger.info("SQLite fallback database initialized")
            self.is_sqlite = True
            
        except Exception as e:
            self.logger.error(f"SQLite fallback failed: {e}")
            self.connection = None
            self.is_sqlite = False
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Create a new user account"""
        if not self.connection:
            return False, "Database connection failed"
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            # Check if username or email already exists
            cursor.execute(f"SELECT id FROM users WHERE username = {placeholder} OR email = {placeholder}", (username, email))
            if cursor.fetchone():
                cursor.close()
                return False, "Username or email already exists"
            
            # Hash password and create user
            password_hash = self.hash_password(password)
            cursor.execute(f"""
                INSERT INTO users (username, email, password_hash) 
                VALUES ({placeholder}, {placeholder}, {placeholder})
            """, (username, email, password_hash))
            
            if self.is_sqlite:
                self.connection.commit()
            
            cursor.close()
            self.logger.info(f"User created successfully: {username}")
            return True, "Account created successfully!"
            
        except Exception as err:
            self.logger.error(f"User creation error: {err}")
            return False, f"Error creating account: {str(err)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[int], str]:
        """Authenticate user login"""
        if not self.connection:
            return False, None, "Database connection failed"
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            # Get user data
            cursor.execute(f"""
                SELECT id, password_hash FROM users 
                WHERE username = {placeholder}
            """, (username,))
            
            result = cursor.fetchone()
            if not result:
                cursor.close()
                return False, None, "Invalid username or password"
            
            user_id, stored_hash = result
            
            # Verify password
            if self.verify_password(password, stored_hash):
                # Update last login
                if self.is_sqlite:
                    cursor.execute(f"""
                        UPDATE users SET last_login = datetime('now') 
                        WHERE id = {placeholder}
                    """, (user_id,))
                    self.connection.commit()
                else:
                    cursor.execute(f"""
                        UPDATE users SET last_login = NOW() 
                        WHERE id = {placeholder}
                    """, (user_id,))
                
                cursor.close()
                self.logger.info(f"User authenticated successfully: {username}")
                return True, user_id, "Login successful!"
            else:
                cursor.close()
                return False, None, "Invalid username or password"
                
        except Exception as err:
            self.logger.error(f"Authentication error: {err}")
            return False, None, f"Authentication error: {str(err)}"
    
    def save_score(self, user_id: int, score: int, snake_length: int, game_duration: int) -> bool:
        """Save a game score to the database"""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            cursor.execute(f"""
                INSERT INTO high_scores (user_id, score, snake_length, game_duration)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (user_id, score, snake_length, game_duration))
            
            if self.is_sqlite:
                self.connection.commit()
            
            cursor.close()
            self.logger.info(f"Score saved: {score} for user {user_id}")
            return True
            
        except Exception as err:
            self.logger.error(f"Score saving error: {err}")
            return False
    
    def get_user_high_score(self, user_id: int) -> Optional[int]:
        """Get user's highest score"""
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            cursor.execute(f"""
                SELECT MAX(score) FROM high_scores 
                WHERE user_id = {placeholder}
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result and result[0] else 0
            
        except Exception as err:
            self.logger.error(f"High score retrieval error: {err}")
            return None
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int, int, str]]:
        """Get top scores leaderboard"""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            if self.is_sqlite:
                cursor.execute(f"""
                    SELECT u.username, h.score, h.snake_length, 
                           strftime('%Y-%m-%d %H:%M', h.achieved_at) as achieved_date
                    FROM high_scores h
                    JOIN users u ON h.user_id = u.id
                    ORDER BY h.score DESC, h.achieved_at ASC
                    LIMIT {placeholder}
                """, (limit,))
            else:
                cursor.execute(f"""
                    SELECT u.username, h.score, h.snake_length, 
                           DATE_FORMAT(h.achieved_at, '%Y-%m-%d %H:%i') as achieved_date
                    FROM high_scores h
                    JOIN users u ON h.user_id = u.id
                    ORDER BY h.score DESC, h.achieved_at ASC
                    LIMIT {placeholder}
                """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Exception as err:
            self.logger.error(f"Leaderboard retrieval error: {err}")
            return []
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get user game statistics"""
        if not self.connection:
            return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Use appropriate placeholder syntax
            placeholder = "?" if self.is_sqlite else "%s"
            
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as games_played,
                    MAX(score) as best_score,
                    MAX(snake_length) as longest_snake,
                    AVG(score) as avg_score,
                    AVG(game_duration) as avg_duration
                FROM high_scores 
                WHERE user_id = {placeholder}
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return {
                    'games_played': result[0] or 0,
                    'best_score': result[1] or 0,
                    'longest_snake': result[2] or 0,
                    'avg_score': round(result[3] or 0, 1),
                    'avg_duration': round(result[4] or 0, 1)
                }
            return {}
            
        except Exception as err:
            self.logger.error(f"User stats retrieval error: {err}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

# Global database instance
db_manager = None

def get_db_manager():
    """Get or create database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager