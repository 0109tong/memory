import simplegui
import random

WIDTH = 400
HEIGHT = 400
tile_num = input('number of tiles?')
tile_num = int(tile_num)
tile_width = 40
tiles ={}
tile_pos = []
tile_keylist= []
tile_numlist = []
t = 0
num = 0
click = 0
first_tile_i = False 
second_tile_i = False
bool = False
tile_val = 0
tile_val_sec = 0
first_pos = 0
current_pos = 0

class Tile :
    def __init__ (self,cor,exp,num):
        self.cor = cor
        self.exposed = exp
        self.num = num

    def is_exposed(self):
        if self.exposed is True:
            return True
        else:
            return False

    def expose(self):
        self.exposed = True

    def hide(self):
        self.exposed = False

    def in_range(self,mpos):
        global tile_width
        up = self.cor[1] 
        down = self.cor[1] + tile_width
        left = self.cor[0] 
        right = self.cor[0] + tile_width
        if left<mpos[0]<right and up<mpos[1]<down:
            return True

    def get_pointlist (self):
        global tile_width
        a = self.cor[0]
        b = self.cor[1] 
        p = [(a,b),(a+tile_width,b),(a+tile_width,b+tile_width),(a,b+tile_width)]
        return p 

    def get_num (self):
        n = self.num
        return n

    def get_num_point (self):
        global tile_width
        a = self.cor[0]
        b = self.cor[1]
        p = (a+(tile_width)/2,b+(tile_width)/2)
        return p

    def get_cor (self):
        s = self.cor
        return s

# create a list of keys for the tiles
def create_keylist():
    global tile_keylist,tile_num,num
    for i in range (0,tile_num*2):
        tile_keylist.append(num)
        num+=1

# create a list of tile values
def create_numlist():
    global tile_numlist,tile_num
    num = 1
    for i in range (0,tile_num):
        tile_numlist.append(num)
        num+=1

def create_numlist_2():
    global tile_numlist,tile_num
    num = 1
    for i in range (0,tile_num):
        tile_numlist.append(num)
        num+=1

# creating positions for the tiles
def create_pos ():
    global tile_pos, tile_num,tile_width
    pos = [0,0]
    p1 = pos[0]
    p2 = pos[1]
    for i in range(0,tile_num*2):
        p = [p1,p2]
        tile_pos.append(p)
        if p1 < WIDTH-tile_width:
            p1 += tile_width
        else:
            p2 += tile_width
            p1 = 0

#creating the actual tiles
def create_tiles ():
    global tile_pos, tile_num, tiles, tile_numlist
    for i in tile_keylist:
        #gets a random position from tile_pos
        pos = random.choice(tile_pos)
        #gets a random number from tile_numlist
        num = random.choice(tile_numlist)
        
        #creates a tile object in tiles dict
        tiles[i] = Tile(pos,False,num)
        tile_pos.remove(pos)
        tile_numlist.remove(num)

def reset ():
    global tile_keylist,tile_numlist,tile_pos,tiles 
    tile_keylist = []
    tile_numlist = []
    tile_pos = []
    tiles = {}


def draw (canvas):
    for i in tile_keylist:
        p = tiles[i].get_pointlist()
        canvas.draw_polygon(p,2,'blue','white')
        if tiles[i].is_exposed() is True:
            p = tiles[i].get_num_point()
            n = tiles[i].get_num()
            canvas.draw_text(str(n),p,10,'red')
        
    canvas.draw_text(str(t),(WIDTH-10,HEIGHT-10),10,'white')

def mouseclick (pos):
    global tile_keylist,click,first_tile_i,second_tile_i,bool,tile_val,tile_val_sec,first_pos,current_pos
    tile_num = 0
    
    if click == 2:
                tiles[second_tile_i].hide()
                tiles[first_tile_i].hide()
                click = 0
                bool = True
                
    for i in tile_keylist:
        if tiles[i].in_range(pos) and click == 0 and bool is False:
            #first click on a tile
            click += 1
            tile_val = tiles[i].get_num()
            first_pos = tiles[i].get_cor()
            first_tile_i = i
            tiles[i].expose()
            print tile_val
        
        elif tiles[i].in_range(pos) and click == 1 :
            #second click
            tiles[i].expose()
            current_pos = tiles[i].get_cor()
            tile_val_sec = tiles[i].get_num()
            second_tile_i = i
            print tile_val_sec
            print tile_val
            print first_pos
            print current_pos
            if first_pos is not current_pos and tile_val == tile_val_sec :
                tile_keylist.remove(i)
                tile_keylist.remove(first_tile_i)
                tiles.pop(i)
                tiles.pop(first_tile_i)
                click = 2
                print 'done'
            elif first_pos is not current_pos:
                click = 2      
    bool = False



def timer ():
    global t 
    t+=1

def start ():
    reset()
    create_keylist()
    create_numlist()
    create_numlist_2()
    create_pos()
    create_tiles()








frame = simplegui.create_frame('move ball',WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)
frame.add_button('start',start)
timer = simplegui.create_timer(1000,timer)

frame.start()
timer.start()