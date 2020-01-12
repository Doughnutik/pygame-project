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

    fon = pygame.transform.scale(load_image('start_fon.jpg'), (w, h))
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

    fon = pygame.transform.scale(load_image('end_fon.jpg'), (w, h))
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


'''def load_level():
    app = QApplication(argv)
    ex = Level()
    ex.show()
    app.exec()

    path = os.path.join('data', level_name)
    with open(path) as f:
        lines = [i.strip() for i in f.readlines()]
        h = len(lines)
        w = len(lines[0])
        return lines, w * 50, h * 50'''


#lines, w, h = load_level()
level_name = ''
size = 900, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
hero = pygame.sprite.Group()
load_start_fon()
load_end_fon()
v = None


class Hero(pygame.sprite.Sprite):
    image = load_image('hero')

    def __init__(self, pos):
        super().__init__(hero)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def update(self):
        pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        ...

pygame.quit()