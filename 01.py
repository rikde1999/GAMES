import pygame

pygame.init()

screen_width,screen_height = 600,450
screen = pygame.display.set_mode((screen_width,screen_height))

background = pygame.image.load('bg.png')

class Ball(pygame.sprite.Sprite):
    def __init__(self,picture_path,ball_x,ball_y,x_speed,y_speed):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (ball_x,ball_y))
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        

        if self.rect.x >= 600 - 15 or self.rect.x <= 0:
            self.x_speed *= -1

        if self.rect.y >= 450 - 15 or self.rect.y <= 0:
            self.y_speed *= -1

    def mouseposition(self):
        self.cursorpos = pygame.mouse.get_pos()
        if abs(self.x_speed) < 0.01 and abs(self.y_speed) < 0.01:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.x_speed = (self.cursorpos[0] - self.rect.x) / 15
                    self.y_speed = (self.cursorpos[1] - self.rect.y) / 15
    
        self.x_speed *= 1
        self.y_speed *= 1

        if abs(self.x_speed) < 0.01 and abs(self.y_speed) < 0.01:
            pygame.draw.line(screen,(255,255,255),(self.ball_x,self.ball_y),self.cursorpos)

class Put(pygame.sprite.Sprite): 
    def __init__(self,picture_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))


ball_group = pygame.sprite.Group()
ball = Ball('ball.png',300,300,1,2)
ball_group.add(ball)

hole_group = pygame.sprite.Group()
hole = Put('hole.png',300,60)
hole_group.add(hole)

clock = pygame.time.Clock()
while True:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
    ball.mouseposition()
    ball_group.draw(screen)
    ball.move()
    
    hole_group.draw(screen)

    pygame.display.update()
    clock.tick(60)