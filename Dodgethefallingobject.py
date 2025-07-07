import pygame
import random

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge Poop!")

player_color = (0, 138, 255)
player_speed = 10

cyan = (0, 255, 255)
red = (255, 0, 0)
brown = (139, 69, 19)
black = (0, 0, 0)
white = (255, 255, 255)

velocity_y = 0
gravity = .5

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 0
        self.velocity_y = 0
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= player_speed
        if keys[pygame.K_d]:
            self.rect.x += player_speed
        if keys[pygame.K_w]:
            self.rect.y -= player_speed
        if keys[pygame.K_s]:
            self.rect.y += player_speed

        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

class Falling_Object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(brown)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
    def update(self):
        if self.rect.top > height:
            self.respawn()

        self.velocity_y += gravity
        self.rect.y += self.velocity_y
    def respawn(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = 0
        self.velocity_y = 0

player = Player(500, 500)
player_group = pygame.sprite.Group()
player_group.add(player)

falling_object = Falling_Object(50, 50)
falling_objects = pygame.sprite.Group()

number_of_falling_objects = 5

for i in range(number_of_falling_objects):    
    x = random.randint(0, width - 50)
    y = random.randint(-300, -50)
    falling_objects.add(Falling_Object(x, y))

running = True
clock = pygame.time.Clock()
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if not game_over:

        hit = pygame.sprite.spritecollide(player, falling_objects, True)
        if hit:
            game_over = True
        # Update the player and the falling object
        player_group.update()
        falling_objects.update()
        
        screen.fill(cyan)

        # Draw the player and the falling object
        player_group.draw(screen)
        falling_objects.draw(screen)

    else:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        text = font.render("Game Over!", True, (white))
        space_text = font.render("Press SPACE To Restart!", True, (white))
        screen.blit(text, (width//2 - text.get_width()// 2,
                           height//2 - text.get_height()//2-30))
        screen.blit(space_text, (width//2 - text.get_width()//2-120,
                                 height//2 + text.get_height()//10+2))
        if keys[pygame.K_SPACE]:
            game_over = False
        
    # Flips the display and caps the game at 60 FPS
    pygame.display.flip()
    clock.tick(60)

pygame.quit()