import math
import random

from random import randint as rnd
from math import pi

import pygame
from pygame import draw
from pygame.draw import *

FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (170, 170, 180)
RED = (255, 0, 0)
BLUE = (34, 70, 185)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (237, 76, 153)
SlateGray = (112, 128, 144)
Silver = (192, 192, 192)

WIDTH = 800 # задаю размеры рабочего поля
HEIGHT = 600
length = 100 # задаю размеры мишеней (дирижаблей и облаков)
height = 65

left_key_down = False
right_key_down = False
score = 0 # ввожу счёт очков



class Gun: # дуло танка, из которого вылетают снаряды - Ball
    def __init__(self, screen):
        # класс Gun
        self.screen = screen
        self.f2_power = 10
        self.f2_on = False  # флаг; меняется при прицеливании
        self.an = pi  # угол поворота дула
        self.color = BLACK
        self.x1 = 40
        self.y1 = HEIGHT - 30
        self.r = 30
        self.x2 = 70
        self.y2 = HEIGHT - 50

    def move(self):
        # С помощью клавиш "стрелочка вправо" и "стрелочка влево" можно двигать дуло вместе с танком
        global left_key_down, right_key_down
        if left_key_down and self.x1 >= 30:
            self.x1 -= 20
        if right_key_down and self.x1 <= WIDTH - 30:
            self.x1 += 30

    def start(self):
        # Запускает power_up
        self.f2_on = True

    def end(self, event):
        # При отпускании ПКМ из дула вылетает ball
        global bullet_count, bullets

        bullet_count += 1
        new_ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        bullets.append(new_ball)
        self.f2_on = False
        self.f2_power = 10

    def targetting(self, event):
        # Двигаем мышь -> можем прицеливаться
        if event.pos[0] == self.x1:
            if event.pos[1] < self.y1:
                self.an = 3 * pi / 2
            else:
                self.an = pi / 2
        elif event.pos[0] > self.x1:
            self.an = math.atan((event.pos[1] - self.y1) / (event.pos[0] - self.x1))
        else:
            self.an = pi + math.atan((event.pos[1] - self.y1) / (event.pos[0] - self.x1))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # Рисует дуло в зависимоти от координат одного конца, радиуса и угла наклона
        draw.line(screen, self.color, (self.x1, self.y1),
                  (self.x1 + self.r * math.cos(self.an), self.y1 + self.r * math.sin(self.an)), 10)

    def power_up(self):
        # При нажатии на правую/левую кнопку мыши меняются цвет дула + увеличивается скорость вылета ball
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 20
            self.color = WHITE

        else:
            self.color = Silver
            self.r = 50


class Tank: # а вот и танк!
    def __init__(self):

        self.alive = True
        self.screen = screen
        self.r = 10
        self.x = gun.x1
        self.y = gun.y1

    def draw(self):
        # Рисует танк
        draw.rect(screen, SlateGray, (self.x - 15, self.y - 10, 30, 10))
        draw.rect(screen, SlateGray, (self.x - 30, self.y, 60, 20))
        draw.rect(screen, BLACK, (self.x - 30, self.y, 60, 20), 1)
        draw.rect(screen, BLACK, (self.x - 30, self.y + 20, 60, 7))
        draw.circle(screen, Silver, (self.x - 30, self.y + 22), 10)
        draw.circle(screen, Silver, (self.x + 30, self.y + 22), 10)
        draw.rect(screen, Silver, (self.x - 30, self.y + 12, 60, 20))
        draw.circle(screen, BLACK, (self.x + 30, self.y + 22), 7, 3)
        draw.circle(screen, BLACK, (self.x + 18, self.y + 22), 7, 3)
        draw.circle(screen, BLACK, (self.x + 6, self.y + 22), 7, 3)
        draw.circle(screen, BLACK, (self.x - 6, self.y + 22), 7, 3)
        draw.circle(screen, BLACK, (self.x - 18, self.y + 22), 7, 3)
        draw.circle(screen, BLACK, (self.x - 30, self.y + 22), 7, 3)
        draw.line(screen, BLACK, (self.x - 30, self.y + 15), (self.x + 30, self.y + 15), 3)  # это должно быть похоже на гусеницу
        draw.line(screen, BLACK, (self.x - 30, self.y + 29), (self.x + 30, self.y + 29), 3)


    def pos_update(self):
        # Дуло и танк должны иметь одинаковые координаты
        self.x = gun.x1
        self.y = gun.y1


class Ball: # снаряды, которые вылетают из танка
    def __init__(self, screen):

        self.screen = screen
        self.x = gun.x1
        self.y = gun.y1
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = random.choice([YELLOW, GREEN, PINK])
        self.max_age = 100
        self.current_age = 0

    def move(self):
        # функция перемещает ball; учитываем, чтобы он не вылетел за границы мира
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx + 10
            self.x = WIDTH - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx - 10
            self.x = self.r
        if self.y + self.r >= round(WIDTH * 0.75):
            self.vy = -self.vy - 5
            self.y = round(WIDTH * 0.75) - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy + 5
            self.y = self.r
        self.vy -= 2
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        # функция рисует ball
        draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        # Проверка на столкновение ball с обЪектом: если столкнулись, и ball, и обЪект удаляем
        global bullets, targets
        if self in bullets and 0 <= (self.x - obj.x) <= length and 0 <= (self.y - obj.y) <= height:
            bullets.remove(self)
            targets.remove(obj)
            return True
        else:
            return False

    def aging(self):
        # Ball через некоторое время должен удалиться из массива
        global bullets
        self.current_age += 1
        if self.current_age > self.max_age:
            bullets = bullets[1:]


