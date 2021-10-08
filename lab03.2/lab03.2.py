import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 550))
rect(screen, (255, 255, 255), (0, 0, 400, 550))

def draw_background():
    rect(screen, (184, 197, 201), (0, 0, 400, 345))
    rect(screen, (82, 108, 113), (0, 350, 400, 200))
    rect(screen, (148, 169, 174), (5, 5, 80, 350))
    rect(screen, (148, 174, 169), (100, 15, 80, 350))
    rect(screen, (184, 201, 197), (70, 50, 80, 350))
    rect(screen, (220, 228, 227), (315, 5, 80, 350))
    rect(screen, (111, 146, 139), (290, 60, 80, 350))
    ellipse(screen, (169, 187, 187), (110, 0, 500, 50))
    ellipse(screen, (169, 187, 187), (50, 100, 300, 60))

def draw_tube(surface, x, y, width, height, color):
    
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))

def draw_downpart(surface, x, y, width, height, color):

    rect(surface, color, (x - width // 2, y - height // 2, width, height))

def draw_wheel(surface, x, y, width, height, color):

    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))

def draw_cabin(surface, x, y, width, height, color):
    rect(surface, color, (x - width // 2, y - height // 2, width, height))



def draw_glass(surface, x, y, width, height, color):
   
    rect(surface, color, (x - width // 2, y - height // 2, width, height))
    
def draw_car(surface, x, y, width, height, body_color, wheel_color, glass_color, direction='right'):
   
    if direction == 'right':
        k = 1
    else:
        k = -1
    
 
    tube_x = x - k*width * 65 // 150
    tube_y = y + height * 17.5 // 50
    tube_width = width * 20 // 150
    tube_height = height * 5 // 50
    draw_tube(surface, tube_x, tube_y, tube_width, tube_height, wheel_color)
    
    #координаты центра, ширина и высота нижней части машинки
    downpart_y = y + height * 10 // 50
    downpart_width = width * 130 // 150
    downpart_height = height * 30 // 50    
    draw_downpart(surface, x, downpart_y, downpart_width, downpart_height, body_color)
    
    #координаты центров, ширина и высота колес
    wheel_y = y + height * 25 // 50
    wheel_width = width * 30 // 150
    wheel_height = height * 25 // 50
    for wheel_x in (x - k*width * 40 // 150, x + k*width * 40 // 150):
            draw_wheel(surface, wheel_x, wheel_y, wheel_width, wheel_height, wheel_color)
    

    cabin_x = x - k*width * 20 // 150
    cabin_y = y - height * 15 // 50
    cabin_width = width * 60 // 150
    cabin_height = height * 20 // 50    
    draw_cabin(surface, cabin_x, cabin_y, cabin_width, cabin_height, body_color)


    glass_y = y - height * 12.5 // 50
    glass_width = width * 20 // 150
    glass_height = height * 15 // 50
    for glass_x in (x - k*width * 35 // 150, x - k*width * 5 // 150):
            draw_glass(surface, glass_x, glass_y, glass_width, glass_height, glass_color)


def draw_smoke():
    ellipse(screen, (108, 134, 129), (70, 450, 70, 30))
    ellipse(screen, (108, 134, 129), (50, 410, 60, 25))
    ellipse(screen, (108, 134, 129), (30, 390, 50, 20))    

draw_background()

k=200

draw_car(screen, 150 + 75 * k // 150, 450 + 25 * k // 150, k, 50 * k // 150, (0, 205, 255), (0, 0, 0), (214, 246, 255), 'right')
draw_smoke()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
