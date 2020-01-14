import pygame
import os
import pygame.freetype
import random
from pygame import *


SCREEN_SIZE = (600, 450)

LEFT_UP = [[60, 120], [90, 140], [120, 160]]
LEFT_DOWN = [[60, 260], [90, 275], [120, 290]]
RIGHT_UP = [[520, 120], [495, 135], [460, 160]]
RIGHT_DOWN = [[520, 260], [495, 270], [460, 290]]
count_of_eggs = 0

screen = pygame.display.set_mode(SCREEN_SIZE)


class Egg(pygame.sprite.Sprite):
    def __init__(self, *groups):
        sprite.Sprite.__init__(self)

    def draw(self):
        pass

    def get_coords(self):
        global count_of_eggs
        count_of_eggs += 1
        place = random.randint(1, 4)
        if place == 1:
            return LEFT_UP[0]
        elif place == 2:
            return LEFT_DOWN[0]
        elif place == 3:
            return RIGHT_UP[0]
        elif place == 4:
            return RIGHT_DOWN[0]


def egg_cought(list_name, body, arms):
    if list_name == LEFT_UP and body == 'left' and arms == 'up':
        return True
    elif list_name == LEFT_DOWN and body == 'left' and arms == 'down':
        return True
    elif list_name == RIGHT_UP and body == 'right' and arms == 'up':
        return True
    elif list_name == RIGHT_DOWN and body == 'right' and arms == 'down':
        return True
    else:
        return False
