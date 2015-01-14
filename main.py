"""A minesweeper clone written with Pygame."""

import pygame
import sys

from pygame.locals import *

x_tiles = 20
y_tiles = 20
mines = 50

#Load all of the tile images
normal_tile = pygame.image.load("NormalTile.png")
smiley = pygame.image.load("Smiley.png")
clicked_tile = []
for i in range(9):
    clicked_tile.append(pygame.image.load("ClickedTile%d.png" % i))


pygame.init()
game_surface = pygame.display.set_mode((x_tiles*25, y_tiles*25 + 40))
pygame.display.set_caption('Minesweeper')


#Initialize the board with blank tiles
for x in range(x_tiles):
    for y in range(y_tiles):
        game_surface.blit(normal_tile, (x*25, y*25 + 40))
game_surface.blit(smiley, ((x_tiles*25)/2 - 20, 0))

        
        
        
        
        
#Below is the main loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()        