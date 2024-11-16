''' the module containing the implementation of the A* algorithm '''

import pygame
from queue import PriorityQueue # a efficient way to get the minimum element form a set
from modules.distance_formulas import h # We use the manhattan distance as we cant move diagonal so the additional calculation of the euclidean distance is not needed
from modules.path_reconstructer import reconstruct_path

# Description: 
#   A* is an informed search algorithm that finds the shortest path between nodes by using both the actual cost from the start (g score)
#   and an estimated cost to the goal (h score). This combination helps prioritize paths that appear closer to the goal.

# Features:
#   Heuristics: Utilizes a heuristic function (h score) to estimate the cost from a node to the goal, along with the actual path cost (g score), combining them to form the f score.
#   Open Set: Maintains nodes to be evaluated in a priority queue, prioritized by their f score.

# Pros:
#   Efficient pathfinding, especially when a good heuristic is used, as it can guide the search towards the goal more directly.
#   Guarantees the shortest path if the heuristic is admissible (does not overestimate the true cost).

# Cons:
#   The efficiency is dependent on the quality of the heuristic; a poor heuristic can lead to inefficiency.
#   More complex to implement, particularly in choosing and designing an appropriate heuristic function.

# using:
#   1. Open Set: Nodes to be evaluated.
#   2. Closed Set: Nodes already evaluated.
#   3. g Score: Cost from the start node to a node.
#   4. h Score: Heuristic estimate from a node to the goal.
#   5. f Score: g+h (total estimated cost).

# Steps:
#   1. Add the start node to the open set.
#   2. While the open set is not empty:
#       1. Remove the node with the lowest f score.
#       2. If it’s the goal node, return the path.
#       3. Generate neighbors, calculate their g, h and f scores
#       4. Add unvisited neighbors to the open set.
#       5. Move the node to the closed set.

def a_star(draw, grid, start, end):
    '''  A* is an informed search algorithm that finds the shortest path between nodes by using both the actual cost from the start (g score)
        and an estimated cost to the goal (h score). This combination helps prioritize paths that appear closer to the goal. Guarantees the shortest path if the heuristic is admissible (does not overestimate the true cost). '''
    count = 0
    open_set = PriorityQueue() # defining the open set
    open_set.put((0, count, start))
    came_from = {} # the path that the algorithm has taken
    
    g_score = {spot: float("inf") for row in grid for spot in row} # the cost of getting to the start spot
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row} # the cost of getting to the end spot
    f_score[start] = h(start.get_pos(), end.get_pos()) # the heuristic function
    
    open_set_hash = {start} # the open set in the form of a hash table
    
    while not open_set.empty(): # to run the algorithm until the open set is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] # 2 is the index of the node after the g and f scores
        open_set_hash.remove(current) # synchronizing to prevent duplicates
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end() # redraw the end color
            start.make_start() # redraw the start color
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]: # checking if the new path is better
                came_from[neighbor] = current # updating the path
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash: # if the neighbor is not in the open set, add it
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    
        draw()
        
        if current != start:  # if current is not the start node, make it closed
            current.make_closed()
            
    return False # if we did not find a path