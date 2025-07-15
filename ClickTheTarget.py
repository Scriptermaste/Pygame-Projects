import pygame
import random
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Click The Target")

score = 0
time = 60

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, target_width, target_height):
        super().__init__()
        self.image = pygame.Surface((target_width, target_height))
        self.image.fill(red)
        self.rect = self.image.get_rect(bottomleft=(x, y))


target = Target(x=100, y=550, target_width=100, target_height=100)
target_group = pygame.sprite.Group(target)
            
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, time - seconds_passed)
    if time_left > 0:
        screen.fill(white)
        target_group.update()
        target_group.draw(screen)


        font = pygame.font.SysFont(None, 50)
        score_text = font.render("Score: "+str(score), True, (black))
        screen.blit(score_text, (width//2 - score_text.get_width()// 2,
                            height//2 - score_text.get_height()//2-30))
        time_text = font.render("Time: "+str(time_left), True, (black))
        screen.blit(time_text, (width//2 - time_text.get_width()// 2,
                                height // 2 - time_text.get_height()//2-90))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if target.rect.collidepoint(mouse_pos):
                target.rect.topleft = (random.randint(0, width - target.rect.width),
                                    random.randint(0, height - target.rect.height))
                score = score + 1
    else:
        screen.fill(black)
        times_up_text = font.render("Times Up!", True, (white))
        screen.blit(times_up_text, (width//2 - times_up_text.get_width()// 2,
                                height // 2 - times_up_text.get_height()//2-90))
        score_text = font.render("Score: "+str(score), True, (white))
        screen.blit(score_text, (width//2 - score_text.get_width()// 2,
                            height//2 - score_text.get_height()//2-30))

    pygame.display.flip()
pygame.quit()
