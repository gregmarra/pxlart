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

    PASTEL_RAINBOW = [
        "F7977A",
        "F9AD81",
        "FDC68A",
        "FFF79A",
        "C4DF9B",
        "A2D39C",
        "82CA9D",
        "7BCDC8",
        "6ECFF6",
        "7EA7D8",
        "8493CA",
        "8882BE",
        "A187BE",
        "BC8DBF",
        "F49AC2",
        "F6989D"
    ]

    @classmethod
    def colors(self, pallette):
        return [tuple(ord(c) for c in rgbstr.decode('hex')) for rgbstr in pallette]