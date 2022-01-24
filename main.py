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

        print(action)
        return action


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

    def update(self):
        screen.blit(self.object, (self.rect.x, self.rect.y))

    def interact(self, *args):
        if args and self.rect.colliderect(args[0]):
            print('yesss')
            return True
        else:
            return False


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
            if self.right:
                screen.blit(player_w, self.rect)
            elif self.left:
                screen.blit(player_w_l, self.rect)
        else:
            if self.right:
                screen.blit(player_s, self.rect)
            elif self.left:
                screen.blit(player_s_l, self.rect)


    def change_room(self, room):
        if self.rect.x > 900 and room != 5:
            self.rect.x = 0
            return 1
        elif self.rect.x < -50 and room != 1:
            self.rect.x = 800
            return -1
        else:
            return 0

    def get_pos(self):
        return self.rect


if __name__ == '__main__':
    pygame.init()

    current_room = 1
    coins = 0
    count = 0

    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Ночной музей')

    clock = pygame.time.Clock()
    fps = 60

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

# объекты классов
    restart = Button('restart.png', 400, 400)
    player = Player(0, width - 450)
    symbol = MainObject('symbol.png', 100, 100)
    painting = MainObject('mona_lisa.png', 65, 135)
    pressure_plate = InteractiveObject('pressure_plate.png', 500, 500)
    lever1 = LeverObject('lever_up.png', 'lever_down.png', 0, 200)
    lever2 = LeverObject('lever_up.png', 'lever_down.png', 200, 200)
    lever3 = LeverObject('lever_up.png', 'lever_down.png', 400, 200)
    lever4 = LeverObject('lever_up.png', 'lever_down.png', 600, 200)
    lever5 = LeverObject('lever_up.png', 'lever_down.png', 800, 200)


    level_passed = False
    running = True

    while running:

        if current_room == 1:
            screen.blit(room1, (0, 0))
            symbol.update()

        elif current_room == 2:
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
            screen.blit(room5, (0, 0))

        player.move()

        if level_passed:
            a = player.change_room(current_room)
            current_room += a
            if a == 1:
                level_passed = False


        if restart.update():
            print('restart')
            level_passed = False
            current_room = 1
            player = Player(0, width - 450)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_room == 1:
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
                    if levers[0] and levers[2] and levers[4] and not levers[1] and not levers[3]:
                        level_passed = True
            if event.type == pygame.KEYDOWN:
                if current_room == 2 and pygame.key.get_pressed()[pygame.K_SPACE]:
                    level_passed = pressure_plate.interact(player.get_pos())
        pygame.display.flip()
    pygame.quit()
