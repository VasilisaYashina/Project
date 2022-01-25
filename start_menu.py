import pygame
import time

# Привет! Немного комментов по программе
# 1) display - переменная, содержащая само окно, измени её на название своей переменной, содержащей
# окно
# 2) font_type - шрифт, я прикрепила файл с ним на гитхаб, называется "start_menu_font.otf"
# 3) start_game (в 51-ой строке) - название твоей функции, отвечающей за начало основной игры,
#    измени эту переменную на название своей функции, отвечающей за начало основной части игры

size = width, height = 1080, 720
screen = pygame.display.set_mode(size)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='start_menu_font.otf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:  # класс, отвечающий за создание кнопки
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (239, 222, 205)
        self.active_clr = (242, 221, 198)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message, x=x + 10, y=y + 10, font_size=font_size)


def start_menu():
    menu_bckgr = pygame.image.load('фон игровое меню.jpg')
    # в скобках указать путь к фону меню, он есть на гитхабе, называется также

    button_w = 400  # ширина кнопки
    button_h = 200  # высота кнопки
    start_button = Button(button_w, button_h)  # button - класс, отвечающий за создание кнопки

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_bckgr, (0, 0))  # display - название переменной, содержащей окно с
        # программой
        start_button.draw(300, 200, 'Начать наше путешествие', 50)
        # start_game  - название твоей функции, отвечающей за начало основной игры
        pygame.display.update()
        time.sleep(0.6)
