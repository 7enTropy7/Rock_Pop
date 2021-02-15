import pymunk
import pygame
from elements import Ground, Player, Rock, Walls, Bullet

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

class Environment():
    def __init__(self):
        self.rock = Rock(100,20,space,screen)
        self.ground = Ground(1,space,screen)
        self.player = Player(2000,500,720,space,screen)
        self.walls = Walls(1,space,screen)

    def draw_env(self):
        self.rock.draw_rock()
        self.ground.draw_ground()
        self.player.draw_player()
        self.player.draw_bullets()
        self.walls.draw_walls()

    def step(self,action):
        if action == 1:
            self.player.triangle_body.velocity = 1000,0
        elif action == 0:
            self.player.triangle_body.velocity = -1000,0
        elif action == 2:
            self.player.bullets.append(Bullet(self.player.triangle_body.position[0],self.player.triangle_body.position[1],space,screen))
        else:
            self.player.triangle_body.velocity = 0,0
        self.player.remove_bullet()

env = Environment()
action = 0.5
score = 0

def coll_begin(arbiter,space,data):
    global score
    global env
    # print(arbiter.shapes)
    if arbiter.shapes[1].radius == 20 and arbiter.shapes[0].radius == 5: 
        score += 1
        print(score)

    elif arbiter.shapes[0].radius == 20 and arbiter.shapes[1].radius == 5: 
        score += 1
        print(score)

    return True

def coll_post(arbiter,space,data):
    #print('post solve')
    if arbiter.shapes[1].radius == 20 and arbiter.shapes[0].radius == 5: 
        for b in range(len(env.player.bullets)):
            if int(env.player.bullets[b].b_circle_shape.body.velocity[0]) != 0:
                space.remove(arbiter.shapes[0].body,arbiter.shapes[0])
                env.player.bullets.pop(b)
                break

    elif arbiter.shapes[0].radius == 20 and arbiter.shapes[1].radius == 5: 
        for b in range(len(env.player.bullets)):
            if int(env.player.bullets[b].b_circle_shape.body.velocity[0]) != 0:
                space.remove(arbiter.shapes[1].body,arbiter.shapes[1])
                env.player.bullets.pop(b)
                break


handler = space.add_default_collision_handler()
handler.begin = coll_begin
handler.post_solve = coll_post


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 0
            if event.key == pygame.K_RIGHT:
                action = 1
            if event.key == pygame.K_SPACE:
                action = 2

    screen.fill((50,50,50))
    env.draw_env()
    env.step(action)
    action = 0.5
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)