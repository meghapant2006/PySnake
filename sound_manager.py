import pygame
import numpy as np

class SoundManager:
    """Simple sound effect generator using pygame's sound capabilities"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.eat_sound = self.create_eat_sound()
        self.game_over_sound = self.create_game_over_sound()
        
    def create_eat_sound(self):
        """Create a pleasant 'eat' sound effect"""
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create a cheerful beep sound
        frequency = 800
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Fade out effect
            amplitude = 0.3 * (1 - i / frames)
            # Add slight frequency modulation for more pleasant sound
            freq_mod = frequency + (frequency * 0.1 * np.sin(2 * np.pi * i * 10 / sample_rate))
            wave = amplitude * np.sin(2 * np.pi * freq_mod * i / sample_rate)
            arr[i] = [wave, wave]
        
        # Convert to integer format
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def create_game_over_sound(self):
        """Create a game over sound effect"""
        duration = 1.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2))
        
        # Create a descending tone
        for i in range(frames):
            # Descending frequency from 400Hz to 100Hz
            progress = i / frames
            frequency = 400 - (300 * progress)
            amplitude = 0.2 * (1 - progress * 0.7)  # Fade out gradually
            
            wave = amplitude * np.sin(2 * np.pi * frequency * i / sample_rate)
            arr[i] = [wave, wave]
        
        # Convert to integer format
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def play_eat_sound(self):
        """Play the eat sound effect"""
        try:
            self.eat_sound.play()
        except:
            pass  # Fail silently if sound can't play
    
    def play_game_over_sound(self):
        """Play the game over sound effect"""
        try:
            self.game_over_sound.play()
        except:
            pass  # Fail silently if sound can't play