import numpy

class ColorHelper(object):
  @classmethod
  def proportional_mix_colors(cls, a, b, a_share):
    return (
      cls.proportional_mix(a[0], b[0], a_share),
      cls.proportional_mix(a[1], b[1], a_share),
      cls.proportional_mix(a[2], b[2], a_share),
      )

  @classmethod
  def proportional_mix(cls, a, b, a_share):
    return a * a_share + b * (1 - a_share)

  @classmethod
  def color_from_intensity(cls, intensity, color_pallette):
    for x in range(0, len(color_pallette) - 1):
      width = 1.0 / len(color_pallette)
      upper_bound = (x+1) * width
      if (intensity < upper_bound):
        pct_of_range = (intensity - (x * width)) / width
        return cls.proportional_mix_colors(color_pallette[x], color_pallette[x+1], 1 - pct_of_range)
    return cls.proportional_mix_colors(color_pallette[-1], color_pallette[-1], 1)

  @classmethod
  def rainbow(cls, intensity, n, cycle_size, phase=0):
    center = 128;
    width = 127;
    frequency = numpy.pi*2/cycle_size;
    color = (
      numpy.sin(frequency*n+2+phase) * width + center,
      numpy.sin(frequency*n+0+phase) * width + center,
      numpy.sin(frequency*n+4+phase) * width + center,
    )
    return cls.proportional_mix_colors(color, (0,0,0), intensity)
