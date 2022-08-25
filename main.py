from cgitb import text
from distutils import ccompiler
from random import random
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from tools import create_tile, Grid, Mines, create_bar
Window.size = (400, 800)
sc = Window.size

sx = sc[0]
sy = sc[1]

difficulties = {'easy':[6, 11, 10], 'medium':[11, 18, 35], 'hard': [15, 25, 75] }
#difficulties = {'easy':[6, 11], 'medium':[10, 18], 'hard': [16, 25] }
#difficulties = {'easy':[4, 8], 'medium':[4, 8], 'hard': [15, 25] }




start_x = 0
start_y = -0.1

COLORS = [(0.1,0.1,0.7), (0.1,0.1,0.1)]




# delta_x = 0
# delta_y = 0
class GameWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_difficulty = 'easy'
        self.tool = 'none'
        self.x_tiles = difficulties[self.current_difficulty][0]
        self.y_tiles = difficulties[self.current_difficulty][1]
       
        self.map = Grid(self.x_tiles, self.y_tiles)
        self.tile_size_y = 0.8/self.map.y
        self.tile_size_x = 1/self.map.x
        m = difficulties[self.current_difficulty][2]
        self.mines = Mines(m, self.map.x, self.map.y)
        self.map.grid = self.mines.fill_grid_with_mines(self.map.grid)
        self.map.grid = self.mines.fill_grid_with_numbers(self.map.grid)
        self.size_x = self.tile_size_x 
        self.size_y = self.tile_size_y 
        
    def overwrite(self):
        x = 0
        y = 0
        id  = str(x) + '.' + str(y)
        self.ids.id.text = 'pes'
        # for line in self.map.sight:
        #         for tile in line:
        #             ypos = 1-self.tile_size_y*y - self.size_y
                        
        #             if tile != 'n':
        #                 id = str(x) +'.' +str(y)
        #                 self.ids.id.text = str(tile)
                       
                    

        #             x += 1
        #         y += 1
        #         x = 0
    def draw(self):
        self.clear_widgets()
        self.canvas.clear()
        c = self.canvas.after
        c.clear()
        
        x = 0
        y = 0
        c = 0
        ypos = 1-self.tile_size_y*y - self.size_y
        with self.canvas:
            l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,str('macka'),sx, sy, COLORS[c])
                    
            self.add_widget(l)
            id = str(x) + '.' + str(y)
            print(id)
            self.ids[id] = l
            # for line in self.map.sight:
            #     if (len(line)+1)%2:
            #         if c == 0:
            #             c = 1
            #         else:
            #             c = 0
            

            #     for tile in line:
            #         ypos = 1-self.tile_size_y*y - self.size_y
            #         # if tile == 'n':
                        
            #         if c == 0:
            #             l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,'',sx, sy, COLORS[c])
            #             self.ids[str(x) + '.' + str(y)] = l
            #             self.add_widget(l)
            #             c = 1
            #         else:
            #             l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,'',sx, sy, COLORS[c])
            #             self.ids[str(x) +'.'+ str(y)] = l
            #             self.add_widget(l)
            #             c = 0
                          
                        
                        
                    # else:
                       
                    #     if c == 0:
                    #         l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,str(tile),sx, sy, COLORS[c])
                        
                    #         self.add_widget(l)
                    #         c = 1
                    #     else:
                    #         l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,str(tile),sx, sy, COLORS[c])
                    
                    #         self.add_widget(l)
                    #         c = 0
                #     x  += 1
                # x = 0
                # y += 1
                

        #     create_bar(0 ,0.9, 1, 0.1,sx, sy, [0.7,0.9, 0.1])
        #     create_bar(0 ,0, 1, 0.1,sx, sy, [0.7,0.9, 0.1])
        #     vlajka = create_tile(0 ,0,0.5 ,0.1 ,'vlajocka',sx, sy, (0,1,1,0))
        #     lopata = create_tile(0.5 ,0,0.5 ,0.1 ,'lopata',sx, sy, (0,0,1,1))           
        #     state = create_tile(0.5 ,0.9,0.3 ,0.1 ,self.tool,sx, sy, (0,0,1,1))
        #     self.ids['state'] = state
        #     self.add_widget(vlajka)
        #     self.add_widget(lopata)
        #     self.add_widget(state)
        # self.create_spinner(0.1, 0.9, 0.2, 0.1, self.current_difficulty)
    



    def create_spinner(self, x, y, size_x, size_y, text):
        self.spinnerObject = Spinner(text =text,values =('easy', 'medium', 'hard'),background_color =(0.784, 0.443, 0.216, 1))
        self.spinnerObject.size_hint = (size_x, size_y)
        self.spinnerObject.pos_hint ={'x': x, 'y':y}
        self.spinnerObject.bind(text=self.on_spinner_select)
        self.add_widget(self.spinnerObject)



    def on_spinner_select(self,a, b):
        self.current_difficulty = b
    
        self.x_tiles = difficulties[self.current_difficulty][0]
        self.y_tiles = difficulties[self.current_difficulty][1]
       
        self.map = Grid(self.x_tiles, self.y_tiles)
        self.tile_size_y = 0.8/self.map.y
        self.tile_size_x = 1/self.map.x
        m = difficulties[self.current_difficulty][2]
        self.mines = Mines(m, self.map.x, self.map.y)
        self.map.grid = self.mines.fill_grid_with_mines(self.map.grid)
        self.map.grid = self.mines.fill_grid_with_numbers(self.map.grid)
        self.size_x = self.tile_size_x 
        self.size_y = self.tile_size_y 
        self.draw()


    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        pos  = touch.pos
        
        x = pos[0]
        y = pos[1]
        y_cor = (1-y/sy) + start_y
   
        if y_cor > 0 and y_cor < 0.8:
            x_pos = int((x/sx)/self.tile_size_x)
            
            y_pos = int(y_cor/self.tile_size_y)
           
            tile = self.map.see(x_pos, y_pos)

            if tile == 'nula':
                self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]
                self.map.cave(x_pos, y_pos)
                
            if tile == 'mine':
                print('miiina')
                self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]
            if tile == 'cislo':
                self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]

            self.overwrite()
        if y_cor > 0.8:
            if x/sx > 0.5:
                
                self.tool = 'lopata'
                self.ids.state.text = 'loptata'
            else:
                
                self.tool = 'vlajka'
                self.ids.state.text = 'vlajka'
    

    # def on_touch_move(self, touch):
    #     global start_x, start_y
    #     pos  = touch.pos
    #     x = pos[0]
    #     y = pos[1]
    #     dx = delta_x - x
    #     dy = delta_y - y
    #     start_x += dx/sx
    #     start_y += dy/sy
    #     self.draw()

    # def on_touch_up(self, touch):
    #     global delta_y, delta_x
    #     delta_x = 0
    #     delta_y = 0



class MenuWindow(Screen):
    pass
kv = Builder.load_file('toomo.kv')
class Start(App):
    def build(self):
        return kv
if __name__ == "__main__":
    Start().run()