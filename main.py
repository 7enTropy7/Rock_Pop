import pymunk
import pygame
from elements import Ground, Player, Rock, Walls

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,1000)

class Environment():
    def __init__(self):
        self.rock = Rock(1,20,space,screen)
        self.ground = Ground(1,space,screen)
        self.player = Player(1000,420,400,space,screen)
        self.walls = Walls(1,space,screen)

    def draw_env(self):
        self.rock.draw_rock()
        self.ground.draw_ground()
        self.player.draw_player()
        self.walls.draw_walls()

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