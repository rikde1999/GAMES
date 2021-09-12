import pygame
from settings import screen_width,screen_height
from obstacle import *
from ball import *

pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.sound()

    ball_group.update()
    ball_group.draw(screen)
    
    obstacle_group.draw(screen)

    hole_group.draw(screen)
        
    pygame.display.update()
    clock.tick(60)