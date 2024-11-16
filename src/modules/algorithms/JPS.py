import pygame
from queue import PriorityQueue
from modules.distance_formulas import h  # Manhattan distance heuristic
from modules.path_reconstructer import reconstruct_path

# Description:
#   Jump Point Search (JPS) is an optimization technique for A* pathfinding. It reduces the number of nodes that need
#   to be explored by skipping over large sections of nodes, especially in uniform-cost grids. This is done by identifying
#   "jump points" that are significant in the pathfinding process and only evaluating those.

# Features:
#   Heuristics: Uses Manhattan distance heuristic to estimate the cost from the current node to the goal.
#   Jump Points: Skips non-critical nodes and focuses on "jump points" that are crucial for finding the optimal path.

# Pros:
#   Can significantly reduce the number of nodes explored compared to standard A*, especially in open areas.
#   Maintains the optimality and completeness of A*.

# Cons:
#   More complex implementation due to the identification of jump points.
#   Performance gain is less significant in very dense or highly complex grids.

# Steps:
#   1. Add the start node to the open set with an initial cost of 0.
#   2. While the open set is not empty:
#       1. Remove the node with the lowest f score (g + h).
#       2. If it’s the goal node, reconstruct and return the path.
#       3. For each direction from the current node:
#           1. Jump in the current direction until a jump point is found or an obstacle is hit.
#           2. If a jump point is found:
#               1. Update the g score.
#               2. Record the current node as the predecessor of the jump point.
#               3. If the jump point is not in the open set, add it.

def jps(draw, grid, start, end):
    ''' Jump Point Search (JPS) is an optimization technique for A* pathfinding. It reduces the number of nodes that need
        to be explored by skipping over large sections of nodes, especially in uniform-cost grids. This is done by identifying
        "jump points" that are significant in the pathfinding process and only evaluating those. Does not guarantee the shortest path. '''
    def get_neighbors(node):
        ''' Get the neighbors of a node while considering jump points '''
        neighbors = []
        x, y = node.get_pos()
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        
        for direction in range(4):
            nx, ny = x, y
            while True:
                nx += dx[direction]
                ny += dy[direction]
                if not (0 <= nx < len(grid) and 0 <= ny < len(grid)):
                    break
                neighbor = grid[nx][ny]
                if neighbor.is_barrier():
                    break
                neighbors.append(neighbor)
                if (nx, ny) == end.get_pos():
                    break
        return neighbors
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            
            # Mark all spots between the paths as path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            for spot in path:
                spot.make_path()
            
            # Mark all intermediate nodes between path nodes
            for i in range(len(path) - 1):
                x1, y1 = path[i].get_pos()
                x2, y2 = path[i + 1].get_pos()
                if x1 == x2:
                    for y in range(min(y1, y2) + 1, max(y1, y2)):
                        intermediate = grid[x1][y]
                        if not intermediate.is_path() and not intermediate.is_barrier():
                            intermediate.make_path()
                elif y1 == y2:
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        intermediate = grid[x][y1]
                        if not intermediate.is_path() and not intermediate.is_barrier():
                            intermediate.make_path()
            
            draw()
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False
