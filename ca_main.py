import numpy
import sys
import time

from filters.fader import FaderFilter
from helpers.color_helper import ColorHelper
from helpers.color_pallette import ColorPallette
from helpers.sixty_to_sixty_four_helper import SixtyToSixtyFourHelper
from simulations.ca import CASimulation

import opc

N_LEDS = 240
simulation = CASimulation(18, N_LEDS)
simulation.start_random()

### interesting rules
# 30 is sort of random, breaks as things stack up in a 101010101 pattern
# 18 serpinski triangle

# connect to OPC server
IP_PORT = '127.0.0.1:7890'
client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT

fader_filter = FaderFilter(N_LEDS, 0.6)
color_pallette = ColorPallette.colors(ColorPallette.WATER)

while True:
  fader_filter.stimulate(simulation.array)
  
  led_colors = [ColorHelper.color_from_intensity(excitement, color_pallette) for excitement in fader_filter.excitements]
  client.put_pixels(SixtyToSixtyFourHelper.transform(led_colors), channel=0)

  time.sleep(.2)
  simulation.step()
