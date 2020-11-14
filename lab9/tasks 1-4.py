from random import randrange as rnd, choice
import tkinter as tk
import math
import time

screen_height = 600
screen_width = 800
SIZE = (screen_width, screen_height)
root = tk.Tk()
fr = tk.Frame(root)
root.geometry(str(SIZE[0])+'x'+str(SIZE[1]))
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

shell_radius = 10
shell_longevity = 30
bomb_longevity = shell_longevity
bomb_radius = 40
shells = []
bullets = 0
weapon_x = 20
weapon_y = 450
initial_shell_x = weapon_x
initial_shell_y = weapon_y

class Shell():
    def __init__(self, x = 0, y = 0):
        """
            Конструктор класса снарядов

            x, у - начальные координаты снаряда
            vx - состовляющая скорости, направленная вдоль Ох
            vy - состовляющая скорости, направленная вдоль Оу
            longevity - продлжительность жизни снаряда
            surface - поверхность, на которой рисуется снаряд
        """
        self.x = x
        self.y = y
        self.type = choice (['circle', 'square'])
        self.r = shell_radius
        self.vx = 0
        self.vy = 0
        self.color = 'black'
        if self.type == 'circle':
            self.surface = canv.create_oval(
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r,
                    fill = self.color
            )
        else:
            self.surface = canv.create_rectangle(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill = self.color
            )
            
        self.longevity = shell_longevity

    def set_coords(self):
        """
            Установка положения полотна, на котором рисуется снаряд
        """
        canv.coords(
                self.surface,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def remove_shell (self):
        shells.pop (shells.index(self))
        canv.delete(self.surface)

    def move(self):
        """
            Переместить снаряд по прошествии единицы времени.

            Метод описывает перемещение и изменение размера снаряда за один кадр перерисовки. То есть, обновляет значения
            self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна 

            Метод учитывает тот факт, что снаряд жив или нет, а также гравитацию
        """
        if self.longevity <= 0:
                self.remove_shell()
        else:
            if self.y >= screen_height - self.r or self.y <= self.r:
                self.vy = -self.vy
            if self.x >= screen_width - self.r:
                self.vx = -self.vx

            self.x += self.vx
            self.y += self.vy
            self.set_coords()

            self.vy += 1
            self.longevity -= 1



    def hit_test_target(self, obj):
        """
            Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

            Args:
                obj: Обьект, с которым проверяется столкновение.
            Returns:
                Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        dist_object_shell = ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5
        if dist_object_shell <= self.r + obj.r:
            return True
        else:
            return False

    def hit_test_gun(self, obj):
        """
            Функция проверяет сталкивалкивается ли данный обьект с пушкой, описываемой в обьекте obj.

            Args:
                obj: Обьект, с которым проверяется столкновение.
            Returns:
                Возвращает True в случае столкновения снаряда и пушки. В противном случае возвращает False.
        """
        dist_object_shell = ((obj.x_lower - self.x) ** 2 + ((obj.y_lower + obj.foundation_size // 2) - self.y) ** 2) ** 0.5
        print(str(dist_object_shell) + " VS " + str(self.r + obj.foundation_size // 2))
        if dist_object_shell <= self.r + obj.foundation_size // 2:
            return True
        else:
            return False


class Gun():
    def __init__(self, power = 10, readiness = 0, an = 1,
                 x_lower_edge = 20, y_lower_edge = 450,
                 x_upper_edge = 50, y_upper_edge = 420,
                 foundation_size = 30, foundation_color = 'yellow',
                 alive = True):
        """
            Конструктор класса пушки
            power - сила выстрела (= полная скорость снаряда)
            readiness - готовность пушки к стрельбе (1 - готова, 0 - нет)
            an - угол между осью пушки и землёй
            surface_muzzle - поверхность, на которой рисуется дуло танка
            surface_foundation - поверхность, на которой рисуется основа танка

        """
        self.power = power
        self.readiness = readiness
        self.an = an
        self.x_lower = x_lower_edge
        self.y_lower = y_lower_edge
        self.x_upper = x_upper_edge
        self.y_upper = y_upper_edge
        self.alive = alive
        self.foundation_size = foundation_size
        self.foundation_color = foundation_color
        self.surface_muzzle = canv.create_line(self.x_lower, self.y_lower,
                                               self.x_upper, self.y_upper,
                                               width = 7)
        self.surface_foundation = canv.create_rectangle(self.x_lower - self.foundation_size,
                                                        self.y_lower + 2 * self.foundation_size,
                                                        self.x_lower + self.foundation_size,
                                                        self.y_lower,
                                                        fill = self.foundation_color)

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
        new_shell = Shell(self.x_lower, self.y_lower)
        bullets += 1
        new_shell.r += 5

        if event.x - new_shell.x == 0:
            self.an = 90
        else:
            self.an = math.atan((event.y - new_shell.y) / (event.x - new_shell.x))
        new_shell.vx = self.power * math.cos(self.an)
        new_shell.vy = self.power * math.sin(self.an)
        shells += [new_shell]
        self.readiness = 0
        self.power = 10

    def targetting(self, event = 0):
        """
            Прицеливание. Зависит от положения курсора

            Поворачивает пушку
        """
        if event:
            if event.x - self.x_lower == 0:
                self.an = 90
            else:
                self.an = math.atan((event.y - self.y_lower) / (event.x - self.x_lower))
        canv.coords(self.surface_muzzle, self.x_lower, self.y_lower,
                    self.x_lower + max(self.power, 20) * math.cos(self.an),
                    self.y_lower + max(self.power, 20) * math.sin(self.an)
                    )
        
    def game_finish (self):
        self.alive = False

    def power_up(self):
        """
            Увеличение силы выстрела
        """
        if self.readiness:
            if self.power < 70:
                self.power += 1
            canv.itemconfig(self.surface_muzzle, fill='orange')
        else:
            canv.itemconfig(self.surface_muzzle, fill='black')

    def move (self, event = 0, speed = 10):
        """
            Движение танка с помощью клавиатуры
        """
        if event:
            if event.keysym == 'Left':
                if self.x_lower >= self.foundation_size // 2:
                    canv.move(self.surface_muzzle, -speed, 0)
                    canv.move(self.surface_foundation, -speed, 0)
                    self.x_lower -= speed
            if event.keysym == 'Right':
                if self.x_lower <= screen_width - self.foundation_size // 2:
                    canv.move(self.surface_muzzle, speed, 0)
                    canv.move(self.surface_foundation, speed, 0)
                    self.x_lower += speed
            if event.keysym == 'Down':
                if self.y_lower >= self.foundation_size // 2:
                    canv.move(self.surface_muzzle, 0, speed)
                    canv.move(self.surface_foundation, 0, speed)
                    self.y_lower += speed
            if event.keysym == 'Up':
                if self.y_lower <= screen_height - self.foundation_size // 2:
                    canv.move(self.surface_muzzle, 0, -speed)
                    canv.move(self.surface_foundation, 0, -speed)
                    self.y_lower -= speed


class Bomb():

    def __init__ (self, x, r = bomb_radius, alive = True):
        """
            Конструктор класса бомб, которые сбрасывают снаряды на пушку
            size - радиус бомбы
            alive - факт жизни бомбы
            surface - поверхность, на которой рисуется бомба
        """
        self.r = r
        self.alive = alive
        self.x = x
        self.y = 2 * self.r
        self.surface = canv.create_oval(
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r,
                    fill = 'black'
                    )



class Target():

    def __init__(self, alive = 1, size_change = 'decrease'):

        """
            Конструктор класса целей

            points - количество поражённых целей
            alive - факт жизни цели (1 - цель жива, 0 - нет)
        """
        self.size_change = size_change
        self.alive = 1
        self.type = choice (['circle', 'square'])
        if self.type == 'circle':
            self.surface = canv.create_oval(0,0,0,0)
        else:
            self.surface = canv.create_rectangle(0,0,0,0)
        self.new_target()

    def new_target(self):
        """
            Инициализация новой мишени
        """
        x = self.x = rnd(400, 780)
        y = self.y = rnd(100, 550)
        r = self.r = self.initial_r = rnd(20, 50)
        vx = self.vx = rnd(5,10)
        vy = self.vy = rnd(5,10)
        color = self.color = choice(['blue', 'green', 'red', 'brown'])
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


    def hit(self):
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
            if self.y >= screen_height - self.r or self.y <= 2 * self.r:
                self.vy = -self.vy
            if self.x >= screen_width - self.r or self.x <= self.r:
                self.vx = -self.vx
                
            self.x += self.vx
            self.y += self.vy
            canv.move(self.surface, self.vx, self.vy)

            self.vy += 1

            self.set_coords()

            if self.type == 'square':
                if self.size_change == 'decrease':
                    self.r -= 1
                    if self.r <= 0:
                        self.size_change = 'increase'
                if self.size_change == 'increase':
                    self.r += 1
                    if self.r >= self.initial_r:
                        self.size_change = 'decrease'


weapon = Gun()
shells = []
points = 0
bullets = 0
canv.create_text(40, 10, text = 'points:' + str(points), font = '28')
canv.create_text(40, 30, text = 'bullets:' + str(bullets), font = '28')
time_since_beginning = 0

def print_scores():
    canv.create_rectangle(0, 0, 100, 100,
                        outline = 'white', fill = 'white')
    canv.create_text(40, 10, text = 'bullets:' + str(bullets), font = '28')
    canv.create_text(40, 30, text = 'points:' + str(points), font = '28')

def show_lose_screen():
    canv.create_rectangle(0, 0, screen_width, screen_height, fill = 'red')
    canv.create_text(screen_width // 2, screen_height // 2, text = "Never give up =)", font = '100')

def new_game(event = ''):
    global gun, target1, target2, shells, bullets, points
    global time_since_beginning
    target1 = Target()
    target2 = Target()
    target1.new_target()
    target2.new_target()
    shells = []
    time_since_beginning = 0
    canv.bind('<Button-1>', weapon.fire2_start)
    canv.bind('<ButtonRelease-1>', weapon.fire2_end)
    canv.bind('<Motion>', weapon.targetting)
    root.bind('<Key>', weapon.move)
    bomb_on_screen = False
    
    target1.alive = 1
    target2.alive = 1
    z = 0.03

    if weapon.alive:
        while target1.alive or target2.alive:
            if not weapon.alive:
                show_lose_screen()
            else:
                weapon_x = weapon.x_lower
                time_since_beginning += 1
                for b in shells:
                    b.move()
                    if b.hit_test_target(target1) and target1.alive:
                        target1.alive = 0
                        target1.hit()
                        points += 1
                        print_scores()
                        
                    if b.hit_test_target(target2) and target2.alive:
                        target2.alive = 0
                        target2.hit()
                        points += 1
                        print_scores()
                        
                if time_since_beginning % 200 == 0:
                    bomb_longevity = shell_longevity
                    bomb_on_screen = True
                    kill_bomb = Bomb (weapon_x)
                    killer_shell = Shell(weapon_x, bomb_radius)
                    killer_shell.vy = 10
                    

            if bomb_on_screen:
                if killer_shell.longevity <= 0:
                    bomb_on_screen = False
                    canv.delete(killer_shell.surface)
                    canv.delete(kill_bomb.surface)
                else:
                    killer_shell.move()
                    if killer_shell.hit_test_gun(weapon):
                        weapon.alive = False
                    
                    
            if target1.alive:
                    target1.move()
            if target2.alive:
                    target2.move()
            canv.update()
            time.sleep(z)
            weapon.targetting()
            weapon.power_up()
                
        print_scores()
        for shell in shells:
            canv.delete(shell.surface)
        canv.update()
        time.sleep(z)
        root.after(750, new_game)
        
    else:
        show_lose_screen()


new_game()
root.mainloop()
