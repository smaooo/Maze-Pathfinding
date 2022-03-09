from math import inf, sqrt
from operator import ne
from Maze import *
import time

#https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all

def AStar_FindPath(maze: Maze) -> None:
    startTime = time.time()
    visited = []
    unvisited = []
    gScores = {}
    fScores = {}
    prevs = {}
    shortestPath = []
    start = maze.start
    end = maze.end

    for c in maze.get_Cells():
        unvisited.append(c)
        gScores[c] = inf
        fScores[c] = inf
        prevs[c] = None
    
    gScores[start] = 0
    fScores[start] = calc_distance(start, end)

    finished = False
    current = None
    while not finished:
        fScores = {k: v for k, v in sorted(fScores.items(), key=lambda item: item[1])}
    
        for k in fScores.keys():
            if k in unvisited:
                current = k
                break

        if current != start and current != end:
            maze.grid[current[0]][current[1]] = Searching(current[0],current[1], maze)
            maze.update(maze.grid[current[0]][current[1]])
        if current == end: 
            finished = True
            #Copy the values for the current node from the unvisited list to the visited list
        else:
            for n in maze.get_neighbors(current):
                if n not in visited:
                    g = calc_distance(start, n)
                    if g < gScores[n] and n in unvisited:
                        gScores[n] = g
                        fScores[n] = g + calc_distance(n, end)
                        prevs[n] = current
            visited.append(current)
            unvisited.remove(current)
    current = end
    if prevs[current] is not None or current is start:
        while current is not None:
            shortestPath.insert(0, current)
            current = prevs[current]

    endTime = time.time()
    maze.draw_path(shortestPath, endTime - startTime)
    print(shortestPath)


def calc_distance(current: Tuple[int,int], cell: Tuple[int,int]) -> float:
    distance = sqrt((cell[0] - current[0])**2 + (cell[1] - current[1]) ** 2)
    return distance
    


