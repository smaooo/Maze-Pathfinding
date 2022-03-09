from dis import dis
from Maze import *
from math import inf, sqrt
from typing import Tuple, List, Dict
import time
# https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html


def Dij_FindPath(maze : Maze):
    # set the start time
    startTime = time.time()
    queue = [] # queue for unvisited cells
    dist = {} # distance from the start point to each cell
    prev = {} # previous or parent cell of a cell
    shortestPath = [] # shortest path as the outcome of the search
    start = maze.start # start point
    end = maze.end # end point
    
    # for each cell in the maze set the distance to infinite and the previous cell to none, and add that to the queue
    for cell in maze.get_Cells():
        dist[cell] = inf
        prev[cell] = None
        queue.append(cell)

    # set the distance for the start node to 0
    dist[start] = 0

    # as long as there's cells in the unvisited queue    
    while queue:
        # order the distance dictionary by value ascending
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        
        # if the minimum value in distance dictionary is in the queue set that as current cell
        for k in dist.keys():
            if k in queue:
                current = k
                break
        # if current cell is neither start point nor end point set its cell as searching
        if current != start and current != end:
            maze.grid[current[0]][current[1]] = Searching(current[0],current[1], maze)
            maze.update(maze.grid[current[0]][current[1]])
        
        # remove the current cell from unvisited queue
        queue.remove(current)

        # check the distance between start point and each neighbor
        for neighbor in maze.get_neighbors(current):
            # if neighbor is unvisited and the calculated distance between start and neighbor is less than its current distance
            if neighbor in queue and dist[current] + calc_distance(current, neighbor) < dist[neighbor]:
                # update its distance
                dist[neighbor] = dist[current] + calc_distance(current, neighbor)
                # set the current as the neighbor's parent 
                prev[neighbor] = current

        # if current cell is the end point stop searching
        if current == end:
            break
    
    # set the current cell as the end point and track back the shortest path to the start point
    current = end
    # if current cell has a parent and it's not the start point
    if prev[current] is not None or current is start:
        # as long as current cell is not none
        while current is not None:
            # insert the cell into the list
            shortestPath.insert(0, current)
            # update the current cell with the parent
            current = prev[current]

    # get the end time
    endTime = time.time()
    # draw the planned path
    maze.draw_path(shortestPath, endTime - startTime)
    print(shortestPath)
    
# calculate the distance between current cell and the given cell
def calc_distance(current: Tuple[int,int], cell: Tuple[int,int]) -> float:
    distance = sqrt((cell[0] - current[0])**2 + (cell[1] - current[1]) ** 2)
    return distance
    
