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
        self.player = Player(2000,500,720,space,screen)
        self.walls = Walls(1,space,screen)

    def draw_env(self):
        self.rock.draw_rock()
        self.ground.draw_ground()
        self.player.draw_player()
        self.walls.draw_walls()

    def step(self,action):
        if action == 1:
            self.player.triangle_body.velocity = 200,0
        elif action == 0:
            self.player.triangle_body.velocity = -200,0
        else:
            self.player.triangle_body.velocity = 0,0
            

env = Environment()
action = 0.5
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 0
            if event.key == pygame.K_RIGHT:
                action = 1

    screen.fill((50,50,50))
    env.draw_env()
    env.step(action)
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)