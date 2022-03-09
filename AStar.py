from math import inf, sqrt
from operator import ne
from Maze import *
import time

#https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all

def AStar_FindPath(maze: Maze) -> None:
    # set the start time
    startTime = time.time()
    visited = [] # list of visited cells
    unvisited = [] # list of unvisited cells
    gScores = {} # g scores for each cell (distance between start and each cell)
    fScores = {} # f scores for each cell (distance between start and end through each cell (f = g + h) h is distance between cell and end point)
    prevs = {} # previous and parent cells for each cell
    shortestPath = [] # the shortest path found
    start = maze.start # start point in the maze
    end = maze.end # end point in the maze

    # add all of the cells to the unvisited list and set their g and f scores to infinite, and their parents to none
    for c in maze.get_Cells():
        unvisited.append(c)
        gScores[c] = inf
        fScores[c] = inf
        prevs[c] = None

    # set start's cell g-score to 0
    gScores[start] = 0
    # f score from start to end
    fScores[start] = calc_distance(start, end)

    current = None

    while unvisited:
        # sort the f score dictionary by value ascending
        fScores = {k: v for k, v in sorted(fScores.items(), key=lambda item: item[1])}
        
        # if the minimum value in distance dictionary is in the queue set that as current cell
        for k in fScores.keys():
            if k in unvisited:
                current = k
                break

        # if current cell is neither start point nor end point set its cell as searching
        if current != start and current != end:
            maze.grid[current[0]][current[1]] = Searching(current[0],current[1], maze)
            maze.update(maze.grid[current[0]][current[1]])
        # if current cell is end point stop searching
        if current == end: 
            break
        # else search through the unvisited cell to find the shortest path
        else:
            # check the g score for each neighbor
            for n in maze.get_neighbors(current):
                # if neighbor is not visited
                if n not in visited:
                    # calculate a its g-score
                    g = calc_distance(start, n)
                    # if the new g-score is less than g-score in the dictionary and the neighbor is not visited
                    if g < gScores[n] and n in unvisited:
                        # update its g-score
                        gScores[n] = g
                        # update its f-score
                        fScores[n] = g + calc_distance(n, end)
                        # set current cell as its parent
                        prevs[n] = current
            # add current cell to visited
            visited.append(current)
            # remove current cell from unvisited
            unvisited.remove(current)
    
    # set the current cell as the end point and track back the shortest path to the start point
    current = end
    # if current cell has a parent and current is not start point
    if prevs[current] is not None or current is start:
        
        while current is not None:
            # insert current to the shortest path list
            shortestPath.insert(0, current)
            # set current's parent as current
            current = prevs[current]

    # get end time
    endTime = time.time()
    # draw the planned path
    maze.draw_path(shortestPath, endTime - startTime)
    print(shortestPath)

# calculate the distance between current cell and the given cell
def calc_distance(current: Tuple[int,int], cell: Tuple[int,int]) -> float:
    distance = sqrt((cell[0] - current[0])**2 + (cell[1] - current[1]) ** 2)
    return distance
    


