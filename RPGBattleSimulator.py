import pygame
pygame.init()

width = 800
height = 600



red = (255, 0, 0)
cyan = (0, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

enemy_defeated = False
surrendered = False

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
class enemy_health(pygame.sprite.Sprite):
    def __init__(self, x, y, color, healthbar_width, healthbar_height):
        super().__init__()
        self.image = pygame.Surface((healthbar_width, healthbar_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class ManaBar(pygame.sprite.Sprite):
    def __init__(self, x, y, color, mana_width, mana_height):
        super().__init__()
        self.image = pygame.Surface((mana_width, mana_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))


player = Player(x=100, y=400, color=cyan, player_width=50, player_height=50)
player_group = pygame.sprite.Group(player)

healthbar = HealthBar(x= 250, y=400, color=green, healthbar_width=100, healthbar_height=20)
healthbar_group = pygame.sprite.Group(healthbar)

manabar = ManaBar(x=400, y=400, color=blue, mana_width=100, mana_height=20)
manabar_group = pygame.sprite.Group(manabar)

enemy = Enemy(x=100, y=100, color=red, enemy_width=50, enemy_height=50)
enemy_group = pygame.sprite.Group(enemy)

running = True
clock = pygame.time.Clock()

all_groups = [player_group, healthbar_group, manabar_group, enemy_group]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not enemy_defeated:
        screen.fill(black)
        font = pygame.font.SysFont(None, 60)
        info_text = font.render("Player", True, (white))
        screen.blit(info_text, (width // 2 - info_text.get_width() // 2-280,
                                   height // 2 - info_text.get_height()//2+150))

        font = pygame.font.SysFont(None, 50)
        attack_text = font.render("> Attack", True, (white))
        attack_button = screen.blit(attack_text, (width // 2 - attack_text.get_width() // 2-280,
                                   height // 2 - attack_text.get_height()//2+200))
        font = pygame.font.SysFont(None, 50)
        defend_text = font.render("> Defend", True, (white))
        defend_button = screen.blit(defend_text, (width // 2 - defend_text.get_width() // 2-280,
                                   height // 2 - defend_text.get_height()//2+250))

        font = pygame.font.SysFont(None, 50)
        inventory_text = font.render("> Inventory", True, (white))
        inventory_button = screen.blit(inventory_text, (width // 2 - inventory_text.get_width() // 2-100,
                                   height // 2 - inventory_text.get_height()//2+250))
        
        font = pygame.font.SysFont(None, 50)
        surrender_text = font.render("> Surrender", True, (white))
        surrender_button = screen.blit(surrender_text, (width // 2 - surrender_text.get_width() // 2-100,
                                   height // 2 - surrender_text.get_height()//2+200))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if surrender_button.collidepoint(mouse_pos):
                surrendered = True

        
        
        for group in all_groups:
            group.update()


        for group in all_groups:
            group.draw(screen)

        if surrendered:
            screen.fill(black)
            font = pygame.font.SysFont(None, 80)
            surrendered_text = font.render("You Lost!", True, (red))
            screen.blit(surrendered_text, (width // 2 - surrendered_text.get_width() // 2,
                                   height // 2 - surrendered_text.get_height()//2-90))

    else:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        victory_text = font.render("You Won!", True, (white))
        screen.blit(victory_text, (width // 2 - victory_text.get_width() // 2,
                                   height // 2 - victory_text.get_height()//2-90))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()