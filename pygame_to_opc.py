import numpy
import pygame
import sys
from contained_simulation import Simulation

import opc

# Pygame setup
pygame.init()

size = width, height = 480, 480
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

simulation = Simulation()

#-------------------------------------------------------------------------------
# connect to server

IP_PORT = '127.0.0.1:7890'
client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
print

# pygame loop

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
  
  led_colors = simulation.project_to_led_strip(240)
  client.put_pixels(led_colors, channel=0)

  offset = 40
  for led_color in led_colors:
    pygame.draw.circle(screen, led_color, (offset,20), 20)
    offset += 40
  
  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
