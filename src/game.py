"""
game.py

This module contains the Game class, which manages the main game logic, 
including the game loop, physics, and rendering.

Game Mechanics:
- The player jumps between platforms to score points.
- Platforms are one-way colliders: the player can pass through from below but lands on them from above.
- The game ends when the player falls below the screen.

Author:     DevXCVIII
Date:       March 24, 2025
"""

# Imports
import pygame
import Box2D

import settings
from player import Player
from platforms import generate_platforms
from contact_listener import ContactListener
from utils import blit_text_with_anchor

class Game:
    """
    The Game class manages the main game logic, including:
    - Initialization of the game world, player, and platforms.
    - Handling game states (main menu, gameplay, game over).
    - Managing physics and rendering.
    """

    """------------------------------------- Initialization -------------------------------------"""
    def __init__(self):
        """
        Initializes the game.
        """
        # Initialize the Pygame screen and set the window title
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Pydood Jump")

        # Set the game to "running"
        self.running = True

        # Initialize the Box2D world with gravity
        self.world = Box2D.b2.world(gravity=settings.GRAVITY, doSleep=True)

        # Initialize the game clock for frame rate control
        self.clock = pygame.time.Clock()

        # Set the initial game state to the main menu
        self.state = "main-menu"

        # Load the game font for rendering text
        #self.font = pygame.font.Font("../assets/fonts/FiraCode.ttf", 24)
        self.font = pygame.font.SysFont("Arial", 24)

        # Initialize the player
        self.player = Player(self.world)

        # Load the background image
        self.background = pygame.image.load("../assets/backgrounds/space-bck@2x.png")

        # Initialize the camera offset for scrolling
        self.camera_offset = 0

        # Generate initial platforms
        self.platforms = generate_platforms(self.world, start_y=1)

        # Set up the contact listener for collision handling
        self.contact_listener = ContactListener(self.player)
        self.world.contactListener = self.contact_listener

        # Initialize the score tracker
        self.score = 0

    """-------------------------------------- Game Loop -----------------------------------------"""
    def run(self):
        """
        Starts the game loop and handles game states.
        """
        while self.running:
            # Handle the current game state
            match self.state:
                case "main-menu":
                    self.main_menu()
                case "playing":
                    self.playing()
                case "game-over":
                    self.game_over()
                case "quit":
                    self.running = False
                case _:
                    print("Invalid game state")
                    self.running = False

    """-------------------------------------- Game States ---------------------------------------"""
    def main_menu(self):
        """
        Renders the main menu and handles input.
        """
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.state = "quit"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game
                        self.state = "playing"
                    if event.key == pygame.K_ESCAPE:  # Quit the game
                        self.state = "quit"

        # Render the main menu UI
        self.screen.fill((0, 0, 0))  # Black background

        # Title Text (centered at the top, with an offset)
        title_text = self.font.render("Pydood Jump", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, title_text, anchor=(0.5, 0.25))

        # Start Text (centered in the middle)
        start_text = self.font.render("Press Enter to Start", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, start_text, anchor=(0.5, 0.5))

        # Quit Text (centered at the bottom)
        quit_text = self.font.render("Press Esc to Quit", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, quit_text, anchor=(0.5, 0.75))

        # Update the display
        pygame.display.flip()

    def playing(self):
        """
        Handles the main gameplay loop.
        """
        # Apply an initial upward force to the player when the game starts
        if self.camera_offset == 0:  # Check if the game is just starting
            self.player.body.ApplyLinearImpulse((0, 1), self.player.body.worldCenter, True)

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.state = "quit"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pause the game
                        self.state = "main-menu"

        # Handle player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1)
        else:
            self.player.move(0)

        if keys[pygame.K_SPACE]:
            self.player.jump()

        # Check if the player has fallen below the screen
        if self.player.body.position.y * settings.PIXELS_PER_METER < -settings.PLAYER_SPRITE_HEIGHT:
            self.state = "game-over"

        # Game Update
        self.world.Step(1 / 60, 6, 2)
        self.world.ClearForces()
        self.player.update()

        # Update the camera offset to follow the player
        player_screen_y = settings.SCREEN_HEIGHT - (self.player.body.position.y * 30 - self.camera_offset)
        if player_screen_y < settings.SCREEN_HEIGHT / 2:
            self.camera_offset += settings.SCREEN_HEIGHT / 2 - player_screen_y

        # Remove off-screen platforms
        self.platforms = [p for p in self.platforms if p.body.position.y * 30 - self.camera_offset > -settings.PLATFORM_HEIGHT]

        # Spawn new platforms
        highest_platform_y = max([p.body.position.y for p in self.platforms], default=1)
        if len(self.platforms) < 10 or self.player.body.position.y > highest_platform_y - 3:
            new_platforms = generate_platforms(self.world, start_y=highest_platform_y + 2, num_platforms=5)
            self.platforms.extend(new_platforms)

        # Update score
        self.score = max(self.score, int(self.player.body.position.y))

        # Render the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        print(f"Score: {self.score}")
        blit_text_with_anchor(self.screen, score_text, anchor=(0.05, 0.05))  # 5% from left and top

        # Game Rendering
        self.screen.blit(self.background, (0, 0))
        self.player.render(self.screen, self.camera_offset)

        # Render platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_offset)
            platform.update_sensor(self.player)
        pygame.display.flip()

        self.clock.tick(60)  # Limit the frame rate to 60 FPS

    def game_over(self):
        """
        Handles the game-over screen.
        """
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.state = "quit"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Restart the game
                        self.__init__()  # Reinitialize the game
                        self.state = "playing"
                    elif event.key == pygame.K_ESCAPE:  # Quit the game
                        self.state = "quit"

        # Render the game-over screen
        self.screen.fill((0, 0, 0))  # Black background

        # Game Over Text
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        blit_text_with_anchor(self.screen, game_over_text, anchor=(0.5, 0.4))

        # Final Score Text
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, score_text, anchor=(0.5, 0.5))

        # Restart Text
        restart_text = self.font.render("Press Enter to Restart", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, restart_text, anchor=(0.5, 0.6))

        # Quit Text
        quit_text = self.font.render("Press Esc to Quit", True, (255, 255, 255))
        blit_text_with_anchor(self.screen, quit_text, anchor=(0.5, 0.7))

        # Update the display
        pygame.display.flip()

    def quit(self):
        """
        Quits the game.
        """
        pygame.quit() 