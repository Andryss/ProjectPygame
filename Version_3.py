import pygame
import random
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = 1000, 1000
tile_size = 68, 33
ground_size = [tile_size[0] * 11 + 34, tile_size[1] * 30]
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
level = 0
frames = 0
cheat = False
music = True
sound = True
playlist = ["data\music_1.mp3", "data\music_2.mp3",
            "data\music_3.mp3", "data\music_4.mp3"]

kolvo_tiles_per_level = []
for i in range(10):
    filename = "data/level{}.txt".format(i+1)
    k = 0
    with open(filename, 'r') as Mapfile:
        level_map = [line.strip() for line in Mapfile]
        max_width = max(map(len, level_map))
        file = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        for stroka in file:
            for word in stroka:
                if word != ".":
                    k += 1
        kolvo_tiles_per_level.append(k)

pygame.mixer.music.load("data\music_2.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.set_endevent(pygame.USEREVENT)

sound1 = pygame.mixer.Sound('data/ball.ogg')
sound2 = pygame.mixer.Sound('data/tile.ogg')
sound3 = pygame.mixer.Sound('data/fail.ogg')
sound4 = pygame.mixer.Sound('data/queen.ogg')
sound5 = pygame.mixer.Sound('data/saving.ogg')
sound_click = pygame.mixer.Sound('data/click.ogg')
sound_shoot = pygame.mixer.Sound('data/shoot.ogg')

def load_image(name, colorkey=None):
    fullname = os.path.join('data/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def terminate():
    pygame.quit()
    sys.exit()

mouse_down = False
Cursor = pygame.transform.scale(load_image('Cursor_normal.png'), (100, 100))
Cursor_Clicked = pygame.transform.scale(load_image('Cursor_Clicked.png'), (100, 100))

def draw_cursor(screen,x,y):
    if mouse_down:
        screen.blit(Cursor_Clicked,(x - 20,y - 18))
    else:
        screen.blit(Cursor,(x - 20,y - 18))

start = True
def start_screen(image):
    global start, level, points, total_points
    fon = pygame.transform.scale(load_image(image), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    if level == 10:
        fon = pygame.transform.scale(load_image(image), (size[0] + 55, size[1] + 50))
        pygame.mixer.music.pause()
        sound4.play()
        intro_text = ["GAME COMPLETED!!!", "Total points:  " + str(points)]
        color = pygame.Color('white')
        font = pygame.font.SysFont('Times New Roman', 75)
        while True:
            screen.blit(pygame.transform.scale(load_image('fon.png'), (size[0], size[1])), (0, 0))
            screen.blit(fon, (-15, -10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                    pygame.mixer.music.unpause()
                    sound4.stop()
                    total_points += points
                    return
                if event.type == pygame.USEREVENT:
                    music_change()

            text_coord = 670
            x = 150

            for line in intro_text:
                string_rendered = font.render(line, 1, color)
                intro_rect = string_rendered.get_rect()
                text_coord += 60
                intro_rect.top = text_coord
                intro_rect.x = x
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            draw_cursor(screen, x, y)

            pygame.display.flip()
            clock.tick(50)
        
    else:
        while True:
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                    start = False
                    return
                if event.type == pygame.USEREVENT:
                    music_change()
                elif event.type == pygame.KEYDOWN :
                    start = False
                    return

            if not start:
                intro_text = ["LEVEL COMPLETED !!!", "",
                              "Press any key, to go to level " + str(level + 1)]
                text_coord = 50
                x = 35
                color = pygame.Color('green')

                font = pygame.font.SysFont('Arial', 85)

                for line in intro_text:
                    string_rendered = font.render(line, 1, color)
                    intro_rect = string_rendered.get_rect()
                    text_coord += 80
                    intro_rect.top = text_coord
                    intro_rect.x = x
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)

            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            draw_cursor(screen, x, y)

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
    def get_coords(self):
        return (self.rect.x + board_size[0] // 2, self.rect.y + board_size[1] // 2)
    def move_left(self):
        if self.rect.x >= 3 + 20:
            self.rect = self.rect.move(-6, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(-6, 0)
    def move_right(self):
        if self.rect.x <= ground_size[0] - 3 - board_size[0] - 20:
            self.rect = self.rect.move(6, 0)
            for ball in ball_group:
                if ball.stopping:
                    ball.rect = ball.rect.move(6, 0)
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
        
class Image(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('gold.png'), (width, height))
        self.rect = self.image.get_rect().move(x, y)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(ball_group)
        self.image = pygame.transform.scale(load_image('ball.png'), (tile_size[1], tile_size[1]))        
        self.rect = self.image.get_rect()
        self.rect.x = 10 + ground_size[0] // 2 - tile_size[1] // 2
        self.rect.y = 10 + ground_size[1] - 15 - 2 * tile_size[1] - tile_size[1]  
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-5])
        self.stopping = True
    def get_coords(self):
        return (self.rect.x + tile_size[1] // 2, self.rect.y + tile_size[1] // 2)
    def move(self):
        global points
        if not self.stopping:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders) or pygame.sprite.spritecollideany(self, vertical_borders) or pygame.sprite.spritecollideany(self, player_group):
                if sound:
                    sound1.play()
            if pygame.sprite.spritecollideany(self, all_tiles):
                if sound:
                    sound2.play()
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                for ball in ball_group:
                    coords = ball.get_coords()
                if coords[0] > ground_size[0] // 2:
                    if self.vx > 0:
                        self.vx = -self.vx
                elif coords[0] < ground_size[0] // 2:
                    if self.vx < 0:
                        self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, player_group):
                for player in player_group:
                    player_coords = player.get_coords()
                ball_coords = self.get_coords()
                if ball_coords[1] > player_coords[1]:
                    if ball_coords[0] < player_coords[0]:
                        if self.vx > 0:
                            self.vx = - self.vx
                    if ball_coords[0] > player_coords[0]:
                        if self.vx < 0:
                            self.vx = - self.vx
                elif ball_coords[1] <= player_coords[1]:
                    leng = ball_coords[0] - player_coords[0]
                    self.vx = leng // 10
                    if self.vx == 0:
                        if leng < 0:
                            self.vx = -1
                        elif leng > 0:
                            self.vx = 1
                        else:
                            self.vx = random.choice([-1,1])
                    v_tiles = (kolvo_tiles_per_level[level - 1] - len(all_tiles)) // 30
                    if abs(self.vx) >= 5:
                        self.vy = -5 - v_tiles + level // 4
                    if abs(self.vx) < 5 and abs(self.vx) >= 3:
                        self.vy = -6 - v_tiles + level // 4
                    if abs(self.vx) < 3:
                        self.vy = -7 - v_tiles + level // 4
                    if self.vy > 0:
                        self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, all_tiles):
                tiles_black = pygame.sprite.spritecollide(self, black_tiles, False)
                tiles = pygame.sprite.spritecollide(self, all_tiles, True)
                for tile in tiles:
                    points += points_from_tile
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
                #отражение 2.0
                if ball_coords[0] >= tile_coords[0] and ball_coords[0] <= tile_coords[0] + tile_size[0]: 
                    self.vy = -self.vy
                elif ball_coords[1] >= tile_coords[1] and ball_coords[1] <= tile_coords[1] + tile_size[1]:
                    self.vx = -self.vx
                else:
                    ball_coords = [self.rect.x, self.rect.y]
                    if self.vx > 0 and self.vy > 0:
                        ball_c = [ball_coords[0] + tile_size[0], ball_coords[1] + tile_size[0]]
                        tile_c = [tile_coords[0], tile_coords[1]]
                    if self.vx < 0 and self.vy > 0:
                        ball_c = [ball_coords[0], ball_coords[1] + tile_size[0]]
                        tile_c = [tile_coords[0] + tile_size[0], tile_coords[1]]
                    if self.vx > 0 and self.vy < 0:
                        ball_c = [ball_coords[0] + tile_size[0], ball_coords[1]]
                        tile_c = [tile_coords[0], tile_coords[1] + tile_size[1]]
                    if self.vx < 0 and self.vy < 0:
                        ball_c = [ball_coords[0], ball_coords[1]]
                        tile_c = [tile_coords[0] + tile_size[0], tile_coords[1] + tile_size[1]]
                    if self.vy == 0:
                        ball_c = [0, 1]
                        tile_c = [0, 0]

                    if abs(ball_c[0] - tile_c[0]) >= abs(ball_c[1] - tile_c[1]):
                        self.vy = -self.vy
                    elif abs(ball_c[0] - tile_c[0]) < abs(ball_c[1] - tile_c[1]):
                        self.vx = -self.vx

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
        self.velocity = [int(dx), int(dy)]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += int(self.velocity[0])
        self.rect.y += int(self.velocity[1])
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 10 - len(all_particles) // 5
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
        self.typy = tile_type
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_size[0], tile_size[1]))
        self.x = 20 + tile_size[0] * pos_x - 3
        self.y = 20 + tile_size[1] * pos_y     
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(self.x, self.y)
    def get_coords(self):
        return self.x, self.y
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
rules_sprites = pygame.sprite.Group()

