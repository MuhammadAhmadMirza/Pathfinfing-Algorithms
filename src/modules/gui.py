""" the main driver file responsible for the gui and running the algorithms """

import os, sys
import pygame, time
from assets.colors import *
from modules.spot import Spot
from modules.algorithms.a_star import a_star
from modules.algorithms.dijkstra import dijkstra
from modules.algorithms.theta_star import theta_star 
from modules.algorithms.DFS import dfs
from modules.algorithms.BS import bidirectional_search
from modules.algorithms.JPS import jps

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
SCREEN_DIMENSIONS = pygame.display.Info().current_w, pygame.display.Info().current_h

WIDTH = SCREEN_DIMENSIONS[0] * 0.8
HEIGHT = SCREEN_DIMENSIONS[1] * 0.8
FPS = 60

# setting up the window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithms")
pygame.display.set_icon(pygame.image.load(resource_path(os.path.join(ROOT_DIR, 'assets', 'images', 'icon.png'))))
clock = pygame.time.Clock()

# loading images
playing = pygame.transform.smoothscale(pygame.image.load(resource_path(os.path.join(ROOT_DIR, 'assets', 'images', 'playing.png'))), (HEIGHT // 30, HEIGHT // 30))
stopped = pygame.transform.smoothscale(pygame.image.load(resource_path(os.path.join(ROOT_DIR, 'assets', 'images', 'stopped.png'))), (HEIGHT // 30, HEIGHT // 30))
found = pygame.mixer.Sound(resource_path(os.path.join(ROOT_DIR, 'assets', 'sounds', 'found.wav')))
not_found = pygame.mixer.Sound(resource_path(os.path.join(ROOT_DIR, 'assets', 'sounds', 'not found.wav')))

# defining globals
ROWS = 50  # the columns will be of the same number and represented by the same variable
algorithm = dfs
elapsed_time = 0
start_time = None
path_length = 0
extra_path_length = 0
font_large = pygame.font.Font(None, int(WIDTH / 25))
font_small = pygame.font.Font(None, int(WIDTH / 40))

def make_grid(rows, width):
	""" Create a grid of spots """
	grid = []
	gap = width / rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid

def draw_thicker_line(win, color, start, end, thickness):
	""" Draw a thicker line by drawing multiple lines """
	x1, y1 = start
	x2, y2 = end
	
	# Calculate the direction vector
	dx = x2 - x1
	dy = y2 - y1
	
	# Normalize the direction vector
	length = (dx**2 + dy**2) ** 0.5
	if length == 0:
		return
	dx /= length
	dy /= length
	
	# Draw multiple lines to achieve thickness
	for i in range(-thickness // 2, thickness // 2 + 1):
		offset_x = int(dy * i)
		offset_y = int(-dx * i)
		pygame.draw.line(win, color, (x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y))

def draw_grid(win, rows, width):
	""" Draw the grid lines with thickness """
	gap = width / rows
	thickness = 1  # Desired thickness of the lines
	
	# Horizontal lines
	for i in range(rows):
		y = i * gap
		draw_thicker_line(win, GRAY, (0, y), (width, y), thickness)
	
	# Vertical lines
	for j in range(rows):
		x = j * gap
		draw_thicker_line(win, GRAY, (x, 0), (x, width), thickness)

def wrap_text(text, font, max_width):
	""" Wraps the text to fit within the specified width """
	words = text.split(" ")
	lines = []
	current_line = ""
	
	for word in words:
		# Test if the word fits on the current line
		test_line = f"{current_line} {word}".strip()
		if font.size(test_line)[0] <= max_width:
			current_line = test_line
		else:
			lines.append(current_line)
			current_line = word
	
	if current_line:
		lines.append(current_line)
	
	return lines

def draw_initials(window):
	""" Draws the initial elements of the settings panel """
	pygame.draw.rect(window, GRAY, (HEIGHT, 0, WIDTH - HEIGHT, HEIGHT))
	
	# Draw the playing or stopped icon
	icon = playing if started else stopped
	window.blit(icon, (WIDTH - icon.get_width() * 2, icon.get_height()))
	
	# Draw the "Controls" heading
	heading = font_large.render("Controls", 1, BLACK)
	window.blit(heading, (HEIGHT + (WIDTH - HEIGHT - heading.get_width()) // 2, 10))
	
	# Draw the grid size
	grid_size_text = font_small.render(f"Size: {ROWS}", 1, BLACK)
	window.blit(grid_size_text, (HEIGHT + font_large.get_height() // 2, font_small.get_height()))
	
	return heading

def draw_controls(window, heading):
	""" Draws the control instructions and returns the position for the next elements """
	controls = [
		"Space: Run Algorithm",
		"Backspace: Clear Grid",
		"Left Click: Place Start/End/Barrier",
		"Right Click: Remove Start/End/Barrier",
		"Up/Down: Increase/Decrease Grid Size",
		"",  # Empty line for separation
		"1: Depth First Search",
		"2: Dijkstra Algorithm",
		"3: Bidirectional Search",
		"4: A* Algorithm",
		"5: Jump Point Search",
		"6: Theta* algorithm"
	]
	
	text_pos = heading.get_height() * 2  # Start position after the heading and grid size
	for control in controls:
		text = font_small.render(control, 1, BLACK)
		window.blit(text, (HEIGHT + (WIDTH - HEIGHT - text.get_width()) // 2, text_pos))
		text_pos += 30
		
	return text_pos

def draw_algorithm_name(window, algorithm_name, text_pos):
	""" Draws the selected algorithm name and returns the position for the next elements """
	text_pos += 20  # Additional space
	
	alg_name_dict = {
		a_star: "A* Algorithm", 
		dijkstra: "Dijkstra Algorithm", 
		theta_star: "Theta* algorithm", 
		dfs: "Depth First Search", 
		bidirectional_search: "Bidirectional Search", 
		jps: "Jump Point Search"
	}
	algo_text = font_large.render(alg_name_dict[algorithm_name], 1, BLACK)
	window.blit(algo_text, (HEIGHT + (WIDTH - HEIGHT - algo_text.get_width()) // 2, text_pos))
	
	return text_pos

def draw_algorithm_description(window, algorithm_name, text_pos):
	""" Draws the algorithm"s documentation """
	# Draw the algorithm"s documentation
	doc_text = algorithm_name.__doc__  # Use the documentation string of the selected algorithm
	wrapped_lines = wrap_text(doc_text, font_small, WIDTH - HEIGHT - 20)  # 20 pixels padding from the edge
	
	# Adjust text position to avoid overlap
	doc_text_pos = text_pos + font_large.get_height() + 20  # Additional space after algorithm name
	
	for line in wrapped_lines:
		doc_text_rendered = font_small.render(line, 1, BLACK)
		window.blit(doc_text_rendered, (HEIGHT + (WIDTH - HEIGHT - doc_text_rendered.get_width()) // 2, doc_text_pos))
		doc_text_pos += 20
		
	return doc_text_pos

def draw_elapsed_time(window, elapsed_time):
	""" Draws the elapsed time """
	elapsed_text = font_small.render(f"Time: {elapsed_time:.2f} s", 1, BLACK)
	window.blit(elapsed_text, (HEIGHT + (WIDTH - HEIGHT - elapsed_text.get_width()) // 2, HEIGHT - elapsed_text.get_height() * 3))

def draw_path_length(window, path_length, extra_path_length):
	""" Displays the path length and extra search length side by side """
	path_length_text = font_small.render(f"Path Length: {path_length}", 1, BLACK)
	extra_path_length_text = font_small.render(f"Extra Search: {extra_path_length}", 1, BLACK)
	
	# Calculate the positions to display the texts side by side
	padding = 20
	path_length_x = HEIGHT + (WIDTH - HEIGHT - (path_length_text.get_width() + extra_path_length_text.get_width() + padding)) // 2
	extra_path_length_x = path_length_x + path_length_text.get_width() + padding
	
	window.blit(path_length_text, (path_length_x, HEIGHT - path_length_text.get_height() * 1.5))
	window.blit(extra_path_length_text, (extra_path_length_x, HEIGHT - extra_path_length_text.get_height() * 1.5))

def draw_settings_panel(window, algorithm_name):
	""" Draws the side panel for control """
	global elapsed_time, path_length, extra_path_length, started
	
	heading = draw_initials(window)
	text_pos = draw_controls(window, heading)
	text_pos = draw_algorithm_name(window, algorithm_name, text_pos)
	text_pos = draw_algorithm_description(window, algorithm_name, text_pos)
	draw_elapsed_time(window, elapsed_time)
	draw_path_length(window, path_length, extra_path_length)

def draw(window, grid, rows):
	""" Redraw the grid and the spots again over the previous screen to update the window """
	window.fill(WHITE)
	
	# Draw spots
	for row in grid:
		for spot in row:
			spot.draw(window)
			
	draw_grid(window, rows, HEIGHT)
	draw_settings_panel(window, algorithm)
	
	pygame.display.flip()
	
def get_clicked_pos(pos, rows):
	""" Get the index position of the spot that the user clicked on from the mouse position"""
	gap = HEIGHT / rows
	y, x = pos
	
	row = int(y / gap)
	col = int(x / gap)
	
	return row, col
	
def main(window):
	""" The main function that runs the game loop """
	global algorithm, elapsed_time, start_time, path_length, extra_path_length, ROWS, started
	
	grid = make_grid(ROWS, HEIGHT)
	
	def in_grid():
		x, y = pygame.mouse.get_pos()
		return x <= HEIGHT and y <= HEIGHT
		
	start = None  # the position of the starting spot
	end = None  # the position of the ending spot
	
	run = True
	global started; started = False  # if the algorithm has started running
	
	while run:
		
		draw(window, grid, ROWS)
		
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				run = False
				
			if started: 
				continue 
			
			if in_grid():
				if pygame.mouse.get_pressed()[0]:  # left button
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS)
					if 0 <= row < ROWS and 0 <= col < ROWS:
						spot = grid[row][col]  # selecting the clicked spot
						
						if not start and spot != end:  # if the start square is not selected, make the current spot the start spot
							start = spot
							start.make_start()
						elif not end and spot != start:  # similarly for the end spot
							end = spot
							end.make_end()
						elif spot != end and spot != start:  # if we are not re selecting start and end, then make barriers
							spot.make_barrier()
						
				elif pygame.mouse.get_pressed()[2]:  # right button
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS)
					if 0 <= row < ROWS and 0 <= col < ROWS:
						spot = grid[row][col]  # selecting the clicked spot
						spot.reset()
						if spot == start:
							start = None
						elif spot == end:
							end = None
			
			if event.type == pygame.KEYDOWN:
				# run the algorithm
				if event.key == pygame.K_SPACE and not started and end:  # if the space key is pressed and the algorithm has not started
					start_time = time.time()  # Start the timer
					started = True
					elapsed_time = 0
					path_length = 0
					extra_path_length = 0
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
							if spot.is_open() or spot.is_closed() or spot.is_path():
								spot.reset()
					path_found = algorithm(lambda: draw(window, grid, ROWS), grid, start, end)
					
					if path_found:
						# Stop the timer after the algorithm finishes
						elapsed_time = time.time() - start_time
						
						# Calculate the path length and extra path length
						path_length = sum(1 for row in grid for spot in row if spot.is_path())
						extra_path_length = sum(1 for row in grid for spot in row if spot.is_closed() and not spot.is_path())
      
						found.play()
					else:
						not_found.play()
      
					started = False  # Reset the started flag

				# clear the grid
				elif event.key == pygame.K_BACKSPACE:
					start = None
					end = None
					grid = make_grid(ROWS, HEIGHT)
				
				# change the algorithm
				elif event.key == pygame.K_1:
					algorithm = dfs
				elif event.key == pygame.K_2:
					algorithm = dijkstra
				elif event.key == pygame.K_3:
					algorithm = bidirectional_search
				elif event.key == pygame.K_4:
					algorithm = a_star
				elif event.key == pygame.K_5:
					algorithm = jps
				elif event.key == pygame.K_6:
					algorithm = theta_star
					
				# changing the grid size
				elif event.key == pygame.K_UP and ROWS < 120:
					ROWS += 10
					start = None
					end = None
					grid = make_grid(ROWS, HEIGHT)
				elif event.key == pygame.K_DOWN and ROWS > 10:
					ROWS -= 10
					start = None
					end = None
					grid = make_grid(ROWS, HEIGHT)
									
		clock.tick(FPS)
	
	pygame.quit()
	