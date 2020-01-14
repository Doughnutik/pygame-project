import pygame
import os
from sys import argv, exit
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from time import sleep


pygame.init()
size = width, height = 900, 700
screen = None


class Level(QMainWindow):

    def __init__(self):
        super().__init__()
        path = os.path.join('data', 'ui_main.ui')
        uic.loadUi(path, self)

        self.buttons.buttonClicked.connect(self.run)
        self.names = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt']

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


class Music:

    def __init__(self):
        self.musics = ['first.mp3', 'second.mp3', 'third.mp3', 'fourth.mp3', 'fifth.mp3']
        self.index = 0

    def play(self):
        music = os.path.join('data/music', self.musics[self.index])
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        self.index = (self.index + 1) % 5


def load_start_fon():
    text = ['Приятного прохождения =)',
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
    sleep(3)
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
        pygame.display.flip()


def load_lose_fon():
    sleep(3)
    text = ['Увы, но ваш персонаж коснулся лавы.',
            'К сожалению, это - мгновенная смерть. :(',
            'Ничего страшного, в следующий раз будьте бдительны!!!']
    x = 180
    y = 500
    count = 0
    color = pygame.Color('white')

    fon = pygame.transform.scale(load_image('lose_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    for line in text:
        count += 1
        string = font.render(line, 1, color)
        rect = string.get_rect()
        rect.x = x
        rect.y = y
        screen.blit(string, rect)
        x -= 25
        y += 50
        if count == 2:
            x -= 75
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()


def load_image(name, colorkey=None):
    path = os.path.join('data/pictures', name)
    image = pygame.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level():
    global screen

    app = QApplication(argv)
    ex = Level()
    ex.show()
    app.exec()
    screen = pygame.display.set_mode(size)
    load_start_fon()

    path = os.path.join('data/levels', level_name)
    with open(path) as f:
        lines = [i.strip() for i in f.readlines()]
        return lines


lines = load_level()
level_name = ''
clock = pygame.time.Clock()
hero = pygame.sprite.Group()
objects = pygame.sprite.Group()
heroes = pygame.sprite.Group()
speed = 0.5
fps = 60
'''music_player = Music()
music_player.play()'''


class Hero(pygame.sprite.Sprite):
    sheet = load_image('hero.png', (0, 0, 0))
    columns = rows = 2

    def __init__(self, pos):
        super().__init__(heroes)
        self.frames = []
        self.cut_sheet(Hero.sheet, Hero.columns, Hero.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.direction = True
        self.count = 0
        self.up = self.down = self.right = self.left = False

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
        if not self.direction:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_intersection(self, parameter):
        sprites = pygame.sprite.spritecollide(self, objects, False)
        flag = 1
        for sprite in sprites:
            if sprite.__class__.__name__ == 'Lava':
                flag = 2
                break
            if sprite.__class__.__name__ == 'Wall':
                if parameter == 1 and sprite.rect.y + 25 - self.rect.y in range(-2, 3):
                    flag = 0
                    break
                if parameter == 2 and sprite.rect.y - self.rect.y - 25 in range(-2, 3):
                    flag = 0
                    break
                if parameter == 3 and sprite.rect.x - self.rect.x - 25 in range(-2, 3):
                    flag = 0
                    break
                if parameter == 4 and sprite.rect.x + 25 - self.rect.x in range(-2, 3):
                    flag = 0
                    break
            if sprite.__class__.__name__ == 'Grass' and sprite.case == 2:
                flag = 3
                break
        return flag

    def check_moving(self):
        result = self.check_intersection(1)
        if result == 2:
            return 0
        if result == 3:
            return 2
        if not result:
            self.up = False
        if not self.check_intersection(2):
            self.down = False
        if not self.check_intersection(3):
            self.right = False
        if not self.check_intersection(4):
            self.left = False
        return 1

    def move(self):
        if self.up:
            self.rect.y -= 1
        if self.down:
            self.rect.y += 1
        if self.right:
            self.rect.x += 1
        if self.left:
            self.rect.x -= 1


class Wall(pygame.sprite.Sprite):
    image1 = load_image('wall1.jpg')
    image2 = load_image('wall2.jpg')

    def __init__(self, pos, case=0):
        super().__init__(objects)
        if not case:
            self.image = Wall.image1
        else:
            self.image = Wall.image2
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


class Grass(pygame.sprite.Sprite):
    image_grass = load_image('grass.jpg')
    image_start_square = load_image('start_square.jpg')
    image_end_square = load_image('end_square.png')

    def __init__(self, pos, case=0):
        super().__init__(objects)
        self.case = case
        if not case:
            self.image = Grass.image_grass
        elif case == 1:
            self.image = Grass.image_start_square
        else:
            self.image = Grass.image_end_square
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


class Stairs(pygame.sprite.Sprite):
    image = load_image('stairs.png', (0, 0, 0))

    def __init__(self, pos):
        super().__init__(objects)
        self.image = Stairs.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


class Lava(pygame.sprite.Sprite):
    image = load_image('lava.png')

    def __init__(self, pos):
        super().__init__(objects)
        self.image = Lava.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width = self.height = 25


def make_level():
    player = None
    n = 10
    m = 10
    for i in range(n):
        for j in range(m):
            if lines[j][i] == '#':
                Wall((i * 25, j * 25), 1)
            elif lines[j][i] == '=':
                Wall((i * 25, j * 25))
            elif lines[j][i] == '@':
                player = Hero((i * 25, j * 25))
                Grass((i * 25, j * 25), 1)
            elif lines[j][i] == '.':
                Grass((i * 25, j * 25))
            elif lines[j][i] == ';':
                Grass((i * 25, j * 25), 2)
            elif lines[j][i] == '!':
                Lava((i * 25, j * 25))
            else:
                Grass((i * 25, j * 25))
                Stairs((i * 25, j * 25))
    return player


player = make_level()
running = True


while running:
    '''if not pygame.mixer.music.get_busy():
        music_player.play()'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right = True
                player.direction = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left = True
                player.direction = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left = False

    result = player.check_moving()
    if not result:
        load_lose_fon()
    if result == 2:
        load_end_fon()
    player.move()
    if player.left or player.right:
        if player.count == 5:
            player.update()
        player.count = (player.count + 1) % 6
    screen.fill((0, 0, 0))
    objects.draw(screen)
    heroes.draw(screen)
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()