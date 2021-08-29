import pygame,random
from math import sqrt

pygame.init()

screen_width,screen_height = 300,450
screen = pygame.display.set_mode((screen_width,screen_height))

background = pygame.image.load('bg.png')

class Ball(pygame.sprite.Sprite):
    def __init__(self,picture_path,ball_x,ball_y,x_speed,y_speed):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (ball_x,ball_y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.mouse_pressed = False
        self.friction = 0.1
        self.speed = 0
        self.initial_speed = 100
        self.initial_x_speed = 100
        self.initial_y_speed = 100
        self.stroke = 7

    def move(self):

        self.x_speed = (self.speed / self.initial_speed) * self.initial_x_speed
        self.y_speed = (self.speed / self.initial_speed) * self.initial_y_speed

        self.speed -= self.friction
        if self.speed < 0: 
            self.speed = 0

        self.ball_x += self.x_speed
        self.ball_y += self.y_speed

        self.rect.x = self.ball_x
        self.rect.y = self.ball_y

        if self.rect.x >= 300 - 15 or self.rect.x <= 0:
            self.initial_x_speed *= -1

        if self.rect.y >= 450 - 15 or self.rect.y <= 0:
            self.initial_y_speed *= -1
        
        # if pygame.sprite.spritecollide(ball,obstacle_group,False):
        #     print("collision")
        
        for rect in obstacle_group:
            # will be checking the collision from top bottom left and right 
            rect.colliderect(self.rect.x,self.rect.y + self.initial_y_speed,self.width,self.height)
            #obstacle.rect.letf - ball.rect.right
            #initial_x *= -1
            # viceversa
            #obstacle.rect.bottom - ball.rect.top
            #initial_y *= -1
            # viceversa



    def put_collide(self):
        #checking collision
        if pygame.sprite.spritecollide(self,ball_group,False):
            if ball == hole_group:

                ball.kill()
        
    def mouseposition(self):
        self.cursorpos = pygame.mouse.get_pos()
        if abs(self.x_speed) < 1 and abs(self.y_speed) < 1:
            if pygame.mouse.get_pressed()[0]:
                if not self.mouse_pressed:
                    self.x_speed = (self.cursorpos[0] - self.rect.center[0]) / 20
                    self.y_speed = (self.cursorpos[1] - self.rect.center[1]) / 20
                    self.speed = sqrt(self.x_speed**2 + self.y_speed**2)
                    self.initial_x_speed = self.x_speed
                    self.initial_y_speed = self.y_speed
                    self.initial_speed = self.speed
                    self.stroke -= 1

                self.mouse_pressed = True
                if self.stroke == 0:
                    pygame.quit()
            else:
                self.mouse_pressed = False

        self.x_speed *= 1
        self.y_speed *= 1

        if abs(self.x_speed) < 1 and abs(self.y_speed) < 1:
            pygame.draw.line(screen,(255,255,255),(self.rect.center),self.cursorpos)


class Put(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))


ball_group = pygame.sprite.Group()
ball = Ball('ball.png',screen_width /  2 - 16,350,1,2)
ball_group.add(ball)

obstacle_group = pygame.sprite.Group()
obstacle = Obstacles('tile64_dark.png',150,200)
obstacle_group.add(obstacle)

hole_group = pygame.sprite.Group()
hole = Put('hole.png',screen_width / 2 - 16,60)
hole_group.add(hole)

# ball_group2 = pygame.sprite.Group()
# for ball in range(1):
#     ball = Ball('ball.png',450,350,1,2)
#     ball_group2.add(ball)
# hole_group2 = pygame.sprite.Group()
# for holes in range (1):
#     holes = Put('hole.png',400,60)
#     hole_group2.add(holes)

clock = pygame.time.Clock()
while True:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    ball.mouseposition()
    
    ball_group.draw(screen)
    ball.move()
    ball.put_collide()
    
    obstacle_group.draw(screen)

    hole_group.draw(screen)

    # ball_group2.draw(screen)
    # ball.move()
    # hole_group2.draw(screen)
    # balls.mouseposition()

    pygame.display.update()
    clock.tick(60)
