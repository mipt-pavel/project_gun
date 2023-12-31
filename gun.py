import math
import random as rnd
from random import choice

import pygame

pygame.font.init()
text_points = pygame.font.Font(None, 36)
text_hit_target = pygame.font.Font(None, 36)
text_freeze_bomb = pygame.font.Font(None, 24)

All_points = 0

FPS = 30

RED = 0xFF0000
INDIGO = (49, 0, 98)
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 207, 255)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, INDIGO, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 200 

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.live -= 1
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 1
        if (self.x + self.r) >= WIDTH:
            self.vx = -self.vx
        if (self.y + self.r) >= HEIGHT-10:
            self.vy = -self.vy*0.7
            self.vx = 0.85*self.vx
        if abs(self.vx) <= 1 and abs(self.vy) <= 1:
            self.vx = 0
            self.vy = 0

    def draw(self):
        """Метод отрисовки снаряда на экране.
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (abs(self.x - obj.x) <= (self.r + obj.r)) and (abs(self.y - obj.y) <= (self.r + obj.r)):
            return True
        else:
            return False
    

class Bomb:
    def __init__(self, screen, x = 40, y = 450):
        """ Конструктор класса Bomb

        Args:
        x - начальное положение бомбы по горизонтали
        y - начальное положение бомбы по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.timer = 30
        self.live = 120
        
    def move(self):
        """Переместить бомбу по прошествии единицы времени.
        
        Метод описывает перемещение бомбы за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, при этом силы гравитации на бомбу, 
        не действуют.
        """
        if self.live != 0:
            self.live -= 1
        if self.timer != 0:
            self.timer -= 1
        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.r) >= WIDTH:
            self.vx = -self.vx
        if (self.x - self.r) <= 0:
            self.vx = -self.vx
        if (self.y - self.r) <= 0:
            self.vy = -self.vy
        if (self.y + self.r) >= HEIGHT:
            self.vy = -self.vy
            
    def draw(self):
        """Метод отрисовки бомбы на экране.
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения бомбы и цели. В противном случае возвращает False.
        """
        if (abs(self.x - obj.x) <= (self.r + obj.r)) and (abs(self.y - obj.y) <= (self.r + obj.r)):
            return True
        else:
            return False

    
