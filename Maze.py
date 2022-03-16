from ctypes import sizeof
import pygame
from random import choice
from pygame import Surface
from typing import List, Tuple
import os

# https://gist.github.com/FrankRuis/4bad6a988861f38cf53b86c185fc50c3

# parent class for all of the cells
class Cell(pygame.sprite.Sprite):
    # the size of each cell
    w, h = 16, 16

    def __init__(self, x : int, y : int, maze) -> None: 
        pygame.sprite.Sprite.__init__(self)
        # Define the visual settings of the cell
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.w
        self.rect.y = y * self.h

        self.x = x
        self.y = y
        self.maze = maze
        # define the neighbors of the cell
        self.nbs = [(x + nx, y + ny) for nx, ny in ((-2, 0), (0, -2), (2, 0), (0, 2))
                    if 0 <= x + nx < maze.w and 0 <= y + ny < maze.h]

    # draw the cell
    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)


# Wall class inhereted from Cell
class Wall(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        # define the look of the Wall cell
        super(Wall, self).__init__(x, y, maze)
        self.image.fill((0, 0, 0))
        self.type = 0


class StartPoint(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        # define the look of the StartPoint cell
        super().__init__(x, y, maze)
        self.image.fill((0,255,0))
        self.type = 1


class EndPoint(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        # define the look of the EndPoint cell
        super().__init__(x, y, maze)
        self.image.fill((255,0,0))
        self.type = 2

class Searching(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        # define the look of the Serching cell
        super().__init__(x, y, maze)
        self.image.fill((0,0,255))
        self.type = 2

class Path(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        # define the look of the Path cell
        super().__init__(x, y, maze)
        self.image.fill((255,0,0))
        self.type = 3


class Maze:
    def __init__(self, size) -> None:
        # define the size of the maze
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h
        # define the grid a 2d array of walls and later we'll add cells on top of them
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]
        
        self.start: Tuple(int,int) # start point
        self.end: Tuple(int,int) # end point
        # initialize pygame
        pygame.init()

        # setup the window
        self.screen = pygame.display.set_mode(size)
        self.size = size

        pygame.display.set_caption('Maze')
        # set the background
        self.screen.fill((0, 0, 0))
        # generate the maze
        self.generate(self.screen)

    # get a cell in the grid
    def get(self, x : int, y : int ) -> List: 
        return self.grid[x][y]

    # draw the maze
    def draw(self, screen: Surface) -> None:
        # for each cell in the grid call the draw function
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    # set the start and the end points 
    def setStartEnd(self, point: int) -> None:

        # define the range for the row and the column according to the point that is currently being set
        frange1 = 0 if point == 0 else self.w
        erange1 = 0 if point == 1 else self.w
        frange2 = 0 if point == 0 else self.h
        erange2 = 0 if point == 1 else self.h
        # define the step for the range
        step = 1 if point == 0 else -1 
        # define the increment value, so that if looking for end the start number is incremented
        increment = 1 if point == 1 else 0
        
        # look for a cell in the grid that is not assigned to start or end and it's block by walls from three side
        for x in range(frange1 - increment,erange1, step):
            for y in range(frange2 - increment, erange2, step):
                # if the current cell is not Wall and it's not the start point
                if (type(self.grid[x][y]) is not Wall and type(self.grid[x][y]) is not StartPoint):
                    # if only the right side of the cell is not blocked
                    if (type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x][y-1]) is Wall and 
                    type(self.grid[x-1][y]) is Wall):
                        self.set_cell(x,y,point)

                        return
                    # if only the cell is not blocked from top
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y-1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        self.set_cell(x,y,point)
                        return
                    # if only the cell is not blocked from bottom
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        self.set_cell(x,y,point)
                        return
                    # if only the cell is not blocked from left
                    elif (type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall):
                        self.set_cell(x,y,point)
                        return

    # set the cell as the start or the end point        
    def set_cell(self, x: int, y: int, point: int) -> None: 
        # if looking for start point
        if point == 0:
            # set the cell as start point
            self.grid[x][y] = StartPoint(x,y,self)
            # set the the start variable
            self.start = (x,y)
            # call the function recursively to set the end point
            self.setStartEnd(1)
        # if looking for end point
        else:
            # set the cell as end point
            self.grid[x][y] = EndPoint(x,y,self)
            # set the end variable
            self.end = (x,y)
        
    # update the cell with a new point
    def update(self, cell: Cell) -> None:
        
        cell.draw(self.screen)
        pygame.display.update()
        pygame.event.pump()

    # reset the maze
    def reset(self) -> None:
        # set all of the cells that are not walls to normal cells
        for x in range(self.w):
            for y in range(self.h):
                c = self.grid[x][y]
                if type(c) is not Wall and type(c) is not StartPoint and type(c) is not EndPoint:
                    self.grid[x][y] = Cell(x,y,self)
        # set the start point
        self.grid[self.start[0]][self.start[1]] = StartPoint(self.start[0], self.start[1], self)
        # set the end point
        self.grid[self.end[0]][self.end[1]] = EndPoint(self.end[0], self.end[1], self)
        # draw the maze
        self.draw(self.screen)
        pygame.time.wait(100)
    
    # draw the planned path
    def draw_path(self, path, time):
        # set the cells on the path as a path cell
        for p in path:
            if p != self.start and p != self.end:
                self.grid[p[0]][p[1]] = Path(p[0],p[1], self)
                self.grid[p[0]][p[1]].draw(self.screen)
                pygame.display.update()
                
                pygame.event.pump()

        # add a text to the center of the screen to show the spent time
        font = pygame.font.Font('freesansbold.ttf', 32)
        green = (0, 160, 0)
        white = (255, 255, 255)
        text = font.render(str(time), True, green, white)
        textRect = text.get_rect()
        textRect.center = (self.size[0] // 2, self.size[1] // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()

    # get the all of the cells as tuples of x and y
    def get_Cells(self) -> List[Tuple[int,int]]:
        cells = []
        for x in range(self.w):
            for y in range(self.h):
                if type(self.grid[x][y]) is not Wall:
                    cells.append((x,y))

        return cells

    # get the neighbors of the given list
    def get_neighbors(self, cell: Tuple[int,int]) -> List[Tuple[int,int]]:
        neighbors: list = []
        # Check if the neighbor cell is not wall
        if cell[0] - 1 >= 0 and type(self.grid[cell[0]-1][cell[1]]) is not Wall:
            neighbors.append((cell[0] - 1, cell[1]))
        if cell[0] + 1 < self.w and type(self.grid[cell[0]+1][cell[1]]) is not Wall:
            neighbors.append((cell[0] + 1, cell[1]))
        if cell[1] - 1 >= 0 and type(self.grid[cell[0]][cell[1]-1]) is not Wall:
            neighbors.append((cell[0], cell[1] - 1))
        if cell[1] + 1 >= 0 and type(self.grid[cell[0]][cell[1]+1]) is not Wall:
            neighbors.append((cell[0], cell[1] + 1))
        
        return neighbors

    # generate the maze using recursive backtracking
    def generate(self, screen: Surface=None) -> None:
        # create a list of all of the unvisited cells
        unvisited = [c for r in self.grid for c in r if c.x % 2 and c.y % 2]
        # set the last element in unvisited list as current
        cur = unvisited.pop()
        # stack to hold current and visit the neighbors
        stack = []
        
        while unvisited:
            try:
                # choose randomly one of the neighbors of the current cell
                n = choice([c for c in map(lambda x: self.get(*x), cur.nbs) if c in unvisited])
                # add current cell to stack
                stack.append(cur)
                # calculate x and y of the neighbor on the screen
                nx, ny = cur.x - (cur.x - n.x) // 2, cur.y - (cur.y - n.y) // 2
                # set the neighbor as cell
                self.grid[nx][ny] = Cell(nx, ny, self)
                # set current as cell
                self.grid[cur.x][cur.y] = Cell(cur.x, cur.y, self)
                # set the neighbor as current
                cur = n
                # remove neighbor from the unvisited list
                unvisited.remove(n)

            # if there's an index error get set the first element of the stack as current because
            # it went beyond the borders
            except IndexError:
                if stack:
                    cur = stack.pop()
        # set the start and the end point
        self.setStartEnd(0)
        # draw the maze
        self.draw(screen)
        pygame.display.update()
            
