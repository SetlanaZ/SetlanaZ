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
RESTART_GAME = False

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
    global RESTART_GAME
    menu_text = ["Меню",
                 "Начать игру Z",
                 "Выход Q"]
    menu_buttons = []

    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_SIZE))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    MENU = True
    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        menu_rect = string_rendered.get_rect()
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        text_coord += 10
        menu_rect.top = text_coord
        menu_rect.x = 10
        text_coord += menu_rect.height
        screen.blit(string_rendered, menu_rect)
        if line != 'Меню':
            pygame.draw.rect(screen, (0, 0, 0), (menu_rect.x, menu_rect.y, text_w, text_h), 1)
            menu_buttons.append([menu_rect.x, menu_rect.y, menu_rect.x + text_w,  menu_rect.y + text_h])
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
                    RESTART_GAME = True
            elif events.type == pygame.MOUSEMOTION:
                if menu_buttons[0][2] > events.pos[0] > menu_buttons[0][0] and menu_buttons[0][3] > \
                        events.pos[1] > menu_buttons[0][1]:
                    txt_x = menu_buttons[0][0]
                    txt_y = menu_buttons[0][1]
                    txt_w = menu_buttons[0][2] - menu_buttons[0][0]
                    txt_h = menu_buttons[0][3] - menu_buttons[0][1]
                    x, y, w, h = 10, 91, 136, 21
                    color = (255, 0, 0)
                    pygame.draw.rect(screen, color, (txt_x, txt_y, txt_w, txt_h), 1)
                else:
                    color = (0, 0, 0)
                    for line in menu_text:
                        if line != 'Меню':
                            if line == "Начать игру Z":
                                x, y, w, h = 10, 91, 136, 21
                                pygame.draw.rect(screen, color, (x, y, w, h), 1)
                        pygame.display.flip()
                    pygame.display.update()
                if menu_buttons[1][2] > events.pos[0] > menu_buttons[1][0] and menu_buttons[1][3] > \
                        events.pos[1] > menu_buttons[1][1]:
                    txt_x = menu_buttons[1][0]
                    txt_y = menu_buttons[1][1]
                    txt_w = menu_buttons[1][2] - menu_buttons[1][0]
                    txt_h = menu_buttons[1][3] - menu_buttons[1][1]
                    x, y, w, h = 10, 122, 91, 21
                    color = (255, 0, 0)
                    pygame.draw.rect(screen, color, (txt_x, txt_y, txt_w, txt_h), 1)
                else:
                    color = (0, 0, 0)
                    for line in menu_text:
                        if line != 'Меню':
                            if line == "Выход Q":
                                x, y, w, h = 10, 122, 91, 21
                                pygame.draw.rect(screen, color, (x, y, w, h), 1)
                        pygame.display.flip()
                    pygame.display.update()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                if menu_buttons[0][2] > events.pos[0] > menu_buttons[0][0] and menu_buttons[0][3] > \
                        events.pos[1] > menu_buttons[0][1]:
                    MENU = False
                    menu_screen = False
                    continue_game = True
                    RESTART_GAME = True
                elif menu_buttons[1][2] > events.pos[0] > menu_buttons[1][0] and menu_buttons[1][3] > \
                        events.pos[1] > menu_buttons[1][1]:
                    MENU = False
                    menu_screen = False
                    running = False


