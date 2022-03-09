from Maze import *
from Dijkstra import *
from AStar import *
import pygame
from pygame.locals import *
import pygame_gui

WINSIZE = (Cell.w * 41, Cell.h * 41)

if __name__ == '__main__':

    maze = Maze(WINSIZE)
    

    done = 1
    while done:
        
        for e in pygame.event.get():
            if e.type == KEYUP and e.key == K_1:
                maze.reset()
                Dij_FindPath(maze)
                break
            elif e.type == KEYUP and e.key == K_2:
                maze.reset()
                
                AStar_FindPath(maze)

            elif e.type == KEYUP and e.key == K_r:
                maze = Maze(WINSIZE)
                break
            elif e.type == KEYUP and e.key == K_ESCAPE:
                done = 0
                break  