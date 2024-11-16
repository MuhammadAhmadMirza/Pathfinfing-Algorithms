''' this modules contains the distance formulas used to calculate the distance between 2 points in the algorithms '''

def h(p1, p2):   # h is the classical name for distance from destination in the A* algorithm
    ''' Return the manhattan distance between two points '''
  # the manhattan distance is the shortest L distance between 2 points unlike slanted distance in the distance formula
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def d(p1, p2):   # the classical distance formula
    ''' Return the euclidean distance between two points '''
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5