class ProjectionHelper(object):

  @classmethod
  def interval_overlap_pct(self,a,b):
    """return pct interval overlap as a pct of the first interval"""
    a = [float(n) for n in a]
    a.sort()

    b = [float(n) for n in b]
    b.sort()

    left1, right1 = a
    left2, right2 = b

    # no overlap
    if right2 < left1:
      return 0

    if left2 > right1:
      return 0

    # 2nd interval is contained or same width
    if (left2 >= left1) and (right2 <= right1):
      return (right2 - left2) / (right1 - left1)

    # half overlap over left edge of 1st interval
    if (left2 <= left1) and (right2 <= right1):
      return abs((right2 - left1) / (right1 - left1))

    # half overlap over right edge of 1st interval
    if (left2 >= left1) and (right2 >= right1):
      return abs((right1 - left2) / (right1 - left1))

    # 2nd interval spans
    return 1