def game_over():
    global menu_screen
    global running
    menu_text = ["Игра закончена",
                 f"Счет: {points}",
                 "Выйти в меню W",
                 "Выход Q"]
    game_over_buttons = []
    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_SIZE))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    game = True
    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        game_over_rect = string_rendered.get_rect()
        text_coord += 10
        game_over_rect.top = text_coord
        game_over_rect.x = 10
        text_coord += game_over_rect.height
        screen.blit(string_rendered, game_over_rect)
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        if line != 'Игра закончена' and line != f"Счет: {points}":
            pygame.draw.rect(screen, (0, 0, 0), (game_over_rect.x, game_over_rect.y, text_w, text_h), 1)
            game_over_buttons.append([game_over_rect.x, game_over_rect.y, game_over_rect.x + text_w,
                                      game_over_rect.y + text_h])
            print(game_over_rect.x, game_over_rect.y, text_w, text_h)
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
            elif events.type == pygame.MOUSEMOTION:
                if game_over_buttons[0][2] > events.pos[0] > game_over_buttons[0][0] and game_over_buttons[0][3] > \
                        events.pos[1] > game_over_buttons[0][1]:
                    txt_x = game_over_buttons[0][0]
                    txt_y = game_over_buttons[0][1]
                    txt_w = game_over_buttons[0][2] - game_over_buttons[0][0]
                    txt_h = game_over_buttons[0][3] - game_over_buttons[0][1]
                    x, y, w, h = 10, 122, 166, 21
                    color = (255, 0, 0)
                    pygame.draw.rect(screen, color, (txt_x, txt_y, txt_w, txt_h), 1)
                else:
                    color = (0, 0, 0)
                    for line in menu_text:
                        if line != 'Игра закончена' and line != f"Счет: {points}":
                            if line == "Выйти в меню W":
                                x, y, w, h = 10, 122, 166, 21
                                pygame.draw.rect(screen, color, (x, y, w, h), 1)
                        pygame.display.flip()
                    pygame.display.update()
                if game_over_buttons[1][2] > events.pos[0] > game_over_buttons[1][0] and game_over_buttons[1][3] > \
                        events.pos[1] > game_over_buttons[1][1]:
                    txt_x = game_over_buttons[1][0]
                    txt_y = game_over_buttons[1][1]
                    txt_w = game_over_buttons[1][2] - game_over_buttons[1][0]
                    txt_h = game_over_buttons[1][3] - game_over_buttons[1][1]
                    x, y, w, h = 10, 153, 91, 21
                    color = (255, 0, 0)
                    pygame.draw.rect(screen, color, (txt_x, txt_y, txt_w, txt_h), 1)
                else:
                    color = (0, 0, 0)
                    for line in menu_text:
                        if line != 'Игра закончена' and line != f"Счет: {points}":
                            if line == "Выход Q":
                                x, y, w, h = 10, 153, 91, 21
                                pygame.draw.rect(screen, color, (x, y, w, h), 1)
                        pygame.display.flip()
                    pygame.display.update()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                if game_over_buttons[0][2] > events.pos[0] > game_over_buttons[0][0] and game_over_buttons[0][3] > \
                        events.pos[1] > game_over_buttons[0][1]:
                    game = False
                    menu_screen = True
                elif game_over_buttons[1][2] > events.pos[0] > game_over_buttons[1][0] and game_over_buttons[1][3] > \
                        events.pos[1] > game_over_buttons[1][1]:
                    game = False
                    running = False


while running:
    if load:
        loading()

    if menu_screen:
        menu()

    if continue_game:
        if RESTART_GAME:
            body = 'left'
            arms = 'down'

            all_sprites.empty()
            eggs.empty()

            clock = pygame.time.Clock()
            speed = 3000
            MYEVENTTYPE = 10
            pygame.time.set_timer(MYEVENTTYPE, speed)

            points = 0
            RESTART_GAME = False

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
                            break

                eggs.update()

        if points > 0 and points % 10 == 0:
            speed *= 0.6

        Wolf.draw(screen, body, arms)
        eggs.draw(wolf)
        f = open("data/record.txt", mode="rt", encoding="utf8")
        recordText = f.read()
        record_text, _ = font.render("Лучший результат: {}".format(recordText), Color("black"))
        f.close()
        scoreText, _ = font.render("Счет: {}".format(points), Color("black"))
        if points > int(recordText):
            f = open("data/record.txt", 'w')
            f.write(str(points))
            f.close()
            f = open("data/record.txt", mode="rt", encoding="utf8")
            recordText = f.read()
            record_text, _ = font.render("Лучший результат: {}".format(recordText), Color("black"))
            f.close()
        screen.blit(scoreText, (100, 20))
        screen.blit(record_text, (230, 20))
        pygame.display.flip()
