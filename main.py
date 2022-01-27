import pygame
from pygame import mixer
import os
import sys
from start_menu import *


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        if not self.scored:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and\
                    self.rect.collidepoint(args[0].pos):
                self.sprite = load_image(self.imagename2)
                screen.blit(self.sprite, (self.rect.x, self.rect.y))
                coin_fx.play()
                self.scored = True
                print('returning one')
                return 1
        return 0


# класс для объектов, которые помогают пройти уровень
class MainObject:
    def __init__(self, imagename, x, y):
        self.object = load_image(imagename)
        self.rect = self.object.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        screen.blit(self.object, (self.rect.x, self.rect.y))
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        else:
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
        self.update()

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
        self.ground = 0
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
            dy = 0

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
        if self.rect.x > 900 and room != 5:
            self.rect.x = -100
            return 1
        # elif self.rect.x < -50 and room != 1:
        #     self.rect.x = 800
        #     return -1
        else:
            return 0

    def get_pos(self):
        return self.rect


if __name__ == '__main__':
    # звук
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()

    pygame.init()

    # главные переменные
    start = False
    current_room = 5
    coins = 0
    level_passed = False
    difficulty = 1

    # переменные для пятой комнаты
    memory_begin = False
    is_dark = False
    memory_game = False
    room_5_time = 0
    current_time = 0
    prep = True

    font_score = pygame.font.SysFont('Bauhaus 93', 30)

    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Ночной музей')

    clock = pygame.time.Clock()
    fps = 60

    # загрузка звуковых файлов
    pygame.mixer.music.load('data/music/music.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 0.0, 5000)
    coin_fx = pygame.mixer.Sound('data/music/coin.mp3')
    coin_fx.set_volume(0.4)
    jump_fx = pygame.mixer.Sound('data/music/jump.mp3')
    jump_fx.set_volume(0.05)

    # загрузка изображений
    player_s = load_image('player_standing.png')
    player_s_l = load_image('player_standing_l.png')
    player_w = load_image('player_walking.png')
    player_w_l = load_image('player_walking_l.png')
    room1 = load_image('room1.png')
    room2 = load_image('room2.png')
    room3 = load_image('room3.png')
    room4 = load_image('room4.png')
    room5 = load_image('room5.png')
    dark = load_image('dark.png')
    coin = load_image('coin.png')

# объекты классов
    restart = Button('restart.png', width - 40, 10)
    player = Player(0, height - 400)
    symbol = MainObject('symbol.png', 100, 100)
    painting = MainObject('mona_lisa.png', 65, 135)
    pressure_plate = InteractiveObject('pressure_plate.png', 500, 500)
    lever1 = LeverObject('lever_up.png', 'lever_down.png', 0, 200)
    lever2 = LeverObject('lever_up.png', 'lever_down.png', 200, 200)
    lever3 = LeverObject('lever_up.png', 'lever_down.png', 400, 200)
    lever4 = LeverObject('lever_up.png', 'lever_down.png', 600, 200)
    lever5 = LeverObject('lever_up.png', 'lever_down.png', 800, 200)
    statue = MainObject('statue.png', 100, 100)

# бонусные объекты
    bonus_statue = BonusObject('1statue1.png', '1statue2.png', 532, 399)
    bonus_vase = BonusObject('1vase1.png', '1vase2.png', 75, 411)

    running = True

    while running:
        if start:
            start_menu()
        else:
            if current_room == 1:
                screen.blit(room1, (0, 0))
                symbol.update()
                bonus_statue.update()
                bonus_vase.update()

            elif current_room == 2:
                pygame.mixer.music.set_volume(0.01)
                screen.blit(room2, (0, 0))
                pressure_plate.update()

            elif current_room == 3:
                screen.blit(room3, (0, 0))
                painting.update()

            elif current_room == 4:
                screen.blit(room4, (0, 0))
                lever1.update()
                lever2.update()
                lever3.update()
                lever4.update()
                lever5.update()

            elif current_room == 5:
                if prep:
                    screen.blit(room5, (0, 0))
                    draw_text('You have', font_score,
                              (0, 0, 0), width / 2, 10)
                    current_time = pygame.time.get_ticks()
                    if not is_dark and not memory_game and not memory_begin:
                        room_5_time = pygame.time.get_ticks()
                        memory_begin = True
                    if current_time - room_5_time > 5000 and memory_begin:
                        room5 = dark
                        is_dark = True
                        memory_begin = False
                    if is_dark and not memory_game:
                        room_5_time = pygame.time.get_ticks()
                        memory_game = True
                    if current_time - room_5_time > 3000 and memory_game:
                        room5 = load_image('room5.png')
                        prep = False
                else:
                    screen.blit(room5, (0, 0))
                    statue.update()

            player.move()
            screen.blit(coin, (5, 5))
            draw_text(str(coins), font_score, (255, 255, 0), 34, 10)

            if level_passed:
                a = player.change_room(current_room)
                current_room += a
                if a == 1:
                    level_passed = False

            # restart уровня
            if restart.update():
                level_passed = False
                current_room = 1
                player = Player(0, width - 450)
                coins = 0

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_room == 1:
                        print(event.pos)
                        coins += bonus_statue.score(event, event.pos)
                        coins += bonus_vase.score(event, event.pos)

                        symbol.update(event, event.pos)
                        level_passed = symbol.update(event)
                    elif current_room == 3:
                        level_passed = painting.update(event)
                    elif current_room == 4:
                        lever1.press_lever(event)
                        lever2.press_lever(event)
                        lever3.press_lever(event)
                        lever4.press_lever(event)
                        lever5.press_lever(event)
                        levers = [lever1.lever_state(), lever2.lever_state(), lever3.lever_state(),
                                  lever4.lever_state(), lever5.lever_state()]
                        if levers[0] and levers[2] and levers[3] and not levers[1] and not levers[4]:
                            level_passed = True
                if event.type == pygame.KEYDOWN:
                    if current_room == 2 and pygame.key.get_pressed()[pygame.K_SPACE]:
                        level_passed = pressure_plate.interact(player.get_pos())

                if event.type == pygame.QUIT:
                    running = False
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
