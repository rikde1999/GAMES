import pygame
import random

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_X = 3
        self.speed_y = 2

    def check_screen_boundaries(self):
        if self.rect.left < 0:
            self.speed_X *= -1
        if self.rect.right > screen.get_width():
            self.speed_X *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen.get_height():
            self.speed_y *= -1

    def collisions(self, sprites):
        for sprite in sprites:
            if sprite != self:
                if self.rect.colliderect(sprite.rect):
                    if abs(self.rect.top - sprite.rect.bottom) < 10:
                        self.speed_y *= -1
                    if abs(self.rect.bottom - sprite.rect.top) < 10:
                        self.speed_y *= -1
                    if abs(self.rect.left - sprite.rect.right) < 10:
                        self.speed_X *= -1
                    if abs(self.rect.right - sprite.rect.left) < 10:
                        self.speed_X *= -1

    def move(self):
        self.rect.x += self.speed_X
        self.rect.y += self.speed_y

    def update(self, rects):
        self.check_screen_boundaries()
        self.collisions(rects)
        self.move()


rectangles = pygame.sprite.Group()
for i in range(3):
    x = random.randint(50, screen.get_width()-50)
    y = random.randint(50, screen.get_height()-50)
    rectangles.add(Rectangle(x, y))

while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    rectangles.update(rectangles.sprites())
    rectangles.draw(screen)

    pygame.display.update()
    clock.tick(60)
