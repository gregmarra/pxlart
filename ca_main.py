import numpy
import pygame
import sys
import time

from helpers.color_helper import ColorHelper
from helpers.sixty_to_sixty_four_helper import SixtyToSixtyFourHelper
from simulations.ca import CASimulation

import opc

N_LEDS = 240
simulation = CASimulation(30, N_LEDS)
simulation.start_single()

### interesting rules
# 18 is sort of random
# 30 serpinski triangle

# connect to OPC server

IP_PORT = '127.0.0.1:7890'
client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
print

# loop

while True:
  color_pallette = [
    pygame.color.THECOLORS["black"],
    pygame.color.THECOLORS["red"],
    pygame.color.THECOLORS["orange"],
    pygame.color.THECOLORS["yellow"],
    pygame.color.THECOLORS["white"]
  ]
  led_colors = [ColorHelper.color_from_intensity(excitement, color_pallette) for excitement in simulation.array]


  client.put_pixels(SixtyToSixtyFourHelper.transform(led_colors), channel=0)

  time.sleep(.1)
  simulation.step()
