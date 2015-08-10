import numpy
import pygame
import sys
import pymunk
import pymunk.pygame_util
from helpers.projection_helper import ProjectionHelper

class CouchBounceSimulation(object):
  def __init__(self, size):
    self.width, self.height = size

    # Physics setup
    self.space = pymunk.Space(iterations = 1)
    self.space.gravity = (0.0,  (self.height / 6 * -9.8)) # say height is 1m
    self.space.damping = 0.999 # to prevent it from blowing up.

    static_body = pymunk.Body()
    static_body.position = (self.width/2, self.height - self.height/10)

    mass = 200 #kg?
    radius = 25
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    couch_body = pymunk.Body(mass, moment)
    couch_body.position = (self.width/2, self.height - self.height/10)
    couch_body.start_position = pymunk.Vec2d(couch_body.position)
    couch_shape = pymunk.Circle(couch_body, radius)
    couch_shape.color = pygame.color.THECOLORS["white"]
    self.space.add(couch_body, couch_shape)
    
    spring = pymunk.constraint.DampedSpring(static_body, couch_body, (0,0), (0,0), 0, (4.4 * mass), 0)
    self.space.add(spring)

  def project_to_pygame_screen(self, screen):
    for c in self.space.constraints:
      pv1 = c.a.position + c.anchr1
      pv2 = c.b.position + c.anchr2
      p1 = pymunk.pygame_util.to_pygame(pv1, screen)
      p2 = pymunk.pygame_util.to_pygame(pv2, screen)
      pygame.draw.aalines(screen, pygame.color.THECOLORS["lightgray"], False, [p1,p2])
        
    for couch in self.space.shapes:
      p = pymunk.pygame_util.to_pygame(couch.body.position, screen)
      pygame.draw.circle(screen, couch.color, p, int(couch.radius), 0)

  def get_couch_force(self):
    for constraint in self.space.constraints:
      return constraint.impulse