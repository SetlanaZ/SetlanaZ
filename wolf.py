import pygame
import os
import pygame.freetype
import random
from pygame import *

COORDS_BODY = (200, 100)
COORDS_ARMS = (0, 0)
SCREEN_SIZE = (600, 450)

screen = pygame.display.set_mode(SCREEN_SIZE)


class Wolf(pygame.sprite.Sprite):
    def __init__(self, *groups):
        sprite.Sprite.__init__(self)

    def draw(self, body='left', arms='down'):
        if body == 'left':
            screen.blit(image.load("data/wolf_left.png"), COORDS_BODY)
            if arms == 'down':
                screen.blit(image.load("data/Arms/left_down.png"), COORDS_ARMS)
            elif arms == 'up':
                screen.blit(image.load("data/Arms/left_up.png"), COORDS_ARMS)
        elif body == 'right':
            screen.blit(image.load("data/wolf_right.png"), COORDS_BODY)
            if arms == 'down':
                screen.blit(image.load("data/Arms/right_down.png"), COORDS_ARMS)
            elif arms == 'up':
                screen.blit(image.load("data/Arms/right_up.png"), COORDS_ARMS)
