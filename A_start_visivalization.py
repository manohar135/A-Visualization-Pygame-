import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pygame.init()
clock = pygame.time.Clock()

WIDTH = 900
ROWS = 30
GREY = (128, 128, 128)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165 ,0)
finder = AStarFinder()

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, WIDTH))

# A* Pathfinding

# SPOTS on the screen
class Spots:
    def __init__(self, rows=None, width = None, screen=None) -> None:
        self.start = None
        self.end = None
        self.rows = rows
        self.width = width
        self.screen = screen
        self.blocks_pos = []
        self.matrix = [[1]*self.rows for _ in range(self.rows)]

    def add_blocks(self, spot):
        self.blocks_pos.append(spot)

    def remove_block(self, spot):
        if spot in self.blocks_pos:
            self.matrix[spot[0]][spot[1]] = 1
            self.blocks_pos.remove(spot)

    def draw_spots(self):
        gap = self.width // self.rows

        if self.start:
            pygame.draw.rect(self.screen, GREEN, (self.start[0]*gap, self.start[1]*gap, gap, gap))
        if self.end:
            pygame.draw.rect(self.screen, BLUE, (self.end[0]*gap, self.end[1]*gap, gap, gap))
        if self.blocks_pos:
            for row, col in self.blocks_pos:
                pygame.draw.rect(self.screen, BLACK, (row*gap, col*gap, gap, gap))
        
    def get_matrix(self):
        for row, col in self.blocks_pos:
            if row <= self.rows and col <= self.rows:
                self.matrix[row][col] = 0

        return self.matrix
    

# Class to find the shortest path
class PathFind:
    def __init__(self, screen, rows, width) -> None:
        self.spots =  Spots(rows, width, screen)
        self.screen = screen
        self.rows = rows
        self.width = width
        self.paths = None
        self.start = False
        self.end = False

    def pathFind(self):
        matrix = self.spots.get_matrix()
        grid = Grid(matrix=matrix)

        y1, x1 = self.spots.start
        y2, x2 = self.spots.end

        start_pos = grid.node(x1, y1)
        end_pos = grid.node(x2, y2)

        self.paths, runs = finder.find_path(start_pos, end_pos, grid)

    def drawPath(self):
        gap = self.width // self.rows
        if self.paths:
            paths = self.paths[1:-1]
            for row, col in paths:
                pygame.draw.rect(self.screen, ORANGE, (col*gap, row*gap, gap, gap))

    # Mouse position to rows and columns of the grid 
    def mouse_clicked_pos(self, pos):
        gap = self.width // self.rows
        y, x = pos
        row = y // gap
        col = x // gap
        
        return row, col
    
    def draw_grids(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.screen, GREY, (0, i*gap), (self.width,i*gap))
            for j in range(self.rows):
                pygame.draw.line(self.screen, GREY, (j*gap, 0), (j*gap, self.width))

    #mouse and keybord intractions
    def mouseKeyEvents(self, event, live=False):
        if pygame.mouse.get_pressed()[0]: # MOUSE_LEFT_CLICK
            pos = pygame.mouse.get_pos()
            spot_pos= self.mouse_clicked_pos(pos)

            if not self.start:
                self.spots.start = spot_pos
                self.start = True
            elif not self.end and self.spots.start != spot_pos:
                self.spots.end = spot_pos
                self.end = True
            elif self.spots.start != spot_pos and self.spots.end != spot_pos:
                self.spots.add_blocks(spot_pos)

            if live:
                if self.start and self.end: #Live changing the path
                    self.pathFind()
        
        elif pygame.mouse.get_pressed()[2]: # MOUSE_RIGHT_CLICK
                pos = pygame.mouse.get_pos()
                spot_pos = self.mouse_clicked_pos(pos)
                if spot_pos == self.spots.start:
                    self.spots.start = None
                    self.start = False
                elif spot_pos == self.spots.end:
                    self.spots.end = None
                    self.end = False
                else:
                    self.spots.remove_block(spot_pos)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.start and self.end:
                self.pathFind()

            if event.key == pygame.K_r:
                self.start = False
                self.end = False
                self.spots.start = None
                self.spots.end = None
                self.paths = None
                self.spots.blocks_pos = []
                self.spots.matrix = [[1]*self.rows for _ in range(self.rows)]
