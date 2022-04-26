import pygame,sys,random

pygame.init()

screen_width,screen_height = 800,600 #
screen = pygame.display.set_mode((screen_width,screen_height))

class Rectangles(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.speed_x = 4
        self.speed_y = 3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

        if self.rect.bottom >= screen_height or self.rect.top <= 0:
            self.speed_y *= -1


player_group= pygame.sprite.Group()
for i in range(6):
    player = Rectangles(random.randrange(50,screen_width - 50),random.randrange(50,screen_height - 50))
    player_group.add(player)

clock = pygame.time.Clock()
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player_group.draw(screen)
    player_group.update()

    pygame.display.update()
    clock.tick(60)
