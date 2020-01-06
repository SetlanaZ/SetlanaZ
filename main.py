import pygame
import os
import pygame.freetype
import random
from pygame import *
from wolf import *
from egg import *

pygame.init()

SCREEN_SIZE = (600, 450)

screen = pygame.display.set_mode(SCREEN_SIZE)
chickens = pygame.display.set_mode(SCREEN_SIZE)
wolf = pygame.display.set_mode(SCREEN_SIZE)

running = True
body = 'left'
arms = 'down'

all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()

clock = pygame.time.Clock()
speed = 3000
MYEVENTTYPE = 10
pygame.time.set_timer(MYEVENTTYPE, speed)

points = 0

font = pygame.freetype.Font(None, 20)

pygame.display.set_caption("Nu Pogodi!")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


while running:

    fon = pygame.transform.scale(load_image('fon.jpg'), SCREEN_SIZE)
    screen.blit(fon, (0, 0))
    chicken = image.load("data/chickens.png")
    chickens.blit(chicken, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                body = 'left'
            if key[pygame.K_RIGHT]:
                body = 'right'
            if key[pygame.K_UP]:
                arms = 'up'
            if key[pygame.K_DOWN]:
                arms = 'down'
        if event.type == MYEVENTTYPE:
            egg = pygame.sprite.Sprite(eggs)
            egg.image = load_image("egg.png", -1)
            egg.rect = egg.image.get_rect()
            egg.rect.x, egg.rect.y = Egg.get_coords(None)
            eggs.add(egg)
            eggs.draw(wolf)
            for egg in eggs:
                if [egg.rect.x, egg.rect.y]in LEFT_UP:
                    list_name = LEFT_UP
                elif [egg.rect.x, egg.rect.y] in LEFT_DOWN:
                    list_name = LEFT_DOWN
                elif [egg.rect.x, egg.rect.y] in RIGHT_UP:
                    list_name = RIGHT_UP
                elif [egg.rect.x, egg.rect.y] in RIGHT_DOWN:
                    list_name = RIGHT_DOWN
                ind = list_name.index([egg.rect.x, egg.rect.y])
                if ind < 2:
                    egg.rect.x, egg.rect.y = list_name[ind + 1]
                elif ind == 2:
                    if egg_cought(list_name, body, arms):
                        points += 1
                        eggs.remove(egg)
                    else:
                        running = False

            eggs.update()

    if points > 0 and points % 10 == 0:
        speed *= 0.8

    Wolf.draw(screen, body, arms)
    eggs.draw(wolf)
    scoreText, _ = font.render("{}".format(points), Color("#ff0000"))
    screen.blit(scoreText, (100, 20))
    pygame.display.flip()

else:
    scoreText, _ = font.render(
                "Game Over {}".format(points), Color("#ff0000"))
    screen.blit(scoreText, (100, 20))
    pygame.display.update()


pygame.quit()