"""
platforms.py

This module contains the Platform class and the generate_platforms function.

Platform:
- Represents a single platform in the game.
- Handles rendering and one-way collision behavior.

generate_platforms:
- Dynamically generates a list of platforms at random positions.

Author:     DevXCVIII
Date:       March 24, 2025
"""

import pygame
from Box2D.b2 import staticBody, polygonShape
import random
import settings

class Platform:
    """
    Represents a single platform in the game.

    Attributes:
        body: The Box2D body representing the platform.
        fixture: The Box2D fixture for the platform's collision shape.

    Methods:
        draw(screen, camera_offset):
            Renders the platform on the screen.
        update_sensor(player):
            Updates the platform's sensor property to allow one-way collisions.
    """
    def __init__(self, body):
        self.body = body
        self.body.userData = "platform"
        self.fixture = self.body.CreateFixture(
            shape=polygonShape(box=(settings.PLATFORM_WIDTH / 2 / settings.PIXELS_PER_METER, 
                                             settings.PLATFORM_HEIGHT / 2 / settings.PIXELS_PER_METER)),
            density=0,
            friction=0.5
        )
        self.fixture.sensor = False

    def draw(self, screen, camera_offset):
        """
        Draws the platform sprite on the screen.

        Args:
            screen: The Pygame screen to draw on.
            camera_offset: The vertical offset of the camera.
        """
        x_pos = self.body.position.x * settings.PIXELS_PER_METER
        y_pos = settings.SCREEN_HEIGHT - (self.body.position.y * settings.PIXELS_PER_METER - camera_offset)

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            pygame.Rect(
                int(x_pos - settings.PLATFORM_WIDTH / 2),
                int(y_pos - settings.PLATFORM_HEIGHT / 2),
                int(settings.PLATFORM_WIDTH),
                int(settings.PLATFORM_HEIGHT)
            ),
            0  # Fill the rectangle
        )

    def update_sensor(self, player):
        """
        Updates the platform's sensor property based on the player's position.

        If the player is above the platform, the platform is solid.
        If the player is below the platform, the platform becomes a sensor,
        allowing the player to pass through from below.
        """
        if player.body.position.y > self.body.position.y:
            self.fixture.sensor = False  # Solid when the player is above
        else:
            self.fixture.sensor = True  # Pass-through when the player is below


def generate_platforms(world, start_y=1, num_platforms=10):
    """
    Generates a list of platforms at random positions.

    Args:
        world: The Box2D world where the platforms will be created.
        start_y: The starting vertical position for the first platform.
        num_platforms: The number of platforms to generate.

    Returns:
        A list of Platform objects.
    """
    platforms = []
    y = start_y
    for _ in range(num_platforms):
        x = random.randint(50, settings.SCREEN_WIDTH - 50) / settings.PIXELS_PER_METER
        y += random.randint(80, 150) / settings.PIXELS_PER_METER
        platform = Platform(world.CreateStaticBody(position=(x, y)))
        platforms.append(platform)
    return platforms