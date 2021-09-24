import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
polygon(screen, (255, 255, 255), [(0,0), (0,400),
                              (400,0), (400,400)])
polygon(screen, (255, 255, 255), [(0,0), (400,0),
                              (0,400), (400,400)])

circle(screen, (255, 255, 0), (200, 175), 50)
circle(screen, (0, 0, 0), (200, 175), 50, 1)
circle(screen, (255, 0, 0), (175, 175), 15)
circle(screen, (255, 0, 0), (225, 175), 15)
circle(screen, (0, 0, 0), (175, 175), 5)
circle(screen, (0, 0, 0), (225, 175), 5)
line(screen, (0, 0, 0), (200, 160), (250, 100),5)
line(screen, (0, 0, 0), (200, 150), (175, 100),5)
line(screen, (0, 0, 0), (170, 205), (230, 205),5)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
