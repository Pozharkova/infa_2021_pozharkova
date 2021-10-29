from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
root.resizable(0, 0)
root.title('Игра "Пушка"')
canv = tk.Canvas(root, bg = 'white')
canv.pack(fill = tk.BOTH, expand = 1)


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
    def __init__(self, x, y):
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
        # ускорение свободного падения
        self.g = 9.8        
        # общее замедление снарядов
        self.axy = 0.5
        self.type = 'Обычный снаряд'
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

        self.vy -= self.g * 0.3
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
    def __init__(self, x, y, color):
        self.f2_power = 10
        self.lives = 10
        self.f2_on = 0
        self.an = 1
        self.x = x 
        self.y = y #координаты
        self.nx = self.x + 30
        self.ny = self.y - 30
        self.v = 0 #скорость
        self.r = 30 #длина пушки
        self.color = color
        self.id = canv.create_line(self.x, self.y, self.x + self.r, self.y - self.r, width = 7)
        self.body = canv.create_oval(self.x - 20, self.y - 5, self.x + 20, self.y + 10, fill = self.color)
        self.wheels = [canv.create_oval(self.x + i * 10 - 3, self.y, self.x + i * 10 + 3, self.y + 5, fill = self.color) for i in range(-2, 3)]

    def draw(self):
        '''
        отрисовка танка
        '''
        self.an = math.acos(((self.nx - self.x)) / math.sqrt((self.nx - self.x) ** 2 + (self.ny - self.y) ** 2))
        if self.f2_on:
            canv.itemconfig(self.id, fill = 'orange')
        else:
            canv.itemconfig(self.id, fill = 'black')
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power, self.r) * math.cos(self.an), self.y - max(self.f2_power, self.r) * math.sin(self.an))
        canv.coords(self.body, self.x - 20, self.y - 5, self.x + 20, self.y + 10)
        for i in range(-2, 3):
            canv.coords(self.wheels[i+2], self.x + i * 10 - 3, self.y, self.x + i * 10 + 3, self.y + 5)

        
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, screen1
        bullet += 1
        self.an = math.acos(((self.nx - self.x)) / math.sqrt((self.nx - self.x) ** 2 + (self.ny - self.y) ** 2))
        new_ball = ball(self.x + 50 * math.cos(self.an), self.y - 50 * math.sin(self.an))
        new_ball.r += 5
        #определение угла и скоростей выстрела

        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        ball_type = rnd(0, 3)
        if ball_type == 0:
            new_ball.g = 9.8        
            new_ball.axy = 0.5
            new_ball.type = 'Обычный снаряд'
        if ball_type == 1:
            new_ball.g = 0        
            new_ball.axy = 0.5
            new_ball.type = 'Антигравитационный снаряд'
        if ball_type == 2:
            new_ball.g = 9.8        
            new_ball.axy = 1
            new_ball.type = 'Вечный снаряд'
        if ball_type == 3:
            new_ball.g = 0        
            new_ball.axy = 1
            new_ball.type = 'Вечный антигравитационный снаряд' 
        canv.itemconfig(screen1, text=new_ball.type)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.v =  (event.x - self.x) / 20
            self.nx = event.x
            self.ny = event.y
            if abs(self.v) < 1:
                self.v = 0
            self.x += self.v
            self.draw()


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 5
            canv.itemconfig(self.id, fill = 'orange')
        else:
            canv.itemconfig(self.id, fill = 'black')
        self.draw()

    def move(self):
        """Движение. Зависит от положения мыши."""
        if abs(self.nx - self.x) > 20:
            self.x += self.v  
        self.draw()

    def hit(self):
        """Попадание цели в танк"""
        self.lives -= 1
        canv.itemconfig(lives_text1, text = 'Жизни: ' + str(self.lives))

