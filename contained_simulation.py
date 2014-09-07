import numpy
import pygame
import sys
import pymunk
import pymunk.pygame_util

class Simulation(object):
  def __init__(self):
    self.width = 640
    self.height = 480

    # Physics setup
    self.space = pymunk.Space(iterations = 1)
    self.space.gravity = (0.0, 0.0)
    self.space.damping = 0.999 # to prevent it from blowing up.

    static_body = pymunk.Body()
    static_body.position = (self.width/2, self.height/2)

    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    ball_body = pymunk.Body(mass, moment)
    ball_body.position = (self.width/10,self.height/2)
    ball_body.start_position = pymunk.Vec2d(ball_body.position)
    ball_shape = pymunk.Circle(ball_body, radius)
    ball_shape.color = pygame.color.THECOLORS["white"]
    self.space.add(ball_body, ball_shape)
    
    spring = pymunk.constraint.DampedSpring(static_body, ball_body, (0,0), (0,0), 0, 50, 0)
    self.space.add(spring)

  def project_to_pygame_screen(self, screen):
    for c in self.space.constraints:
      pv1 = c.a.position + c.anchr1
      pv2 = c.b.position + c.anchr2
      p1 = pymunk.pygame_util.to_pygame(pv1, screen)
      p2 = pymunk.pygame_util.to_pygame(pv2, screen)
      pygame.draw.aalines(screen, pygame.color.THECOLORS["lightgray"], False, [p1,p2])
        
    for ball in self.space.shapes:
      p = pymunk.pygame_util.to_pygame(ball.body.position, screen)
      pygame.draw.circle(screen, ball.color, p, int(ball.radius), 0)

  def project_to_led_strip(self, n_leds):
    pxl_ranges = [((i * self.width/n_leds), ((i+1) * self.width/n_leds)) for i in range(n_leds)]

    for ball in self.space.shapes:
      ball_left = ball.body.position.x - (self.width/n_leds) / 2
      ball_right = ball.body.position.x + (self.width/n_leds) / 2
      pct_overlaps = [self.interval_overlap_pct((pxl_range), (ball_left,ball_right)) for pxl_range in pxl_ranges]

      pxl_colors = [(255*pct_overlap,255*pct_overlap,255*pct_overlap) for pct_overlap in pct_overlaps]

    return pxl_colors

  def interval_overlap_pct(self,a,b):
    """return pct interval overlap as a pct of the first interval"""
    a = [float(n) for n in a]
    a.sort()

    b = [float(n) for n in b]
    b.sort()

    left1, right1 = a
    left2, right2 = b

    # no overlap
    if right2 < left1:
      return 0

    if left2 > right1:
      return 0

    # 2nd interval is contained or same width
    if (left2 >= left1) and (right2 <= right1):
      return (right2 - left2) / (right1 - left1)

    # half overlap over left edge of 1st interval
    if (left2 <= left1) and (right2 <= right1):
      return abs((right2 - left1) / (right1 - left1))

    # half overlap over right edge of 1st interval
    if (left2 >= left1) and (right2 >= right1):
      return abs((right1 - left2) / (right1 - left1))

    # 2nd interval spans
    return 1
