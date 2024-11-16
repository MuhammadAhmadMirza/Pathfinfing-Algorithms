import pygame
from queue import PriorityQueue
from modules.distance_formulas import h  # Manhattan distance heuristic
from modules.path_reconstructer import reconstruct_path

# Description:
#   Theta* is an optimization technique for A* pathfinding that introduces more direct paths by allowing shortcuts 
#   when traversing between nodes. It refines A* by permitting straight-line paths when they provide a better route, 
#   which can lead to more optimal paths in certain scenarios.
#
# Features:
#   Heuristics: Uses Manhattan distance heuristic to estimate the cost from the current node to the goal.
#   Shortcuts: Enables direct connections between nodes if they improve the path efficiency, allowing for straight-line 
#              paths when they are beneficial.
#
# Pros:
#   Can find shorter and more efficient paths compared to standard A* by allowing direct connections.
#   Retains the optimality and completeness of A* while potentially enhancing performance with better pathfinding.
#
# Cons:
#   More complex implementation due to the need to validate and manage direct connections between nodes.
#   Performance gains might be less significant in highly complex or dense grids where shortcuts are less effective.
#
# Steps:
#   1. Add the start node to the open set with an initial cost of 0.
#   2. While the open set is not empty:
#       1. Remove the node with the lowest f score (g + h).
#       2. If it’s the goal node, reconstruct and return the path.
#       3. For each neighbor:
#           1. Update the g score and f score for the neighbor.
#           2. If the neighbor is not in the open set, add it.
#           3. Validate potential shortcuts by checking if a direct path from the current node to a neighbor is valid and improves the path.


def theta_star(draw, grid, start, end):
    ''' Theta* is an optimization technique for A* pathfinding that introduces more direct paths by allowing shortcuts 
        when traversing between nodes. It refines A* by permitting straight-line paths when they provide a better route, 
        which can lead to more optimal paths in certain scenarios. '''
    
    def get_neighbors(node):
        ''' Get the neighbors of a node considering the grid and diagonals '''
        neighbors = []
        x, y = node.get_pos()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                    break
                neighbor = grid[nx][ny]
                if neighbor.is_barrier():
                    break
                neighbors.append(neighbor)
                if (nx, ny) == end.get_pos():
                    break
        return neighbors
    
    def spot_key(spot):
        ''' Generate a unique key for each spot based on its position '''
        return (spot.get_pos(), id(spot))
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {spot_key(spot): float("inf") for row in grid for spot in row}
    g_score[spot_key(start)] = 0
    f_score = {spot_key(spot): float("inf") for row in grid for spot in row}
    f_score[spot_key(start)] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {spot_key(start)}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(spot_key(current))
        
        if current == end:
            # Reconstruct the path from the goal to the start
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            
            # Ensure the entire path is marked as path
            path = [end]
            while path[-1] in came_from:
                path.append(came_from[path[-1]])
            path.reverse()
            
            for spot in path:
                spot.make_path()
            
            # Mark all intermediate nodes between path nodes
            for i in range(len(path) - 1):
                x1, y1 = path[i].get_pos()
                x2, y2 = path[i + 1].get_pos()
                
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                sx = 1 if x1 < x2 else -1
                sy = 1 if y1 < y2 else -1
                err = dx - dy

                while True:
                    if not grid[x1][y1].is_path() and not grid[x1][y1].is_barrier():
                        grid[x1][y1].make_path()
                    if x1 == x2 and y1 == y2:
                        break
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x1 += sx
                    if e2 < dx:
                        err += dx
                        y1 += sy
            
            draw()
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in get_neighbors(current):
            temp_g_score = g_score[spot_key(current)] + 1
            
            if temp_g_score < g_score[spot_key(neighbor)]:
                came_from[neighbor] = current
                g_score[spot_key(neighbor)] = temp_g_score
                f_score[spot_key(neighbor)] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if spot_key(neighbor) not in open_set_hash:
                    count += 1
                    open_set.put((f_score[spot_key(neighbor)], count, neighbor))
                    open_set_hash.add(spot_key(neighbor))
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False
