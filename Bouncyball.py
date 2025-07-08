import pygame
pygame.init()

width = 800
height = 600

blue = (0, 0, 255)
white = (255, 255, 255)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncy Ball!")

class Bouncyball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, x_speed, y_speed):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((radius * 2,radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.velocity_x = 0 
        self.velocity_x = 0 

        self.speed_y = x_speed
        self.speed_x = y_speed
    def update(self):
        #Movement of the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #Bounce on horizontal walls
        if self.rect.left <= 0 or self.rect.right >= width:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.speed_y *= -1


bouncyball = Bouncyball(x=300, y=200, radius=20, color=(blue), x_speed=5, y_speed=3)
bouncyballs = pygame.sprite.Group()
bouncyballs.add(bouncyball)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)  
    bouncyballs.update()
    bouncyballs.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()