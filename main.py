import pymunk
import pygame

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,1000)

class Ball():
    def __init__(self,mass,radius):
        self.mass = mass
        self.radius  = radius
        self.elasticity = 0.8
        self.circle_moment = pymunk.moment_for_circle(self.mass,0,self.radius)
        self.circle_body = pymunk.Body(self.mass,self.circle_moment)
        self.circle_body.position = 0,0
        self.circle_shape = pymunk.Circle(self.circle_body,self.radius)
        self.circle_shape.body.velocity = (400,0)
        self.circle_shape.elasticity = self.elasticity
        space.add(self.circle_body, self.circle_shape)
        
    def draw_ball(self):
        pos_x = int(self.circle_body.position.x)
        pos_y = int(self.circle_body.position.y)
        pygame.draw.circle(screen,(0,0,0),(pos_x,pos_y),30)

class Ground():
    def __init__(self,mass):
        self.mass = mass
        self.segment_moment = pymunk.moment_for_segment(self.mass,(0,750),(1000,750),2) #end points and thickness
        self.segment_body = pymunk.Body(self.mass,self.segment_moment,pymunk.Body.STATIC)
        self.segment_body.position = 0,0
        self.segment_shape = pymunk.Segment(self.segment_body,(0,750),(1000,750),2)
        self.segment_shape.elasticity = 1
        space.add(self.segment_body,self.segment_shape)

    def draw_ground(self):
        pygame.draw.rect(screen, (0,0,200), pygame.Rect(0, 750, 1000, 0),2)

class Basket():
    def __init__(self,mass,height):
        self.mass = mass
        self.hoop_height = height
        self.segment1_moment = pymunk.moment_for_segment(mass,(950,self.hoop_height),(1000,self.hoop_height),2) #end points and thickness
        self.segment1_body = pymunk.Body(self.mass,self.segment1_moment,pymunk.Body.KINEMATIC)
        self.segment1_body.position = 0,0
        self.segment1_shape = pymunk.Segment(self.segment1_body,(950,self.hoop_height),(1000,self.hoop_height),2)
        self.segment1_shape.elasticity = 1
        self.segment2_moment = pymunk.moment_for_segment(self.mass,(1000,self.hoop_height-50),(1000,self.hoop_height),2) #end points and thickness
        self.segment2_body = pymunk.Body(self.mass,self.segment2_moment,pymunk.Body.KINEMATIC)
        self.segment2_body.position = 0,0
        self.segment2_shape = pymunk.Segment(self.segment2_body,(1000,self.hoop_height-50),(1000,self.hoop_height),2)
        self.segment2_shape.elasticity = 1
        space.add(self.segment1_body,self.segment1_shape,self.segment2_body,self.segment2_shape)

    def draw_hoop(self):
        pygame.draw.rect(screen, (0,200,0), pygame.Rect(950, self.hoop_height, 50, 0),2)
        pygame.draw.rect(screen, (0,200,0), pygame.Rect(1000, self.hoop_height-50, 0, 50),2)


ball = Ball(1,30)
ground = Ground(1)
basket = Basket(1,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

    screen.fill((50,50,50))
    ball.draw_ball()
    ground.draw_ground()
    basket.draw_hoop()
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)