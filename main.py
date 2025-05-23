# Import
import pygame
from game import *



def main() -> None:
    
    # Initialisation de pygame 
    pygame.init()
    
    game: object = Game()
    
    game.run() 
    
    
    


if __name__ == "__main__":
    main()