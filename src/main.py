"""
main.py

This is the entry point for Pydood Jump.
It initializes the game and starts the main game loop.

Author:     DevXCVIII
Date:       March 24, 2025
License:    MIT
"""

# Imports
import pygame
import Box2D
import game

# Initialize Pygame
pygame.init()

if __name__ == "__main__":
    # Initialize the game
    game = game.Game()

    # Start the game loop
    game.run()