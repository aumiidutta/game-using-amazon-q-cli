import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
BOARD_SIZE = 600
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 50
CELL_SIZE = BOARD_SIZE // 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class SnakeLadderGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🎵 Snake & Ladder with Music! 🎵")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize simple audio
        self.init_simple_audio()
        
        # Game state
        self.current_player = 0
        self.players = [
            {"name": "Player 1", "position": 0, "color": RED, "moves": 0},
            {"name": "Player 2", "position": 0, "color": BLUE, "moves": 0}
        ]
        self.dice_value = 1
        self.game_over = False
        self.winner = None
        self.dice_rolling = False
        self.animation_counter = 0
        self.move_history = []
        self.sound_enabled = True
        self.music_enabled = True
        
        # Enhanced snakes and ladders
        self.snakes = {
            16: {"end": 6, "desc": "Greed"},
            47: {"end": 26, "desc": "Anger"}, 
            49: {"end": 11, "desc": "Pride"},
            56: {"end": 53, "desc": "Lust"},
            62: {"end": 19, "desc": "Theft"},
            64: {"end": 60, "desc": "Lies"},
            87: {"end": 24, "desc": "Murder"},
            93: {"end": 73, "desc": "Ego"},
            95: {"end": 75, "desc": "Vanity"},
            98: {"end": 78, "desc": "Cruelty"}
        }
        
        self.ladders = {
            1: {"end": 38, "desc": "Faith"},
            4: {"end": 14, "desc": "Reliability"},
            9: {"end": 21, "desc": "Generosity"},
            21: {"end": 42, "desc": "Knowledge"},
            28: {"end": 84, "desc": "Asceticism"},
            36: {"end": 44, "desc": "Humility"},
            51: {"end": 67, "desc": "Truthfulness"},
            71: {"end": 91, "desc": "Devotion"},
            80: {"end": 100, "desc": "Enlightenment"}
        }
        
        # Buttons
        self.dice_button = pygame.Rect(650, 300, 100, 50)
        self.music_button = pygame.Rect(650, 360, 100, 30)
        
    def init_simple_audio(self):
        """Initialize simple audio without external dependencies"""
        try:
            # Create simple beep sounds using pygame's built-in capabilities
            self.create_simple_background_music()
            
            # Start background music
            if self.music_enabled:
                pygame.mixer.music.play(-1)  # Loop indefinitely
                pygame.mixer.music.set_volume(0.3)
                
        except Exception as e:
            print(f"Audio initialization failed: {e}")
            self.sound_enabled = False
            self.music_enabled = False
    
    def create_simple_background_music(self):
        """Create a simple background music track using basic tones"""
        try:
            # Create a simple WAV file with basic tones
            import wave
            import struct
            
            sample_rate = 22050
            duration = 4.0  # 4 second loop
            frames = int(duration * sample_rate)
            
            # Simple melody frequencies
            melody = [523, 587, 659, 698]  # C-D-E-F
            note_duration = duration / len(melody)
            
            with wave.open('/tmp/simple_bg_music.wav', 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                
                for i in range(frames):
                    t = i / sample_rate
                    note_index = int(t / note_duration) % len(melody)
                    frequency = melody[note_index]
                    
                    # Create sine wave
                    wave_value = math.sin(2 * math.pi * frequency * t)
                    # Make it very quiet
                    sample = int(wave_value * 3276)  # 10% volume
                    
                    wav_file.writeframes(struct.pack('<h', sample))
            
            pygame.mixer.music.load('/tmp/simple_bg_music.wav')
            
        except Exception as e:
            print(f"Could not create background music: {e}")
            self.music_enabled = False
    
    def play_beep(self, frequency=800, duration=0.1):
        """Play a simple beep sound"""
        if not self.sound_enabled:
            return
            
        try:
            # Create a simple beep using pygame's mixer
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            import wave
            import struct
            
            with wave.open('/tmp/beep.wav', 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                
                for i in range(frames):
                    t = i / sample_rate
                    wave_value = math.sin(2 * math.pi * frequency * t)
                    # Apply fade out
                    fade = max(0, 1 - (t / duration))
                    sample = int(wave_value * fade * 16383)
                    wav_file.writeframes(struct.pack('<h', sample))
            
            # Play the beep
            beep_sound = pygame.mixer.Sound('/tmp/beep.wav')
            beep_sound.play()
            
        except:
            pass  # Ignore sound errors
    
    def toggle_music(self):
        """Toggle background music"""
        if self.music_enabled:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
    
    def toggle_sound(self):
        """Toggle sound effects"""
        self.sound_enabled = not self.sound_enabled
    
    def get_board_position(self, cell_number):
        """Convert cell number to screen coordinates"""
        if cell_number == 0:
            return BOARD_OFFSET_X - 30, BOARD_OFFSET_Y + BOARD_SIZE + 10
        
        cell_number -= 1
        row = 9 - (cell_number // 10)
        col = cell_number % 10
        
        if (9 - row) % 2 == 1:
            col = 9 - col
            
        x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
        
        return x, y
    
    def draw_board(self):
        """Draw the game board"""
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        
        for i in range(10):
            for j in range(10):
                cell_rect = pygame.Rect(
                    BOARD_OFFSET_X + j * CELL_SIZE,
                    BOARD_OFFSET_Y + i * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                row = 9 - i
                col = j if row % 2 == 0 else 9 - j
                cell_number = row * 10 + col + 1
                
                # Color special cells
                if cell_number in self.snakes:
                    pygame.draw.rect(self.screen, (255, 200, 200), cell_rect)
                elif cell_number in self.ladders:
                    pygame.draw.rect(self.screen, (200, 255, 200), cell_rect)
                else:
                    color = (245, 245, 245) if (i + j) % 2 == 0 else WHITE
                    pygame.draw.rect(self.screen, color, cell_rect)
                
                pygame.draw.rect(self.screen, BLACK, cell_rect, 1)
                
                # Draw cell number
                text = self.font.render(str(cell_number), True, BLACK)
                text_rect = text.get_rect(center=(cell_rect.centerx, cell_rect.y + 15))
                self.screen.blit(text, text_rect)
    
    def draw_snakes_and_ladders(self):
        """Draw snakes and ladders"""
        # Draw ladders
        for start, ladder_info in self.ladders.items():
            end = ladder_info["end"]
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            pygame.draw.line(self.screen, GREEN, start_pos, end_pos, 6)
            
            # Draw rungs
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            length = math.sqrt(dx*dx + dy*dy)
            steps = max(3, int(length // 25))
            
            for i in range(1, steps):
                t = i / steps
                x = start_pos[0] + t * dx
                y = start_pos[1] + t * dy
                perp_x = -dy / length * 12
                perp_y = dx / length * 12
                pygame.draw.line(self.screen, GREEN, 
                               (x - perp_x, y - perp_y), 
                               (x + perp_x, y + perp_y), 3)
        
        # Draw snakes
        for start, snake_info in self.snakes.items():
            end = snake_info["end"]
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            
            # Simple curved snake
            mid_x = (start_pos[0] + end_pos[0]) // 2 + random.randint(-20, 20)
            mid_y = (start_pos[1] + end_pos[1]) // 2 + random.randint(-20, 20)
            
            pygame.draw.line(self.screen, RED, start_pos, (mid_x, mid_y), 8)
            pygame.draw.line(self.screen, RED, (mid_x, mid_y), end_pos, 8)
            pygame.draw.circle(self.screen, RED, start_pos, 10)
            pygame.draw.circle(self.screen, DARK_GRAY, end_pos, 6)
    
    def draw_players(self):
        """Draw player pieces"""
        for i, player in enumerate(self.players):
            if player["position"] > 0:
                x, y = self.get_board_position(player["position"])
            else:
                x, y = self.get_board_position(0)
            
            offset_x = 15 if i == 0 else -15
            
            # Glow for current player
            if i == self.current_player and not self.game_over:
                pygame.draw.circle(self.screen, YELLOW, (x + offset_x, y), 16)
            
            pygame.draw.circle(self.screen, player["color"], (x + offset_x, y), 12)
            pygame.draw.circle(self.screen, BLACK, (x + offset_x, y), 12, 2)
            
            # Player number
            num_text = self.small_font.render(str(i+1), True, WHITE)
            num_rect = num_text.get_rect(center=(x + offset_x, y))
            self.screen.blit(num_text, num_rect)
    
    def draw_dice(self):
        """Draw dice and controls"""
        # Dice
        dice_rect = pygame.Rect(650, 200, 60, 60)
        pygame.draw.rect(self.screen, WHITE, dice_rect)
        pygame.draw.rect(self.screen, BLACK, dice_rect, 3)
        
        if self.dice_rolling:
            offset = random.randint(-2, 2)
            dice_rect.x += offset
            dice_rect.y += offset
        
        self.draw_dice_dots(dice_rect, self.dice_value)
        
        # Roll button
        button_color = LIGHT_GRAY if not self.dice_rolling else DARK_GRAY
        pygame.draw.rect(self.screen, button_color, self.dice_button)
        pygame.draw.rect(self.screen, BLACK, self.dice_button, 2)
        
        button_text = "ROLL DICE" if not self.dice_rolling else "ROLLING..."
        text = self.font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center=self.dice_button.center)
        self.screen.blit(text, text_rect)
        
        # Music button
        music_color = GREEN if pygame.mixer.music.get_busy() else RED
        pygame.draw.rect(self.screen, music_color, self.music_button)
        pygame.draw.rect(self.screen, BLACK, self.music_button, 2)
        
        music_text = "♪ ON" if pygame.mixer.music.get_busy() else "♪ OFF"
        music_label = self.small_font.render(music_text, True, BLACK)
        music_rect = music_label.get_rect(center=self.music_button.center)
        self.screen.blit(music_label, music_rect)
    
    def draw_dice_dots(self, rect, value):
        """Draw dice dots"""
        center_x, center_y = rect.center
        dot_positions = {
            1: [(center_x, center_y)],
            2: [(center_x - 15, center_y - 15), (center_x + 15, center_y + 15)],
            3: [(center_x - 15, center_y - 15), (center_x, center_y), (center_x + 15, center_y + 15)],
            4: [(center_x - 15, center_y - 15), (center_x + 15, center_y - 15), 
                (center_x - 15, center_y + 15), (center_x + 15, center_y + 15)],
            5: [(center_x - 15, center_y - 15), (center_x + 15, center_y - 15), (center_x, center_y),
                (center_x - 15, center_y + 15), (center_x + 15, center_y + 15)],
            6: [(center_x - 15, center_y - 15), (center_x + 15, center_y - 15),
                (center_x - 15, center_y), (center_x + 15, center_y),
                (center_x - 15, center_y + 15), (center_x + 15, center_y + 15)]
        }
        
        for pos in dot_positions[value]:
            pygame.draw.circle(self.screen, BLACK, pos, 4)
    
    def draw_ui(self):
        """Draw UI elements"""
        # Title with music note
        title = self.big_font.render("🎵 Snake & Ladder with Music! 🎵", True, BLACK)
        self.screen.blit(title, (180, 10))
        
        # Player info
        y_offset = 700
        for i, player in enumerate(self.players):
            color = player["color"] if i == self.current_player else DARK_GRAY
            text = f"{player['name']}: Position {player['position']} (Moves: {player['moves']})"
            if i == self.current_player and not self.game_over:
                text += " ⭐"
            
            player_text = self.font.render(text, True, color)
            self.screen.blit(player_text, (50, y_offset + i * 30))
            
            pygame.draw.circle(self.screen, player["color"], (30, y_offset + i * 30 + 10), 10)
            pygame.draw.circle(self.screen, BLACK, (30, y_offset + i * 30 + 10), 10, 2)
        
        # Game status
        if self.game_over:
            winner_text = self.big_font.render(f"🎉 {self.winner} Wins! 🎉", True, GREEN)
            self.screen.blit(winner_text, (250, 750))
            restart_text = self.font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, (320, 780))
        else:
            turn_text = self.font.render(f"Current Turn: {self.players[self.current_player]['name']}", True, BLACK)
            self.screen.blit(turn_text, (300, 750))
        
        # Controls
        controls = self.small_font.render("SPACE=Roll | M=Music | S=Sound | ESC=Quit", True, DARK_GRAY)
        self.screen.blit(controls, (50, 850))
        
        # Move history
        if self.move_history:
            history = self.small_font.render("Last: " + self.move_history[-1], True, DARK_GRAY)
            self.screen.blit(history, (50, 670))
    
    def roll_dice(self):
        """Roll dice"""
        if not self.dice_rolling and not self.game_over:
            self.dice_rolling = True
            self.animation_counter = 30
            self.play_beep(600, 0.2)  # Dice roll sound
    
    def move_player(self, player_index, steps):
        """Move player"""
        player = self.players[player_index]
        old_position = player["position"]
        new_position = player["position"] + steps
        player["moves"] += 1
        
        if new_position >= 100:
            player["position"] = 100
            self.game_over = True
            self.winner = player["name"]
            self.move_history.append(f"{player['name']} won!")
            self.play_beep(800, 0.5)  # Victory sound
            return
        
        player["position"] = new_position
        move_desc = f"{player['name']}: {old_position}→{new_position}"
        self.play_beep(400, 0.1)  # Move sound
        
        # Check snakes/ladders
        if new_position in self.snakes:
            snake_end = self.snakes[new_position]["end"]
            player["position"] = snake_end
            move_desc += f" 🐍→{snake_end}"
            self.play_beep(200, 0.3)  # Snake sound (low frequency)
        elif new_position in self.ladders:
            ladder_end = self.ladders[new_position]["end"]
            player["position"] = ladder_end
            move_desc += f" 🪜→{ladder_end}"
            self.play_beep(1000, 0.3)  # Ladder sound (high frequency)
        
        self.move_history.append(move_desc)
        if len(self.move_history) > 3:
            self.move_history.pop(0)
    
    def next_turn(self):
        """Next player turn"""
        self.current_player = (self.current_player + 1) % len(self.players)
    
    def restart_game(self):
        """Restart game"""
        for player in self.players:
            player["position"] = 0
            player["moves"] = 0
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.dice_value = 1
        self.dice_rolling = False
        self.move_history = []
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.dice_button.collidepoint(event.pos):
                    self.roll_dice()
                elif self.music_button.collidepoint(event.pos):
                    self.toggle_music()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE:
                    self.roll_dice()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_m:
                    self.toggle_music()
                elif event.key == pygame.K_s:
                    self.toggle_sound()
        return True
    
    def update(self):
        """Update game"""
        if self.dice_rolling:
            self.animation_counter -= 1
            if self.animation_counter > 0:
                self.dice_value = random.randint(1, 6)
            else:
                self.dice_rolling = False
                self.dice_value = random.randint(1, 6)
                
                self.move_player(self.current_player, self.dice_value)
                
                if self.dice_value != 6 and not self.game_over:
                    self.next_turn()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            
            self.screen.fill(LIGHT_GRAY)
            self.draw_board()
            self.draw_snakes_and_ladders()
            self.draw_players()
            self.draw_dice()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎮 Starting Snake & Ladder with Music!")
    print("🎵 Background music and sound effects included!")
    print("🎯 Controls: SPACE=Roll, M=Music, S=Sound, ESC=Quit")
    game = SnakeLadderGame()
    game.run()
