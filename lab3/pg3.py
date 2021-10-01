import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 500))

x1 = 100; y1 = 100
x2 = 300; y2 = 200
N = 10
color = (255, 255, 255)
rect(screen, (0, 255, 0), (0, 0, 400, 0), 500)
rect(screen, (139, 139, 100), (0, 400, 400, 0), 400)



rect(screen, (255, 250, 0), (270, 0, 0, 250),30)
rect(screen, (255, 250, 0), (350, 0, 0, 300),30)
x=339
y=400
deltax=0
deltay=0
def grib(x, y, k):
    ellipse(screen, (255, 255, 255), (x+15*k, y+10*k, 20*k, 50*k))
    ellipse(screen, (139, 139, 255), (x+15*k, y+10*k, 20*k, 50*k),int(k+0.5) )
    ellipse(screen, (255, 0, 0), (x, y, 50*k, 20*k))
    ellipse(screen, (139, 139, 255), (x, y, 50*k, 20*k),int(k+0.5) )
    ellipse(screen, (255, 255, 255), (x+10*k, y+10*k, 5*k, 2*k))
    ellipse(screen, (255, 255, 255), (x+8*k, y+6*k, 5*k, 2*k))
    ellipse(screen, (255, 255, 255), (x+20*k, y+6*k, 5*k, 2*k))
    ellipse(screen, (255, 255, 255), (x+39*k, y+5*k, 7*k, 2*k))
    ellipse(screen, (255, 255, 255), (x+30*k, y+7*k, 5*k, 2*k))
    ellipse(screen, (255, 255, 255), (x+35*k, y+10*k, 5*k, 2*k))

def igl(x, y, k, angle):
    polygon(screen, (65, 58, 58), [(x-80*k*math.sin(angle/180*math.pi), y+80*k*(1-math.cos(angle/180*math.pi))),
                                   (x+3*k*math.cos(angle/180*math.pi), y+80*k*(1-math.sin(angle/180*math.pi))),
                                   (x-10*k*math.cos(angle/180*math.pi), y+80*k*(1+math.sin(angle/180*math.pi)))])
    polygon(screen, (0, 0, 0), [(x-80*k*math.sin(angle/180*math.pi), y+80*k*(1-math.cos(angle/180*math.pi))),
                                   (x+3*k*math.cos(angle/180*math.pi), y+80*k*(1-math.sin(angle/180*math.pi))),
                                   (x-10*k*math.cos(angle/180*math.pi), y+80*k*(1+math.sin(angle/180*math.pi)))], int(k+0.5))
   


def yozh(x, y, k):
    ellipse(screen, (65, 58, 39), (x-10*k, y+50*k, 30*k, 20*k))
    ellipse(screen,(255, 255, 255) , (x-10*k, y+50*k, 30*k, 20*k), int(k+0.5))
    ellipse(screen, (65, 58, 39), (x+120*k, y+60*k, 25*k, 20*k))
    ellipse(screen,(255, 255, 255) , (x+120*k, y+60*k, 25*k, 20*k), int(k+0.5))
    ellipse(screen, (65, 58, 39), (x, y, 150*k, 90*k))
    ellipse(screen, (255, 255, 255), (x, y, 150*k, 90*k),int(k+0.5) )
    ellipse(screen, (65, 58, 39), (x+130*k, y+30*k, 60*k, 40*k))
    circle(screen, (0, 0,0), (x+150*k, y+45*k), 3*k)
    circle(screen, (255, 255,255), (x+150*k, y+45*k), 3*k, int(k+0.5))
    circle(screen, (0, 0,0), (x+165*k, y+43*k), 3*k)
    circle(screen, (255, 255,255), (x+165*k, y+43*k), 3*k, int(k+0.5))
    circle(screen, (0, 0,0), (x+190*k, y+48*k), 2*k)
    circle(screen, (255, 255,255), (x+190*k, y+48*k), 2*k, int(k+0.5))
    
    
    ellipse(screen, (255, 255, 255), (x+130*k, y+30*k, 60*k, 40*k), int(k+0.5))
    ellipse(screen, (65, 58, 39), (x+10*k, y+75*k, 30*k, 20*k))
    ellipse(screen,(255, 255, 255) , (x+10*k, y+75*k, 30*k, 20*k), int(k+0.5))
    ellipse(screen, (65, 58, 39), (x+100*k, y+75*k, 25*k, 20*k))
    ellipse(screen,(255, 255, 255) , (x+100*k, y+75*k, 25*k, 20*k), int(k+0.5))
    for i in range(1, 20, 1):
        igl(x+10*k+k*13*i/2, y-15*k+k*randint(-30, -10), k, randint(-5, 5))
    grib(x+39*k, y, 0.9*k)
    circle(screen, (255, 0, 0), (x+110*k, y+10*k), 17*k)
    circle(screen,(255, 255, 255) , (x+110*k, y+10*k), 17*k, int(0.5+k))
    circle(screen, (239, 187, 0), (x+20*k, y+20*k), 15*k)
    circle(screen, (255, 255, 255), (x+20*k, y+20*k), 15*k, int(k+0.5))
    circle(screen, (239, 187, 0), (x+27*k, y+27*k), 15*k)
    circle(screen, (255, 255, 255), (x+27*k, y+27*k), 15*k, int(k+0.5))
    for i in range(1, 10, 1):
        igl(x+10*k+k*12*i, y+k*randint(-30, 10), k, randint(-5, 5))
    

yozh(200, 300, 0.9)
yozh(140, 200, 0.6)
yozh(-40, 390, 0.7)

yozh(330, 200, 0.6)
grib(200, 450, 1)
grib(240, 490, 0.7)
grib(260, 460, 0.9)
grib(290, 495, 0.7)
grib(320, 450, 1.2)
grib(360, 480, 0.6)
grib(380, 439, 1.3)
rect(screen, (255, 250, 0), (0, 0, 0, 300), 50)
rect(screen, (255, 250, 0), (130, 0, 0, 400), 70)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
