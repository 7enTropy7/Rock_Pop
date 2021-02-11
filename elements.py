import pymunk
import pygame
        
class Bullet():
    def __init__(self,x,y,space,screen):
        self.b_mass = 1
        self.b_radius = 5
        self.screen = screen
        self.b_elasticity = 1.0
        self.b_circle_moment = pymunk.moment_for_circle(self.b_mass,0,self.b_radius)
        self.b_circle_body = pymunk.Body(self.b_mass,self.b_circle_moment,pymunk.Body.KINEMATIC)
        self.b_circle_body.position = x,y
        self.b_circle_shape = pymunk.Circle(self.b_circle_body,self.b_radius)
        self.b_circle_shape.body.velocity = (0,-20)
        self.b_circle_shape.elasticity = self.b_elasticity
        
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
        self.circle_shape.body.velocity = (400,0)
        self.circle_shape.elasticity = self.elasticity
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

        self.space = space
        self.space.add(self.triangle_body,self.triangle_shape)

        self.bullets = []

    def shoot_bullet(self):
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
        print(vertices)
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
        space.add(self.segment1_body,self.segment1_shape,self.segment2_body,self.segment2_shape)

    def draw_walls(self):
        pygame.draw.rect(self.screen, (0,200,0), pygame.Rect(0, 0, 0, 800),2)
        pygame.draw.rect(self.screen, (0,200,0), pygame.Rect(1000, 0, 0, 800),2)