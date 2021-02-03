import pygame
import pymunk

def create_ball(space):
    mass = 1
    radius = 30
    circle_moment = pymunk.moment_for_circle(mass,0,radius)
    circle_body = pymunk.Body(mass,circle_moment)
    circle_body.position = 0,0
    circle_shape = pymunk.Circle(circle_body,radius)
    circle_shape.body.velocity = (400,0)
    circle_shape.elasticity = 0.8
    space.add(circle_body, circle_shape)
    return circle_shape

def draw_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen,(0,0,0),(pos_x,pos_y),30)

def static_ground(space):
    mass = 1
    segment_moment = pymunk.moment_for_segment(mass,(0,750),(1000,750),2) #end points and thickness
    segment_body = pymunk.Body(mass,segment_moment,pymunk.Body.STATIC)
    segment_body.position = 0,0
    segment_shape = pymunk.Segment(segment_body,(0,750),(1000,750),2)
    segment_shape.elasticity = 1
    space.add(segment_body,segment_shape)
    return segment_shape

def draw_static_ground():
    pygame.draw.rect(screen, (0,0,200), pygame.Rect(0, 750, 1000, 0),2)

def hoop(space,hoop_height):
    mass = 1
    segment1_moment = pymunk.moment_for_segment(mass,(950,hoop_height),(1000,hoop_height),2) #end points and thickness
    segment1_body = pymunk.Body(mass,segment1_moment,pymunk.Body.KINEMATIC)
    segment1_body.position = 0,0
    segment1_shape = pymunk.Segment(segment1_body,(950,hoop_height),(1000,hoop_height),2)
    segment1_shape.elasticity = 1

    segment2_moment = pymunk.moment_for_segment(mass,(1000,hoop_height-50),(1000,hoop_height),2) #end points and thickness
    segment2_body = pymunk.Body(mass,segment2_moment,pymunk.Body.KINEMATIC)
    segment2_body.position = 0,0
    segment2_shape = pymunk.Segment(segment2_body,(1000,hoop_height-50),(1000,hoop_height),2)
    segment2_shape.elasticity = 1

    space.add(segment1_body,segment1_shape,segment2_body,segment2_shape)
    return segment1_shape, segment2_shape

def draw_hoop(hoop_height):
    pygame.draw.rect(screen, (0,200,0), pygame.Rect(950, hoop_height, 50, 0),2)
    pygame.draw.rect(screen, (0,200,0), pygame.Rect(1000, hoop_height-50, 0, 50),2)


pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,1000)

hoop_height = 550

balls = []
balls.append(create_ball(space))
ground = static_ground(space)
hoop = hoop(space,hoop_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()
            sys.exit()
    
    screen.fill((50,50,50))
    draw_ball(balls)
    draw_static_ground()
    draw_hoop(hoop_height)
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)