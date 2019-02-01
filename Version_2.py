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
#pygame.mouse.set_visible(0)
level = 0
cheat = False
board_size = (tile_size[1] * 4, tile_size[1])

playlist = ["data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3", "data\Polka.mp3",
            "data\Trr_cha.mp3"]

pygame.mixer.music.load("data\Polka.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.set_endevent(pygame.USEREVENT)

sound1 = pygame.mixer.Sound('data/ball.ogg')
sound2 = pygame.mixer.Sound('data/tile.ogg')
sound3 = pygame.mixer.Sound('data/fail.ogg')
sound4 = pygame.mixer.Sound('data/queen.ogg')

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
    global start, level, points
    fon = pygame.transform.scale(load_image(image), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    if level == 10:
        pygame.mixer.music.pause()
        sound4.play()
        intro_text = ["GAME COMPLETED!!!", "Total points:  " + str(points)]
        text_coord = 670
        x = 200
        color = pygame.Color('white')
        
        font = pygame.font.SysFont('Times New Roman', 75)
        for line in intro_text:
            string_rendered = font.render(line, 1, color)
            intro_rect = string_rendered.get_rect()
            text_coord += 60
            intro_rect.top = text_coord
            intro_rect.x = x
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()
            clock.tick(50)
        
    else:
        intro_text = ["LEVEL COMPLETED !!!", "",
                  "Press any key, to go to level "+ str(level + 1)] 
        text_coord = 50
        x = 35
        color = pygame.Color('green')
        if not start:        
            font = pygame.font.SysFont('Arial', 85)
        
            for line in intro_text:
                string_rendered = font.render(line, 1, color)
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
        self.image = pygame.transform.scale(load_image('door.png'), (board_size[0], board_size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - board_size[0] // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1]
    def move_left(self):
        if self.rect.x >= 3 + 20:
            self.rect = self.rect.move(-5, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(-5, 0)
    def move_right(self):
        if self.rect.x <= ground_size[0] - 3 - board_size[0] - 20:
            self.rect = self.rect.move(5, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(5, 0)
    def target(self, target):
        now = self.rect.x + tile_size[1] * 2
        end = target
        if target <= ground_size[0] - 23 - tile_size[1] * 2 and target >= 23 + tile_size[1] * 2:
            self.rect = self.rect.move(end - now, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(end - now, 0)
                    
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
        
class Cheat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('roma.png'), (size[0] - ground_size[0], size[1] // 2))  
        self.rect = self.image.get_rect()
        self.rect.x = ground_size[0]
        self.rect.y = size[1] // 2
        

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
            if pygame.sprite.spritecollideany(self, horizontal_borders) or pygame.sprite.spritecollideany(self, vertical_borders) or pygame.sprite.spritecollideany(self, player_group):
                sound1.play()
            if pygame.sprite.spritecollideany(self, all_tiles):
                sound2.play()
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, player_group):
                for ball in ball_group:
                    ball_coords = ball.get_coords()
                for player in player_group:
                    player_coords = player.rect.x, player.rect.y
                    if ball_coords[0] >= player_coords[0] - 20 and ball_coords[0] <= player_coords[0] + tile_size[1] * 4 + 20:
                        self.vy = -self.vy
                    elif ball_coords[1] >= player_coords[1] and ball_coords[1] <= player_coords[1] + tile_size[1]:
                        self.vx = -self.vx
                    else:
                        otraz = False
                        if ball_coords[0] < player_coords[0] and ball_coords[1] < player_coords[1]:
                            for i in range(20):
                                if not otraz:
                                    ball_co = (ball_coords[0] + i, ball_coords[1] + i)
                                    if ball_co[0] > player_coords[0]:
                                        len_x, len_y = 2, 1
                                        otraz = True
                                    elif ball_co[1] > player_coords[1]:
                                        len_x, len_y = 1, 2
                                        otraz = True
                        elif ball_coords[0] > player_coords[0] + board_size[0] and ball_coords[1] < player_coords[1]:
                            for i in range(20):
                                if not otraz:
                                    ball_co = (ball_coords[0] - i, ball_coords[1] + i)
                                    if ball_co[0] < player_coords[0] + board_size[0]:
                                        len_x, len_y = 2, 1
                                        otraz = True
                                    elif ball_co[1] > player_coords[1]:
                                        len_x, len_y = 1, 2
                                        otraz = True
                        elif ball_coords[0] <= player_coords[0] and ball_coords[1] >= player_coords[1] + tile_size[1]:
                            for i in range(20):
                                if not otraz:
                                    ball_co = (ball_coords[0] + i, ball_coords[1] - i)
                                    if ball_co[0] > player_coords[0]:
                                        len_x, len_y = 2, 1
                                        otraz = True
                                    elif ball_co[1] < player_coords[1] + tile_size[1]:
                                        len_x, len_y = 1, 2
                                        otraz = True
                        elif ball_coords[0] >= player_coords[0] + tile_size[0] and ball_coords[1] >= player_coords[1] + tile_size[1]:
                            for i in range(20):
                                if not otraz:
                                    ball_co = (ball_coords[0] - i, ball_coords[1] + i)
                                    if ball_co[0] < player_coords[0] + board_size[0]:
                                        len_x, len_y = 2, 1
                                        otraz = True
                                    elif ball_co[1] < player_coords[1] + tile_size[1]:
                                        len_x, len_y = 1, 2
                                        otraz = True
                        if len_x < len_y:
                            self.vx = -self.vx
                        elif len_x > len_y:
                            self.vy = -self.vy
                        elif len_x == len_y:
                            self.vx = -self.vx
                            self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, all_tiles):
                tiles_black = pygame.sprite.spritecollide(self, black_tiles, False)
                tiles = pygame.sprite.spritecollide(self, all_tiles, True)
                for tile in tiles:
                    points += 20
                    create_particles((tile.rect.x + tile_size[0] // 2, tile.rect.y + tile_size[1] // 2))
                for ball in ball_group:
                    ball_coords = ball.get_coords()
                for tile in tiles_black:
                    tile.get_hit()
                tile_coords = 0
                if len(tiles) != 1:
                    for tile in tiles:
                        if ball_coords[0] >= tile.x and ball_coords[0] <= tile.x + tile_size[0]:
                            tile_coords = tile.x, tile.y
                        elif ball_coords[1] >= tile.y and ball_coords[1] <= tile.y + tile_size[1]:
                            tile_coords = tile.x, tile.y
                    if tile_coords == 0:
                        tile = random.choice(tiles)
                        tile_coords = tile.x, tile.y
                else:
                    tile_coords = tiles[0].x, tiles[0].y
                if ball_coords[0] >= tile_coords[0] and ball_coords[0] <= tile_coords[0] + tile_size[0]: 
                    self.vy = -self.vy
                elif ball_coords[1] >= tile_coords[1] and ball_coords[1] <= tile_coords[1] + tile_size[1]:
                    self.vx = -self.vx
                else:
                    otraz = False
                    if ball_coords[0] <= tile_coords[0] and ball_coords[1] <= tile_coords[1]:
                        for i in range(20):
                            if not otraz:
                                ball_co = (ball_coords[0] + i, ball_coords[1] + i)
                                if ball_co[0] > tile_coords[0]:
                                    len_x, len_y = 2, 1
                                    otraz = True
                                elif ball_co[1] > tile_coords[1]:
                                    len_x, len_y = 1, 2
                                    otraz = True
                    elif ball_coords[0] >= tile_coords[0] + tile_size[0] and ball_coords[1] <= tile_coords[1]:
                        for i in range(20):
                            if not otraz:
                                ball_co = (ball_coords[0] - i, ball_coords[1] + i)
                                if ball_co[0] < tile_coords[0] + tile_size[0]:
                                    len_x, len_y = 2, 1
                                    otraz = True
                                elif ball_co[1] > tile_coords[1]:
                                    len_x, len_y = 1, 2
                                    otraz = True
                    elif ball_coords[0] <= tile_coords[0] and ball_coords[1] >= tile_coords[1] + tile_size[1]:
                        for i in range(20):
                            if not otraz:
                                ball_co = (ball_coords[0] + i, ball_coords[1] - i)
                                if ball_co[0] > tile_coords[0]:
                                    len_x, len_y = 2, 1
                                    otraz = True
                                elif ball_co[1] < tile_coords[1] + tile_size[1]:
                                    len_x, len_y = 1, 2
                                    otraz = True
                    elif ball_coords[0] >= tile_coords[0] + tile_size[0] and ball_coords[1] >= tile_coords[1] + tile_size[1]:
                        for i in range(20):
                            if not otraz:
                                ball_co = (ball_coords[0] - i, ball_coords[1] - i)
                                if ball_co[0] < tile_coords[0] + tile_size[0]:
                                    len_x, len_y = 2, 1
                                    otraz = True
                                elif ball_co[1] < tile_coords[1] + tile_size[1]:
                                    len_x, len_y = 1, 2
                                    otraz = True
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
            
gravity = 0.25     
screen_rect = (10, 10, ground_size[0], ground_size[1])       
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.transform.scale(load_image('gold.png'), (10, 10))]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.add(all_particles)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

tile_images = {
    'blue': load_image('blue.png'),
    'green': load_image('green.png'),
    'red': load_image('red.png'),
    'yellow': load_image('yellow.png'),
    'black': load_image('black.png'),
    'black_hit': load_image('black_hit.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        if tile_type == 'black':
            self.add(black_tiles)
        self.add(all_tiles)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_size[0], tile_size[1]))
        self.x = 20 + tile_size[0] * pos_x - 3
        self.y = 20 + tile_size[1] * pos_y     
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(self.x, self.y)
    def get_hit(self):
        Tile('black_hit', self.pos_x, self.pos_y)
        
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
            elif level[y][x] == 'x':
                Tile('black', x, y)
            else:
                pass

main_game = True
main_menu_sprites = pygame.sprite.Group()
shop_sprites = pygame.sprite.Group()
rules_sprites = pygame.sprite.Group()

class Button(pygame.sprite.Sprite): 
    def __init__(self, group, name, x, y, focused):
        super().__init__(group)
        self.image = pygame.Surface((300, 100))
        self.image.fill((0, 0, 230))
        self.image.blit(pygame.font.Font(None, 35).render(str(name) , 1, (255, 255, 255)), (10, 25))
        self.rect = pygame.Rect(x, y, 500, 200)
        self.rect.x = x
        self.start_x = x
        self.rect.y = y
        self.start_y = y 
        self.name = name
        self.focused = focused
    def update(self):
        try:
            if main_menu_buttons[self.name]:
                self.rect = pygame.Rect(self.start_x + 10, self.start_y, 500, 200)
            else:
                self.rect = pygame.Rect(self.start_x, self.start_y, 500, 200)
        except:
            if shop_buttons[self.name]:
                self.rect = pygame.Rect(self.start_x + 10, self.start_y, 500, 200)
            else:
                self.rect = pygame.Rect(self.start_x, self.start_y, 500, 200)
        

bas_lives = 3
total_points = 0
upgrade_kolvo = 1
level = 0
main_menu_buttons = {
        'Play' : False,
        'Shop' : False,
        'Quit' : False
        }
shop_buttons = {
        'Buy live (cost 10000)' : False,
        'Main menu' : False,
        'Upgrade (cost 25000)' : False
        }
while main_game:
    pygame.mixer.music.unpause()
    y_start = 500
    for i in range(3):
        if i == 0:
            name = "Play"
        if i == 1:
            name = "Shop"
        if i == 2:
            name = "Quit"
        Button(main_menu_sprites, name, size[0] // 2 - 150, y_start, main_menu_buttons[name])
        y_start += 120
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            main_game = False
        if event.type == pygame.MOUSEMOTION:
            for button in main_menu_sprites:
                if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                    if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                        main_menu_buttons[button.name] = True
                    elif event.pos[1] < button.rect.y or event.pos[1] > button.rect.y + 100:
                        main_menu_buttons[button.name] = False
                elif event.pos[0] < button.rect.x or event.pos[0] > button.rect.x + 300:
                    main_menu_buttons[button.name] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in main_menu_sprites:
                if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                    if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                        if button.name == "Play":
                            start_seconds = pygame.time.get_ticks()
                            level = 0
                            points = 0
                            while True:
                                pygame.mixer.music.unpause()
                                fon = pygame.transform.scale(load_image('fon.png'), (size[0], size[1]))
                                speed = 1
                                pauze = False
                                game_over = False

                                all_sprites = pygame.sprite.Group()
                                horizontal_borders = pygame.sprite.Group()
                                vertical_borders = pygame.sprite.Group()  
                                ball_group = pygame.sprite.Group()
                                player_group = pygame.sprite.Group() 
                                all_tiles = pygame.sprite.Group()
                                black_tiles = pygame.sprite.Group()
                                coin_group = pygame.sprite.Group()
                                all_particles = pygame.sprite.Group()
        
                                Border(10, 10, 10, ground_size[1] - 10)
                                Border(ground_size[0] - 10, 10, ground_size[0] - 10, ground_size[1] - 10)
                                Border(10, 10, ground_size[0] - 10, 10) 
                                if cheat:
                                    Cheat()
                                Player()  
                                Ball()
                                AnimatedSprite(load_image("money.png"), 16, 1, size[0] - 200, 50)
    
                                pygame.mixer.music.set_volume(0.5)
    
                                level += 1
                                speed += 1
                                first = True
                                lives = bas_lives 
                                for ball in ball_group:
                                    ball.vy -= speed // 2
                                generate_level(load_level('level' + str(level) + '.txt'))
                                while True:
                                    mouse_moving = False
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            terminate()
                                            pygame.quit()
                                        if event.type == pygame.USEREVENT: 
                                            if len ( playlist ) > 0:
                                                pygame.mixer.music.pop()
                                                pygame.mixer.music.load(playlist[-1])
                                                playlist.pop()
                                                pygame.mixer.music.play()
                                        if event.type == pygame.MOUSEMOTION:
                                            mouse_moving = True
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            if event.button == 1:
                                                first = False
                                                for ball in ball_group:
                                                    ball.stopping = False
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_z:
                                                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                                    cheat = True
                                                    Cheat()
                                            if event.key == pygame.K_UP:
                                                for ball in ball_group:
                                                    ball.vy -= 1
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
                                        pygame.mixer.music.set_volume(0.5)
                                        if mouse_moving and cheat:
                                            for player in player_group:
                                                x = event.pos[0]
                                                player.target(x)
                                        if pygame.key.get_pressed()[pygame.K_LEFT]:
                                            for player in player_group:
                                                player.move_left()
                                        if pygame.key.get_pressed()[pygame.K_RIGHT]:
                                            for player in player_group:
                                                player.move_right()
                                        for ball in ball_group:
                                            ball.move()
                                            if ball.rect.y >= size[1]:
                                                lives -= 1
                                                if lives >= 1:
                                                    for player in player_group:
                                                        all_sprites.remove(player)
                                                    first = True
                                                    ball_group = pygame.sprite.Group()
                                                    player_group = pygame.sprite.Group()
                                                    Player()
                                                    Ball()
                                                else:
                                                    game_over = True
                                        for particle in all_particles:
                                            particle.update()
                                        screen.blit(fon, (0, 0))
                                        seconds_in_game = (pygame.time.get_ticks() - start_seconds) // 1000
                                        screen.blit(pygame.font.Font(None, 50).render("TIME {}".format(str(seconds_in_game)), 1, (255, 255, 255)), (size[0] - 200, 200))
                                    else:
                                        pygame.mixer.music.set_volume(0.25)
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
                                    screen.blit(pygame.font.Font(None, 50).render(str(points) , 1, (255, 255, 255)), (size[0] - 170, 50))
                                    screen.blit(pygame.font.Font(None, 50).render("LIVES x {}".format(str(lives)), 1, (255, 255, 255)), (size[0] - 200, 325))
                                    screen.blit(pygame.font.Font(None, 50).render("LEVEL {}".format(str(level)) , 1, (255, 255, 255)), (size[0] - 200, 450))
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(100)
                                    if len(all_tiles) == 0 or game_over:
                                        break
                                if game_over:
                                    break
                                pygame.time.wait(500)
                                if level != 10:
                                    start_screen('fon.png')
                                elif level == 10:
                                    start_screen("gameend.jpg")
                                    break
                            if game_over:  
                                gameover = pygame.sprite.Group()
                                pygame.mixer.music.pause()
                                class GameOver(pygame.sprite.Sprite): 
                                    def __init__(self, group):
                                        super().__init__(group)
                                        self.image = pygame.transform.scale(load_image('gameover.jpg'), (ground_size[0], size[1]))
                                        self.rect = self.image.get_rect()
                                        self.rect.x = -1000
                                        self.rect.y = 0
                                    def get_coords(self):
                                        return (self.rect.x, self.rect.y)
                                    def move_right(self):
                                        self.rect.x += 5
                                GameOver(gameover)
                                running = True
                                sound3.play()
                                while running:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                    for table in gameover:
                                        if table.get_coords()[0] < 0:
                                            table.move_right()
                                        else:
                                            pygame.time.wait(5000)
                                            running = False
                                    screen.blit(fon, (0, 0))
                                    screen.blit(pygame.font.Font(None, 50).render(str(points) , 1, (255, 255, 255)), (size[0] - 170, 50))
                                    screen.blit(pygame.font.Font(None, 50).render("TIME {}".format(str(seconds_in_game)), 1, (255, 255, 255)), (size[0] - 200, 200))
                                    screen.blit(pygame.font.Font(None, 50).render("LIVES x {}".format(str(lives)), 1, (255, 255, 255)), (size[0] - 200, 325))
                                    screen.blit(pygame.font.Font(None, 50).render("LEVEL {}".format(str(level)) , 1, (255, 255, 255)), (size[0] - 200, 450))
                                    all_sprites.draw(screen)
                                    gameover.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(140)
                                total_points += points
                                break
                            total_points += points
                        if button.name == "Shop":
                            shopping = True
                            while shopping:
                                second = True
                                Button(shop_sprites, 'Buy live (cost 10000)', 300, 100, shop_buttons['Buy live (cost 10000)'])
                                Button(shop_sprites, 'Main menu', 50, size[1] - 150, shop_buttons['Main menu'])
                                Button(shop_sprites, 'Upgrade (cost 25000)', 300, 230, shop_buttons['Upgrade (cost 25000)'])
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        terminate()
                                        pygame.quit()
                                    if event.type == pygame.MOUSEMOTION:
                                        for button in shop_sprites:
                                            if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                                                if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                                                    shop_buttons[button.name] = True
                                                elif event.pos[1] < button.rect.y or event.pos[1] > button.rect.y + 100:
                                                    shop_buttons[button.name] = False
                                            elif event.pos[0] < button.rect.x or event.pos[0] > button.rect.x + 300:
                                                shop_buttons[button.name] = False
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        for button in shop_sprites:
                                            if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                                                if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                                                    if button.name == 'Buy live (cost 10000)' and second:
                                                        if total_points >= 10000:
                                                            total_points -= 10000
                                                            bas_lives += 1
                                                            second = False
                                                    elif button.name == 'Upgrade (cost 25000)':
                                                        if total_points >= 25000 and upgrade_kolvo <= 3 and second:
                                                            total_points -= 25000
                                                            board_size = (board_size[0] + tile_size[1] // 2, board_size[1])
                                                            upgrade_kolvo += 1
                                                            second = False
                                                    elif button.name == 'Main menu':
                                                        shopping = False
                                for button in shop_sprites:
                                    button.update()
                                screen.blit(pygame.transform.scale(load_image('fon.png'), (size[0], size[1])), (0, 0))
                                screen.blit(pygame.transform.scale(load_image('door.png'), (board_size[0], board_size[1])), (50, 250))
                                screen.blit(pygame.font.Font(None, 50).render("LIVES x {}".format(str(bas_lives)), 1, (255, 255, 255)), (50, 127))
                                screen.blit(pygame.font.Font(None, 50).render("TOTAL POINTS:  {}".format(str(total_points)), 1, (255, 255, 255)), (100, 50))
                                shop_sprites.draw(screen)
                                pygame.display.flip()
                                clock.tick(140)   
                        if button.name == "Quit":
                            terminate()
                            pygame.quit()        
    screen.blit(pygame.transform.scale(load_image('fon.png'), (size[0], size[1])), (0, 0))
    text = ["Правила игры:",
            "Цель игры заключается в том, чтобы сломать все",
            "кирпичики на всех уровнях",
            "Управление:",
            "Стрелочки '<-' и '->' перемещение отбивающей пластины",
            "Пробел или ЛКМ для отпускания мячика"]
    y = 50
    for line in range(len(text)):
        if line == 0 or line == 3:
            screen.blit(pygame.font.Font(None, 80).render((str(text[line])), 1, (255, 255, 255)), (15, y))
            y += 75
        else:
            screen.blit(pygame.font.Font(None, 50).render((str(text[line])), 1, (255, 255, 255)), (15, y))
            y += 50
    for button in main_menu_sprites:
        button.update()
    main_menu_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(140)    
pygame.quit()