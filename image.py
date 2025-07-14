import pygame
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Image")

white = (255, 255, 255)

class Image(pygame.sprite.Sprite):
   def __init__(self, x, y, image_width, image_height):
      super().__init__()
      self.image = pygame.image.load("Image/binary.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (image_width, image_height))
      self.rect = self.image.get_rect(bottomleft=(x, y))
   def update(self):
      pass
image = Image(x= 350, y =350, image_width= 100, image_height=100)
image_group = pygame.sprite.Group(image)
      


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
         running = False
   
    image_group.update()
    screen.fill(white)
    image_group.draw(screen)
    pygame.display.flip()
pygame.quit()