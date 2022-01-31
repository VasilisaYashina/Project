import pygame
from pygame import mixer
import os
import sys
from pygame.locals import *


# загрузка изображений
def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_text(text, fontt, color, surface, x, y):
    textobj = fontt.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# игра
pygame.init()
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Ночной музей')
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Bauhaus 93', 30)


def main_menu(click):
    difficulty, volume = 1, 0.1
    blue = (39, 48, 97)
    while True:
        f = open("records.txt", encoding="utf8")
        lines = f.readlines()
        records = [int(i) for i in lines]
        f.close()
        a = max(records)

        screen.blit(load_image('main_menu.png'), (0, 0))
        draw_text(f'Ваш рекорд: {a}', font, (255, 255, 0), screen, width // 2 - 80, 600)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(width // 2 - 100, 350, 200, 50)
        button_2 = pygame.Rect(width // 2 - 100, 420, 200, 50)
        button_3 = pygame.Rect(width // 2 - 100, 490, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game(difficulty, volume)
        if button_2.collidepoint((mx, my)):
            if click:
                difficulty, volume = options(False)
        if button_3.collidepoint((mx, my)):
            if click:
                rules()
        pygame.draw.rect(screen, blue, button_1)
        draw_text(f'Начать игру', font, (255, 255, 255), screen, width // 2 - 60, 365)
        pygame.draw.rect(screen, blue, button_2)
        draw_text(f'Настройки', font, (255, 255, 255), screen, width // 2 - 50, 435)
        pygame.draw.rect(screen, blue, button_3)
        draw_text(f'Правила игры', font, (255, 255, 255), screen, width // 2 - 70, 505)

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
        clock.tick(60)


def game(difficulty, volume):
    # звук
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()

    # главные переменные
    start = False
    current_room = 1
    coins = 0
    level_passed = False
    count = 15
    count_2 = 3
    note_opened = False
    dif_3_time = 0
    dif_3_count = 120
    prep = True
    score_added = False

    # шрифты
    font_score = pygame.font.SysFont('Bauhaus 93', 30)

    # загрузка звуковых файлов
    pygame.mixer.music.load('data/music/music.mp3')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, 0.0, 5000)
    coin_fx = pygame.mixer.Sound('data/music/coin.mp3')
    coin_fx.set_volume(0.4)
    jump_fx = pygame.mixer.Sound('data/music/jump.mp3')
    jump_fx.set_volume(0.05)
    yay_fx = pygame.mixer.Sound('data/music/yay.mp3')
    yay_fx.set_volume(0.4)

    # загрузка изображений
    player_s = load_image('player_standing.png')
    player_s_l = load_image('player_standing_l.png')
    player_w = load_image('player_walking.png')
    player_w_l = load_image('player_walking_l.png')
    room1 = load_image('room1.png')
    room1_note = load_image('room1_note.png')
    room2 = load_image('room2.png')
    room3 = load_image('room3.png')
    room4 = load_image('room4.png')
    room5 = load_image('room5.png')
    win = load_image('win.png')
    lose = load_image('lose.png')
    dark = load_image('dark.png')
    coin = load_image('coin.png')

    # кнопка restart
    class Button:
        def __init__(self, imagename, x, y):
            self.object = load_image(imagename)
            self.rect = self.object.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def update(self):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.object, self.rect)

            return action

    # класс для объектов, которые дают монетки
    class BonusObject:
        def __init__(self, imagename1, imagename2, x, y):
            self.sprite = load_image(imagename1)
            self.imagename2 = imagename2
            self.rect = self.sprite.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.scored = False

        def update(self):
            screen.blit(self.sprite, (self.rect.x, self.rect.y))

        def score(self, *args):
            # screen.blit(self.sprite, (self.rect.x, self.rect.y))
            if not self.scored:
                if args and args[0].type == pygame.MOUSEBUTTONDOWN and\
                        self.rect.collidepoint(args[0].pos):
                    self.sprite = load_image(self.imagename2)
                    # screen.blit(self.sprite, (self.rect.x, self.rect.y))
                    coin_fx.play()
                    self.scored = True
                    return 1
            return 0

    # класс для объектов, которые помогают пройти уровень
    class MainObject:
        def __init__(self, imagename, x, y):
            self.object = load_image(imagename)
            self.rect = self.object.get_rect()
            self.rect.x = x
            self.rect.y = y

        def draw(self):
            screen.blit(self.object, (self.rect.x, self.rect.y))

        def update(self, *args):
            # screen.blit(self.object, (self.rect.x, self.rect.y))
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                # screen.blit(self.object, (self.rect.x, self.rect.y))
                return True
            else:
                # screen.blit(self.object, (self.rect.x, self.rect.y))
                return False

    # класс для объектов, с которыми можно взаимодействовать, которые помогают пройти уровень
    class InteractiveObject:
        def __init__(self, imagename, x, y):
            self.object = load_image(imagename)
            self.rect = self.object.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            screen.blit(self.object, (self.rect.x, self.rect.y))

        def interact(self, *args):
            if args and self.rect.colliderect(args[0]):
                # print(self.rect, args[0])
                return True
            else:
                return False

    # класс для рычагов
    class LeverObject:
        def __init__(self, imagename, imagename2, x, y):
            self.object = load_image(imagename)
            self.object2 = load_image(imagename2)
            self.rect = self.object.get_rect()
            self.rect2 = self.object2.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.rect2.x = x
            self.rect2.y = y
            self.state = [self.object, self.rect, self.rect.x, self.rect.y]

        def update(self):
            screen.blit(self.state[0], (self.state[2], self.state[3]))

        def press_lever(self, *args):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                if self.state[0] == self.object:
                    self.state = [self.object2, self.rect2, self.rect2.x, self.rect2.y]
                elif self.state[0] == self.object2:
                    self.state = [self.object, self.rect, self.rect.x, self.rect.y]
            # self.update()

        def lever_state(self):
            if self.state[0] == self.object:
                return False
            elif self.state[0] == self.object2:
                return True
            return False

    # класс аватара игрока
    class Player:
        def __init__(self, x, y):
            self.rect = player_s.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.ground = 1
            self.v = 0
            self.jumped = False
            self.walking = False
            self.right = True
            self.left = False

        def move(self):
            # проверка и передвижение героя
            dx = 0
            dy = 0
            key = pygame.key.get_pressed()
            # print(self.rect.y)
            if key[pygame.K_UP] and not self.jumped and self.rect.y == self.ground:
                jump_fx.play()
                self.v = -20
                self.jumped = True
            else:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 12
                self.walking = True
                self.right = False
                self.left = True
            if key[pygame.K_RIGHT]:
                dx += 12
                self.walking = True
                self.right = True
                self.left = False
            if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
                self.walking = False

            self.v += 4
            if self.v > 10:
                self.v = 10
            dy += self.v

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height:
                self.rect.bottom = height
                # dy = 0

            if self.walking:
                if self.right:
                    screen.blit(player_w, self.rect)
                elif self.left:
                    screen.blit(player_w_l, self.rect)
            elif self.rect.y < self.ground and self.right:
                screen.blit(player_w, self.rect)  # изменить спрайт
            elif self.rect.y < self.ground and self.left:
                screen.blit(player_w_l, self.rect)
            else:
                if self.right:
                    screen.blit(player_s, self.rect)
                elif self.left:
                    screen.blit(player_s_l, self.rect)

        def change_room(self, room):
            if self.rect.x > 900 and room != 6:
                self.rect.x = -100
                return 1
            else:
                return 0

        def get_pos(self):
            return self.rect

    # объекты классов
    restart = Button('restart.png', width - 40, 10)
    player = Player(0, height - 400)
    note = MainObject('note.png', 898, 648)
    symbol = MainObject('symbol.png', 358, 86)
    painting = MainObject('painting.png', 60, 350)
    pressure_plate = InteractiveObject('pressure_plate.png', 700, 666)
    lever1 = LeverObject('lever_up.png', 'lever_down.png', 400, 205)
    lever2 = LeverObject('lever_up.png', 'lever_down.png', 472, 205)
    lever3 = LeverObject('lever_up.png', 'lever_down.png', 544, 205)
    lever4 = LeverObject('lever_up.png', 'lever_down.png', 616, 205)
    lever5 = LeverObject('lever_up.png', 'lever_down.png', 690, 205)
    statue = MainObject('statue.png', 40, 372)

    # бонусные объекты
    bonus_statue = BonusObject('1statue1.png', '1statue2.png', 532, 399)
    bonus_vase = BonusObject('1vase1.png', '1vase2.png', 75, 411)
    bonus_painting = BonusObject('1painting1.png', '1painting2.png', 257, 355)

    bonus_bench = BonusObject('2bench1.png', '2bench2.png', 690, 480)
    bonus_plant = BonusObject('2plant1.png', '2plant2.png', 810, 410)
    bonus_trapdoor = BonusObject('2trapdoor1.png', '2trapdoor2.png', 103, 133)

    bonus_carpet = BonusObject('3carpet1.png', '3carpet2.png', 220, 584)
    bonus_bignote = BonusObject('3bignote1.png', '3bignote2.png', 50, 523)
    bonus_littlenote = BonusObject('3littlenote1.png', '3littlenote2.png', 682, 485)

    bonus_frame = BonusObject('4frame1.png', '4frame2.png', 755, 292)
    bonus_light = BonusObject('4light1.png', '4light2.png', 340, 0)
    bonus_box = BonusObject('4box1.png', '4box2.png', 100, 480)

    bonus_chair = BonusObject('5chair1.png', '5chair2.png', 405, 362)
    bonus_bigframe = BonusObject('5bigframe1.png', '5bigframe2.png', 875, 195)
    bonus_pot = BonusObject('5pot1.png', '5pot2.png', 787, 345)

    running = True

    while running:
        if start:
            # start_menu()
            pass
        else:
            # объекты в каждой комнате
            if current_room == 1:
                screen.blit(room1, (0, 0))
                draw_text(f'Найдите записку',
                          font_score, (255, 255, 255), screen, width / 2 - 80, 20)
                bonus_statue.update()
                bonus_vase.update()
                bonus_painting.update()
                if not note_opened:
                    note.draw()
                else:
                    screen.blit(room1_note, (0, 0))
                    symbol.draw()
            elif current_room == 2:
                screen.blit(room2, (0, 0))
                draw_text(f'Наступите на правильную плиту и нажмите на пробел',
                          font_score, (255, 255, 255), screen, width / 2 - 243, 20)
                bonus_bench.update()
                bonus_plant.update()
                bonus_trapdoor.update()
                pressure_plate.update()

            elif current_room == 3:
                screen.blit(room3, (0, 0))
                draw_text(f'Какая картина написана ван Гогом?',
                          font_score, (255, 255, 255), screen, width / 2 - 172, 20)
                bonus_carpet.update()
                bonus_bignote.update()
                bonus_littlenote.update()
                painting.draw()

            elif current_room == 4:
                screen.blit(room4, (0, 0))
                draw_text(f'Осмотрите комнату и опустите правильные 3 рычага',
                          font_score, (255, 255, 255), screen, width / 2 - 245, 20)
                bonus_frame.update()
                bonus_light.update()
                bonus_box.update()
                lever1.update()
                lever2.update()
                lever3.update()
                lever4.update()
                lever5.update()

            elif current_room == 5:
                screen.blit(room5, (0, 0))
                if prep:
                    if count > 0:
                        draw_text(f'Запомните комнату! Через {str(count)} секунд выключится свет!',
                                  font_score, (255, 255, 255), screen, width / 2 - 260, 10)
                        bonus_bigframe.update()
                        bonus_chair.update()
                        bonus_pot.update()
                    if count == 0:
                        room5 = dark
                    if count_2 == 0:
                        room5 = load_image('room5.png')
                        prep = False
                else:
                    statue.draw()
                    draw_text(f'Найдите отличие',
                              font_score, (255, 255, 255), screen, width / 2 - 95, 20)
                    bonus_bigframe.update()
                    bonus_chair.update()
                    bonus_pot.update()

            elif current_room == 6:
                if difficulty == 1:
                    screen.blit(win, (0, 0))
                    restart = Button('restart.png', width // 2, height // 2 - 100)
                    draw_text(f'Счет: {200 + coins * 50}', font, (255, 255, 0), screen,
                              width // 2 - 30, height // 2 - 40)
                    if not score_added:
                        f = open("records.txt", 'a')
                        print(str(200 + coins * 50), file=f)
                        f.close()
                    score_added = True
                elif difficulty == 2:
                    if coins == 15:
                        screen.blit(win, (0, 0))
                        draw_text(f'Счет: {400 + coins * 50}', font, (255, 255, 0), screen,
                                  width // 2 - 30, height // 2 - 40)
                        if not score_added:
                            f = open("records.txt", 'a')
                            print(str(400 + coins * 50), file=f)
                            f.close()
                        score_added = True
                    else:
                        screen.blit(lose, (0, 0))
                    restart = Button('restart.png', width / 2, height / 2 - 100)
                if difficulty == 3:
                    if coins == 15 and dif_3_count > 0:
                        screen.blit(win, (0, 0))
                        draw_text(f'Счет: {600 + coins * 50}', font, (255, 255, 0), screen,
                                  width // 2 - 30, height // 2 - 40)
                        if not score_added:
                            f = open("records.txt", 'a')
                            print(str(600 + coins * 50), file=f)
                            f.close()
                        score_added = True
                    else:
                        screen.blit(lose, (0, 0))
                    restart = Button('restart.png', width / 2, height / 2 - 100)

            # перемещение игрока
            if current_room != 6 and not note_opened:
                player.move()

            # монетки
            screen.blit(coin, (5, 5))
            draw_text(str(coins), font_score, (255, 255, 0), screen, 34, 10)

            # таймер для сложной сложности
            if difficulty == 3:
                dif_3_current_time = pygame.time.get_ticks()
                if dif_3_current_time - dif_3_time > 1000 and dif_3_count > 0:
                    dif_3_count -= 1
                    dif_3_time = pygame.time.get_ticks()
                if current_room != 6:
                    draw_text(str(dif_3_count), font_score, (255, 255, 0), screen, width - 100, 15)
                if dif_3_count == 0:
                    current_room = 6

            # смена уровней
            if level_passed:
                a = player.change_room(current_room)
                current_room += a
                if a == 1 and current_room == 5:
                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                    level_passed = False
                if a == 1:
                    level_passed = False

            # restart уровня
            if restart.update():
                current_room = 1
                score_added = False
                coins = 0
                level_passed = False
                count = 10
                count_2 = 3
                note_opened = False
                dif_3_time = 0
                dif_3_count = 120
                prep = True
                player = Player(0, height - 400)
                restart = Button('restart.png', width - 40, 10)
                note = MainObject('note.png', 898, 648)
                symbol = MainObject('symbol.png', 358, 86)
                painting = MainObject('painting.png', 65, 135)
                pressure_plate = InteractiveObject('pressure_plate.png', 700, 666)
                lever1 = LeverObject('lever_up.png', 'lever_down.png', 0, 200)
                lever2 = LeverObject('lever_up.png', 'lever_down.png', 200, 200)
                lever3 = LeverObject('lever_up.png', 'lever_down.png', 400, 200)
                lever4 = LeverObject('lever_up.png', 'lever_down.png', 600, 200)
                lever5 = LeverObject('lever_up.png', 'lever_down.png', 800, 200)
                statue = MainObject('statue.png', 40, 372)

                # бонусные объекты
                bonus_statue = BonusObject('1statue1.png', '1statue2.png', 532, 399)
                bonus_vase = BonusObject('1vase1.png', '1vase2.png', 75, 411)
                bonus_painting = BonusObject('1painting1.png', '1painting2.png', 257, 355)
                bonus_bench = BonusObject('2bench1.png', '2bench2.png', 690, 480)
                bonus_plant = BonusObject('2plant1.png', '2plant2.png', 810, 410)
                bonus_trapdoor = BonusObject('2trapdoor1.png', '2trapdoor2.png', 103, 133)
                bonus_carpet = BonusObject('3carpet1.png', '3carpet2.png', 220, 584)
                bonus_bignote = BonusObject('3bignote1.png', '3bignote2.png', 50, 523)
                bonus_littlenote = BonusObject('3littlenote1.png', '3littlenote2.png', 682, 485)
                bonus_frame = BonusObject('4frame1.png', '4frame2.png', 755, 292)
                bonus_light = BonusObject('4light1.png', '4light2.png', 340, 0)
                bonus_box = BonusObject('4box1.png', '4box2.png', 100, 480)
                bonus_chair = BonusObject('5chair1.png', '5chair2.png', 405, 362)
                bonus_bigframe = BonusObject('5bigframe1.png', '5bigframe2.png', 875, 195)
                bonus_pot = BonusObject('5pot1.png', '5pot2.png', 787, 345)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_room == 1:
                        coins += bonus_statue.score(event, event.pos)
                        coins += bonus_vase.score(event, event.pos)
                        coins += bonus_painting.score(event, event.pos)
                        if not note_opened:
                            note_opened = note.update(event, event.pos)
                        else:
                            if symbol.update(event):
                                level_passed = True
                                yay_fx.play()
                                note_opened = False
                    elif current_room == 3:
                        coins += bonus_carpet.score(event, event.pos)
                        coins += bonus_bignote.score(event, event.pos)
                        coins += bonus_littlenote.score(event, event.pos)
                        if painting.update(event):
                            level_passed = True
                            yay_fx.play()
                    elif current_room == 4:
                        lever1.press_lever(event)
                        lever2.press_lever(event)
                        lever3.press_lever(event)
                        lever4.press_lever(event)
                        lever5.press_lever(event)
                        coins += bonus_frame.score(event, event.pos)
                        coins += bonus_light.score(event, event.pos)
                        coins += bonus_box.score(event, event.pos)
                        levers = [lever1.lever_state(), lever2.lever_state(), lever3.lever_state(),
                                  lever4.lever_state(), lever5.lever_state()]
                        if levers[0] and levers[2] and levers[3] and not levers[1] and not levers[4]\
                                and not level_passed:
                            level_passed = True
                            yay_fx.play()
                    elif current_room == 5:
                        if count > 0:
                            coins += bonus_bigframe.score(event, event.pos)
                            coins += bonus_chair.score(event, event.pos)
                            coins += bonus_pot.score(event, event.pos)
                        if not prep:
                            coins += bonus_bigframe.score(event, event.pos)
                            coins += bonus_chair.score(event, event.pos)
                            coins += bonus_pot.score(event, event.pos)
                            level_passed = statue.update(event)
                            if level_passed:
                                yay_fx.play()
                    elif current_room == 2:
                        coins += bonus_bench.score(event, event.pos)
                        coins += bonus_plant.score(event, event.pos)
                        coins += bonus_trapdoor.score(event, event.pos)
                if event.type == pygame.KEYDOWN:
                    if current_room == 2 and event.key == pygame.K_SPACE:
                        level_passed = pressure_plate.interact(player.get_pos())
                        if level_passed:
                            yay_fx.play()
                if event.type == pygame.USEREVENT:
                    if current_room == 5:
                        if count > 0:
                            count -= 1
                        if count == 0 and count_2 > 0:
                            count_2 -= 1
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.set_volume(0)
                        running = False
        pygame.display.flip()
        clock.tick(fps)


def options(options_click):
    running = True
    dif = 1
    volume = 0.1
    blue = (39, 48, 97)
    while running:
        screen.blit(load_image('options.png'), (0, 0))

        draw_text('Выберите уровень сложности', font, (255, 255, 255), screen, width // 2 - 160, 120)
        draw_text('Выберите громкость музыки', font, (255, 255, 255), screen, width // 2 - 158, 450)
        draw_text('Чтобы вернуться, нажмите esc', font, (255, 255, 255), screen, width // 2 - 158,
                  580)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(200, 170, 200, 50)
        button_2 = pygame.Rect(width // 2 - 120, 170, 200, 50)
        button_3 = pygame.Rect(640, 170, 200, 50)
        button_music1 = pygame.Rect(width // 2 - 200, 500, 80, 50)
        button_music2 = pygame.Rect(width // 2 - 100, 500, 80, 50)
        button_music3 = pygame.Rect(width // 2, 500, 80, 50)
        button_music4 = pygame.Rect(width // 2 + 100, 500, 80, 50)

        if button_1.collidepoint((mx, my)):
            if options_click:
                dif = 1
        if button_2.collidepoint((mx, my)):
            if options_click:
                dif = 2
        if button_3.collidepoint((mx, my)):
            if options_click:
                dif = 3
        if button_music1.collidepoint((mx, my)):
            if options_click:
                volume = 0.05
        if button_music2.collidepoint((mx, my)):
            if options_click:
                volume = 0.1
        if button_music3.collidepoint((mx, my)):
            if options_click:
                volume = 0.25
        if button_music4.collidepoint((mx, my)):
            if options_click:
                volume = 0.5
        options_click = False
        pygame.draw.rect(screen, blue, button_1)
        draw_text('Легкий', font, (255, 255, 255), screen, width // 2 - 278, 185)
        draw_text('- Пройдите 5', font, (255, 255, 255), screen, 200, 230)
        draw_text('комнат', font, (255, 255, 255), screen, 200, 255)
        pygame.draw.rect(screen, blue, button_2)
        draw_text('Средний', font, (255, 255, 255), screen, width // 2 - 65, 185)
        draw_text('- Пройдите 5', font, (255, 255, 255), screen, width // 2 - 120, 230)
        draw_text('комнат и соберите', font, (255, 255, 255), screen, width // 2 - 120, 255)
        draw_text('15 монет', font, (255, 255, 255), screen, width // 2 - 120, 280)
        pygame.draw.rect(screen, blue, button_3)
        draw_text('Сложный', font, (255, 255, 255), screen, width // 2 + 150, 185)
        draw_text('- Пройдите 5', font, (255, 255, 255), screen, 640, 230)
        draw_text('комнат и соберите', font, (255, 255, 255), screen, 640, 255)
        draw_text('15 монет на время', font, (255, 255, 255), screen, 640, 280)
        pygame.draw.rect(screen, blue, button_music1)
        draw_text('10%', font, (255, 255, 255), screen, width // 2 - 180, 515)
        pygame.draw.rect(screen, blue, button_music2)
        draw_text('25%', font, (255, 255, 255), screen, width // 2 - 80, 515)
        pygame.draw.rect(screen, blue, button_music3)
        draw_text('50%', font, (255, 255, 255), screen, width // 2 + 22, 515)
        pygame.draw.rect(screen, blue, button_music4)
        draw_text('100%', font, (255, 255, 255), screen, width // 2 + 115, 515)
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
        clock.tick(fps)
    return dif, volume


def rules():
    running = True
    while running:
        screen.blit(load_image('rules.png'), (0, 0))
        draw_text('Чтобы вернуться, нажмите esc', font, (255, 255, 255), screen, width // 2 - 158,
                  580)
        draw_text(
            'Вы застряли в музее ночью. Ваша цель - пройти 5 комнат и выбраться из него.', font,
            (255, 255, 255), screen, 50, 100)
        draw_text('Чтобы пройти в следующую комнату, вы должны решить головоломку.', font,
                  (255, 255, 255), screen, 50, 160)
        draw_text('Следуйте подсказам на экране. На предметы можно и нужно нажимать курсором.', font,
                  (255, 255, 255), screen, 50, 190)
        draw_text(
            'В некоторых предметах спрятаны монетки. Нажимайте на них, чтобы их получить.',
            font, (255, 255, 255), screen, 50, 250)
        draw_text(
            'Монетки дают бонусные очки, а на среднем и сложном уровнях они обязательны для '
            'выигрыша!',
            font, (255, 255, 255), screen, 50, 280)

        draw_text('Используйте клавиши влево, вправо и вверх для передвижения.', font,
                  (255, 255, 255), screen, 50, 340)
        draw_text('Когда вы решили головоломку и услышали сигнал, идите в правую часть экрана,',
                  font, (255, 255, 255), screen, 50, 370)
        draw_text('чтобы пройти в следующую комнату.', font, (255, 255, 255), screen, 50, 400)
        draw_text('Нажмите esc, чтобы выйти из игры.', font, (255, 255, 255), screen, 50, 460)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        clock.tick(fps)


main_menu(False)
