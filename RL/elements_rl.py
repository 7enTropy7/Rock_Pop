import pymunk
import pygame
import numpy as np 

class Environment():
    def __init__(self,space,screen):
        self.rock = Rock(100,20,space,screen)
        self.ground = Ground(1,space,screen)
        self.player = Player(2000,500,720,space,screen)
        self.walls = Walls(1,space,screen)
        self.done = False
        self.reward = 0
        self.space = space
        self.screen = screen

    def get_state(self):
        return np.array([int(self.player.triangle_body.position[0]), int(self.rock.circle_body.position[0]), int(self.rock.circle_body.position[1])])

    def reset(self):
        self.space.remove(self.rock.circle_shape,self.rock.circle_body)
        self.space.remove(self.player.triangle_shape,self.player.triangle_body)
        self.rock = Rock(100,20,self.space,self.screen)
        self.player = Player(2000,500,720,self.space,self.screen)
        observation = self.get_state()
        self.done = False
        self.reward = 0
        return observation

    def draw_env(self):
        self.rock.draw_rock()
        self.ground.draw_ground()
        self.player.draw_player()
        self.player.draw_bullets()
        self.walls.draw_walls()

    def step(self,action,shoot):
        self.player.triangle_body.velocity = 1000*action[0],0
        if shoot == 0:
            self.player.bullets.append(Bullet(self.player.triangle_body.position[0],self.player.triangle_body.position[1],self.space,self.screen))
        self.player.remove_bullet()
        self.draw_env()
        observation_ = self.get_state()
        if self.player.collided == False:
            self.reward -= 0.01
        done = self.done
        return observation_, self.reward, done



class Bullet():
    def __init__(self,x,y,space,screen):
        self.b_mass = 0.001
        self.b_radius = 5
        self.screen = screen
        self.b_elasticity = 1.0
        self.b_circle_moment = pymunk.moment_for_circle(self.b_mass,0,self.b_radius)
        self.b_circle_body = pymunk.Body(self.b_mass,self.b_circle_moment,pymunk.Body.DYNAMIC)
        self.b_circle_body.position = x,y
        self.b_circle_shape = pymunk.Circle(self.b_circle_body,self.b_radius)
        self.b_circle_shape.body.velocity = (0,-500)
        self.b_circle_shape.elasticity = self.b_elasticity
        self.b_circle_shape.id = 1
        self.collided = False

        self.space = space
        self.space.add(self.b_circle_body, self.b_circle_shape)

    def draw_bullet(self):
        pos_x = int(self.b_circle_body.position.x)
        pos_y = int(self.b_circle_body.position.y)
    
        pygame.draw.circle(self.screen,(200,0,0),(pos_x,pos_y),self.b_radius)


class Rock():
    def __init__(self,mass,radius,space,screen):
        self.mass = mass
        self.radius  = radius
        self.elasticity = 1.0
        self.screen = screen
        self.circle_moment = pymunk.moment_for_circle(self.mass,0,self.radius)
        self.circle_body = pymunk.Body(self.mass,self.circle_moment)
        self.circle_body.position = 0,10
        self.circle_shape = pymunk.Circle(self.circle_body,self.radius)
        self.circle_shape.body.velocity = (100,0)
        self.circle_shape.elasticity = self.elasticity
        self.circle_shape.id = 2
        self.zindgi = 5

        space.add(self.circle_body, self.circle_shape)
        
    def draw_rock(self):
        pos_x = int(self.circle_body.position.x)
        pos_y = int(self.circle_body.position.y)
        pygame.draw.circle(self.screen,(0,0,0),(pos_x,pos_y),30)


class Player():
    def __init__(self,mass,x,y,space,screen):
        self.mass = mass
        self.screen = screen
        self.triangle_shape = pymunk.Poly(None,((0, -25), (-25, 25), (25, 25)))
        self.triangle_moment = pymunk.moment_for_poly(mass,self.triangle_shape.get_vertices())
        self.triangle_body = pymunk.Body(mass,self.triangle_moment,pymunk.Body.KINEMATIC)
        self.triangle_body.position = x,y
        self.triangle_body.velocity = 0,0
        self.triangle_shape.body = self.triangle_body       
        self.triangle_shape.body.angle = 0.0
        self.triangle_shape.id = 3
        self.collided = False

        self.space = space
        self.space.add(self.triangle_body,self.triangle_shape)

        self.bullets = []

    def remove_bullet(self):
        for b in range(len(self.bullets)):
            if int(self.bullets[b].b_circle_body.position.y)<=0:
                self.space.remove(self.bullets[b].b_circle_body,self.bullets[b].b_circle_shape)
                self.bullets.pop(b)
                break
    
    def draw_bullets(self):    
        for bullet in self.bullets:
            bullet.draw_bullet()
    
    def draw_player(self):
        if self.triangle_body.position[0] >= 970:
             self.triangle_body.position = 970,720
        elif self.triangle_body.position[0] <= 30:
             self.triangle_body.position = 30,720
        
        vertices = []
        for v in self.triangle_shape.get_vertices():
            x,y = v.rotated(self.triangle_shape.body.angle) + self.triangle_shape.body.position
            vertices.append((int(x),int(y)))
        pygame.draw.polygon(self.screen,(0,200,0),(vertices))

class Ground():
    def __init__(self,mass,space,screen):
        self.mass = mass
        self.screen = screen
        self.segment_moment = pymunk.moment_for_segment(self.mass,(0,750),(1000,750),2) #end points and thickness
        self.segment_body = pymunk.Body(self.mass,self.segment_moment,pymunk.Body.STATIC)
        self.segment_body.position = 0,0
        self.segment_shape = pymunk.Segment(self.segment_body,(0,750),(1000,750),2)
        self.segment_shape.elasticity = 1
        self.segment_shape.id = 4

        space.add(self.segment_body,self.segment_shape)

    def draw_ground(self):
        pygame.draw.rect(self.screen, (0,0,200), pygame.Rect(0, 750, 1000, 0),2)

class Walls():
    def __init__(self,mass,space,screen):
        self.mass = mass
        self.screen = screen
        self.segment1_moment = pymunk.moment_for_segment(mass,(0,0),(0,800),2) #end points and thickness
        self.segment1_body = pymunk.Body(self.mass,self.segment1_moment,pymunk.Body.STATIC)
        self.segment1_body.position = 0,0
        self.segment1_shape = pymunk.Segment(self.segment1_body,(0,0),(0,800),2)
        self.segment1_shape.elasticity = 1
        self.segment2_moment = pymunk.moment_for_segment(self.mass,(1000,0),(1000,800),2) #end points and thickness
        self.segment2_body = pymunk.Body(self.mass,self.segment2_moment,pymunk.Body.STATIC)
        self.segment2_body.position = 0,0
        self.segment2_shape = pymunk.Segment(self.segment2_body,(1000,0),(1000,800),2)
        self.segment2_shape.elasticity = 1
        self.segment1_shape.id = 5
        self.segment2_shape.id = 6

        space.add(self.segment1_body,self.segment1_shape,self.segment2_body,self.segment2_shape)

    def draw_walls(self):
        pygame.draw.rect(self.screen, (0,200,0), pygame.Rect(0, 0, 0, 800),2)
        pygame.draw.rect(self.screen, (0,200,0), pygame.Rect(1000, 0, 0, 800),2)