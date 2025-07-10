import pygame
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

gravity = 0.5
jump_strength = -15


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player_speed = 5
        self.velocity_y = 0
        self.velocity_x = 0
        self.not_jumping = True
    def update(self):
        ground = height
        self.rect.x += self.velocity_x

        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.player_speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.player_speed
        if keys[pygame.K_SPACE] and  self.not_jumping:
            self.velocity_y = jump_strength
            self.not_jumping = False
        

        self.velocity_y += gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= ground:
            self.rect.bottom = ground
            self.velocity_y = 0
            self.not_jumping = True
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.velocity_x = 0
                elif self.velocity_x < 0:
                    self.velocity_x = 0
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
            
                    self.velocity_y = 0
                    self.not_jumping = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((300, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Winners(pygame.sprite.Sprite):
    def __init__(self, x, y, color, WIDTH, HEIGHT):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))


platform1 = Platform(x= 300, y=500, color=black)
platform2 = Platform(x= 50, y=400, color=black)
platform3 = Platform(x= 300, y= 250, color=black)
player = Player(x=10, y=height)

player_group = pygame.sprite.Group(player)
platform_sprites = pygame.sprite.Group(platform1, platform2, platform3)
platforms = [platform1, platform2, platform3]

winner_area = Winners(x=400, y=240, color=green, WIDTH=100, HEIGHT=100)
winner_group = pygame.sprite.Group(winner_area)

running = True
clock = pygame.time.Clock()
won = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not won:
        player_group.update()
        platform_sprites.update()
        winner_area.update()

        hit = pygame.sprite.spritecollide(player, winner_group, False)
        if hit:
            won = True

        screen.fill(white)

        player_group.draw(screen)
        platform_sprites.draw(screen)
        winner_group.draw(screen)
    else:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        win_text = font.render("You Won!", True, (green))
        screen.blit(win_text, (width//2 - win_text.get_width()// 2,
                           height//2 - win_text.get_height()//2-30))
        
    pygame.display.flip()
    clock.tick(60)
pygame.quit()