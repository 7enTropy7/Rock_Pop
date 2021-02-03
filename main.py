import pymunk
import pygame
from elements import Basket,Ball,Ground

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,1000)

class Environment():
    def __init__(self):
        self.ball = Ball(1,30,space,screen)
        self.ground = Ground(1,space,screen)
        self.basket = Basket(1,300,space,screen)

    def draw_env(self):
        self.ball.draw_ball()
        self.ground.draw_ground()
        self.basket.draw_hoop()

    def reset():
        pass

    def step():
        pass

    def calculate_reward():
        pass

    def update():
        pass

    def get_state():
        pass

env = Environment()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

    screen.fill((50,50,50))
    env.draw_env()
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)