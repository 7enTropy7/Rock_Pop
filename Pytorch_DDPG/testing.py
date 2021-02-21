import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import random
import pymunk
import pygame
from elements_rl import Ground, Player, Rock, Walls, Bullet, Environment

from agent import DDPG_Agent

def coll_begin(arbiter,space,data):
    global env
    if arbiter.shapes[1].id == 2 and arbiter.shapes[0].id == 1:
        env.rock.hit_by_bullet = True
        env.rock.zindgi -= 1

    if arbiter.shapes[0].id == 2 and arbiter.shapes[1].id == 1:
        env.rock.hit_by_bullet = True
        env.rock.zindgi -= 1

    if arbiter.shapes[0].id == 3 and arbiter.shapes[1].id == 2:
        env.done = True
        env.player.collided = True
        env.reward = -10

    if arbiter.shapes[1].id == 3 and arbiter.shapes[0].id == 2:
        env.done = True
        env.player.collided = True
        env.reward = -10

    
    # if arbiter.shapes[0].id == 3 and  (arbiter.shapes[1].id == 5 or arbiter.shapes[1].id == 6):
    #     env.reward = -1 
    # if arbiter.shapes[1].id == 3 and  (arbiter.shapes[0].id == 5 or arbiter.shapes[0].id == 6):
    #     env.reward = -1 
    
    if env.rock.zindgi == 0:
        env.done = True
        env.reward = 10

    return True

def coll_post(arbiter,space,data):
    #print('post solve')
    global env
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

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

env = Environment(space,screen)

agent = DDPG_Agent(state_space_size=3,action_space_size=1,random_seed=10)

agent.actor_local.load_state_dict(torch.load('actor_checkpoint.pth'))
agent.critic_local.load_state_dict(torch.load('critic_checkpoint.pth'))

handler = space.add_default_collision_handler()
handler.begin = coll_begin
handler.post_solve = coll_post

while True:
    state = env.reset()
    agent.reset()   
    c = 0
    while True:
        screen.fill((50,50,50))
        action = agent.current_action(state)
        next_state, reward, done = env.step(action,c)
        state = next_state
        if done:
            break
        c += 1
        space.step(1/50)
        clock.tick(120)
        pygame.display.update()
