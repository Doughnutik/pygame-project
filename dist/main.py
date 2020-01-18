import pygame
import os
from sys import argv, exit
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap
from time import sleep
from random import choice


pygame.init()
size = width, height = 950, 750
SPRITE_SIDE = 25
HERO_SIDE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = None


class Level(QMainWindow):

    def __init__(self):
        super().__init__()
        path = os.path.join('data', 'ui_main.ui')
        uic.loadUi(path, self)
        path = os.path.join('data/pictures', 'labyrinth.jpg')
        self.widget = None

        self.pixmap = QPixmap(path)
        self.image.setPixmap(self.pixmap)

        self.menu = QAction('Помощь', self)
        self.file.addAction(self.menu)
        self.menu.triggered.connect(self.help)

        path = os.path.join('data', 'levels')
        self.levels = [i for i in os.listdir(path)]
        self.names = [str(i) for i in range(1, len(self.levels) + 1)]

        self.choose.clicked.connect(self.run)

    def run(self):
        global level_name
        while True:
            name, btn_pressed = QInputDialog.getItem(self, "Уровень", "Выберите уровень", self.names, 0, False)
            if btn_pressed:
                break
            else:
                self.result.setText('Необходимо выбрать уровень!')
        if name:
            level_name = self.levels[self.names.index(name)]
        self.close()

    def help(self):
        self.widget = Help()
        self.widget.show()


class Help(QWidget):

    def __init__(self):
        super().__init__()
        path = os.path.join('data', 'ui_help.ui')
        uic.loadUi(path, self)


class Music:

    def __init__(self):
        path = os.path.join('data', 'music')
        self.musics = [i for i in os.listdir(path) if i != 'win.mp3' and i != 'lose.mp3']
        self.length = len(self.musics)

        self.index = 0
        self.order = False
        self.played = [False] * self.length
        self.change = 0
        self.playing = False
        self.pause = False

    def play(self):
        if all([self.played[i] for i in range(self.length)]):
            self.played = [False] * self.length

        if not self.order:
            self.index = choice([i for i in range(self.length) if not self.played[i]])
        else:
            self.index = (self.index + 1) % self.length

        self.played[self.index] = True
        music = os.path.join('data/music', self.musics[self.index])
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def choose_music(self, number):
        if all([self.played[i] for i in range(self.length)]):
            self.played = [False] * self.length

        self.index = number
        self.played[self.index] = True
        music = os.path.join('data/music', self.musics[self.index])
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    @staticmethod
    def win():
        music = os.path.join('data/music', 'win.mp3')
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    @staticmethod
    def lose():
        music = os.path.join('data/music', 'lose.mp3')
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def change_volume(self):
        if self.change == 1:
            volume = pygame.mixer.music.get_volume() + 0.01
            if volume <= 1:
                pygame.mixer.music.set_volume(volume)
        elif self.change == 2:
            volume = pygame.mixer.music.get_volume() - 0.001
            if volume >= 0:
                pygame.mixer.music.set_volume(volume)

    def next_track(self, difference):
        if all([self.played[i] for i in range(self.length)]):
            self.played = [False] * self.length

        self.index = (self.index + difference) % self.length
        self.played[self.index] = True
        music = os.path.join('data/music', self.musics[self.index])
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()


