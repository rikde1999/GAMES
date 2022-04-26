# import pygame

# pygame.init()
# screen = pygame.display.set_mode((500, 500))

# x = 250
# y = 250
# radius = 15
# velocity_x = 10
# velocity_y = 10
# jump = False

# run = True
# while run:
#     screen.fill((0, 0, 0))
#     pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     # Movement
#     userInput = pygame.key.get_pressed()
#     if userInput[pygame.K_LEFT] and x > 0:
#         x -= velocity_x
#     if userInput[pygame.K_RIGHT] and x < 500:
#         x += velocity_x

#     #Jump
#     if jump is False and userInput[pygame.K_SPACE]:
#         jump = True
#     if jump is True:
#         y -= velocity_y*4
#         velocity_y -= 1
#         if velocity_y < -10:
#             jump = False
#             velocity_y = 10

#     pygame.time.delay(20)
#     pygame.display.update()



import pygame,sys

pygame.init()

screen_width,screen_height = 500,500
screen = pygame.display.set_mode((screen_width,screen_height))

acceleration = .5

class Ball:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.velocity = 10
        self.jump = False

    def draw(self):
        pygame.draw.circle(screen,(255,0,0),(250,self.y - 30),15)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.jump == False and keys[pygame.K_SPACE]:
            self.jump = True

        if self.jump is True:
            self.velocity += acceleration
            self.y += self.velocity

            if self.y >= 505:
                self.jump = False
                self.velocity = -self.velocity

ball = Ball()

clock = pygame.time.Clock()
while True:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.line(screen,(0,0,0),(0,500),(500,500),22)
    #drawing the ball
    ball.draw()
    ball.move()

    pygame.display.update()
    clock.tick(60)
