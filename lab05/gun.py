from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg = 'white')
canv.pack(fill = tk.BOTH, expand = 1)
# ускорение свободного падения
g = 9.8

# окончание выстрелов в заисимости от количества
def russian_shot(shot_count):
    if shot_count > 4 and shot_count < 21:
        return 'выстрелов'        
    else:
        if shot_count % 10 == 1:
            return 'выстрел'
        elif shot_count % 10 < 5 and shot_count % 10 > 0:
            return 'выстрела'
        else:
            return 'выстрелов'

class ball():
    def __init__(self, x = 40, y = 450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали 
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        # общее замедление снарядов
        self.axy = 0.5        
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill = self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXED
        self.x += self.vx
        self.y -= self.vy
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx *= -self.axy
            self.vy *= self.axy 
        if self.x + self.r >= 800:
            self.x = 800 - self.r
            self.vx *= -self.axy
            self.vy *= self.axy 
        if self.y - self.r <= 0:
            self.y = self.r
            self.vx *= self.axy
            self.vy *= -self.axy 
        if self.y + self.r >= 600:
            self.y = 600 - self.r
            self.vx *= self.axy
            self.vy *= -self.axy 

        self.vy -= g * 0.3
        self.set_coords()


    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXED
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width = 7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill = 'orange')
        else:
            canv.itemconfig(self.id, fill = 'black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill = 'orange')
        else:
            canv.itemconfig(self.id, fill = 'black')


class target():
    def __init__(self):
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить цель по прошествии единицы времени.
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
        if self.x + self.r >= 800:
            self.x = 800 - self.r
            self.vx = -self.vx
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy 
        if self.y + self.r >= 600:
            self.y = 600 - self.r
            self.vy = -self.vy 
        self.set_coords()
    
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(50, 750)
        y = self.y = rnd(50, 550)
        r = self.r = rnd(2, 50)
        self.vx = rnd(1, 10)
        self.vy = rnd(1, 10)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill = color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global sum_points, points_text
        canv.coords(self.id, -10, -10, -10, -10)
        sum_points += points
        canv.itemconfig(points_text, text = sum_points)


#цель 1, цель 2
t1 = target()
t2 = target()
#сумма очков
sum_points = 0
screen1 = canv.create_text(400, 10, text = '', font = '28')
points_text = canv.create_text(30 ,10 ,text = sum_points, font = '28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, t1, t2, screen1, balls, bullet
    t1.new_target()
    t2.new_target()
    if (t1.x - t2.x) ** 2 + (t1.y - t2.y) ** 2 <= (t1.r +t2.r) ** 2:
        t1.r = t2.r = max(abs(t1.x - t2.x) // 2 - 1, abs(t1.y - t2.y) // 2 - 1, 1)
    
    #счетчик паузы перед появлением новых целей    
    counter = 50
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    t1.live = 1
    t2.live = 1
    while t1.live or t2.live or balls:
        if t1.live:
            t1.move()
        if t2.live:
            t2.move()
        if t1.live and t2.live: #столкновение целей
            if (t1.x - t2.x) ** 2 + (t1.y - t2.y) ** 2 <= (t1.r +t2.r) ** 2:
                t1.vx = -t1.vx
                t2.vx = -t2.vx
                t1.vy = -t1.vy
                t2.vy = -t2.vy
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:#если попали в первую цель
                t1.live = 0
                t1.hit()
                canv.itemconfig(screen1, text='Последняя цель уничтожена за ' + str(bullet) + ' ' + russian_shot(bullet))
                bullet = 0
            if b.hittest(t2) and t2.live:#если попали во вторую цель
                t2.live = 0
                t2.hit()
                canv.itemconfig(screen1, text='Последняя цель уничтожена за ' + str(bullet) + ' ' + russian_shot(bullet))
                bullet = 0
            if not t1.live and not t2.live:
                counter -= 1
        
        if counter == 0:
            for b in balls:
                canv.coords(b.id, -10, -10, -10, -10) #удаление снаряда с экрана
            balls.clear() #отчистка списка снарядов
                
        canv.update() #обновление игрового поля
        time.sleep(0.03) #пауза
        g1.targetting() 
        g1.power_up()

    canv.delete(gun) 
    root.after(750, new_game) #новый цикл игры

new_game()
root.mainloop()
