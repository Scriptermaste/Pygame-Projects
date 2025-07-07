import pygame
import random
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch The Falling Object")

player_color = (162, 42, 42)
player_speed = 15

cyan = (0, 255, 255)
red = (255, 0, 0)

running = True
clock = pygame.time.Clock()

#For gravity
velocity_y = 0
gravity = .5


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(player_color)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_x = 0 
        self.velocity_y = 0
    def update(self):
        # Gravity logic

        self.rect.x += self.velocity_x

        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= player_speed
        if keys[pygame.K_d]:
            self.rect.x += player_speed
        if keys[pygame.K_w]:
            self.rect.y -= player_speed
        if keys[pygame.K_s]:
            self.rect.y += player_speed


# Creating a new sprite called the falling object
class Falling_Object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50)) # Sets the appearance for the Sprite
        #Make the object red
        self.image.fill(red)
        # Make the object a rectangle
        self.rect = self.image.get_rect(topleft=(x, y))
        # Velocity for the object
        self.velocity_x = 0
        self.velocity_y = 0
    def update(self):
        if self.rect.top > height:
            self.kill()

        self.velocity_y += gravity
        self.rect.y += self.velocity_y
        screen_rect = pygame.Rect(0, 0, width, height)



        if self.rect.top > 600:
            self.respawn()


    def respawn(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = 0
        self.velocity_y = 0

# Adding the sprite in the all sprites group
falling_object = Falling_Object(50, 50)
falling_objects = pygame.sprite.Group()
falling_objects.add(falling_object)

player = Player(50, 50)
player_group = pygame.sprite.Group()
player_group.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    hit = pygame.sprite.spritecollide(player, falling_objects, True)
    if hit:
        
        random_x = random.randint(0, width - 50)
        new_falling_object = Falling_Object(random_x, 0)
        falling_objects.add(new_falling_object)

    screen.fill(cyan)

    player_group.update()
    falling_objects.update()

    player_group.draw(screen)
    falling_objects.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()