class Gun:
    def __init__(self, screen, x=40, y=450):
        """ Конструктор класса Gun

        Args:
        x - начальное положение пушки по горизонтали
        y - начальное положение пушки по вертикали
        """
        self.x = x
        self.y = y
        self.screen = screen
        self.f2_power = 10
        self.f2_on_ba = 0
        self.f2_on_bo = 0
        self.an = 1
        self.color = GREY
        self.bullet = 0
        self.length = 40

    def fire2_start(self, event):
        """ Метод считывает нажатие кнопки мыши (отличая нажатие левой кнопки от правой) и 
        передает в атрибут пушки, при условии, что игра не на паузе.
        """
        global pause, All_points
        if not pause:
            if event.button == 1:
                self.f2_on_ba = 1
            if event.button == 3:
                if All_points >= 5:
                    self.f2_on_bo = 1

    def fire2_end(self, event):
        """Выстрел снарядом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bombs, pause, time_pause, All_points
        self.targetting(event)
        if not pause:
            time_pause = 1
            self.bullet += 1
            if self.f2_on_ba == 1:
                new_ball = Ball(self.screen)
                new_ball.r += 5
                new_ball.vx = self.f2_power * math.cos(self.an)
                new_ball.vy = - self.f2_power * math.sin(self.an)
                balls.append(new_ball)
                self.f2_on_ba = 0
            if self.f2_on_bo == 1:
                new_bomb = Bomb(self.screen)
                new_bomb.r += 5
                new_bomb.vx = self.f2_power * math.cos(self.an)
                new_bomb.vy = - self.f2_power * math.sin(self.an)
                bombs.append(new_bomb)
                self.f2_on_bo = 0
                All_points -= 5
            self.f2_power = 10
            self.length = 40

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши. Возвращает угол, под которым должна
        стрелять пушка"""
        if event:
            if (event.pos[0]-20) != 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
            elif (event.pos[1]-450) >= 0:
                self.an = math.pi/2
            else:
                self.an = (3*math.pi)/2
        return self.an

    def draw(self):
        """ Рисование пушки. Зависит от положения мыши. """
        x_m, y_m = pygame.mouse.get_pos()
        an = math.atan2((self.y-y_m), (x_m - self.x))
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + (self.length*math.cos(an)), self.y - (self.length*math.sin(an))),
            10
            )

    def power_up(self):
        """ Зарядка пушки, увеличивает начальную скорость с коэффициентом self.f2_power. 
        Зависит от времени нажатия кнопки мыши.
        """
        if self.f2_on_ba or self.f2_on_bo:
            if self.f2_power < 100:
                self.f2_power += 1
                self.length += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def new_target(self):
        """ Инициализация новой цели. Все параметры цели являются случайными величинами. """
        self.x = rnd.randint(600, 745)
        self.y = rnd.randint(100, 550)
        self.r = rnd.randint(7, 50)
        self.vx = rnd.randint(3, 10)*math.cos(rnd.randint(0, 3))
        self.vy = rnd.randint(3, 10)*math.sin(rnd.randint(0, 3))
        self.live = 1
        self.notfreeze = 1
        
    def __init__(self, screen, color):
        self.screen = screen
        self.new_target()
        self.color = color

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global All_points, pause, time_pause
        All_points += points
        pause = 1
        time_pause = 100
        
    def count_point(self, screen):
        """ Метод отвечает за вывод текста на экран: количество набранных очков, количество
        выстрелов до попадания, информация о замораживающей бомбе.
        """
        text1 = text_points.render(str(All_points), True, BLACK)
        self.screen.blit(text1, (100, 50))
        text3 = text_freeze_bomb.render('Набери 5 очков для замораживающей бомбы (правая кнопка мыши)', True, BLACK)
        self.screen.blit(text3, (150, 50))
        if pause:
            text2 = text_hit_target.render('Вы попали в цель за '+str(gun.bullet)+' выстрел(а)', True, BLACK)
            self.screen.blit(text2, (225, 270))

    def draw(self):
        """Метод отрисовки целей на экране.
        """
        if not(self.notfreeze):
            pygame.draw.circle(
                self.screen,
                LIGHT_BLUE,
                (self.x, self.y),
                self.r
                )
        else:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
                )
        
    def move(self):
        """Переместить цель по прошествии единицы времени.
        
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        if self.notfreeze:
            self.x += self.vx
            self.y += self.vy
            if (self.x + self.r) >= WIDTH:
                self.vx = -self.vx
            if (self.x - self.r) <= 350:
                self.vx = -self.vx
            if (self.y - self.r) <= 0:
                self.vy = -self.vy
            if (self.y + self.r) >= HEIGHT-60:
                self.vy = -self.vy


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pause = 0
time_pause = 1
balls = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen, RED)
target2 = Target(screen, INDIGO)
finished = False


while not finished:
    screen.fill(WHITE)
    gun.draw()
    
    if pause and (time_pause > 0):
        time_pause -= 1
    elif time_pause == 0:
        pause = 0
        gun.bullet = 0
        
    target1.count_point(screen)
    
    if not pause:
        target1.draw()
        target2.draw()
        target1.move()
        target2.move()

    for ba in balls:
        if not pause:
            ba.draw()

    for bo in bombs:
        bo.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
           

    for ba in balls:
        ba.move()
        if ba.hittest(target1) and target1.live and pause != 1:
            target1.live = 0
            target1.notfreeze = 1
            target1.hit()
            target1.new_target()
        elif ba.hittest(target2) and target2.live and pause != 1:
            target2.live = 0
            target2.notfreeze = 1
            target2.hit()
            target2.new_target()
        if ba.live == 0:
            balls.pop(0)
    for bo in bombs:
        bo.move()
        if bo.hittest(target1) and target1.notfreeze:
            target1.notfreeze = 0
        if bo.hittest(target2) and target2.notfreeze:
            target2.notfreeze = 0
        if bo.timer == 0:
            if bo.r != 30:
                bo.r += 1
        if bo.live == 0:
            bombs.pop(0)
    gun.power_up()

pygame.quit()