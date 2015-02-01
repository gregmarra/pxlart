import pygame

class ColorPallette(object):
    FIRE = [
        "000000",
        "FF0000",
        "FF6666",
        "FFAAAA",
        "FFFFFF"
    ]

    WATER = [
        "000000",
        "1693A5",
        "45B5C4",
        "7ECECA",
        "A0DED6",
        "C7EDE8",
        "FFFFFF"
    ]

    @classmethod
    def colors(self, pallette):
        return [tuple(ord(c) for c in rgbstr.decode('hex')) for rgbstr in pallette]