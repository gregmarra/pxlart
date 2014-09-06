import collections
import numpy
import pygame
import sys
import time

N_LEDS = 20

pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)

colors = collections.deque([(0,0,0) for a in range(N_LEDS)])

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  colors.append([numpy.floor(n * 255) for n in numpy.random.rand(3)])
  colors.popleft()

  offset = 10
  for color in colors:
    pygame.draw.circle(screen, color, (offset,10), 5)
    offset += 20

  pygame.display.flip()
  time.sleep(0.1)
