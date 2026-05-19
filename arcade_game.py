"""
Classic Snake Arcade Game - CodeHS Pygame Edition
A fun retro game with scoring system and visual effects.
"""

import pygame
import random
import sys
from enum import Enum

# ============================================================================
# INITIALIZE PYGAME
# ============================================================================
pygame.init()

# ============================================================================
# GAME CONSTANTS & CONFIGURATION
# ============================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # Each cell is 20x20 pixels
FPS = 10  # Game speed (lower = slower, higher = faster)

# Colors (RGB tuples)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_DARK_GRAY = (40, 40, 40)
COLOR_LIGHT_GRAY = (100, 100, 100)

# ============================================================================
# DIRECTION ENUM
# ============================================================================
class Direction(Enum):
    """Enum for snake movement directions"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# ============================================================================
# SNAKE CLASS
# ============================================================================
class Snake:
    """Represents the player's snake"""
    
    def __init__(self, start_x, start_y):
        """
        Initialize snake with starting position
        
        Args:
            start_x: Starting X coordinate (in grid units)
            start_y: Starting Y coordinate (in grid units)
        """
        # Snake body is a list of (x, y) coordinates
        # Head is at index 0
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = Direction.RIGHT
        self.grow_pending = False
    
    def move(self):
        """Move the snake in current direction"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        
        # Calculate new head position
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head to front of body
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
    
    def grow(self):
        """Mark the snake to grow on next move"""
        self.grow_pending = True
    
    def set_direction(self, new_direction):
        """
        Set snake direction (prevents 180° turns)
        
        Args:
            new_direction: New Direction enum value
        """
        # Prevent snake from turning into itself
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction
    
    def get_head(self):
        """Return (x, y) of snake head"""
        return self.body[0]
    
    def check_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]
        return head in self.body[1:]
    
    def check_boundary(self):
        """Check if snake hits the boundary"""
        head_x, head_y = self.get_head()
        
        # Grid-based boundaries
        max_x = SCREEN_WIDTH // GRID_SIZE
        max_y = SCREEN_HEIGHT // GRID_SIZE
        
        return head_x < 0 or head_x >= max_x or head_y < 0 or head_y >= max_y
    
    def draw(self, screen):
        """
        Draw the snake on screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw head in brighter green
        head_x, head_y = self.body[0]
        head_rect = pygame.Rect(
            head_x * GRID_SIZE, 
            head_y * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        pygame.draw.rect(screen, COLOR_GREEN, head_rect)
        pygame.draw.rect(screen, COLOR_WHITE, head_rect, 2)  # White border
        
        # Draw body in darker green
        for segment in self.body[1:]:
            seg_x, seg_y = segment
            seg_rect = pygame.Rect(
                seg_x * GRID_SIZE, 
                seg_y * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(screen, COLOR_LIGHT_GRAY, seg_rect)
            pygame.draw.rect(screen, COLOR_WHITE, seg_rect, 1)

# ============================================================================
# FOOD CLASS
# ============================================================================
class Food:
    """Represents food pellets the snake eats"""
    
    def __init__(self):
        """Initialize food at random location"""
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
    
    def get_position(self):
        """Return (x, y) position of food"""
        return (self.x, self.y)
    
    def respawn(self):
        """Move food to new random location"""
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
    
    def draw(self, screen):
        """
        Draw food on screen
        
        Args:
            screen: Pygame surface to draw on
        """
        food_rect = pygame.Rect(
            self.x * GRID_SIZE, 
            self.y * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        pygame.draw.rect(screen, COLOR_RED, food_rect)
        pygame.draw.circle(
            screen, 
            COLOR_YELLOW, 
            (self.x * GRID_SIZE + GRID_SIZE // 2, 
             self.y * GRID_SIZE + GRID_SIZE // 2), 
            GRID_SIZE // 3
        )

# ============================================================================
# GAME CLASS
# ============================================================================
class Game:
    """Main game manager"""
    
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐍 SNAKE ARCADE GAME 🐍")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Initialize game objects
        self.snake = Snake(
            SCREEN_WIDTH // (2 * GRID_SIZE), 
            SCREEN_HEIGHT // (2 * GRID_SIZE)
        )
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Arrow keys or WASD for movement
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.snake.set_direction(Direction.UP)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.snake.set_direction(Direction.DOWN)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.snake.set_direction(Direction.LEFT)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.snake.set_direction(Direction.RIGHT)
                elif event.key == pygame.K_SPACE and self.game_over:
                    # Restart game on SPACE
                    self.__init__()
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Move snake
        self.snake.move()
        
        # Check if snake ate food
        if self.snake.get_head() == self.food.get_position():
            self.snake.grow()
            self.food.respawn()
            self.score += 10
        
        # Check collisions
        if self.snake.check_collision() or self.snake.check_boundary():
            self.game_over = True
    
    def draw(self):
        """Draw everything to screen"""
        # Clear screen
        self.screen.fill(COLOR_DARK_GRAY)
        
        # Draw grid lines (optional - for visual appeal)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_BLACK, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_BLACK, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw game objects
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font_small.render(f"Score: {self.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(COLOR_BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.font_large.render("GAME OVER!", True, COLOR_RED)
            final_score_text = self.font_small.render(
                f"Final Score: {self.score}", True, COLOR_YELLOW
            )
            restart_text = self.font_small.render(
                "Press SPACE to Restart or ESC to Quit", True, COLOR_WHITE
            )
            
            self.screen.blit(
                game_over_text, 
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200)
            )
            self.screen.blit(
                final_score_text, 
                (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 280)
            )
            self.screen.blit(
                restart_text, 
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 380)
            )
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle input
            running = self.handle_input()
            
            # Update game state
            self.update()
            
            # Draw
            self.draw()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    game = Game()
    game.run()
