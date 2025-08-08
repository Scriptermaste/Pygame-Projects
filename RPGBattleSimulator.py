import pygame
pygame.init()

width = 800
height = 600

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle Simulator")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, player_width, player_height):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, color, healthbar_width, healthbar_height):
        super().__init__()
        self.image = pygame.Surface((healthbar_width, healthbar_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, enemy_width, enemy_height):
        super().__init__()
        self.image = pygame.Surface((enemy_width, enemy_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

player = Player(x=100, y=400, color=blue, player_width=50, player_height=50)
player_group = pygame.sprite.Group(player)

enemy = Enemy(x=100, y=100, color=red, enemy_width=50, enemy_height=50)
enemy_group = pygame.sprite.Group(enemy)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player_group.update()
    enemy_group.update()

    player_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()