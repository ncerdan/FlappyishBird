#IMPORTS
import pygame
import random
import math

#INITIALIZE AND CLOCK
pygame.init()
clock = pygame.time.Clock()

#CREATES DISPLAY AND ITS VARIABLES
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 600
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
GAME_RECT = GAME_DISPLAY.get_rect()
pygame.display.set_caption('Flappyish Bird')

#IMPORTS BIRD AND MAKES ITS VARIABLES
ORIGINAL_BIRD_IMAGE = pygame.image.load('res\ird.png')
BIRD_WIDTH = 41
BIRD_HEIGHT = 41

#IMPORTS BASE AND MAKES ITS VARIABLES
BASE_IMAGE = pygame.image.load('res\ground.png')
BASE_HEIGHT = DISPLAY_HEIGHT * .1

#IMPORT SKY AND DEAD BIRD
SKY_IMAGE = pygame.image.load('res\sky.png')
SKY_IMAGE_RECT = SKY_IMAGE.get_rect()
DEAD_BIRD_IMAGE = pygame.image.load('res\dead_bird.png')

#MAKES PIPES VARIABLES
PIPE_WIDTH = 65
PIPE_SPEED = -3
PIPE_GAP = 185

#COLORS
PIPE_GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#FONTS
IN_GAME_SCORE_FONT = pygame.font.SysFont('bookman old style', 30)
MENU_SUPER_SMALL_FONT = pygame.font.SysFont('bookman old style', 15)
MENU_SMALL_FONT = pygame.font.SysFont('bookman old style', 25)
MENU_LARGE_FONT = pygame.font.SysFont('bookman old style', 50)

#GLOBAL VARIABLES
high_score = 0

#START MENU
def startMenu():
    while True:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()
                    
        GAME_DISPLAY.fill(WHITE)
        
        show_text_middle('Flappyish Bird', MENU_LARGE_FONT, 200, BLACK)
        show_text_middle('Press SPACE to Play!', MENU_SMALL_FONT, 275, BLACK)
        pygame.display.update()

#DEATH MENU
def death_menu(score, new_high_score):
    while True:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
        GAME_DISPLAY.fill(WHITE)
        
        if new_high_score:
            show_text_middle('NEW HIGH SCORE OF ' + str(score) + '!', MENU_SMALL_FONT, 100, PIPE_GREEN)
        
        show_text_middle('YOU DIED!', MENU_LARGE_FONT, 175, RED)
        show_text_middle('Score: ' + str(score) + '', MENU_LARGE_FONT, 250, BLACK)
        show_text_middle('Press SPACE to Play Again!', MENU_SMALL_FONT, 325, BLACK)     
        show_text_middle('Or ESC to Quit', MENU_SUPER_SMALL_FONT, 375, BLACK)
        GAME_DISPLAY.blit(DEAD_BIRD_IMAGE, (125, 425))
        
        pygame.display.update()
         
         
#DRAWS BIRD 
def draw_bird(x, y, vel):
    xchange = -PIPE_SPEED;
    ychange = -vel
    rad = math.atan2(ychange, xchange)
    deg = math.degrees(rad)
    
    if deg > 60:
        deg = 60
    if deg < -60:
        deg = -60
    
    temp_image = pygame.transform.rotate(ORIGINAL_BIRD_IMAGE, deg)
    GAME_DISPLAY.blit(temp_image, (x, y))
    
#DRAWS PIPE
def draw_pipe(x, y_top):
    pygame.draw.rect(GAME_DISPLAY, PIPE_GREEN, (x, 0, PIPE_WIDTH, y_top))
    pygame.draw.rect(GAME_DISPLAY, PIPE_GREEN, (x, y_top + PIPE_GAP, PIPE_WIDTH, DISPLAY_HEIGHT - (y_top + PIPE_GAP + BASE_HEIGHT / 2)))
    
#RETURN SURFACE AND RECT OF TEXT GIVEN TEXT, FONT, AND COLOR
def text_object(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

#BLITS SURFACE IN TOP-LEFT CORNER DURING GAME
def show_score(score):
    text_surf, text_rect = text_object(score, IN_GAME_SCORE_FONT, BLACK)
    GAME_DISPLAY.blit(text_surf, (15, 15))

#BLITS SURFACE WITH TEXT IN MIDDLE
def show_text_middle(text, font, y, color):
    text_surf, text_rect = text_object(text, font, color)
    GAME_DISPLAY.blit(text_surf, (GAME_RECT.width / 2 - text_rect.width / 2, y))

#RUNS GAME
def gameLoop():
    
    global high_score
    
    frame_counter = 0
    pipe_counter = 0
    pipes = []

    gravity = 1.2
    velocity = -17

    x = 20
    y = DISPLAY_HEIGHT / 2 - BIRD_HEIGHT / 2
    
    while True:

        #MAKES PIPES EVERY 90 FRAMES
        if frame_counter % 90 == 0:
            pipe = {
                'x' : DISPLAY_WIDTH,
                'y' : random.randrange(10, DISPLAY_HEIGHT - (PIPE_GAP + 10 + BASE_HEIGHT)),
                'counted' : False
            }
            pipes.append(pipe)

        #CHECKS INPUT EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = -17
 
        #COUNTS PIPES PASSED
        for pipe in pipes:
            if pipe['x'] + PIPE_WIDTH < x:
                if not pipe['counted']:
                    pipe_counter += 1
                    pipe['counted'] = True
 
        #UPDATES BIRD POS
        velocity += gravity
        y += velocity

        #UPDATES PIPES POS
        for pipe in pipes:
            pipe['x'] += PIPE_SPEED
            
        #MAX SPEED
        if (velocity > 10):
            velocity = 10

        #ENDS IF BIRD HITS BOTTOM
        if y + BIRD_HEIGHT > DISPLAY_HEIGHT - BASE_HEIGHT:
            if pipe_counter > high_score:
                high_score = pipe_counter
                death_menu(pipe_counter, True)
            else:
                death_menu(pipe_counter, False)
        #RESETS SPEED IF BIRD HITS TOP
        if y < 0:
            y = 0
            velocity = 0

        #CHECKS IF BIRD HITS PIPE
        for pipe in pipes:
            if x < pipe['x'] + PIPE_WIDTH and x + BIRD_WIDTH > pipe['x']:
                if y < pipe['y'] or y + BIRD_HEIGHT > pipe['y'] + PIPE_GAP:
                    if pipe_counter > high_score:
                        high_score = pipe_counter
                        death_menu(pipe_counter, True)
                    else:
                        death_menu(pipe_counter, False)
        
        #CHECKS IF PIPE IS OFF SCREEN
        for pipe in pipes:
            if pipe['x'] + PIPE_WIDTH < 0:
                pipes.remove(pipe)

        #CLEARS SCREEN AND DRAWS OBJECTS TO SCREEN
        GAME_DISPLAY.blit(SKY_IMAGE, (0, 0))
        GAME_DISPLAY.blit(BASE_IMAGE, (0, DISPLAY_HEIGHT - BASE_HEIGHT))
        
        draw_bird(x, y, velocity)

        for pipe in pipes:
            draw_pipe(pipe['x'], pipe['y'])

        show_score(str(pipe_counter))
    
        #UPDATES, TICKS, COUNTS FRAME
        pygame.display.update()
        clock.tick(60)
        frame_counter += 1

#CALLS START MENU TO START IT ALL
startMenu()

#QUITS EVERYTHING IN CASE IT BREAKS
pygame.quit()
quit()
