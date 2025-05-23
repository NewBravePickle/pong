import pygame, random

class Ball:
    def __init__(self):
        self.ball_image = pygame.image.load('./assets/arts/Ball.png')
        self.posy = 300
        self.posx = 800 - 400 - self.ball_image.get_width() / 2
        self.vx = 3
        self.vy = 2
        self.speed_multiplier = 1.05  
        self.max_speed = 10 

        
        
    def update(self):
        self.x += self.vx
        self.y += self.vy

    def increase_speed(self):
        self.vx *= self.speed_multiplier
        self.vy *= self.speed_multiplier

        if abs(self.vx) > self.max_speed:
            self.vx = self.max_speed if self.vx > 0 else -self.max_speed
        if abs(self.vy) > self.max_speed:
            self.vy = self.max_speed if self.vy > 0 else -self.max_speed
            
    def random_speed(self):
        self.reset_speed()
        self.vx *= self.speed_multiplier * 3
        self.vy *= self.speed_multiplier * 3
            
    def reset_speed(self):
        self.vx = 3 if random.choice([True, False]) else -3
        self.vy = 2