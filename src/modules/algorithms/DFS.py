''' the module containing the implementation of the DFS algorithm '''

import pygame
from modules.path_reconstructer import reconstruct_path
# no need for priority queue as this algorithm doesn't have to decide between nodes

# Description:
#   DFS is an uninformed search algorithm that explores as far as possible along each branch before backtracking.

# Features:
#   - Utilizes a stack to keep track of the nodes to explore.
#   - Does not consider weights and may not find the shortest path in unweighted graphs.
#   - It doesn't guarantee the shortest path, but can be used to check if a path exists.

# Pros:
#   - Can be more memory efficient than BFS in certain situations, as it doesn't need to store all the nodes at the current depth.
#   - Can find solutions without exploring all nodes if the solution is deep.

# Cons:
#   - Does not guarantee the shortest path in unweighted graphs.
#   - Can get stuck in deep paths and miss shallower solutions.

# using:
#   1. Stack: Nodes to be explored, stored in a stack.
#   2. Visited Set: Tracks visited nodes to avoid revisiting them.
#   3. Parent Mapping: Maps nodes to their parents to reconstruct the path.

# Steps:
#   1. Add the start node to the stack.
#   2. While the stack is not empty:
#       1. Pop the top node.
#       2. If it’s the goal node, return the path.
#       3. Generate neighbors.
#       4. Add unvisited neighbors to the stack.
#       5. Mark the node as visited.

def dfs(draw, grid, start, end):
    ''' DFS is an uninformed search algorithm that explores as far as possible along each branch before backtracking.
    Does not guarantee the shortest path in unweighted graphs. '''
    stack = [start]  # stack for DFS
    came_from = {}  # to reconstruct the path
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = stack.pop()  # get the top node to explore

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()  # redraw the end color
            start.make_start()  # redraw the start color
            return True

        for neighbor in current.neighbors:
            if not visited[neighbor] and not neighbor.is_barrier():
                came_from[neighbor] = current
                stack.append(neighbor)
                visited[neighbor] = True
                neighbor.make_open()

        draw()

        if current != start:  # if current is not the start node, mark it as closed
            current.make_closed()

    return False  # if we did not find a path
