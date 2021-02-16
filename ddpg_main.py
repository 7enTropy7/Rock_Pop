import pymunk
import pygame
from elements import Ground, Player, Rock, Walls, Bullet, Environment


pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

def coll_begin(arbiter,space,data):
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


env = Environment(space,screen)

#  agent = Agent(input_dims=env.observation_space.shape, env=env, n_actions=env.action_space.shape[0])

n_games = 250
best_score = float('-inf')
score_history = []
load_checkpoint = False

for i in range(n_games):
    observation = env.reset()
    env.done = False
    score = 0
    while not env.done:
        action = agent.choose_action(observation, evaluate)
        observation_, reward, done, info = env.step(action) # counter 
        score += reward
        agent.remember(observation, action, reward, observation_, done)
        if not load_checkpoint:
            agent.learn()
        observation = observation_

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