#класс пушки-противника
class antigun(gun):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.v = -10
        self.f2_power = 100
        
    def hit(self):
        """Попадание цели в танк"""
        self.lives -= 1
        canv.itemconfig(lives_text2, text = 'Жизни: ' + str(self.lives))        
        
    def fire2_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, screen1
        #bullet += 1
        self.f2_power = 10
        self.an = math.acos(((self.nx - self.x)) / math.sqrt((self.nx - self.x) ** 2 + (self.ny - self.y) ** 2))
        new_ball = ball(self.x + 50 * math.cos(self.an), self.y - 50 * math.sin(self.an))
        new_ball.r += 5
        #определение угла и скоростей выстрела

        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        new_ball.g = 0        
        new_ball.axy = 1
        new_ball.type = 'Вечный антигравитационный снаряд'
        balls += [new_ball]


    def move(self):
        """Движение по вертикали."""
        self.y -= self.v
        if self.y < 50:
            self.y = 50
            self.v = -self.v
        if self.y > 580:
            self.fire2_end()
            self.y = 580
            self.v = -self.v
        self.draw()

    
class target():
    def __init__(self):
        self.live = 1
        self.color = 'red'
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
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill = self.color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global sum_points, points_text
        canv.coords(self.id, -10, -10, -10, -10)
        sum_points += points
        canv.itemconfig(points_text, text = 'Очки: ' + str(sum_points))

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

#цель со случайными флуктуациями скорости
class rand_target(target):
    def __init__(self):
        super().__init__()
        self.color = 'orange'
   
    def move(self):
        self.x += self.vx + rnd(-10, 10)
        self.y -= self.vy + rnd(-10, 10)
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

#падающая цель
class drop_target(target):
    def __init__(self):
        super().__init__()
        self.color = 'blue'

   
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(50, 750)
        y = self.y = rnd(50, 150)
        r = self.r = rnd(2, 50)
        self.vx = 5
        self.vy = 0
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill = self.color)     

    def move(self, gx, gr):
        if self.vx != 0:
            if self.x + self.r < gx - gr:
                self.vx = 5
            elif self.x - self.r > gx + gr:
                self.vx = -5
            else:
                self.vx = 0
                self.vy = -20
            self.x += self.vx
            if self.x - self.r <= 0:
                self.x = self.r
                self.vx = -self.vx
            if self.x + self.r >= 800:
                self.x = 800 - self.r
                self.vx = -self.vx
        else:
            self.y -= self.vy
            if self.y - self.r <= 0:
                self.y = self.r
                self.vy = -self.vy 
            if self.y + self.r >= 600:
                self.y = 600 - self.r
                self.vy = -self.vy             
        self.set_coords()  

#цель 1, цель 2
t1 = drop_target()
t2 = rand_target()
t3 = target()
#сумма очков
sum_points = 0
screen1 = canv.create_text(400, 10, text = '', font = '28')


g1 = gun(400, 400, 'red')
g2 = antigun(30, 580, 'green')

points_text = canv.create_text(40 ,10 ,text = 'Очки: ' + str(sum_points), font = '28', fill = 'red')
lives_text1 = canv.create_text(120 ,10 ,text = 'Жизни: ' + str(g1.lives), font = '28', fill = 'red')
lives_text2 = canv.create_text(120 ,30 ,text = 'Жизни: ' + str(g1.lives), font = '28', fill = 'green')

bullet = 0
balls = []


