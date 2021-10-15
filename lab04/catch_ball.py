import pygame
from pygame.draw import *
from random import randint
from math import cos, sin
from os import path

pygame.init()
# частота обновления
FPS = 50
# параметры игрового окна
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# шрифт для вывода очков
score_font = pygame.font.Font(None, 36)
# максимально возможное количество фигур на экране
max_figure = 10
# массивы координат, скоростей, радиусов, типов и цветов фигур
x = [0] * max_figure
y = [0] * max_figure
dx = [0] * max_figure
dy = [0] * max_figure
figure_type = [0] * max_figure
r = [0] * max_figure
figure_color = [0] * max_figure
# текущее количество шариков на экране
figure_count = 0
# очки
score = 0
# очки за особую фигуру
spec_score = 10
# имя игрока
player_name = ''
# цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_figure():
    '''создает новую фигуру '''
    global x, y, dx, dy, r, figure_color, figure_type, figure_count
    if figure_count < max_figure:
        x[figure_count] = randint(100, screen_width - 100)
        y[figure_count] = randint(100,screen_height - 100)
        dx[figure_count] = randint(-5, 5)
        dy[figure_count] = randint(-5, 5)
        # соотношение вероятностей появления шарика и фигуры особого типа 4:1
        i = randint(0, 5)
        if i > 0:
            figure_type[figure_count] = 0
            r[figure_count] = randint(30,50)
        else:
            figure_type[figure_count] = 1
            r[figure_count] = randint(50,75)
        figure_color[figure_count] = randint(0, 5)
        figure_count += 1

def move_figures():
    '''сдвигает фигуры'''
    global x, y, dx, dy, r
    for i in range(0, figure_count):
        x[i] += dx[i]
        y[i] += dy[i]
        if x[i] - r[i] < 0:
            x[i] = r[i]
            dx[i] = - dx[i]
            dy[i] = randint(-5, 5) 
        if x[i] + r[i] > screen_width:
            x[i] = screen_width - r[i]
            dx[i] = - dx[i]
            dy[i] = randint(-5, 5)           
        if y[i] - r[i] < 0:
            y[i] = r[i]
            dy[i] = - dy[i]
            dx[i] = randint(-5, 5)
        if y[i] + r[i] > screen_height:
            y[i] = screen_height - r[i]
            dy[i] = - dy[i]
            dx[i] = randint(-5, 5)    

