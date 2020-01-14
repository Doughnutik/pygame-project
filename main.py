import pygame
import os
from sys import argv, exit
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


pygame.init()


class Level(QMainWindow):

    def __init__(self):
        super().__init__()
        path = os.path.join('data', 'ui_main.ui')
        uic.loadUi(path, self)

        self.buttons.buttonClicked.connect(self.run)
        self.names = [None for _ in range(5)]

    def run(self, btn):
        global level_name
        if btn == self.first:
            name = self.names[0]
        elif btn == self.second:
            name = self.names[1]
        elif btn == self.third:
            name = self.names[2]
        elif btn == self.fourth:
            name = self.names[3]
        else:
            name = self.names[4]
        level_name = name
        self.close()


def load_start_fon():
    text = ['Приятного прохождения!! =)',
            'Чтобы начать игру, нажмите любую клавишу.']
    x = 200
    y = 270
    color = pygame.Color('red')

    fon = pygame.transform.scale(load_image('start_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    for line in text:
        string = font.render(line, 1, color)
        rect = string.get_rect()
        rect.x = x
        rect.y = y
        screen.blit(string, rect)
        x -= 140
        y += 100
        color = pygame.Color('blue')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


def load_end_fon():
    text = ['Вы справились, поздравляю!!!',
            'Спасибо, что прошли этот лабиринт :)']
    x = 180
    y = 600
    color = pygame.Color('purple')

    fon = pygame.transform.scale(load_image('end_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    for line in text:
        string = font.render(line, 1, color)
        rect = string.get_rect()
        rect.x = x
        rect.y = y
        screen.blit(string, rect)
        x -= 50
        y += 50
        color = pygame.Color('green')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


def load_image(name, colorkey=None):
    path = os.path.join('data', name)
    image = pygame.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level():
    app = QApplication(argv)
    ex = Level()
    ex.show()
    app.exec()

    path = os.path.join('data', level_name)
    with open(path) as f:
        lines = [i.strip() for i in f.readlines()]
        h = len(lines)
        w = len(lines[0])
        return lines


lines = load_level()
level_name = ''
size = width, height = 900, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
hero = pygame.sprite.Group()
load_start_fon()
load_end_fon()
objects = pygame.sprite.Group()
heroes = pygame.sprite.Group()
speed = 1


def make_level():
    player = None
    n = width * 25
    m = height * 25
    for i in range(n):
        for j in range(m):
            if lines[j][i] == '#':
                Wall((i * 25, j * 25))
            elif lines[j][i] == '@':
                Hero((i * 25, j * 25))
                Grass((i * 25, j * 25))
            elif lines[j][i] == '.':
                Grass((i * 25, j * 25))
            else:
                Stairs((i * 25, j * 25))
                Grass((i * 25, j * 25))


class Hero(pygame.sprite.Sprite):
    sheet = load_image('hero.png')
    columns = rows = 2

    def __init__(self, pos):
        super().__init__(heroes)
        self.frames = []
        self.cut_sheet(Hero.sheet, Hero.columns, Hero.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def change_direction(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Wall(pygame.sprite.Sprite):
    image = load_image('wall.jpg')

    def __init__(self, pos):
        super().__init__(objects)
        self.image = Wall.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


class Grass(pygame.sprite.Sprite):
    image = load_image('grass.jpg')

    def __init__(self, pos):
        super().__init__(objects)
        self.image = Grass.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


class Stairs(pygame.sprite.Sprite):
    image = load_image('stairs.jpg', (255, 255, 255))

    def __init__(self, pos):
        super().__init__(objects)
        self.image = Grass.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        ...

pygame.quit()