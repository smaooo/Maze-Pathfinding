from Maze import *
from Dijkstra import *
from AStar import *
import pygame
from pygame.locals import *

# define the window size
WINSIZE = (Cell.w * 91, Cell.h * 51)

if __name__ == '__main__':

    # create the maze and open the pygame window
    maze = Maze(WINSIZE)
    

    done = 1
    while done:
        
        for e in pygame.event.get():
            # if 1 is pressed run Dijkstra algorithm on the maze
            if e.type == KEYUP and e.key == K_1:
                # reset maze if it's already planned for a path
                maze.reset()
                # run the algorithm
                Dij_FindPath(maze)
                break
            # if 2 is pressed run A* algorithm on the maze
            elif e.type == KEYUP and e.key == K_2:
                # reset maze if it's already planned for a path
                maze.reset()
                # run the algorithm
                AStar_FindPath(maze)
            # generate a new maze
            elif e.type == KEYUP and e.key == K_r:
                maze = Maze(WINSIZE)
                break
            # terminate the program
            elif e.type == KEYUP and e.key == K_ESCAPE:
                done = 0
                break  