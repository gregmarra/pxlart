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

  def color_from_excitement(excitement):
    color0 = pygame.color.THECOLORS["black"]
    color1 = pygame.color.THECOLORS["red"]
    color2 = pygame.color.THECOLORS["yellow"]
    color3 = pygame.color.THECOLORS["white"]
    if (excitement < 0.25):
      share = 1 - (excitement / 0.25)
      return proportional_mix_colors(color0, color1, share)
    elif (excitement < 0.5):
      share = 1 - ((excitement - 0.25) / 0.25)
      return  proportional_mix_colors(color1, color2, share)
    elif (excitement < 0.75):
      share = 1 - ((excitement - 0.5) / 0.25)
      return proportional_mix_colors(color2, color3, share)
    else:
      share = 1 - ((excitement - 0.75) / 0.25)
      return proportional_mix_colors(color3, color3, share)

  led_colors = [color_from_excitement(excitement) for excitement in fader_filter.excitements]

  client.put_pixels(led_colors, channel=0)

  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
