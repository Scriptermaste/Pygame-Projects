import pygame
import time
pygame.init()

width = 800
height = 600

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hello World!")

running = True
clock = pygame.time.Clock()

World = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not World:
        screen.fill(white)
        font = pygame.font.SysFont(None, 80)
        Hello_text = font.render("Hello", True, (black))
        screen.blit(Hello_text, (width // 2 - Hello_text.get_width() // 2,
                                 height // 2 - Hello_text.get_height()//2-30))
        time.sleep(.5)
        World = True
    else:
        screen.fill(white)
        font = pygame.font.SysFont(None, 80)
        World_text = font.render("World!", True, (black))
        screen.blit(World_text, (width // 2 - World_text.get_width() // 2,
                                        height // 2 - World_text.get_height()//2-30))
        time.sleep(.5)
        World = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()