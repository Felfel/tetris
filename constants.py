import os.path
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   100, 255,   100)
RED      = ( 255,   0,   0)
REDISH   = ( 214, 19, 2)
LIGHT_RED = ( 255, 150, 150)
OFF_WHITE = ( 220, 220, 220)
LIGHT_BLUE = ( 39, 240, 219)

MAIN = 19
NEW = 0
CONTINUE = 1
SCORE = 2
EXIT = 3

PLAYING = 125125
LOST = 682936
PUASED = 1242

SOUND = "sound"
IMAGE = "images"
FONT = "fonts"

MUSIC_LIST = [None]*20
MUSIC_LIST[NEW] = os.path.join(SOUND, "game_loop.ogg")
MUSIC_LIST[CONTINUE] = MUSIC_LIST[NEW]
MUSIC_LIST[MAIN] = os.path.join(SOUND,"main_loop.ogg")

def load_image(name):
    img = os.path.join(IMAGE, name)
    return pygame.image.load(img)

def load_font(name, size):
    font = os.path.join(FONT, name+".otf")
    return pygame.font.Font(font, size)