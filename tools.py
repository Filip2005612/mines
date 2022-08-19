from html.entities import name2codepoint
from turtle import xcor
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
import random
n1 = [-1, 1]
n2 = [0, 1]
n3 = [1, 1]
n4 = [-1, 0]
n5 = [1, 0]
n6 = [-1, -1]
n7 = [0, -1]
n8 = [1, -1]
neighbours = []
neighbours.append(n1)
neighbours.append(n2)
neighbours.append(n3)
neighbours.append(n4)
neighbours.append(n5)
neighbours.append(n6)
neighbours.append(n7)
neighbours.append(n8)
def create_tile(x, y, size_x, size_y, text_, sx, sy, color):
    Color(color[0], color[1], color[2])
    Rectangle(pos = (x*sx,y*sy), size = (sx*size_x, sy*size_y))
    l = Label(text = text_, pos_hint = {'x':x, 'y':y}, size_hint = [size_x, size_y])
    return l

class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = []
        self.sight = []
        self.create_grid()
        self.create_sight()
    def create_grid(self):
        
        for i in range(self.y):
            self.grid.append([])
            for j in range(self.x):
                self.grid[i].append(0)
            
    def create_sight(self):
        for i in range(self.y):
            self.sight.append([])
            for j in range(self.x):
                self.sight[i].append('n')
    def see(self, x, y):
        if self.grid[y][x] == 0:
            return 'nula'
        elif self.grid[y][x] == 'mine':
            return 'mine'
        else:
            return 'cislo'

    def cave(self, x, y):
        
        len_x = len(self.grid[0])
        len_y = len(self.grid)
        for neighbour in neighbours:
            x_pos = x + neighbour[0]
            y_pos = y + neighbour[1]
            if x_pos >= 0 and x_pos < len_x:
                if y_pos >= 0 and y_pos < len_y:
                
                    if self.grid[y_pos][x_pos] != 'mine' and self.sight[y_pos][x_pos] == 'n':
                    
                        self.sight[y_pos][x_pos] = self.grid[y_pos][x_pos]
                        if self.grid[y_pos][x_pos] == 0:

                            self.cave(x_pos, y_pos)
                        
        
        
                        

    def print_grid(self):
        for i in self.sight:
            print(i, '\n')
            
        

class Mines:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y

    def fill_grid_with_mines(self, grid):
        possibilities = []
        for i in range(self.y):
            for j in range(self.x):
                p = [j, i]
                possibilities.append(p)


        m = random.sample(possibilities, self.n)
       
    
        for i in range(len(m)):
            x_pos = m[i][0]
            y_pos = m[i][1]
            grid[y_pos][x_pos] = 'mine'
        return grid
    
    def fill_grid_with_numbers(self, grid):
        for y, line in enumerate(grid):
            for x,tile in enumerate(line):
                if tile == 'mine':
                    grid = self.find_neighbours(x ,y, grid)
        return grid
    def find_neighbours(self, x ,y, grid):
        len_x = len(grid[0])
        len_y = len(grid)
        
        for neighbour in neighbours:
            x_pos = x + neighbour[0]
            y_pos = y + neighbour[1]
            if x_pos >= 0 and x_pos < len_x:
                if y_pos >= 0 and y_pos < len_y:
                    if grid[y_pos][x_pos] != 'mine':
                        grid[y_pos][x_pos] += 1
        return grid









