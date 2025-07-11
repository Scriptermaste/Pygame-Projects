import pygame
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Escape!")

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height, color):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player_speed = 5
        
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)
        
        self.velocity_y = self.rect.y
        self.velocity_x= self.rect.x

        keys = pygame.key.get_pressed()
        #WASD Controls
        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.player_speed
        if keys[pygame.K_w]:
            self.rect.y -= self.player_speed
        if keys[pygame.K_s]:
            self.rect.y += self.player_speed
        # Up/Left/Down/Right Controls
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.player_speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.player_speed

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = self.velocity_x

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.y = self.velocity_y


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_width, wall_height, color):
        super().__init__()
        self.image = pygame.Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Winners(pygame.sprite.Sprite):
    def __init__(self, x, y, winner_width, winner_height, color):
        super().__init__()
        self.image = pygame.Surface((winner_width, winner_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

player = Player(x=30, y=height, player_width=50, player_height=50, color=red)
player_group = pygame.sprite.Group(player)

wall_1 = Wall(x= 0, y=500, wall_width=400, wall_height=20, color=black)
wall_2 = Wall(x= 250, y=400, wall_width= 800, wall_height=20, color=black)
wall_3 = Wall(x= 0, y= 300, wall_width=400, wall_height=20, color=black)
wall_4 = Wall(x= 250, y=200, wall_width= 800, wall_height=20, color=black)
wall_5 = Wall(x= 0, y= 100, wall_width=400, wall_height=20, color=black)
walls = [wall_1, wall_2, wall_3, wall_4, wall_5]
wall_group = pygame.sprite.Group(walls)


winners_area = Winners(x = 0 ,y = 50, winner_width= 1000, winner_height=100, color=green)
winner_group = pygame.sprite.Group(winners_area)

running = True
clock = pygame.time.Clock()
won = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not won:
        player_group.update()
        wall_group.update()
        winner_group.update()
        
        hit = pygame.sprite.spritecollide(player, winner_group, False)
        if hit:
            won = True

        screen.fill(white)
        player_group.draw(screen)
        wall_group.draw(screen)
        winner_group.draw(screen)
    else:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        win_text = font.render("You Win!", True, (green))
        screen.blit(win_text, (width//2 - win_text.get_width()// 2,
                           height//2 - win_text.get_height()//2-30))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
