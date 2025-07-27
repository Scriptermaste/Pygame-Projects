import pygame
pygame.init()

width = 800
height = 600

black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

started = False

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
        
        if keys[pygame.K_UP]:
            self.rect.y -= self.playerspeed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.playerspeed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.playerspeed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.playerspeed

        if keys[pygame.K_LSHIFT]:
            self.playerspeed = 5
        if not keys[pygame.K_LSHIFT]:
            self.playerspeed = 3
    
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.y > 0:
                    self.rect.bottom = wall.rect.top
            
                    self.rect.y = 0
                    self.not_jumping = True
                elif self.rect.y < 0:
                    self.rect.top = wall.rect.bottom
                    self.rect.y = 0
        

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y, diamond_width, diamond_height, color):
        super().__init__()
        self.image = pygame.Surface((diamond_width, diamond_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))  
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_width, wall_height, color):
        super().__init__()
        self.image = pygame.Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Exit_Door(pygame.sprite.Sprite):
    def __init__(self, x, y, door_width, door_height, color):
        super().__init__()
        self.image = pygame.Surface((door_width, door_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y)) 

class Guard(pygame.sprite.Sprite):
    def __init__(self,  guard_width, guard_height, color, waypoints, speed):
        super().__init__()
        self.image = pygame.Surface((guard_width, guard_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=waypoints[0])
    
        self.speed = speed
        self.current_point = 1
        self.wait_time = 1000
        self.waypoints = waypoints
        self.lastwait = 0
        self.waiting = False
    def update(self, current_time):
        if self.waiting:
            if current_time - self.lastwait >= self.wait_time:
                self.waiting = False
                self.current_point = (self.current_point + 1) % len(self.waypoints)
            return
        
        target = self.waypoints[self.current_point]

        dx = target[0] - self.rect.x
        dy = target[1] - self.rect.y

        dist = (dx**2 + dy**2) ** .5

        if dist < self.speed:
            self.rect.topleft = target
            self.waiting = True
            self.lastwait = current_time

        else:
            direction_x = dx / dist
            direction_y = dy / dist
            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed
        
wall = Wall(x=400, y=250, wall_width=50, wall_height=300, color=white)
walls = [wall]
wall_group = pygame.sprite.Group(wall)

exit_door = Exit_Door(x=400, y=height, door_width=100, door_height=10, color=green) 
door_group = pygame.sprite.Group(exit_door)

guard = Guard(guard_width=50, guard_height=50, color=blue, speed=3, waypoints=[(100, 200), (300, 200), (300, 350), (100, 350)])
guard_group = pygame.sprite.Group(guard)

diamond = Diamond(x=550,y=150, diamond_width=100, diamond_height=100, color=cyan)   
diamond_group = pygame.sprite.Group(diamond)     

player = Player(x=100, y= 50, player_width=50, player_height=50, color=red)
player_group = pygame.sprite.Group(player)

clock = pygame.time.Clock()
running = True

failed = False

level1_completion = False
got_diamond = False

condition = None

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    font = pygame.font.SysFont(None, 80)
    title = font.render("Rob The Diamond!", True, (white))
    screen.blit(title, (width // 2 - title.get_width() // 2,
                              height // 2 - title.get_height()//2-90))
    font = pygame.font.SysFont(None, 80)
    Start = font.render("Start", True, (white))
    start_button = screen.blit(Start, (width // 2 - Start.get_width() // 2,
                              height // 2 - Start.get_height()//2-30))

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            started = True


    if not level1_completion and started:
        screen.fill(black)
        font = pygame.font.SysFont(None, 50)
        diamond = font.render("Has Diamond: "+str(condition), True, (white))
        diamond_condition = screen.blit(diamond, (width // 2 - diamond.get_width() // 2-250,
                              height // 2 - diamond.get_height()//2-280))
        if got_diamond == True:
            condition = "Yes"
        else:
            condition = "No"
        
            

        steal = pygame.sprite.spritecollide(player, diamond_group, True)
        exit = pygame.sprite.spritecollide(player, door_group, False)
        caught = pygame.sprite.spritecollide(player, guard_group, False)
        if steal:
            got_diamond = True

        if caught:
            failed = True


        player_group.update()
        diamond_group.update()
        door_group.update()
        wall_group.update()
        guard_group.update(current_time)

    
        player_group.draw(screen)
        diamond_group.draw(screen)
        door_group.draw(screen)
        wall_group.draw(screen)
        guard_group.draw(screen)
    if got_diamond and exit:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        level1_text = font.render("Level 1 Complete!", True, (green))
        screen.blit(level1_text, (width // 2 - level1_text.get_width() // 2,
                                  height // 2 - level1_text.get_height()//2-30))
    if failed:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        level1_text = font.render("Caught!", True, (red))
        screen.blit(level1_text, (width // 2 - level1_text.get_width() // 2,
                                  height // 2 - level1_text.get_height()//2-30))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()