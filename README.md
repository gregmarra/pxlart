pxlart
======

Playing around with led pxl art

usage
---
- Run OPC server from where you've installed OPC: `bin/gl_server layouts/xyz.json`
- Run pxlart simulation with projections: `python pygame_to_opc.py`


libraries
---
I'm using a few other libraries to do things

### Open Pixel Control
http://openpixelcontrol.org/

OPC is a server/client library for controller LED lighting fixtures. It is used by the Fadecandy for USB control of ws281x LEDs, and offers a local visualization for testing.

`opc.py` is a python client for communicating with the server.


### pygame
http://www.pygame.org/

PyGame is a library for building games in Python. It is being used to get user input, display state information about the system, and because PyMunk integrates into it well.


### pymunk
http://www.pymunk.org/

PyMunk is a 2D python physics library. It is being used to simulate physical systems to display on the LEDs. 
