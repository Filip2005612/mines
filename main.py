from random import random
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from tools import create_tile, Grid, Mines, create_bar, convertor
from kivy.clock import Clock
import json
# image = f'data/{random.randint(0,4)}.png'
Window.size = (400, 800)
sc = Window.size

sx = sc[0]
sy = sc[1]

difficulties = {'easy':[6, 11, 7], 'medium':[10, 18, 35], 'hard': [15, 25, 75] }
#difficulties = {'easy':[6, 11], 'medium':[10, 18], 'hard': [16, 25] }
#difficulties = {'easy':[4, 8], 'medium':[4, 8], 'hard': [15, 25] }




start_x = 0
start_y = -0.1

COLORS = [(0.1,0.1,0.7), (0.1,0.1,0.1)]
SURFACES = [f'data/surface1.png',f'data/surface2.png' ]
first_click = True
click_allowed = True
class P(Popup):
    def __init__(self, caller,**kwargs):
        super().__init__(**kwargs)
        
        self.caller = caller
        bx = BoxLayout()
        self.size_hint = [0.7, 0.7]
        self.auto_dismiss = True
        self.on_dismiss = self.restart
        self.content = bx
        self.title = 'Prehral si'
        self.background = "data/bomba.png"
       
    
    def restart(self):
        global click_allowed
        click_allowed = True
        self.caller.restart()
        
class W(Popup):
    def __init__(self, caller,**kwargs):
        super().__init__(**kwargs)
        
        self.caller = caller
        bx = BoxLayout()
        self.title = 'Vyhral si'
        self.background = 'data/bomba.png'
        self.size_hint = [0.7, 0.7]
        self.content = bx
        f = open('score.json', 'r')
        data = json.load(f)
        f.close()
        self.on_dismiss = self.win
        score = Label(text = 'Tvoje skóre je: ' + str(GameWindow.time) + '\n' + 'high score je: ' + str(data[self.caller.current_difficulty]), pos_hint = {'x':0.1, 'y':0.5}, size_hint = [0.3, 0.3])
        bx.add_widget(score)
        

    def win(self):
        f = open('score.json', 'r')
        data = json.load(f)
        self.caller.ids.high.text = 'high score: ' + str(data[self.caller.current_difficulty])
        f.close()

class MenuWindow(Screen):
    def on_pre_enter(self, *args):
        self.draw()
    def draw(self):

        self.clear_widgets()
        self.canvas.clear()
        egg  = Button(size_hint = (0.05, 0.05), pos_hint = {'x':0.14, 'y':0.78},text ="", on_press = self.egg)
        self.add_widget(egg)
        

        with self.canvas:
            
            Rectangle(source = 'data/debili.png',pos = (sx*0,sy*1 - sy), size = (sx*1, sy*1))
            l = Label(text = '', pos_hint = {'x':0, 'y':0.4}, size_hint = [1, 0.5],halign="left", valign="middle")
            self.ids['basnicka'] = l
            self.add_widget(l)

    def egg(self, *args):
       
        if self.ids.basnicka.text == "":
            str = 'Natálka si pre mňa jediná \nnie si až tak lenivá \nvolejbal ťa pochitil \na ja som ťa zachytil \n \nOd Vikinky ďaleko nemáš \nale aspoň sa na nič nehráš \npre mňa niečo znamenáš \na aj ty po mne zazeráš\n\nRaz ti niečo ukážem \na pojdeme na masáže \naj keď prejdeme cez pasáže\ntak sa zase nájdeme\n\nPostavu máš nádhernú \na pre mňa perfektnú\npleť máš strašne príjemnú\nale pre niekoho mizernú\n\nDúfam, že sme si súdení\nale zase nie sme skúsení\nverím, že sme pre seba stvorení\na dúfam, že sa s tebou ožením'
            self.ids.basnicka.text = str
            
        else:
            self.ids.basnicka.text = ''
                    
