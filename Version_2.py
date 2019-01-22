import pygame
import random
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = 800, 800
ground = 400, 800
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen(image): 
    fon = pygame.transform.scale(load_image(image), (size[0], size[1]))
    screen.blit(fon, (0, 0))
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)    
        
start_screen('background.png')

balls = pygame.sprite.Group()
class Ball(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(all_sprites)
        self.add(balls)
        self.image = pygame.transform.scale(load_image('ball.png'), (30, 30))        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25, ground[0] - 30)
        self.rect.y = 15
        self.vx = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        self.vy = random.choice([5])
    def move(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()        
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

Border(5, 5, ground[0] - 5, 5)
Border(5, ground[1] - 5, ground[0] - 5, ground[1] - 5)
Border(5, 5, 5, ground[1] - 5)
Border(ground[0] - 5, 5, ground[0] - 5, ground[1] - 5)

new_ball = 0
fon = pygame.transform.scale(load_image('gameground.jpg'), (size[0], size[1]))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    new_ball += 1
    if new_ball == 250:
        new_ball = 0
        Ball(balls)
    for ball in balls:
        ball.move()
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(140)
    pygame.time.wait(10)
    