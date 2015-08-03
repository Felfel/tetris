import pygame
import random
import constants
import math
import shelve
import dbm.dumb
import eztext
import gjapi
import _thread 

pygame.init()
pygame.display.set_mode([800,600])
x_s = 22
y_s = 22
x_low_limit = 55
x_upr_limit = 495
y_low_limit = 39
y_upr_limit = 545
x_midpoint = x_low_limit + (10*x_s)
start_speed = 2
speed = 2

def prepare_alpha(source,  opacity):
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    return temp

class Block():
    # Frames for explosion animation
    explode_img = [constants.load_image("frame8.png").convert(), constants.load_image("frame7.png").convert(), 
                   constants.load_image("frame6.png").convert(), constants.load_image("frame5.png").convert(), 
                   constants.load_image("frame4.png").convert(), constants.load_image("frame3.png").convert(), 
                   constants.load_image("frame2.png").convert(), constants.load_image("frame1.png").convert() ]
    
    def __init__(self, x, y, img, y_spd, s = False):
        self.x_pos = x
        self.y_pos = y
        self.img = img
        self.y_spd = y_spd
        self.ori_spd = y_spd
        self.special = s
      
    # Check if the block entered the playing area or not yet  
    def drawable(self):
        return self.y_pos >= y_low_limit    
    # Bilt the block to screen
    def draw(self, screen, x = None, y = None):
        if x == None :
            x = self.x_pos
        if y == None :
            y = self.y_pos
        screen.blit(self.img, [x, y])
        
    # Update block's position using it's speed
    def update_pos(self):
        self.y_pos += self.y_spd
        
    # Change block's speed
    def update_speed(self, y):
        self.y_spd = y
    
    # Restore the original speed given to the block at it's creation
    def restore_speed(self):
        self.y_spd = self.ori_spd
    
    # Stop the block
    def stop(self):
        self.update_speed(0)
    
    # Draw the block with a frame of the explosion
    def explode(self,screen, n):
        screen.blit(Block.explode_img[n], [self.x_pos, self.y_pos])
    
    # Move the block one step right    
    def move_right(self):
        self.x_pos += x_s
    
    # Move the block one step left
    def move_left(self):
        self.x_pos -= x_s
    
    # Get X position of the block    
    def get_x(self):
        return self.x_pos
    
    # Get Y position of the block 
    def get_y(self):
        return self.y_pos
    # Set the position of X
    def set_x(self, x):
        self.x_pos = x
    # Change X's position with a magnitude    
    def trans_x(self, x):
        self.x_pos += x
    # Set the position of Y
    def set_y(self, y):
        self.y_pos = y
    # Change Y's position with a magnitude    
    def trans_y(self, y):
        self.y_pos += y
 
    
