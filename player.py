
import pygame, random


class Player:
    def __init__(self):
        
        
        self.player1_image = pygame.image.load('./assets/arts/player1.png')
        self.player2_image = pygame.image.load('./assets/arts/player2.png')
        
        self.speed = 5 
        self.speed_multiplier = 1.02
        self.max_speed = 10
        
        self.P1_y: int = 300
        self.P2_y: int = 300
        
        self.P1_s = 0
        self.P2_s = 0
    
    def increase_speed(self):
        self.speed *= self.speed_multiplier
        self.speed = min(self.speed, self.max_speed)  # clamp
        
    def reset_speed(self):
        self.speed = 5  # vitesse fixe et positive
        
    def random_speed(self):
        self.reset_speed()
        self.speed *= self.speed_multiplier * 3
            