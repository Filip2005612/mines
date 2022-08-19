
from turtle import color, pos
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from tools import create_tile, Grid, Mines
# Window.size = (500, 500)
sc = Window.size

sx = sc[0]
sy = sc[1]

map = Grid(10, 10)

mines = Mines(10, map.x, map.y)
map.grid = mines.fill_grid_with_mines(map.grid)
map.grid = mines.fill_grid_with_numbers(map.grid)
gap = 100
tile_size_x = 1/map.x
tile_size_y = 1/map.y
class GameWindow(Screen):
    def draw(self):
        self.clear_widgets()
        self.canvas.clear()
        tile_size_x = 1/map.x
        tile_size_y = 1/map.y
        
        x = 0
        y = 1
        with self.canvas:
            # for line in map.grid:
            #     for tile in line:

            #         l = create_tile(tile_size_x*x ,1 - tile_size_y*y, tile_size_x - tile_size_x/gap, tile_size_y - tile_size_y/gap, str(tile),sx, sy, [tile_size_x*x, tile_size_y*y, 0.4])
            #         self.add_widget(l)
            #         x  += 1
            #     x = 0
            #     y += 1
            for line in map.sight:
                for tile in line:
                    if tile == 'n':
                        l = create_tile(tile_size_x*x ,1 - tile_size_y*y, tile_size_x - tile_size_x/gap, tile_size_y - tile_size_y/gap, '',sx, sy, [tile_size_x*x, tile_size_y*y, 0.4])
                        self.add_widget(l)
                    else:
                        l = create_tile(tile_size_x*x ,1 - tile_size_y*y, tile_size_x - tile_size_x/gap, tile_size_y - tile_size_y/gap, str(tile),sx, sy, [tile_size_x*x, tile_size_y*y, 0.4])
                        self.add_widget(l)
                    x  += 1
                x = 0
                y += 1

    def on_touch_down(self, touch):
        pos  = touch.pos
        x = pos[0]
        y = pos[1]
    
        x_pos = int((x/sx)/tile_size_x)
        y_pos = int((1-y/sy)/tile_size_y)
        tile = map.see(x_pos, y_pos)

        if tile == 'nula':
            map.sight[y_pos][x_pos] = map.grid[y_pos][x_pos]
            map.cave(x_pos, y_pos)
            
        if tile == 'mine':
            print('miiina')
            map.sight[y_pos][x_pos] = map.grid[y_pos][x_pos]
        if tile == 'cislo':
            map.sight[y_pos][x_pos] = map.grid[y_pos][x_pos]

        self.draw()
class MenuWindow(Screen):
    pass
kv = Builder.load_file('toomo.kv')
class Start(App):
    def build(self):
        return kv
if __name__ == "__main__":
    Start().run()