from ctypes import sizeof
import pygame
from random import choice
from pygame import Surface
from typing import List, Tuple
import os
import pygame_gui
# https://gist.github.com/FrankRuis/4bad6a988861f38cf53b86c185fc50c3



class Cell(pygame.sprite.Sprite):
    w, h = 16, 16

    def __init__(self, x : int, y : int, maze) -> None: 
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([self.w, self.h])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.w
        self.rect.y = y * self.h

        self.x = x
        self.y = y
        self.maze = maze
        self.nbs = [(x + nx, y + ny) for nx, ny in ((-2, 0), (0, -2), (2, 0), (0, 2))
                    if 0 <= x + nx < maze.w and 0 <= y + ny < maze.h]

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)


class Wall(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        super(Wall, self).__init__(x, y, maze)
        self.image.fill((0, 0, 0))
        self.type = 0

class StartPoint(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        super().__init__(x, y, maze)
        self.image.fill((0,255,0))
        self.type = 1

class EndPoint(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        super().__init__(x, y, maze)
        self.image.fill((255,0,0))
        self.type = 2

class Searching(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        super().__init__(x, y, maze)
        self.image.fill((0,0,255))
        self.type = 2

class Path(Cell):
    def __init__(self, x: int, y: int, maze) -> None:
        super().__init__(x, y, maze)
        self.image.fill((255,0,0))
        self.type = 3

class Maze:
    def __init__(self, size) -> None:
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]
        self.start: Tuple(int,int)
        self.end: Tuple(int,int)
        pygame.init()
        self.clock = pygame.time.Clock()
        scr_inf = pygame.display.Info()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(scr_inf.current_w // 2 - size[0] // 2,
                                                         scr_inf.current_h // 2 - size[1] // 2)
        self.screen = pygame.display.set_mode(size)
        self.size = size
        pygame.display.set_caption('Maze')
        self.screen.fill((0, 0, 0))
        self.wall = []
        print(self.grid[0][0])
        self.generate(self.screen, False)

    def get(self, x : int, y : int ) -> List: 
        return self.grid[x][y]

    def place_wall(self, x : int, y : int) -> None:
        self.grid[x][y] = Wall(x, y, self)

    def draw(self, screen: Surface) -> None:
        for row in self.grid:
            for cell in row:
                cell.draw(screen)


    def setStartEnd(self, point: int) -> None:
        
        frange1 = 0 if point == 0 else self.w
        erange1 = 0 if point == 1 else self.w
        frange2 = 0 if point == 0 else self.h
        erange2 = 0 if point == 1 else self.h
        step = 1 if point == 0 else -1 
        increment = 1 if point == 1 else 0
        print(str(frange1) + ' '+ str(erange1))
        print(str(frange2) + ' '+ str(erange2))
        for x in range(frange1 - increment,erange1, step):
            for y in range(frange2 - increment, erange2, step):
                if (type(self.grid[x][y]) is not Wall and type(self.grid[x][y]) is not StartPoint):
                    if (type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x][y-1]) is Wall and 
                    type(self.grid[x-1][y]) is Wall):
                        if (point == 0):
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.start = (x,y)
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.end = (x,y)
                            self.grid[x][y] = EndPoint(x,y,self)

                        return
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y-1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        if (point == 0):
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.start = (x,y)

                            print('Start: ' + str(x) + ' ' + str(y))
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.end = (x,y)
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        if (point == 0):
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.start = (x,y)
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.end = (x,y)
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
                    elif (type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall):
                        if (point == 0):
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.start = (x,y)
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.end = (x,y)
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
            
    def update(self, cell: Cell):
        
        cell.draw(self.screen)
        pygame.display.update()
        # pygame.time.wait(1)
        pygame.event.pump()

    def reset(self):
        for x in range(self.w):
            for y in range(self.h):
                c = self.grid[x][y]
                if type(c) is not Wall and type(c) is not StartPoint and type(c) is not EndPoint:
                    self.grid[x][y] = Cell(x,y,self)
        self.grid[self.start[0]][self.start[1]] = StartPoint(self.start[0], self.start[1], self)
        self.grid[self.end[0]][self.end[1]] = EndPoint(self.end[0], self.end[1], self)
        self.draw(self.screen)
        pygame.time.wait(100)
                    
    def draw_path(self, path, time):
        for p in path:
            if p != self.start and p != self.end:
                self.grid[p[0]][p[1]] = Path(p[0],p[1], self)
                self.grid[p[0]][p[1]].draw(self.screen)
                pygame.display.update()
                # pygame.time.wait(1)
                pygame.event.pump()

        font = pygame.font.Font('freesansbold.ttf', 32)
 
        green = (0, 255, 0)
        blue = (0, 0, 128)
        text = font.render(str(time), True, green, blue)
        textRect = text.get_rect()


        textRect.center = (self.size[0] // 2, self.size[1] // 2)

        self.screen.blit(text, textRect)
        pygame.display.update()

    def get_Cells(self):
        cells = []
        for x in range(self.w):
            for y in range(self.h):
                if type(self.grid[x][y]) is not Wall:
                    cells.append((x,y))

        return cells

    def get_neighbors(self, cell: Tuple[int,int]) -> List[Tuple[int,int]]:
        neighbors: list = []
        if cell[0] - 1 >= 0 and type(self.grid[cell[0]-1][cell[1]]) is not Wall:
            neighbors.append((cell[0] - 1, cell[1]))
        if cell[0] + 1 < self.w and type(self.grid[cell[0]+1][cell[1]]) is not Wall:
            neighbors.append((cell[0] + 1, cell[1]))
        if cell[1] - 1 >= 0 and type(self.grid[cell[0]][cell[1]-1]) is not Wall:
            neighbors.append((cell[0], cell[1] - 1))
        if cell[1] + 1 >= 0 and type(self.grid[cell[0]][cell[1]+1]) is not Wall:
            neighbors.append((cell[0], cell[1] + 1))
        
        return neighbors

        
    def generate(self, screen: Surface=None, animate: bool=False) -> None:
        unvisited = [c for r in self.grid for c in r if c.x % 2 and c.y % 2]
        cur = unvisited.pop()
        stack = []
        
        while unvisited:
            try:
                n = choice([c for c in map(lambda x: self.get(*x), cur.nbs) if c in unvisited])
                stack.append(cur)
                
                nx, ny = cur.x - (cur.x - n.x) // 2, cur.y - (cur.y - n.y) // 2
                self.grid[nx][ny] = Cell(nx, ny, self)
                self.grid[cur.x][cur.y] = Cell(cur.x, cur.y, self)
                cur = n
                unvisited.remove(n)


                if animate:
                    self.draw(screen)
                    pygame.display.update()
                    # pygame.time.wait(10)
            except IndexError:
                if stack:
                    cur = stack.pop()
        self.setStartEnd(0)
        if not animate:
            self.draw(screen)
            pygame.display.update()
            
