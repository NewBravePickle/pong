import pygame
from player import *
from ball import *
import random

class Game:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        
        self.violet = (124, 81, 201)
        self.black = (0, 0, 0)
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Pong")
        

        original_bg = pygame.image.load('./assets/arts/Board.png')
        self.bg_image = pygame.transform.scale(original_bg, (self.WIDTH, self.HEIGHT))
        self.score_bar = pygame.image.load('./assets/arts/ScoreBar.png')
        self.score_bar_flipped = pygame.transform.flip(self.score_bar, True, False)
        
        
        self.font = pygame.font.Font('./assets/fonts/Teko-VariableFont_wght.ttf', 32)
        
        self.sound2 = pygame.mixer.Sound("./assets/sounds/2.mp3")
        self.sound3 = pygame.mixer.Sound("./assets/sounds/3.mp3")
        
        self.player = Player()
        self.ball = Ball()
        
        self.time_set = 120
        self.time = self.time_set
        self.last_time_update = pygame.time.get_ticks()
        
        self.start = False
        self.paused = False
        
    def scale_image_to_fit(self, image, target_width, target_height):
        img_width, img_height = image.get_size()
        scale_ratio = min(target_width / img_width, target_height / img_height)
        new_width = int(img_width * scale_ratio)
        new_height = int(img_height * scale_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
    
    def reset_game(self):
        self.player.P1_s = 0
        self.player.P2_s = 0
        self.player.P1_y = self.HEIGHT // 2 - self.player.player1_image.get_height() // 2
        self.player.P2_y = self.HEIGHT // 2 - self.player.player2_image.get_height() // 2
        self.ball.posx = (self.WIDTH // 2) - (self.ball.ball_image.get_width() // 2)
        self.ball.posy = self.HEIGHT // 2
        self.ball.reset_speed()
        self.player.reset_speed()
        self.time = self.time_set
        self.start = False
        self.paused = False
        
    def run(self):
        running: bool = True
        
        while running:
            
            minutes = self.time // 60
            seconds = self.time % 60
            time_str = f"{minutes:02} : {seconds:02}"
            text = self.font.render(time_str, True, self.violet)
            text_score_p1 = self.font.render(str(self.player.P1_s), True, self.black)
            text_score_p2 = self.font.render(str(self.player.P2_s), True, self.black)

            textRect = text.get_rect()
            textRect_P1 = text_score_p1.get_rect()
            textRect_P2 = text_score_p2.get_rect()


            textRect.center = (self.WIDTH-400, 0 + 25)
            textRect_P1.center = (self.WIDTH-500, 0+25)
            textRect_P2.center = (self.WIDTH-300, 0+25)
            self.screen.blit(self.bg_image, (0, 0))
            self.screen.blit(self.player.player1_image, (0, self.player.P1_y))
            self.screen.blit(self.player.player2_image,
                            (800 - self.player.player2_image.get_width(), self.player.P2_y))
            self.screen.blit(self.ball.ball_image, (self.ball.posx, self.ball.posy))
            self.screen.blit(self.score_bar, (0, 0))
            self.screen.blit(self.score_bar_flipped, (800-self.score_bar_flipped.get_width(), 0))
            self.screen.blit(text, textRect)
            self.screen.blit(text_score_p1, textRect_P1)
            self.screen.blit(text_score_p2, textRect_P2)
            

            if self.start and not self.paused:
                # Mettre à jour la position de la balle
                self.ball.posx += self.ball.vx
                self.ball.posy += self.ball.vy

                # Rectangles pour collision
                ball_rect = pygame.Rect(self.ball.posx, self.ball.posy,
                                        self.ball.ball_image.get_width(), self.ball.ball_image.get_height())
                p1_rect = pygame.Rect(0, self.player.P1_y,
                                    self.player.player1_image.get_width(), self.player.player1_image.get_height())
                p2_rect = pygame.Rect(self.WIDTH - self.player.player2_image.get_width(), self.player.P2_y,
                                    self.player.player2_image.get_width(), self.player.player2_image.get_height())

                score_bar_height = self.score_bar.get_height()
                
                current_time = pygame.time.get_ticks()
                if self.time > 0 and current_time - self.last_time_update >= 1000:
                    self.time -= 1
                    self.last_time_update = current_time
                    
                if self.ball.posy <= score_bar_height:
                    self.ball.vy = -self.ball.vy
                
                if self.ball.posy + self.ball.ball_image.get_height() >= self.HEIGHT:
                    self.ball.vy = -self.ball.vy

                if ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect):
                    self.ball.vx = -self.ball.vx
                    
                    s = random.randint(1, 2)
                    if s == 1:
                        self.sound2.play()
                    else:
                        self.sound3.play()

                    self.ball.increase_speed()
                    self.player.increase_speed()
                    
                    ch = random.randint(0, 20)
                    if  ch == 7:
                        self.player.random_speed()
                        self.ball.random_speed()
                        

                if self.ball.posx + self.ball.ball_image.get_width() >= self.WIDTH:
                    self.ball.posx = (self.WIDTH // 2) - (self.ball.ball_image.get_width() // 2)
                    self.ball.posy = self.HEIGHT // 2
                    self.player.P1_s += 1
                    self.ball.reset_speed()
                    self.player.reset_speed()

                    self.start = False

                if self.ball.posx <= 0:
                    self.ball.posx = (self.WIDTH // 2) - (self.ball.ball_image.get_width() // 2)
                    self.ball.posy = self.HEIGHT // 2
                    self.player.P2_s += 1
                    self.start = False
                    self.ball.reset_speed()
                    self.player.reset_speed()

                    
                if self.time <= 0 and self.player.P1_s != self.player.P2_s:
                    self.start = False
                    self.time = 0
  
                    
            if self.time <= 0 and self.player.P1_s != self.player.P2_s:
                winner_text = "P1 gagne !" if self.player.P1_s > self.player.P2_s else "P2 gagne !" if self.player.P2_s > self.player.P1_s else "Égalité"
                winner_surface = self.font.render(winner_text, True, self.violet)
                winner_rect = winner_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(winner_surface, winner_rect)
                info_surface = self.font.render("Appuyez sur R pour rejouer", True, self.violet)
                info_rect = info_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 40))
                self.screen.blit(info_surface, info_rect)

                                
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.time > 0:
                        self.start = True
                    if event.key == pygame.K_r and self.time == 0:
                        self.reset_game()
        
            keys = pygame.key.get_pressed()

            score_bar_height = self.score_bar.get_height()
            player_height = self.player.player1_image.get_height() 

            # Joueur 1
            if keys[pygame.K_z] and self.player.P1_y > score_bar_height:
                self.player.P1_y -= self.player.speed
            if keys[pygame.K_s] and self.player.P1_y + player_height < self.HEIGHT:
                self.player.P1_y += self.player.speed

            # Joueur 2
            if keys[pygame.K_UP] and self.player.P2_y > score_bar_height:
                self.player.P2_y -= self.player.speed
            if keys[pygame.K_DOWN] and self.player.P2_y + player_height < self.HEIGHT:
                self.player.P2_y += self.player.speed


        pygame.quit()
