"""A minesweeper clone written with Pygame."""

import pygame
import random
import sys
import math
import time

from pygame.locals import *

FPS = 30
X_TILES = 20
Y_TILES = 20
TILE_SIZE = 25
MINES = 50
SMILEY_SIZE = 40
LEFT = 1
RIGHT = 3
GAME_SURFACE = pygame.display.set_mode((X_TILES*TILE_SIZE,
                                        Y_TILES*TILE_SIZE + SMILEY_SIZE))
state = [[[0 for z in range(2)] for y in range(Y_TILES)] for x in range(X_TILES)]

#Load all of the tile images.
NORMAL_TILE = pygame.image.load("NormalTile.png")
BOMB_TILE = pygame.image.load("RedBombTile.png")
FLAGGED_TILE = pygame.image.load("FlaggedTile.png")
QUESTION_TILE = pygame.image.load("QuestionTile.png")
SMILEY = pygame.image.load("Smiley.png")
DEAD_SMILEY = pygame.image.load("Dead.png")
COOL_SMILEY = pygame.image.load("Glasses.png")
CLICKED_TILE = []
for i in range(9):
    CLICKED_TILE.append(pygame.image.load("ClickedTile%d.png" % i))

#Define what the program does if the user left clicks on a tile.
def left_click(coordinate):
    global state
    global lost_game
    if(coordinate[1] < 0 and math.floor(X_TILES/2-2) < coordinate[0] < math.floor(X_TILES/2+1)):
        reinit()
    elif(not lost_game and not won_game):
        if(state[coordinate[0]][coordinate[1]][0] is 0 and coordinate[1] >= 0):
            if(check_if_mine(coordinate)):
                lost_game = True
                end_the_game()
            else:
                uncover_tile(coordinate)
                state[coordinate[0]][coordinate[1]][0] = 1
                did_you_win()
                if(state[coordinate[0]][coordinate[1]][1] is 0):
                    propagate(coordinate)
        elif(state[coordinate[0]][coordinate[1]][0] is 1 and coordinate[1] >= 0):
            destroy_adjacent(coordinate)
        
#Define what the program does if the use right clicks on a tile.
def right_click(coordinate):
    global state
    global remaining_mines
    if(state[coordinate[0]][coordinate[1]][0] is 0):
        GAME_SURFACE.blit(FLAGGED_TILE, get_pixel(coordinate))
        state[coordinate[0]][coordinate[1]][0] = 2
        remaining_mines -= 1
    elif(state[coordinate[0]][coordinate[1]][0] is 2):
        GAME_SURFACE.blit(QUESTION_TILE, get_pixel(coordinate))
        state[coordinate[0]][coordinate[1]][0] = 3
    elif(state[coordinate[0]][coordinate[1]][0] is 3):
        GAME_SURFACE.blit(NORMAL_TILE, get_pixel(coordinate))
        state[coordinate[0]][coordinate[1]][0] = 0
        remaining_mines += 1
        
#Uncover a blank tile to expose a bomb or numbered tile.    
def uncover_tile(coordinate):
    if(check_if_mine(coordinate)):
        GAME_SURFACE.blit(BOMB_TILE, get_pixel(coordinate))
        return True
    else:   
        GAME_SURFACE.blit(CLICKED_TILE[state[coordinate[0]][coordinate[1]][1]], get_pixel(coordinate))
        return False
        
#Find the tile that corresponds to the pixel coordinates of a mouse click.        
def get_tile(coordinate):
    box = (int(math.floor(coordinate[0]/TILE_SIZE)), 
            int(math.floor((coordinate[1]-SMILEY_SIZE)/TILE_SIZE)))

    return box

#Figure out the upper left pixel of a specific tile for drawing purposes.    
def get_pixel(coordinate):
    pixel = (coordinate[0]*TILE_SIZE, 
                (coordinate[1]*TILE_SIZE + SMILEY_SIZE))
    return pixel
    
#Check to see if the tile you clicked on contains a mine.    
def check_if_mine(coordinate):
    if(state[coordinate[0]][coordinate[1]][1] is 10):
        return True
    else:
        return False

#Check to see if the use has won the game or not.
def did_you_win():
    global won_game
    for x in range(X_TILES):
        for y in range(Y_TILES):
            if(state[x][y][0] is 0 and state[x][y][1] is not 10):
                return
    won_game = True
    end_the_game()
        
#Check all of the neighbors around the tile you left clicked on and count the mines.        
def check_neighbors(coordinate):
    mine_counter=0
    for dx, dy in [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i is j is 0)]: #iterate through adjacent cells
        if(0 <= (coordinate[0] + dx) < X_TILES and 0 <= (coordinate[1] + dy) < Y_TILES): #check boundaries
            if(check_if_mine((coordinate[0] + dx,coordinate[1] + dy))):
                mine_counter += 1
    return mine_counter     