def load_start_fon():
    text = ['Приятного прохождения =)',
            'Чтобы начать игру, нажмите любую клавишу.']

    x = 200
    y = 270
    color = pygame.Color('red')

    fon = pygame.transform.scale(load_image('start_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 50)

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
    music_player.win()
    text = ['Вы справились, поздравляю!!!',
            'Спасибо, что прошли этот лабиринт :)']

    x = 180
    y = 600
    color = pygame.Color('purple')

    fon = pygame.transform.scale(load_image('end_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 50)

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
    music_player.lose()
    text = ['Увы, но ваш персонаж коснулся лавы.',
            'К сожалению, это - мгновенная смерть. :(',
            'Ничего страшного, в следующий раз будьте бдительней!!!']

    x = 180
    y = 500
    count = 0
    color = WHITE

    fon = pygame.transform.scale(load_image('lose_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 40)

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


level_name = ''


def load_level():
    global screen

    app = QApplication(argv)
    ex = Level()
    ex.show()
    app.exec()

    if not level_name:
        exit()
    screen = pygame.display.set_mode(size)
    load_start_fon()

    path = os.path.join('data/levels', level_name)
    with open(path) as f:
        lines = [i.strip() for i in f.readlines()]
        return lines


lines = load_level()
clock = pygame.time.Clock()
objects = pygame.sprite.Group()
heroes = pygame.sprite.Group()
fps = 60
music_player = Music()


class Hero(pygame.sprite.Sprite):
    sheet = load_image('hero.png', BLACK)
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
            if (sprite.__class__.__name__ == 'Lava' and
                    any(i in range(sprite.rect.y + 3, sprite.rect.y + 23) for i in
                        [self.rect.y, self.rect.y + HERO_SIDE])
                    and any(i in range(sprite.rect.x + 3, sprite.rect.x + 23) for i in
                            [self.rect.x, self.rect.x + HERO_SIDE])):
                flag = 2
                break
            if sprite.__class__.__name__ == 'Wall':
                if parameter == 1 and sprite.rect.y + SPRITE_SIDE - self.rect.y in range(-2, 3):
                    flag = 0
                    break
                if parameter == 2 and sprite.rect.y - self.rect.y - HERO_SIDE in range(-2, 3):
                    flag = 0
                    break
                if parameter == 3 and sprite.rect.x - self.rect.x - HERO_SIDE in range(-2, 3):
                    flag = 0
                    break
                if parameter == 4 and sprite.rect.x + SPRITE_SIDE - self.rect.x in range(-2, 3):
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


class Stairs(pygame.sprite.Sprite):
    image = load_image('stairs.png', BLACK)

    def __init__(self, pos):
        super().__init__(objects)

        self.image = Stairs.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Lava(pygame.sprite.Sprite):
    image = load_image('lava.png')

    def __init__(self, pos):
        super().__init__(objects)

        self.image = Lava.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


def make_level():
    global lines, player

    n = width // SPRITE_SIDE
    m = height // SPRITE_SIDE

    for i in range(n):
        for j in range(m):
            if lines[j][i] == '#':
                Wall((i * SPRITE_SIDE, j * SPRITE_SIDE), 1)
            elif lines[j][i] == '=':
                Wall((i * SPRITE_SIDE, j * SPRITE_SIDE))
            elif lines[j][i] == '@':
                player = Hero((i * SPRITE_SIDE, j * SPRITE_SIDE))
                Grass((i * SPRITE_SIDE, j * SPRITE_SIDE), 1)
            elif lines[j][i] == '.':
                Grass((i * SPRITE_SIDE, j * SPRITE_SIDE))
                Stairs((i * SPRITE_SIDE, j * SPRITE_SIDE))
            elif lines[j][i] == ';':
                Grass((i * SPRITE_SIDE, j * SPRITE_SIDE), 2)
            elif lines[j][i] == '!':
                Lava((i * SPRITE_SIDE, j * SPRITE_SIDE))
            else:
                Grass((i * SPRITE_SIDE, j * SPRITE_SIDE))


player = None
make_level()
running = True

while running:
    if music_player.playing:
        if music_player.change:
            music_player.change_volume()
        if not pygame.mixer.music.get_busy():
            music_player.play()
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

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
            if event.key == pygame.K_EQUALS:
                music_player.change = 1
            if event.key == pygame.K_MINUS:
                music_player.change = 2
            if event.key == pygame.K_CAPSLOCK:
                music_player.order = not music_player.order
            if event.key == pygame.K_1:
                music_player.choose_music(0)
            if event.key == pygame.K_2:
                music_player.choose_music(1)
            if event.key == pygame.K_3:
                music_player.choose_music(2)
            if event.key == pygame.K_4:
                music_player.choose_music(3)
            if event.key == pygame.K_5:
                music_player.choose_music(4)
            if event.key == pygame.K_6:
                music_player.choose_music(5)
            if event.key == pygame.K_7:
                music_player.choose_music(6)
            if event.key == pygame.K_8:
                music_player.choose_music(7)
            if event.key == pygame.K_9:
                music_player.choose_music(8)
            if event.key == pygame.K_0:
                music_player.choose_music(9)
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                music_player.next_track(-1)
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                music_player.next_track(1)
            if event.key == pygame.K_q:
                music_player.playing = not music_player.playing
            if event.key == pygame.K_e:
                if music_player.pause:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                music_player.pause = not music_player.pause

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left = False
            if event.key == pygame.K_EQUALS or event.key == pygame.K_MINUS:
                music_player.change = 0

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

    screen.fill(BLACK)
    objects.draw(screen)
    heroes.draw(screen)
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
