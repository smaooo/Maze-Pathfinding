from dis import dis
from Maze import *
from math import inf, sqrt
from typing import Tuple, List, Dict

# https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html


def Dij_FindPath(maze : Maze):

    queue = []
    dist = {}
    prev = {}
    shortestPath = []
    start = maze.start
    end = maze.end
    
    for cell in maze.get_Cells():
        dist[cell] = inf
        prev[cell] = None
        queue.append(cell)

    dist[start] = 0
    current = start

    while queue:
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        
        for k in dist.keys():
            if k in queue:
                current = k
                break
        if current != start and current != end:
            maze.grid[current[0]][current[1]] = Searching(current[0],current[1], maze)
            maze.update(maze.grid[current[0]][current[1]])
        queue.remove(current)
        neighbors = maze.get_neighbors(current)
        for neighbor in neighbors:
            
            if neighbor in queue and dist[current] + calc_distance(current, neighbor) < dist[neighbor]:
                dist[neighbor] = dist[current] + calc_distance(current, neighbor)
                prev[neighbor] = current
        
        if current == end:
            break
    
    current = end
    if prev[current] is not None or current is start:
        while current is not None:
            shortestPath.insert(0, current)
            current = prev[current]
    maze.draw_path(shortestPath)
    print(shortestPath)
    
def calc_distance(current: Tuple[int,int], cell: Tuple[int,int]) -> float:
    distance = sqrt((cell[0] - current[0])**2 + (cell[1] - current[1]) ** 2)
    return distance
    
