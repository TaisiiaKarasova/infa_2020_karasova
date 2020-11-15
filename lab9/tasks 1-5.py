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
bomb_radius = 40
shells = []
bullets = 0
weapon1_x = 20
weapon2_x = screen_width - weapon1_x
weapon1_y = 450
weapon2_y = weapon1_y
muzzle_size = 20

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
        if dist_object_shell <= self.r + obj.foundation_size // 2:
            return True
        else:
            return False


class Gun():
    def __init__(self,
                 x_lower_edge, y_lower_edge,
                 muzzle_size,
                 foundation_size = 30, foundation_color = 'yellow',
                 power = 10, readiness = 0, an = 1,
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
        self.x_upper = x_lower_edge + muzzle_size
        self.y_upper = y_lower_edge - muzzle_size
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
            if event.y <= self.y_lower:
                    self.an = - math.pi/2
            else:
                    self.an = math.pi/2
        else:
                angle_tan = (event.y - self.y_lower) / (event.x - self.x_lower)
                if (angle_tan) >= 0:
                    self.an = math.atan(angle_tan)
                else:
                    self.an = math.atan(angle_tan) + math.pi
                    
        new_shell.vx = -self.power * math.cos(self.an)
        new_shell.vy = -self.power * math.sin(self.an)
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
                if event.y < self.y_lower:
                    self.an = - math.pi/2
                else:
                    self.an = math.pi/2
            else:
                angle_tan = (event.y - self.y_lower) / (event.x - self.x_lower)
                if (angle_tan) >= 0:
                    self.an = math.atan(angle_tan)
                else:
                    self.an = math.atan(angle_tan) + math.pi
        canv.coords(self.surface_muzzle, self.x_lower, self.y_lower,
                    self.x_lower - max(self.power, 20) * math.cos(self.an),
                    self.y_lower - max(self.power, 20) * math.sin(self.an)
                    )
        

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

    def move_left (self, event = 0, speed = 10):
        """
            Движение танка влево с помощью стрелки на клавиатуре
        """
        if event:
            if self.x_lower >= self.foundation_size // 2:
                canv.move(self.surface_muzzle, -speed, 0)
                canv.move(self.surface_foundation, -speed, 0)
                self.x_lower -= speed

                    
    def move_right (self, event = 0, speed = 10):
        """
            Движение танка вправо с помощью стрелки на клавиатуре
        """
        if event:
            if self.x_lower <= screen_width - self.foundation_size // 2:
                canv.move(self.surface_muzzle, speed, 0)
                canv.move(self.surface_foundation, speed, 0)
                self.x_lower += speed

                    
    def move_down (self, event = 0, speed = 10):
        """
            Движение танка вниз с помощью стрелки на клавиатуре
        """
        if event:
            if self.y_lower >= self.foundation_size // 2:
                canv.move(self.surface_muzzle, 0, speed)
                canv.move(self.surface_foundation, 0, speed)
                self.y_lower += speed

                    
    def move_up (self, event = 0, speed = 10):
        """
            Движение танка вверх с помощью стрелки на клавиатуре
        """
        if event:
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
                        

def print_scores():
    canv.create_rectangle(0, 0, 100, 100,
                        outline = 'white', fill = 'white')
    canv.create_text(40, 10, text = 'bullets:' + str(bullets), font = '28')
    canv.create_text(40, 30, text = 'points:' + str(points), font = '28')


def show_end_screen(winner):
    canv.create_rectangle(0, 0, screen_width, screen_height, fill = 'red')
    canv.create_text(screen_width // 2, screen_height // 2, text = winner + ' player won!', font = '100')




weapon1 = Gun(weapon1_x, weapon1_y, muzzle_size)
weapon2 = Gun(weapon2_x, weapon2_y, muzzle_size)
shells = []
points = 0
bullets = 0
canv.create_text(40, 10, text = 'points:' + str(points), font = '28')
canv.create_text(40, 30, text = 'bullets:' + str(bullets), font = '28')
time_since_beginning = 0

def set_buttons_events ():
    canv.bind('<Button-1>', weapon1.fire2_start)
    canv.bind('<ButtonRelease-1>', weapon1.fire2_end)
    
    canv.bind('<Button-3>', weapon2.fire2_start)
    canv.bind('<ButtonRelease-3>', weapon2.fire2_end)
    
    canv.bind('<Motion>', weapon1.targetting)
    canv.bind('<B2-Motion>', weapon2.targetting)
    
    root.bind('<Up>', weapon1.move_up)
    root.bind('<Down>', weapon1.move_down)
    root.bind('<Right>', weapon1.move_right)
    root.bind('<Left>', weapon1.move_left)

    root.bind('u', weapon2.move_up)
    root.bind('d', weapon2.move_down)
    root.bind('r', weapon2.move_right)
    root.bind('l', weapon2.move_left)

def killed_target (target):
    global points
    target.alive = 0
    target.hit()
    points += 1
    print_scores()

    
def new_game(event = ''):
    global gun, target1, target2, shells, bullets, points
    global time_since_beginning
    target1 = Target()
    target2 = Target()
    target1.new_target()
    target2.new_target()
    shells = []
    time_since_beginning = 0
    bomb_on_screen = False
    set_buttons_events()
    
    target1.alive = 1
    target2.alive = 1
    z = 0.03

    if weapon1.alive and weapon2.alive:
        while target1.alive or target2.alive:
            if not weapon1.alive:
                show_end_screen('left')
            elif not weapon2.alive:
                show_end_screen('right')
            else:
                time_since_beginning += 1
                for b in shells:
                    b.move()
                    if b.hit_test_target(target1) and target1.alive:
                        killed_target (target1)
                        
                    if b.hit_test_target(target2) and target2.alive:
                        killed_target (target2)

                    if b.hit_test_gun(weapon1) and weapon1.alive:
                        weapon1.alive = False
                        
                    if b.hit_test_gun(weapon2) and weapon2.alive:
                        weapon2.alive = False
                        
                if time_since_beginning % 400 == 0:
                    bomb_on_screen = True
                    kill_bomb = Bomb (weapon1.x_lower)
                    killer_shell = Shell(weapon1.x_lower, bomb_radius)
                    killer_shell.vy = 10

                if (time_since_beginning - 200) % 400 == 0:
                    bomb_on_screen = True
                    kill_bomb = Bomb (weapon2.x_lower)
                    killer_shell = Shell(weapon2.x_lower, bomb_radius)
                    killer_shell.vy = 5

            if bomb_on_screen:
                if killer_shell.longevity <= 0:
                    bomb_on_screen = False
                    canv.delete(killer_shell.surface)
                    canv.delete(kill_bomb.surface)
                else:
                    killer_shell.move()
                    if killer_shell.hit_test_gun(weapon1):
                        weapon1.alive = False
                    if killer_shell.hit_test_gun(weapon2):
                        weapon2.alive = False                    
                    
            if target1.alive:
                    target1.move()
            if target2.alive:
                    target2.move()
                    
            canv.update()
            time.sleep(z)
            weapon1.targetting()
            weapon1.power_up()
            weapon2.power_up()
            weapon2.targetting()
                
        print_scores()
        for shell in shells:
            canv.delete(shell.surface)
        canv.update()
        time.sleep(z)
        root.after(750, new_game)
        
    elif not weapon2.alive:
        show_end_screen('right')
    else:
        show_end_screen('left')


new_game()
root.mainloop()
