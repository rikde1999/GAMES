import pygame

class Put(pygame.sprite.Sprite):
    def __init__(self,picture_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))