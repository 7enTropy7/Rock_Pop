import pymunk
import pygame
from elements import Ground, Player, Rock, Walls, Bullet, Environment

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

env = Environment(space,screen)
action = 0.5
score = 0

def coll_begin(arbiter,space,data):
    global score
    global env
    if arbiter.shapes[1].radius == 20 and arbiter.shapes[0].radius == 5: 
        score += 1
        env.rock.zindgi -= 1
        print(score)

    elif arbiter.shapes[0].radius == 20 and arbiter.shapes[1].radius == 5: 
        score += 1
        env.rock.zindgi -= 1
        print(score)

    elif arbiter.shapes[0].id == 3 and arbiter.shapes[1].id == 2:
        env.done = True
    elif arbiter.shapes[1].id == 3 and arbiter.shapes[0].id == 2:
        env.done = True


    if env.rock.zindgi == 0:
        env.done = True

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

counter = 0
while not env.done:
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

    counter += 1
    screen.fill((50,50,50))
    env.draw_env()
    env.step(action,counter%30)
    action = 0.5
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)