class BlockObject():
    # Images used to create blocks
    i_block1 = constants.load_image("i_block.png").convert()
    j_block1 = constants.load_image("j_block.png").convert()
    o_block1 = constants.load_image("o_block.png").convert()
    z_block1 = constants.load_image("z_block.png").convert()
    t_block1 = constants.load_image("t_block.png").convert()
    sp_block1 = constants.load_image("special_block.png").convert()
    
    # Block objects images for instant blit on the screen
    next_block = [constants.load_image("i_next.png").convert(), constants.load_image("j_next.png"),
                  constants.load_image("o_next.png").convert(), constants.load_image("z_next.png"),
                  constants.load_image("t_next.png"), constants.load_image("special_block.png").convert()] 
    
    def __init__(self):
        self.next_list = []
        self.moving_list = []
        self.variation = None
        self.rtype = None
        self.ntype = None
        self.special = None
        # Mapping functions to spawn objects using type and variation of the object
        self.dic = {0: {0:self.add_i_v1, 1:self.add_i_v2 ,2:self.add_i_v1 ,3:self.add_i_v2},
                    1: {0:self.add_j_v1, 1:self.add_j_v2 ,2:self.add_j_v3 ,3:self.add_j_v4},
                    2: {0:self.add_o, 1:self.add_o, 2:self.add_o, 3:self.add_o},
                    3: {0:self.add_z_v1, 1:self.add_z_v2 ,2:self.add_z_v1 ,3:self.add_z_v2},
                    4: {0:self.add_t_v1, 1:self.add_t_v2 ,2:self.add_t_v3 ,3:self.add_t_v4}} 
        # Mapping functions to help replace variotaions
        self.pos = {0: self.get_i, 1: self.get_j, 2: self.get_o, 3: self.get_z, 4: self.get_t}         

    # This current moving object is taken from the 'previous' next object, the next object
    # gets a new random object
    def new_object(self):
        # Spawn a special block object with 1/2o chance
        if random.randint(0,20) == 20:
            self.rtype = self.ntype
            self.ntype = 5
            self.variation = 0
            self.moving_list = self.next_list
            self.next_list = [Block( x_midpoint, y_low_limit , BlockObject.sp_block1, speed)]  
        # Spawn a typical block object
        else: 
            temp = random.randint(0, 4)
            self.rtype = self.ntype
            self.ntype = temp
            self.variation = 0
            self.moving_list = self.next_list
            self.next_list = self.dic[self.ntype][0]()
        self.special = (self.rtype == 5)
          
    # Functions to add 'I' Blocks and it's vartiations
    def add_i_v1(self, x= x_midpoint, y= y_low_limit - y_s): 
        blocks = [0,0,0,0]
        for i in range(4):
            blocks[i] = Block( x, y -(i*y_s) , BlockObject.i_block1, speed)
        return blocks
    def add_i_v2(self, x = (x_midpoint - (2 * x_s) ), y= y_low_limit): 
        blocks = [0,0,0,0]
        for i in range(4):
            blocks[i] = Block( x + (i * x_s), y, BlockObject.i_block1, speed)
        return blocks      
    
    # Functions to add 'J' Blocks and it's vartiations
    def add_j_v1(self, x = x_midpoint - x_s, y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.j_block1, speed)
        for i in range(3):
            blocks[i+1] = Block( x + x_s , y-(i*y_s), BlockObject.j_block1, speed)
        return blocks
    def add_j_v2(self, x = x_midpoint - x_s, y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        for i in range(3):
            blocks[i] = Block( x + (i* x_s) , y, BlockObject.j_block1, speed)
        blocks[3] = Block( x , y - y_s, BlockObject.j_block1, speed)
        return blocks    
    def add_j_v3(self, x = x_midpoint - x_s, y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        for i in range(3):
            blocks[i] = Block( x , y-(i*y_s), BlockObject.j_block1, speed)
        blocks[3] = Block( x + x_s , y - 2 * y_s, BlockObject.j_block1, speed)
        return blocks
    def add_j_v4(self, x = x_midpoint - x_s, y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        for i in range(3):
            blocks[i+1] = Block( x - (i* x_s) , y, BlockObject.j_block1, speed)
        blocks[0] = Block( x , y+y_s, BlockObject.j_block1, speed)
        return blocks             

    # Functions to add 'O' Blocks and no variations OBVIOUSLY
    def add_o(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.o_block1, speed)
        blocks[1] = Block( x - x_s , y, BlockObject.o_block1, speed)
        blocks[2] = Block( x , y - y_s, BlockObject.o_block1, speed) 
        blocks[3] = Block( x - x_s , y - y_s, BlockObject.o_block1, speed) 
        return blocks     
    
    # Functions to add 'Z' Blocks and it's vartiations    
    def add_z_v1(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x + x_s , y, BlockObject.z_block1, speed)
        blocks[1] = Block( x , y, BlockObject.z_block1, speed)
        blocks[2] = Block( x , y - y_s, BlockObject.z_block1, speed) 
        blocks[3] = Block( x - x_s, y - y_s, BlockObject.z_block1, speed) 
        return blocks 
    def add_z_v2(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.z_block1, speed)
        blocks[1] = Block( x , y - y_s, BlockObject.z_block1, speed)
        blocks[2] = Block( x + x_s, y - y_s, BlockObject.z_block1, speed) 
        blocks[3] = Block( x + x_s, y - 2*y_s, BlockObject.z_block1, speed) 
        return blocks    
    
    # Functions to add 'T' Blocks and it's vartiations
    def add_t_v1(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.t_block1, speed)
        blocks[1] = Block( x , y - y_s, BlockObject.t_block1, speed)
        blocks[2] = Block( x - x_s, y - y_s, BlockObject.t_block1, speed) 
        blocks[3] = Block( x + x_s, y - y_s, BlockObject.t_block1, speed) 
        return blocks   
    def add_t_v2(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.t_block1, speed)
        blocks[1] = Block( x , y - y_s, BlockObject.t_block1, speed)
        blocks[2] = Block( x , y - 2*y_s, BlockObject.t_block1, speed) 
        blocks[3] = Block( x - x_s, y - y_s, BlockObject.t_block1, speed) 
        return blocks     
    def add_t_v3(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.t_block1, speed)
        blocks[1] = Block( x + x_s, y, BlockObject.t_block1, speed)
        blocks[2] = Block( x - x_s, y, BlockObject.t_block1, speed) 
        blocks[3] = Block( x , y - y_s, BlockObject.t_block1, speed) 
        return blocks     
    def add_t_v4(self, x = x_midpoint , y = y_low_limit - y_s): 
        blocks = [0,0,0,0]
        blocks[0] = Block( x , y, BlockObject.t_block1, speed)
        blocks[1] = Block( x , y - y_s, BlockObject.t_block1, speed)
        blocks[2] = Block( x , y - 2*y_s, BlockObject.t_block1, speed) 
        blocks[3] = Block( x + x_s, y - y_s, BlockObject.t_block1, speed) 
        return blocks
    
    # Update the positions of the current moving object
    def update(self):
        for b in self.moving_list:
            b.update_pos()  
    # Return the list of the blocks of the current moving object   
    def get_list(self):
        return self.moving_list
    
    # Stop the object, 
    #if it had already crossed a line bring it back and STOP IT
    def stop(self):
        for b in self.moving_list :
            b.stop()
            
    def transfer(self, x, y):
        for b in self.moving_list:
            b.trans_y(y)
            b.trans_x(x)
            
    # Blit an image of the next coming object in the 'Next' Area        
    def draw_next(self, screen):
        img = BlockObject.next_block[self.ntype]
        s = img.get_rect().size
        x = 650 - s[0]/2
        y = 175 - s[1]/2
        screen.blit(img , [x , y])    
        
    # Cuased by the down arrow key
    # Makes the object move faster
    def move_down(self):
            for b in self.moving_list:
                b.update_speed(speed*5)  
                
    # Cuased by releasing the down arrow key
    # Makes the objects move at it's own pace, peacefully
    def restore_spd(self):
        for b in self.moving_list:
            b.restore_speed()  
    
    # Move object one step right
    def move_right(self):
        for b in self.moving_list:
            b.move_right()
            
    # Move object one step left
    def move_left(self):
        for b in self.moving_list:
            b.move_left()    

    # Cuased by up arrow key
    # Try to transform object into next variation, pass results to Controler
    def change_v(self):
        if self.special:
            return (self.moving_list, self.variation)
        pos = self.pos[self.rtype]()
        v = (self.variation + 1) % 4
        l = self.dic[self.rtype][v](*pos)
        return (l,v)
    
    # If it's cool with the controler, it's cool with me!
    def ok(self, l, v):
        self.variation = v
        self.moving_list = l

    # Helper for I's transformations
    def get_i(self):
        if self.variation == 0 or self.variation == 2 :
            x = self.moving_list[0].get_x() - 2 * x_s
            y = self.moving_list[0].get_y()
        else:
            x = self.moving_list[0].get_x() + 2 * x_s
            y = self.moving_list[3].get_y()   
        return (x, y) 
    
    # Helper for J's transformations
    def get_j(self):
        if self.variation == 0:
            x = self.moving_list[0].get_x() -  x_s
            y = self.moving_list[0].get_y()
        elif self.variation == 1:
            x = self.moving_list[0].get_x() + 2 * x_s
            y = self.moving_list[0].get_y()   
        elif self.variation == 2:
            x = self.moving_list[0].get_x() + x_s
            y = self.moving_list[0].get_y()   
        elif self.variation == 3:
            x = self.moving_list[0].get_x() - 2 * x_s
            y = self.moving_list[0].get_y()           
        return (x, y)  
    
    # Do nothing, just make O objects feel not so deficient
    def get_o(self):
        return (self.moving_list[0].get_x(), self.moving_list[0].get_y())
    
    # Helper for Z's transformations
    def get_z(self):
        if self.variation == 0 or self.variation == 2 :
            x = self.moving_list[3].get_x() + x_s
            y = self.moving_list[0].get_y()
        else:
            x = self.moving_list[0].get_x() 
            y = self.moving_list[0].get_y()   
        return (x, y) 
    
    # Just like O's Helper
    def get_t(self):
        return (self.moving_list[0].get_x(), self.moving_list[0].get_y())        

# Control the moving objects, and the stable ones too
# After objects are stopped, they are treated as blocks instead of objects
# Also maintain score and such
class BlockControler():
    def __init__(self, block_list = []):
        self.score = 0
        self.add_score = 0
        self.stop_list = block_list
        self.to_remove_list = []
        # Only one moving object at a time
        self.moving_object = BlockObject()
        self.animate = 0
        self.lost = False
        self.grid = [[0 for x in range(20)] for x in range(23)] 
        self.c1 = 0
        
    # Tell Block object to move his ass and create a new one    
    def new_object(self):
        self.moving_object.new_object()
    
    # Create two new objects, one for currently moving and one for next, you are set to go.
    def initiate(self):
        self.new_object()
        self.new_object()
        self.c1 = 0
        self.c2 = 0        
    
    # Update positions, scores, check for collisions
    # If an animation is going on, hold back the updates
    def update(self):
        if self.animate == 0:
            self.score += self.add_score
            self.add_score = 0 
            self.to_remove_list = []
            self.update_grid()
            self.moving_object.update()
            self.check_collision()
            self.update_speed()
            
            
    def update_speed(self):
        global speed
        speed = start_speed + self.score // 4000
        if speed > 5 : speed = 5
        
    def update_grid(self):
        self.grid = [[0 for x in range(20)] for x in range(23)]
        for b in self.stop_list:
            x = (b.get_x() - x_low_limit) // 22
            y = (b.get_y() - y_low_limit) // 22
            self.grid[y][x] = 1
        
    # Take a list of blocks and check for collisions with 
    # other blocks, or lines
    def check(self,l):
        for b in l:
            x = (b.get_x() - x_low_limit) // 22
            y = (b.get_y() - y_low_limit) // 22
            # X limits
            con2 = x >= 0
            con3 = x < 20
            con4 = y < 23
            con5 = y >= 0
            if con2 and con3 and con4 and con5:
                if self.grid[y][x] == 1: 
                    return False
            else :
                return False
        return True
            
    # Check collisions between moving object and other blocks
    # Routine of the logical updating
    def check_collision(self):
        mlist = self.moving_object.get_list()
        for b in mlist : 
            x = (b.get_x() - x_low_limit) / 22
            y = (b.get_y() - y_low_limit) / 22
            x, y = math.ceil(x), math.ceil(y)
            # Y upper limit
            if y > 22:
                self.stop()
                return
            # Other blocks Y collision
            if y >= 0 and self.grid[y][x] == 1:
                self.stop()
                return            
     
    # In case of collision, stop the object, check for score, create a new object
    # Routine of the logical updating, if there is collision
    def stop(self):
        mlist = self.moving_object.get_list()
        y = (mlist[0].get_y() - y_low_limit) // 22
        y = y * 22 + y_low_limit
        self.moving_object.transfer(0, y - mlist[0].get_y())
        
        while not self.check(self.moving_object.get_list()):
            for b in self.moving_object.get_list():
                y = (b.get_y() - y_low_limit) // 22
                if y < 0:
                    self.lost = True
            if self.lost : 
                break
            self.moving_object.transfer(0, -22)
        self.moving_object.stop()
        drawable_list = [x for x in self.moving_object.get_list() if x.drawable()]
        if not self.lost:
            self.stop_list += drawable_list
            if self.moving_object.special :
                self.special_score()
            else:
                self.calculate_score()
            self.new_object()   
        else:
            add_list = []
            for b in drawable_list:
                x = (b.get_x() - x_low_limit) // 22
                y = (b.get_y() - y_low_limit) // 22
                if self.grid[y][x] == 0:
                    add_list.append(b)
            self.stop_list += add_list
        
    
    # Calculate score for a special block
    def special_score(self):
        # The line the special block has landed in
        b = self.moving_object.get_list()[0]
        line = (b.get_y() - y_low_limit) // 22
        # Number of blocks in this line
        self.to_remove_list = [x for x in self.stop_list if (x.get_y() - y_low_limit) // 22 == line]
        multiplier = len(self.to_remove_list)
        # 25 Score per block 
        self.add_score+= 25*multiplier
        # Delete the blocks in the line
        self.stop_list = [x for x in self.stop_list if (x.get_y() - y_low_limit) // 22 != line]
        # Shift down upper lines of blocks
        for bl in self.stop_list:
            if (bl.get_y() - y_low_limit) // 22 < line:
                bl.trans_y(y_s)          
        c = len(self.to_remove_list)
        if c > 0 : self.animate = 15; self.c1 += c
     
    # Calculate score for regular blocks       
    def calculate_score(self):
        arr = [0] * 23
        # Get number of blocks in each horizontal line
        for b in self.stop_list:
            arr[(b.get_y() - y_low_limit) // 22] += 1
        index = []
        for i in range(23) :
            if arr[i] == 20:
                self.add_score += 400
                # append the index of a completed line
                index.append(i)
          
        # Delete a line if it's complete      
        for i in index :
            self.to_remove_list += [x for x in self.stop_list if (x.get_y() - y_low_limit) // 22 == i]
            self.stop_list = [x for x in self.stop_list if (x.get_y() - y_low_limit) // 22 != i]
            # Move all upper remaining lines down
            for b in self.stop_list:
                if (b.get_y() - y_low_limit) // 22 < i:
                    b.trans_y(y_s)    
        # Got blocks to remove? raise the animation flag 
        c = len(self.to_remove_list)
        if c > 0 : self.animate = 15; self.c2 += c
    
    # Main draw function, draw blocks(actually tell them to draw themselves), animation
    def draw(self,screen):
        self.moving_object.draw_next(screen)
        # List of stopped blocks, and any moving block in the game area
        # ** Moving blocks are spawned above the game area, if they haven't 
        # ** entered yet, they are not drawn
        for b in self.stop_list:
            b.draw(screen)
        mlist = []
        if not self.lost :
            mlist = [ x for x in self.moving_object.get_list() if x.drawable()]
        for b in mlist:
            b.draw(screen)
        font = constants.load_font("LithosPro", 27)    
        label = font.render(str(self.score), 1, constants.LIGHT_BLUE)
        s = label.get_rect().size
        screen.blit(label, (651 - s[0]/2, 446 - s[1]/2))
        # Animation bitch
        if self.animate > 0:
            font = constants.load_font("LithosPro", 17)
            label = font.render("+"+str(self.add_score), 1, constants.LIGHT_BLUE)
            screen.blit(label, (651 + s[0]/2 + 3, 446 - s[1]/2 + 3))
            for b in self.to_remove_list:
                b.explode(screen, self.animate//2)             
            self.animate -= 1       
            
    # Tell the object to move right if it's legal, do nothing otherwise 
    # Cuased by right arrow key
    def move_right(self):
        mlist = self.moving_object.get_list()
        mlist = self.moving_object.get_list()
        for b in mlist :
            x = (b.get_x() - x_low_limit) / 22
            y = (b.get_y() - y_low_limit) / 22
            x, y = math.ceil(x), math.ceil(y)
            x += 1
            if x < 0 or x > 19:
                return
            elif self.grid[y][x] == 1:
                return
        self.moving_object.move_right()
    
    # Tell the object to move left if it's legal, do nothing otherwise   
    # Cuased by left arrow key
    def move_left(self):
        mlist = self.moving_object.get_list()
        for b in mlist :
            x = (b.get_x() - x_low_limit) / 22
            y = (b.get_y() - y_low_limit) / 22
            x, y = math.ceil(x), math.ceil(y)
            x -= 1
            if x < 0 or x > 19:
                return
            elif self.grid[y][x] == 1:
                return
        self.moving_object.move_left()
        
    # Cuased by down arrow key, speed up the object
    def move_down(self):
        self.moving_object.move_down()
    
    # Cuased by releasing down arrow key, restore object's pace
    def restore_spd(self):
        self.moving_object.restore_spd()
    
    # Transform object into another variation if this is legal
    def key_up(self):
        cc = self.moving_object.change_v()
        if self.check(cc[0]) :
            self.moving_object.ok(*cc)
     
    def get_score(self):
        return self.score + self.add_score
    
    def game_done(self):
        return self.lost
#-------------------------------------------------------------------------------        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Menu class to take care of the menu items
class Menu():
    def __init__(self, screen, item_list = []):
        self.item_list = item_list
        self.count = len(item_list)
        self.key_pos = 0
        self.screen = screen
     
    # Add a menu item   
    def add(self, item):
        self.item_list.append(item)
        self.count += 1
        
    # Draw menu items    
    def draw(self):
        for item in self.item_list:
            item.draw(self.screen)
     
    # Which item is highlightened 
    def get_pos(self):
        return self.key_pos
    
    # Highlight the item if mouse is hovering over it
    def check_mouse(self, pos):
        temp = self.hover(pos)
        if temp != -1 :
            self.key_pos = temp
            self.highlight()
            return True
        return False
     
    # Check if mouse is hovering over any item       
    def hover(self, pos):
        for i in range(self.count):
            if self.item_list[i].hover(pos[0], pos[1]):
                self.key_pos = i
                return i
        return -1
    
    # Highlight the item, using index stored
    def highlight(self):
        for item in self.item_list:
            item.unhighlight()
        self.item_list[self.key_pos].highlight()
    
    # Move to the next item in the list
    def key_down(self):
        self.key_pos = (self.key_pos + 1) % self.count
        while self.item_list[self.key_pos].disabled == True :
            self.key_pos = (self.key_pos + 1) % self.count
        self.highlight()
    
    # Move to the previous item in the list    
    def key_up(self):
        self.key_pos = (self.key_pos - 1) % self.count
        while self.item_list[self.key_pos].disabled == True :
            self.key_pos = (self.key_pos - 1) % self.count        
        self.highlight()

# Represtens a single item in the menu        
class MenuItem():
    
    dis = prepare_alpha(constants.load_image("button_disable.png"),  200)
    highlighted_btn = prepare_alpha(constants.load_image("highlighted_button.png"),  200)
    btn  = prepare_alpha(constants.load_image("button.png"),  200)
    
    def __init__(self, file, btn_high,text_pos, btn_pos, disabled = False):
        self.text = constants.load_image(file)
        self.text_position = text_pos
        self.btn_position = btn_pos
        self.disabled = disabled
        if btn_high :
            self.btn = MenuItem.highlighted_btn
        else:
            self.btn = MenuItem.btn
            
    def draw(self, screen):
        screen.blit(self.btn, self.btn_position)
        screen.blit(self.text, self.text_position)
        if self.disabled :
            screen.blit(MenuItem.dis, self.btn_position)
        
    def unhighlight(self):
        self.btn = MenuItem.btn
    def highlight(self):
        self.btn = MenuItem.highlighted_btn
    def disable(self):
        self.disabled = True
    def enable(self):
        self.disabled = False
    def hover(self, x, y):
        if self.disabled :
            return False
        size = self.btn.get_rect().size
        pos = self.btn_position
        return (x >= pos[0] and x <= pos[0] + size[0] and 
                  y >= pos[1] and y <= pos[1] + size[1])
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class Speaker():
    active = [constants.load_image("speaker1.png"), constants.load_image("speaker2.png")]
    mute = constants.load_image("speaker3.png")
    def __init__(self, screen, x, y, music):
        self.screen = screen
        self.x_pos = x
        self.y_pos = y
        self.music = music
        
        d = shelve.open('info')
        try:
            self.playing = d['sound']
        except:
            self.playing = True
        d.close()
        self.img_no = 0
        if self.playing:
            self.img = Speaker.active[0]
            #self.update_music()
            pygame.time.set_timer(26, 500)
        else:
            self.img = Speaker.mute

    def draw(self):
        self.screen.blit(self.img, (self.x_pos,self.y_pos))
    
    def logic(self):
        pass
    
    def check_mouse(self, pos):
        x, y = pos
        x2, y2 = Speaker.mute.get_rect().size
        con1 = x > self.x_pos
        con2 = x <= self.x_pos + x2
        con3 = y > self.y_pos
        con4 = y <= self.y_pos + y2
        if con1 and con2 and con3 and con4 :
            self.click()
        
    
    def update_music(self):
        d = shelve.open('info')
        try:
            self.playing = d['sound']
        except:
            pass
        d.close()        
        if self.playing:
            self.img = Speaker.active[0]
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1) 
            pygame.time.set_timer(26, 500)            
        else:
            self.img = Speaker.mute
            pygame.mixer.music.stop()    
            
    def click(self):
        self.playing = not self.playing
        d = shelve.open('info')
        d['sound'] = self.playing
        d.close()        
        self.update_music()
        
    def timer(self):
        if self.playing:
            self.img_no = (self.img_no + 1) % 2
            self.img = Speaker.active[self.img_no]
            pygame.time.set_timer(26, 500)
#------------------------------------------------------------------------------------
class Gj():
    logo = constants.load_image("gj_logo.png")
    btn = constants.load_image("gj_b1.png")
    btnh = constants.load_image("gj_b2.png")
    ov = constants.load_image("ov1.png")
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x_logo = x
        self.y_logo = y
        self.x_btn = x-30
        self.y_btn = y+70
        self.font = constants.load_font("LithosPro", 20)
        self.y_t = self.y_btn+10
        d = shelve.open('info')
        try :
            self.user, self.token = d['user'] 
        except:
            self.user, self.token = ('','')
        d.close()
        self.api = gjapi.GameJoltTrophy(self.user, self.token, constants.GAME_ID, constants.PRIVATE_KEY)
        #if self.api.authenticateUser():
            #self.logged = True
            #self.api.openSession()
            #self.btn =  Gj.btnh
            #self.text = self.font.render(self.user, 1, constants.BLACK) 
            #pygame.time.set_timer(27, 35000)            
        #else:
        self.logged = False
        self.btn = Gj.btn
        self.text = self.font.render("Offline", 1, constants.BLACK)
        _thread.start_new_thread(self.login, (self.user, self.token))
        self.opened = False
        options = {'x':150, 'y':200, 'font':self.font, 'color':constants.DLIGHT_BLUE,
                   'maxlength':25, 'prompt1':"Username:  ", 'prompt2':"Token:  "}
        self.txtbx = eztext.Input(**options)
        self.tip1 = self.font.render("- Tab to switch between text boxes", 1, constants.OFF_WHITE)
        self.tip2 = self.font.render("- Enter to login", 1, constants.OFF_WHITE)
        self.tip3 = self.font.render("- Esc to go back", 1, constants.OFF_WHITE)
        
    def draw(self):
        self.x_t = self.x_btn+60-self.text.get_rect().size[0]/2
        self.screen.blit(Gj.logo, (self.x_logo,self.y_logo))
        self.screen.blit(self.btn, (self.x_btn, self.y_btn))
        self.screen.blit(self.text, (self.x_t, self.y_t ))
        if self.opened:
            self.screen.blit(Gj.ov, (0,0)) 
            self.screen.fill(constants.BLACK, [150,400, 500, 70])
            self.screen.blit(self.tip1, (160, 405 ))
            self.screen.blit(self.tip2, (160, 425 ))
            self.screen.blit(self.tip3, (160, 445 ))
            self.txtbx.draw(self.screen)
            
    def logic(self, events):
        self.txtbx.update(events) 
    
    def key_enter(self):
        self.user, self.token = self.txtbx.get_text()
        _thread.start_new_thread(self.login, (self.user, self.token))
        
    def login(self, user, token):
        self.api.changeUsername(user)
        self.api.changeUserToken(token)
        if self.api.authenticateUser():
            d = shelve.open('info')
            d['user'] = (user, token)
            d.close()
            self.api.openSession()
            self.logged = True
            self.opened = False
            self.btn =  Gj.btnh
            self.text = self.font.render(self.user, 1, constants.BLACK) 
            pygame.time.set_timer(27, 35000)
        else:
            pygame.event.post(pygame.event.Event(28))
        
    def check_mouse(self, pos):
        x, y = pos
        x2, y2 = Gj.btn.get_rect().size
        con1 = x > self.x_btn
        con2 = x <= self.x_btn + x2
        con3 = y > self.y_btn
        con4 = y <= self.y_btn + y2
        if con1 and con2 and con3 and con4 :
            self.click()  
            
    def click(self):
        if self.logged:
            self.logged = False
            d = shelve.open('info')
            d['user'] = ('', '')
            d.close()            
            self.btn =  Gj.btn
            self.text = self.font.render("Offline", 1, constants.BLACK)            
        else:
            self.opened = True
#------------------------------------------------------------------------------------
# Unused
class Snow():
    def __init__(self, screen, x, y, total = 120, vel = 3):
        self.snow_list = []
        for i in range(total):
            snow_x = random.randrange(0, x)
            snow_y = random.randrange(0, y)
            new_snow = [ snow_x, snow_y ]
            self.snow_list.append(new_snow)   
        self.screen_y = y
        self.vel = vel
        self.screen = screen
    
    def draw(self):
        for i in range(len(self.snow_list)):
                self.snow_list[i][1] += random.randint(1, self.vel)
                self.snow_list[i][0] += random.randint(-1,1)
                if(self.snow_list[i][1] > self.screen_y):
                    self.snow_list[i][1] = random.randint(-200,0)
                pygame.draw.circle(self.screen, constants.WHITE, self.snow_list[i], 4)     