class GameWindow(Screen):
    time = 0
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
        self.images = self.map.images()
        self.rectangles = {}
        self.flags = str(m)
    
    def update(self,d):
        GameWindow.time += 1
        self.ids.time.text = str(GameWindow.time)

    def overwrite(self):
        
        
        for y, line in enumerate(self.map.sight):
            for x, tile in enumerate(line):
            
                id = convertor(x,y)
                if tile == 'mine':
                    self.rectangles[id].source = f'data/bomba.png'
                elif tile == 'vlajka':
                    self.rectangles[id].source = f'data/vlajka.png'
                elif tile == 'n':
                    if y %2 ==0:
                        if x%2 == 0:
                            self.rectangles[id].source = f'data/surface1.png'
                        else:
                            self.rectangles[id].source = f'data/surface2.png'
                    else:
                        if x%2 == 0:
                            self.rectangles[id].source = f'data/surface2.png'
                        else:
                            self.rectangles[id].source = f'data/surface1.png'
                else:
                    if tile != 0:
                        self.ids[id].text = str(tile)
                    self.rectangles[id].source = self.images[y][x]



    def draw(self):
        self.clear_widgets()
        self.canvas.clear()

        x = 0
        y = 0
        c = 0
        ypos = 1-self.tile_size_y*y - self.size_y
        with self.canvas.before:
            
            for line in self.map.sight:
                
            
                for tile in line:
                    ypos = 1-self.tile_size_y*y - self.size_y
                    
                        
                    l = create_tile(start_x + self.tile_size_x*x ,start_y + ypos ,self.size_x ,self.size_y ,'',sx, sy,self, image = SURFACES[c])
                    id  = convertor(x,y)
                    self.rectangles[id] = l[1]
                    self.ids[id] = l[0]
                    if c == 0:
                        c = 1
                    else:
                        c = 0
                    x  += 1
                x = 0
                y += 1
                
                if (len(line)+1)%2:
                    if c == 0:
                        c = 1
                    else:
                        c = 0
            create_bar(0 ,0.9, 1, 0.1,sx, sy, [0.7,0.9, 0.1])
            create_bar(0 ,0, 1, 0.1,sx, sy, [0.7,0.9, 0.1])
            
                      
            state = create_tile(0.35 ,0.9,0.2 ,0.1 ,self.tool,sx, sy,self, color = (0,0,1,1))
            restart  = Button(size_hint = (0.15, 0.1), pos_hint = {'x':0.2, 'y':0.9},text ="restart",background_color = (1,0,1,1), on_press = self.restart)
            time = create_tile(0.8, 0.9, 0.1, 0.1, str(GameWindow.time), sx, sy,self, color = (1,0,1,0))
            vlajky = create_tile(0.9 ,0.9,0.1 ,0.1 ,self.flags,sx, sy,self, image = 'data/vlajka.png')
            vlajka = create_tile(0 ,0,0.5 ,0.1 ,'',sx, sy,self , image= 'data/vlajka.png')
            lopata = create_tile(0.5 ,0,0.5 ,0.1 ,'',sx, sy,self, image = 'data/lopata.png') 
            f = open('score.json', 'r')
            data = json.load(f)
            f.close()
            hihg_score = create_tile(0.55 ,0.9,0.25 ,0.1 ,'high score: ' +  str(data[self.current_difficulty]),sx, sy,self, color = (0,1,0,1))
            
            self.ids['vlajky'] = vlajky[0]
            self.ids['state'] = state[0]
            self.ids['time'] = time[0]
            self.ids['high'] = hihg_score[0]
            self.add_widget(restart)

          
        self.create_spinner(0, 0.9, 0.2, 0.1, self.current_difficulty)
    

    def restart(self, *args):
        global first_click
        first_click = True
        Clock.unschedule(self.update)
        GameWindow.time = 0
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
        self.images = self.map.images()
        self.flags = str(m)
        self.draw()



    def create_spinner(self, x, y, size_x, size_y, text):
        self.spinnerObject = Spinner(text =text,values =('easy', 'medium', 'hard'),background_color =(0.784, 0.443, 0.216, 1))
        self.spinnerObject.size_hint = (size_x, size_y)
        self.spinnerObject.pos_hint ={'x': x, 'y':y}

        self.spinnerObject.bind(text=self.on_spinner_select)
        self.add_widget(self.spinnerObject)



    def on_spinner_select(self,a, b):
        self.current_difficulty = b
        self.restart('debil')
   
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        
        global first_click, click_allowed
        if click_allowed:
            pos  = touch.pos
            
            x = pos[0]
            y = pos[1]
        
            y_cor = (1-y/sy) + start_y
            if first_click and self.ids.state.text != 'none':
                if y_cor > 0 and y_cor < 0.8:
                    Clock.schedule_interval(self.update, 1)
                    first_click = False
            if self.tool == 'lopata':
                if y_cor > 0 and y_cor < 0.8:

                    x_pos = int((x/sx)/self.tile_size_x)
                    
                    y_pos = int(y_cor/self.tile_size_y)
                    if self.map.sight[y_pos][x_pos] == 'n':
                        tile = self.map.see(x_pos, y_pos)

                        if tile == 'nula':
                            self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]
                            self.map.cave(x_pos, y_pos)
                            
                        if tile == 'mine':
                            click_allowed = False
                            Clock.schedule_once(self.show_popup_lost, 1)
                            self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]

                        if tile == 'cislo':
                            self.map.sight[y_pos][x_pos] = self.map.grid[y_pos][x_pos]

                        self.overwrite()

            if self.tool == 'vlajka':
                if y_cor > 0 and y_cor < 0.8:
                    x_pos = int((x/sx)/self.tile_size_x) 
                    y_pos = int(y_cor/self.tile_size_y)
                    
                    if self.map.sight[y_pos][x_pos] == 'vlajka':
                        self.map.sight[y_pos][x_pos] = 'n'
                        self.flags = str(int(self.flags) + 1)
                        self.ids.vlajky.text = self.flags
                        self.overwrite()
                        
                    elif self.map.sight[y_pos][x_pos] == 'n':
                        self.map.sight[y_pos][x_pos] = 'vlajka'
                        self.flags = str(int(self.flags) - 1)
                        self.ids.vlajky.text = self.flags
                        self.overwrite()
                    else:
                        pass
                        
                    
                        
            if y_cor > 0.8:
                if x/sx > 0.5:
                    
                    self.tool = 'lopata'
                    self.ids.state.text = 'loptata'
                else:
                    
                    self.tool = 'vlajka'
                    self.ids.state.text = 'vlajka'
        win = self.check_win()
        if win:
            self.show_popup_win()
            self.win()

    def win(self):
        f = open('score.json', 'r')

        data = json.load(f)
        f.close()
        d = self.current_difficulty
        score = self.time
        if data[d] == 'n':
            data[d] = score
        else:
            
            if data[d] > score:
                data[d] = score
               
        jsonFile = open("score.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
         


    def show_popup_lost(self, d):
        show = P(self)
        show.open()
        Clock.unschedule(self.update)

    def show_popup_win(self):
        show = W(self)
        show.open()
        Clock.unschedule(self.update)

    def check_win(self):
        
        if self.flags == '0':
            for y,line in enumerate(self.map.sight):
                for x,tile in enumerate(line):
                    if tile == 'vlajka':
                        if self.map.grid[y][x] != 'mine':
                            return False
                    if tile == 'n':
                        return False
            return True
        return False





kv = Builder.load_file('toomo.kv')
class Start(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    Start().run()