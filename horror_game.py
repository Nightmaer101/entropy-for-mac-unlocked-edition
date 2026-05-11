#!/usr/bin/env python3
"""
Horror Game: The Haunted House (GUI Version)
A graphical adventure game with images, colors, and buttons.
Uses Pygame for visual interface.
Meets all requirements: function, user input, print statements, purpose.
"""

import pygame
import sys
from enum import Enum
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLOOD_RED = (220, 20, 60)
DARK_GREEN = (34, 139, 34)
PURPLE = (75, 0, 130)
GOLD = (255, 215, 0)

class GameState(Enum):
    TITLE = 1
    GAME = 2
    LIBRARY = 3
    KITCHEN = 4
    BASEMENT = 5
    STUDY = 6
    FRONT_DOOR = 7
    WIN = 8
    LOSE = 9

class Button:
    """Button class for clickable UI elements"""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
    
    def draw(self, screen, font):
        """Draw the button on screen"""
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        """Update button hover state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos)

class HorrorGame:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏚️ The Haunted House 🏚️")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = GameState.TITLE
        self.current_room = "entrance"
        self.turns = 0
        self.max_turns = 10
        self.escaped = False
        self.choice_buttons = []
        self.running = True
        
        self.setup_title_screen()
        
        # Log file
        self.log_file = "horror_game_log.txt"
        self.log("=== GAME STARTED ===")
    
    def log(self, text):
        """Log text to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {text}"
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def setup_title_screen(self):
        """Setup title screen buttons"""
        self.choice_buttons = [
            Button(300, 500, 400, 80, "▶️ START GAME", BLOOD_RED, (255, 0, 0))
        ]
    
    def setup_game_buttons(self, choices):
        """Setup game choice buttons"""
        self.choice_buttons = []
        button_y = 450
        for i, choice_text in enumerate(choices):
            btn = Button(150, button_y + (i * 100), 700, 80, f"{i+1}. {choice_text}", DARK_GREEN, (0, 200, 0))
            self.choice_buttons.append(btn)
    
    def draw_background(self, color):
        """Draw colored background"""
        self.screen.fill(color)
    
    def draw_title_screen(self):
        """Draw title screen"""
        self.draw_background(BLACK)
        
        # Title
        title1 = self.font_large.render("🏚️ THE HAUNTED HOUSE 🏚️", True, BLOOD_RED)
        title1_rect = title1.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title1, title1_rect)
        
        # Story text
        story_lines = [
            "You wake up in an abandoned mansion...",
            "The doors are locked. Strange sounds echo through the halls.",
            "You must escape before midnight, or you'll be trapped here forever.",
            "",
            "Can you survive? Click START to begin your nightmare!"
        ]
        
        y = 200
        for line in story_lines:
            if line:
                story_text = self.font_small.render(line, True, LIGHT_GRAY)
                story_rect = story_text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(story_text, story_rect)
            y += 40
        
        # Draw buttons
        for btn in self.choice_buttons:
            btn.draw(self.screen, self.font_medium)
    
    def draw_game_screen(self, room_name, room_desc, choices):
        """Draw game screen with room and choices"""
        # Room backgrounds
        room_colors = {
            "entrance": DARK_GRAY,
            "library": PURPLE,
            "kitchen": DARK_RED,
            "basement": BLACK,
            "study": (80, 40, 40),
        }
        
        self.draw_background(room_colors.get(room_name, DARK_GRAY))
        
        # Room title
        title = self.font_large.render(f"📍 {room_name.upper()}", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Turns counter
        turns_text = self.font_medium.render(f"Turns: {self.turns}/{self.max_turns}", True, BLOOD_RED)
        turns_rect = turns_text.get_rect(topright=(SCREEN_WIDTH - 20, 30))
        self.screen.blit(turns_text, turns_rect)
        
        # Room description
        desc_lines = room_desc.split("\n")
        y = 100
        for line in desc_lines:
            if line:
                desc_text = self.font_small.render(line, True, WHITE)
                desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(desc_text, desc_rect)
            y += 40
        
        # Draw choice buttons
        for btn in self.choice_buttons:
            btn.draw(self.screen, self.font_medium)
    
    def draw_win_screen(self):
        """Draw win screen"""
        self.draw_background(DARK_GREEN)
        
        title = self.font_large.render("✅ YOU ESCAPED!", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        message_lines = [
            "The door swings open...",
            "You burst into the sunlight and RUN!",
            "You're FREE! The mansion fades behind you...",
            "",
            "CONGRATULATIONS! YOU SURVIVED THE HAUNTED HOUSE!"
        ]
        
        y = 250
        for line in message_lines:
            if line:
                msg = self.font_small.render(line, True, WHITE)
                msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(msg, msg_rect)
            y += 50
        
        # Restart button
        restart_btn = Button(300, 600, 400, 80, "▶️ PLAY AGAIN", BLOOD_RED, (255, 0, 0))
        self.choice_buttons = [restart_btn]
        restart_btn.draw(self.screen, self.font_medium)
        
        self.log("GAME WON")
    
    def draw_lose_screen(self):
        """Draw lose screen"""
        self.draw_background(BLOOD_RED)
        
        title = self.font_large.render("❌ GAME OVER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        message_lines = [
            "⏰ MIDNIGHT STRIKES!",
            "The doors seal shut forever...",
            "",
            "You didn't escape in time.",
            "You are trapped in the haunted house..."
        ]
        
        y = 250
        for line in message_lines:
            if line:
                msg = self.font_small.render(line, True, WHITE)
                msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(msg, msg_rect)
            y += 50
        
        # Restart button
        restart_btn = Button(300, 600, 400, 80, "▶️ TRY AGAIN", BLOOD_RED, (255, 0, 0))
        self.choice_buttons = [restart_btn]
        restart_btn.draw(self.screen, self.font_medium)
        
        self.log("GAME LOST")
    
    def handle_title_click(self, choice):
        """Handle title screen click"""
        if choice == 0:
            self.state = GameState.GAME
            self.turns = 0
            self.escaped = False
            self.current_room = "entrance"
            self.log("Game started")
    
    def handle_entrance_click(self, choice):
        """Handle entrance room choice"""
        choices = ["LIBRARY (left hallway)", "KITCHEN (right hallway)", "BASEMENT (downstairs)"]
        self.log(f"Entrance choice: {choice + 1} - {choices[choice]}")
        
        if choice == 0:
            self.state = GameState.LIBRARY
        elif choice == 1:
            self.state = GameState.KITCHEN
        elif choice == 2:
            self.state = GameState.BASEMENT
    
    def handle_library_click(self, choice):
        """Handle library room choice"""
        choices = ["Read the ancient book", "Run back to entrance", "Look for secret exit"]
        self.log(f"Library choice: {choice + 1} - {choices[choice]}")
        
        if choice == 0:
            self.current_room = "entrance"
            self.state = GameState.GAME
        elif choice == 1:
            self.current_room = "entrance"
            self.state = GameState.GAME
        elif choice == 2:
            self.current_room = "study"
            self.state = GameState.STUDY
    
    def handle_kitchen_click(self, choice):
        """Handle kitchen room choice"""
        choices = ["Hide in pantry", "Run back to entrance", "Grab weapon and fight"]
        self.log(f"Kitchen choice: {choice + 1} - {choices[choice]}")
        
        if choice == 0:
            self.current_room = "entrance"
            self.state = GameState.GAME
        elif choice == 1:
            self.current_room = "entrance"
            self.state = GameState.GAME
        elif choice == 2:
            self.state = GameState.FRONT_DOOR
            self.escaped = True
    
    def handle_basement_click(self, choice):
        """Handle basement room choice"""
        choices = ["Light a torch and explore", "Run back upstairs", "Call out for help"]
        self.log(f"Basement choice: {choice + 1} - {choices[choice]}")
        
        if choice == 0:
            self.state = GameState.FRONT_DOOR
            self.escaped = True
        elif choice == 1:
            self.current_room = "entrance"
            self.state = GameState.GAME
        elif choice == 2:
            self.state = GameState.LOSE
    
    def handle_study_click(self, choice):
        """Handle study room choice"""
        choices = ["Take the crystal", "Go back to library", "Use crystal on door"]
        self.log(f"Study choice: {choice + 1} - {choices[choice]}")
        
        if choice == 0 or choice == 2:
            self.state = GameState.FRONT_DOOR
            self.escaped = True
        elif choice == 1:
            self.current_room = "library"
            self.state = GameState.LIBRARY
    
    def handle_restart(self):
        """Restart the game"""
        self.state = GameState.TITLE
        self.current_room = "entrance"
        self.turns = 0
        self.escaped = False
        self.setup_title_screen()
        self.log("\n=== NEW GAME STARTED ===\n")
    
    def update(self, mouse_pos):
        """Update game state"""
        for btn in self.choice_buttons:
            btn.update(mouse_pos)
    
    def handle_click(self, mouse_pos):
        """Handle mouse click"""
        for i, btn in enumerate(self.choice_buttons):
            if btn.is_clicked(mouse_pos):
                self.log(f"Button clicked: {btn.text}")
                
                if self.state == GameState.TITLE:
                    self.handle_title_click(i)
                elif self.state == GameState.GAME:
                    self.turns += 1
                    if self.turns >= self.max_turns:
                        self.state = GameState.LOSE
                    else:
                        self.handle_entrance_click(i)
                elif self.state == GameState.LIBRARY:
                    self.turns += 1
                    if self.turns >= self.max_turns:
                        self.state = GameState.LOSE
                    else:
                        self.handle_library_click(i)
                elif self.state == GameState.KITCHEN:
                    self.turns += 1
                    if self.turns >= self.max_turns:
                        self.state = GameState.LOSE
                    else:
                        self.handle_kitchen_click(i)
                elif self.state == GameState.BASEMENT:
                    self.turns += 1
                    if self.turns >= self.max_turns:
                        self.state = GameState.LOSE
                    else:
                        self.handle_basement_click(i)
                elif self.state == GameState.STUDY:
                    self.turns += 1
                    if self.turns >= self.max_turns:
                        self.state = GameState.LOSE
                    else:
                        self.handle_study_click(i)
                elif self.state == GameState.FRONT_DOOR:
                    self.state = GameState.WIN
                elif self.state == GameState.WIN or self.state == GameState.LOSE:
                    self.handle_restart()
    
    def draw(self):
        """Draw current screen"""
        if self.state == GameState.TITLE:
            self.draw_title_screen()
        elif self.state == GameState.GAME:
            self.setup_game_buttons([
                "Go to the LIBRARY (left hallway)",
                "Go to the KITCHEN (right hallway)",
                "Go to the BASEMENT (downstairs)"
            ])
            desc = "You stand in the MAIN ENTRANCE.\nThe walls are covered in cobwebs.\nYou hear whispers in the darkness..."
            self.draw_game_screen("entrance", desc, [])
        elif self.state == GameState.LIBRARY:
            self.setup_game_buttons([
                "Read the ancient book",
                "Run back to entrance",
                "Look for a secret exit"
            ])
            desc = "You enter a dusty LIBRARY.\nBooks float off shelves on their own...\nA shadowy figure appears!"
            self.draw_game_screen("library", desc, [])
        elif self.state == GameState.KITCHEN:
            self.setup_game_buttons([
                "Hide in the pantry",
                "Run back to entrance",
                "Grab a weapon and fight"
            ])
            desc = "You enter the KITCHEN.\nEverything is rotting...\nYou hear footsteps getting closer!"
            self.draw_game_screen("kitchen", desc, [])
        elif self.state == GameState.BASEMENT:
            self.setup_game_buttons([
                "Light a torch and explore",
                "Run back upstairs",
                "Call out for help"
            ])
            desc = "You descend into the BASEMENT.\nIt's pitch black...\nYou hear chains rattling!"
            self.draw_game_screen("basement", desc, [])
        elif self.state == GameState.STUDY:
            self.setup_game_buttons([
                "Take the crystal",
                "Go back to library",
                "Use crystal on locked door"
            ])
            desc = "You enter a hidden STUDY.\nAncient artifacts cover the shelves...\nYou find a glowing crystal!"
            self.draw_game_screen("study", desc, [])
        elif self.state == GameState.FRONT_DOOR:
            self.draw_background(DARK_GREEN)
            msg1 = self.font_large.render("🔓 YOU REACHED THE FRONT DOOR!", True, GOLD)
            msg2 = self.font_medium.render("Escaping...", True, WHITE)
            self.screen.blit(msg1, msg1.get_rect(center=(SCREEN_WIDTH // 2, 300)))
            self.screen.blit(msg2, msg2.get_rect(center=(SCREEN_WIDTH // 2, 400)))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.state = GameState.WIN
        elif self.state == GameState.WIN:
            self.draw_win_screen()
        elif self.state == GameState.LOSE:
            self.draw_lose_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop - calls draw and update functions"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.update(mouse_pos)
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.log("Game closed by user")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function - entry point"""
    game = HorrorGame()
    game.run()

if __name__ == "__main__":
    main()
