import pygame
pygame.init()

width = 800
height = 600

blue = (0, 0, 255)
black = (0, 0, 0)

chapter_1 = True

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Detective Game")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, player_width, player_height):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.playerspeed = 3
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.playerspeed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.playerspeed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.playerspeed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.playerspeed



player = Player(x=50, y=50, color=blue, player_width=50, player_height=50)
player_group = pygame.sprite.Group(player)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if chapter_1:
        screen.fill(black)
        player_group.update()

        player_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()