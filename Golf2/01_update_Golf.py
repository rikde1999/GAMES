import pygame,random,sys
from math import *
from pygame.math import Vector2

pygame.init()

screen_width,screen_height = 300,450
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
        self.mouse_pressed = False
        self.friction = 0.1
        self.speed = 0
        self.initial_speed = 100
        self.initial_x_speed = 100
        self.initial_y_speed = 100
        self.arrow = pygame.sprite.GroupSingle()
        self.arrow.add(Arrow('point.png',self.rect.centerx,self.rect.centery))
        self.strokes = 7
        self.shot = pygame.mixer.Sound("swing.mp3")
        self.par = pygame.mixer.Sound("hole.mp3")
        self.angle = 0

    def sound(self):
        self.shot.play()

    def move(self):

        self.x_speed = (self.speed / self.initial_speed) * self.initial_x_speed
        self.y_speed = (self.speed / self.initial_speed) * self.initial_y_speed

        self.speed -= self.friction
        if self.speed < 0:
            self.speed = 0

        self.ball_x += self.x_speed
        self.ball_y += self.y_speed

        self.rect.x = self.ball_x
        ball.horizontal_collision()

        self.rect.y = self.ball_y
        ball.vertical_collision()

        self.arrow.update(self.rect, self.angle)
        if self.speed < 1:
            self.arrow.draw(screen)

        if self.rect.x >= 300 - 15 or self.rect.x <= 2:
            self.initial_x_speed *= -1

        if self.rect.y >= 450 - 15 or self.rect.top <= 2:
            self.initial_y_speed *= -1

        if pygame.sprite.spritecollide(ball,hole_group,False):
            self.par.play()
            ball.sound()
            self.kill()

    def horizontal_collision(self):
        for rect in obstacle_group.sprites():
            if rect.rect.colliderect(self.rect):
                if self.rect.left <= rect.rect.right:
                    self.rect.left *= -1


                if self.rect.right >= rect.rect.left:
                    self.rect.right *= -1

    def vertical_collision(self):
        for rect in obstacle_group.sprites():
            if rect.rect.colliderect(self.rect):
                if self.rect.top <= rect.rect.bottom:
                    self.rect.top *= -1

                if self.rect.bottom >= rect.rect.top:
                    self.rect.bottom *= -1

    def mouseposition(self):
        self.cursorpos = pygame.mouse.get_pos()
        if abs(self.x_speed) < 1 and abs(self.y_speed) < 1:
            self.angle = degrees(atan2(((self.cursorpos[1] - self.rect.centery)*-1), (self.cursorpos[0] - self.rect.centerx))) - 90
            print(self.angle)
            if pygame.mouse.get_pressed()[0]:
                if not self.mouse_pressed:
                    self.x_speed = (self.cursorpos[0] - self.rect.center[0]) / 20
                    self.y_speed = (self.cursorpos[1] - self.rect.center[1]) / 20
                    self.speed = sqrt(self.x_speed**2 + self.y_speed**2)
                    self.initial_x_speed = self.x_speed
                    self.initial_y_speed = self.y_speed
                    self.initial_speed = self.speed
                    self.strokes -= 1
                    
                self.mouse_pressed = True
                if self.strokes == 0:
                    pygame.quit()
            else:
                self.mouse_pressed = False

        self.x_speed *= 1
        self.y_speed *= 1

        # if abs(self.x_speed) < 1 and abs(self.y_speed) < 1:
        #     pass
            # pygame.draw.line(screen,(255,255,255),(self.rect.center),self.cursorpos)

    def update(self):
        self.mouseposition()
        self.move()



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


class Arrow(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.orig_image = self.image
        self.pos = Vector2(x_pos,y_pos)

    def rotate(self, ball_rect, angle):
        direction = pygame.mouse.get_pos() - self.pos
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        #radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pygame.transform.rotate(self.orig_image, angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center = ball_rect.center)

    def update(self, ball_rect, angle):
        self.rotate(ball_rect, angle)


class PowerMeter(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos,power = 100):
        super().__init__()
        self.power = power
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center=(x_pos,y_pos))

power_group = pygame.sprite.Group()
powers = PowerMeter('powermeter_bg.png',screen_width - 26,350)


#arrow_group = pygame.sprite.Group()
#arrow = Arrow('point.png',screen_width/2 - 7,350)
#arrow_group.add(arrow)

ball_group = pygame.sprite.Group()
ball = Ball('ball.png',screen_width /  2 - 16,350,1,2)
ball_group.add(ball)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacles('tile64_dark.png',100,200))
obstacle_group.add(Obstacles('tile64_light.png',50,50))
obstacle_group.add(Obstacles('tile32_dark.png',130,100))
obstacle_group.add(Obstacles('tile64_light.png',200,200))
obstacle_group.add(Obstacles('tile64_dark.png',160,400))
obstacle_group.add(Obstacles('tile32_dark.png',160,100))

hole_group = pygame.sprite.Group()
hole = Put('hole.png',screen_width / 2 - 16,60)
hole_group.add(hole)


clock = pygame.time.Clock()
while True:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.sound()

    
    power_group.draw(screen)

    ball_group.update()
    ball_group.draw(screen)
    
    obstacle_group.draw(screen)

    hole_group.draw(screen)

    pygame.display.update()
    clock.tick(60)