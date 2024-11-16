''' This module contains the function used to draw the shortest selected path in purple '''

def reconstruct_path(came_from, current, draw):
    ''' Reconstructs the path taken by the algorithm '''
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()