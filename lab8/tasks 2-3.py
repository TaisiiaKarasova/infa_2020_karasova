from random import randrange as rnd, choice
import tkinter as tk
import math
import time

screen_height = 900
screen_width = 1440
SIZE = (screen_width, screen_height)
root = tk.Tk()
fr = tk.Frame(root)
root.geometry(str(SIZE[0])+'x'+str(SIZE[1]))
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

shell_radius = 10
shell_longevity = 100
shells = []
weapon_x = 20
weapon_y = 450
initial_shell_x = weapon_x
initial_shell_y = weapon_y

class shell():
    def __init__(self, x = initial_shell_x, y = initial_shell_y):
        """ Конструктор класса снарядов

        x, у - начальные координаты снаряда
        vx - состовляющая скорости, направленная вдоль Ох
        vy - состовляющая скорости, направленная вдоль Оу
        longevity - продлжительность жизни снаряда
        surface - поверхность, на которой рисуется снаряд
        """
        self.x = x
        self.y = y
        self.r = shell_radius
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.surface = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill = self.color
        )
        self.longevity = shell_longevity

    def set_coords(self):
        """ Установка положения полотна, на котором рисуется снаряд """
        canv.coords(
                self.surface,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def remove_shell (self):
        canv.delete(self.surface)
        shells.pop (shells.index(self))

    def move(self):
        """
            Переместить мяч по прошествии единицы времени.

            Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
            self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600).

            Метод учитывает тот факт, что снаряд жив или нет, а также гравитацию
        """

        if self.longevity <= 0:
            shells.pop (shells.index(self))
            canv.delete(self.surface)
        else:
            if self.y >= screen_height - self.r or self.y <= self.r:
                self.vy = -self.vy
            if self.x >= screen_width - self.r:
                self.vx = -self.vx
                
            self.x += self.vx
            self.y -= self.vy

            self.vy -= 1
            self.longevity -= 1

            self.set_coords()

    def hittest(self, obj):
        """
            Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

            Args:
                obj: Обьект, с которым проверяется столкновение.
            Returns:
                Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        dist_object_shell = ((obj.x - self.x) ** 2 + (obj.y - self.y)**2) ** 0.5
        if dist_object_shell <= self.r + obj.r:
            return True
        else:
            return False


class gun():
    def __init__(self, power = 10, readiness = 0, an = 1):
        """
            Конструктор класса пушки
            power - сила выстрела (= полная скорость снаряда)
            readiness - готовность пушки к стрельбе (1 - готова, 0 - нет)
            an - угол между осью пушки и землёй
            surface - поверхность, на которой рисуется пушка

        """
        self.power = power
        self.readiness = readiness
        self.an = an
        self.surface = canv.create_line(20, 450, 50, 420, width = 7)

    def fire2_start(self, event):
        self.readiness = 1

    def fire2_end(self, event):
        """
            Выстрел снарядом.

            Происходит при отпускании кнопки мыши.
            Начальные значения компонент скорости мяча vx и vy зависят от положения курсора.

            bullets - количество использованых снарядов
        """
        global shells, bullets
        new_shell = shell()
        bullets += 1
        new_shell.r += 5

        if event.x - new_shell.x == 0:
            self.an = 90
        else:
            self.an = math.atan((event.y - new_shell.y) / (event.x - new_shell.x))
        new_shell.vx = self.power * math.cos(self.an)
        new_shell.vy = - self.power * math.sin(self.an)
        shells += [new_shell]
        self.readiness = 0
        self.power = 10

    def targetting(self, event = 0):
        """
            Прицеливание. Зависит от положения курсора

            Поворачивает пушку
        """
        if event:
            if event.x - weapon_x == 0:
                self.an = 90
            else:
                self.an = math.atan((event.y - weapon_y) / (event.x-weapon_x))
        canv.coords(self.surface, weapon_x, weapon_y,
                    weapon_x + max(self.power, 20) * math.cos(self.an),
                    weapon_y + max(self.power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        """
            Увеличение силы выстрела
        """
        if self.readiness:
            if self.power < 100:
                self.power += 1
            canv.itemconfig(self.surface, fill='orange')
        else:
            canv.itemconfig(self.surface, fill='black')


class target():

    def __init__(self, alive = 1):

        """
            Конструктор класса целей

            points - количество поражённых целей
            points_surface - поверхность, на которой рисуются очки
            alive - факт жизни цели (1 - цель жива, 0 - нет)
        """
        self.alive = 1
        self.surface = canv.create_oval(0,0,0,0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой мишени """
        x = self.x = rnd(400, 780)
        y = self.y = rnd(100, 550)
        r = self.r = rnd(20, 50)
        vx = self.vx = rnd(5,10)
        vy = self.vy = rnd(5,10)
        color = self.color = 'red'
        canv.coords(self.surface, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.surface, fill = color)

    def set_coords(self):
        """ Установка положения полотна, на котором рисуется мишень """
        canv.coords(
                self.surface,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )


    def hit(self, points=1):
        """Попадание шарика в цель"""
        canv.coords(self.surface, -10, -10, -10, -10)

    
    def move(self):
        """
            Переместить мишень по прошествии единицы времени.

            Метод описывает перемещение мишени за один кадр перерисовки. То есть, обновляет значения
            self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600).
        """

        if self.alive:
            if self.y >= screen_height - self.r or self.y <= self.r:
                self.vy = -self.vy
            if self.x >= screen_width - self.r or self.x <= self.r:
                self.vx = -self.vx
                
            self.x += self.vx
            self.y -= self.vy

            self.vy -= 1

            self.set_coords()

target1 = target()
target2 = target()
weapon = gun()
shells = []
points = 0
bullets = 0
some_target_hit = False
canv.create_text(32, 30, text = 'points:' + str(points), font = '28')
canv.create_text(32, 60, text = 'bullets:' + str(bullets), font = '28')

def new_game(event=''):
    global gun, target1, target2, screen1, shells, bullets, points
    target1.new_target()
    target2.new_target()
    shells = []
    canv.bind('<Button-1>', weapon.fire2_start)
    canv.bind('<ButtonRelease-1>', weapon.fire2_end)
    canv.bind('<Motion>', weapon.targetting)


    z = 0.03
    target1.alive = 1
    target2.alive = 1
    while target1.alive or target2.alive:
        for b in shells:
            b.move()
            if b.hittest(target1) and target1.alive:
                some_target_hit = True
                target1.alive = 0
                target1.hit()
                points += 1
                canv.create_rectangle(0, 0, 100, 100,
                                      outline = 'white', fill = 'white')
                canv.create_text(30, 30, text = 'points:' + str(points), font = '28')
            if b.hittest(target2) and target2.alive:
                some_target_hit = True
                target2.alive = 0
                target2.hit()
                points += 1
                canv.create_rectangle(0, 0, 100, 100,
                                      outline = 'white', fill = 'white')
                canv.create_text(30, 30, text = 'points:' + str(points), font = '28')
                
            if some_target_hit:
                for b in shells:
                    b.remove_shell()
                
        canv.create_rectangle(0, 0, 100, 100,
                                      outline = 'white', fill = 'white')
        canv.create_text(40, 60, text = 'bullets:' + str(bullets), font = '28')
        canv.create_text(32, 30, text = 'points:' + str(points), font = '28')

        some_target_hit = False
        
        if target1.alive:
            target1.move()
        if target2.alive:
            target2.move()
            
        canv.update()
        time.sleep(z)
        weapon.targetting()
        weapon.power_up()
    canv.delete(gun)
    root.after(750, new_game)


new_game()

