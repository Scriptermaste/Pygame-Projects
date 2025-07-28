import pygame
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Trivia Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

running = True
clock = pygame.time.Clock()

question_answered = False
correct = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not question_answered:
        screen.fill(white)
        font = pygame.font.SysFont(None, 80)
        question_text= font.render("What is 2+2? ", True, (black))
        screen.blit(question_text, (width // 2 - question_text.get_width() // 2,
                              height // 2 - question_text.get_height()//2-90))
        font = pygame.font.SysFont(None, 50)
        answer_a= font.render("A) 4 ", True, (black))
        answera_button = screen.blit(answer_a, (width // 2 - answer_a.get_width() // 2,
                              height // 2 - answer_a.get_height()//2-30))
        
        answer_b = font.render("B) 2 ", True, (black))
        answerb_button = screen.blit(answer_b, (width // 2 - answer_b.get_width() // 2,
                              height // 2 - answer_b.get_height()//2-0))
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if answera_button.collidepoint(mouse_pos):
                correct = True
                question_answered = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if answerb_button.collidepoint(mouse_pos):
                question_answered = True
    else:
        if correct:
            screen.fill(black)
            font = pygame.font.SysFont(None, 80)
            correct_text = font.render("Correct!", True, (green))
            screen.blit(correct_text, (width // 2 - correct_text.get_width() // 2,
                                    height // 2 - correct_text.get_height()//2-30))
        else:
            screen.fill(black)
            font = pygame.font.SysFont(None, 80)
            wrong_text= font.render("Wrong!", True, (red))
            screen.blit(wrong_text, (width // 2 - wrong_text.get_width() // 2,
                                    height // 2 - wrong_text.get_height()//2-30))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()  
