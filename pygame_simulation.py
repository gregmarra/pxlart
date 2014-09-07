import numpy
import pygame
import sys
from contained_simulation import Simulation

# Pygame setup
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

simulation = Simulation()

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
  
  led_colors = simulation.project_to_led_strip(10)

  offset = 40
  for led_color in led_colors:
    pygame.draw.circle(screen, led_color, (offset,20), 20)
    offset += 40
  
  screen.blit(font.render("fps: " + str(clock.get_fps()), 1, pygame.color.THECOLORS["white"]), (0,0))
  
  pygame.display.flip()
  clock.tick(fps)
