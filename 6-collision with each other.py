import pygame
import sys
from math import *
import random
import math

pygame.init()
width = 660
height = 360
outerHeight = 400
margin = 30
display = pygame.display.set_mode((width, outerHeight))
pygame.display.set_caption("8 Ball Pool")
clock = pygame.time.Clock()

background = (51, 51, 51)
white = (236, 240, 241)

gray = (123, 125, 125)

black = (23, 32, 42)
colors = [black]

balls = []
noBalls = 15
radius = 10
friction = 0.005

class Ball:
    def __init__(self, x, y, colors,speed,angle):
        self.x = x + radius
        self.y = y + radius
        self.colors = colors
        self.speed = speed
        self.angle = angle
    
    def draw(self, x, y):
        pygame.draw.ellipse(display, self.colors, (x - radius, y - radius, radius*2, radius*2))

        # Moves the Ball around the Screen
    def move(self):
        self.speed -= friction
        if self.speed <= 0:
            self.speed = 0
        self.x = self.x + self.speed*cos(radians(self.angle))
        self.y = self.y + self.speed*sin(radians(self.angle))

        if not (self.x < width - radius - margin):
            self.x = width - radius - margin
            self.angle = 180 - self.angle
        if not(radius + margin < self.x):
            self.x = radius + margin
            self.angle = 180 - self.angle
        if not (self.y < height - radius - margin):
            self.y = height - radius - margin
            self.angle = 360 - self.angle
        if not(radius + margin < self.y):
            self.y = radius + margin
            self.angle = 360 - self.angle


class Pockets:
    def __init__(self, x, y, color):
        self.r = margin/2
        self.x = x + self.r + 10
        self.y = y + self.r + 10
        self.color = color

    # Draws the Pockets on Pygame Window
    def draw(self):
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))

    # Checks if ball has entered the Hole
    def checkPut(self):
        global balls
        ballsCopy = balls[:]
        for i in range(len(balls)):
            dist = ((self.x - balls[i].x)**2 + (self.y - balls[i].y)**2)**0.5
            if dist < self.r + radius:
                if balls[i] in ballsCopy:
                    # if balls[i].ballNum == 8:
                    #     pass
                    # else:
                    ballsCopy.remove(balls[i])

        balls = ballsCopy[:]

# Checks Collision
def collision(ball1, ball2):
    dist = ((ball2.x - ball1.x)**2 + (ball2.y - ball1.y)**2)**0.5

    if dist <= radius*2:
        return True
    else:
        return False

# Checks Collision Between Balls
def checkCollision():
    for i in range(len(balls)):
        for j in range(len(balls) - 1, i, -1):
            if collision(balls[i], balls[j]):
                if balls[i].x == balls[j].x:
                    pass
                else:
                    u1 = balls[i].speed
                    u2 = balls[j].speed

                    balls[i].speed = ((u1*cos(radians(balls[i].angle)))**2 + (u2*sin(radians(balls[j].angle)))**2)**0.5
                    balls[j].speed = ((u2*cos(radians(balls[j].angle)))**2 + (u1*sin(radians(balls[i].angle)))**2)**0.5

                    tangent = degrees((atan((balls[i].y - balls[j].y)/(balls[i].x - balls[j].x)))) + 90
                    angle = tangent + 90

                    balls[i].angle = (2*tangent - balls[i].angle)
                    balls[j].angle = (2*tangent - balls[j].angle)

                    balls[i].x += (balls[i].speed)*sin(radians(angle))
                    balls[i].y -= (balls[i].speed)*cos(radians(angle))
                    balls[j].x -= (balls[j].speed)*sin(radians(angle))
                    balls[j].y += (balls[j].speed)*cos(radians(angle))

noBalls = 15
balls = []
for i in range(noBalls):
    newBall = Ball(random.randrange(radius,width - radius),random.randrange(radius,height,radius),random.choice(colors),10,random.randrange(-180,180))
    balls.append(newBall)

noPockets = 6
pockets = []

p1 = Pockets(0, 0, black)
p2 = Pockets(width/2 - p1.r*2, 0, black)
p3 = Pockets(width - p1.r - margin - 5, 0, black)
p4 = Pockets(0, height - margin - 5 - p1.r, black)
p5 = Pockets(width/2 - p1.r*2, height - margin - 5 - p1.r, black)
p6 = Pockets(width - p1.r - margin - 5, height - margin - 5 - p1.r, black)

pockets.append(p1)
pockets.append(p2)
pockets.append(p3)
pockets.append(p4)
pockets.append(p5)
pockets.append(p6)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display.fill((255,255,255))

    for i in range(len(balls)):
        balls[i].draw(balls[i].x, balls[i].y)

    for i in range(len(balls)):
        balls[i].move()
    for i in range(noPockets):
        pockets[i].draw()

    for i in range(noPockets):
        pockets[i].checkPut()

    checkCollision()

    pygame.display.update()
    clock.tick(60)

