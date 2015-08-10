import numpy
import sys
import time

from filters.fader import FaderFilter
from helpers.color_helper import ColorHelper
from helpers.color_pallette import ColorPallette
from helpers.dimmer_helper import DimmerHelper
from helpers.sixty_to_sixty_four_helper import SixtyToSixtyFourHelper

import opc

N_LEDS = 240

# connect to OPC server
IP_PORT = '127.0.0.1:7890'
client = opc.Client(IP_PORT)
if client.can_connect():
  print '    connected to %s' % IP_PORT
else:
  # can't connect, but keep running in case the server appears later
  print '    WARNING: could not connect to %s' % IP_PORT


while True:
  led_colors = [ColorHelper.rainbow(float(a)/256, index, 128) for index, a in enumerate(range(N_LEDS))]

  client.put_pixels(SixtyToSixtyFourHelper.transform(led_colors), channel=0)

  time.sleep(.2)
  