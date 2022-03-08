
import pygame
from random import choice


class Cell(pygame.sprite.Sprite):
    w, h = 16, 16

    def __init__(self, x, y, maze):
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Wall(Cell):
    def __init__(self, x, y, maze):
        super(Wall, self).__init__(x, y, maze)
        self.image.fill((0, 0, 0))
        self.type = 0

class StartPoint(Cell):
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze)
        self.image.fill((0,255,0))
        self.type = 1

class EndPoint(Cell):
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze)
        self.image.fill((255,0,0))
        self.type = 2

class Maze:
    def __init__(self, size):
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]
        pygame.init()
        scr_inf = pygame.display.Info()
       
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Maze')
        self.screen.fill((0, 0, 0))
        self.wall = []

        self.generate(self.screen, False)

    def get(self, x, y):
        return self.grid[x][y]

    def place_wall(self, x, y):
        self.grid[x][y] = Wall(x, y, self)

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    def setStartEnd(self, point: int):
        
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
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = EndPoint(x,y,self)

                        return
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y-1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        if (point == 0):
                            self.grid[x][y] = StartPoint(x,y,self)
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
                    elif (type(self.grid[x-1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall):
                        if (point == 0):
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
                    elif (type(self.grid[x][y+1]) is Wall and
                    type(self.grid[x+1][y]) is Wall and
                    type(self.grid[x][y+1]) is Wall):
                        if (point == 0):
                            print('Start: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = StartPoint(x,y,self)
                            self.setStartEnd(1)
                        elif (point == 1) :
                            print('End: ' + str(x) + ' ' + str(y))
                            self.grid[x][y] = EndPoint(x,y,self)
                        return
            
        
        
    def generate(self, screen=None, animate=False):
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


