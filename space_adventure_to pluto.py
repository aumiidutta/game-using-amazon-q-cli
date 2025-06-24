import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_AREA_SIZE = 30
CELL_SIZE = 20  # Each pixel in our 30x30 grid will be 20x20 screen pixels
ROCKET_SIZE = 2
OBSTACLE_SIZE = 2
LARGE_OBSTACLE_SIZE = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

# Obstacle types
METEOR = "meteor"
ASTEROID = "asteroid"
COMET = "comet"
STAR = "star"
BLACK_HOLE = "black_hole"
PLANET_ORBIT = "planet_orbit"
PLUTO = "pluto"

class SpaceJourneyGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Journey to Pluto")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game variables
        self.username = ""
        self.estimated_time = ""
        self.difficulty = ""
        self.score = 0  # Starting score
        self.rocket_x = GAME_AREA_SIZE // 2 - 1  # Center horizontally
        self.rocket_y = GAME_AREA_SIZE - 3  # Near bottom
        self.obstacles = []
        self.game_running = False
        self.game_over = False
        self.game_won = False
        self.message = ""
        self.move_counter = 0
        self.distance_traveled = 0
        self.total_distance = 1000  # Distance to Pluto
        
        # Difficulty settings
        self.obstacle_spawn_rate = 0
        self.move_speed = 0
        self.set_difficulty_settings()
        
    def set_difficulty_settings(self):
        """Set game parameters based on difficulty"""
        if self.difficulty == "easy":
            self.obstacle_spawn_rate = 15  # Lower number = more frequent spawning
            self.move_speed = 8  # Higher number = slower movement
        elif self.difficulty == "medium":
            self.obstacle_spawn_rate = 10
            self.move_speed = 6
        elif self.difficulty == "hard":
            self.obstacle_spawn_rate = 7
            self.move_speed = 4
        
    def get_player_input(self):
        """Get username, estimated time, and difficulty from player"""
        print("Welcome to Space Journey to Pluto!")
        
        # Get username
        while not self.username:
            self.username = input("Enter your username: ").strip()
            if not self.username:
                print("Please enter a valid username.")
        
        # Get estimated time
        while not self.estimated_time:
            self.estimated_time = input("Enter estimated time for the journey (e.g., '5 minutes'): ").strip()
            if not self.estimated_time:
                print("Please enter an estimated time.")
        
        # Get difficulty
        while self.difficulty not in ['easy', 'medium', 'hard']:
            self.difficulty = input("Choose difficulty (easy/medium/hard): ").lower().strip()
            if self.difficulty not in ['easy', 'medium', 'hard']:
                print("Please choose 'easy', 'medium', or 'hard'.")
        
        # Set difficulty settings after getting input
        self.set_difficulty_settings()
        
        print(f"\nWelcome {self.username}!")
        print(f"Estimated journey time: {self.estimated_time}")
        print(f"Difficulty: {self.difficulty}")
        print("Use LEFT/RIGHT arrow keys or A/D keys to navigate your spaceship!")
        print("Game starting in 3 seconds...")
        time.sleep(3)
        
    def run(self):
        """Main game loop"""
        self.get_player_input()
        
        running = True
        self.game_running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_running and not self.game_over:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.move_left()
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.move_right()
            
            # Clear screen
            self.screen.fill(BLACK)
            
            if self.game_running:
                if not self.game_over:
                    self.update_game()
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    

    
    def move_left(self):
        """Move rocket left"""
        new_x = self.rocket_x - 1
        if 0 <= new_x <= GAME_AREA_SIZE - ROCKET_SIZE:
            self.rocket_x = new_x
    
    def move_right(self):
        """Move rocket right"""
        new_x = self.rocket_x + 1
        if 0 <= new_x <= GAME_AREA_SIZE - ROCKET_SIZE:
            self.rocket_x = new_x
    
    def move_rocket(self, direction):
        """Move rocket left or right (legacy function)"""
        if direction == -1:
            self.move_left()
        elif direction == 1:
            self.move_right()
    
    def create_obstacle(self, obstacle_type, x, y, size):
        """Create an obstacle"""
        return {
            'type': obstacle_type,
            'x': x,
            'y': y,
            'size': size
        }
    
    def spawn_obstacles(self):
        """Spawn new obstacles at the top of the screen"""
        if random.randint(1, self.obstacle_spawn_rate) == 1:
            obstacle_types = [METEOR, ASTEROID, COMET, STAR]
            large_obstacle_types = [BLACK_HOLE, PLANET_ORBIT]
            
            # 80% chance for regular obstacles, 20% for large obstacles
            if random.randint(1, 10) <= 8:
                obstacle_type = random.choice(obstacle_types)
                size = OBSTACLE_SIZE
                x = random.randint(0, GAME_AREA_SIZE - size)
            else:
                obstacle_type = random.choice(large_obstacle_types)
                size = LARGE_OBSTACLE_SIZE
                x = random.randint(0, GAME_AREA_SIZE - size)
            
            self.obstacles.append(self.create_obstacle(obstacle_type, x, 0, size))
    
    def spawn_pluto(self):
        """Spawn Pluto when close to the end"""
        if self.distance_traveled >= self.total_distance - 50 and not any(obs['type'] == PLUTO for obs in self.obstacles):
            x = random.randint(0, GAME_AREA_SIZE - LARGE_OBSTACLE_SIZE)
            self.obstacles.append(self.create_obstacle(PLUTO, x, 0, LARGE_OBSTACLE_SIZE))
    
    def move_obstacles(self):
        """Move obstacles down the screen"""
        for obstacle in self.obstacles[:]:
            obstacle['y'] += 1
            if obstacle['y'] >= GAME_AREA_SIZE:
                self.obstacles.remove(obstacle)
                # Award points for successfully passing an obstacle
                if obstacle['type'] != PLUTO:
                    self.score += 10
    
    def check_collisions(self):
        """Check for collisions between rocket and obstacles"""
        rocket_positions = []
        for rx in range(self.rocket_x, self.rocket_x + ROCKET_SIZE):
            for ry in range(self.rocket_y, self.rocket_y + ROCKET_SIZE):
                rocket_positions.append((rx, ry))
        
        for obstacle in self.obstacles[:]:
            obstacle_positions = []
            for ox in range(obstacle['x'], obstacle['x'] + obstacle['size']):
                for oy in range(obstacle['y'], obstacle['y'] + obstacle['size']):
                    obstacle_positions.append((ox, oy))
            
            # Check for collision
            if any(pos in obstacle_positions for pos in rocket_positions):
                if obstacle['type'] == BLACK_HOLE:
                    self.game_over = True
                    self.message = f"{self.username} entered a black hole!"
                elif obstacle['type'] == PLANET_ORBIT:
                    self.game_over = True
                    self.message = f"{self.username} entered wrong planet!"
                elif obstacle['type'] == PLUTO:
                    self.game_over = True
                    self.game_won = True
                    self.message = f"{self.username} won the game with a score of {self.score}!"
                else:
                    # Hit regular obstacle
                    self.score -= 5
                    self.obstacles.remove(obstacle)
                    if self.score < 0:  # Changed from <= 0 to < 0 since we start at 0
                        self.score = 0
                        self.game_over = True
                        self.message = f"{self.username} lost the game!"
                break
    
    def get_obstacle_color(self, obstacle_type):
        """Get color for different obstacle types"""
        colors = {
            METEOR: RED,
            ASTEROID: GRAY,
            COMET: CYAN,
            STAR: YELLOW,
            BLACK_HOLE: BLACK,
            PLANET_ORBIT: PURPLE,
            PLUTO: PINK
        }
        return colors.get(obstacle_type, WHITE)
    
    def update_game(self):
        """Update game state"""
        self.move_counter += 1
        
        # Move obstacles every few frames based on difficulty
        if self.move_counter % self.move_speed == 0:
            self.move_obstacles()
            self.distance_traveled += 1
            
            # Check if reached Pluto distance
            if self.distance_traveled >= self.total_distance:
                self.spawn_pluto()
        
        # Spawn new obstacles
        self.spawn_obstacles()
        
        # Check collisions
        self.check_collisions()
    
    def draw_game(self):
        """Draw the game area and objects"""
        # Draw game area border
        game_area_pixel_size = GAME_AREA_SIZE * CELL_SIZE
        start_x = (WINDOW_WIDTH - game_area_pixel_size) // 2
        start_y = 50
        
        pygame.draw.rect(self.screen, WHITE, 
                        (start_x - 2, start_y - 2, 
                         game_area_pixel_size + 4, game_area_pixel_size + 4), 2)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obs_screen_x = start_x + obstacle['x'] * CELL_SIZE
            obs_screen_y = start_y + obstacle['y'] * CELL_SIZE
            color = self.get_obstacle_color(obstacle['type'])
            
            if obstacle['type'] == BLACK_HOLE:
                # Draw black hole with white border
                pygame.draw.rect(self.screen, WHITE, 
                               (obs_screen_x - 1, obs_screen_y - 1, 
                                obstacle['size'] * CELL_SIZE + 2, obstacle['size'] * CELL_SIZE + 2))
                pygame.draw.rect(self.screen, color, 
                               (obs_screen_x, obs_screen_y, 
                                obstacle['size'] * CELL_SIZE, obstacle['size'] * CELL_SIZE))
            elif obstacle['type'] == STAR:
                # Draw star shape (simplified as diamond)
                center_x = obs_screen_x + (obstacle['size'] * CELL_SIZE) // 2
                center_y = obs_screen_y + (obstacle['size'] * CELL_SIZE) // 2
                size = obstacle['size'] * CELL_SIZE // 2
                points = [
                    (center_x, center_y - size),
                    (center_x + size, center_y),
                    (center_x, center_y + size),
                    (center_x - size, center_y)
                ]
                pygame.draw.polygon(self.screen, color, points)
            elif obstacle['type'] == COMET:
                # Draw comet with tail
                pygame.draw.rect(self.screen, color, 
                               (obs_screen_x, obs_screen_y, 
                                obstacle['size'] * CELL_SIZE, obstacle['size'] * CELL_SIZE))
                # Draw tail
                pygame.draw.rect(self.screen, WHITE, 
                               (obs_screen_x + obstacle['size'] * CELL_SIZE, obs_screen_y, 
                                CELL_SIZE // 2, obstacle['size'] * CELL_SIZE))
            else:
                # Draw regular rectangle
                pygame.draw.rect(self.screen, color, 
                               (obs_screen_x, obs_screen_y, 
                                obstacle['size'] * CELL_SIZE, obstacle['size'] * CELL_SIZE))
        
        # Draw rocket
        rocket_screen_x = start_x + self.rocket_x * CELL_SIZE
        rocket_screen_y = start_y + self.rocket_y * CELL_SIZE
        pygame.draw.rect(self.screen, BLUE, 
                        (rocket_screen_x, rocket_screen_y, 
                         ROCKET_SIZE * CELL_SIZE, ROCKET_SIZE * CELL_SIZE))
        
        # Draw rocket details (simple triangle on top)
        pygame.draw.polygon(self.screen, WHITE, [
            (rocket_screen_x + CELL_SIZE, rocket_screen_y),
            (rocket_screen_x + CELL_SIZE // 2, rocket_screen_y - CELL_SIZE // 2),
            (rocket_screen_x + CELL_SIZE + CELL_SIZE // 2, rocket_screen_y - CELL_SIZE // 2)
        ])
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        progress = min(100, (self.distance_traveled / self.total_distance) * 100)
        progress_text = self.small_font.render(f"Progress to Pluto: {progress:.1f}%", True, WHITE)
        self.screen.blit(progress_text, (10, 50))
        
        # Debug info
        debug_text = self.small_font.render(f"Rocket Position: ({self.rocket_x}, {self.rocket_y})", True, WHITE)
        self.screen.blit(debug_text, (10, 75))
        
        pilot_text = self.small_font.render(f"Pilot: {self.username}", True, GREEN)
        self.screen.blit(pilot_text, (WINDOW_WIDTH - 200, 10))
        
        difficulty_text = self.small_font.render(f"Difficulty: {self.difficulty.upper()}", True, YELLOW)
        self.screen.blit(difficulty_text, (WINDOW_WIDTH - 200, 35))
        
        controls_text = self.small_font.render("Controls: LEFT/RIGHT arrows or A/D keys", True, WHITE)
        self.screen.blit(controls_text, (WINDOW_WIDTH - 300, 60))
        
        # Draw legend
        legend_y = WINDOW_HEIGHT - 150
        legend_items = [
            ("Meteor", RED),
            ("Asteroid", GRAY),
            ("Comet", CYAN),
            ("Star", YELLOW),
            ("Black Hole", BLACK),
            ("Planet Orbit", PURPLE),
            ("Pluto", PINK)
        ]
        
        legend_title = self.small_font.render("Legend:", True, WHITE)
        self.screen.blit(legend_title, (10, legend_y - 25))
        
        for i, (name, color) in enumerate(legend_items):
            y_pos = legend_y + i * 20
            pygame.draw.rect(self.screen, color, (10, y_pos, 15, 15))
            if color == BLACK:
                pygame.draw.rect(self.screen, WHITE, (10, y_pos, 15, 15), 1)
            text = self.small_font.render(name, True, WHITE)
            self.screen.blit(text, (30, y_pos))
        
        # Draw game over message if applicable
        if self.game_over:
            message_text = self.font.render(self.message, True, RED if not self.game_won else GREEN)
            message_rect = message_text.get_rect(center=(WINDOW_WIDTH//2, start_y + game_area_pixel_size + 50))
            
            # Draw background for message
            pygame.draw.rect(self.screen, BLACK, message_rect.inflate(20, 10))
            pygame.draw.rect(self.screen, WHITE, message_rect.inflate(20, 10), 2)
            self.screen.blit(message_text, message_rect)

if __name__ == "__main__":
    game = SpaceJourneyGame()
    game.run()
