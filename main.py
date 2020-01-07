import pygame
import os
import pygame.freetype
import random
from pygame import *
from wolf import *
from egg import *
# from loadings import *

pygame.init()

SCREEN_SIZE = (600, 450)

screen = pygame.display.set_mode(SCREEN_SIZE)
chickens = pygame.display.set_mode(SCREEN_SIZE)
wolf = pygame.display.set_mode(SCREEN_SIZE)

load = True
running = True
menu_screen = False
continue_game = False

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

FPS = 50


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


def terminate():
    global running
    running = False
    global load
    load = False

def loading():
    global menu_screen
    global load
    intro_text = ["ЗАСТАВКА"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_SIZE))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    LOAD = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
    while LOAD:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                LOAD = False
                terminate()
            elif events.type == pygame.KEYDOWN or events.type == pygame.MOUSEBUTTONDOWN:
                LOAD = False
                load = False
                menu_screen = True


def menu():
    global menu_screen
    global running
    global continue_game
    menu_text = ["Меню",
                  "Нажмите Z для начала игры",
                  "Нажмите Q для выхода",
                  "Нажмите TAB для просмотра рекордов"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_SIZE))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    MENU = True
    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
    while MENU:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                MENU = False
                menu_screen = False
                running = False
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_q:
                    MENU = False
                    menu_screen = False
                    running = False
                elif events.key == pygame.K_z:
                    MENU = False
                    menu_screen = False
                    continue_game = True
                elif events.key == pygame.K_z:
                    pass


def game_over():
    global menu_screen
    global running
    menu_text = [f"Счет: {points}",
                 "Нажмите W для выхода в меню",
                 "Нажмите Q для выхода",
                 "Нажмире R для сохранения результата"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_SIZE))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    game = True
    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
    while game:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game = False
                running = False
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_q:
                    game = False
                    running = False
                elif events.key == pygame.K_w:
                    game = False
                    menu_screen = True
                elif events.key == pygame.K_r:
                    pass


while running:
    if load:
        loading()

    if menu_screen:
        menu()

    if continue_game:

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
                            game_over()

                eggs.update()

        if points > 0 and points % 10 == 0:
            speed *= 0.6

        Wolf.draw(screen, body, arms)
        eggs.draw(wolf)
        scoreText, _ = font.render("{}".format(points), Color("#ff0000"))
        screen.blit(scoreText, (100, 20))
        pygame.display.flip()
