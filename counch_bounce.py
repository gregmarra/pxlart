import numpy
import pygame
import sys

from filters.fader import FaderFilter
from helpers.color_helper import ColorHelper
from helpers.dimmer_helper import DimmerHelper
from simulations.couch_bounce_simulation import CouchBounceSimulation

import opc

# Pygame setup
pygame.init()

N_LEDS = 240
size = width, height = N_LEDS * 2, N_LEDS * 2
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

simulation = CouchBounceSimulation(size)

# connect to OPC server

IP_PORT = '127.0.0.1:7890'
client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
print

# pygame loop

fader_filter = FaderFilter(N_LEDS)
min_couch_position = 0
max_couch_position = 0

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  
  ### Update physics
  fps = 50
  iterations = 25
  dt = 1.0/float(fps)/float(iterations)
  for x in range(iterations): # 10 iterations to get a more stable simulation
      simulation.space.step(dt)

  ### Clear screen
  screen.fill(pygame.color.THECOLORS["black"])

  simulation.project_to_pygame_screen(screen)

  couch = simulation.get_couch()
  min_couch_position = min(min_couch_position, couch.position[1])
  max_couch_position = max(max_couch_position, couch.position[1])

  dim = 1 - (couch.position[1] - min_couch_position) / (max_couch_position - min_couch_position)

  led_colors = [ColorHelper.rainbow(float(a)/256, index, 128) for index, a in enumerate(range(N_LEDS))]
  led_colors = DimmerHelper.dim(led_colors, dim)

  client.put_pixels(led_colors, channel=0)

  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
