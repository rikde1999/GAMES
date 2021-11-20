import sys, random, pygame

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 400,700
screen = pygame.display.set_mode((screen_width, screen_height))


class Board:
    def __init__(self):
        self.original_image = pygame.transform.scale((pygame.image.load('wood1.png')),(131,131))
        self.speed = random.randint(-2,2)
        if self.speed == 0: 
            self.speed = -1
        self.angle = 0
        self.rotation = True
                
    def rotation_speed(self):
    
        if self.rotation:
            self.speed += random.uniform(0,0.1)
        
        else:
            self.speed -= random.uniform(0,0.1)

        if self.speed >= 6:
            self.rotation= False

        if self.speed <= -6:
            self.rotation= True

        if random.random() < 0.002:
            self.rotation= not self.rotation

    def update(self):
        self.angle += self.speed
        self.image = pygame.transform.rotozoom(self.original_image, self.angle , 1)
        self.rect = self.image.get_rect(center = (screen_width//2, screen_height//4))
        if abs(self.angle) == 360: 
            self.angle = 0

        self.rotation_speed()

    def draw(self):
        screen.blit(self.image,self.rect)

class Knife:
    def __init__(self):
        self.moving = False
        self.speed = 20
        self.angle = 0
        self.original_image = pygame.transform.scale(pygame.image.load('knife1.png'),(15,100))
        self.image = self.original_image#pygame.transform.rotozoom(self.original_image , 0 ,0.4)
        self.rect = self.original_image.get_rect(center = (screen_width/2,screen_height))
        self.y = screen_height
        self.x = screen_width/2 - self.image.get_width()/2

    def update(self):
        if not(self.rect.centery <= screen_height//4 + 64.6):
            self.y -= self.speed
            self.rect.centery -= self.speed
            

    def rotate(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.center = self.image.get_rect(center = (screen_width/2,screen_height/4))

    def draw(self):
        screen.blit(self.image, self.rect)

class Main:
    def __init__(self):
        self.collision = False
        self.board = Board()
        self.knives = []
        # self.knife_image = pygame.transform.scale(pygame.image.load('Data/knife1.png'),(15,100))
        self.knife_image = pygame.transform.rotozoom(pygame.image.load('knife1.png'), 0 ,0.2)
        self.knife_rect = self.knife_image.get_rect(center = (screen_width/2,0))
        self.knife_rect.bottom = screen_height


    def update(self):
        self.board.update()
        
        for knife in self.knives:
            knife.update()
            
            self.knife_image
            knife.rotate()


        screen.blit(self.board.image, self.board.rect)

    def draw(self):
        screen.blit(self.knife_image, self.knife_rect)
        for knife in self.knives:
            knife.draw()

        screen.blit(self.board.image, self.board.rect)

main = Main()

while True:
    screen.fill('light green')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                knife = Knife()
                main.knives.append(knife)

    main.update()
    main.draw()

    if main.collision:
        main = Main()
        sys.exit()

    pygame.display.update()
    clock.tick(60)