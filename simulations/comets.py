import numpy
import pygame
import sys
import pymunk
import pymunk.pygame_util
from helpers.projection_helper import ProjectionHelper

class CometsSimulation(object):
  """Comets as added as masses on springs that get pulled from off-screen right to off-screen left."""

  def __init__(self, size):
    self.width, self.height = size

    # Physics setup
    self.space = pymunk.Space(iterations = 1)
    self.space.gravity = (0.0, 0.0)
    self.space.damping = 0.999 # to prevent it from blowing up.
    self.space.add_collision_handler(0, 1, begin=self.removeComet)

    self.static_body = pymunk.Body()
    self.static_body.position = (self.width/2, self.height/2)

    left_laser_body = pymunk.Body()
    left_laser_body.position = (-self.width/4, self.height/2)

    left_laser_forcefield = pymunk.Segment(left_laser_body, (0,0), (0,self.height), 1)
    left_laser_forcefield.color = pygame.color.THECOLORS["blue"]
    left_laser_forcefield.collision_type = 0
    self.space.add(left_laser_forcefield)

    self.addComet()

  def addComet(self):

    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    comet_body = pymunk.Body(mass, moment)
    comet_body.position = (self.width * 2,self.height/2)
    comet_body.start_position = pymunk.Vec2d(comet_body.position)
    comet_shape = pymunk.Circle(comet_body, radius)
    comet_shape.color = pygame.color.THECOLORS["white"]
    comet_shape.collision_type = 1
    self.space.add(comet_body, comet_shape)
    
    spring_strength = numpy.random.rand() * 50
    spring = pymunk.constraint.DampedSpring(self.static_body, comet_body, (0,0), (0,0), 0, spring_strength, 0)
    self.space.add(spring)

  def removeComet(self, space, arbiter):
    comet = arbiter.shapes[1]
    for constraint in comet.body.constraints:
      self.space.remove(constraint)
    self.space.remove(comet, comet.body)
    return True

  def project_to_pygame_screen(self, screen):
    for c in self.space.constraints:
      pv1 = c.a.position + c.anchr1
      pv2 = c.b.position + c.anchr2
      p1 = pymunk.pygame_util.to_pygame(pv1, screen)
      p2 = pymunk.pygame_util.to_pygame(pv2, screen)
      pygame.draw.aalines(screen, pygame.color.THECOLORS["lightgray"], False, [p1,p2])
        
    for comet in self.space.shapes:
      p = pymunk.pygame_util.to_pygame(comet.body.position, screen)
      pygame.draw.circle(screen, comet.color, p, int(comet.radius), 0)

  def project_to_intensity_list(self, n_leds):
    pxl_ranges = [((i * self.width/n_leds), ((i+1) * self.width/n_leds)) for i in range(n_leds)]
    COMET_WIDTH = 8

    pct_overlaps = [0 for a in range(n_leds)]
    for comet in self.space.shapes:
      comet_left = comet.body.position.x - (self.width/n_leds) * COMET_WIDTH
      comet_right = comet.body.position.x + (self.width/n_leds) * COMET_WIDTH
      comet_pct_overlaps = [ProjectionHelper.interval_overlap_pct((pxl_range), (comet_left,comet_right)) for pxl_range in pxl_ranges]
      pct_overlaps = [a+b for a,b in zip(pct_overlaps, comet_pct_overlaps)]

    pct_overlaps = [min(a, 1) for a in pct_overlaps]

    return pct_overlaps

  def project_to_led_strip(self, n_leds):
    pxl_colors = [(255*intensity,255*intensity,255*intensity) for intensity in self.project_to_intensity_list(n_leds)]

    return pxl_colors

