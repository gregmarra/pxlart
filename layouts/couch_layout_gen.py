### NOTE NEED TO MANUALLY DELETE COMMA AFTER LAST POINT

LEDS_PER_METER = 30.0
# Dimensions from http://www.ikea.com/us/en/catalog/products/S99932597/
COUCH_WIDTH = 2.18
COUCH_DEPTH = 0.88

def layout_leds(width, depth, leds_per_meter):
  led_coordinates = []
  direction = ""
  next_direction = "east"

  x = -width/2
  y = -depth/2

  # Go east
  while True:
    if direction == "east":
      x = x + 1/LEDS_PER_METER
      if x > width/2:
        remainder = (x - width/2)
        x = width/2
        y = y + remainder
        next_direction = "north"
    if direction == "north":
      y = y + 1/LEDS_PER_METER
      if y > depth/2:
        remainder = (y - depth/2)
        y = depth/2
        x = x - remainder
        next_direction = "west"
    if direction == "west":
      x = x - 1/LEDS_PER_METER
      if x < -depth/2:
        remainder = (-depth/2) - x
        x = -depth/2
        y = y - remainder
        next_direction = "south"
    if direction == "south":
      y = y - 1/LEDS_PER_METER
      if y < -depth/2:
        break

    direction = next_direction
    led_coordinates.append((x, y))

  return led_coordinates

def print_coordinates(led_coordinates):
  print "["
  for x, y in led_coordinates:
    print "{\"point\": [%5.3f, %5.3f, %5.3f]}," % (x, y, 0)
  print "]"

def main():
  print_coordinates(layout_leds(COUCH_WIDTH, COUCH_DEPTH, LEDS_PER_METER))

if __name__ == "__main__":
  main()
