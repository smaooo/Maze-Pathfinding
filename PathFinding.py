from Maze import *
import os
import pygame
from pygame.locals import *


WINSIZE = (Cell.w * 41, Cell.h * 41)


if __name__ == '__main__':

    maze = Maze(WINSIZE)

    input()