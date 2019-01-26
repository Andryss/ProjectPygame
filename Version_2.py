import pygame
import random
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = 1000, 1000
tile_size = 68, 33
ground_size = tile_size[0] * 11, tile_size[1] * 30 
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
        
start_screen('background.jpg')

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()  
ball_group = pygame.sprite.Group()
player_group = pygame.sprite.Group() 
all_tiles = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(player_group)
        self.image = pygame.transform.scale(load_image('door.png'), (tile_size[1] * 4, 33))
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - tile_size[1] * 4 // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1]
    def move_left(self):
        self.rect = self.rect.move(-3, 0)
        for ball in ball_group:
            if ball.stopping:
                ball.rect = ball.rect.move(-3, 0)
    def move_right(self):
        self.rect = self.rect.move(3, 0)
        for ball in ball_group:
            if ball.stopping:
                ball.rect = ball.rect.move(3, 0)
        
Player()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(ball_group)
        self.image = pygame.transform.scale(load_image('ball.png'), (tile_size[1], tile_size[1]))        
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - tile_size[1] // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1] - tile_size[1]  
        self.vx = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        self.vy = random.choice([-5])
        self.stopping = True
    def move(self):
        if not self.stopping:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders) or pygame.sprite.spritecollideany(self, player_group):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
  
Ball()

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.transform.scale(load_image('left.png'), (10, ground_size[1])) 
            self.rect = self.image.get_rect().move(x1 - 5, y1 - 5)
        else:
            self.add(horizontal_borders)
            self.image = pygame.transform.scale(load_image('top.png'), (ground_size[0] - 10, 10))
            self.rect = self.image.get_rect().move(x1 - 5, y1 - 5)

Border(10, 10, 10, ground_size[1] - 10)
Border(ground_size[0] - 10, 10, ground_size[0] - 10, ground_size[1] - 10)
Border(10, 10, ground_size[0] - 10, 10)

tile_images = {
    'blue': load_image('blue.png'),
    'green': load_image('green.png'),
    'red': load_image('red.png'),
    'yellow': load_image('yellow.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_tiles, all_sprites)
        self.image = tile_images[tile_type]
        x = 20 + tile_size[0] * pos_x
        y = 20 + tile_size[1] * pos_y
        self.rect = self.image.get_rect().move(x, y)
        
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map)) 
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'b':
                Tile('blue', x, y)
            elif level[y][x] == 'g':
                Tile('green', x, y)
            elif level[y][x] == 'r':
                Tile('red', x, y)
            elif level[y][x] == 'y':
                Tile('yellow', x, y)

fon = pygame.transform.scale(load_image('fon.png'), (size[0], size[1]))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for ball in ball_group:
                    ball.stopping = False
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        for player in player_group:
            player.move_left()
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        for player in player_group:
            player.move_right()
    screen.blit(fon, (0, 0))
    for ball in ball_group:
        ball.move()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(140)