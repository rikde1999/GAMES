import pygame,random,sys
from math import *
from pygame.math import Vector2

pygame.init()

screen_width,screen_height = 300,450
screen = pygame.display.set_mode((screen_width,screen_height))

background = pygame.image.load('Assets/bg.png')
pygame.mixer.music.load('Assets/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0)

game_active = False

def reset_game(game_data,level):
    global ball_group,game_active,ball,obstacle_group

    obstacle_group = game_data[level]

    ball_group = pygame.sprite.GroupSingle()
    ball = Ball('Assets/ball.png',screen_width / 2 - 16,350,1,2)
    ball_group.add(ball)   



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
        self.arrow.add(Arrow('Assets/point.png',self.rect.centerx,self.rect.centery))
        self.strokes = 5
        self.shot = pygame.mixer.Sound("Assets/swing.mp3")
        self.par = pygame.mixer.Sound("Assets/hole.mp3")
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
            if pygame.mouse.get_pressed()[0]:
                if not self.mouse_pressed:
                    self.x_speed = (self.cursorpos[0] - self.rect.center[0]) / 20
                    self.y_speed = (self.cursorpos[1] - self.rect.center[1]) / 20
                    self.speed = sqrt(self.x_speed**2 + self.y_speed**2)
                    self.initial_x_speed = self.x_speed
                    self.initial_y_speed = self.y_speed
                    self.initial_speed = self.speed
                    self.strokes -= 1
                    self.shot.play()
                    
                self.mouse_pressed = True
                # if self.strokes == 0:
                    
                #     replay_btn.draw(screen)
                #     game_active = False
                    # pygame.quit()
                    # sys.exit()
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
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.orig_image = self.image
        self.pos = Vector2(x_pos,y_pos)

    def rotate(self, ball_rect, angle):
        direction = pygame.mouse.get_pos() - self.pos
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center = ball_rect.center)

    def update(self, ball_rect, angle):
        self.rotate(ball_rect, angle)

class ScoreManager:
    def __init__(self,ball_group,obstacle_group):
        
        self.strokes = 7
        self.ball_group = ball_group
        self.obstacle_group = obstacle_group
        
    def draw_score(self,ball):

        # if self.strokes == 0:
        #     replay_btn.draw(screen)
            # pygame.quit()

        golf_score = font.render(f'Strokes left - {ball.strokes}', True,(27,35,43))
        golf_score_rect = golf_score.get_rect(midleft = (100,20))
        
        screen.blit(golf_score,golf_score_rect)


# class PowerMeter(pygame.sprite.Sprite):
#     def __init__(self,picture_path,x_pos,y_pos,power = 100):
#         super().__init__()
#         self.power = power
#         self.image = pygame.image.load(picture_path)
#         self.rect = self.image.get_rect(center=(x_pos,y_pos))


class Button(pygame.sprite.Sprite):
    def __init__(self, img, scale, x, y):

        self.scale = scale
        self.image = pygame.transform.scale(img, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.clicked = False

    def update_image(self, img):
        self.image = pygame.transform.scale(img, self.scale)

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

            if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                action = True

        screen.blit(self.image, self.rect)
        return action


sound_off_img = pygame.image.load("Assets/soundOff.png")
sound_on_img = pygame.image.load("Assets/soundOn.png")

sound_btn = Button(sound_on_img, (36, 36), 50,100)
sound_on = True

replay_img = pygame.image.load("Assets/replay.png")
replay_btn = Button(replay_img, (36, 36), 50,100)

font = pygame.font.Font('freesansbold.ttf',16)

ball_group = pygame.sprite.Group()
ball = Ball('Assets/ball.png',screen_width /  2 - 16,350,1,2)
ball_group.add(ball)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacles('Assets/tile64_dark.png',100,200))
obstacle_group.add(Obstacles('Assets/tile64_light.png',50,50))
obstacle_group.add(Obstacles('Assets/tile32_dark.png',130,100))
obstacle_group.add(Obstacles('Assets/tile64_light.png',200,200))
obstacle_group.add(Obstacles('Assets/tile64_dark.png',160,400))
obstacle_group.add(Obstacles('Assets/tile32_dark.png',160,100))

level1 = obstacle_group

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacles('Assets/tile64_dark.png',200,100))
obstacle_group.add(Obstacles('Assets/tile64_light.png',50,50))
obstacle_group.add(Obstacles('Assets/tile32_dark.png',120,50))
obstacle_group.add(Obstacles('Assets/tile64_light.png',200,200))
obstacle_group.add(Obstacles('Assets/tile64_dark.png',160,80))
obstacle_group.add(Obstacles('Assets/tile32_dark.png',120,100))

level2 = obstacle_group

game_data = {
1:level1,
2:level2,
}

level = 1
obstacle_group = game_data[level]


hole_group = pygame.sprite.Group()
hole = Put('Assets/hole.png',screen_width / 2 - 16,60)
hole_group.add(hole)

score_manager = ScoreManager(ball_group,obstacle_group)

play_button_img = pygame.image.load("Assets/play.png")
play_btn = Button(play_button_img, (36, 36), 100,100)

# power_group = pygame.sprite.Group()
# powers = PowerMeter('Assets/powermeter_bg.png',screen_width - 26,350)

clock = pygame.time.Clock()
while True:
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if game_active:
        score_manager.draw_score(ball)
    
        ball_group.update()
        ball_group.draw(screen)
    
        obstacle_group.draw(screen)

        hole_group.draw(screen)

    else:
        
        if play_btn.draw(screen):
            game_active = True

        if sound_btn.draw(screen):
            sound_on = not sound_on

        if sound_on:
            sound_btn.update_image(sound_on_img)
            pygame.mixer.music.play(loops = -1) 

            if game_active:
                pygame.mixer.music.set_volume(0.5)           

        else:
            sound_btn.update_image(sound_off_img)	
            pygame.mixer.music.set_volume(0)	
            pygame.mixer.music.stop()

    if ball.strokes == 0:
    
        level += 1
        if level > len(game_data.keys()):
            level = len(game_data.keys())
            game_active = False

            if replay_btn.draw(screen):
                reset_game(game_data,level)


    pygame.display.update()
    clock.tick(60)