import pygame
import random
from pygame import mixer
pygame.init()

clock = pygame.time.Clock()
current_time = 0
start_time = pygame.time.get_ticks()
crossHair = pygame.image.load('data\\image\\crosshair.png')
pygame.display.set_icon(crossHair)
background = pygame.image.load('data\\image\\haunted_house.png')
background = pygame.transform.scale(background, (1400, 800))
pygame.display.set_caption('Aim Game')
mixer.music.load('data\\sound\\Advent.mp3')
mixer.music.play(-1)
# Enemy
bigSkeleton = pygame.image.load('data\\image\\skele2.png')
smallSkeleton = pygame.image.load('data\\image\\skele1.png')
biggestSkeleton = pygame.image.load('data\\image\\skeleBig.png')
running = True
screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE, pygame.VIDEORESIZE)

# Variables
bigX = random.randint(0, 1300)
bigY = random.randint(100, 700)
smallX = random.randint(0, 1300)
smallY = random.randint(100, 700)

smallRect = smallSkeleton.get_rect(center = (smallX, smallY))
bigRect = bigSkeleton.get_rect(center = (bigX, bigY))

score = 0
active = True
before = True
game_font = pygame.font.Font('data\\animeace2_bld.ttf', 30)
# Mouse
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
def mouse(x, y):
    return pygame.draw.circle(screen, (255, 255, 255), (x, y), 6, width=1)

def draw(x, y):
    screen.blit(x, y)

# ----------- Game Loop --------------
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    mx, my = pygame.mouse.get_pos()

    score_text = game_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center = (150, 50))

    time_left_text = game_font.render('Time Left: ' + str(60 - int((current_time - start_time)/1000)),
        True, (255, 255, 255))
    time_left_rect = time_left_text.get_rect(center = (600, 750))
    if active == True:
        if before == True:
            screen.blit(biggestSkeleton, (0, 0))
            taunt_text = game_font.render('Let\'s test your aim', True, (255, 255, 255))
            taunt_rect = taunt_text.get_rect(center= (400, 150))

            start_text = game_font.render("Aim Game", True, (255, 255, 255))
            start_rect = start_text.get_rect(center = (650, 350))
            
            press_text = game_font.render("Press any key to Start", True, (255, 255, 255))
            press_rect = press_text.get_rect(center = (650, 500))
            screen.blit(taunt_text, taunt_rect)
            screen.blit(start_text, start_rect)
            screen.blit(press_text, press_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    before = False
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    background = pygame.transform.scale(background, (event.w, event.h))
    if active == True:
        if before == False:
            # -------- Timer ----------
            current_time = pygame.time.get_ticks()
            left = current_time - start_time 
            # --------- Collision ----------
            if mouse(mx, my).colliderect(smallRect):
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            smallX = random.randint(0, 1300)
                            smallY = random.randint(100, 700)
                            smallRect = smallSkeleton.get_rect(center = (smallX, smallY))
                            score += 150
                            sound = mixer.Sound('data\\sound\\gunshot.mp3')
                            sound.set_volume(0.5)
                            sound.play()
            if mouse(mx, my).colliderect(bigRect):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bigX = random.randint(0, 1300)
                        bigY = random.randint(100, 700)
                        bigRect = bigSkeleton.get_rect(center = (bigX, bigY))
                        score += 100
                        sound = mixer.Sound('data\\sound\\gunshot.mp3')
                        sound.set_volume(0.5)
                        sound.play()
            if left >= 30*1000:
                draw(smallSkeleton, smallRect)
            if left < 30*1000:
                draw(bigSkeleton, bigRect)

            screen.blit(score_text, score_rect)   
            screen.blit(time_left_text, time_left_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            background = pygame.transform.scale(background, (event.w, event.h))
    # --------- Game Over ------------
    if (current_time - start_time >= 1000*60):
        active = False
        over_text = game_font.render('Game Over', True, (255, 255, 255))
        over_rect = over_text.get_rect(center = (750, 350))
        screen.blit(over_text, over_rect)
        screen.blit(score_text, (600, 150))
    mouse(mx, my)
    pygame.display.update()