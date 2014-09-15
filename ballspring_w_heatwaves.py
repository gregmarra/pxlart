import numpy
import pygame
import sys

from filters.fader import FaderFilter
from simulations.ball_spring_simulation import BallSpringSimulation

import opc

# Pygame setup
pygame.init()

N_LEDS = 240
size = width, height = N_LEDS * 2, N_LEDS * 2
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

simulation = BallSpringSimulation(size)

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

fader_filter = FaderFilter(clock, N_LEDS)

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

  fader_filter.stimulate(simulation.project_to_intensity_list(N_LEDS))

  def proportional_mix_colors(a, b, a_share):
    return (
      proportional_mix(a[0], b[0], a_share),
      proportional_mix(a[1], b[1], a_share),
      proportional_mix(a[2], b[2], a_share),
      )

  def proportional_mix(a, b, a_share):
    return a * a_share + b * (1 - a_share)

  def color_from_excitement(excitement, color_pallette):
    for x in range(0, len(color_pallette) - 1):
      width = 1.0 / len(color_pallette)
      upper_bound = (x+1) * width
      if (excitement < upper_bound):
        pct_of_range = (excitement - (x * width)) / width
        return proportional_mix_colors(color_pallette[x], color_pallette[x+1], 1 - pct_of_range)
    return proportional_mix_colors(color_pallette[-1], color_pallette[-1], 1)

  color_pallette = [
    pygame.color.THECOLORS["black"],
    pygame.color.THECOLORS["red"],
    pygame.color.THECOLORS["orange"],
    pygame.color.THECOLORS["yellow"],
    pygame.color.THECOLORS["white"]
  ]
  led_colors = [color_from_excitement(excitement, color_pallette) for excitement in fader_filter.excitements]

  client.put_pixels(led_colors, channel=0)

  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
