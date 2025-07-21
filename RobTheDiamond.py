import pygame
pygame.init()

width = 800
height = 600

black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
green = (0, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Steal The Diamond")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height, color):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.playerspeed = 2
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= self.playerspeed
        if keys[pygame.K_s]:
            self.rect.y += self.playerspeed
        if keys[pygame.K_a]:
            self.rect.x -= self.playerspeed
        if keys[pygame.K_d]:
            self.rect.x += self.playerspeed

        if keys[pygame.K_LSHIFT]:
            self.playerspeed = 5
        if not keys[pygame.K_LSHIFT]:
            self.playerspeed = 3
            
class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y, diamond_width, diamond_height, color):
        super().__init__()
        self.image = pygame.Surface((diamond_width, diamond_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))  

class Exit_Door(pygame.sprite.Sprite):
    def __init__(self, x, y, door_width, door_height, color):
        super().__init__()
        self.image = pygame.Surface((door_width, door_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y)) 

exit_door = Exit_Door(x=400, y=height, door_width=100, door_height=10, color=green) 
door_group = pygame.sprite.Group(exit_door)

diamond = Diamond(x=550,y=150, diamond_width=100, diamond_height=100, color=cyan)   
diamond_group = pygame.sprite.Group(diamond)     

player = Player(x=100, y= 50, player_width=50, player_height=50, color=red)
player_group = pygame.sprite.Group(player)

clock = pygame.time.Clock()
running = True

level1_completion = False
got_diamond = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not level1_completion:
        steal = pygame.sprite.spritecollide(player, diamond_group, True)
        exit = pygame.sprite.spritecollide(player, door_group, False)
        if steal:
            got_diamond = True


        player_group.update()
        diamond_group.update()
        door_group.update()

        screen.fill(black)
    
        player_group.draw(screen)
        diamond_group.draw(screen)
        door_group.draw(screen)
    if got_diamond and exit:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        level1_text = font.render("Level 1 Complete!", True, (green))
        screen.blit(level1_text, (width // 2 - level1_text.get_width() // 2,
                                  height // 2 - level1_text.get_height()//2-30))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()