class Target:
    def __init__(self):
        # класс Target - облака, скрывающие за собой нечто опасное!
        self.alive = True
        self.screen = screen
        self.x = rnd(0, WIDTH - 20)
        self.y = rnd(0, 300)
        self.r = rnd(20, 40)


        self.vx = rnd(3, 5) * random.choice([-1, 1])
        self.vy = rnd(3, 5) * random.choice([-1, 1])

    def move(self):
        if self.x + self.r >= 800:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= 300:
            self.vy = -self.vy
            self.y = 300 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy
            self.y = self.r
        self.x += self.vx
        self.y -= self.vy

    def draw(self):

        tel_image = pygame.image.load('sky.png')
        tel_image = pygame.transform.scale(tel_image, (length, height))
        tel_image.set_colorkey(BLACK)
        screen.blit(tel_image, (self.x, self.y))


    def hit(self):
        # Если попали в цель, то +очко
        global score
        score += 1

    def spawn_bomb(self):
        # Цель может сбросить бомбу на танк
        global bombs
        if not rnd(0, 99):
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y
            bombs.append(new_bomb)

class New_Target(Target): # Новый вид мишеней - дирижабли!
    def __init__(self):
        self.alive = True
        self.screen = pygame.Surface
        self.x = - 100
        self.y = rnd(0, 300)
        self.vx = rnd(2, 8)
        self.current_age = 0
        self.max_age = 0


    def move(self):
        # движение происходит в одном направлении
        self.x += self.vx

    def draw(self):

        # Рисует new_target дирижабль.

        tel_image = pygame.image.load('2 (1).png')
        tel_image = pygame.transform.scale(tel_image, (length, height))
        tel_image.set_colorkey(BLACK)
        screen.blit(tel_image, (self.x, self.y))





class Bomb:
    def __init__(self):
        # класс Bomb
        self.r = 8
        self.vy = 7

    def move(self):
        # Движется вниз, если вышла за границы экрана, то ее удаляем
        global bombs
        self.y += self.vy
        if len(bullets) > 0 and self.y >= HEIGHT:
            bombs.remove(self)

    def draw(self):
        # Рисует саму бомбу
        if self.y < HEIGHT - 30:
            draw.circle(screen, RED, (self.x, self.y), self.r)
        else: # если бомба упала, она взрывается безобидно для танка
            size_bang = 70
            bang = pygame.image.load("blow_up.png")
            bang = pygame.transform.scale(bang, (size_bang, size_bang))
            screen.blit(bang, (self.x, self.y + 5))

    def hit_tank(self, obj):
        # Если бомба попала в танк, то танк умирает
        if abs(self.x - obj.x) < 25 and abs(self.y - obj.y) < 25:
            obj.alive = False


def cloud():
    # создание новой цели в виде облака и добавление ее в список целей
    global targets
    cloud = Target()
    targets.append(cloud)


def airship():
    # создание новой цели в виде дирижабля и добавление ее в список
    global targets

    airship = New_Target()
    targets.append(airship)


def display_score():
    # показывает число очков - количество сбитых мишеней
    font = pygame.font.SysFont('Verdana', 26)
    text = font.render('SCORE: ' + str(score) + '', True, PINK)
    textpos = text.get_rect(centerx=WIDTH - 100, y=20)
    screen.blit(text, textpos)


def display_results():
    # если танк умер, он эпично взрывается
    size_bang = length * 2 # размер картинки
    bang = pygame.image.load("blow_up.png")
    bang = pygame.transform.scale(bang, (size_bang, size_bang))
    screen.blit(bang, (tank.x - length, tank.y - round(1.3 * length)))



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('back.png')
bullet_count = 0
targets = []
bullets = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank()

for i in range(6): # в начале игры всегда появляются 6 целей
    if rnd(0, 1):
        cloud()
    else:
        airship()

finished = False

while not finished:

    if not tank.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        display_results()
        pygame.display.update()

    else:
        screen.blit(background, (0, 0))

        k = 1
        tel_image = pygame.image.load('back.png')
        tel_image = pygame.transform.scale(tel_image, (WIDTH * k, HEIGHT * k))
        tel_image.set_colorkey(BLACK)
        screen.blit(tel_image, (0,0))


        gun.move()
        gun.draw()
        tank.pos_update()
        tank.draw()
        display_score()
        for target in targets:
            target.spawn_bomb()
            target.move()
            target.draw()
        for bomb in bombs:
            bomb.hit_tank(tank)
            bomb.move()
            bomb.draw()
        for bullet in bullets:
            bullet.aging()
            bullet.draw()
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_down = False
                if event.key == pygame.K_RIGHT:
                    right_key_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_down = True
                if event.key == pygame.K_RIGHT:
                    right_key_down = True

            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.start()
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for b in bullets:
            b.move()
            for t in targets:
                if b.hittest(t) and t.alive:
                    t.alive = False
                    t.hit()
                    if rnd(0, 1): # с равной вероятностью генерятся облака и дирижабли
                        cloud()
                    else:
                        airship()
        gun.power_up()

pygame.quit()
