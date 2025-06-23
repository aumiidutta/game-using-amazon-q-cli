import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

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
        pygame.display.set_caption("Snake and Ladder - Online Gaming Style")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Game state
        self.current_player = 0
        self.players = [
            {"name": "Player 1", "position": 0, "color": RED},
            {"name": "Player 2", "position": 0, "color": BLUE}
        ]
        self.dice_value = 1
        self.game_over = False
        self.winner = None
        self.dice_rolling = False
        self.animation_counter = 0
        
        # Snakes and Ladders positions
        self.snakes = {
            16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78
        }
        self.ladders = {
            1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100
        }
        
        # Button for dice roll
        self.dice_button = pygame.Rect(650, 300, 100, 50)
        
    def get_board_position(self, cell_number):
        """Convert cell number (1-100) to screen coordinates"""
        if cell_number == 0:
            return BOARD_OFFSET_X - 30, BOARD_OFFSET_Y + BOARD_SIZE + 10
        
        cell_number -= 1  # Convert to 0-based indexing
        row = 9 - (cell_number // 10)  # Bottom to top
        col = cell_number % 10
        
        # Reverse direction for odd rows (snake pattern)
        if (9 - row) % 2 == 1:
            col = 9 - col
            
        x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
        
        return x, y
    
    def draw_board(self):
        """Draw the game board with numbers"""
        # Draw board background
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        
        # Draw grid and numbers
        for i in range(10):
            for j in range(10):
                cell_rect = pygame.Rect(
                    BOARD_OFFSET_X + j * CELL_SIZE,
                    BOARD_OFFSET_Y + i * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.screen, WHITE, cell_rect)
                pygame.draw.rect(self.screen, BLACK, cell_rect, 1)
                
                # Calculate cell number
                row = 9 - i
                col = j if row % 2 == 0 else 9 - j
                cell_number = row * 10 + col + 1
                
                # Color special cells
                if cell_number in self.snakes:
                    pygame.draw.rect(self.screen, (255, 200, 200), cell_rect)
                elif cell_number in self.ladders:
                    pygame.draw.rect(self.screen, (200, 255, 200), cell_rect)
                
                # Draw cell number
                text = self.font.render(str(cell_number), True, BLACK)
                text_rect = text.get_rect(center=(cell_rect.centerx, cell_rect.y + 15))
                self.screen.blit(text, text_rect)
    
    def draw_snakes_and_ladders(self):
        """Draw snakes and ladders on the board"""
        # Draw ladders
        for start, end in self.ladders.items():
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            pygame.draw.line(self.screen, GREEN, start_pos, end_pos, 5)
            
            # Draw ladder rungs
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            length = math.sqrt(dx*dx + dy*dy)
            steps = int(length // 20)
            
            for i in range(1, steps):
                t = i / steps
                x = start_pos[0] + t * dx
                y = start_pos[1] + t * dy
                # Draw perpendicular line for rung
                perp_x = -dy / length * 10
                perp_y = dx / length * 10
                pygame.draw.line(self.screen, GREEN, 
                               (x - perp_x, y - perp_y), 
                               (x + perp_x, y + perp_y), 2)
        
        # Draw snakes
        for start, end in self.snakes.items():
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            
            # Draw snake body with curves
            mid_x = (start_pos[0] + end_pos[0]) // 2 + random.randint(-20, 20)
            mid_y = (start_pos[1] + end_pos[1]) // 2 + random.randint(-20, 20)
            
            # Draw snake segments
            pygame.draw.circle(self.screen, RED, start_pos, 8)  # Head
            pygame.draw.line(self.screen, RED, start_pos, (mid_x, mid_y), 6)
            pygame.draw.line(self.screen, RED, (mid_x, mid_y), end_pos, 6)
            pygame.draw.circle(self.screen, DARK_GRAY, end_pos, 5)  # Tail
    
    def draw_players(self):
        """Draw player pieces on the board"""
        for i, player in enumerate(self.players):
            if player["position"] > 0:
                x, y = self.get_board_position(player["position"])
                # Offset players so they don't overlap
                offset_x = 15 if i == 0 else -15
                pygame.draw.circle(self.screen, player["color"], (x + offset_x, y), 12)
                pygame.draw.circle(self.screen, BLACK, (x + offset_x, y), 12, 2)
            else:
                # Draw at start position
                x, y = self.get_board_position(0)
                offset_x = 15 if i == 0 else -15
                pygame.draw.circle(self.screen, player["color"], (x + offset_x, y), 12)
                pygame.draw.circle(self.screen, BLACK, (x + offset_x, y), 12, 2)
    
    def draw_dice(self):
        """Draw dice and roll button"""
        # Draw dice
        dice_rect = pygame.Rect(650, 200, 60, 60)
        pygame.draw.rect(self.screen, WHITE, dice_rect)
        pygame.draw.rect(self.screen, BLACK, dice_rect, 3)
        
        # Draw dice dots
        self.draw_dice_dots(dice_rect, self.dice_value)
        
        # Draw roll button
        button_color = LIGHT_GRAY if not self.dice_rolling else DARK_GRAY
        pygame.draw.rect(self.screen, button_color, self.dice_button)
        pygame.draw.rect(self.screen, BLACK, self.dice_button, 2)
        
        button_text = "ROLL DICE" if not self.dice_rolling else "ROLLING..."
        text = self.font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center=self.dice_button.center)
        self.screen.blit(text, text_rect)
    
    def draw_dice_dots(self, rect, value):
        """Draw dots on dice based on value"""
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
        """Draw game UI elements"""
        # Draw title
        title = self.big_font.render("Snake & Ladder Game", True, BLACK)
        self.screen.blit(title, (250, 10))
        
        # Draw player info
        y_offset = 700
        for i, player in enumerate(self.players):
            color = player["color"] if i == self.current_player else DARK_GRAY
            text = f"{player['name']}: Position {player['position']}"
            if i == self.current_player and not self.game_over:
                text += " (Current Turn)"
            
            player_text = self.font.render(text, True, color)
            self.screen.blit(player_text, (50, y_offset + i * 30))
            
            # Draw player color indicator
            pygame.draw.circle(self.screen, player["color"], (30, y_offset + i * 30 + 10), 8)
        
        # Draw game status
        if self.game_over:
            winner_text = self.big_font.render(f"{self.winner} Wins!", True, GREEN)
            self.screen.blit(winner_text, (300, 750))
            restart_text = self.font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, (320, 780))
        else:
            turn_text = self.font.render(f"Current Turn: {self.players[self.current_player]['name']}", True, BLACK)
            self.screen.blit(turn_text, (300, 750))
    
    def roll_dice(self):
        """Roll the dice"""
        if not self.dice_rolling and not self.game_over:
            self.dice_rolling = True
            self.animation_counter = 30  # Animation frames
    
    def move_player(self, player_index, steps):
        """Move player and handle snakes/ladders"""
        player = self.players[player_index]
        new_position = player["position"] + steps
        
        # Check if player reaches or exceeds 100
        if new_position >= 100:
            player["position"] = 100
            self.game_over = True
            self.winner = player["name"]
            return
        
        player["position"] = new_position
        
        # Check for snakes
        if new_position in self.snakes:
            player["position"] = self.snakes[new_position]
        
        # Check for ladders
        elif new_position in self.ladders:
            player["position"] = self.ladders[new_position]
    
    def next_turn(self):
        """Switch to next player"""
        self.current_player = (self.current_player + 1) % len(self.players)
    
    def restart_game(self):
        """Restart the game"""
        for player in self.players:
            player["position"] = 0
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.dice_value = 1
        self.dice_rolling = False
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.dice_button.collidepoint(event.pos):
                    self.roll_dice()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE:
                    self.roll_dice()
        
        return True
    
    def update(self):
        """Update game state"""
        if self.dice_rolling:
            self.animation_counter -= 1
            # Animate dice rolling
            if self.animation_counter > 0:
                self.dice_value = random.randint(1, 6)
            else:
                # Dice roll finished
                self.dice_rolling = False
                self.dice_value = random.randint(1, 6)
                
                # Move current player
                self.move_player(self.current_player, self.dice_value)
                
                # Switch turns (unless player got 6 or game is over)
                if self.dice_value != 6 and not self.game_over:
                    self.next_turn()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            
            # Draw everything
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
    game = SnakeLadderGame()
    game.run()
