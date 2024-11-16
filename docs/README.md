# Pathfinfing Algorithms
 
This project provides simple implementations of several graph traversal and pathfinding algorithms in Python. The algorithms included are designed to find the shortest path between two points on a graph or grid.

Algorithms Implemented:
    1. Depth First Search (DFS)
    2. Dijkstra's Algorithm
    3. Bidirectional Search
    4. A* Algorithm
    5. Jump Point Search (JPS)
    6. Theta* Algorithm

Features:
    GUI for visualizing live search
    Customizable path and start/end points
    Customizable Grid Size

Prerequisites
    Python 3.x
    Required libraries:
        pygame
    You can install the required libraries using the following command:
    pip install -r requirements.txt

Packaging the Project with PyInstaller
To package this project into a standalone executable, you can use PyInstaller. Follow the instructions below to create the executable:
pyinstaller --noconfirm --onefile --windowed --icon "C:\Users\muahm\Documents\Programming Projects\Python programs\Pathfinfing-Algorithms\src\assets\images\icon.ico" --name "Pathfinding Algorithms" --add-data "C:\Users\muahm\Documents\Programming Projects\Python programs\Pathfinfing-Algorithms\src;src/" --add-data "C:\Users\muahm\Documents\Programming Projects\Python programs\Pathfinfing-Algorithms\src\assets;assets/" --hidden-import "pygame" --hidden-import "qeue"  "C:\Users\muahm\Documents\Programming Projects\Python programs\Pathfinfing-Algorithms\src\__main__.py"