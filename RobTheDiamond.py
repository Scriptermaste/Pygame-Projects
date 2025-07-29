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

running = True
failed = False
level1_completion = False
got_diamond = False
started = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Steal The Diamond")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height, color):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)
        keys = pygame.key.get_pressed()

        self.playerspeed = 5 if keys[pygame.K_LSHIFT] else 3

        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.playerspeed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.playerspeed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.playerspeed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.playerspeed

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left

                elif dx < 0:
                    self.rect.left = wall.rect.right
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top

                elif dy < 0:
                    self.rect.top = wall.rect.bottom
                   
        

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y, diamond_width, diamond_height, color):
        super().__init__()
        self.image = pygame.Surface((diamond_width, diamond_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))   
        print(self.rect.y)  
    def update(self,caught, steal):
        if steal:
            self.image.fill(black)

        if caught:
            self.respawn()
            self.image.fill(cyan)

    def respawn(self):
        self.rect.x = 550
        self.rect.y = 50

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

diamondx = 550
diamondy = 150

diamond = Diamond(x=diamondx, y=diamondy, diamond_width=100, diamond_height=100, color=cyan)   
diamond_group = pygame.sprite.Group(diamond)     

player = Player(x=100, y= 50, player_width=50, player_height=50, color=red)
player_group = pygame.sprite.Group(player)

clock = pygame.time.Clock()


condition = None

while running:
    keys = pygame.key.get_pressed()
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

        steal = pygame.sprite.spritecollide(player, diamond_group, False)
        exit = pygame.sprite.spritecollide(player, door_group, False)
        caught = pygame.sprite.spritecollide(player, guard_group, False)
        if steal:
            got_diamond = True
            diamond_group.remove(diamond)
            

        if caught:
            failed = True

        diamond_group.update(caught=bool(caught), steal = bool(steal))
        player_group.update()
        door_group.update()
        wall_group.update()
        guard_group.update(current_time)

        diamond_group.draw(screen)
        player_group.draw(screen)
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
                                  height // 2 - level1_text.get_height()//2-90))
        
        restart_text = font.render("Press R To Restart", True, (red))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2,
                                  height // 2 - restart_text.get_height()//2-30))
        if keys[pygame.K_r]:
            failed = False
            player.rect.x = 100
            player.rect.y = 50
            got_diamond = False
            level1_completion = False
            diamond_group.draw(screen)
            
            

    pygame.display.flip()
    clock.tick(60)
pygame.quit()