class Button(pygame.sprite.Sprite): 
    def __init__(self, group, name, x, y, rect_x, rect_y, focused):
        super().__init__(group)
        self.image = pygame.Surface((300, 100))
        self.image.fill((0, 0, 230))
        self.image.blit(pygame.font.Font(None, 35).render(str(name) , 1, (255, 255, 255)), (10, 25))
        self.rect = pygame.Rect(x, y, rect_x, rect_y)
        self.rect.x = x
        self.start_x = x
        self.rect.y = y
        self.start_y = y 
        self.name = name
        self.focused = focused
        if self.focused:
            pygame.draw.rect(self.image, (20, 230, 20), (0, 0, 300, 100), 5)
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
    
def music_change():
    global playlist
    pygame.mixer.music.load(playlist[-1])
    playlist.pop()
    pygame.mixer.music.play()
    if len(playlist) == 0:
        playlist = ["data\music_1.mp3", "data\music_2.mp3",
                    "data\music_3.mp3", "data\music_4.mp3"]
    
def load():
    filename = "data/saves.txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        bas_lives = int(level_map[0].split("=")[1])
        total_points = int(level_map[1].split("=")[1])
        upgrade_kolvo = int(level_map[2].split("=")[1])
        points_from_tile = int(level_map[3].split("=")[1])
        if int(level_map[4].split("=")[1]) == 1:
            randombreaker = True
        else:
            randombreaker = False
    return bas_lives, total_points, upgrade_kolvo, points_from_tile, randombreaker
