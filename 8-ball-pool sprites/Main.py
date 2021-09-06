import pygame,random
from settings import screen
from Ball_class import Ball

pygame.init()

ball_group = pygame.sprite.Group()
ball_group.add(Ball('ball1.png',200,200,1,2,4,10))
ball_group.add(Ball('ball2.png',100,300,1,2,4,10))
ball_group.add(Ball('ball3.png',20,20,1,2,4,10))
ball_group.add(Ball('ball4.png',50,100,1,2,4,10))

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    ball_group.update()
    ball_group.draw(screen)
    
    pygame.display.update()