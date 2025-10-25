import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple, Optional
import math
import time
from sound_manager import SoundManager

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors (Modern color palette)
class Colors:
    # Background and UI
    BACKGROUND = (15, 15, 35)      # Dark navy
    GRID_LINE = (30, 30, 60)       # Darker navy for grid
    UI_BACKGROUND = (25, 25, 50)   # UI panel background
    
    # Snake colors (gradient)
    SNAKE_HEAD = (100, 255, 100)   # Bright green
    SNAKE_BODY = (50, 200, 50)     # Medium green
    SNAKE_TAIL = (30, 150, 30)     # Dark green
    
    # Food colors
    FOOD = (255, 100, 100)         # Bright red
    FOOD_GLOW = (255, 150, 150)    # Light red glow
    
    # Text colors
    TEXT_PRIMARY = (255, 255, 255) # White
    TEXT_SECONDARY = (200, 200, 200) # Light gray
    TEXT_ACCENT = (100, 255, 100)  # Green accent
    
    # Game over
    GAME_OVER_BG = (0, 0, 0)       # Black with transparency
    GAME_OVER_TEXT = (255, 100, 100) # Red

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # Start in the middle of the screen
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        
        self.body = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
        self.direction = Direction.RIGHT
        self.grow_pending = 0
        
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def change_direction(self, new_direction: Direction):
        # Prevent moving backwards into itself
        if len(self.body) > 1:
            dx, dy = new_direction.value
            current_dx, current_dy = self.direction.value
            if (dx, dy) != (-current_dx, -current_dy):
                self.direction = new_direction
        else:
            self.direction = new_direction
    
    def grow(self, amount=1):
        self.grow_pending += amount
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        # Self collision
        if (head_x, head_y) in self.body[1:]:
            return True
        
        return False
    
    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            if i == 0:  # Head
                # Draw head with glow effect
                glow_rect = pygame.Rect(x * GRID_SIZE - 2, y * GRID_SIZE - 2, 
                                       GRID_SIZE + 4, GRID_SIZE + 4)
                pygame.draw.rect(screen, Colors.SNAKE_BODY, glow_rect, border_radius=8)
                pygame.draw.rect(screen, Colors.SNAKE_HEAD, rect, border_radius=6)
                
                # Draw eyes
                eye_size = 3
                eye_offset = 5
                if self.direction == Direction.RIGHT:
                    eye1_pos = (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset)
                    eye2_pos = (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset)
                elif self.direction == Direction.LEFT:
                    eye1_pos = (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset)
                    eye2_pos = (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset)
                elif self.direction == Direction.UP:
                    eye1_pos = (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset)
                    eye2_pos = (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset)
                else:  # DOWN
                    eye1_pos = (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset)
                    eye2_pos = (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset)
                
                pygame.draw.circle(screen, (255, 255, 255), eye1_pos, eye_size)
                pygame.draw.circle(screen, (255, 255, 255), eye2_pos, eye_size)
                pygame.draw.circle(screen, (0, 0, 0), eye1_pos, eye_size-1)
                pygame.draw.circle(screen, (0, 0, 0), eye2_pos, eye_size-1)
                
            else:  # Body
                # Gradient effect for body segments
                intensity = max(0.3, 1.0 - (i / len(self.body)) * 0.7)
                body_color = (
                    int(Colors.SNAKE_BODY[0] * intensity),
                    int(Colors.SNAKE_BODY[1] * intensity),
                    int(Colors.SNAKE_BODY[2] * intensity)
                )
                pygame.draw.rect(screen, body_color, rect, border_radius=4)
                
                # Add inner highlight
                inner_rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, 
                                       GRID_SIZE - 4, GRID_SIZE - 4)
                highlight_color = (
                    min(255, int(body_color[0] * 1.3)),
                    min(255, int(body_color[1] * 1.3)),
                    min(255, int(body_color[2] * 1.3))
                )
                pygame.draw.rect(screen, highlight_color, inner_rect, border_radius=2)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.animation_offset = 0
        
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    
    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, screen):
        x, y = self.position
        
        # Animated pulsing effect
        self.animation_offset += 0.2
        pulse = math.sin(self.animation_offset) * 2
        
        # Glow effect
        glow_size = GRID_SIZE + 8 + pulse
        glow_rect = pygame.Rect(x * GRID_SIZE - 4 - pulse/2, y * GRID_SIZE - 4 - pulse/2, 
                               glow_size, glow_size)
        pygame.draw.rect(screen, Colors.FOOD_GLOW, glow_rect, border_radius=8)
        
        # Main food
        food_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, Colors.FOOD, food_rect, border_radius=6)
        
        # Inner highlight
        highlight_rect = pygame.Rect(x * GRID_SIZE + 3, y * GRID_SIZE + 3, 
                                   GRID_SIZE - 6, GRID_SIZE - 6)
        pygame.draw.rect(screen, (255, 180, 180), highlight_rect, border_radius=4)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PySnake - Classic Snake Game!")
        
        # Game fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Sound manager
        try:
            self.sound_manager = SoundManager()
            self.sound_enabled = True
        except:
            self.sound_manager = None
            self.sound_enabled = False
        
        # Game state
        self.clock = pygame.time.Clock()
        self.game_start_time = None
        self.high_score = 0  # Simple high score tracking in memory
        
        self.reset_game()
        self.game_over = False
        self.paused = False
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.game_start_time = time.time()
        
        # Ensure food doesn't spawn on snake
        while self.food.position in self.snake.body:
            self.food.respawn(self.snake.body)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def update(self):
        if not self.game_over and not self.paused:
            self.snake.move()
            
            # Check collision
            if self.snake.check_collision():
                self.game_over = True
                # Update high score if current score is better
                if self.score > self.high_score:
                    self.high_score = self.score
                
                # Play game over sound
                if self.sound_enabled and self.sound_manager:
                    self.sound_manager.play_game_over_sound()
                return
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.score += 10
                self.snake.grow(1)
                self.food.respawn(self.snake.body)
                # Play eat sound
                if self.sound_enabled and self.sound_manager:
                    self.sound_manager.play_eat_sound()
    
    def draw_grid(self):
        # Draw subtle grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (0, y), (WINDOW_WIDTH, y))
    
    def draw_ui(self):
        # Current score
        score_text = self.font_medium.render(f"Score: {self.score}", True, Colors.TEXT_PRIMARY)
        self.screen.blit(score_text, (10, 10))
        
        # Length
        length_text = self.font_small.render(f"Length: {len(self.snake.body)}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(length_text, (10, 40))
        
        # High score
        if self.high_score > 0:
            high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, Colors.TEXT_ACCENT)
            self.screen.blit(high_score_text, (10, 65))
            
            # New high score indicator
            if self.score > self.high_score:
                new_record_text = self.font_small.render("NEW RECORD!", True, Colors.FOOD)
                self.screen.blit(new_record_text, (10, 85))
        
        # Game time
        if self.game_start_time:
            elapsed_time = int(time.time() - self.game_start_time)
            time_text = self.font_small.render(f"Time: {elapsed_time}s", True, Colors.TEXT_SECONDARY)
            time_rect = time_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
            self.screen.blit(time_text, time_rect)
        
        # Controls hint
        if self.score == 0 and not self.game_over:
            controls_text = self.font_small.render("WASD/Arrows: Move | SPACE: Pause | ESC: Exit", True, Colors.TEXT_SECONDARY)
            text_rect = controls_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 20))
            self.screen.blit(controls_text, text_rect)
        
        # Pause indicator
        if self.paused:
            pause_text = self.font_large.render("PAUSED", True, Colors.TEXT_ACCENT)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            
            # Semi-transparent background
            s = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            s.set_alpha(128)
            s.fill(Colors.GAME_OVER_BG)
            bg_rect = s.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(s, bg_rect)
            
            self.screen.blit(pause_text, text_rect)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.GAME_OVER_BG)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.GAME_OVER_TEXT)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, Colors.TEXT_PRIMARY)
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
        self.screen.blit(final_score_text, score_rect)
        
        # Length achieved
        length_text = self.font_medium.render(f"Length Achieved: {len(self.snake.body)}", True, Colors.TEXT_PRIMARY)
        length_rect = length_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
        self.screen.blit(length_text, length_rect)
        
        # Game duration
        if self.game_start_time:
            game_duration = int(time.time() - self.game_start_time)
            duration_text = self.font_medium.render(f"Time Played: {game_duration}s", True, Colors.TEXT_PRIMARY)
            duration_rect = duration_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(duration_text, duration_rect)
        
        # High score achievement
        if self.score > 0 and self.score >= self.high_score:
            achievement_text = self.font_small.render("🏆 NEW HIGH SCORE! 🏆", True, Colors.TEXT_ACCENT)
            achievement_rect = achievement_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
            self.screen.blit(achievement_text, achievement_rect)
        
        # Restart instructions
        restart_text = self.font_small.render("SPACE: Play Again | ESC: Exit", True, Colors.TEXT_SECONDARY)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        # Clear screen
        self.screen.fill(Colors.BACKGROUND)
        
        # Draw grid
        self.draw_grid()
        
        # Draw game objects
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Control game speed
            self.clock.tick(10)  # 10 FPS for classic snake feel
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to start the Snake game"""
    print("Starting PySnake - Classic Snake Game!")
    print("\nFeatures:")
    print("  - Classic snake gameplay")
    print("  - High score tracking")
    print("  - Modern graphics and sound")
    print("\nControls:")
    print("  - Use WASD or Arrow Keys to move")
    print("  - SPACE to pause/unpause")
    print("  - ESC to exit")
    print("  - When game over: SPACE to restart")
    print("\nStarting game...")
    
    # Start the game directly
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()