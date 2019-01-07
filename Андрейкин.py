import pygame
import random

pygame.init() 
size = 400, 800
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
clock = pygame.time.Clock()
balls = {}
door = [size[0] // 2 - 40, size[1] - 15]
moves = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
move = 10
pygame.time.set_timer(move, 50000)
k = 10
pygame.time.set_timer(k, 10)
new = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if k:
            new += 10
        if new == 4000:
            new = 0
            pos = (random.randint(10, size[0] - 10), 15)
            pygame.draw.circle(screen, (255, 255, 255), pos, 10)
            balls[pos] = random.choice(moves)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if door[0] < size[0] - 85:
                door[0] += 5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if door[0] > 5:
                door[0] -= 5
        
            
        if balls != {} and move:
            screen.fill((0, 0, 255))
            pygame.draw.rect(screen, (255, 255, 255), (door[0], door[1], 80, 15))
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
                    if balls[ball] == moves[2]:
                        balls[ball] = moves[1]
                    elif balls[ball] == moves[3]:
                        balls[ball] = moves[0]
                
    pygame.display.flip()            
    clock.tick(140)       

pygame.quit()