#Count the number of flags that are on adjacent tiles to the one you clicked.    
def check_neighbors_flags(coordinate):
    flag_counter=0
    for dx, dy in [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i is j is 0)]: #iterate through adjacent cells
        if(0 <= (coordinate[0] + dx) < X_TILES and 0 <= (coordinate[1] + dy) < Y_TILES): #check boundaries
            if(state[coordinate[0] + dx][coordinate[1] + dy][0] is 2):
                flag_counter += 1
    return flag_counter     

#Propagates through a big empty pocket for the player.
def propagate(coordinate):
    global state
    for dx, dy in [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i is j is 0)]: #iterate through adjacent cells
        if(0 <= (coordinate[0] + dx) < X_TILES and 0 <= (coordinate[1] + dy) < Y_TILES): #check boundaries
            if(state[coordinate[0] + dx][coordinate[1] + dy][0] is 0):
                left_click((coordinate[0] + dx,coordinate[1] + dy))

#Click on all of the adjacent mines to blow them up.                
def destroy_adjacent(coordinate):
    if(check_neighbors_flags(coordinate) is state[coordinate[0]][coordinate[1]][1]):
        for dx, dy in [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i is j is 0)]: #iterate through adjacent cells
            if(0 <= (coordinate[0] + dx) < X_TILES and 0 <= (coordinate[1] + dy) < Y_TILES): #check boundaries
                if(state[coordinate[0] + dx][coordinate[1] + dy][0] is 0):
                    left_click((coordinate[0] + dx,coordinate[1] + dy))
        
#Randomly generate the mines.
def generate_mines(mine_quantity):
    global state
    i = 0
    while(i < mine_quantity):
        x = random.randint(0,X_TILES-1)
        y = random.randint(0,Y_TILES-1)
        if(state[x][y][1] is 0):
            state[x][y][1] = 10
            i += 1
    
#populate the 3d list that contains data about the board.    
def populate_state():
    global state
    for x in range(X_TILES):
            for y in range(Y_TILES):
                if(state[x][y][1] !=10):
                    state[x][y][1] = check_neighbors((x, y))

#Uncover all bombs and lock the screen up if the game is lost.                    
def end_the_game():
    if(lost_game):
        GAME_SURFACE.blit(DEAD_SMILEY, ((X_TILES*TILE_SIZE)/2 - SMILEY_SIZE/2, 0))
        for x in range(X_TILES):
            for y in range(Y_TILES):
                if(check_if_mine((x,y)) and state[x][y][0] is 0):
                    uncover_tile((x, y))
    elif(won_game):
        GAME_SURFACE.blit(COOL_SMILEY, ((X_TILES*TILE_SIZE)/2 - SMILEY_SIZE/2, 0))

#Calculates the time to be displayed in the upper left hand corner.        
def get_time():
    global lost_game
    time_dif = math.floor(time.time()-initial_time)
    if(time_dif < 10):
        return "00" + str(time_dif)
    elif(time_dif < 100):
        return "0" + str(time_dif)
    elif(time_dif < 1000):
        return str(time_dif)
    else:
        lost_game = True
        end_the_game()
        
#Refresh the mine_counter and timer text boxes.
def set_text():
    timer = DIGITAL_FONT.render(get_time(), True, (255,0,0), (0, 0, 0))
    mine_counter = DIGITAL_FONT.render(str(remaining_mines), True, (255,0,0), (0, 0, 0))
    timer_box = timer.get_rect()
    timer_box.topright = (X_TILES*TILE_SIZE,0)
    mine_counter_box = mine_counter.get_rect()
    mine_counter_box.topleft = (0,0)
    if(not lost_game):
        GAME_SURFACE.blit(timer, timer_box)
        GAME_SURFACE.blit(mine_counter, mine_counter_box)
    
#Below are the initializations and main loop.
remaining_mines = MINES
pygame.init()
pygame.display.set_caption('Minesweeper')
FPSCLOCK = pygame.time.Clock()
DIGITAL_FONT = pygame.font.Font('digital-7 (mono).ttf', 40)
initial_time = 0

#Initialize the board with blank tiles and rest counters and timers.
def reinit():
    global lost_game
    global won_game
    global remaining_mines
    global state
    global initial_time
    for x in range(X_TILES):
        for y in range(Y_TILES):
            GAME_SURFACE.blit(NORMAL_TILE, (x*TILE_SIZE, y*TILE_SIZE + SMILEY_SIZE))
            state[x][y][0] = 0
            state[x][y][1] = 0
    lost_game = False
    won_game = False
    generate_mines(MINES)
    populate_state()   
    GAME_SURFACE.blit(SMILEY, ((X_TILES*TILE_SIZE)/2 - SMILEY_SIZE/2, 0))
    remaining_mines = MINES
    initial_time = time.time()

#Below is the main loop.
reinit()
while True:
    for event in pygame.event.get():
        if event.type is QUIT:
            pygame.quit()
            sys.exit()
        elif event.type is  MOUSEBUTTONDOWN and event.button is LEFT:
            left_click(get_tile(event.pos))
        elif event.type is  MOUSEBUTTONDOWN and event.button is RIGHT:
            right_click(get_tile(event.pos))
        
    set_text()
    pygame.display.update() 
    FPSCLOCK.tick(FPS)           

 