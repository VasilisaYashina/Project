import pygame
import os
import sys


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# класс для объектов, которые дают монетки
class BonusObject:
    def __init__(self, imagename1, imagename2, x, y):
        self.sprite = load_image(imagename1)
        self.imagename2 = imagename2
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.sprite = load_image(self.imagename2)


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


class InteractiveObject:
    def __init__(self, imagename, x, y):
        self.object = load_image(imagename)
        self.rect = self.object.get_rect()
        self.rect.x = x
        self.rect.y = y


# class LeverObject:
#     def __init__(self, imagename, x, y):
#         self.object = load_image(imagename)
#         self.rect = self.object.get_rect()
#         self.rect.x = x
#         self.rect.y = y


# класс аватара игрока
class Player:
    def __init__(self, x, y):
        self.rect = player_s.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = 0
        self.jumped = False
        self.walking = False

    def move(self):
        # проверка и передвижение героя
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumped:
            self.jumped = True
            self.v = -15
        else:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 8
            self.walking = True
        if key[pygame.K_RIGHT]:
            dx += 8
            self.walking = True
        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            self.walking = False

        self.v += 2
        if self.v > 10:
            self.v = 10
        dy += self.v

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        if self.walking:
            screen.blit(player_w, self.rect)
        else:
            screen.blit(player_s, self.rect)

    def change_room(self, room):
        if self.rect.x > 900 and room != 3:
            self.rect.x = 0
            return 1
        elif self.rect.x < -50 and room != 1:
            self.rect.x = 800
            return -1
        else:
            return 0


if __name__ == '__main__':

    pygame.init()

    current_room = 1
    coins = 0

    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Ночной музей')

    clock = pygame.time.Clock()
    fps = 60

    player_s = load_image('player_standing.png')
    player_w = load_image('player_walking.png')
    room1 = load_image('room1.png')
    room2 = load_image('room2.png')
    room3 = load_image('room3.png')
    room4 = load_image('room4.png')
    room5 = load_image('room5.png')

# объекты классов
    player = Player(0, width - 450)

    symbol = BonusObject('symbol.png', 'symbol2.png', 100, 100)
    painting = MainObject('mona_lisa.png', 65, 135)

    level_passed = False
    # level2_passed = False
    # level3_passed = False
    # level4_passed = False
    # level5_passed = False
    # game_over = False

    running = True
    while running:
        if current_room == 1:
            screen.blit(room1, (0, 0))
            symbol.update()
        elif current_room == 2:
            screen.blit(room2, (0, 0))
            painting.update()
        elif current_room == 3:
            screen.blit(room3, (0, 0))
        elif current_room == 4:
            screen.blit(room4, (0, 0))
        elif current_room == 5:
            screen.blit(room5, (0, 0))

        player.move()

        if level_passed:
            a = player.change_room(current_room)
            current_room += a
            if a == 1:
                level_passed = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_room == 1:
                    level_passed = symbol.update(event)
                elif current_room == 2:
                    level_passed = painting.update(event)

        pygame.display.flip()
    pygame.quit()
