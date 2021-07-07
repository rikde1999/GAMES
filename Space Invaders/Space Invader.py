import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_width))

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5 

        self.rect.x += self.speedx

        if self.rect.right > screen_width:
            self.rect.right = screen_width
        
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100,-20)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-2,3)
    
    def update(Self):
        Self.rect.x += Self.speedx
        Self.rect.y += Self.speedy
        if Self.rect.top > screen_height + 10 or Self.rect.left < -25 or Self.rect.right > screen_width + 20:
            Self.rect.x = random.randrange(screen_width - Self.rect.width)
            Self.rect.y = random.randrange(-100,-40)
            Self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#loading the game graphics
background = pygame.image.load(path.join(img_dir,"purple.png")).convert()
background_Rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"player.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"laser.png")).convert()

meteor_images = []
meteor_list = ['meteor.png','m3.png','m4.png','meteor2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
player = Player()
all_sprites.add(player)

running = True
while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    all_sprites.update()

    #check if the bullet collides with the mobs

    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #collsion with the player with the mobs
    hits = pygame.sprite.spritecollide(player,mobs,False,pygame.sprite.collide_circle)
    if hits:
        running = False
    
    # Draw / render
    # screen.fill(black)
    screen.blit(background,background_Rect)
    all_sprites.draw(screen)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
