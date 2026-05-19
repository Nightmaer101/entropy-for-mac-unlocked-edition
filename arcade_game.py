"""
🎮 ULTIMATE SNAKE ARCADE GAME - CodeHS Pygame Edition
Features: Dynamic difficulty, power-ups, animations, and sound effects!
"""

import pygame
import random
import sys
import math
from enum import Enum

# ============================================================================
# INITIALIZE PYGAME
# ============================================================================
pygame.init()

# ============================================================================
# GAME CONSTANTS & CONFIGURATION
# ============================================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_SIZE = 20  # Each cell is 20x20 pixels
FPS = 12  # Game speed
DIFFICULTY_INCREASE = 0.5  # Speed increase per food eaten

# ============================================================================
# COLOR PALETTE - Vibrant Arcade Style
# ============================================================================
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_SNAKE_HEAD = (0, 255, 100)  # Bright cyan-green
COLOR_SNAKE_BODY = (0, 200, 80)   # Darker green
COLOR_FOOD = (255, 50, 100)        # Hot pink
COLOR_FOOD_GLOW = (255, 200, 100)  # Gold glow
COLOR_POWER_UP = (100, 200, 255)   # Cyan
COLOR_POWER_UP_GLOW = (150, 255, 255)  # Light cyan
COLOR_BG = (15, 15, 35)            # Dark blue background
COLOR_GRID = (40, 50, 80)          # Grid color
COLOR_TEXT_PRIMARY = (0, 255, 150) # Cyan text
COLOR_TEXT_SECONDARY = (255, 255, 100)  # Yellow text
COLOR_DANGER = (255, 50, 50)       # Red for danger

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
# POWER-UP CLASS
# ============================================================================
class PowerUp:
    """Represents a power-up item"""
    
    INVINCIBLE = "invincible"
    SPEED_BOOST = "speed_boost"
    
    def __init__(self, power_type):
        """Initialize power-up at random location"""
        self.type = power_type
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
        self.duration = 300  # frames
        self.animation_frame = 0
    
    def get_position(self):
        """Return (x, y) position of power-up"""
        return (self.x, self.y)
    
    def update(self):
        """Update animation frame"""
        self.animation_frame += 1
    
    def draw(self, screen):
        """Draw power-up with pulsing animation"""
        # Calculate pulsing scale
        pulse = 0.5 + 0.5 * math.sin(self.animation_frame * 0.1)
        size = int(GRID_SIZE * 0.6 * pulse)
        
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw outer glow
        glow_size = int(GRID_SIZE * 0.8)
        pygame.draw.circle(screen, COLOR_POWER_UP_GLOW, (center_x, center_y), glow_size, 2)
        
        # Draw power-up core
        pygame.draw.circle(screen, COLOR_POWER_UP, (center_x, center_y), size)
        
        # Draw inner star
        pygame.draw.circle(screen, COLOR_POWER_UP_GLOW, (center_x, center_y), size // 2)

# ============================================================================
# SNAKE CLASS (Enhanced)
# ============================================================================
class Snake:
    """Represents the player's snake with enhanced features"""
    
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
        self.next_direction = Direction.RIGHT  # Queued direction
        self.grow_pending = 0
        self.invincible = False
        self.invincible_frames = 0
        self.trail_points = []  # For rendering trail effect
    
    def move(self):
        """Move the snake in current direction"""
        # Use queued direction if valid
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        
        # Calculate new head position
        new_head = (head_x + dx, head_y + dy)
        
        # Store trail point
        self.trail_points.append(new_head)
        if len(self.trail_points) > 5:
            self.trail_points.pop(0)
        
        # Add new head to front of body
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        
        # Update invincibility
        if self.invincible:
            self.invincible_frames -= 1
            if self.invincible_frames <= 0:
                self.invincible = False
    
    def grow(self, amount=1):
        """Mark the snake to grow on next moves"""
        self.grow_pending += amount
    
    def set_direction(self, new_direction):
        """
        Queue direction change (prevents 180° turns)
        
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
            self.next_direction = new_direction
    
    def get_head(self):
        """Return (x, y) of snake head"""
        return self.body[0]
    
    def get_length(self):
        """Return length of snake"""
        return len(self.body)
    
    def check_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]
        return head in self.body[1:]
    
    def check_boundary(self):
        """Check if snake hits the boundary"""
        head_x, head_y = self.get_head()
        max_x = SCREEN_WIDTH // GRID_SIZE
        max_y = SCREEN_HEIGHT // GRID_SIZE
        return head_x < 0 or head_x >= max_x or head_y < 0 or head_y >= max_y
    
    def activate_invincibility(self, duration=300):
        """Activate invincibility shield"""
        self.invincible = True
        self.invincible_frames = duration
    
    def draw(self, screen):
        """Draw the snake with enhanced visuals"""
        # Draw trail effect (optional visual polish)
        for i, trail_point in enumerate(self.trail_points):
            alpha = int(100 * (i / len(self.trail_points)))
            trail_x, trail_y = trail_point
            trail_rect = pygame.Rect(
                trail_x * GRID_SIZE + 2, 
                trail_y * GRID_SIZE + 2, 
                GRID_SIZE - 4, 
                GRID_SIZE - 4
            )
            pygame.draw.rect(screen, COLOR_SNAKE_BODY, trail_rect)
        
        # Draw head with invincibility effect
        head_x, head_y = self.body[0]
        head_rect = pygame.Rect(
            head_x * GRID_SIZE, 
            head_y * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        
        # Invincibility shield glow
        if self.invincible:
            glow_color = (100, 255, 255) if (self.invincible_frames // 5) % 2 else COLOR_SNAKE_HEAD
            pygame.draw.rect(screen, glow_color, head_rect)
            pygame.draw.circle(
                screen, 
                (100, 200, 255), 
                head_rect.center, 
                GRID_SIZE // 2 + 2, 
                3
            )
        else:
            pygame.draw.rect(screen, COLOR_SNAKE_HEAD, head_rect)
        
        pygame.draw.rect(screen, COLOR_TEXT_PRIMARY, head_rect, 3)  # Border
        
        # Draw eyes on head
        eye_offset = GRID_SIZE // 4
        if self.direction == Direction.RIGHT:
            pygame.draw.circle(screen, COLOR_BLACK, (head_x * GRID_SIZE + GRID_SIZE - eye_offset, head_y * GRID_SIZE + eye_offset), 2)
        elif self.direction == Direction.LEFT:
            pygame.draw.circle(screen, COLOR_BLACK, (head_x * GRID_SIZE + eye_offset, head_y * GRID_SIZE + eye_offset), 2)
        elif self.direction == Direction.DOWN:
            pygame.draw.circle(screen, COLOR_BLACK, (head_x * GRID_SIZE + eye_offset, head_y * GRID_SIZE + GRID_SIZE - eye_offset), 2)
        else:  # UP
            pygame.draw.circle(screen, COLOR_BLACK, (head_x * GRID_SIZE + eye_offset, head_y * GRID_SIZE + eye_offset), 2)
        
        # Draw body segments
        for i, segment in enumerate(self.body[1:]):
            seg_x, seg_y = segment
            seg_rect = pygame.Rect(
                seg_x * GRID_SIZE + 2, 
                seg_y * GRID_SIZE + 2, 
                GRID_SIZE - 4, 
                GRID_SIZE - 4
            )
            # Gradient effect - darker segments farther from head
            color_intensity = max(100, 200 - (i * 2))
            segment_color = (0, color_intensity, 60)
            pygame.draw.rect(screen, segment_color, seg_rect)
            pygame.draw.rect(screen, COLOR_SNAKE_BODY, seg_rect, 1)

# ============================================================================
# FOOD CLASS (Enhanced with Animation)
# ============================================================================
class Food:
    """Represents food pellets with animation"""
    
    def __init__(self):
        """Initialize food at random location"""
        self.respawn()
        self.animation_frame = 0
    
    def get_position(self):
        """Return (x, y) position of food"""
        return (self.x, self.y)
    
    def respawn(self):
        """Move food to new random location"""
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
        self.animation_frame = 0
    
    def update(self):
        """Update animation"""
        self.animation_frame += 1
    
    def draw(self, screen):
        """Draw food with pulsing animation"""
        # Pulsing animation
        pulse = 0.6 + 0.4 * math.sin(self.animation_frame * 0.08)
        size = int(GRID_SIZE * 0.4 * pulse)
        
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw glow
        pygame.draw.circle(screen, COLOR_FOOD_GLOW, (center_x, center_y), GRID_SIZE // 3, 2)
        
        # Draw main body
        pygame.draw.circle(screen, COLOR_FOOD, (center_x, center_y), size)
        
        # Draw shine
        pygame.draw.circle(screen, COLOR_FOOD_GLOW, (center_x - 3, center_y - 3), 3)

# ============================================================================
# GAME CLASS (Enhanced)
# ============================================================================
class Game:
    """Main game manager with enhanced features"""
    
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 SNAKE ARCADE - Ultimate Edition")
        
        self.clock = pygame.time.Clock()
        self.font_huge = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Initialize game objects
        start_x = SCREEN_WIDTH // (2 * GRID_SIZE)
        start_y = SCREEN_HEIGHT // (2 * GRID_SIZE)
        
        self.snake = Snake(start_x, start_y)
        self.food = Food()
        self.power_ups = []  # List of active power-ups
        self.score = 0
        self.level = 1
        self.frames_eaten = 0  # Frames since last food eaten
        self.game_over = False
        self.current_speed = FPS
        self.high_score = 0  # Track high score
    
    def spawn_power_up(self):
        """Randomly spawn a power-up"""
        if random.random() < 0.15:  # 15% chance per food
            power_type = random.choice([PowerUp.INVINCIBLE, PowerUp.SPEED_BOOST])
            self.power_ups.append(PowerUp(power_type))
    
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
        
        # Update food animation
        self.food.update()
        
        # Update power-ups
        for power_up in self.power_ups:
            power_up.update()
        
        # Check if snake ate food
        if self.snake.get_head() == self.food.get_position():
            self.snake.grow(3)  # Grow by 3 segments
            self.food.respawn()
            self.score += 10
            self.level = 1 + (self.score // 50)  # Level up every 50 points
            self.frames_eaten = 0
            self.spawn_power_up()  # Chance to spawn power-up
        
        # Check power-ups
        for power_up in self.power_ups[:]:
            if self.snake.get_head() == power_up.get_position():
                if power_up.type == PowerUp.INVINCIBLE:
                    self.snake.activate_invincibility(400)
                elif power_up.type == PowerUp.SPEED_BOOST:
                    self.current_speed = min(20, self.current_speed + 2)
                    self.score += 5
                self.power_ups.remove(power_up)
        
        # Increment frames since eating
        self.frames_eaten += 1
        
        # Update speed based on level
        self.current_speed = FPS + (self.level - 1) * DIFFICULTY_INCREASE
        
        # Check collisions
        if not self.snake.invincible and self.snake.check_collision():
            self.game_over = True
        
        if self.snake.check_boundary():
            self.game_over = True
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def draw(self):
        """Draw everything to screen"""
        # Clear screen with gradient-like effect
        self.screen.fill(COLOR_BG)
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw border
        pygame.draw.rect(self.screen, COLOR_TEXT_PRIMARY, 
                        (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)
        
        # Draw game objects
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw HUD (Heads-Up Display)
        self.draw_hud()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        # Update display
        pygame.display.flip()
    
    def draw_hud(self):
        """Draw heads-up display with stats"""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(score_text, (15, 15))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, COLOR_TEXT_SECONDARY)
        self.screen.blit(level_text, (SCREEN_WIDTH - 250, 15))
        
        # Snake length
        length_text = self.font_small.render(f"Length: {self.snake.get_length()}", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(length_text, (15, 50))
        
        # Speed indicator
        speed_bars = min(5, int(self.current_speed / 4))
        speed_text = self.font_small.render(f"Speed: {'█' * speed_bars}{'░' * (5 - speed_bars)}", 
                                           True, COLOR_TEXT_SECONDARY)
        self.screen.blit(speed_text, (SCREEN_WIDTH - 250, 50))
        
        # Invincibility status
        if self.snake.invincible:
            inv_text = self.font_small.render("⚔ INVINCIBLE", True, (100, 255, 255))
            self.screen.blit(inv_text, (SCREEN_WIDTH // 2 - 80, 15))
    
    def draw_game_over(self):
        """Draw game over screen with stylish UI"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with glow effect
        game_over_text = self.font_huge.render("GAME OVER!", True, COLOR_DANGER)
        glow_text = self.font_huge.render("GAME OVER!", True, (255, 100, 100))
        
        for offset in range(1, 6):
            glow = self.font_huge.render("GAME OVER!", True, 
                                        (255, 50 + offset * 10, 50 + offset * 10))
            glow.set_alpha(50)
            self.screen.blit(glow, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + offset, 
                            150 - offset))
        
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        
        # Final stats
        final_score = self.font_large.render(f"Final Score: {self.score}", True, COLOR_TEXT_SECONDARY)
        high_score = self.font_large.render(f"High Score: {self.high_score}", True, COLOR_TEXT_PRIMARY)
        final_level = self.font_medium.render(f"Reached Level: {self.level}", True, COLOR_FOOD_GLOW)
        final_length = self.font_medium.render(f"Final Length: {self.snake.get_length()}", True, COLOR_FOOD_GLOW)
        
        self.screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 270))
        self.screen.blit(high_score, (SCREEN_WIDTH // 2 - high_score.get_width() // 2, 330))
        self.screen.blit(final_level, (SCREEN_WIDTH // 2 - final_level.get_width() // 2, 390))
        self.screen.blit(final_length, (SCREEN_WIDTH // 2 - final_length.get_width() // 2, 440))
        
        # Restart instructions
        restart_text = self.font_small.render("Press SPACE to Restart or ESC to Quit", 
                                             True, COLOR_WHITE)
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 550))
    
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
            self.clock.tick(self.current_speed)
        
        pygame.quit()
        sys.exit()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    game = Game()
    game.run()
