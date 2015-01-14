"""A minesweeper clone written with Pygame."""

import pygame
import random
import sys
import math

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
CLICKED_TILE = []
for i in range(9):
    CLICKED_TILE.append(pygame.image.load("ClickedTile%d.png" % i))

#Define what the program does if the user left clicks on a tile.
def left_click(coordinate):
    global state
    if(state[coordinate[0]][coordinate[1]][0] is 0):
        if(check_if_mine(coordinate)):
            lost_the_game()
        else:
            uncover_tile(coordinate)
            state[coordinate[0]][coordinate[1]][0] = 1

        
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
        
#Uncover a blank tile to expose a bomb or numbered tile    
def uncover_tile(coordinate):
    if(check_if_mine(coordinate)):
        GAME_SURFACE.blit(BOMB_TILE, get_pixel(coordinate))
        return True
    else:
        GAME_SURFACE.blit(CLICKED_TILE[state[coordinate[0]][coordinate[1]][1]], get_pixel(coordinate))
        return False
        
#Find the tile that corresponds to the pixel coordinates of a mouse click.        
def get_tile(coordinate):
    box = (math.floor(coordinate[0]/TILE_SIZE), 
            math.floor((coordinate[1]-SMILEY_SIZE)/TILE_SIZE))
    return box

#Figure out the upper left pixel of a specific tile for drawing purposes.    
def get_pixel(coordinate):
    pixel = (coordinate[0]*TILE_SIZE, 
                (coordinate[1]*TILE_SIZE + SMILEY_SIZE))
    return pixel
    
#Check to see if the tile you clicked on contains a mine.    
def check_if_mine(coordinate):
    if(state[coordinate[0]][coordinate[1]][1] == 10):
        return True
    else:
        return False

#Check all of the neighbors around the tile you left clicked on and count the mines.        
def check_neighbors(coordinate):
    mine_counter=0
    for dx, dy in [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]: #iterate through adjacent cells
        if(0 <= (coordinate[0]+dx) < X_TILES and 0 <= (coordinate[1]+dy) < Y_TILES): #check boundaries
            if(check_if_mine((coordinate[0]+dx,coordinate[1]+dy))):
                mine_counter += 1
    return mine_counter        
        
#Randomly generate the mines.
def generate_mines(mine_quantity):
    global state
    i = 0
    while(i < mine_quantity):
        x = random.randint(0,X_TILES-1)
        y = random.randint(0,Y_TILES-1)
        if(state[x][y][1] is 0):
            state[x][y][1] = 10
            print("(", x, ",", y, ")")
            i += 1
        else:
            pass
    
#populate the 3d list that contains data about the board.    
def populate_state():
    global state
    for x in range(X_TILES):
            for y in range(Y_TILES):
                if(state[x][y][1] !=10):
                    state[x][y][1] = check_neighbors((x, y))

#Uncover all bombs and lock the screen up if the game is lost                    
def lost_the_game():
    global LOST_GAME
    LOST_GAME = True
    for x in range(X_TILES):
        for y in range(Y_TILES):
            if(check_if_mine((x,y))):
                uncover_tile((x, y))
                
#Below are the initializations and main loop
generate_mines(MINES)
populate_state()
pygame.init()
pygame.display.set_caption('Minesweeper')
FPSCLOCK = pygame.time.Clock()

#Initialize the board with blank tiles
def reinit():
    global LOST_GAME
    LOST_GAME = False
    for x in range(X_TILES):
        for y in range(Y_TILES):
            GAME_SURFACE.blit(NORMAL_TILE, (x*TILE_SIZE, y*TILE_SIZE + SMILEY_SIZE))
    '''for x in range(X_TILES):
        for y in range(Y_TILES):
            uncover_tile((x, y))'''      
    GAME_SURFACE.blit(SMILEY, ((X_TILES*TILE_SIZE)/2 - SMILEY_SIZE/2, 0))
    remaining_mines = MINES

#Below is the main loop
reinit()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type is  MOUSEBUTTONDOWN and event.button is LEFT:
            left_click(get_tile(event.pos))
        elif event.type is  MOUSEBUTTONDOWN and event.button is RIGHT:
            right_click(get_tile(event.pos))                
    pygame.display.update() 
    FPSCLOCK.tick(FPS)           

 