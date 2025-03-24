"""
player.py

This module contains the Player class, which represents the character in the game.

The Player class handles:
- Movement (left and right).
- Jumping with a cooldown.
- Rendering the player sprite on the screen.
- Interacting with the physics world (e.g., platforms).

Author:     DevXCVIII
Date:       March 24, 2025
"""

# Imports
import pygame
import Box2D
import settings
from Box2D.b2 import polygonShape

class Player:
    """
    Represents the player character in the game.

    Attributes:
        world: The Box2D world the player belongs to.
        body: The Box2D dynamic body representing the player.
        grounded: A boolean indicating whether the player is on the ground.
        jump_cooldown: An integer cooldown timer to prevent continuous jumping.
        sprite: The Pygame surface representing the player's sprite.

    Methods:
        update():
            Updates the player's state (e.g., cooldown timer).
        render(screen, camera_offset):
            Renders the player sprite on the screen.
        jump():
            Makes the player jump if grounded and cooldown is over.
        move(direction):
            Moves the player left or right based on the given direction.
    """
    def __init__(self, world):
        """
        Initializes the player.

        Args:
            world: The Box2D world where the player will be created.
        """
        self.world = world

        # Physics setup
        starting_pos = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4)
        self.body = world.CreateDynamicBody(
            position=(starting_pos[0] / settings.PIXELS_PER_METER, starting_pos[1] / settings.PIXELS_PER_METER)
        )
        self.grounded = False
        self.jump_cooldown = 0

        # Create a rectangular hitbox for the player
        hitbox = polygonShape(box=(settings.PLAYER_HITBOX_WIDTH / 2, settings.PLAYER_HITBOX_HEIGHT / 2))
        self.body.CreateFixture(shape=hitbox, density=1, friction=0.3)

        # Sprite setup
        self.sprite = pygame.image.load("assets/space-left@2x.png").convert_alpha()
        self.sprite = pygame.transform.scale(
            self.sprite, (settings.PLAYER_SPRITE_WIDTH, settings.PLAYER_SPRITE_HEIGHT)
        )

    def update(self):
        """
        Updates the player's state (e.g., position, velocity, etc.).
        """
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def render(self, screen, camera_offset):
        """
        Renders the player sprite on the screen.

        Converts the player's position from Box2D world coordinates to Pygame screen
        coordinates. The sprite is centered on the player's physics body.

        Args:
            screen: The Pygame screen to draw on.
            camera_offset: The vertical offset of the camera.
        """
        # Get the player's position from the Box2D world
        x, y = self.body.position

        # Convert the Box2D position to Pygame coordinates
        screen_x = x * settings.PIXELS_PER_METER
        screen_y = settings.SCREEN_HEIGHT - (y * settings.PIXELS_PER_METER - camera_offset)

        # Adjust for sprite size (center the sprite on the physics body)
        screen_x -= settings.PLAYER_SPRITE_WIDTH / 2
        screen_y -= settings.PLAYER_SPRITE_HEIGHT / 2

        # Draw the sprite to the screen
        screen.blit(self.sprite, (screen_x, screen_y))

    def jump(self):
        """
        Makes the player jump if grounded and the cooldown is over.
        """
        if self.grounded and self.jump_cooldown == 0:
            self.body.ApplyLinearImpulse((0, settings.JUMP_STRENGTH), self.body.worldCenter, True)
            self.jump_cooldown = settings.JUMP_COOLDOWN

    def move(self, direction):
        """
        Moves the player left or right.

        Args:
            direction: -1 for left, 1 for right, 0 for no movement.
        """
        max_speed = settings.PLAYER_MAX_SPEED
        self.body.linearVelocity = (direction * max_speed, self.body.linearVelocity.y)


