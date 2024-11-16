''' this module contains the implementation of the dijkstra's algorithm '''

import pygame
from queue import PriorityQueue # a efficient way to get the minimum element form a set
from modules.path_reconstructer import reconstruct_path

# Description: 
#   Dijkstra's algorithm is a pathfinding algorithm used to find the shortest path between nodes in a graph. 
#   It works by exploring all possible paths from the start node, prioritizing paths with the lowest accumulated cost 
#   until the goal is reached.

# Features:
#   Heuristics: Does not use a heuristic; relies solely on the actual path cost (g score).
#   Open Set: Maintains nodes to be evaluated in a priority queue based on their g score.

# Pros:
#   Guarantees the shortest path in graphs with non-negative weights.
#   Simple and can be applied to both unweighted and weighted graphs.

# Cons:
#   Can be slow and inefficient for large graphs due to exhaustive exploration.
#   Not as fast as others like A* for specific searches since it doesn't use heuristics to guide the search.

# using:
#   1. Open Set: Nodes to be evaluated, stored in a priority queue.
#   2. g Score: The cost from the start node to a node.

# Steps:
#   1. Add the start node to the open set with a g score of 0.
#   2. While the open set is not empty:
#       1. Remove the node with the lowest g score.
#       2. If it’s the goal node, reconstruct and return the path.
#       3. For each neighbor of the current node:
#           1. Calculate the tentative g score.
#           2. If the tentative g score is lower than the current g score:
#               1. Update the g score.
#               2. Record the current node as the predecessor of the neighbor.
#           3. If the neighbor is not in the open set, add it.

# Note: This is equivalent to BFS when all the weights are equal to 1.

def dijkstra(draw, grid, start, end):
    ''' Dijkstra's algorithm is a pathfinding algorithm used to find the shortest path between nodes in a graph. 
    It works by exploring all possible paths from the start node, prioritizing paths with the lowest accumulated cost 
    until the goal is reached. Guarantees the shortest path in graphs with non-negative weights.
    '''
    count = 0
    open_set = PriorityQueue() # Priority queue for the open set
    open_set.put((0, count, start))
    came_from = {} # Dictionary to store the path

    g_score = {spot: float("inf") for row in grid for spot in row} # Distance to start node
    g_score[start] = 0
    
    open_set_hash = {start} # Set to keep track of items in the priority queue

    while not open_set.empty(): # Continue until open set is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # Get the node with the lowest cost
        open_set_hash.remove(current)

        if current == end: # If the goal is reached, reconstruct the path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # The cost from the start node to the neighbor

            if temp_g_score < g_score[neighbor]: # If a shorter path to the neighbor is found
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash: # Add neighbor to open set if not already present
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:  # Mark the current node as visited
            current.make_closed()

    return False # If no path is found