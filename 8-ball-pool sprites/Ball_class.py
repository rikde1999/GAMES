import pygame
from math import radians,sin,cos

class Ball(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos,x_speed,y_speed,speed,angle):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.angle = angle 

    def move(self):
        self.rect.x = self.rect.x + self.speed*cos(radians(self.angle))
        self.rect.x = self.rect.y + self.speed*sin(radians(self.angle))

    def update(self):
    #     # self.draw()
        self.move()