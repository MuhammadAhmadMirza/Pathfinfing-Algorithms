''' the Bidirectional Search algorithm '''

import pygame
from queue import Queue
from modules.path_reconstructer import reconstruct_path

# Description:
#   Bidirectional Search is a graph traversal algorithm that simultaneously searches from the start node and the goal node.
#   It aims to meet in the middle, reducing the search space compared to a single-direction search.

# Features:
#   - Utilizes two queues to keep track of nodes from both directions.
#   - Can be more efficient than single-direction search in practice.

# Pros:
#   - Often more efficient than single-direction search.
#   - Reduces the search space by exploring from both directions.

# Cons:
#   - More complex to implement than single-direction search.
#   - Requires additional memory to keep track of both searches.

# using:
#   1. Open Sets: Nodes to be evaluated from both directions.
#   2. Closed Sets: Nodes already evaluated from both directions.
#   3. Parent Mapping: Maps nodes to their parents to reconstruct the path.
#   4. Meeting Point: The point where the two searches meet.

# Steps:
#   1. Initialize the open and closed sets for both searches.
#   2. Add the start node to the open set of the start search and the end node to the open set of the goal search.
#   3. While both open sets are not empty:
#       1. Expand the front of both open sets.
#       2. Check if the two searches have met.
#       3. If they meet, reconstruct and return the path.
#       4. Otherwise, add unvisited neighbors to the respective open sets and mark them as visited.

def bidirectional_search(draw, grid, start, end):
    ''' Bidirectional Search is a graph traversal algorithm that simultaneously searches from the start node and the goal node.
        It aims to meet in the middle, reducing the search space compared to a single-direction search. Guarantees the shortest path if the heuristic is admissible (does not overestimate the true cost). '''
    if start == end:
        return True

    open_set_start = Queue()
    open_set_end = Queue()
    open_set_start.put(start)
    open_set_end.put(end)
    came_from_start = {}
    came_from_end = {}
    visited_start = {spot: False for row in grid for spot in row}
    visited_end = {spot: False for row in grid for spot in row}
    visited_start[start] = True
    visited_end[end] = True

    while not open_set_start.empty() and not open_set_end.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Expand the start search
        current_start = open_set_start.get()
        if visited_end[current_start]:
            # Collect and mark the path from start to meeting point
            path_from_start = []
            temp = current_start
            while temp in came_from_start:
                path_from_start.append(temp)
                temp = came_from_start[temp]
            path_from_start.append(start)
            path_from_start.reverse()

            # Collect and mark the path from end to meeting point
            path_from_end = []
            temp = current_start
            while temp in came_from_end:
                path_from_end.append(temp)
                temp = came_from_end[temp]
            path_from_end.append(end)

            # Combine both paths and mark them
            all_path_spots = set(path_from_start + path_from_end)
            for spot in all_path_spots:
                spot.make_path()
                
            end.make_end()  # redraw the end color
            start.make_start()  # redraw the start color
            return True

        for neighbor in current_start.neighbors:
            if not visited_start[neighbor] and not neighbor.is_barrier():
                came_from_start[neighbor] = current_start
                open_set_start.put(neighbor)
                visited_start[neighbor] = True
                neighbor.make_open()

        # Expand the end search
        current_end = open_set_end.get()
        if visited_start[current_end]:
            # Collect and mark the path from end to meeting point
            path_from_end = []
            temp = current_end
            while temp in came_from_end:
                path_from_end.append(temp)
                temp = came_from_end[temp]
            path_from_end.append(end)
            path_from_end.reverse()

            # Collect and mark the path from start to meeting point
            path_from_start = []
            temp = current_end
            while temp in came_from_start:
                path_from_start.append(temp)
                temp = came_from_start[temp]
            path_from_start.append(start)

            # Combine both paths and mark them
            all_path_spots = set(path_from_start + path_from_end)
            for spot in all_path_spots:
                spot.make_path()
                
            end.make_end()  # redraw the end color
            start.make_start()  # redraw the start color
            return True

        for neighbor in current_end.neighbors:
            if not visited_end[neighbor] and not neighbor.is_barrier():
                came_from_end[neighbor] = current_end
                open_set_end.put(neighbor)
                visited_end[neighbor] = True
                neighbor.make_open()

        draw()

        if current_start != start:  # Mark it as closed
            current_start.make_closed()
        if current_end != end:  # Mark it as closed
            current_end.make_closed()

    return False  # if we did not find a path