def new_game(event=''):
    global g1, g2, t1, t2, t3, screen1, balls, bullet, points_text, lives_text1, lives_text2, sum_points
    t1.new_target()
    t2.new_target()
    t3.new_target()
    
    # если шары пересекаются при создании, то их радиусы уменьшаются так, чтобы убрать пересечение
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
    t3.live = 1
    canv.itemconfig(points_text, text = 'Очки: ' + str(sum_points))
    canv.itemconfig(lives_text1, text = 'Жизни: ' + str(g1.lives))
    canv.itemconfig(lives_text2, text = 'Жизни: ' + str(g2.lives))    
    while (t1.live or t2.live or t3.live or balls) and g1.lives and g2.lives:
        if t1.live:
            t1.move(g1.x, 10)
        if t2.live:
            t2.move()
        if t3.live:
            t3.move()
        if t1.live and t2.live: #столкновение целей
            if (t1.x - t2.x) ** 2 + (t1.y - t2.y) ** 2 <= (t1.r +t2.r) ** 2:
                t1.vx = -t1.vx
                t2.vx = -t2.vx
                t1.vy = -t1.vy
                t2.vy = -t2.vy
        if t1.live and t3.live: #столкновение целей
            if (t1.x - t3.x) ** 2 + (t1.y - t3.y) ** 2 <= (t1.r +t3.r) ** 2:
                t1.vx = -t1.vx
                t3.vx = -t3.vx
                t1.vy = -t1.vy
                t3.vy = -t3.vy
        if t3.live and t2.live: #столкновение целей
            if (t3.x - t2.x) ** 2 + (t3.y - t2.y) ** 2 <= (t3.r +t2.r) ** 2:
                t3.vx = -t3.vx
                t2.vx = -t2.vx
                t3.vy = -t3.vy
                t2.vy = -t2.vy
        g1.move()
        g2.nx = g1.x
        g2.ny = g1.y
        g2.move()
        if t1.hittest(g1) and t1.live:#столкновение цели и танка игрока:
            t1.live = 0
            g1.hit()
            t1.hit(0)
        if t2.hittest(g1) and t2.live:#столкновение цели и танка игрока:
            t2.live = 0
            g1.hit()
            t2.hit(0)
        if t3.hittest(g1) and t3.live:#столкновение цели и танка игрока:
            t3.live = 0
            g1.hit()
            t3.hit(0)
        if t1.hittest(g2) and t1.live:#столкновение цели и танка противника:
            t1.live = 0
            g2.hit()
            t1.hit(0)
        if t2.hittest(g2) and t2.live:#столкновение цели и танка противника:
            t2.live = 0
            g2.hit()
            t2.hit(0)
        if t3.hittest(g2) and t3.live:#столкновение цели и танка противника:
            t3.live = 0
            g2.hit()
            t3.hit(0)
        for b in balls:
            b.move()
            if b.hittest(g1):# попадание снаряда в танк игрока
                g1.hit()
                balls.remove(b)
                canv.coords(b.id, -10, -10, -10, -10)
            if b.hittest(g2):# попадание снаряда в танк противника
                g2.hit()
                balls.remove(b)
                canv.coords(b.id, -10, -10, -10, -10)
            if b.hittest(t1) and t1.live:#если попали в первую цель
                t1.live = 0
                t1.hit(2)
                canv.itemconfig(screen1, text='Последняя цель уничтожена за ' + str(bullet) + ' ' + russian_shot(bullet))
                bullet = 0
            if b.hittest(t2) and t2.live:#если попали во вторую цель
                t2.live = 0
                t2.hit(5) #5 очков за уничтожение дерганной цели
                canv.itemconfig(screen1, text='Последняя цель уничтожена за ' + str(bullet) + ' ' + russian_shot(bullet))
                bullet = 0
            if b.hittest(t3) and t3.live:#если попали в третью цель
                t3.live = 0
                t3.hit() 
                canv.itemconfig(screen1, text='Последняя цель уничтожена за ' + str(bullet) + ' ' + russian_shot(bullet))
                bullet = 0
       
        if not t1.live and not t2.live and not t3.live:
            counter -= 1
        if counter == 0:
            for b in balls:
                canv.coords(b.id, -10, -10, -10, -10) 
            balls.clear() 
                
        canv.update() 
        time.sleep(0.03) 
        g1.targetting() 
        g1.power_up()
    if g1.lives and g2.lives:
        root.after(50, new_game) #новый цикл игры
    elif g1.lives:
        canv.itemconfig(screen1, text = 'Победил игрок')
        for b in balls:
            canv.coords(b.id, -10, -10, -10, -10) #удаление снаряда с экрана
        balls.clear() #очистка списка снарядов        
        sum_points = 0
        g1.lives = 10
        g2.lives = 10
        root.after(2500, new_game) #новый цикл игры
    else:
        canv.itemconfig(screen1, text = 'Победил противник')
        for b in balls:
            canv.coords(b.id, -10, -10, -10, -10) #удаление снаряда с экрана
        balls.clear() #очистка списка снарядов        
        sum_points = 0
        g1.lives = 10
        g2.lives = 10
        root.after(2500, new_game) #новый цикл игры
new_game()
root.mainloop()
