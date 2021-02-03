import pymunk
import pygame
from elements import Basket,Ball,Ground

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,1000)

ball = Ball(1,30,space,screen)
ground = Ground(1,space,screen)
basket = Basket(1,300,space,screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

    screen.fill((50,50,50))
    ball.draw_ball()
    ground.draw_ground()
    basket.draw_hoop()
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)