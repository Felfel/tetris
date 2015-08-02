# input lib
from pygame.locals import *
import pygame, string
import constants

class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class Input:
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font', 'pygame.font.Font(None, 32)'],
                              ['color', '(0,0,0)'], ['restricted', '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt1', '\'\''], ['prompt2', '\'\''])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt1 = self.options.prompt1
        self.prompt2 = self.options.prompt2
        self.values = ['','']
        self.no = 0
        self.shifted = False
        self.box = [constants.load_image("text_box.png"), constants.load_image("text_box2.png")]

    def set_pos(self, x, y):
        """ Set the position to x, y """
        self.x = x
        self.y = y

    def set_font(self, font):
        """ Set the font for the input """
        self.font = font

    def draw(self, surface):
        """ Draw the text input to a surface """
        text1 = self.font.render(self.prompt1+self.values[0], 1, self.color)
        surface.blit(self.box[self.no], (self.x, self.y))
        surface.blit(text1, (self.x+10, self.y+17))
        text2 = self.font.render(self.prompt2+self.values[1], 1, self.color)
        surface.blit(self.box[(self.no+1)%2], (self.x, self.y+100))
        surface.blit(text2, (self.x+10, self.y+117))        
        
    def update(self, events):
        """ Update the input based on passed events """
        for event in events:
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE: self.values[self.no] = self.values[self.no][:-1]
                elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                elif event.key == K_SPACE: self.values[self.no] += ' '
                elif event.key == K_TAB: 
                    self.no = (self.no + 1 ) % 2
                if not self.shifted:
                    if event.key == K_a and 'a' in self.restricted: self.values[self.no] += 'a'
                    elif event.key == K_b and 'b' in self.restricted: self.values[self.no] += 'b'
                    elif event.key == K_c and 'c' in self.restricted: self.values[self.no] += 'c'
                    elif event.key == K_d and 'd' in self.restricted: self.values[self.no] += 'd'
                    elif event.key == K_e and 'e' in self.restricted: self.values[self.no] += 'e'
                    elif event.key == K_f and 'f' in self.restricted: self.values[self.no] += 'f'
                    elif event.key == K_g and 'g' in self.restricted: self.values[self.no] += 'g'
                    elif event.key == K_h and 'h' in self.restricted: self.values[self.no] += 'h'
                    elif event.key == K_i and 'i' in self.restricted: self.values[self.no] += 'i'
                    elif event.key == K_j and 'j' in self.restricted: self.values[self.no] += 'j'
                    elif event.key == K_k and 'k' in self.restricted: self.values[self.no] += 'k'
                    elif event.key == K_l and 'l' in self.restricted: self.values[self.no] += 'l'
                    elif event.key == K_m and 'm' in self.restricted: self.values[self.no] += 'm'
                    elif event.key == K_n and 'n' in self.restricted: self.values[self.no] += 'n'
                    elif event.key == K_o and 'o' in self.restricted: self.values[self.no] += 'o'
                    elif event.key == K_p and 'p' in self.restricted: self.values[self.no] += 'p'
                    elif event.key == K_q and 'q' in self.restricted: self.values[self.no] += 'q'
                    elif event.key == K_r and 'r' in self.restricted: self.values[self.no] += 'r'
                    elif event.key == K_s and 's' in self.restricted: self.values[self.no] += 's'
                    elif event.key == K_t and 't' in self.restricted: self.values[self.no] += 't'
                    elif event.key == K_u and 'u' in self.restricted: self.values[self.no] += 'u'
                    elif event.key == K_v and 'v' in self.restricted: self.values[self.no] += 'v'
                    elif event.key == K_w and 'w' in self.restricted: self.values[self.no] += 'w'
                    elif event.key == K_x and 'x' in self.restricted: self.values[self.no] += 'x'
                    elif event.key == K_y and 'y' in self.restricted: self.values[self.no] += 'y'
                    elif event.key == K_z and 'z' in self.restricted: self.values[self.no] += 'z'
                    elif event.key == K_0 and '0' in self.restricted: self.values[self.no] += '0'
                    elif event.key == K_1 and '1' in self.restricted: self.values[self.no] += '1'
                    elif event.key == K_2 and '2' in self.restricted: self.values[self.no] += '2'
                    elif event.key == K_3 and '3' in self.restricted: self.values[self.no] += '3'
                    elif event.key == K_4 and '4' in self.restricted: self.values[self.no] += '4'
                    elif event.key == K_5 and '5' in self.restricted: self.values[self.no] += '5'
                    elif event.key == K_6 and '6' in self.restricted: self.values[self.no] += '6'
                    elif event.key == K_7 and '7' in self.restricted: self.values[self.no] += '7'
                    elif event.key == K_8 and '8' in self.restricted: self.values[self.no] += '8'
                    elif event.key == K_9 and '9' in self.restricted: self.values[self.no] += '9'
                    elif event.key == K_BACKQUOTE and '`' in self.restricted: self.values[self.no] += '`'
                    elif event.key == K_MINUS and '-' in self.restricted: self.values[self.no] += '-'
                    elif event.key == K_EQUALS and '=' in self.restricted: self.values[self.no] += '='
                    elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.values[self.no] += '['
                    elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.values[self.no] += ']'
                    elif event.key == K_BACKSLASH and '\\' in self.restricted: self.values[self.no] += '\\'
                    elif event.key == K_SEMICOLON and ';' in self.restricted: self.values[self.no] += ';'
                    elif event.key == K_QUOTE and '\'' in self.restricted: self.values[self.no] += '\''
                    elif event.key == K_COMMA and ',' in self.restricted: self.values[self.no] += ','
                    elif event.key == K_PERIOD and '.' in self.restricted: self.values[self.no] += '.'
                    elif event.key == K_SLASH and '/' in self.restricted: self.values[self.no] += '/'
                elif self.shifted:
                    if event.key == K_a and 'A' in self.restricted: self.values[self.no] += 'A'
                    elif event.key == K_b and 'B' in self.restricted: self.values[self.no] += 'B'
                    elif event.key == K_c and 'C' in self.restricted: self.values[self.no] += 'C'
                    elif event.key == K_d and 'D' in self.restricted: self.values[self.no] += 'D'
                    elif event.key == K_e and 'E' in self.restricted: self.values[self.no] += 'E'
                    elif event.key == K_f and 'F' in self.restricted: self.values[self.no] += 'F'
                    elif event.key == K_g and 'G' in self.restricted: self.values[self.no] += 'G'
                    elif event.key == K_h and 'H' in self.restricted: self.values[self.no] += 'H'
                    elif event.key == K_i and 'I' in self.restricted: self.values[self.no] += 'I'
                    elif event.key == K_j and 'J' in self.restricted: self.values[self.no] += 'J'
                    elif event.key == K_k and 'K' in self.restricted: self.values[self.no] += 'K'
                    elif event.key == K_l and 'L' in self.restricted: self.values[self.no] += 'L'
                    elif event.key == K_m and 'M' in self.restricted: self.values[self.no] += 'M'
                    elif event.key == K_n and 'N' in self.restricted: self.values[self.no] += 'N'
                    elif event.key == K_o and 'O' in self.restricted: self.values[self.no] += 'O'
                    elif event.key == K_p and 'P' in self.restricted: self.values[self.no] += 'P'
                    elif event.key == K_q and 'Q' in self.restricted: self.values[self.no] += 'Q'
                    elif event.key == K_r and 'R' in self.restricted: self.values[self.no] += 'R'
                    elif event.key == K_s and 'S' in self.restricted: self.values[self.no] += 'S'
                    elif event.key == K_t and 'T' in self.restricted: self.values[self.no] += 'T'
                    elif event.key == K_u and 'U' in self.restricted: self.values[self.no] += 'U'
                    elif event.key == K_v and 'V' in self.restricted: self.values[self.no] += 'V'
                    elif event.key == K_w and 'W' in self.restricted: self.values[self.no] += 'W'
                    elif event.key == K_x and 'X' in self.restricted: self.values[self.no] += 'X'
                    elif event.key == K_y and 'Y' in self.restricted: self.values[self.no] += 'Y'
                    elif event.key == K_z and 'Z' in self.restricted: self.values[self.no] += 'Z'
                    elif event.key == K_0 and ')' in self.restricted: self.values[self.no] += ')'
                    elif event.key == K_1 and '!' in self.restricted: self.values[self.no] += '!'
                    elif event.key == K_2 and '@' in self.restricted: self.values[self.no] += '@'
                    elif event.key == K_3 and '#' in self.restricted: self.values[self.no] += '#'
                    elif event.key == K_4 and '$' in self.restricted: self.values[self.no] += '$'
                    elif event.key == K_5 and '%' in self.restricted: self.values[self.no] += '%'
                    elif event.key == K_6 and '^' in self.restricted: self.values[self.no] += '^'
                    elif event.key == K_7 and '&' in self.restricted: self.values[self.no] += '&'
                    elif event.key == K_8 and '*' in self.restricted: self.values[self.no] += '*'
                    elif event.key == K_9 and '(' in self.restricted: self.values[self.no] += '('
                    elif event.key == K_BACKQUOTE and '~' in self.restricted: self.values[self.no] += '~'
                    elif event.key == K_MINUS and '_' in self.restricted: self.values[self.no] += '_'
                    elif event.key == K_EQUALS and '+' in self.restricted: self.values[self.no] += '+'
                    elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.values[self.no] += '{'
                    elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.values[self.no] += '}'
                    elif event.key == K_BACKSLASH and '|' in self.restricted: self.values[self.no] += '|'
                    elif event.key == K_SEMICOLON and ':' in self.restricted: self.values[self.no] += ':'
                    elif event.key == K_QUOTE and '"' in self.restricted: self.values[self.no] += '"'
                    elif event.key == K_COMMA and '<' in self.restricted: self.values[self.no] += '<'
                    elif event.key == K_PERIOD and '>' in self.restricted: self.values[self.no] += '>'
                    elif event.key == K_SLASH and '?' in self.restricted: self.values[self.no] += '?'

        if len(self.values[self.no]) > self.maxlength and self.maxlength >= 0: self.values[self.no] = self.values[self.no][:-1]
