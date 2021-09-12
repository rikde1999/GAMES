import pygame
from pygame.math import Vector2

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