def draw_cross(x, y, width, angle, color):
    '''рисует крестообразный зрачок'''
    # преобразование градусов в радианы
    angle = angle * 3.14 / 180
    # угол 90 градусов для поворота второй палки креста
    a90 = 3.14/2
    line(screen, color, [x - (width * cos(angle)) // 2, y - (width * sin(angle)) // 2], [x + (width * cos(angle)) // 2, y + (width * sin(angle)) // 2])
    line(screen, color, [x - (width * cos(angle + a90)) // 2, y - (width * sin(angle + a90)) // 2], [x + (width * cos(angle + a90)) // 2, y + (width * sin(angle + a90)) // 2])
    
def draw_cat(x, y, width, color):
    '''рисует кота Шрёдингера'''
    # ящик
    rect(screen, color, (x - width // 2, y - width // 2, width, width), 1)
    # морда
    ellipse(screen, color, (x - width // 2, y - width // 6,  width, 2 * width // 3))
    # уши
    line(screen, color, [x - width // 2 + 5, y], [x - width // 2 + 10, y - width // 4])
    line(screen, color, [x - width // 4, y - width // 8], [x - width // 2 + 10, y - width // 4])
    line(screen, color, [x + width // 2 - 5, y + width // 6], [x + width // 2 - 15, y - width // 5])
    line(screen, color, [x + width // 4, y - width // 8], [x + width // 2 - 15, y - width // 5])
    # глаза
    circle(screen, BLACK, (x - width // 5 + randint(-5, 5), y - width // 8 + width // 6 + randint(-5, 5)), randint(5, 10))
    circle(screen, BLACK, (x + width // 5 + randint(0, 5), y - width // 8 + width // 6 + randint(0, 5)), randint(10, 15))
    # зрачки
    circle(screen, color, (x - width // 5 + randint(-2, 2), y - width // 8 + width // 6 + randint(-2, 2)), randint(1, 3))
    draw_cross(x + width // 5 + randint(-2, 2), y - width // 8 + width // 6, randint(10, 15), randint(0, 90), color)
    #нос
    circle(screen, BLACK, (x, y + width // 6), 5)
    # рот
    ellipse(screen, BLACK, (x - width // 3, y + width // 5,  2 * width // 3, width // 5))
    # зубы
    for i in range(x - width // 3 + 5, x + width // 3, 5):
        line(screen, color, [i, y + width // 5], [i, y + 2 * width // 5])
    # надпись
    cat_font = pygame.font.Font(None, width // 6)
    cat_text = cat_font.render('Кот Шрёдингера', True, color)
    screen.blit(cat_text,(x - width // 2 + 3, y - width // 2 + 3))   

def draw_figures():
    '''рисует фигуры'''
    for i in range(0, figure_count):
        if figure_type[i] == 0:
            circle(screen, COLORS[figure_color[i]], (x[i], y[i]), r[i])
        else:
            draw_cat(x[i], y[i], 2 * r[i], COLORS[figure_color[i]])

def destroy_figure(num):
    '''уничтожает фигуру'''
    global x, y, dx, dy, r, figure_color, figure_type, figure_count
    for i in range(num, figure_count - 1): # смещение вышележащих элементов массивов на один шаг вниз
        x[i] = x[i + 1]
        y[i] = y[i + 1]
        dx[i] = dx[i + 1]
        dy[i] = dy[i + 1]
        r[i] = r[i + 1]
        figure_type[i] = figure_type[i + 1]
        figure_color[i] = figure_color[i + 1]
    figure_count -= 1
        

def click(event):
    '''оценивает попадание по фигуре'''
    global score
    i = 0
    while i < figure_count:
        if figure_type[i] == 0:
            if (event.pos[0] - x[i]) ** 2 + (event.pos[1] - y[i]) ** 2 <= r[i] ** 2: # проверка попадания в круг (шарик)
                score += 1
                destroy_figure(i)
                i -= 1
        else:
            if abs(event.pos[0] - x[i]) <= r[i] and abs(event.pos[1] - y[i]) <= r[i]: # проверка попадания в квадрат (ящик)
                score += spec_score * (-1, 1)[randint(0, 1)] #случайным образом выбираем множитель -1 или +1
                destroy_figure(i)
                i -= 1
        i += 1
    if score < 0: 
        score = 0

def draw_score():
    '''выводит очки с именем игрока на экран'''
    score_text = score_font.render(player_name + ': ' + str(score), True, WHITE)
    screen.blit(score_text,(10,10))
    
def draw_score_table(score_table):
    '''выводит таблицу лучших результатов на экран'''
    i = 0
    if len(score_table) > 0:
        # вывод шапки таблицы
        scores_text = score_font.render('Лучшие результаты:', True, WHITE)
        screen.blit(scores_text,(10, 10))
        # вывод лучшей десятки
        while i <= 10 and i < len(score_table):
            scores_text = score_font.render(' '.join(score_table[i]), True, WHITE)
            screen.blit(scores_text,(10, 40 + i * 40))
            i += 1    

def draw_player_name():
    '''выводит форму ввода имени игрока'''
    player_text = score_font.render('Введите имя игрока:' + player_name, True, WHITE)
    screen.blit(player_text, (10, 460))

def read_scores(line):
    '''считывает имена игроков и результаты'''
    name, res = line.split('\t')
    res = res[:-1]
    return name, res
    
    
pygame.display.update()
# считывание результатов игроков
if path.exists('scores.txt'): #если файл с результатами существует
    f = open('scores.txt', 'r')
    score_table = [read_scores(line) for line in f]
    f.close()
    
else:
    score_table = [] # пустой список

clock = pygame.time.Clock()
finished = False
# цикл ввода имени игрока
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        # считывание нажатой клавиши
        elif event.type == pygame.KEYDOWN:
            # если Enter, то окончание цикла ввода
            if event.key == pygame.K_RETURN:
                finished = True
            # если Backspace, то удаляется последний символ
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            # добавление введенного символа к имени игрока
            else:
                player_name += event.unicode

    # вывод таблицы лучших результатов
    draw_score_table(score_table)
    # вывод текущей формы ввода имени
    draw_player_name()
    pygame.display.update()
    screen.fill(BLACK)
if player_name == '':
    player_name = 'Ленивый енот'

finished = False
# основной игровой цикл
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    new_figure()
    move_figures()
    draw_figures()
    draw_score()
    pygame.display.update()
    screen.fill(BLACK)

score_table.append((player_name, str(score)))
score_table = sorted(score_table, key = lambda elem: int(elem[1]), reverse = True)
# Запись 
f = open('scores.txt', 'w')
for s in score_table:
    f.write('\t'.join(s)+'\n')   
f.close()
pygame.quit()
