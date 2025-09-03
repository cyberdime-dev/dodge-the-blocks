"""
Main entry point for Dodge the Blocks game.
Initializes pygame and starts the game.
"""

import pygame
from game import Game


def main():
    """Initialize pygame and run the game"""
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
