import pygame
import random
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = 1000, 1000
tile_size = 68, 33
ground_size = tile_size[0] * 11 + 34, tile_size[1] * 30 
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

start = True
def start_screen(image):
    global start, level
    fon = pygame.transform.scale(load_image(image), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    if level == 10:
        intro_text = ["ИГРА ПРОЙДЕНА !!!", "",
                  "ПОЗДРАВЛЯЮ !!!"]
        text_coord = 200
        x = 60
    else:
        intro_text = ["УРОВЕНЬ ПРОЙДЕН !!!", "",
                  "Нажмите любую кнопку,",
                  "чтобы перейти на уровень "+ str(level + 1)] 
        text_coord = 50
        x = 40
    if not start:        
        font = pygame.font.Font(None, 95)
        
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 80
            intro_rect.top = text_coord
            intro_rect.x = x
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start = False
                return
        pygame.display.flip()
        clock.tick(50)    
        
start_screen('background.jpg')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(player_group)
        self.image = pygame.transform.scale(load_image('door.png'), (tile_size[1] * 4, tile_size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - tile_size[1] * 4 // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1]
    def move_left(self):
        if self.rect.x >= 3 + 20:
            self.rect = self.rect.move(-5, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(-5, 0)
    def move_right(self):
        if self.rect.x <= ground_size[0] - 3 - tile_size[1] * 4 - 20:
            self.rect = self.rect.move(5, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(5, 0)
                    
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.add(coin_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
                    

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(ball_group)
        self.image = pygame.transform.scale(load_image('ball.png'), (tile_size[1], tile_size[1]))        
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - tile_size[1] // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1] - tile_size[1]  
        self.vx = random.choice([-4, -3, -2, 2, 3, 4])
        self.vy = random.choice([-4])
        self.stopping = True
    def get_coords(self):
        return (self.rect.x + tile_size[1] // 2, self.rect.y + tile_size[1] // 2)
    def move(self):
        global points
        if not self.stopping:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, player_group):
                for ball in ball_group:
                    ball_coords = ball.get_coords()
                for player in player_group:
                    player_coords = player.rect.x, player.rect.y
                    if ball_coords[0] >= player_coords[0] and ball_coords[0] <= player_coords[0] + tile_size[1] * 4:
                        self.vy = -self.vy
                    elif ball_coords[1] >= player_coords[1] and ball_coords[1] <= player_coords[1] + tile_size[1]:
                        self.vx = -self.vx
                    else:
                        if ball_coords[0] < player_coords[0] and ball_coords[1] < player_coords[1]:
                            len_x = - (player_coords[0] - ball_coords[0])
                            len_y = - (player_coords[1] - ball_coords[1])
                        elif ball_coords[0] > player_coords[0] + tile_size[1] * 4 and ball_coords[1] < player_coords[1]:
                            len_x = - (ball_coords[0] - player_coords[0] + tile_size[0] * 4)
                            len_y = - (player_coords[1] - ball_coords[1])
                        if len_x < len_y:
                            self.vx = -self.vx
                        elif len_x > len_y:
                            self.vy = -self.vy
                        elif len_x == len_y:
                            self.vx = -self.vx
                            self.vy = -self.vy 
            if pygame.sprite.spritecollideany(self, all_tiles):
                tiles = pygame.sprite.spritecollide(self, all_tiles, True)
                for tile in tiles:
                    points += 20
                for ball in ball_group:
                    ball_coords = ball.get_coords()
                if len(tiles) != 1:
                    for tile in tiles:
                        if ball_coords[0] >= tile.x and ball_coords[0] <= tile.x + tile_size[0]:
                            tile_coords = tile.x, tile.y
                        elif ball_coords[1] >= tile.y and ball_coords[1] <= tile.y + tile_size[1]:
                            tile_coords = tile.x, tile.y
                else:
                    tile_coords = tiles[0].x, tiles[0].y
                if ball_coords[0] >= tile_coords[0] and ball_coords[0] <= tile_coords[0] + tile_size[0]:
                    self.vy = -self.vy
                elif ball_coords[1] >= tile_coords[1] and ball_coords[1] <= tile_coords[1] + tile_size[1]:
                    self.vx = -self.vx
                else:
                    if ball_coords[0] <= tile_coords[0] and ball_coords[1] <= tile_coords[1]:
                        len_x = - (tile_coords[0] - ball_coords[0])
                        len_y = - (tile_coords[1] - ball_coords[1])
                    elif ball_coords[0] >= tile_coords[0] + tile_size[0] and ball_coords[1] <= tile_coords[1]:
                        len_x = - (ball_coords[0] - tile_coords[0] - tile_size[0])
                        len_y = - (tile_coords[1] - ball_coords[1])
                    elif ball_coords[0] <= tile_coords[0] and ball_coords[1] >= tile_coords[1] + tile_size[1]:
                        len_x = - (tile_coords[0] - ball_coords[0])
                        len_y = - (ball_coords[1] - tile_coords[1] - tile_size[1])
                    elif ball_coords[0] >= tile_coords[0] + tile_size[0] and ball_coords[1] >= tile_coords[1] + tile_size[1]:
                        len_x = - (ball_coords[0] - tile_coords[0] - tile_size[0])
                        len_y = - (ball_coords[1] - tile_coords[1] - tile_size[1])
                    if len_x < len_y:
                        self.vx = -self.vx
                    elif len_x > len_y:
                        self.vy = -self.vy
                    elif len_x == len_y:
                        self.vx = -self.vx
                        self.vy = -self.vy
                        

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

tile_images = {
    'blue': load_image('blue.png'),
    'green': load_image('green.png'),
    'red': load_image('red.png'),
    'yellow': load_image('yellow.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(all_tiles)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_size[0], tile_size[1]))
        self.x = 20 + tile_size[0] * pos_x - 3
        self.y = 20 + tile_size[1] * pos_y        
        self.rect = self.image.get_rect().move(self.x, self.y)
        
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
            else:
                pass

fon = pygame.transform.scale(load_image('fon.png'), (size[0], size[1]))
level = 0
speed = 1
pauze = False
game_over = False
points = 0
start_seconds = pygame.time.get_ticks()
while True:
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()  
    ball_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group() 
    all_tiles = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
        
    Border(10, 10, 10, ground_size[1] - 10)
    Border(ground_size[0] - 10, 10, ground_size[0] - 10, ground_size[1] - 10)
    Border(10, 10, ground_size[0] - 10, 10)    
    Player()  
    Ball()
    AnimatedSprite(load_image("money.png"), 16, 1, size[0] - 200, 50)
    
    level += 1
    speed += 1
    first = True
    for ball in ball_group:
        ball.vy -= speed // 2
    generate_level(load_level('level' + str(level) + '.txt'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if first:
                        first = False
                        for ball in ball_group:
                            ball.stopping = False
                    else:
                        if not pauze:
                            pauze = True
                        else:
                            pauze = False
        if not pauze:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                for player in player_group:
                    player.move_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                for player in player_group:
                    player.move_right()
            for ball in ball_group:
                ball.move()
                if ball.rect.y >= size[1]:
                    game_over = True
            screen.blit(fon, (0, 0))
        else:
            pauze = pygame.sprite.Group()
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(load_image('pauze.png'), (200, 200))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = ground_size[0] // 2 + 20
            sprite.rect.y = ground_size[1] // 2 + 20
            sprite.add(pauze)
            pauze.draw(screen)
        for coin in coin_group:
            coin.update()
        seconds_in_game = (pygame.time.get_ticks() - start_seconds) // 1000
        screen.blit(pygame.font.Font(None, 50).render(str(points) , 1, (255, 255, 255)), (size[0] - 170, 50))
        screen.blit(pygame.font.Font(None, 50).render("TIME {}".format(str(seconds_in_game)), 1, (255, 255, 255)), (size[0] - 200, 200))
        screen.blit(pygame.font.Font(None, 50).render("LEVEL {}".format(str(level)) , 1, (255, 255, 255)), (size[0] - 200, 450))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(100)
        if len(all_tiles) == 0 or game_over:
            break
    if game_over:
        break
    pygame.time.wait(1000)
    if level != 10:
        start_screen('fon.png')
    elif level == 10:
        start_screen("background.jpg")
        break
    
gameover = pygame.sprite.Group()
class GameOver(pygame.sprite.Sprite): 
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('gameover.png'), (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = 0
    def get_coords(self):
        return (self.rect.x, self.rect.y)
    def move_right(self):
        self.rect.x += 5
GameOver(gameover)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for table in gameover:
        if table.get_coords()[0] < 0:
            table.move_right()
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    gameover.draw(screen)
    pygame.display.flip()
    clock.tick(140)
pygame.quit()