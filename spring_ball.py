import numpy
import pygame
import sys
import pymunk
import pymunk.pygame_util

# Pygame setup
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

# Physics setup
space = pymunk.Space(iterations = 1)
space.gravity = (0.0, 0.0)
space.damping = 0.999 # to prevent it from blowing up.

static_body = pymunk.Body()
static_body.position = (width/2, height/2)

mass = 10
radius = 25
moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
ball_body = pymunk.Body(mass, moment)
ball_body.position = (width/10,height/2)
ball_body.start_position = pymunk.Vec2d(ball_body.position)
ball_shape = pymunk.Circle(ball_body, radius)
ball_shape.color = pygame.color.THECOLORS["white"]
space.add(ball_body, ball_shape)
spring = pymunk.constraint.DampedSpring(static_body, ball_body, (0,0), (0,0), 0, 50, 0)
space.add(spring)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  
  ### Update physics
  fps = 50
  iterations = 25
  dt = 1.0/float(fps)/float(iterations)
  for x in range(iterations): # 10 iterations to get a more stable simulation
      space.step(dt)

  ### Clear screen
  screen.fill(pygame.color.THECOLORS["black"])

  ### Draw stuff
  for c in space.constraints:
    pv1 = c.a.position + c.anchr1
    pv2 = c.b.position + c.anchr2
    p1 = pymunk.pygame_util.to_pygame(pv1, screen)
    p2 = pymunk.pygame_util.to_pygame(pv2, screen)
    pygame.draw.aalines(screen, pygame.color.THECOLORS["lightgray"], False, [p1,p2])
      
  for ball in space.shapes:
    p = pymunk.pygame_util.to_pygame(ball.body.position, screen)
    pygame.draw.circle(screen, ball.color, p, int(ball.radius), 0)
  
  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
