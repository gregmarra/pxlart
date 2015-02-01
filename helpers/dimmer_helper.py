from helpers.color_helper import ColorHelper

class DimmerHelper(object):
    @classmethod
    def dim(cls, colors, alpha):
        return [ColorHelper.proportional_mix_colors(color, (0,0,0), alpha) for color in colors]
