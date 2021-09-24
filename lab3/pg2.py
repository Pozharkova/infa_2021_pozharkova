import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 500))

x1 = 100; y1 = 100
x2 = 300; y2 = 200
N = 10
color = (255, 255, 255)
rect(screen, (0, 255, 0), (0, 0, 400, 0), 500)
rect(screen, (139, 139, 100), (0, 400, 400, 0), 400)

rect(screen, (255, 250, 0), (0, 0, 0, 300), 50)
rect(screen, (255, 250, 0), (130, 0, 0, 400), 70)
rect(screen, (255, 250, 0), (270, 0, 0, 250),30)
rect(screen, (255, 250, 0), (350, 0, 0, 300),30)
x=339
y=400
deltax=0
deltay=0
circle(screen, (100, 0, 0), (300, 395), 50)
circle(screen, (250, 250, 250), (300, 395), 50, 2)
circle(screen, (100, 0, 0), (350, 385), 20)
circle(screen, (250, 250, 250), (350, 385), 20, 2)
circle(screen, (0, 0, 0), (345, 385), 2)
circle(screen, (0, 0, 0), (350, 380), 2)
circle(screen, (0, 0, 0), (360, 390), 2)
circle(screen, (100, 0, 0), (340, 410), 10)
circle(screen, (100, 0, 0), (345, 430), 10)
circle(screen, (100, 0, 0), (260, 430), 10)
circle(screen, (100, 0, 0), (250, 400), 10)
for i in range(N**2+2*N):
    polygon(screen, (139, 39, 139), [(x,y), (x+1+deltax,y+deltay),
                               (x-9, y+10), (x,y-100)])
    polygon(screen, (0, 0, 0), [(x,y), (x+1+deltax,y+deltay),
                               (x-9,y+10), (x,y-100)], 2)
    x=randint(260, 330)
    y=randint(380,420)
    deltax=randint(-5, 5)
    deltax=randint(-5, 5)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
