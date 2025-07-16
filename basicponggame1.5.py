import pygame
import time
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

player1_score = 0
player2_score = 0

class Player_1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill(blue)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player_speed = 10
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= self.player_speed
        if keys[pygame.K_s]:
            self.rect.y += self.player_speed

        

class Player_2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill(red)
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.player_speed = 10
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.player_speed

    


class PongBall(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, x_speed, y_speed):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA )
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = x_speed
        self.velocity_y = y_speed
    def update(self):
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.velocity_y *= -1
        
player_1 = Player_1(x= 0, y= 150)
player_2 = Player_2(x= 790, y= 150)
players = pygame.sprite.Group()
players.add(player_1, player_2)

pongball = PongBall(x=50, y=50, radius=20, color=yellow,x_speed=5, y_speed=5)
pongballs = pygame.sprite.Group()
pongballs.add(pongball)

clock = pygame.time.Clock()
running = True
player1_victory = False
player2_victory = False

started = False
paused = False



while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not started:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        title_text = font.render("2 Player Pong!", True, (white))
        start_text = font.render("Start Game", True, (white))
        screen.blit(title_text, (width//2 - title_text.get_width()// 2,
                            height//2 - title_text.get_height()//2-90))
        Start_game = screen.blit(start_text, (width//2 - start_text.get_width()// 2,
                            height//2 - start_text.get_height()//2-10))
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if Start_game.collidepoint(mouse_pos):
                started = True


    if  not player1_victory and not player2_victory and started and not paused:
        screen.fill(black)

        players.update()
        pongballs.update()

        hit = pygame.sprite.spritecollide(player_1 , pongballs, False)
        hit2 = pygame.sprite.spritecollide(player_2, pongballs, False)
        if hit and pongball.velocity_x < 0:
            pongball.velocity_x *= -1
        if hit2 and pongball.velocity_x > 0:
            pongball.velocity_x *= -1
        if pongball.rect.right >= width:
            player1_score += 1
            pongball.velocity_x *= -1
        elif pongball.rect.left <= 0:
            player2_score += 1
            pongball.velocity_x *= -1
        if player1_score >= 3:
            player1_victory = True 
        elif player2_score >= 3:
            player2_victory = True

                

        players.draw(screen)
        pongballs.draw(screen)
        font = pygame.font.SysFont(None, 50)

        player1_score_text = font.render("Player 1 Score: "+str(player1_score), True, (white))
        player2_score_text = font.render("Player 2 Score: "+str(player2_score), True, (white))
        screen.blit(player1_score_text, (width//2 - player1_score_text.get_width()// 2,
                           height//2 - player1_score_text.get_height()//2-70))
        screen.blit(player2_score_text, (width//2 - player2_score_text.get_width()// 2,
                           height//2 - player2_score_text.get_height()//2-30))
    elif paused:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        paused_text = font.render("Paused", True, (white))
        screen.blit(paused_text, (width//2 - paused_text.get_width()// 2,
                        height//2 - paused_text.get_height()//2-70))            


    if player1_victory:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        player1_text = font.render("Player 1 Won!", True, (white))
        r_text = font.render("Press R to Restart", True, (white))
        screen.blit(player1_text, (width//2 - player1_text.get_width()// 2,
                           height//2 - player1_text.get_height()//2-30))
        screen.blit(r_text, (width//2 - r_text.get_width()//2,
                                 height//2 + player1_text.get_height()))

        if keys[pygame.K_r]:
            player1_victory = False
            player2_victory = False
            pongball.rect.x = 300
            pongball.rect.y = 300
            player_1.rect.y = 150
            player_2.rect.y = 150
            player1_score = 0
            player2_score = 0

    if player2_victory:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        player2_text = font.render("Player 2 Won!", True, (white))
        r_text = font.render("Press R to Restart", True, (white))
        screen.blit(player2_text, (width//2 - player2_text.get_width()// 2,
                           height//2 - player2_text.get_height()//2-30))
        screen.blit(r_text, (width//2 - r_text.get_width()//2,
                                 height//2 + player2_text.get_height()))
        if keys[pygame.K_r]:
            player2_victory = False
            player1_victory = False
            pongball.rect.x = 300
            pongball.rect.y = 300
            player_1.rect.y = 150
            player_2.rect.y = 150
            player1_score = 0
            player2_score = 0

    pygame.display.flip()
    clock.tick(60)
pygame.quit()