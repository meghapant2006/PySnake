#!/usr/bin/env python3
"""
Database Viewer for PySnake
This script helps you view user data and game statistics
"""

import os
import sys
from database_manager import get_db_manager

def print_separator(title=""):
    """Print a nice separator line"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*50)

def view_users():
    """Display all users in the database"""
    print_separator("USERS")
    
    db = get_db_manager()
    if not db.connection:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = db.connection.cursor()
        placeholder = "?" if db.is_sqlite else "%s"
        
        # Get all users
        cursor.execute("SELECT id, username, email, created_at, last_login FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        if not users:
            print("📭 No users found in database")
            return
        
        print(f"👥 Found {len(users)} users:")
        print(f"{'ID':<4} {'Username':<15} {'Email':<25} {'Created':<20} {'Last Login':<20}")
        print("-" * 90)
        
        for user in users:
            user_id, username, email, created_at, last_login = user
            created_str = str(created_at)[:19] if created_at else "Unknown"
            login_str = str(last_login)[:19] if last_login else "Never"
            print(f"{user_id:<4} {username:<15} {email:<25} {created_str:<20} {login_str:<20}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error viewing users: {e}")

def view_high_scores():
    """Display high scores"""
    print_separator("HIGH SCORES")
    
    db = get_db_manager()
    if not db.connection:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = db.connection.cursor()
        placeholder = "?" if db.is_sqlite else "%s"
        
        # Get top scores with usernames
        if db.is_sqlite:
            query = """
                SELECT u.username, h.score, h.snake_length, h.game_duration,
                       strftime('%Y-%m-%d %H:%M', h.achieved_at) as achieved_date
                FROM high_scores h
                JOIN users u ON h.user_id = u.id
                ORDER BY h.score DESC
                LIMIT 20
            """
        else:
            query = """
                SELECT u.username, h.score, h.snake_length, h.game_duration,
                       DATE_FORMAT(h.achieved_at, '%Y-%m-%d %H:%i') as achieved_date
                FROM high_scores h
                JOIN users u ON h.user_id = u.id
                ORDER BY h.score DESC
                LIMIT 20
            """
        
        cursor.execute(query)
        scores = cursor.fetchall()
        
        if not scores:
            print("📭 No scores found in database")
            return
        
        print(f"🏆 Top {len(scores)} High Scores:")
        print(f"{'Rank':<5} {'Player':<15} {'Score':<8} {'Length':<8} {'Duration':<10} {'Date':<17}")
        print("-" * 75)
        
        for i, score in enumerate(scores, 1):
            username, score_val, length, duration, date = score
            duration_str = f"{duration}s" if duration else "N/A"
            print(f"{i:<5} {username:<15} {score_val:<8} {length:<8} {duration_str:<10} {date:<17}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error viewing scores: {e}")

def view_user_stats():
    """Display user statistics"""
    print_separator("USER STATISTICS")
    
    db = get_db_manager()
    if not db.connection:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = db.connection.cursor()
        
        # Get user statistics
        query = """
            SELECT u.username,
                   COUNT(h.id) as total_games,
                   COALESCE(MAX(h.score), 0) as best_score,
                   COALESCE(AVG(h.score), 0) as avg_score,
                   COALESCE(MAX(h.snake_length), 0) as longest_snake,
                   COALESCE(AVG(h.game_duration), 0) as avg_duration
            FROM users u
            LEFT JOIN high_scores h ON u.id = h.user_id
            GROUP BY u.id, u.username
            ORDER BY best_score DESC
        """
        
        cursor.execute(query)
        stats = cursor.fetchall()
        
        if not stats:
            print("📭 No user statistics found")
            return
        
        print(f"📊 User Statistics:")
        print(f"{'Player':<15} {'Games':<7} {'Best':<7} {'Avg':<7} {'Max Len':<8} {'Avg Time':<9}")
        print("-" * 65)
        
        for stat in stats:
            username, games, best, avg, max_len, avg_time = stat
            avg_str = f"{avg:.1f}" if avg > 0 else "0.0"
            time_str = f"{avg_time:.1f}s" if avg_time > 0 else "0.0s"
            print(f"{username:<15} {games:<7} {best:<7} {avg_str:<7} {max_len:<8} {time_str:<9}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error viewing statistics: {e}")

def search_user():
    """Search for a specific user"""
    print_separator("USER SEARCH")
    
    username = input("🔍 Enter username to search: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return
    
    db = get_db_manager()
    if not db.connection:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = db.connection.cursor()
        placeholder = "?" if db.is_sqlite else "%s"
        
        # Find user
        cursor.execute(f"SELECT id, username, email, created_at, last_login FROM users WHERE username = {placeholder}", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User '{username}' not found")
            cursor.close()
            return
        
        user_id, username, email, created_at, last_login = user
        print(f"✅ Found user: {username}")
        print(f"   ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Created: {created_at}")
        print(f"   Last Login: {last_login}")
        
        # Get user's scores
        cursor.execute(f"""
            SELECT score, snake_length, game_duration, achieved_at
            FROM high_scores
            WHERE user_id = {placeholder}
            ORDER BY achieved_at DESC
            LIMIT 10
        """, (user_id,))
        
        scores = cursor.fetchall()
        
        if scores:
            print(f"\n🎮 Recent Games (Last {len(scores)}):")
            print(f"{'Score':<8} {'Length':<8} {'Duration':<10} {'Date':<20}")
            print("-" * 50)
            
            for score, length, duration, date in scores:
                duration_str = f"{duration}s" if duration else "N/A"
                date_str = str(date)[:19] if date else "Unknown"
                print(f"{score:<8} {length:<8} {duration_str:<10} {date_str:<20}")
        else:
            print(f"\n📭 No games found for {username}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error searching user: {e}")

def database_info():
    """Show database information"""
    print_separator("DATABASE INFO")
    
    db = get_db_manager()
    
    if not db.connection:
        print("❌ Cannot connect to database!")
        return
    
    print(f"📊 Database Type: {'SQLite' if db.is_sqlite else 'MySQL'}")
    
    if db.is_sqlite:
        print("📂 Database File: snake_game.db")
    else:
        print(f"🖥️  Host: {db.host}")
        print(f"👤 User: {db.user}")
        print(f"🗄️  Database: {db.database}")
    
    try:
        cursor = db.connection.cursor()
        
        # Count users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        # Count scores
        cursor.execute("SELECT COUNT(*) FROM high_scores")
        score_count = cursor.fetchone()[0]
        
        print(f"👥 Total Users: {user_count}")
        print(f"🎮 Total Games: {score_count}")
        
        if score_count > 0:
            # Get highest score
            cursor.execute("SELECT MAX(score) FROM high_scores")
            max_score = cursor.fetchone()[0]
            print(f"🏆 Highest Score: {max_score}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")

def main_menu():
    """Display main menu"""
    while True:
        print_separator("PYSNAKE DATABASE VIEWER")
        print("📋 Choose an option:")
        print("1. 👥 View All Users")
        print("2. 🏆 View High Scores")
        print("3. 📊 View User Statistics")
        print("4. 🔍 Search Specific User")
        print("5. 🗄️  Database Information")
        print("6. 🚪 Exit")
        
        choice = input("\n➤ Enter your choice (1-6): ").strip()
        
        if choice == '1':
            view_users()
        elif choice == '2':
            view_high_scores()
        elif choice == '3':
            view_user_stats()
        elif choice == '4':
            search_user()
        elif choice == '5':
            database_info()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\n📍 Press Enter to continue...")

if __name__ == "__main__":
    print("🐍 PySnake Database Viewer")
    print("=" * 40)
    
    # Check if database file exists for SQLite
    if os.path.exists("snake_game.db"):
        print("✅ SQLite database found")
    else:
        print("ℹ️  No SQLite database found (will be created when game runs)")
    
    main_menu()