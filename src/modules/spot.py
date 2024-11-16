''' This module contains the Spot class which is used to represent each square on the grid. 
Each spot has a color, position, neighbors and other attributes. 
The class also contains methods to check the state of the spot and to update the state of the spot. '''

import pygame
from assets.colors import *

class Spot:
	''' A class to represent each square on the grid '''
	def __init__(self, row, col, width, total_rows): # we need width only as all the spots will be squares
		''' Initialize the spot '''
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		
	def get_pos(self):
		''' Return the position of the spot as row, col'''
		return self.row, self.col
	
	def is_closed(self):
		''' Id the spot is not in the open set and has already been considered'''
		return self.color == RED
	
	def is_open(self):
		''' If the spot is in the open set and is yet to be considered'''
		return self.color == GREEN
	
	def is_barrier(self):
		''' If the spot is a wall that the algorithm cannot visit '''
		return self.color == BLACK
	
	def is_start(self):
		''' If the spot is the origin point '''
		return self.color == ORANGE
	
	def is_end(self):
		''' If the spot is the destination point '''
		return self.color == TURQUOISE

	def is_path(self):
		''' If the spot is part of the path '''
		return self.color == PURPLE
	
	def reset(self):
		''' Reset the spot to its default state '''
		self.color = WHITE
		
	def make_closed(self):
		''' Mark the spot as considered '''
		self.color = RED
	
	def make_open(self):
		''' Mark the spot as to be considered '''
		self.color = GREEN
	
	def make_barrier(self):
		''' Mark the spot as a wall '''
		self.color = BLACK
		
	def make_start(self):
		''' Mark the spot as the origin point '''
		self.color = ORANGE
	
	def make_end(self):
		''' Mark the spot as the destination point '''
		self.color = TURQUOISE
	
	def make_path(self):
		''' Mark the spot as part of the path '''
		self.color = PURPLE
		
	def draw(self, window):
		''' Draw the spot on the window '''
		# +1 because one pixel of the rectangle covered by the line so it leaves some extra space on the other side
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width + 1, self.width + 1)) 
  
	def update_neighbors(self, grid):
		''' Update the neighbors of the spot '''
		self.neighbors = []
		
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])
	
	def __It__(self, other):
		''' Compare the spots '''
		return False
