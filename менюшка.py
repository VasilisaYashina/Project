import pygame, sys

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1080, 720), 0, 32)

font = pygame.font.SysFont('Bauhaus 93', 30)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False
options_click = False


def main_menu(click):
    while True:
        f = open("records.txt", encoding="utf8")
        lines = f.readlines()
        records = [int(i) for i in lines]
        f.close()
        a = max(records)

        screen.fill((0, 0, 0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
        draw_text(f'ваш рекорд {a}', font, (255, 255, 255), screen, 100, 100)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options(False)
        if button_3.collidepoint((mx, my)):
            if click:
                rules()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def options(options_click):
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        draw_text('Выберите уровень сложности', font, (255, 255, 255), screen, 100, 20)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        button_music1 = pygame.Rect(50, 400, 20, 50)
        button_music2 = pygame.Rect(100, 400, 20, 50)
        button_music3 = pygame.Rect(150, 400, 20, 50)
        button_music4 = pygame.Rect(200, 400, 20, 50)
        if button_1.collidepoint((mx, my)):
            if options_click:
                return 1
        if button_2.collidepoint((mx, my)):
            if options_click:
                return 2
        if button_3.collidepoint((mx, my)):
            if options_click:
                return 3
        if button_music1.collidepoint((mx, my)):
            if options_click:
                return 0.25
        if button_music2.collidepoint((mx, my)):
            if options_click:
                return 0.5
        if button_music3.collidepoint((mx, my)):
            if options_click:
                return 0.75
        if button_music4.collidepoint((mx, my)):
            if options_click:
                return 1
        options_click = False
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        pygame.draw.rect(screen, (255, 0, 0), button_music1)
        pygame.draw.rect(screen, (255, 0, 0), button_music2)
        pygame.draw.rect(screen, (255, 0, 0), button_music3)
        pygame.draw.rect(screen, (255, 0, 0), button_music4)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    options_click = True
        pygame.display.update()
        mainClock.tick(60)


def rules():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('rules', font, (255, 255, 255), screen, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)


main_menu(click)