bas_lives, total_points, upgrade_kolvo, points_from_tile, randombreaker = load()

level = 0
main_menu_buttons = {
        'Play' : False,
        'Shop' : False,
        'Save data' : False,
        'Quit' : False
        }
board_size = (tile_size[1] * 3 + upgrade_kolvo * tile_size[1], tile_size[1])

while main_game:
    main_menu_sprites = pygame.sprite.Group()
    shop_sprites = pygame.sprite.Group()
    if music:
        pygame.mixer.music.unpause()
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.pause()
    y_start = 500
    for i in range(4):
        if i == 0:
            name = "Play"
        if i == 1:
            name = "Shop"
        if i == 2:
            name = "Save data"
        if i == 3:
            name = "Quit"
        Button(main_menu_sprites, name, size[0] // 2 - 150, y_start, 500, 200, main_menu_buttons[name])
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
        if event.type == pygame.USEREVENT:
            music_change()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            if sound:
                sound_click.play()
            if event.pos[0] >= 830 and event.pos[0] <= 880 and event.pos[1] >= 900 and event.pos[1] <= 950:
                if music:
                    music = False
                else:
                    music = True
            if event.pos[0] >= 900 and event.pos[0] <= 950 and event.pos[1] >= 900 and event.pos[1] <= 950:
                if sound:
                    sound = False
                else:
                    sound = True
            for button in main_menu_sprites:
                if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                    if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                        if button.name == "Play":
                            lives = bas_lives
                            start_seconds = pygame.time.get_ticks()
                            level = 0
                            points = 0
                            while True:
                                if music:
                                    pygame.mixer.music.unpause()
                                else:
                                    pygame.mixer.music.pause()
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
                                Player()
                                Ball()
                                AnimatedSprite(load_image("money.png"), 16, 1, size[0] - 200, 50)

                                pygame.mixer.music.set_volume(0.5)

                                level += 1
                                first = True
                                generate_level(load_level('level' + str(level) + '.txt'))
                                while True:
                                    mouse_moving = False
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            terminate()
                                            pygame.quit()
                                        if event.type == pygame.USEREVENT:
                                            music_change()
                                        if event.type == pygame.MOUSEMOTION:
                                            mouse_moving = True
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            mouse_down = False
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_down = True
                                            if sound:
                                                sound_click.play()
                                            if event.button == 1 and first:
                                                if cheat:
                                                    first = False
                                                    for ball in ball_group:
                                                        ball.stopping = False
                                            if pauze and event.pos[0] >= 830 and event.pos[0] <= 980 and event.pos[1] >= 900 and event.pos[1] <= 970:
                                                game_over = True
                                                break
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_x:
                                                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                                    cheat = True
                                            if event.key == pygame.K_z:
                                                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                                        for tile in all_tiles:
                                                            all_tiles.remove(tile)
                                            if event.key == pygame.K_UP:
                                                for ball in ball_group:
                                                    ball.vy -= 1
                                            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                                                if first:
                                                    first = False
                                                    for ball in ball_group:
                                                        ball.stopping = False
                                                    without_breaking = pygame.time.get_ticks()
                                                else:
                                                    if not pauze:
                                                        pauze = True
                                                    else:
                                                        pauze = False
                                    screen.blit(fon, (0, 0))
                                    if cheat:
                                        for ball in ball_group:
                                            screen.blit(pygame.font.Font(None, 40).render("VX {} VY {}".format(ball.vx, ball.vy), 1, (255, 255, 255)), (size[0] - 200, 650))
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
                                        if randombreaker and not first:
                                            seconds_without_breaking = pygame.time.get_ticks() - without_breaking
                                            if seconds_without_breaking % 10000 <= 15:
                                                if sound:
                                                    sound_shoot.play()
                                                tiles_list = [tile for tile in all_tiles]
                                                best_tile = random.choice(tiles_list)
                                                if best_tile.typy == 'black':
                                                    black_tiles.remove(best_tile)
                                                all_sprites.remove(best_tile)
                                                all_tiles.remove(best_tile)
                                        for coin in coin_group:
                                            coin.update()
                                    else:

                                        pygame.mixer.music.set_volume(0.25)
                                        pause = pygame.sprite.Group()
                                        sprite = pygame.sprite.Sprite()
                                        sprite.image = pygame.transform.scale(load_image('pauze.png'), (200, 200))
                                        sprite.rect = sprite.image.get_rect()
                                        sprite.rect.x = ground_size[0] // 2 + 20
                                        sprite.rect.y = ground_size[1] // 2 + 20
                                        sprite.add(pause)

                                        pos = pygame.mouse.get_pos()
                                        x = pos[0]
                                        y = pos[1]
                                        menu = pygame.Surface((150, 70))
                                        menu.fill((0, 0, 230))
                                        menu.blit(pygame.font.Font(None, 35).render("Main menu", 1, (255, 255, 255)), (10, 25))
                                        if x >= 830 and x <= 980 and y >= 900 and y <= 970:
                                            pygame.draw.rect(menu, (20, 230, 20), (0, 0, 150, 70), 5)


                                    screen.blit(pygame.font.Font(None, 50).render(str(points) , 1, (255, 255, 255)), (size[0] - 170, 50))
                                    screen.blit(pygame.font.Font(None, 50).render("LIVES x {}".format(str(lives)), 1, (255, 255, 255)), (size[0] - 200, 325))
                                    screen.blit(pygame.font.Font(None, 50).render("LEVEL {}".format(str(level)) , 1, (255, 255, 255)), (size[0] - 200, 450))
                                    seconds_in_game = (pygame.time.get_ticks() - start_seconds) // 1000
                                    screen.blit(pygame.font.Font(None, 50).render("TIME {}".format(str(seconds_in_game)), 1, (255, 255, 255)), (size[0] - 200, 200))
                                    all_sprites.draw(screen)

                                    if pauze:
                                        pause.draw(screen)
                                        screen.blit(menu, (830, 900))

                                    pos = pygame.mouse.get_pos()
                                    x = pos[0]
                                    y = pos[1]
                                    draw_cursor(screen, x, y)

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
                                    start_screen("gameend.png")
                                    break
                            if level == 10 and not game_over:
                                break
                            if game_over:
                                gameover = pygame.sprite.Group()
                                pygame.mixer.music.set_volume(0.1)
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
                                if sound:
                                    sound3.play()
                                while running:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                        if event.type == pygame.USEREVENT:
                                            music_change()
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
                            coin_group = pygame.sprite.Group()
                            Image(coin_group, 100, 100, 90, 350)
                            shopping = True
                            shop_buttons = {
                                        'Buy live (cost 7000)' : False,
                                        'Main menu' : False,
                                        'Upgrade (cost 10000)' : False,
                                        'Points + 5 (cost 8000)' : False,
                                        'Breaker (cost 10000)' : False
                                        }
                            while shopping:
                                second = True
                                Button(shop_sprites, 'Buy live (cost 7000)', 300, 100, 500, 200, shop_buttons['Buy live (cost 7000)'])
                                Button(shop_sprites, 'Main menu', 50, size[1] - 150, 500, 200, shop_buttons['Main menu'])
                                Button(shop_sprites, 'Upgrade (cost 10000)', 300, 230, 500, 200, shop_buttons['Upgrade (cost 10000)'])
                                Button(shop_sprites, 'Points + 5 (cost 8000)', 300, 360, 500, 200, shop_buttons['Points + 5 (cost 8000)'])
                                Button(shop_sprites, 'Breaker (cost 10000)', 300, 490, 500, 200, shop_buttons['Breaker (cost 10000)'])
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        terminate()
                                        pygame.quit()
                                    if event.type == pygame.USEREVENT:
                                        music_change()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_z:
                                            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                                total_points += 100000
                                    if event.type == pygame.MOUSEMOTION:
                                        for button in shop_sprites:
                                            if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                                                if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                                                    shop_buttons[button.name] = True
                                                elif event.pos[1] < button.rect.y or event.pos[1] > button.rect.y + 100:
                                                    shop_buttons[button.name] = False
                                            elif event.pos[0] < button.rect.x or event.pos[0] > button.rect.x + 300:
                                                shop_buttons[button.name] = False
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        mouse_down = False
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_down = True
                                        if sound:
                                            sound_click.play()
                                        for button in shop_sprites:
                                            if event.pos[0] >= button.rect.x and event.pos[0] <= button.rect.x + 300:
                                                if event.pos[1] >= button.rect.y and event.pos[1] <= button.rect.y + 100:
                                                    if button.name == 'Buy live (cost 7000)' and second:
                                                        if total_points >= 7000:
                                                            total_points -= 7000
                                                            bas_lives += 1
                                                            second = False
                                                    elif button.name == 'Upgrade (cost 10000)':
                                                        if total_points >= 10000 and upgrade_kolvo < 3 and second:
                                                            total_points -= 10000
                                                            board_size = (board_size[0] + tile_size[1] // 2, board_size[1])
                                                            upgrade_kolvo += 1
                                                            second = False
                                                    elif button.name == 'Points + 5 (cost 8000)':
                                                        if total_points >= 8000 and second:
                                                            total_points -= 8000
                                                            points_from_tile += 5
                                                            second = False
                                                    elif button.name == 'Breaker (cost 10000)' and not randombreaker:
                                                        if total_points >= 10000 and second:
                                                            total_points -= 10000
                                                            randombreaker = True
                                                            second = False
                                                    elif button.name == 'Main menu':
                                                        shopping = False
                                for button in shop_sprites:
                                    button.update()
                                screen.blit(pygame.transform.scale(load_image('fon.png'), (size[0], size[1])), (0, 0))
                                screen.blit(pygame.transform.scale(load_image('door.png'), (board_size[0], board_size[1])), (50 + tile_size[1] * 3 - board_size[0] // 2, 250))
                                screen.blit(pygame.transform.scale(load_image('sniper.png'), (100, 100)), (100, 490))
                                screen.blit(pygame.font.Font(None, 50).render("+ {}".format(str(points_from_tile)), 1, (255, 255, 255)), (200, 370))
                                screen.blit(pygame.font.Font(None, 50).render("LIVES x {}".format(str(bas_lives)), 1, (255, 255, 255)), (50, 127))
                                screen.blit(pygame.font.Font(None, 50).render("TOTAL POINTS:  {}".format(str(total_points)), 1, (255, 255, 255)), (100, 50))
                                shop_sprites.draw(screen)

                                if upgrade_kolvo == 3:
                                    screen.blit(pygame.transform.scale(load_image('byied.png'), (100, 100)), (100, 230))
                                    screen.blit(pygame.transform.scale(load_image('nobyied.png'), (320, 120)), (300 - 10, 230 - 10))
                                if randombreaker:
                                    screen.blit(pygame.transform.scale(load_image('byied.png'), (100, 100)), (100, 490))
                                    screen.blit(pygame.transform.scale(load_image('nobyied.png'), (320, 120)), (300 - 10, 490 - 10))
                                coin_group.draw(screen)

                                pos = pygame.mouse.get_pos()
                                x = pos[0]
                                y = pos[1]
                                draw_cursor(screen, x, y)

                                pygame.display.flip()
                                clock.tick(60)
                        if button.name == "Save data":
                            if sound:
                                sound5.play()
                            filename = "data/saves.txt"
                            if randombreaker:
                                breaker = 1
                            else:
                                breaker = 0
                            with open(filename, 'w') as mapFile:
                                mapFile.write("lives={}\ntotal_points={}\nupgrade_kolvo={}\npoints_from_tile={}\nrandombreaker={}".format(bas_lives, total_points, upgrade_kolvo, points_from_tile, breaker))
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

    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]

    mus = pygame.Surface((50, 50))
    mus.fill((0, 0, 230))
    if x >= 830 and x <= 880 and y >= 900 and y <= 950:
        pygame.draw.rect(mus, (20, 230, 20), (0, 0, 50, 50), 5)
    screen.blit(mus, (830, 900))
    screen.blit(pygame.transform.scale(load_image('music.png'), (46, 46)), (830 + 2, 900 + 2))
    if not music:
        screen.blit(pygame.transform.scale(load_image('nobyied.png'), (60, 60)), (830 - 5, 900 - 5))

    sou = pygame.Surface((50, 50))
    sou.fill((0, 0, 230))
    if x >= 900 and x <= 950 and y >= 900 and y <= 950:
        pygame.draw.rect(sou, (20, 230, 20), (0, 0, 50, 50), 5)
    screen.blit(sou, (900, 900))
    screen.blit(pygame.transform.scale(load_image('sound.png'), (46, 46)), (900 + 2, 900 + 2))
    if not sound:
        screen.blit(pygame.transform.scale(load_image('nobyied.png'), (60, 60)), (900 - 5, 900 - 5))
    for button in main_menu_sprites:
        button.update()
    main_menu_sprites.draw(screen)

    draw_cursor(screen, x, y)

    pygame.display.flip()
    frames = (frames + 1) % 60
    clock.tick(60)
pygame.quit()