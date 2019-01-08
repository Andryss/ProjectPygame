import pygame
import random

pygame.init() 
size = 400, 800
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
clock = pygame.time.Clock()
balls = {}
door_size = (100, 40)
door = [size[0] // 2 - 40, size[1] - 5 - door_size[1]]
moves = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
move = 10
pygame.time.set_timer(move, 500)
k = 10
pygame.time.set_timer(k, 10)
new = 0
points = 0
level = 5
kolvo = 0

running = True
pygame.draw.rect(screen, (255, 255, 255), (door[0], door[1], door_size[0], door_size[1]))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if k:
            new += 10
        if new == 5000:
            new = 0
            if len(balls) < level:
                kolvo += 1
                pos = (random.randint(10, size[0] - 10), 15)
                pygame.draw.circle(screen, (255, 255, 255), pos, 10)
                balls[pos] = random.choice(moves)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if door[0] < size[0] - 5 - door_size[0]:
                door[0] += 5
                screen.fill((0, 0, 255))
                pygame.draw.rect(screen, (255, 255, 255), (door[0], door[1], door_size[0], door_size[1]))
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if door[0] > 5:
                door[0] -= 5
                screen.fill((0, 0, 255))
                pygame.draw.rect(screen, (255, 255, 255), (door[0], door[1], door_size[0], door_size[1]))
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN:
                if level > 1:
                    level -= 1
                    kolvo -= 1
                    balls.popitem()
        
            
        if balls != {} and move:
            points += 1 * kolvo
            screen.fill((0, 0, 255))
            pygame.draw.rect(screen, (255, 255, 255), (door[0], door[1], door_size[0], door_size[1]))
            screen.blit(pygame.font.Font(None, 50).render(str(points), 1, (100, 255, 100)), (5, 5))
            screen.blit(pygame.font.Font(None, 50).render("LEVEL {}".format(kolvo) , 1, (100, 255, 100)), (5, 45))
            for ball in balls.keys():
                if balls[ball] == moves[0]:
                    ball_cop = (ball[0] - 1, ball[1] - 1)
                    del balls[ball]
                    ball = ball_cop
                    balls[ball] = moves[0]
                    pygame.draw.circle(screen, (255, 255, 255), ball, 10)
                elif balls[ball] == moves[1]:
                    ball_cop = (ball[0] + 1, ball[1] - 1)
                    del balls[ball]
                    ball = ball_cop
                    balls[ball] = moves[1]
                    pygame.draw.circle(screen, (255, 255, 255), ball, 10) 
                elif balls[ball] == moves[2]:
                    ball_cop = (ball[0] + 1, ball[1] + 1)
                    del balls[ball]
                    ball = ball_cop
                    balls[ball] = moves[2]
                    pygame.draw.circle(screen, (255, 255, 255), ball, 10) 
                elif balls[ball] == moves[3]:
                    ball_cop = (ball[0] - 1, ball[1] + 1)
                    del balls[ball]
                    ball = ball_cop
                    balls[ball] = moves[3]
                    pygame.draw.circle(screen, (255, 255, 255), ball, 10)                
                if ball[0] == 10:
                    if balls[ball] == moves[0]:
                        balls[ball] = moves[1]
                    elif balls[ball] == moves[3]:
                        balls[ball] = moves[2]
                if ball[1] == 10:
                    if balls[ball] == moves[0]:
                        balls[ball] = moves[3]
                    elif balls[ball] == moves[1]:
                        balls[ball] = moves[2]  
                if ball[0] == size[0]-10:
                    if balls[ball] == moves[2]:
                        balls[ball] = moves[3]
                    elif balls[ball] == moves[1]:
                        balls[ball] = moves[0]
                if ball[1] == size[1]-10:
                    running = False
                    game_over = True
                if (ball[0] > door[0]) and (ball[0] < door[0] + door_size[0]):
                    if ball[1] == door[1] - 10:
                        if balls[ball] == moves[2]:
                            balls[ball] = moves[1]
                        elif balls[ball] == moves[3]:
                            balls[ball] = moves[0]
                elif (ball[1] <= door[1] + door_size[1]) and (ball[1] >= door[1] - 10):
                    if (ball[0] >= door[0] - 10) and (ball[0] <= door[0] + 10 + door_size[0]):
                        if balls[ball] == moves[2]:
                            balls[ball] = moves[0]
                        elif balls[ball] == moves[3]:
                            balls[ball] = moves[1]
                
    pygame.display.flip()            
    clock.tick(140)     
    
while game_over:
    text = pygame.font.Font(None, 50).render("GAME OVER", 1, (100, 255, 100))
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
    pygame.display.flip()            
    clock.tick(140)    
            
pygame.quit()