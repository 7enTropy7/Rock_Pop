import pymunk
import pygame
from elements_rl import Ground, Player, Rock, Walls, Bullet, Environment
import numpy as np
from ddpg_tf2 import Agent
from utils import plot_learning_curve


def coll_begin(arbiter,space,data):
    global env
    if arbiter.shapes[1].radius == 20 and arbiter.shapes[0].radius == 5: 
        env.reward += 5
        env.rock.zindgi -= 1

    elif arbiter.shapes[0].radius == 20 and arbiter.shapes[1].radius == 5: 
        env.reward += 5
        env.rock.zindgi -= 1

    elif arbiter.shapes[0].id == 3 and arbiter.shapes[1].id == 2:
        env.done = True
        env.player.collided = True
        env.reward -= 5

    elif arbiter.shapes[1].id == 3 and arbiter.shapes[0].id == 2:
        env.done = True
        env.player.collided = True
        env.reward -= 5

    if env.rock.zindgi == 0:
        env.done = True
        env.reward += 10

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

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

env = Environment(space,screen)
agent = Agent(input_dims=((3,)), env=env, n_actions=1)
n_games = 100

figure_file = 'plots/rock_pop.png'

best_score = float('-inf')
score_history = []
load_checkpoint = False

handler = space.add_default_collision_handler()
handler.begin = coll_begin
handler.post_solve = coll_post

# counter = 0

if load_checkpoint:
    n_steps = 0
    c = 0
    while n_steps <= agent.batch_size:
        observation = env.reset()
        action = np.array([np.random.uniform(-1,1)])
        observation_, reward, done = env.step(action,c%3)
        agent.remember(observation, action, reward, observation_, done)
        n_steps += 1
        c += 1
    agent.learn()
    agent.load_models()
    evaluate = True
else:
    evaluate = False

for i in range(n_games):
    counter = 0
    observation = env.reset()
    done = False
    score = 0
    while not done:
        action = agent.choose_action(observation, evaluate)
        observation_, reward, done = env.step(action,counter%3)
        score += reward
        agent.remember(observation, action, reward, observation_, done)
        if not load_checkpoint:
            agent.learn()
        observation = observation_

        counter += 1
        screen.fill((50,50,50))
        space.step(1/50)
        pygame.display.update()
        clock.tick(120)
        print(score)
        # print(reward)
    score_history.append(score)
    avg_score = np.mean(score_history[-100:])

    if avg_score > best_score:
        best_score = avg_score
        if not load_checkpoint:
            agent.save_models()

    print('episode ', i, 'score %.1f' % score, 'avg score %.1f' % avg_score)

if not load_checkpoint:
    x = [i+1 for i in range(n_games)]
    plot_learning_curve(x, score_history, figure_file)