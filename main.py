"""
Main entry point for Dodge the Blocks game.
Initializes pygame and starts the game.
"""

import pygame
import sys
import traceback
from game import Game


def main():
    """Initialize pygame and run the game"""
    try:
        # Initialize pygame
        pygame.init()
        print("✅ Pygame initialized successfully")
        
        # Create and run the game
        game = Game()
        game.run()
        
    except pygame.error as e:
        print(f"❌ Pygame error: {e}")
        print("Please make sure pygame is properly installed:")
        print("  pip install pygame")
        sys.exit(1)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all required modules are available")
        print("Check that config.py, player.py, enemy.py, and game.py exist")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Error details:")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Ensure pygame is properly quit
        try:
            pygame.quit()
            print("✅ Pygame closed successfully")
        except:
            pass


if __name__ == "__main__":
    main()
