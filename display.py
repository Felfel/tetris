import random 
import pygame
import math 
import constants
import models
import shelve
import dbm.dumb

screen_x_size = 800
screen_y_size = 600
size = (screen_x_size, screen_y_size)
pygame.display.set_caption("Cool Game")
screen = pygame.display.set_mode(size)
screen_no = constants.MAIN
PI = 3.141592653
events = [] 
class Display():
    cursor = constants.load_image("cursor1.png")
    def __init__(self): pass
    def left_mousebtn(self): pass
    def key_down(self): pass
    def key_up(self): pass
    def key_right(self): pass
    def key_left(self): pass
    def key_enter(self): pass
    def key_down_upd(self): pass 
    def draw(self): pass
    def logic(self): pass
    def key_esc(self): pass
    def timer_event(self):pass
    def p_key(self): pass
    def speaker_event(self): pass
    def update_music(self): pass

class DisplayMain(Display):
    def __init__(self, game): 
            
        self.bg_list = [constants.load_image("main_bg1.jpg").convert(), constants.load_image("main_bg2.jpg").convert(), constants.load_image("main_bg3.jpg").convert()]
        self.bg_no = 0
        self.bg = self.bg_list[0]
        self.speaker = models.Speaker(screen, 700, 20, constants.MUSIC_LIST[constants.MAIN])
        self.gamejolt = models.Gj(screen, 55, 30)
        new_key = models.MenuItem("newgame_text.png", True, (295,209), (275, 185) )
        con_key = models.MenuItem("continue_text.png", False, (300,305), (275, 280), True )
        high_score = models.MenuItem("high_score_text.png", False, (295,398), (275, 375) )
        ex_key = models.MenuItem("exit_text.png", False, (350,490), (275,470) )
        self.menu = models.Menu(screen, [ new_key, con_key, high_score, ex_key ])
        self.cursor = Display.cursor
        self.game = game
        self.title = constants.load_image("tetris.png")
        pygame.time.set_timer(25, 500)
        
    def left_mousebtn(self):
        if not self.gamejolt.opened:
            if self.menu.check_mouse(self.mouse_pos):
                self.key_enter()
            else :
                self.speaker.check_mouse(self.mouse_pos)
                self.gamejolt.check_mouse(self.mouse_pos)
            
    def key_down(self):
        if not self.gamejolt.opened:
            self.menu.key_down()
        
    def key_up(self):
        if not self.gamejolt.opened:
            self.menu.key_up()
        
    def key_enter(self):
        if self.gamejolt.opened:
            self.gamejolt.login()
        else:
            global screen_no
            screen_no = self.menu.get_pos()
        
    def draw(self):
        screen.blit(self.bg, [0,0]) 
        self.speaker.draw()
        self.menu.draw()
        self.gamejolt.draw()
        screen.blit(self.title, (227,15))
        screen.blit(self.cursor, (self.mouse_pos[0], self.mouse_pos[1]) )

    def logic(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if not self.gamejolt.opened:
            self.menu.check_mouse(self.mouse_pos)
            status = self.game.get_status()
            if status == constants.PLAYING or status == constants.PUASED:
                self.menu.item_list[1].enable()
            else:
                self.menu.item_list[1].disable()
        else:
            self.gamejolt.logic(events)
            
    def timer_event(self):
        self.bg_no = (self.bg_no +1) % 3
        self.bg = self.bg_list[self.bg_no]
        pygame.time.set_timer(25, 300)
  
    def speaker_event(self):
        self.speaker.timer()
    
    def update_music(self):
        self.speaker.update_music()
    def key_esc(self):
        if self.gamejolt.opened:
            self.gamejolt.opened = False
class DisplayGame(Display):
    def __init__(self):
              
        self.speaker = models.Speaker(screen, 615, 290, constants.MUSIC_LIST[constants.NEW])
        self.bg = constants.load_image("game_bg.jpg").convert()
        self.block1 = constants.load_image("block1.png")
        self.block2 = constants.load_image("block2.png")
        self.block3 = constants.load_image("block3.png")
        self.next_text = constants.load_image("next_text.png")
        self.cursor = Display.cursor
        self.score_text = constants.load_image("score.png")
        self.block_controler = models.BlockControler()
        self.block_controler.initiate()
        self.puase_img = constants.load_image("puase.png")
        self.lost_img = constants.load_image("lost.png")
        self.status = None
        
    def draw(self): 
        screen.blit(self.bg, [0,0])
        screen.blit(self.block1, [50,34])
        screen.blit(self.block2, [550,34])
        screen.blit(self.block3, [575,100])
        screen.blit(self.next_text, [605,60])
        screen.blit(self.score_text, [588,375])
        self.speaker.draw()
        self.block_controler.draw(screen)
        screen.blit(self.cursor, (self.mouse_pos[0], self.mouse_pos[1]))
        if self.status == constants.PUASED : screen.blit(self.puase_img, [0,0])
        if self.status == constants.LOST : screen.blit(self.lost_img, [0,0])
        
        
    def logic(self):
        if self.status == constants.PLAYING:
            self.mouse_pos = pygame.mouse.get_pos()
            self.block_controler.update()
            if self.block_controler.game_done() :
                self.status = constants.LOST
                self.save_score()
                
    def save_score(self):
        d = shelve.open('info')
        score = self.block_controler.get_score()
        try:
            info = d['info']
        except:
            info = []
            
        if len(info) < 5:
            info.extend([0]*(5-len(info)))
            
        for i in range(5):
            if score > info[i]:
                for j in range(4, i, -1):
                    info[j] = info[j-1]
                info[i] = score
                break
        d['info'] = info
        d.close()        

    def new_game(self):
        self.block_controler = models.BlockControler([])
        self.block_controler.initiate() 
        self.status = constants.PLAYING
        
    def key_right(self):
        if self.status == constants.PLAYING:
            self.block_controler.move_right()
    def key_left(self):
        if self.status == constants.PLAYING:
            self.block_controler.move_left()   
    def key_down(self):
        if self.status == constants.PLAYING:
            self.block_controler.move_down()
    def key_down_upd(self):
        if self.status == constants.PLAYING:
            self.block_controler.restore_spd()
    def key_up(self):
        if self.status == constants.PLAYING:
            self.block_controler.key_up()
    def key_esc(self):
        global screen_no
        screen_no = constants.MAIN    
    def p_key(self):
        if self.status == constants.PLAYING:
            self.status = constants.PUASED    
        else:
            if self.block_controler.game_done() :
                self.status = constants.LOST
            else:
                self.status = constants.PLAYING
    def get_status(self):
        return self.status
    def speaker_event(self):
        self.speaker.timer()
    def update_music(self):
        self.speaker.update_music()    
    def left_mousebtn(self):
        self.speaker.check_mouse(self.mouse_pos)    
        
class DisplayScore(DisplayMain):
    def __init__(self):
        self.bg_list = [constants.load_image("main_bg1.jpg").convert(), constants.load_image("main_bg2.jpg").convert(), constants.load_image("main_bg3.jpg").convert()]
        self.bg_no = 0
        self.bg = self.bg_list[0]
        back_key = models.MenuItem("back_text.png", False, (335,500), (275,480) )
        self.menu = models.Menu(screen, [ back_key ])
        self.cursor = Display.cursor
        self.score_block_img = constants.load_image("score_block.png")
        pygame.time.set_timer(25, 500)  
    
    def logic(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.menu.check_mouse(self.mouse_pos)   
        d = shelve.open('info')
        try :
            self.score = d['info']
        except:
            self.score = [0]*5
        d.close()        
        
    def draw(self):
        screen.blit(self.bg, [0,0]) 
        self.menu.draw()                
        screen.blit(self.score_block_img, (175, 95))
        font = constants.load_font("LithosPro", 32) 
        for i in range(5):   
            n = font.render(str(i+1)+" - ", 1, constants.LIGHT_BLUE)
            label = font.render(str(self.score[i]), 1, constants.LIGHT_BLUE)
            s = label.get_rect().size     
            screen.blit(n, (200, 150 + (50*i) - s[1]/2))
            screen.blit(label, ( 400 - s[0]/2, 150 + (50*i) - s[1]/2))   
        screen.blit(self.cursor, (self.mouse_pos[0], self.mouse_pos[1]))
                    
    def key_enter(self):
        global screen_no
        screen_no = constants.MAIN   
    def left_mousebtn(self):
        if self.menu.check_mouse(self.mouse_pos):
            self.key_enter()   
            
    def key_esc(self):
        self.key_enter()     
    def speaker_event(self):
        pass
    
    def update_music(self):
        pass