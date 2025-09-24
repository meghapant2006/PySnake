import pygame
import sys
from typing import Optional, Tuple
from database_manager import get_db_manager
import re

class AuthScreen:
    """Authentication screen for login and signup"""
    
    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PySnake - Login")
        
        # Colors
        self.colors = {
            'background': (20, 25, 40),
            'panel': (35, 45, 65),
            'panel_border': (60, 80, 110),
            'button': (70, 130, 180),
            'button_hover': (100, 150, 200),
            'button_active': (50, 100, 150),
            'text': (255, 255, 255),
            'text_secondary': (200, 200, 200),
            'input_bg': (45, 55, 75),
            'input_border': (80, 100, 130),
            'input_focus': (100, 180, 100),
            'error': (255, 100, 100),
            'success': (100, 255, 100)
        }
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Input fields
        self.input_fields = {
            'username': {'value': '', 'active': False, 'rect': None},
            'email': {'value': '', 'active': False, 'rect': None},
            'password': {'value': '', 'active': False, 'rect': None},
            'confirm_password': {'value': '', 'active': False, 'rect': None}
        }
        
        # UI state
        self.current_screen = 'login'  # 'login' or 'signup'
        self.message = ''
        self.message_color = self.colors['text']
        self.buttons = {}
        
        # Database manager
        self.db = get_db_manager()
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI elements positions"""
        center_x = self.screen_width // 2
        
        # Input field dimensions
        field_width = 300
        field_height = 40
        field_spacing = 60
        
        # Calculate starting Y position for centered layout
        if self.current_screen == 'login':
            num_fields = 2
        else:
            num_fields = 4
        
        total_height = (num_fields * field_height) + ((num_fields - 1) * (field_spacing - field_height)) + 200
        start_y = (self.screen_height - total_height) // 2 + 50
        
        # Username field
        self.input_fields['username']['rect'] = pygame.Rect(
            center_x - field_width // 2, start_y, field_width, field_height
        )
        
        # Email field (only for signup)
        if self.current_screen == 'signup':
            self.input_fields['email']['rect'] = pygame.Rect(
                center_x - field_width // 2, start_y + field_spacing, field_width, field_height
            )
            password_y = start_y + field_spacing * 2
        else:
            self.input_fields['email']['rect'] = None
            password_y = start_y + field_spacing
        
        # Password field
        self.input_fields['password']['rect'] = pygame.Rect(
            center_x - field_width // 2, password_y, field_width, field_height
        )
        
        # Confirm password field (only for signup)
        if self.current_screen == 'signup':
            self.input_fields['confirm_password']['rect'] = pygame.Rect(
                center_x - field_width // 2, password_y + field_spacing, field_width, field_height
            )
        else:
            self.input_fields['confirm_password']['rect'] = None
        
        # Buttons
        button_width = 120
        button_height = 40
        button_y = password_y + field_spacing + (field_spacing if self.current_screen == 'signup' else 0)
        
        if self.current_screen == 'login':
            self.buttons = {
                'login': pygame.Rect(center_x - button_width - 10, button_y, button_width, button_height),
                'signup_switch': pygame.Rect(center_x + 10, button_y, button_width, button_height)
            }
        else:
            self.buttons = {
                'signup': pygame.Rect(center_x - button_width - 10, button_y, button_width, button_height),
                'login_switch': pygame.Rect(center_x + 10, button_y, button_width, button_height)
            }
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 6
    
    def handle_input(self, event):
        """Handle text input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Switch between input fields
                fields = ['username']
                if self.current_screen == 'signup':
                    fields.extend(['email', 'password', 'confirm_password'])
                else:
                    fields.append('password')
                
                # Find current active field
                current_index = -1
                for i, field in enumerate(fields):
                    if self.input_fields[field]['active']:
                        current_index = i
                        break
                
                # Deactivate all fields
                for field in self.input_fields:
                    self.input_fields[field]['active'] = False
                
                # Activate next field
                next_index = (current_index + 1) % len(fields)
                self.input_fields[fields[next_index]]['active'] = True
                
            elif event.key == pygame.K_RETURN:
                if self.current_screen == 'login':
                    result = self.attempt_login()
                    if result and result[0] is not None:
                        return result
                else:
                    self.attempt_signup()
                    
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace for active field
                for field, data in self.input_fields.items():
                    if data['active'] and data['value']:
                        data['value'] = data['value'][:-1]
                        
        elif event.type == pygame.TEXTINPUT:
            # Add text to active field
            for field, data in self.input_fields.items():
                if data['active']:
                    if len(data['value']) < 50:  # Limit input length
                        data['value'] += event.text
        
        return None
    
    def handle_mouse(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check input field clicks
            for field, data in self.input_fields.items():
                if data['rect'] and data['rect'].collidepoint(mouse_pos):
                    # Deactivate all fields first
                    for f in self.input_fields:
                        self.input_fields[f]['active'] = False
                    # Activate clicked field
                    data['active'] = True
                    return None
            
            # Check button clicks
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    if button_name == 'login':
                        result = self.attempt_login()
                        if result and result[0] is not None:
                            return result
                    elif button_name == 'signup':
                        self.attempt_signup()
                    elif button_name == 'signup_switch':
                        self.switch_to_signup()
                    elif button_name == 'login_switch':
                        self.switch_to_login()
                    return None
            
            # Deactivate all fields if clicking elsewhere
            for field in self.input_fields:
                self.input_fields[field]['active'] = False
        
        return None
    
    def switch_to_signup(self):
        """Switch to signup screen"""
        self.current_screen = 'signup'
        self.message = ''
        self.clear_inputs()
        self.setup_ui()
    
    def switch_to_login(self):
        """Switch to login screen"""
        self.current_screen = 'login'
        self.message = ''
        self.clear_inputs()
        self.setup_ui()
    
    def clear_inputs(self):
        """Clear all input fields"""
        for field in self.input_fields:
            self.input_fields[field]['value'] = ''
            self.input_fields[field]['active'] = False
    
    def attempt_login(self):
        """Attempt to log in user"""
        username = self.input_fields['username']['value'].strip()
        password = self.input_fields['password']['value']
        
        if not username or not password:
            self.show_message("Please fill in all fields", 'error')
            return
        
        success, user_id, message = self.db.authenticate_user(username, password)
        
        if success:
            self.show_message(message, 'success')
            return user_id, username  # Return user info for game
        else:
            self.show_message(message, 'error')
            return None, None
    
    def attempt_signup(self):
        """Attempt to create new user account"""
        username = self.input_fields['username']['value'].strip()
        email = self.input_fields['email']['value'].strip()
        password = self.input_fields['password']['value']
        confirm_password = self.input_fields['confirm_password']['value']
        
        # Validation
        if not username or not email or not password or not confirm_password:
            self.show_message("Please fill in all fields", 'error')
            return
        
        if len(username) < 3:
            self.show_message("Username must be at least 3 characters", 'error')
            return
        
        if not self.validate_email(email):
            self.show_message("Please enter a valid email address", 'error')
            return
        
        if not self.validate_password(password):
            self.show_message("Password must be at least 6 characters", 'error')
            return
        
        if password != confirm_password:
            self.show_message("Passwords do not match", 'error')
            return
        
        success, message = self.db.create_user(username, email, password)
        
        if success:
            self.show_message(message, 'success')
            pygame.time.wait(1000)  # Show success message briefly
            self.switch_to_login()
        else:
            self.show_message(message, 'error')
    
    def show_message(self, message: str, message_type: str = 'info'):
        """Show a message to the user"""
        self.message = message
        if message_type == 'error':
            self.message_color = self.colors['error']
        elif message_type == 'success':
            self.message_color = self.colors['success']
        else:
            self.message_color = self.colors['text']
    
    def draw_input_field(self, field_name: str, label: str, is_password: bool = False):
        """Draw an input field"""
        field_data = self.input_fields[field_name]
        if not field_data['rect']:
            return
        
        rect = field_data['rect']
        is_active = field_data['active']
        
        # Draw field background
        pygame.draw.rect(self.screen, self.colors['input_bg'], rect)
        
        # Draw border
        border_color = self.colors['input_focus'] if is_active else self.colors['input_border']
        pygame.draw.rect(self.screen, border_color, rect, 2)
        
        # Draw label
        label_surface = self.font_small.render(label, True, self.colors['text_secondary'])
        label_rect = label_surface.get_rect()
        label_rect.bottomleft = (rect.left, rect.top - 5)
        self.screen.blit(label_surface, label_rect)
        
        # Draw text
        display_text = field_data['value']
        if is_password and display_text:
            display_text = '*' * len(display_text)
        
        text_surface = self.font_medium.render(display_text, True, self.colors['text'])
        text_rect = text_surface.get_rect()
        text_rect.centery = rect.centery
        text_rect.left = rect.left + 10
        
        # Clip text to field
        self.screen.set_clip(rect)
        self.screen.blit(text_surface, text_rect)
        self.screen.set_clip(None)
        
        # Draw cursor if active
        if is_active:
            cursor_x = text_rect.right + 2
            if cursor_x < rect.right - 10:
                pygame.draw.line(self.screen, self.colors['text'], 
                               (cursor_x, rect.top + 8), (cursor_x, rect.bottom - 8), 2)
    
    def draw_button(self, button_name: str, text: str):
        """Draw a button"""
        if button_name not in self.buttons:
            return
        
        rect = self.buttons[button_name]
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        
        # Draw button background
        color = self.colors['button_hover'] if is_hover else self.colors['button']
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        
        # Draw button border
        pygame.draw.rect(self.screen, self.colors['panel_border'], rect, 2, border_radius=5)
        
        # Draw button text
        text_surface = self.font_medium.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        """Draw the authentication screen"""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw main panel
        panel_width = 400
        panel_height = 500 if self.current_screen == 'signup' else 350
        panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width, panel_height
        )
        
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['panel_border'], panel_rect, 3, border_radius=10)
        
        # Draw title
        title = "Sign Up" if self.current_screen == 'signup' else "Login"
        title_surface = self.font_large.render(f"PySnake - {title}", True, self.colors['text'])
        title_rect = title_surface.get_rect(centerx=self.screen_width // 2, 
                                          y=panel_rect.top + 30)
        self.screen.blit(title_surface, title_rect)
        
        # Draw input fields
        self.draw_input_field('username', 'Username')
        
        if self.current_screen == 'signup':
            self.draw_input_field('email', 'Email')
        
        self.draw_input_field('password', 'Password', is_password=True)
        
        if self.current_screen == 'signup':
            self.draw_input_field('confirm_password', 'Confirm Password', is_password=True)
        
        # Draw buttons
        if self.current_screen == 'login':
            self.draw_button('login', 'Login')
            self.draw_button('signup_switch', 'Sign Up')
        else:
            self.draw_button('signup', 'Sign Up')
            self.draw_button('login_switch', 'Login')
        
        # Draw message
        if self.message:
            message_surface = self.font_small.render(self.message, True, self.message_color)
            message_rect = message_surface.get_rect(centerx=self.screen_width // 2,
                                                   y=panel_rect.bottom + 20)
            self.screen.blit(message_surface, message_rect)
        
        # Draw instructions
        instructions = [
            "Press TAB to switch between fields",
            "Press ENTER to submit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.font_small.render(instruction, True, self.colors['text_secondary'])
            inst_rect = inst_surface.get_rect(centerx=self.screen_width // 2,
                                            y=self.screen_height - 60 + (i * 25))
            self.screen.blit(inst_surface, inst_rect)
        
        pygame.display.flip()
    
    def run(self) -> Tuple[Optional[int], Optional[str]]:
        """Run the authentication screen and return user info if successful"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None, None
                    else:
                        result = self.handle_input(event)
                        if result and result[0] is not None:
                            return result
                
                elif event.type == pygame.TEXTINPUT:
                    self.handle_input(event)
                
                elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                    result = self.handle_mouse(event)
                    if result and result[0] is not None:
                        return result
            
            self.draw()
            self.clock.tick(60)
        
        return None, None

def show_auth_screen() -> Tuple[Optional[int], Optional[str]]:
    """Show authentication screen and return user info"""
    auth_screen = AuthScreen()
    return auth_screen.run()